import openstudio


class PlantLoopComponent:

    @staticmethod
    def plant_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fluid_type: str = None,
            max_loop_temp=None,
            min_loop_temp=None,
            max_loop_flow_rate=None,
            min_loop_flow_rate=None,
            plant_loop_volume=None,
            load_distribution_scheme=None,  # Optimal, SequentialLoad, UniformLoad, UniformPLR, SequentialUniformPLR
            common_pipe_simulation=None):  # None, CommonPipe, TwoWayCommonPipe

        plant = openstudio.openstudiomodel.PlantLoop(model)
        if name is not None: plant.setName(name)
        if fluid_type is not None: plant.setFluidType(fluid_type)
        if max_loop_temp is not None: plant.setMaximumLoopTemperature(max_loop_temp)
        if min_loop_temp is not None: plant.setMinimumLoopTemperature(min_loop_temp)

        if max_loop_flow_rate is not None:
            plant.setMaximumLoopFlowRate(max_loop_flow_rate)
        else:
            plant.autosizeMaximumLoopFlowRate()

        if min_loop_flow_rate is not None:
            plant.setMinimumLoopFlowRate(min_loop_flow_rate)
        else:
            plant.autosizeMinimumLoopFlowRate()

        if plant_loop_volume is not None:
            plant.setPlantLoopVolume(plant_loop_volume)
        else:
            plant.autocalculatePlantLoopVolume()

        if load_distribution_scheme is not None:
            plant.setLoadDistributionScheme(load_distribution_scheme)

        if common_pipe_simulation is not None:
            plant.setCommonPipeSimulation(common_pipe_simulation)

        return plant

    @staticmethod
    def plant_sizing(
            model: openstudio.openstudiomodel.Model,
            plant_loop: openstudio.openstudiomodel.PlantLoop,
            loop_type,  # Cooling, Heating, Condenser, Steam
            loop_exit_temp=None,
            loop_temp_diff=None):

        sizing = openstudio.openstudiomodel.SizingPlant(model, plant_loop)

        sizing.setLoopType(loop_type)
        if loop_exit_temp is not None:
            sizing.setDesignLoopExitTemperature(loop_exit_temp)
        if loop_temp_diff is not None:
            sizing.setLoopDesignTemperatureDifference(loop_temp_diff)

    @staticmethod
    def chiller_electric(
            model: openstudio.openstudiomodel.Model,
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
            coefficient_1=None,
            coefficient_2=None,
            coefficient_3=None,
            coefficient_4=None, ):

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

        if coefficient_1 is not None:
            pump.setCoefficient1ofthePartLoadPerformanceCurve(coefficient_1)
        if coefficient_2 is not None:
            pump.setCoefficient2ofthePartLoadPerformanceCurve(coefficient_2)
        if coefficient_3 is not None:
            pump.setCoefficient3ofthePartLoadPerformanceCurve(coefficient_3)
        if coefficient_4 is not None:
            pump.setCoefficient4ofthePartLoadPerformanceCurve(coefficient_4)

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
