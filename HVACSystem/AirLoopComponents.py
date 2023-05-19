import openstudio
from HVACSystem.SetpointManagers import SetpointManager
from HVACSystem.PerformanceCurves import Curve
from Schedules.ScheduleTools import ScheduleTool


class AirLoopComponent:

    # @staticmethod
    # def air_loop(
    #         model: openstudio.openstudiomodel.Model,
    #         name: str = None,
    #         design_air_flow_rate=None,
    #         design_return_air_flow_fraction=None,
    #         thermal_zones: openstudio.openstudiomodel.ThermalZone = []):
    #
    #     loop = openstudio.openstudiomodel.AirLoopHVAC(model)
    #     if name is not None: loop.setName(name)
    #     if design_air_flow_rate is not None:
    #         loop.setDesignSupplyAirFlowRate(design_air_flow_rate)
    #     else:
    #         loop.autosizeDesignSupplyAirFlowRate()
    #
    #     if design_return_air_flow_fraction is not None:
    #         loop.setDesignReturnAirFlowFractionofSupplyAirFlow(design_return_air_flow_fraction)
    #
    #     supply_inlet_node = loop.supplyInletNode()
    #     supply_outlet_node = loop.supplyOutletNode()
    #
    #     # Add outdoor air system to the loop
    #     controller = openstudio.openstudiomodel.ControllerOutdoorAir(model)
    #     outdoor_air_system = openstudio.openstudiomodel.AirLoopHVACOutdoorAirSystem(model, controller)
    #     outdoor_air_system.addToNode(supply_inlet_node)
    #
    #     oa_node = outdoor_air_system.outboardOANode().get()
    #     relief_node = outdoor_air_system.outboardReliefNode().get()
    #
    #     # Add relief fan
    #     relief_fan = AirLoopComponent.fan_variable_speed(model, "kunyu relief fan")
    #     relief_fan.addToNode(relief_node)
    #
    #     # Add heat exchanger
    #     heat_exchanger = AirLoopComponent.heat_exchanger_air_to_air(model)
    #     heat_exchanger.addToNode(oa_node)
    #
    #     # Add cooling coil
    #     coil_cooling = AirLoopComponent.coil_cooling_water(model, "kunyu's cooling coil")
    #     coil_cooling.addToNode(supply_outlet_node)
    #
    #     # Add heating coil
    #     coil_heating = AirLoopComponent.coil_heating_electric(model, efficiency=0.97)
    #     coil_heating.addToNode(supply_outlet_node)
    #
    #     # Add fan
    #     fan = AirLoopComponent.fan_variable_speed(model, "kunyu's fan")
    #     fan.addToNode(supply_outlet_node)
    #
    #     # Add setpoint manager
    #     spm = SetpointManager.scheduled(model, constant_value=12.6)
    #     spm.addToNode(supply_outlet_node)
    #
    #     # Demand branch
    #     if thermal_zones is not None and len(thermal_zones) != 0:
    #         for zone in thermal_zones:
    #             diffuser = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeNoReheat(
    #                 model, ScheduleTool.always_on(model))
    #             loop.addBranchForZone(zone, diffuser)
    #
    #     return loop

    # Sizing:
    @staticmethod
    def sizing(
            model: openstudio.openstudiomodel.Model,
            air_loop: openstudio.openstudiomodel.AirLoopHVAC,
            type_of_load_to_size_on: int = 1,
            design_outdoor_air_flow_rate=None,
            central_heating_max_flow_ratio=None,
            system_outdoor_air_method: int = None,
            preheat_temp=None,
            preheat_humidity_ratio=None,
            precool_temp=None,
            precool_humidity_ratio=None,
            central_cooling_supply_air_temp=None,
            central_heating_supply_air_temp=None,
            sizing_option: int = None,
            all_outdoor_air_cooling: bool = False,
            all_outdoor_air_heating: bool = False,
            cooling_design_capacity_method: int = None,
            heating_design_capacity_method: int = None,
            cooling_design_capacity=None,
            heating_design_capacity=None,
            cooling_design_capacity_per_floor_area=None,
            heating_design_capacity_per_floor_area=None,
            fraction_of_autosized_cooling_design_capacity=None,
            fraction_of_autosized_heating_design_capacity=None,
            central_cooling_capacity_control_method: int = 1,
            occupant_diversity=None):

        """
        -Options for "type_of_load_to_size_on":
            1: Total (Sensible + Latent)
            2: Sensible
            3: VentilationRequirement (choose this option for DOAS)

        -Options for "system_outdoor_air_method":
            1: ZoneSum
            2: Standard62.1VentilationRateProcedure (VRP)
            3: Standard62.1SimplifiedProcedure (SP)
            (Default is ZoneSum)

        -Options for "sizing_option":
            1: Coincident
            2: NonCoincident
            (Default is NonCoincident)

        -Options for "cooling_design_capacity_method":
            1: DesignDay
            2: Flow/System
            3: FlowPerFloorArea
            4: FractionOfAutosizedCoolingAirflow
            5: FlowPerCoolingCapacity
            (Default is DesignDay)

        -Options for "heating_design_capacity_method": same as above

        -Options for "central_cooling_capacity_control_method":
            1: OnOff
            2: VAV
            3: Bypass
            4: VT
            (Default is OnOff)
        """

        load_types = {1: "Total", 2: "Sensible", 3: "VentilationRequirement"}
        outdoor_air_methods = {1: "ZoneSum", 2: "Standard62.1VentilationRateProcedure",
                               3: "Standard62.1SimplifiedProcedure"}
        sizing_options = {1: "Coincident", 2: "NonCoincident"}
        cooling_capacity_methods = {1: "DesignDay", 2: "Flow/System", 3: "FlowPerFloorArea",
                                    4: "FractionOfAutosizedCoolingAirflow", 5: "FlowPerCoolingCapacity"}
        cooling_control_methods = {1: "OnOff", 2: "VAV", 3: "Bypass", 4: "VT"}

        sizing = openstudio.openstudiomodel.SizingSystem(model, air_loop)

        if type_of_load_to_size_on is not None:
            sizing.setTypeofLoadtoSizeOn(load_types[type_of_load_to_size_on])

        if design_outdoor_air_flow_rate is not None:
            sizing.setDesignOutdoorAirFlowRate(design_outdoor_air_flow_rate)
        else:
            sizing.autosizeDesignOutdoorAirFlowRate()

        if central_heating_max_flow_ratio is not None:
            sizing.setCentralHeatingMaximumSystemAirFlowRatio(central_heating_max_flow_ratio)
        else:
            sizing.autosizeCentralHeatingMaximumSystemAirFlowRatio()

        if system_outdoor_air_method is not None:
            sizing.setSystemOutdoorAirMethod(outdoor_air_methods[system_outdoor_air_method])

        if preheat_temp is not None:
            sizing.setPreheatDesignTemperature(preheat_temp)

        if preheat_humidity_ratio is not None:
            sizing.setPreheatDesignHumidityRatio(preheat_humidity_ratio)

        if precool_temp is not None:
            sizing.setPreheatDesignTemperature(preheat_temp)

        if precool_humidity_ratio is not None:
            sizing.setPrecoolDesignHumidityRatio(precool_humidity_ratio)

        if central_heating_supply_air_temp is not None:
            sizing.setCentralHeatingDesignSupplyAirTemperature(central_heating_supply_air_temp)

        if central_cooling_supply_air_temp is not None:
            sizing.setCentralCoolingDesignSupplyAirTemperature(central_cooling_supply_air_temp)

        if sizing_option is not None:
            sizing.setSizingOption(sizing_options[sizing_option])

        if all_outdoor_air_heating is not None:
            sizing.setAllOutdoorAirinHeating(all_outdoor_air_heating)
        if all_outdoor_air_cooling is not None:
            sizing.setAllOutdoorAirinCooling(all_outdoor_air_cooling)

        if cooling_design_capacity_method is not None:
            sizing.setCoolingDesignCapacityMethod(cooling_capacity_methods[cooling_design_capacity_method])
        if heating_design_capacity_method is not None:
            sizing.setHeatingDesignCapacityMethod(cooling_capacity_methods[heating_design_capacity_method])

        if cooling_design_capacity is not None:
            sizing.setCoolingDesignCapacity(cooling_design_capacity)
        else:
            sizing.autosizeCoolingDesignCapacity()

        if heating_design_capacity is not None:
            sizing.setHeatingDesignCapacity(heating_design_capacity)
        else:
            sizing.autosizeHeatingDesignCapacity()

        if cooling_design_capacity_per_floor_area is not None:
            sizing.setCoolingDesignCapacityPerFloorArea(cooling_design_capacity_per_floor_area)
        if heating_design_capacity_per_floor_area is not None:
            sizing.setHeatingDesignCapacityPerFloorArea(heating_design_capacity_per_floor_area)

        if fraction_of_autosized_cooling_design_capacity is not None:
            sizing.setFractionofAutosizedCoolingDesignCapacity(fraction_of_autosized_cooling_design_capacity)
        if fraction_of_autosized_heating_design_capacity is not None:
            sizing.setFractionofAutosizedHeatingDesignCapacity(fraction_of_autosized_heating_design_capacity)

        if central_cooling_capacity_control_method is not None:
            sizing.setCentralCoolingCapacityControlMethod(
                cooling_control_methods[central_cooling_capacity_control_method])

        if occupant_diversity is not None:
            sizing.setOccupantDiversity(occupant_diversity)
        else:
            sizing.autosizeOccupantDiversity()

    # Coils
    # ********************************************************************************
    @staticmethod
    def coil_cooling_water(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            design_water_flow_rate=None,
            design_air_flow_rate=None,
            design_inlet_water_temp=None,
            design_inlet_air_temp=None,
            design_outlet_air_temp=None,
            design_inlet_air_humidity_ratio=None,
            design_outlet_air_humidity_ratio=None,
            type_of_analysis: str = None,
            heat_exchanger_config: str = None):

        coil = openstudio.openstudiomodel.CoilCoolingWater(model)
        if name is not None:
            coil.setName(name)

        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if design_water_flow_rate is not None:
            coil.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            coil.autosizeDesignWaterFlowRate()

        if design_air_flow_rate is not None:
            coil.setDesignAirFlowRate(design_air_flow_rate)
        else:
            coil.autosizeDesignAirFlowRate()

        if design_inlet_water_temp is not None:
            coil.setDesignInletWaterTemperature(design_inlet_water_temp)
        else:
            coil.autosizeDesignInletWaterTemperature()

        if design_inlet_air_temp is not None:
            coil.setDesignInletAirTemperature(design_inlet_air_temp)
        else:
            coil.autosizeDesignInletAirTemperature()

        if design_outlet_air_temp is not None:
            coil.setDesignOutletAirTemperature(design_outlet_air_temp)
        else:
            coil.autosizeDesignOutletAirTemperature()

        if design_inlet_air_humidity_ratio is not None:
            coil.setDesignInletAirHumidityRatio(design_inlet_air_humidity_ratio)
        else:
            coil.autosizeDesignInletAirHumidityRatio()

        if design_outlet_air_humidity_ratio is not None:
            coil.setDesignOutletAirHumidityRatio(design_outlet_air_humidity_ratio)
        else:
            coil.autosizeDesignOutletAirHumidityRatio()

        if type_of_analysis is not None:
            coil.setTypeOfAnalysis(type_of_analysis)

        if heat_exchanger_config is not None:
            coil.setHeatExchangerConfiguration(heat_exchanger_config)

        # controller = coil.controllerWaterCoil().get()

        return coil

    @staticmethod
    def coil_cooling_dx_single_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            capacity=None,
            sensible_heat_ratio=None,
            cop=None,
            rated_air_flow_rate=None,
            evaporator_fan_power_per_flow_2017=None,
            evaporator_fan_power_per_flow_2023=None,
            min_outdoor_air_temp_compressor_operation=None,
            crankcase_heater_capacity=None,
            max_outdoor_air_temp_crankcase_operation=None,
            condenser_type: str = None,
            evaporative_condenser_effectiveness=None,
            evaporative_condenser_air_flow_rate=None,
            evaporative_condenser_pump_power=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            capacity_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            cop_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            plr_curve: openstudio.openstudiomodel.CurveQuadratic = None):

        coil = openstudio.openstudiomodel.CoilCoolingDXSingleSpeed(model)
        if name is not None:
            coil.setName(name)

        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if capacity is not None:
            coil.setRatedTotalCoolingCapacity(capacity)
        else:
            coil.autosizeRatedTotalCoolingCapacity()

        if sensible_heat_ratio is not None:
            coil.setRatedSensibleHeatRatio(sensible_heat_ratio)
        else:
            coil.autosizeRatedSensibleHeatRatio()

        if cop is not None:
            coil.setRatedCOP(cop)

        if rated_air_flow_rate is not None:
            coil.setRatedAirFlowRate(rated_air_flow_rate)
        else:
            coil.autosizeRatedAirFlowRate()

        if evaporator_fan_power_per_flow_2017 is not None:
            coil.setRatedEvaporatorFanPowerPerVolumeFlowRate2017(evaporator_fan_power_per_flow_2017)

        if evaporator_fan_power_per_flow_2023 is not None:
            coil.setRatedEvaporatorFanPowerPerVolumeFlowRate2023(evaporator_fan_power_per_flow_2023)

        if min_outdoor_air_temp_compressor_operation is not None:
            coil.setMinimumOutdoorDryBulbTemperatureforCompressorOperation(min_outdoor_air_temp_compressor_operation)

        if max_outdoor_air_temp_crankcase_operation is not None:
            coil.setMaximumOutdoorDryBulbTemperatureForCrankcaseHeaterOperation(
                max_outdoor_air_temp_crankcase_operation)

        if crankcase_heater_capacity is not None:
            coil.setCrankcaseHeaterCapacity(crankcase_heater_capacity)

        if condenser_type is not None:
            coil.setCondenserType(condenser_type)

        if evaporative_condenser_effectiveness is not None:
            coil.setEvaporativeCondenserEffectiveness(evaporative_condenser_effectiveness)

        if evaporative_condenser_air_flow_rate is not None:
            coil.setEvaporativeCondenserAirFlowRate(evaporative_condenser_air_flow_rate)
        else:
            coil.autosizeEvaporativeCondenserAirFlowRate()

        if evaporative_condenser_pump_power is not None:
            coil.setEvaporativeCondenserPumpRatedPowerConsumption(evaporative_condenser_pump_power)
        else:
            coil.autosizeEvaporativeCondenserPumpRatedPowerConsumption()

        if capacity_temperature_curve is not None:
            coil.setTotalCoolingCapacityFunctionOfTemperatureCurve(capacity_temperature_curve)
        if capacity_flow_curve is not None:
            coil.setTotalCoolingCapacityFunctionOfFlowFractionCurve(capacity_flow_curve)
        if cop_temperature_curve is not None:
            coil.setEnergyInputRatioFunctionOfTemperatureCurve(cop_temperature_curve)
        if cop_flow_curve is not None:
            coil.setEnergyInputRatioFunctionOfFlowFractionCurve(cop_flow_curve)
        if plr_curve is not None:
            coil.setPartLoadFractionCorrelationCurve(plr_curve)

        return coil

    @staticmethod
    def coil_cooling_vrf(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            capacity=None,
            rated_air_flow_rate=None,
            sensible_heat_ratio=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            capacity_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None):

        coil = openstudio.openstudiomodel.CoilCoolingDXVariableRefrigerantFlow(model)

        if name is not None:
            coil.setName(name)
        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if capacity is not None:
            coil.setRatedTotalCoolingCapacity(capacity)
        else:
            coil.autosizeRatedTotalCoolingCapacity()

        if rated_air_flow_rate is not None:
            coil.setRatedAirFlowRate(rated_air_flow_rate)
        else:
            coil.autosizeRatedAirFlowRate()

        if sensible_heat_ratio is not None:
            coil.setRatedSensibleHeatRatio(sensible_heat_ratio)
        else:
            coil.autosizeRatedSensibleHeatRatio()

        if capacity_temperature_curve is not None:
            coil.setCoolingCapacityRatioModifierFunctionofTemperatureCurve(capacity_temperature_curve)
        if capacity_flow_curve is not None:
            coil.setCoolingCapacityModifierCurveFunctionofFlowFraction(capacity_flow_curve)

        return coil

    @staticmethod
    def coil_cooling_four_pipe_beam(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            cooling_capacity_per_beam_length=None,
            room_air_chilled_water_temp_difference=None,
            chilled_water_flow_rate_per_beam_length=None,
            capacity_temp_difference_factor_curve=None,
            capacity_air_flow_factor_curve=None,
            capacity_chilled_water_flow_factor_curve=None):

        coil = openstudio.openstudiomodel.CoilCoolingFourPipeBeam(model)

        if name is not None:
            coil.setName(name)

        if cooling_capacity_per_beam_length is not None:
            coil.setBeamRatedCoolingCapacityperBeamLength(cooling_capacity_per_beam_length)
        if room_air_chilled_water_temp_difference is not None:
            coil.setBeamRatedCoolingRoomAirChilledWaterTemperatureDifference(room_air_chilled_water_temp_difference)
        if chilled_water_flow_rate_per_beam_length is not None:
            coil.setBeamRatedChilledWaterVolumeFlowRateperBeamLength(chilled_water_flow_rate_per_beam_length)

        if capacity_temp_difference_factor_curve is not None:
            coil.setBeamCoolingCapacityTemperatureDifferenceModificationFactorCurve(
                capacity_temp_difference_factor_curve)
        if capacity_air_flow_factor_curve is not None:
            coil.setBeamCoolingCapacityAirFlowModificationFactorCurve(capacity_air_flow_factor_curve)
        if capacity_chilled_water_flow_factor_curve is not None:
            coil.setBeamCoolingCapacityChilledWaterFlowModificationFactorCurve(capacity_chilled_water_flow_factor_curve)

        return coil

    @staticmethod
    def coil_cooling_cooled_beam(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            coil_surface_area_per_coil_length=None,
            model_parameter_a=None,
            model_parameter_n1=None,
            model_parameter_n2=None,
            model_parameter_n3=None,
            model_parameter_a0=None,
            model_parameter_k1=None,
            model_parameter_n=None,
            leaving_pipe_inside_diameter=None):

        coil = openstudio.openstudiomodel.CoilCoolingCooledBeam(model)

        if name is not None:
            coil.setName(name)
        if coil_surface_area_per_coil_length is not None:
            coil.setCoilSurfaceAreaperCoilLength(coil_surface_area_per_coil_length)
        if model_parameter_a is not None:
            coil.setModelParametera(model_parameter_a)
        if model_parameter_n1 is not None:
            coil.setModelParametern1(model_parameter_n1)
        if model_parameter_n2 is not None:
            coil.setModelParametern2(model_parameter_n2)
        if model_parameter_n3 is not None:
            coil.setModelParametern3(model_parameter_n3)
        if model_parameter_a0 is not None:
            coil.setModelParametera0(model_parameter_a0)
        if model_parameter_k1 is not None:
            coil.setModelParameterK1(model_parameter_k1)
        if model_parameter_n is not None:
            coil.setModelParametern(model_parameter_n)
        if leaving_pipe_inside_diameter is not None:
            coil.setLeavingPipeInsideDiameter(leaving_pipe_inside_diameter)

        return coil

    @staticmethod
    def coil_cooling_low_temperature_radiant_variable_flow(
            model: openstudio.openstudiomodel.Model,
            cooling_control_temp_schedule=None,
            capacity_method: int = 1,
            design_capacity=None,
            capacity_per_floor_area=None,
            fraction_of_autosized_capacity=None,
            max_cold_water_flow=None,
            cooling_control_throttling_range=None,
            condensation_control_type: int = 1,
            condensation_control_dewpoint_offset=None,
            name: str = None):

        """
        -Capacity_method: \n
        1.CoolingDesignCapacity 2.CapacityPerFloorArea 3.FractionOfAutosizedCoolingCapacity \n

        -Condensation_control_type: \n
        1.Off 2.SimpleOff 3.VariableOff
        """

        cap_methods = {1: "CoolingDesignCapacity", 2: "CapacityPerFloorArea", 3: "FractionOfAutosizedCoolingCapacity"}
        condensations = {1: "Off", 2: "SimpleOff", 3: "VariableOff"}

        if cooling_control_temp_schedule is not None:
            schedule = cooling_control_temp_schedule
        else:
            type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 50)
            schedule = ScheduleTool.schedule_ruleset(model, 21, type_limit, "Var Vol Rad Clg Air Temp Sch")

        coil = openstudio.openstudiomodel.CoilCoolingLowTempRadiantVarFlow(model, schedule)

        coil.setCoolingDesignCapacityMethod(cap_methods[capacity_method])

        if design_capacity is not None:
            coil.setCoolingDesignCapacity(design_capacity)
        else:
            coil.autosizeCoolingDesignCapacity()

        if capacity_per_floor_area is not None:
            coil.setCoolingDesignCapacityPerFloorArea(capacity_per_floor_area)

        if fraction_of_autosized_capacity is not None:
            coil.setFractionofAutosizedCoolingDesignCapacity(fraction_of_autosized_capacity)

        if max_cold_water_flow is not None:
            coil.setMaximumColdWaterFlow(max_cold_water_flow)
        else:
            coil.autosizedMaximumColdWaterFlow()

        if cooling_control_throttling_range is not None:
            coil.setCoolingControlThrottlingRange(cooling_control_throttling_range)

        coil.setCondensationControlType(condensations[condensation_control_type])

        if condensation_control_dewpoint_offset is not None:
            coil.setCondensationControlDewpointOffset(condensation_control_dewpoint_offset)

        if name is not None:
            coil.setName(name)

        return coil

    @staticmethod
    def coil_cooling_low_temperature_radiant_constant_flow(
            model: openstudio.openstudiomodel.Model,
            cooling_high_water_temp_schedule=None,
            cooling_low_water_temp_schedule=None,
            cooling_high_control_temp_schedule=None,
            cooling_low_control_temp_schedule=None,
            cooling_high_water_temp=None,
            cooling_low_water_temp=None,
            cooling_high_control_temp=None,
            cooling_low_control_temp=None,
            condensation_control_type: int = 1,
            condensation_control_dewpoint_offset=None,
            name: str = None):

        """
        -Condensation_control_type: \n
        1.Off 2.SimpleOff 3.VariableOff
        """

        condensations = {1: "Off", 2: "SimpleOff", 3: "VariableOff"}

        type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 50)
        if cooling_high_water_temp_schedule is not None:
            high_water_temp_schedule = cooling_high_water_temp_schedule
        else:
            if cooling_high_water_temp is not None:
                high_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, cooling_high_water_temp, type_limit, "Const Vol Rad Clg Hi Wtr Temp Sch")
            else:
                high_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 15, type_limit, "Const Vol Rad Clg Hi Wtr Temp Sch")

        if cooling_low_water_temp_schedule is not None:
            low_water_temp_schedule = cooling_low_water_temp_schedule
        else:
            if cooling_low_water_temp is not None:
                low_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, cooling_low_water_temp, type_limit, "Const Vol Rad Clg Low Wtr Temp Sch")
            else:
                low_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 10, type_limit, "Const Vol Rad Clg Low Wtr Temp Sch")

        if cooling_high_control_temp_schedule is not None:
            high_air_temp_schedule = cooling_high_control_temp_schedule
        else:
            if cooling_high_control_temp is not None:
                high_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, cooling_high_control_temp, type_limit, "Const Vol Rad Clg Hi Air Temp Sch")
            else:
                high_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 25, type_limit, "Const Vol Rad Clg Hi Air Temp Sch")

        if cooling_low_control_temp_schedule is not None:
            low_air_temp_schedule = cooling_low_control_temp_schedule
        else:
            if cooling_low_control_temp is not None:
                low_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, cooling_low_control_temp, type_limit, "Const Vol Rad Clg Low Air Temp Sch")
            else:
                low_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 21, type_limit, "Const Vol Rad Clg Low Air Temp Sch")

        coil = openstudio.openstudiomodel.CoilCoolingLowTempRadiantConstFlow(
            model, high_water_temp_schedule, low_water_temp_schedule, high_air_temp_schedule, low_air_temp_schedule)

        coil.setCondensationControlType(condensations[condensation_control_type])

        if condensation_control_dewpoint_offset is not None:
            coil.setCondensationControlDewpointOffset(condensation_control_dewpoint_offset)

        if name is not None:
            coil.setName(name)

        return coil

    @staticmethod
    def coil_heating_water(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            ufactor_times_area=None,
            max_water_flow_rate=None,
            performance_input_method=None,
            rated_capacity=None,
            inlet_water_temp=None,
            inlet_air_temp=None,
            outlet_water_temp=None,
            outlet_air_temp=None,
            ratio_air_water_convection=None):

        coil = openstudio.openstudiomodel.CoilHeatingWater(model)
        if name is not None:
            coil.setName(name)

        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if ufactor_times_area is not None:
            coil.setUFactorTimesAreaValue(ufactor_times_area)
        else:
            coil.autosizeUFactorTimesAreaValue()

        if max_water_flow_rate is not None:
            coil.setMaximumWaterFlowRate(max_water_flow_rate)
        else:
            coil.autosizeMaximumWaterFlowRate()

        if performance_input_method is not None:
            coil.setPerformanceInputMethod(performance_input_method)

        if rated_capacity is not None:
            coil.setRatedCapacity(rated_capacity)
        else:
            coil.autosizeRatedCapacity()

        if inlet_water_temp is not None:
            coil.setRatedInletWaterTemperature(inlet_water_temp)

        if inlet_air_temp is not None:
            coil.setRatedInletAirTemperature(inlet_air_temp)

        if outlet_water_temp is not None:
            coil.setRatedOutletWaterTemperature(outlet_water_temp)

        if outlet_air_temp is not None:
            coil.setRatedOutletAirTemperature(outlet_air_temp)

        if ratio_air_water_convection is not None:
            coil.setRatedRatioForAirAndWaterConvection(ratio_air_water_convection)

        return coil

    @staticmethod
    def coil_heating_dx_single_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            capacity=None,
            cop=None,
            rated_air_flow_rate=None,
            supply_fan_power_per_flow_2017=None,
            supply_fan_power_per_flow_2023=None,
            min_outdoor_air_temp_compressor_operation=None,
            max_outdoor_air_temp_defrost_operation=None,
            crankcase_heater_capacity=None,
            max_outdoor_air_temp_crankcase_operation=None,
            defrost_strategy: str = None,
            defrost_control: str = None,
            defrost_time_period_fraction=None,
            resistive_defrost_heater_capacity=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            capacity_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            cop_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            plr_curve: openstudio.openstudiomodel.CurveQuadratic = None):

        coil = openstudio.openstudiomodel.CoilHeatingDXSingleSpeed(model)
        if name is not None:
            coil.setName(name)

        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if capacity is not None:
            coil.setRatedTotalHeatingCapacity(capacity)
        else:
            coil.autosizeRatedTotalHeatingCapacity()

        if cop is not None:
            coil.setRatedCOP(cop)

        if rated_air_flow_rate is not None:
            coil.setRatedAirFlowRate(rated_air_flow_rate)
        else:
            coil.autosizeRatedAirFlowRate()

        if supply_fan_power_per_flow_2017 is not None:
            coil.setRatedSupplyFanPowerPerVolumeFlowRate2017(supply_fan_power_per_flow_2017)

        if supply_fan_power_per_flow_2023 is not None:
            coil.setRatedSupplyFanPowerPerVolumeFlowRate2023(supply_fan_power_per_flow_2023)

        if min_outdoor_air_temp_compressor_operation is not None:
            coil.setMinimumOutdoorDryBulbTemperatureforCompressorOperation(min_outdoor_air_temp_compressor_operation)

        if max_outdoor_air_temp_defrost_operation is not None:
            coil.setMaximumOutdoorDryBulbTemperatureforDefrostOperation(max_outdoor_air_temp_defrost_operation)

        if max_outdoor_air_temp_crankcase_operation is not None:
            coil.setMaximumOutdoorDryBulbTemperatureforCrankcaseHeaterOperation(
                max_outdoor_air_temp_crankcase_operation)

        if crankcase_heater_capacity is not None:
            coil.setCrankcaseHeaterCapacity(crankcase_heater_capacity)

        if defrost_strategy is not None:
            coil.setDefrostStrategy(defrost_strategy)

        if defrost_control is not None:
            coil.setDefrostControl(defrost_control)

        if defrost_time_period_fraction is not None:
            coil.setDefrostTimePeriodFraction(defrost_time_period_fraction)

        if resistive_defrost_heater_capacity is not None:
            coil.setResistiveDefrostHeaterCapacity(resistive_defrost_heater_capacity)

        if capacity_temperature_curve is not None:
            coil.setTotalHeatingCapacityFunctionofTemperatureCurve(capacity_temperature_curve)
        if capacity_flow_curve is not None:
            coil.setTotalHeatingCapacityFunctionofFlowFractionCurve(capacity_flow_curve)
        if cop_temperature_curve is not None:
            coil.setEnergyInputRatioFunctionofTemperatureCurve(cop_temperature_curve)
        if cop_flow_curve is not None:
            coil.setEnergyInputRatioFunctionofFlowFractionCurve(cop_flow_curve)
        if plr_curve is not None:
            coil.setPartLoadFractionCorrelationCurve(plr_curve)

        return coil

    @staticmethod
    def coil_heating_vrf(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            capacity=None,
            rated_air_flow_rate=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            capacity_flow_curve: openstudio.openstudiomodel.CurveQuadratic = None):

        coil = openstudio.openstudiomodel.CoilHeatingDXVariableRefrigerantFlow(model)

        if name is not None:
            coil.setName(name)
        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if capacity is not None:
            coil.setRatedTotalHeatingCapacity(capacity)
        else:
            coil.autosizeRatedTotalHeatingCapacity()

        if rated_air_flow_rate is not None:
            coil.setRatedAirFlowRate(rated_air_flow_rate)
        else:
            coil.autosizeRatedAirFlowRate()

        if capacity_temperature_curve is not None:
            coil.setHeatingCapacityRatioModifierFunctionofTemperatureCurve(capacity_temperature_curve)
        if capacity_flow_curve is not None:
            coil.setHeatingCapacityModifierFunctionofFlowFractionCurve(capacity_flow_curve)

        return coil

    @staticmethod
    def coil_heating_electric(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            efficiency=None,
            capacity=None):

        coil = openstudio.openstudiomodel.CoilHeatingElectric(model)
        if name is not None:
            coil.setName(name)

        if schedule is not None:
            coil.setAvailabilitySchedule(schedule)

        if efficiency is not None:
            coil.setEfficiency(efficiency)

        if capacity is not None:
            coil.setNominalCapacity(capacity)
        else:
            coil.autosizeNominalCapacity()

        return coil

    @staticmethod
    def coil_heating_gas(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            efficiency=None,
            capacity=None,
            parasitic_electric_load=None,
            parasitic_gas_load=None,
            fuel_type: str = "NaturalGas"):

        coil = openstudio.openstudiomodel.CoilHeatingGas(model)
        if name is not None:
            coil.setName(name)

        if efficiency is not None:
            coil.setGasBurnerEfficiency(efficiency)

        if capacity is not None:
            coil.setNominalCapacity(capacity)
        else:
            coil.autosizeNominalCapacity()

        if parasitic_electric_load is not None:
            coil.setParasiticElectricLoad(parasitic_electric_load)

        if parasitic_gas_load is not None:
            coil.setParasiticGasLoad(parasitic_gas_load)

        coil.setFuelType(fuel_type)

        return coil

    @staticmethod
    def coil_heating_four_pipe_beam(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            heating_capacity_per_beam_length=None,
            room_air_hot_water_temp_difference=None,
            hot_water_flow_rate_per_beam_length=None,
            capacity_temp_difference_factor_curve=None,
            capacity_air_flow_factor_curve=None,
            capacity_hot_water_flow_factor_curve=None):

        coil = openstudio.openstudiomodel.CoilHeatingFourPipeBeam(model)

        if name is not None:
            coil.setName(name)

        if heating_capacity_per_beam_length is not None:
            coil.setBeamRatedHeatingCapacityperBeamLength(heating_capacity_per_beam_length)
        if room_air_hot_water_temp_difference is not None:
            coil.setBeamRatedHeatingRoomAirHotWaterTemperatureDifference(room_air_hot_water_temp_difference)
        if hot_water_flow_rate_per_beam_length is not None:
            coil.setBeamRatedHotWaterVolumeFlowRateperBeamLength(hot_water_flow_rate_per_beam_length)

        if capacity_temp_difference_factor_curve is not None:
            coil.setBeamHeatingCapacityTemperatureDifferenceModificationFactorCurve(
                capacity_temp_difference_factor_curve)
        if capacity_air_flow_factor_curve is not None:
            coil.setBeamHeatingCapacityAirFlowModificationFactorCurve(capacity_air_flow_factor_curve)
        if capacity_hot_water_flow_factor_curve is not None:
            coil.setBeamHeatingCapacityHotWaterFlowModificationFactorCurve(capacity_hot_water_flow_factor_curve)

        return coil

    @staticmethod
    def coil_heating_low_temperature_radiant_variable_flow(
            model: openstudio.openstudiomodel.Model,
            heating_control_temp_schedule=None,
            capacity_method: int = 1,
            design_capacity=None,
            capacity_per_floor_area=None,
            fraction_of_autosized_capacity=None,
            max_hot_water_flow=None,
            heating_control_throttling_range=None,
            name: str = None):

        """
        -Capacity_method: \n
        1.CoolingDesignCapacity 2.CapacityPerFloorArea 3.FractionOfAutosizedCoolingCapacity \n
        """

        cap_methods = {1: "CoolingDesignCapacity", 2: "CapacityPerFloorArea", 3: "FractionOfAutosizedCoolingCapacity"}

        if heating_control_temp_schedule is not None:
            schedule = heating_control_temp_schedule
        else:
            type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 50)
            schedule = ScheduleTool.schedule_ruleset(model, 15, type_limit, "Var Vol Rad Htg Air Temp Sch")

        coil = openstudio.openstudiomodel.CoilHeatingLowTempRadiantVarFlow(model, schedule)

        coil.setHeatingDesignCapacityMethod(cap_methods[capacity_method])

        if design_capacity is not None:
            coil.setHeatingDesignCapacity(design_capacity)
        else:
            coil.autosizeHeatingDesignCapacity()

        if capacity_per_floor_area is not None:
            coil.setHeatingDesignCapacityPerFloorArea(capacity_per_floor_area)

        if fraction_of_autosized_capacity is not None:
            coil.setFractionofAutosizedHeatingDesignCapacity(fraction_of_autosized_capacity)

        if max_hot_water_flow is not None:
            coil.setMaximumHotWaterFlow(max_hot_water_flow)
        else:
            coil.autosizedMaximumHotWaterFlow()

        if heating_control_throttling_range is not None:
            coil.setHeatingControlThrottlingRange(heating_control_throttling_range)

        if name is not None:
            coil.setName(name)

        return coil

    @staticmethod
    def coil_heating_low_temperature_radiant_constant_flow(
            model: openstudio.openstudiomodel.Model,
            heating_high_water_temp_schedule=None,
            heating_low_water_temp_schedule=None,
            heating_high_control_temp_schedule=None,
            heating_low_control_temp_schedule=None,
            heating_high_water_temp=None,
            heating_low_water_temp=None,
            heating_high_control_temp=None,
            heating_low_control_temp=None,
            name: str = None):

        type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 50)
        if heating_high_water_temp_schedule is not None:
            high_water_temp_schedule = heating_high_water_temp_schedule
        else:
            if heating_high_water_temp is not None:
                high_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, heating_high_water_temp, type_limit, "Const Vol Rad Htg Hi Wtr Temp Sch")
            else:
                high_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 50, type_limit, "Const Vol Rad Htg Hi Wtr Temp Sch")

        if heating_low_water_temp_schedule is not None:
            low_water_temp_schedule = heating_low_water_temp_schedule
        else:
            if heating_low_water_temp is not None:
                low_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, heating_low_water_temp, type_limit, "Const Vol Rad Htg Low Wtr Temp Sch")
            else:
                low_water_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 30, type_limit, "Const Vol Rad Htg Low Wtr Temp Sch")

        if heating_high_control_temp_schedule is not None:
            high_air_temp_schedule = heating_high_control_temp_schedule
        else:
            if heating_high_control_temp is not None:
                high_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, heating_high_control_temp, type_limit, "Const Vol Rad Htg Hi Air Temp Sch")
            else:
                high_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 20, type_limit, "Const Vol Rad Htg Hi Air Temp Sch")

        if heating_low_control_temp_schedule is not None:
            low_air_temp_schedule = heating_low_control_temp_schedule
        else:
            if heating_low_control_temp is not None:
                low_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, heating_low_control_temp, type_limit, "Const Vol Rad Htg Low Air Temp Sch")
            else:
                low_air_temp_schedule = ScheduleTool.schedule_ruleset(
                    model, 17, type_limit, "Const Vol Rad Htg Low Air Temp Sch")

        coil = openstudio.openstudiomodel.CoilHeatingLowTempRadiantConstFlow(
            model, high_water_temp_schedule, low_water_temp_schedule, high_air_temp_schedule, low_air_temp_schedule)

        if name is not None:
            coil.setName(name)

        return coil

    # Fan
    # ********************************************************************************
    @staticmethod
    def fan_variable_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fan_total_efficiency=None,
            pressure_rise=None,
            max_flow_rate=None,
            power_min_flow_rate_input_method: str = "FixedFlowRate",
            power_min_flow_rate_fraction=None,
            power_min_flow_rate=None,
            motor_efficiency=None,
            motor_in_airstream_fraction=None,
            fan_curve_coeff=None):

        """
        -Options for "power_min_flow_rate_input_method":
        1: Fraction, 2: FixedFlowRate
        """

        fan = openstudio.openstudiomodel.FanVariableVolume(model)
        if name is not None:
            fan.setName(name)

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if pressure_rise is not None:
            fan.setPressureRise(pressure_rise)

        if max_flow_rate is not None:
            fan.setMaximumFlowRate(max_flow_rate)
        else:
            fan.autosizeMaximumFlowRate()

        fan.setFanPowerMinimumFlowRateInputMethod(power_min_flow_rate_input_method)

        if power_min_flow_rate_fraction is not None:
            fan.setFanPowerMinimumFlowFraction(power_min_flow_rate_fraction)

        if power_min_flow_rate is not None:
            fan.setFanPowerMinimumAirFlowRate(power_min_flow_rate)

        if motor_efficiency is not None:
            fan.setMotorEfficiency(motor_efficiency)

        if motor_in_airstream_fraction is not None:
            fan.setMotorInAirstreamFraction(motor_in_airstream_fraction)

        if fan_curve_coeff is not None:
            if isinstance(fan_curve_coeff, list) and len(fan_curve_coeff) == 4:
                fan.setFanPowerCoefficient1(fan_curve_coeff[0])
                fan.setFanPowerCoefficient2(fan_curve_coeff[1])
                fan.setFanPowerCoefficient3(fan_curve_coeff[2])
                fan.setFanPowerCoefficient4(fan_curve_coeff[3])
                if len(fan_curve_coeff) > 4:
                    fan.setFanPowerCoefficient5(fan_curve_coeff[4])

        return fan

    @staticmethod
    def fan_constant_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fan_total_efficiency=None,
            pressure_rise=None,
            max_flow_rate=None,
            motor_efficiency=None,
            motor_in_airstream_fraction=None):

        fan = openstudio.openstudiomodel.FanConstantVolume(model)
        if name is not None:
            fan.setName(name)

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if pressure_rise is not None:
            fan.setPressureRise(pressure_rise)

        if max_flow_rate is not None:
            fan.setMaximumFlowRate(max_flow_rate)
        else:
            fan.autosizeMaximumFlowRate()

        if motor_efficiency is not None:
            fan.setMotorEfficiency(motor_efficiency)

        if motor_in_airstream_fraction is not None:
            fan.setMotorInAirstreamFraction(motor_in_airstream_fraction)

        return fan

    @staticmethod
    def fan_on_off(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            pressure_rise=None,
            max_flow_rate=None,
            fan_total_efficiency=None,
            fan_efficiency=None,
            motor_efficiency=None,
            motor_in_airstream_fraction=None,
            power_ratio_function_speed_ratio_curve=None,
            efficiency_ratio_function_speed_ratio_curve=None):

        fan = openstudio.openstudiomodel.FanOnOff(model)
        if name is not None:
            fan.setName(name)

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if pressure_rise is not None:
            fan.setPressureRise(pressure_rise)

        if max_flow_rate is not None:
            fan.setMaximumFlowRate(max_flow_rate)
        else:
            fan.autosizeMaximumFlowRate()

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if fan_efficiency is not None:
            fan.setFanEfficiency(fan_efficiency)

        if motor_efficiency is not None:
            fan.setMotorEfficiency(motor_efficiency)

        if motor_in_airstream_fraction is not None:
            fan.setMotorInAirstreamFraction(motor_in_airstream_fraction)

        if power_ratio_function_speed_ratio_curve is not None:
            try:
                fan.setFanPowerRatioFunctionofSpeedRatioCurve(power_ratio_function_speed_ratio_curve)
            except TypeError:
                print("Curve type can only be exponent curve")

        if efficiency_ratio_function_speed_ratio_curve is not None:
            try:
                fan.setFanEfficiencyRatioFunctionofSpeedRatioCurve(efficiency_ratio_function_speed_ratio_curve)
            except TypeError:
                print("Curve type can only be quadratic or cubic")

        return fan

    @staticmethod
    def fan_system_model_variable(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            speed_control_method="Continuous",  # Continuous, Discrete
            electric_power_min_flow_rate_fraction=None,
            fan_total_efficiency=None,
            pressure_rise=None,
            max_flow_rate=None,
            design_electric_power=None,
            design_power_sizing_method: str = None,
            electric_power_per_flow_rate=None,
            electric_power_per_flow_per_pressure=None,
            electric_power_function_flow_fraction_curve: openstudio.openstudiomodel.CurveQuartic = None,
            night_ventilation_pressure_rise=None,
            night_ventilation_flow_fraction=None,
            motor_loss_zone=None,
            motor_loss_radiative_fraction=None,
            motor_efficiency=None,
            motor_in_airstream_fraction=None):

        fan = openstudio.openstudiomodel.FanSystemModel(model)
        if name is not None:
            fan.setName(name)

        if speed_control_method is not None:
            fan.setSpeedControlMethod(speed_control_method)

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if pressure_rise is not None:
            fan.setDesignPressureRise(pressure_rise)

        if electric_power_min_flow_rate_fraction is not None:
            fan.setElectricPowerMinimumFlowRateFraction(electric_power_min_flow_rate_fraction)
        else:
            fan.setElectricPowerMinimumFlowRateFraction(0)

        if max_flow_rate is not None:
            fan.setDesignMaximumAirFlowRate(max_flow_rate)
        else:
            fan.autosizeDesignMaximumAirFlowRate()

        if design_electric_power is not None:
            fan.setDesignElectricPowerConsumption(design_electric_power)
        else:
            fan.autosizeDesignElectricPowerConsumption()

        # Options:
        # ********************************************************
        # PowerPerFlow
        # PowerPerFlowPerPressure
        # TotalEfficiencyAndPressure
        if design_power_sizing_method is not None:
            fan.setDesignPowerSizingMethod(design_power_sizing_method)

        if electric_power_per_flow_rate is not None:
            fan.setElectricPowerPerUnitFlowRate(electric_power_per_flow_rate)

        if electric_power_per_flow_per_pressure is not None:
            fan.setElectricPowerPerUnitFlowRatePerUnitPressure(electric_power_per_flow_per_pressure)

        if electric_power_function_flow_fraction_curve is not None:
            fan.setElectricPowerFunctionofFlowFractionCurve(electric_power_function_flow_fraction_curve)
        else:
            curve = Curve.quartic(model, 0.04076, 0.088, -0.0729, 0.9437, 0, 0, 1, 0, 1)
            fan.setElectricPowerFunctionofFlowFractionCurve(curve)

        if night_ventilation_pressure_rise is not None:
            fan.setNightVentilationModePressureRise(night_ventilation_pressure_rise)

        if night_ventilation_flow_fraction is not None:
            fan.setNightVentilationModeFlowFraction(night_ventilation_flow_fraction)

        if motor_loss_zone is not None:
            fan.setMotorLossZone(motor_loss_zone)

        if motor_loss_radiative_fraction is not None:
            fan.setMotorLossRadiativeFraction(motor_loss_radiative_fraction)

        if motor_efficiency is not None:
            fan.setMotorEfficiency(motor_efficiency)

        if motor_in_airstream_fraction is not None:
            fan.setMotorInAirStreamFraction(motor_in_airstream_fraction)

        return fan

    @staticmethod
    def fan_system_model_constant(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            speed_control_method="Discrete",
            number_of_speed=1.0,
            electric_power_min_flow_rate_fraction=None,
            fan_total_efficiency=None,
            pressure_rise=None,
            max_flow_rate=None,
            design_electric_power=None,
            design_power_sizing_method: str = None,
            electric_power_per_flow_rate=None,
            electric_power_per_flow_per_pressure=None,
            night_ventilation_pressure_rise=None,
            night_ventilation_flow_fraction=None,
            motor_loss_zone=None,
            motor_loss_radiative_fraction=None,
            motor_efficiency=None,
            motor_in_airstream_fraction=None):

        """
        -Options for "speed_control_method":
        1: Continuous, 2: Discrete

        -Options for "design_power_sizing_method":
        1: PowerPerFlow, 2: PowerPerFlowPerPressure 3: TotalEfficiencyAndPressure
        """

        fan = openstudio.openstudiomodel.FanSystemModel(model)
        if name is not None:
            fan.setName(name)

        fan.setSpeedControlMethod(speed_control_method)
        if number_of_speed == 1:
            fan.addSpeed(1.0, 1.0)
        elif number_of_speed > 1:
            for i in range(int(number_of_speed)):
                fan.addSpeed((i + 1) / number_of_speed, (i + 1) / number_of_speed)
        else:
            raise ValueError("number of speed cannot be less than 0")

        if fan_total_efficiency is not None:
            fan.setFanTotalEfficiency(fan_total_efficiency)

        if pressure_rise is not None:
            fan.setDesignPressureRise(pressure_rise)

        if electric_power_min_flow_rate_fraction is not None:
            fan.setElectricPowerMinimumFlowRateFraction(electric_power_min_flow_rate_fraction)
        else:
            fan.setElectricPowerMinimumFlowRateFraction(0.2)

        if max_flow_rate is not None:
            fan.setDesignMaximumAirFlowRate(max_flow_rate)
        else:
            fan.autosizeDesignMaximumAirFlowRate()

        if design_electric_power is not None:
            fan.setDesignElectricPowerConsumption(design_electric_power)
        else:
            fan.autosizeDesignElectricPowerConsumption()

        if design_power_sizing_method is not None:
            fan.setDesignPowerSizingMethod(design_power_sizing_method)

        if electric_power_per_flow_rate is not None:
            fan.setElectricPowerPerUnitFlowRate(electric_power_per_flow_rate)

        if electric_power_per_flow_per_pressure is not None:
            fan.setElectricPowerPerUnitFlowRatePerUnitPressure(electric_power_per_flow_per_pressure)

        if night_ventilation_pressure_rise is not None:
            fan.setNightVentilationModePressureRise(night_ventilation_pressure_rise)

        if night_ventilation_flow_fraction is not None:
            fan.setNightVentilationModeFlowFraction(night_ventilation_flow_fraction)

        if motor_loss_zone is not None:
            fan.setMotorLossZone(motor_loss_zone)

        if motor_loss_radiative_fraction is not None:
            fan.setMotorLossRadiativeFraction(motor_loss_radiative_fraction)

        if motor_efficiency is not None:
            fan.setMotorEfficiency(motor_efficiency)

        if motor_in_airstream_fraction is not None:
            fan.setMotorInAirStreamFraction(motor_in_airstream_fraction)

        return fan

    # Heat exchanger:
    # ***************************************************************************
    @staticmethod
    def heat_exchanger_air_to_air(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            supply_air_flow_rate=None,
            sensible_only: bool = False,
            sensible_effectiveness_100_heating=None,
            latent_effectiveness_100_heating=None,
            sensible_effectiveness_75_heating=None,
            latent_effectiveness_75_heating=None,
            sensible_effectiveness_100_cooling=None,
            latent_effectiveness_100_cooling=None,
            sensible_effectiveness_75_cooling=None,
            latent_effectiveness_75_cooling=None,
            nominal_electric_power=None,
            supply_air_outlet_temp_control: bool = False,
            heat_exchanger_type: int = 0,
            frost_control_type:int = 0,
            threshold_temp=None,
            initial_defrost_time_fraction=None,
            rate_of_defrost_time_fraction_increase=None,
            economizer_lockout: bool = False):

        """
        -Heat_exchanger_type: 1.Plate 2.Rotary \n
        -Frost_control_type: \n
        1.None 2.ExhaustAirRecirculation 3.ExhaustOnly 4.MinimumExhaustTemperature
        """

        types = {0: "Plate", 1: "Rotary"}
        frost_types = {0: "None", 1: "ExhaustAirRecirculation", 2: "ExhaustOnly", 3: "MinimumExhaustTemperature"}

        heat_exchanger = openstudio.openstudiomodel.HeatExchangerAirToAirSensibleAndLatent(model)
        if name is not None:
            heat_exchanger.setName(name)

        if supply_air_flow_rate is not None:
            heat_exchanger.setNominalSupplyAirFlowRate(supply_air_flow_rate)
        else:
            heat_exchanger.autosizeNominalSupplyAirFlowRate()

        if sensible_effectiveness_100_heating is not None:
            heat_exchanger.setSensibleEffectivenessat100HeatingAirFlow(sensible_effectiveness_100_heating)

        if sensible_only:
            heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(0)
        else:
            if latent_effectiveness_100_heating is not None:
                heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(latent_effectiveness_100_heating)

        if sensible_effectiveness_75_heating is not None:
            heat_exchanger.setSensibleEffectivenessat75HeatingAirFlow(sensible_effectiveness_75_heating)

        if sensible_only:
            heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(0)
        else:
            if latent_effectiveness_75_heating is not None:
                heat_exchanger.setLatentEffectivenessat75HeatingAirFlow(latent_effectiveness_75_heating)

        if sensible_effectiveness_100_cooling is not None:
            heat_exchanger.setSensibleEffectivenessat100CoolingAirFlow(sensible_effectiveness_100_cooling)

        if sensible_only:
            heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(0)
        else:
            if latent_effectiveness_100_cooling is not None:
                heat_exchanger.setLatentEffectivenessat100CoolingAirFlow(latent_effectiveness_100_cooling)

        if sensible_effectiveness_75_cooling is not None:
            heat_exchanger.setSensibleEffectivenessat75CoolingAirFlow(sensible_effectiveness_75_cooling)

        if sensible_only:
            heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(0)
        else:
            if latent_effectiveness_75_cooling is not None:
                heat_exchanger.setLatentEffectivenessat75CoolingAirFlow(latent_effectiveness_75_cooling)

        if nominal_electric_power is not None:
            heat_exchanger.setNominalElectricPower(nominal_electric_power)

        if supply_air_outlet_temp_control is not None:
            heat_exchanger.setSupplyAirOutletTemperatureControl(supply_air_outlet_temp_control)

        if heat_exchanger_type is not None:
            heat_exchanger.setHeatExchangerType(types[heat_exchanger_type])

        if frost_control_type is not None:
            heat_exchanger.setFrostControlType(frost_types[frost_control_type])

        if initial_defrost_time_fraction is not None:
            heat_exchanger.setInitialDefrostTimeFraction(initial_defrost_time_fraction)

        if rate_of_defrost_time_fraction_increase is not None:
            heat_exchanger.setRateofDefrostTimeFractionIncrease(rate_of_defrost_time_fraction_increase)

        if economizer_lockout is not None:
            heat_exchanger.setEconomizerLockout(economizer_lockout)

        # Default value for threshold temperature:
        if threshold_temp is not None:
            temp = threshold_temp
        else:
            if frost_control_type == 2:
                if heat_exchanger_type == 0:
                    temp = -1.1 if sensible_only else -12.2
                else:
                    temp = -12.2 if sensible_only else -23.3
            elif frost_control_type == 3:
                if heat_exchanger_type == 0:
                    temp = -1.1 if sensible_only else -12.2
                else:
                    temp = -12.2 if sensible_only else -23.3
            elif frost_control_type == 4:
                temp = 1.7
            else:
                temp = 1.7

        heat_exchanger.setThresholdTemperature(temp)

        return heat_exchanger

    @staticmethod
    def heat_exchanger_air_to_air_simplified(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            supply_air_flow_rate=None,
            sensible_only: bool = False,
            efficiency=None,
            nominal_electric_power=None,
            supply_air_outlet_temp_control: bool = False,
            heat_exchanger_type=None,
            frost_control_type: int = 3,
            threshold_temp=None,
            economizer_lockout: bool = False):

        """
        -frost_control_type: \n
        1.None 2.ExhaustAirRecirculation 3.ExhaustOnly 4.MinimumExhaustTemperature
        """

        frost_types = {0: "None", 1: "ExhaustAirRecirculation", 2: "ExhaustOnly", 3: "MinimumExhaustTemperature"}

        heat_exchanger = openstudio.openstudiomodel.HeatExchangerAirToAirSensibleAndLatent(model)
        if name is not None:
            heat_exchanger.setName(name)

        if supply_air_flow_rate is not None:
            heat_exchanger.setNominalSupplyAirFlowRate(supply_air_flow_rate)
        else:
            heat_exchanger.autosizeNominalSupplyAirFlowRate()

        if efficiency is not None:
            if sensible_only:
                heat_exchanger.setSensibleEffectivenessat100HeatingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(0)
                heat_exchanger.setSensibleEffectivenessat75HeatingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat75HeatingAirFlow(0)
                heat_exchanger.setSensibleEffectivenessat100CoolingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat100CoolingAirFlow(0)
                heat_exchanger.setSensibleEffectivenessat75CoolingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat75CoolingAirFlow(0)
            else:
                heat_exchanger.setSensibleEffectivenessat100HeatingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat100HeatingAirFlow(efficiency)
                heat_exchanger.setSensibleEffectivenessat75HeatingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat75HeatingAirFlow(efficiency)
                heat_exchanger.setSensibleEffectivenessat100CoolingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat100CoolingAirFlow(efficiency)
                heat_exchanger.setSensibleEffectivenessat75CoolingAirFlow(efficiency)
                heat_exchanger.setLatentEffectivenessat75CoolingAirFlow(efficiency)

        if nominal_electric_power is not None:
            heat_exchanger.setNominalElectricPower(nominal_electric_power)

        if supply_air_outlet_temp_control is not None:
            heat_exchanger.setSupplyAirOutletTemperatureControl(supply_air_outlet_temp_control)

        if heat_exchanger_type is not None:
            heat_exchanger.setHeatExchangerType(heat_exchanger_type)

        if frost_control_type is not None:
            heat_exchanger.setFrostControlType(frost_types[frost_control_type])

        if economizer_lockout is not None:
            heat_exchanger.setEconomizerLockout(economizer_lockout)

        # Default value for threshold temperature:
        if threshold_temp is not None:
            temp = threshold_temp
        else:
            if frost_control_type == 2:
                if heat_exchanger_type == 0:
                    temp = -1.1 if sensible_only else -12.2
                else:
                    temp = -12.2 if sensible_only else -23.3
            elif frost_control_type == 3:
                if heat_exchanger_type == 0:
                    temp = -1.1 if sensible_only else -12.2
                else:
                    temp = -12.2 if sensible_only else -23.3
            elif frost_control_type == 4:
                temp = 1.7
            else:
                temp = 1.7

        heat_exchanger.setThresholdTemperature(temp)

        return heat_exchanger

    # Controller:
    # ***************************************************************************
    @staticmethod
    def controller_water_coil(
            controller: openstudio.openstudiomodel.ControllerWaterCoil,
            name: str = None,
            control_variable: int = 1,
            action: int = None,  # Normal, Reverse
            actuator_variable: str = None,
            convergence_tolerance=None,
            max_actuated_flow=None,
            min_actuated_flow=None):

        """
        -Control_variable: \n
        1.Temperature \n
        2.HumidityRatio \n
        3.TemperatureAndHumidityRatio \n

        -Action: 1.Normal 2.Reverse
        """

        control_variables = {1: "Temperature", 2: "HumidityRatio", 3: "TemperatureAndHumidityRatio"}
        actions = {1: "Normal", 2: "Reverse"}

        if controller is not None:

            if name is not None:
                controller.setName(name)

            controller.setControlVariable(control_variables[control_variable])

            if action is not None:
                controller.setAction(actions[action])

            if actuator_variable is not None:
                controller.setActuatorVariable(actuator_variable)

            if convergence_tolerance is not None:
                controller.setControllerConvergenceTolerance(convergence_tolerance)
            else:
                controller.autosizeControllerConvergenceTolerance()

            if max_actuated_flow is not None:
                controller.setMaximumActuatedFlow(max_actuated_flow)
            else:
                controller.autosizeMaximumActuatedFlow()

            if min_actuated_flow is not None:
                controller.setMinimumActuatedFlow(min_actuated_flow)
        else:
            raise ValueError("Controller input cannot be empty.")

    @staticmethod
    def controller_outdoor_air(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            min_outdoor_air_flow_rate=None,
            max_outdoor_air_flow_rate=None,
            economizer_control_type: int = 0,
            economizer_control_action_type: int = 0,
            max_limit_dry_bulb_temp=None,
            max_limit_enthalpy=None,
            max_limit_dewpoint_temp=None,
            min_limit_dry_bulb_temp=None,
            lockout_type: str = None,
            min_limit_type: str = None,
            min_outdoor_air_schedule=None,
            min_fraction_outdoor_air_schedule=None,
            max_fraction_outdoor_air_schedule=None,
            time_of_day_economizer_control_schedule=None,
            heat_recovery_bypass_control_type: str = None):

        """
        -Economizer Control Type: \n
        1.NoEconomizer \n
        2.FixedDryBulb \n
        3.FixedDewPointAndDryBulb \n
        4.FixedEnthalpy \n
        5.DifferentialDryBulb \n
        6.DifferentialEnthalpy \n
        7.DifferentialDryBulbAndEnthalpy \n
        8.ElectronicEnthalpy \n

        -Economizer Control Action Type: \n
        1.ModulateFlow \n
        2.MinimumFlowWithBypass
        """

        economizer_types = {0: "NoEconomizer", 1: "FixedDryBulb", 2: "FixedDewPointAndDryBulb", 3: "FixedEnthalpy",
                            4: "FixedEnthalpy", 5: "DifferentialDryBulb", 6: "DifferentialEnthalpy",
                            7: "DifferentialDryBulbAndEnthalpy", 8: "ElectronicEnthalpy"}
        economizer_action_types = {0: "ModulateFlow", 1: "MinimumFlowWithBypass"}

        controller = openstudio.openstudiomodel.ControllerOutdoorAir(model)
        if name is not None:
            controller.setName(name)

        if min_outdoor_air_flow_rate is not None:
            controller.setMinimumOutdoorAirFlowRate(min_outdoor_air_flow_rate)
        else:
            controller.autosizeMinimumOutdoorAirFlowRate()

        if max_outdoor_air_flow_rate is not None:
            controller.setMaximumOutdoorAirFlowRate(max_outdoor_air_flow_rate)
        else:
            controller.autosizeMaximumOutdoorAirFlowRate()
        if economizer_control_type != 0:
            controller.setEconomizerControlType(economizer_types[economizer_control_type])

        if economizer_control_action_type is not None:
            controller.setEconomizerControlActionType(economizer_action_types[economizer_control_action_type])

        if max_limit_dry_bulb_temp is not None:
            controller.setEconomizerMaximumLimitDryBulbTemperature(max_limit_dry_bulb_temp)

        if max_limit_enthalpy is not None:
            controller.setEconomizerMaximumLimitEnthalpy(max_limit_enthalpy)

        if max_limit_dewpoint_temp is not None:
            controller.setEconomizerMaximumLimitDewpointTemperature(max_limit_dewpoint_temp)

        if min_limit_dry_bulb_temp is not None:
            controller.setEconomizerMinimumLimitDryBulbTemperature(min_limit_dry_bulb_temp)

        if lockout_type is not None:
            controller.setLockoutType(lockout_type)

        if min_limit_type is not None:
            controller.setMinimumLimitType(min_limit_type)

        if min_outdoor_air_schedule is not None:
            controller.setMinimumOutdoorAirSchedule(min_outdoor_air_schedule)

        if max_fraction_outdoor_air_schedule is not None:
            controller.setMaximumFractionofOutdoorAirSchedule(max_fraction_outdoor_air_schedule)

        if min_fraction_outdoor_air_schedule is not None:
            controller.setMinimumFractionofOutdoorAirSchedule(min_fraction_outdoor_air_schedule)

        if time_of_day_economizer_control_schedule is not None:
            controller.setTimeofDayEconomizerControlSchedule(time_of_day_economizer_control_schedule)

        if heat_recovery_bypass_control_type is not None:
            controller.setHeatRecoveryBypassControlType(heat_recovery_bypass_control_type)

        return controller

    @staticmethod
    def controller_mechanical_ventilation(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            demand_control_ventilation: bool = False,
            system_outdoor_air_method: int = 0):

        """
        -system_outdoor_air_method: \n
        1.ZoneSum
        2.Standard62.1VentilationRateProcedure
        3.Standard62.1VentilationRateProcedureWithLimit
        4.IndoorAirQualityProcedure
        5.ProportionalControlBasedOnOccupancySchedule
        6.ProportionalControlBasedOnDesignOccupancy
        7.ProportionalControlBasedOnDesignOARate
        8.IndoorAirQualityProcedureGenericContaminant
        """

        oa_methods = {0: "ZoneSum", 1: "Standard62.1VentilationRateProcedure",
                      2: "Standard62.1VentilationRateProcedureWithLimit", 3: "IndoorAirQualityProcedure",
                      4: "IndoorAirQualityProcedure", 5: "ProportionalControlBasedOnOccupancySchedule",
                      6: "ProportionalControlBasedOnDesignOccupancy", 7: "ProportionalControlBasedOnDesignOARate",
                      8: "IndoorAirQualityProcedureGenericContaminant"}

        controller = openstudio.openstudiomodel.ControllerMechanicalVentilation(model)

        if name is not None:
            controller.setName(name)

        if schedule is not None:
            controller.setAvailabilitySchedule(schedule)

        controller.setDemandControlledVentilation(demand_control_ventilation)

        if system_outdoor_air_method is not None:
            controller.setSystemOutdoorAirMethod(oa_methods[system_outdoor_air_method])

        return controller
