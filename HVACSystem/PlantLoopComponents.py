import openstudio
from Resources.Helpers import Helper


class PlantLoopComponent:

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

        # Add branches to the loop:
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

        if demand_branches is not None and len(demand_branches) != 0:
            for item in demand_branches:
                plant.addSupplyBranchForComponent(demand_branches.pop(-1))
                node = plant.demandMixer().inletModelObjects()[-1].to_Node().get()
                item.addToNode(node)

        node_supply_out = plant.supplyOutletNode()
        node_demand_inlet = plant.demandInletNode()

        if setpoint_manager is not None:
            setpoint_manager.addToNode(node_supply_out)

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
    def sizing(
            model: openstudio.openstudiomodel.Model,
            plant_loop: openstudio.openstudiomodel.PlantLoop,
            loop_type: int = 1,
            loop_exit_temp=None,
            loop_temp_diff=None,
            sizing_option: int = None,
            zone_timesteps_in_averaging_window=None,
            coincident_sizing_factor_mode: int = 1):

        """
        -Loop_type: 1:Cooling 2:Heating 3:Condenser 4:Steam \n

        -Sizing_option:
        1: Coincident
        2: NonCoincident
        (Default is NonCoincident) \n

        -Coincident_sizing_factor_mode: \n
        1: None \n
        2: GlobalCoolingSizingFactor \n
        3: GlobalHeatingSizingFactor \n
        4: LoopComponentSizingFactor
        """

        loop_types = {1: "Cooling", 2: "Heating", 3: "Condenser", 4: "Steam"}
        sizing_options = {1: "Coincident", 2: "NonCoincident"}
        sizing_factor_modes = {1: "None", 2: "GlobalCoolingSizingFactor",
                               3: "GlobalHeatingSizingFactor", 4: "LoopComponentSizingFactor"}

        sizing = openstudio.openstudiomodel.SizingPlant(model, plant_loop)

        sizing.setLoopType(loop_types[loop_type])

        if loop_exit_temp is not None:
            sizing.setDesignLoopExitTemperature(loop_exit_temp)
        else:
            match loop_type:
                case 1:
                    sizing.setDesignLoopExitTemperature(Helper.f_to_c(44))
                case 2:
                    sizing.setDesignLoopExitTemperature(Helper.f_to_c(180))
                case 3:
                    sizing.setDesignLoopExitTemperature(Helper.f_to_c(85))
                case 4 | _:
                    sizing.setDesignLoopExitTemperature(Helper.f_to_c(210))

        if loop_temp_diff is not None:
            sizing.setLoopDesignTemperatureDifference(loop_temp_diff)
        else:
            match loop_type:
                case 1:
                    sizing.setLoopDesignTemperatureDifference(Helper.delta_temp_f_to_c(12))
                case 2:
                    sizing.setLoopDesignTemperatureDifference(Helper.delta_temp_f_to_c(30))
                case 3:
                    sizing.setLoopDesignTemperatureDifference(Helper.delta_temp_f_to_c(10))
                case 4 | _:
                    sizing.setLoopDesignTemperatureDifference(Helper.delta_temp_f_to_c(50))

        if sizing_option is not None:
            sizing.setSizingOption(sizing_options[sizing_option])

        if coincident_sizing_factor_mode is not None:
            sizing.setCoincidentSizingFactorMode(sizing_factor_modes[coincident_sizing_factor_mode])

    @staticmethod
    def chiller_electric(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            condenser_type="WaterCooled",  # WaterCooled, AirCooled, EvaporativelyCooled
            capacity=None,
            cop=5.5,
            leaving_chilled_water_temp=None,
            entering_condenser_water_temp=None,
            chilled_water_flow_rate=None,
            condenser_water_flow_rate=None,
            heat_recovery_water_flow_rate=None,
            min_part_load_ratio=None,
            max_part_load_ratio=None,
            optimal_part_load_ratio=None,
            min_unload_ratio=None,
            condenser_fan_power_ratio=None,
            compressor_by_condenser_fraction=None,
            chiller_flow_mode=None,  # NotModulated, LeavingSetpointModulated, ConstantFlow
            sizing_factor=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_plr_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            plant_loop: openstudio.openstudiomodel.PlantLoop = None):

        chiller = openstudio.openstudiomodel.ChillerElectricEIR(model)
        chiller.setReferenceCOP(cop)
        if name is not None:
            chiller.setName(name)
        if condenser_type is not None:
            chiller.setCondenserType(condenser_type)
        if leaving_chilled_water_temp is not None:
            chiller.setReferenceLeavingChilledWaterTemperature(leaving_chilled_water_temp)
        if entering_condenser_water_temp is not None:
            chiller.setReferenceEnteringCondenserFluidTemperature(entering_condenser_water_temp)
        if chiller_flow_mode is not None:
            chiller.setChillerFlowMode(chiller_flow_mode)
        if sizing_factor is not None:
            chiller.setSizingFactor(sizing_factor)
        if min_part_load_ratio is not None:
            chiller.setMinimumPartLoadRatio(min_part_load_ratio)
        if max_part_load_ratio is not None:
            chiller.setMaximumPartLoadRatio(max_part_load_ratio)
        if optimal_part_load_ratio is not None:
            chiller.setOptimumPartLoadRatio(optimal_part_load_ratio)
        if min_unload_ratio is not None:
            chiller.setMinimumUnloadingRatio(min_unload_ratio)
        if condenser_fan_power_ratio is not None:
            chiller.setCondenserFanPowerRatio(condenser_fan_power_ratio)
        if compressor_by_condenser_fraction is not None:
            chiller.setFractionofCompressorElectricConsumptionRejectedbyCondenser(compressor_by_condenser_fraction)

        if heat_recovery_water_flow_rate is not None:
            chiller.setDesignHeatRecoveryWaterFlowRate(heat_recovery_water_flow_rate)
        else:
            chiller.autosizeDesignHeatRecoveryWaterFlowRate()

        if capacity is not None:
            chiller.setReferenceCapacity(capacity)
        else:
            chiller.autosizeReferenceCapacity()

        if chilled_water_flow_rate is not None:
            chiller.setReferenceChilledWaterFlowRate(chilled_water_flow_rate)
        else:
            chiller.autosizeReferenceChilledWaterFlowRate()

        if condenser_water_flow_rate is not None:
            chiller.setReferenceCondenserFluidFlowRate(condenser_water_flow_rate)
        else:
            chiller.autosizeReferenceCondenserFluidFlowRate()

        if capacity_temperature_curve is not None:
            chiller.setCoolingCapacityFunctionOfTemperature(capacity_temperature_curve)
        if cop_temperature_curve is not None:
            chiller.setElectricInputToCoolingOutputRatioFunctionOfTemperature(cop_temperature_curve)
        if cop_plr_curve is not None:
            chiller.setElectricInputToCoolingOutputRatioFunctionOfPLR(cop_plr_curve)

        if plant_loop is not None: plant_loop.addSupplyBranchForComponent(chiller)

        return chiller

    @staticmethod
    def boiler_hot_water(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fuel_type: int = 1,
            nominal_capacity=None,
            efficiency=None,
            efficiency_curve_temp_eval_variable: int = 1,
            boiler_efficiency_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            design_water_flow_rate=None,
            min_part_load_ratio=None,
            max_part_load_ratio=None,
            optimal_part_load_ratio=None,
            water_outlet_upper_temp_limit=None,
            boiler_flow_mode: int = 1,
            parasitic_electric_load=None,
            sizing_factor=None):

        boiler = openstudio.openstudiomodel.BoilerHotWater(model)

        if name is not None:
            boiler.setName(name)

        return boiler

    @staticmethod
    def boiler_steam(
            model: openstudio.openstudiomodel.Model,
            name: str = None,):

        boiler = openstudio.openstudiomodel.BoilerSteam(model)

        if name is not None:
            boiler.setName(name)

        return boiler

    @staticmethod
    def adiabatic_pipe(model: openstudio.openstudiomodel.Model):
        pipe = openstudio.openstudiomodel.PipeAdiabatic(model)
        return pipe

    @staticmethod
    def pump_variable_speed(
            model: openstudio.openstudiomodel.Model,
            name=None,
            rated_head=None,
            rated_flow_rate=None,
            min_flow_rate=None,
            rated_power=None,
            motor_efficiency=None,
            control_type=None,  # Intermittent, Continuous
            vfd_control_type=None,  # PressureSetPointControl, ManualControl
            power_sizing_method=None,  # PowerPerFlowPerPressure, PowerPerFlow
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
            skin_loss_radiative_fraction=None,
            pump_curve_coeff=None):

        pump = openstudio.openstudiomodel.PumpVariableSpeed(model)

        if name is not None: pump.setName(name)
        if rated_head is not None: pump.setRatedPumpHead(rated_head)

        if rated_flow_rate is not None:
            pump.setRatedFlowRate(rated_flow_rate)
        else:
            pump.autosizeRatedFlowRate()

        if min_flow_rate is not None: pump.setMinimumFlowRate(min_flow_rate)

        if rated_power is not None:
            pump.setRatedPowerConsumption(rated_power)
        else:
            pump.autosizeRatedPowerConsumption()

        if motor_efficiency is not None:
            pump.setMotorEfficiency(motor_efficiency)
        if control_type is not None:
            pump.setPumpControlType(control_type)
        if power_sizing_method is not None:
            pump.setDesignPowerSizingMethod(power_sizing_method)
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)
        if vfd_control_type is not None:
            pump.setVFDControlType(vfd_control_type)

        if thermal_zone is not None:
            pump.setZone(thermal_zone)
        if skin_loss_radiative_fraction is not None:
            pump.setSkinLossRadiativeFraction(skin_loss_radiative_fraction)

        if pump_curve_coeff is not None:
            if isinstance(pump_curve_coeff, list) and len(pump_curve_coeff) == 4:
                pump.setCoefficient1ofthePartLoadPerformanceCurve(pump_curve_coeff[0])
                pump.setCoefficient2ofthePartLoadPerformanceCurve(pump_curve_coeff[1])
                pump.setCoefficient3ofthePartLoadPerformanceCurve(pump_curve_coeff[2])
                pump.setCoefficient4ofthePartLoadPerformanceCurve(pump_curve_coeff[3])

        return pump

    @staticmethod
    def pump_constant_speed(
            model: openstudio.openstudiomodel.Model,
            name=None,
            rated_head=None,
            rated_flow_rate=None,
            rated_power=None,
            motor_efficiency=None,
            control_type=None,  # Intermittent, Continuous
            power_sizing_method=None,  # PowerPerFlowPerPressure, PowerPerFlow
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None):

        pump = openstudio.openstudiomodel.PumpConstantSpeed(model)

        if name is not None: pump.setName(name)
        if rated_head is not None: pump.setRatedPumpHead(rated_head)

        if rated_flow_rate is not None:
            pump.setRatedFlowRate(rated_flow_rate)
        else:
            pump.autosizeRatedFlowRate()

        if rated_power is not None:
            pump.setRatedPowerConsumption(rated_power)
        else:
            pump.autosizeRatedPowerConsumption()

        if motor_efficiency is not None:
            pump.setMotorEfficiency(motor_efficiency)
        if control_type is not None:
            pump.setPumpControlType(control_type)
        if power_sizing_method is not None:
            pump.setDesignPowerSizingMethod(power_sizing_method)
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)

        if thermal_zone is not None:
            pump.setZone(thermal_zone)

        return pump
