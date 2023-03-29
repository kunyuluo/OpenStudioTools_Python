import openstudio
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.SetpointManagers import SetpointManager


class HVACTool:

    @staticmethod
    def air_loop_simplified(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_air_flow_rate=None,
            design_return_air_flow_fraction=None,
            air_terminal_type: str = None,
            air_terminal_reheat_type: str = None,
            thermal_zones: openstudio.openstudiomodel.ThermalZone = []):

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
        2.Electric
        3.Gas
        """

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
                    case "SingleDuctConstantVolumeNoReheat":
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(model)

                    case "SingleDuctConstantVolumeReheat":
                        match air_terminal_reheat_type:
                            case "Water":
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case "Gas":
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case "Electric" | _:
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_constant_volume_reheat(model, coil=reheat_coil)
                    case "SingleDuctVAVNoReheat":
                        terminal = AirTerminal.single_duct_vav_no_reheat(model)

                    case "SingleDuctVAVReheat":
                        match air_terminal_reheat_type:
                            case "Water":
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case "Gas":
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case "Electric" | _:
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_vav_reheat(model, coil=reheat_coil)

                    case "SingleDuctVAVHeatAndCoolNoReheat":
                        terminal = AirTerminal.single_duct_vav_heat_and_cool_no_reheat(model)

                    case "SingleDuctVAVHeatAndCoolReheat":
                        match air_terminal_reheat_type:
                            case "Water":
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case "Gas":
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case "Electric" | _:
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal = AirTerminal.single_duct_vav_heat_and_cool_reheat(
                            model, coil=reheat_coil)

                    case "SingleDuctSeriesPIUReheat":
                        match air_terminal_reheat_type:
                            case "Water":
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case "Gas":
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case "Electric" | _:
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal_fan = AirLoopComponent.fan_constant_speed(model)

                        terminal = AirTerminal.single_duct_series_piu_reheat(model, fan=terminal_fan, coil=reheat_coil)

                    case "SingleDuctParallelPIUReheat":
                        match air_terminal_reheat_type:
                            case "Water":
                                reheat_coil = AirLoopComponent.coil_heating_water(model)
                                reheat_water_coils.append(reheat_coil)
                            case "Gas":
                                reheat_coil = AirLoopComponent.coil_heating_gas(model)
                            case "Electric" | _:
                                reheat_coil = AirLoopComponent.coil_heating_electric(model)

                        terminal_fan = AirLoopComponent.fan_constant_speed(model)

                        terminal = AirTerminal.single_duct_parallel_piu_reheat(model, fan=terminal_fan,
                                                                               coil=reheat_coil)

                    case "SingleDuctConstantVolumeFourPipeInduction":
                        terminal = AirTerminal.single_duct_constant_volume_four_pipe_induction(model)
                        try:
                            beam_cool_coils.append(terminal.coolingCoil())
                        except ValueError:
                            pass
                        try:
                            beam_heat_coils.append(terminal.heatingCoil())
                        except ValueError:
                            pass
                    case "SingleDuctConstantVolumeFourPipeBeam":
                        terminal = AirTerminal.single_duct_constant_volume_four_pipe_beam(model)
                        try:
                            beam_cool_coils.append(terminal.coolingCoil())
                        except ValueError:
                            pass
                        try:
                            beam_heat_coils.append(terminal.heatingCoil())
                        except ValueError:
                            pass
                    case "SingleDuctConstantVolumeFourCooledBeam":
                        terminal = AirTerminal.single_duct_constant_volume_cooled_beam(model)
                        try:
                            beam_cool_coils.append(terminal.coilCoolingCooledBeam())
                        except ValueError:
                            pass
                    case _:
                        terminal = AirTerminal.single_duct_constant_volume_no_reheat(model)
                        print('This terminal type is currently not supported. Please choose another type, '
                              'or the "constant volume no reheat" will be used as default')

                loop.addBranchForZone(zone, terminal)

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
