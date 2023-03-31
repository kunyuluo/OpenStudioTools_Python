import openstudio
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.SetpointManagers import SetpointManager
from Resources.Helpers import Helper


class HVACTool:

    @staticmethod
    def plant_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fluid_type: int = 1,
            max_loop_temp=None,
            min_loop_temp=None,
            max_loop_flow_rate=None,
            min_loop_flow_rate=None,
            plant_loop_volume=None,
            load_distribution_scheme: int = 1,
            common_pipe_simulation: int = 1,
            supply_branches=None,
            demand_branches=None,
            setpoint_manager: openstudio.openstudiomodel.SetpointManager = None,
            setpoint_manager_secondary: openstudio.openstudiomodel.SetpointManager = None):

        """
        -Fluid_type:
            1:Water 2:Steam 3:PropyleneGlycol 4:EthyleneGlycol \n

        -Load_distribution_scheme:
            1:Optimal 2:SequentialLoad 3:UniformLoad 4:UniformPLR 5:SequentialUniformPLR \n

        -Common_pipe_simulation:
            1:None \n
            2:CommonPipe (for secondary pump system.
            Typically, constant pump on primary side and variable speed pump on secondary side)\n
            3:TwoWayCommonPipe (for thermal energy storage system, with temperature control for
            both primary and secondary sides)
        """

        fluid_types = {1: "Water", 2: "Steam", 3: "PropyleneGlycol", 4: "EthyleneGlycol"}
        load_distribution_schemes = {1: "Optimal", 2: "SequentialLoad", 3: "UniformLoad",
                                     4: "UniformPLR", 5: "SequentialUniformPLR"}
        common_pipe_types = {1: "None", 2: "CommonPipe", 3: "TwoWayCommonPipe"}

        plant = openstudio.openstudiomodel.PlantLoop(model)

        if name is not None:
            plant.setName(name)
        if fluid_type != 1:
            plant.setFluidType(fluid_types[fluid_type])
        if max_loop_temp is not None:
            plant.setMaximumLoopTemperature(max_loop_temp)
        if min_loop_temp is not None:
            plant.setMinimumLoopTemperature(min_loop_temp)

        if max_loop_flow_rate is not None:
            plant.setMaximumLoopFlowRate(max_loop_flow_rate)
        else:
            plant.autosizeMaximumLoopFlowRate()

        if min_loop_flow_rate is not None:
            plant.setMinimumLoopFlowRate(min_loop_flow_rate)

        if plant_loop_volume is not None:
            plant.setPlantLoopVolume(plant_loop_volume)
        else:
            plant.autocalculatePlantLoopVolume()

        if load_distribution_scheme != 1:
            plant.setLoadDistributionScheme(load_distribution_schemes[load_distribution_scheme])

        if common_pipe_simulation != 1:
            plant.setCommonPipeSimulation(common_pipe_types[common_pipe_simulation])

        # Add supply branches to the loop:
        if isinstance(supply_branches, list):
            if len(supply_branches) != 0:
                # for multiple branches (2-d list)
                if isinstance(supply_branches[0], list) and isinstance(supply_branches[-1], list):
                    for branch in supply_branches:
                        plant.addSupplyBranchForComponent(branch.pop(-1))
                        node = plant.supplyMixer().inletModelObjects()[-1].to_Node().get()
                        for item in branch:
                            item.addToNode(node)
                # for single branch (1-d list)
                else:
                    plant.addSupplyBranchForComponent(supply_branches.pop(-1))
                    node = plant.supplyMixer().inletModelObjects()[-1].to_Node().get()
                    for item in supply_branches:
                        item.addToNode(node)
            else:
                raise ValueError("supply_branches cannot be empty")
        else:
            raise TypeError("Invalid input format of supply_branches. It has to be list (either 1d or 2d)")

        # Add demand branches to the loop:
        if demand_branches is not None and isinstance(demand_branches, list):
            if len(demand_branches) != 0:
                for item in demand_branches:
                    plant.addDemandBranchForComponent(item)

        # Add set point manager to the loop:
        node_supply_out = plant.supplyOutletNode()
        node_demand_inlet = plant.demandInletNode()

        if setpoint_manager is not None:
            setpoint_manager.addToNode(node_supply_out)

        # Set up for secondary pump system if needed:
        match common_pipe_simulation:
            case 0:
                pass
            case 1:
                pump = PlantLoopComponent.pump_variable_speed(model)
                pump.addToNode(node_demand_inlet)
            case 2:
                pump = PlantLoopComponent.pump_variable_speed(model)
                pump.addToNode(node_demand_inlet)
                try:
                    setpoint_manager_secondary.addToNode(node_demand_inlet)
                except ValueError:
                    print('For "TwoWayCommonPipe", a setpoint manager in needed at demand inlet or supply inlet node.')

        return plant

    @staticmethod
    def service_hot_water_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            heater_efficiency=0.8,
            supply_water_temp=Helper.f_to_c(135)):

        spm = SetpointManager.scheduled(model, 1, supply_water_temp)
        heater = PlantLoopComponent.water_heater_mixed(
            model, thermal_efficiency=heater_efficiency, heater_control_type=2)
        pump = PlantLoopComponent.pump_variable_speed(model)

        plant = HVACTool.plant_loop(
            model, name, setpoint_manager=spm, supply_branches=[pump, heater])

        return plant

    @staticmethod
    def air_loop_simplified(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_air_flow_rate=None,
            design_return_air_flow_fraction=None,
            air_terminal_type: int = 1,
            air_terminal_reheat_type: int = 3,
            thermal_zones=[]):

        """
        -Air Terminal Type: \n
        1.SingleDuctConstantVolumeNoReheat \n
        2.SingleDuctConstantVolumeReheat \n
        3.SingleDuctVAVNoReheat \n
        4.SingleDuctVAVReheat \n
        5.SingleDuctVAVHeatAndCoolNoReheat \n
        6.SingleDuctVAVHeatAndCoolReheat \n
        7.SingleDuctSeriesPIUReheat \n
        8.SingleDuctParallelPIUReheat \n
        9.SingleDuctConstantVolumeFourPipeInduction \n
        10.SingleDuctConstantVolumeFourPipeBeam \n
        11.SingleDuctConstantVolumeFourCooledBeam

        -Air Terminal Reheat Type: \n
        1.Water
        2.Gas
        3.Electric
        """

        terminal_types = {1: "SingleDuctConstantVolumeNoReheat"}

        loop = openstudio.openstudiomodel.AirLoopHVAC(model)
        reheat_water_coils = []
        beam_cool_coils = []
        beam_heat_coils = []

        if name is not None:
            loop.setName(name)
        if design_air_flow_rate is not None:
            loop.setDesignSupplyAirFlowRate(design_air_flow_rate)
        else:
            loop.autosizeDesignSupplyAirFlowRate()

        if design_return_air_flow_fraction is not None:
            loop.setDesignReturnAirFlowFractionofSupplyAirFlow(design_return_air_flow_fraction)

        # Demand branch
        if thermal_zones is not None and len(thermal_zones) != 0:

            for zone in thermal_zones:
                match air_terminal_type:
                    case 1:  # SingleDuctConstantVolumeNoReheat
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(model)

                    case 2:  # SingleDuctConstantVolumeReheat
                        match air_terminal_reheat_type:
                            case 1:  # Water
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case 2:  # Gas
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case 3 | _:  # Electric
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_constant_volume_reheat(model, coil=reheat_coil)
                    case 3:  # SingleDuctVAVNoReheat
                        terminal = AirTerminal.single_duct_vav_no_reheat(model)

                    case 4:  # SingleDuctVAVReheat
                        match air_terminal_reheat_type:
                            case 1:  # Water
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case 2:  # Gas
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case 3 | _:  # Electric
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_vav_reheat(model, coil=reheat_coil)

                    case 5:  # SingleDuctVAVHeatAndCoolNoReheat
                        terminal = AirTerminal.single_duct_vav_heat_and_cool_no_reheat(model)

                    case 6:  # SingleDuctVAVHeatAndCoolReheat
                        match air_terminal_reheat_type:
                            case 1:  # Water
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case 2:  # Gas
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case 3 | _:  # Electric
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_vav_heat_and_cool_reheat(
                            model, coil=reheat_coil)

                    case 7:  # SingleDuctSeriesPIUReheat
                        match air_terminal_reheat_type:
                            case 1:  # Water
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case 2:  # Gas
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case 3 | _:  # Electric
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal_fan = AirLoopComponent.fan_constant_speed(model)

                        terminal = AirTerminal.single_duct_series_piu_reheat(model, fan=terminal_fan, coil=reheat_coil)

                    case 8:  # SingleDuctParallelPIUReheat
                        match air_terminal_reheat_type:
                            case 1:  # Water
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case 2:  # Gas
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case 3 | _:  # Electric
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal_fan = AirLoopComponent.fan_constant_speed(model)

                        terminal = AirTerminal.single_duct_parallel_piu_reheat(model, fan=terminal_fan,
                                                                               coil=reheat_coil)

                    case 9:  # SingleDuctConstantVolumeFourPipeInduction
                        terminal = AirTerminal.single_duct_constant_volume_four_pipe_induction(model)
                        try:
                            beam_cool_coils.append(terminal.coolingCoil())
                        except ValueError:
                            pass
                        try:
                            beam_heat_coils.append(terminal.heatingCoil())
                        except ValueError:
                            pass
                    case 10:  # SingleDuctConstantVolumeFourPipeBeam
                        terminal = AirTerminal.single_duct_constant_volume_four_pipe_beam(model)
                        try:
                            beam_cool_coils.append(terminal.coolingCoil())
                        except ValueError:
                            pass
                        try:
                            beam_heat_coils.append(terminal.heatingCoil())
                        except ValueError:
                            pass
                    case 11:  # SingleDuctConstantVolumeFourCooledBeam
                        terminal = AirTerminal.single_duct_constant_volume_cooled_beam(model)
                        try:
                            beam_cool_coils.append(terminal.coilCoolingCooledBeam())
                        except ValueError:
                            pass
                    case _:
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(model)
                        print('This terminal type is currently not supported. Please choose another type, '
                              'or the "constant volume no reheat" will be used as default')

                try:
                    loop.addBranchForZone(zone, terminal)
                except ValueError:
                    print("Cannot add zone and terminal pair to the air loop branch.")

        results = (loop, reheat_water_coils, beam_cool_coils, beam_heat_coils)

        return results


# class ChilledWaterLoop:
#
#     def __init__(self, model, name=None, condenser_type="WaterCooled", number_of_chillers=1, secondary_pump_system=False):
#         self._model = model
#         self._name = name
#         self._condenser_type = condenser_type
#         self._number_of_chillers = number_of_chillers
#         self._secondary_pump_system = secondary_pump_system
#
#     def make_loop(self):
#
#         plant = openstudio.openstudiomodel.PlantLoop(self._model)
#         if self._name is not None: plant.setName(self._name)
#
#         for i in range(self._number_of_chillers):
#             if self._condenser_type == "WaterCooled":
#                 chiller = PlantLoopComponent.chiller_electric(self._model,condenser_type=self._condenser_type)
#
#         node_supply_out = plant.supplyOutletNode()
#         node_supply_in = plant.supplyInletNode()
#
#         return plant
