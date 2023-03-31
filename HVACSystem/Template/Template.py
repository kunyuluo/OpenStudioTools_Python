import openstudio
from HVACSystem.HVACTools import HVACTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent
from HVACSystem.PerformanceCurves import Curve
from HVACSystem.SetpointManagers import SetpointManager


class Template:

    model_null_message = "Model cannot be empty"
    zone_null_message = "Please check the validity of the input thermal zones"

    @staticmethod
    def vrf_system(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            cooling_capacity=None,
            heating_capacity=None,
            cooling_cop=None,
            heating_cop=None,
            heating_capacity_sizing_ratio=None,
            min_outdoor_temp_cooling_mode=None,
            max_outdoor_temp_cooling_mode=None,
            min_outdoor_temp_heating_mode=None,
            max_outdoor_temp_heating_mode=None,
            min_heat_pump_part_load_ratio=None,
            zone_for_master_thermostat_location: openstudio.openstudiomodel.ThermalZone = None,
            master_thermostat_priority_control_type: str = None,
            thermostat_priority_schedule=None,
            heat_pump_waste_heat_recovery: bool = False,
            pipe_length_for_piping_correction_factor_cooling=None,
            vertical_height_for_piping_correction_factor=None,
            piping_correction_factor_for_height_cooling=None,
            pipe_length_for_piping_correction_factor_heating=None,
            piping_correction_factor_for_height_heating=None,
            crankcase_heater_power_per_compressor=None,
            number_of_compressor=None,
            defrost_strategy: str = None,
            defrost_control: str = None,
            condenser_type: str = None,
            water_condenser_volume_flow_rate=None,
            evaporative_condenser_effectiveness=None,
            evaporative_condenser_air_flow_rate=None,
            evaporative_condenser_pump_power=None,
            fuel_type: str = None,
            min_outdoor_temp_heat_recovery=None,
            max_outdoor_temp_heat_recovery=None,
            initial_heat_recovery_cooling_capacity_fraction=None,
            heat_recovery_cooling_capacity_time_constant=None,
            initial_heat_recovery_cooling_energy_fraction=None,
            heat_recovery_cooling_energy_time_constant=None,
            initial_heat_recovery_heating_capacity_fraction=None,
            heat_recovery_heating_capacity_time_constant=None,
            initial_heat_recovery_heating_energy_fraction=None,
            heat_recovery_heating_energy_time_constant=None,
            performance_curve_set=None,
            terminals=None):

        """
        -master_thermostat_priority_control_type: (Default is LoadPriority)
            1: LoadPriority \n
            2: ZonePriority \n
            3: ThermostatOffsetPriority \n
            4: MasterThermostatPriority \n
            5: Scheduled
        -defrost_strategy: 1: ReverseCycle, 2: Resistive \n
        -defrost_control: 1: Timed, 2: OnDemand \n
        -condenser_type: 1: AirCooled, 2: WaterCooled, 3: EvapCooled
        """

        vrf_sys = openstudio.openstudiomodel.AirConditionerVariableRefrigerantFlow(model)

        if name is not None:
            vrf_sys.setName(name)

        if schedule is not None:
            vrf_sys.setAvailabilitySchedule(schedule)

        if cooling_capacity is not None:
            vrf_sys.setGrossRatedTotalCoolingCapacity(cooling_capacity)
        else:
            vrf_sys.autosizeGrossRatedTotalCoolingCapacity()
        if heating_capacity is not None:
            vrf_sys.setGrossRatedHeatingCapacity(heating_capacity)
        else:
            vrf_sys.autosizeGrossRatedHeatingCapacity()

        if cooling_cop is not None:
            vrf_sys.setGrossRatedCoolingCOP(cooling_cop)
        if heating_cop is not None:
            vrf_sys.setRatedHeatingCOP(heating_cop)
        if heating_capacity_sizing_ratio is not None:
            vrf_sys.setRatedHeatingCapacitySizingRatio(heating_capacity_sizing_ratio)

        if min_outdoor_temp_cooling_mode is not None:
            vrf_sys.setMinimumOutdoorTemperatureinCoolingMode(min_outdoor_temp_cooling_mode)
        if min_outdoor_temp_heating_mode is not None:
            vrf_sys.setMinimumOutdoorTemperatureinHeatingMode(min_outdoor_temp_heating_mode)
        if max_outdoor_temp_cooling_mode is not None:
            vrf_sys.setMaximumOutdoorTemperatureinCoolingMode(max_outdoor_temp_cooling_mode)
        if max_outdoor_temp_heating_mode is not None:
            vrf_sys.setMaximumOutdoorTemperatureinHeatingMode(max_outdoor_temp_heating_mode)

        if min_heat_pump_part_load_ratio is not None:
            vrf_sys.setMinimumHeatPumpPartLoadRatio(min_heat_pump_part_load_ratio)

        if zone_for_master_thermostat_location is not None:
            vrf_sys.setZoneforMasterThermostatLocation(zone_for_master_thermostat_location)

        # Options:
        # ******************************************************************
        # LoadPriority
        # ZonePriority
        # ThermostatOffsetPriority
        # MasterThermostatPriority
        # Scheduled
        if master_thermostat_priority_control_type is not None:
            vrf_sys.setMasterThermostatPriorityControlType(master_thermostat_priority_control_type)

        if thermostat_priority_schedule is not None:
            vrf_sys.setThermostatPrioritySchedule(thermostat_priority_schedule)

        if heat_pump_waste_heat_recovery:
            vrf_sys.setHeatPumpWasteHeatRecovery(heat_pump_waste_heat_recovery)

        if pipe_length_for_piping_correction_factor_cooling is not None:
            vrf_sys.setEquivalentPipingLengthusedforPipingCorrectionFactorinCoolingMode(
                pipe_length_for_piping_correction_factor_cooling)

        if vertical_height_for_piping_correction_factor is not None:
            vrf_sys.setVerticalHeightusedforPipingCorrectionFactor(vertical_height_for_piping_correction_factor)

        if piping_correction_factor_for_height_cooling is not None:
            vrf_sys.setPipingCorrectionFactorforHeightinCoolingModeCoefficient(
                piping_correction_factor_for_height_cooling)

        if pipe_length_for_piping_correction_factor_heating is not None:
            vrf_sys.setEquivalentPipingLengthusedforPipingCorrectionFactorinHeatingMode(
                pipe_length_for_piping_correction_factor_heating)

        if piping_correction_factor_for_height_heating is not None:
            vrf_sys.setPipingCorrectionFactorforHeightinHeatingModeCoefficient(
                piping_correction_factor_for_height_heating)

        if crankcase_heater_power_per_compressor is not None:
            vrf_sys.setCrankcaseHeaterPowerperCompressor(crankcase_heater_power_per_compressor)
        if number_of_compressor is not None:
            vrf_sys.setNumberofCompressors(number_of_compressor)

        if defrost_strategy is not None:
            vrf_sys.setDefrostStrategy(defrost_strategy)
        if defrost_control is not None:
            vrf_sys.setDefrostControl(defrost_control)

        if condenser_type is not None:
            vrf_sys.setCondenserType(condenser_type)

        if water_condenser_volume_flow_rate is not None:
            vrf_sys.setWaterCondenserVolumeFlowRate(water_condenser_volume_flow_rate)
        if evaporative_condenser_effectiveness is not None:
            vrf_sys.setEvaporativeCondenserEffectiveness(evaporative_condenser_effectiveness)
        if evaporative_condenser_air_flow_rate is not None:
            vrf_sys.setEvaporativeCondenserAirFlowRate(evaporative_condenser_air_flow_rate)
        if evaporative_condenser_pump_power is not None:
            vrf_sys.setEvaporativeCondenserPumpRatedPowerConsumption(evaporative_condenser_pump_power)

        if fuel_type is not None:
            vrf_sys.setFuelType(fuel_type)

        if min_outdoor_temp_heat_recovery is not None:
            vrf_sys.setMinimumOutdoorTemperatureinHeatRecoveryMode(min_outdoor_temp_heat_recovery)
        if max_outdoor_temp_heat_recovery is not None:
            vrf_sys.setMaximumOutdoorTemperatureinHeatRecoveryMode(max_outdoor_temp_heat_recovery)

        if initial_heat_recovery_cooling_capacity_fraction is not None:
            vrf_sys.setInitialHeatRecoveryCoolingCapacityFraction(initial_heat_recovery_cooling_capacity_fraction)
        if initial_heat_recovery_cooling_energy_fraction is not None:
            vrf_sys.setInitialHeatRecoveryCoolingEnergyFraction(initial_heat_recovery_cooling_energy_fraction)
        if heat_recovery_cooling_capacity_time_constant is not None:
            vrf_sys.setHeatRecoveryCoolingCapacityTimeConstant(heat_recovery_cooling_capacity_time_constant)
        if heat_recovery_cooling_energy_time_constant is not None:
            vrf_sys.setHeatRecoveryCoolingEnergyTimeConstant(heat_recovery_cooling_energy_time_constant)

        if initial_heat_recovery_heating_capacity_fraction is not None:
            vrf_sys.setInitialHeatRecoveryHeatingCapacityFraction(initial_heat_recovery_heating_capacity_fraction)
        if initial_heat_recovery_heating_energy_fraction is not None:
            vrf_sys.setInitialHeatRecoveryHeatingEnergyFraction(initial_heat_recovery_heating_energy_fraction)
        if heat_recovery_heating_capacity_time_constant is not None:
            vrf_sys.setHeatRecoveryHeatingCapacityTimeConstant(heat_recovery_heating_capacity_time_constant)
        if heat_recovery_heating_energy_time_constant is not None:
            vrf_sys.setHeatRecoveryHeatingEnergyTimeConstant(heat_recovery_heating_energy_time_constant)

        # Apply performance curves if available
        if performance_curve_set is not None:
            if isinstance(performance_curve_set, dict):
                if len(performance_curve_set) != 0:
                    # Cooling
                    # ***********************************************************************************
                    try:
                        vrf_sys.setCoolingCapacityRatioModifierFunctionofLowTemperatureCurve(
                            performance_curve_set["Cooling Capacity Ratio Modifier Function of Low Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Capacity Ratio Modifier Function of Low Temperature Curve' key")
                    try:
                        vrf_sys.setCoolingCapacityRatioModifierFunctionofHighTemperatureCurve(
                            performance_curve_set["Cooling Capacity Ratio Modifier Function of High Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Capacity Ratio Modifier Function of High Temperature Curve' key")
                    try:
                        vrf_sys.setCoolingCapacityRatioBoundaryCurve(
                            performance_curve_set["Cooling Capacity Ratio Boundary Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Capacity Ratio Boundary Curve' key")
                    try:
                        vrf_sys.setCoolingEnergyInputRatioModifierFunctionofLowTemperatureCurve(
                            performance_curve_set[
                                "Cooling Energy Input Ratio Modifier Function of Low Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Energy Input Ratio Modifier Function of Low Temperature Curve' key")
                    try:
                        vrf_sys.setCoolingEnergyInputRatioModifierFunctionofHighTemperatureCurve(
                            performance_curve_set[
                                "Cooling Energy Input Ratio Modifier Function of High Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Energy Input Ratio Modifier Function of High Temperature Curve' key")
                    try:
                        vrf_sys.setCoolingEnergyInputRatioBoundaryCurve(
                            performance_curve_set["Cooling Energy Input Ratio Boundary Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Energy Input Ratio Boundary Curve' key")
                    try:
                        vrf_sys.setCoolingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve(
                            performance_curve_set[
                                "Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve' key")
                    try:
                        vrf_sys.setCoolingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve(
                            performance_curve_set[
                                "Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve' key")
                    try:
                        vrf_sys.setCoolingCombinationRatioCorrectionFactorCurve(
                            performance_curve_set["Cooling Combination Ratio Correction Factor Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Combination Ratio Correction Factor Curve' key")
                    try:
                        vrf_sys.setCoolingPartLoadFractionCorrelationCurve(
                            performance_curve_set["Cooling Part-Load Fraction Correlation Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Cooling Part-Load Fraction Correlation Curve' key")

                    # Heating
                    # ***********************************************************************************
                    try:
                        vrf_sys.setHeatingCapacityRatioModifierFunctionofLowTemperatureCurve(
                            performance_curve_set["Heating Capacity Ratio Modifier Function of Low Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Capacity Ratio Modifier Function of Low Temperature Curve' key")
                    try:
                        vrf_sys.setHeatingCapacityRatioModifierFunctionofHighTemperatureCurve(
                            performance_curve_set["Heating Capacity Ratio Modifier Function of High Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Capacity Ratio Modifier Function of High Temperature Curve' key")
                    try:
                        vrf_sys.setHeatingCapacityRatioBoundaryCurve(
                            performance_curve_set["Heating Capacity Ratio Boundary Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Capacity Ratio Boundary Curve' key")
                    try:
                        vrf_sys.setHeatingEnergyInputRatioModifierFunctionofLowTemperatureCurve(
                            performance_curve_set[
                                "Heating Energy Input Ratio Modifier Function of Low Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Energy Input Ratio Modifier Function of Low Temperature Curve' key")
                    try:
                        vrf_sys.setHeatingEnergyInputRatioModifierFunctionofHighTemperatureCurve(
                            performance_curve_set[
                                "Heating Energy Input Ratio Modifier Function of High Temperature Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Energy Input Ratio Modifier Function of High Temperature Curve' key")
                    try:
                        vrf_sys.setHeatingEnergyInputRatioBoundaryCurve(
                            performance_curve_set["Heating Energy Input Ratio Boundary Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Energy Input Ratio Boundary Curve' key")
                    try:
                        vrf_sys.setHeatingEnergyInputRatioModifierFunctionofLowPartLoadRatioCurve(
                            performance_curve_set[
                                "Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve' key")
                    try:
                        vrf_sys.setHeatingEnergyInputRatioModifierFunctionofHighPartLoadRatioCurve(
                            performance_curve_set[
                                "Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve' key")
                    try:
                        vrf_sys.setHeatingCombinationRatioCorrectionFactorCurve(
                            performance_curve_set["Heating Combination Ratio Correction Factor Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Combination Ratio Correction Factor Curve' key")
                    try:
                        vrf_sys.setHeatingPartLoadFractionCorrelationCurve(
                            performance_curve_set["Heating Part-Load Fraction Correlation Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heating Part-Load Fraction Correlation Curve' key")

                    # Piping
                    # ***********************************************************************************
                    try:
                        vrf_sys.setPipingCorrectionFactorforLengthinCoolingModeCurve(
                            performance_curve_set["Piping Correction Factor for Length in Cooling Mode Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Piping Correction Factor for Length in Cooling Mode Curve' key")
                    try:
                        vrf_sys.setPipingCorrectionFactorforLengthinHeatingModeCurve(
                            performance_curve_set["Piping Correction Factor for Length in Heating Mode Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Piping Correction Factor for Length in Heating Mode Curve' key")

                    # Heat Recovery
                    # ***********************************************************************************
                    try:
                        vrf_sys.setHeatRecoveryCoolingCapacityModifierCurve(
                            performance_curve_set["Heat Recovery Cooling Capacity Modifier Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heat Recovery Cooling Capacity Modifier Curve' key")
                    try:
                        vrf_sys.setHeatRecoveryHeatingCapacityModifierCurve(
                            performance_curve_set["Heat Recovery Heating Capacity Modifier Curve"])
                    except KeyError:
                        print("Cannot find element with the "
                              "'Heat Recovery Heating Capacity Modifier Curve' key")

                else:
                    raise ValueError("performance_curve_set cannot be empty.")
            else:
                raise TypeError("Invalid input type. performance_curve_set should be dictionary")

        # Add VRF terminal unit to the system
        if terminals is not None:
            if isinstance(terminals, openstudio.openstudiomodel.ZoneHVACTerminalUnitVariableRefrigerantFlow):
                vrf_sys.addTerminal(terminals)
            if isinstance(terminals, list):
                for terminal in terminals:
                    vrf_sys.addTerminal(terminal)

        return vrf_sys

    @staticmethod
    def vav_chiller_boiler(
            model: openstudio.openstudiomodel.Model,
            thermal_zones,
            vav_need_relief_fan: bool = False,
            vav_need_heat_exchanger: bool = False,
            air_loop_dehumidification_control: bool = False,
            number_of_chiller: int = 1,
            chiller_cop=5.5,
            chiller_condenser_type: int = 1,
            number_of_boiler: int = 1,
            boiler_efficiency=0.95,
            number_of_cooling_tower: int = 1):

        """
        Thermal_zones: \n
        could be: \n
        1: a single thermal zone \n
        2: a list of thermal zone (will be all in one air loop) \n
        3: a 2-d list of thermal zone (will be in several air loops based on substructure of the list) \n
        4: a dictionary of thermal zone (each key represents an individual air loop,
        and will have a list of thermal zone as input) \n

        Chiller condenser type: 1: AirCooled 2: WaterCooled 3: EvapCooled
        """

        # Check input validity:
        if model is not None:
            if thermal_zones is not None or len(thermal_zones) != 0:

                # Build an air loop:
                # *****************************************************************************
                air_loops = []
                cooling_coils = []
                heating_coils = []
                reheat_coils = []

                # if the input thermal zone is a single thermal zone object:
                if isinstance(thermal_zones, openstudio.openstudiomodel.ThermalZone):
                    air_loop = HVACTool.air_loop_simplified(
                        model, "VAV Loop", air_terminal_type=4, air_terminal_reheat_type=1,
                        thermal_zones=[thermal_zones])
                    air_loops.append(air_loop[0])

                    if len(air_loop[1]) != 0:
                        reheat_coils.extend(air_loop[1])
                    if len(air_loop[2]) != 0:
                        cooling_coils.extend(air_loop[2])
                    if len(air_loop[3]) != 0:
                        heating_coils.extend(air_loop[3])

                # if the input thermal zone is a list of thermal zone objects
                elif isinstance(thermal_zones, list):
                    # for 1-D list of thermal zone objects:
                    if isinstance(thermal_zones[0], openstudio.openstudiomodel.ThermalZone)\
                            and isinstance(thermal_zones[-1], openstudio.openstudiomodel.ThermalZone):

                        air_loop = HVACTool.air_loop_simplified(
                            model, "VAV Loop", air_terminal_type=4,
                            air_terminal_reheat_type=1,
                            thermal_zones=thermal_zones)
                        air_loops.append(air_loop[0])

                        if len(air_loop[1]) != 0:
                            reheat_coils.extend(air_loop[1])
                        if len(air_loop[2]) != 0:
                            cooling_coils.extend(air_loop[2])
                        if len(air_loop[3]) != 0:
                            heating_coils.extend(air_loop[3])

                    # for 2-D list of thermal zone objects:
                    if isinstance(thermal_zones[0], list) and isinstance(thermal_zones[-1], list):
                        for i in range(len(thermal_zones)):
                            air_loop = HVACTool.air_loop_simplified(
                                model, "VAV Loop", air_terminal_type=4,
                                air_terminal_reheat_type=1,
                                thermal_zones=thermal_zones[i])
                            air_loops.append(air_loop[0])

                            if len(air_loop[1]) != 0:
                                reheat_coils.extend(air_loop[1])
                            if len(air_loop[2]) != 0:
                                cooling_coils.extend(air_loop[2])
                            if len(air_loop[3]) != 0:
                                heating_coils.extend(air_loop[3])

                # if the input thermal zones is a dictionary of thermal zone objects:
                elif isinstance(thermal_zones, dict):
                    for key in thermal_zones:
                        air_loop = HVACTool.air_loop_simplified(
                            model, "VAV Loop" + str(key), air_terminal_type=4,
                            air_terminal_reheat_type=1,
                            thermal_zones=thermal_zones[key])
                        air_loops.append(air_loop[0])

                        if len(air_loop[1]) != 0:
                            reheat_coils.extend(air_loop[1])
                        if len(air_loop[2]) != 0:
                            cooling_coils.extend(air_loop[2])
                        if len(air_loop[3]) != 0:
                            heating_coils.extend(air_loop[3])

                else:
                    raise TypeError("Check format of thermal zones")

                # Add other components into the air loop:
                try:
                    for loop in air_loops:
                        # Set sizing parameters
                        AirLoopComponent.sizing(model, loop, type_of_load_to_size_on=1)

                        supply_inlet_node = loop.supplyInletNode()
                        supply_outlet_node = loop.supplyOutletNode()

                        # Add outdoor air system to the loop
                        controller = AirLoopComponent.controller_outdoor_air(model, economizer_control_type=2)
                        outdoor_air_system = openstudio.openstudiomodel.AirLoopHVACOutdoorAirSystem(model, controller)
                        outdoor_air_system.addToNode(supply_inlet_node)

                        oa_node = outdoor_air_system.outboardOANode().get()
                        relief_node = outdoor_air_system.outboardReliefNode().get()

                        # Add relief fan if needed
                        if vav_need_relief_fan:
                            relief_fan = AirLoopComponent.fan_variable_speed(model)
                            relief_fan.addToNode(relief_node)
                        # Add heat exchanger if needed
                        if vav_need_heat_exchanger:
                            heat_exchanger = AirLoopComponent.heat_exchanger_air_to_air_simplified(
                                model, efficiency=0.7)
                            heat_exchanger.addToNode(oa_node)

                        # Add cooling water coil
                        coil_cooling = AirLoopComponent.coil_cooling_water(model)
                        coil_cooling.addToNode(supply_outlet_node)
                        cooling_coils.append(coil_cooling)

                        # Add set point manager after cooling coil for dehumidification:
                        if air_loop_dehumidification_control:
                            spm_dehum = SetpointManager.scheduled(model, control_variable=5, constant_value=0.008)
                            spm_dehum.addToNode(supply_outlet_node)

                        # Add heating water coil
                        coil_heating = AirLoopComponent.coil_heating_water(model)
                        coil_heating.addToNode(supply_outlet_node)
                        heating_coils.append(coil_heating)

                        # Add fan
                        fan = AirLoopComponent.fan_variable_speed(model, fan_curve_coeff=Curve.fan_curve_set(1))
                        fan.addToNode(supply_outlet_node)

                        # Add set point manager
                        spm = SetpointManager.scheduled(model, control_variable=1, constant_value=12.6)
                        spm.addToNode(supply_outlet_node)

                except ValueError:
                    pass

                # Build a hot water loop:
                # *****************************************************************************
                hot_water_supply_branches = []
                hot_water_demand_branches = []

                if len(heating_coils) != 0:
                    hot_water_demand_branches.extend(heating_coils)
                if len(reheat_coils) != 0:
                    hot_water_demand_branches.extend(reheat_coils)

                for i in range(number_of_boiler):
                    branch = []

                    pump = PlantLoopComponent.pump_variable_speed(model)
                    boiler = PlantLoopComponent.boiler_hot_water(model, efficiency=boiler_efficiency)

                    branch.append(pump)
                    branch.append(boiler)

                    hot_water_supply_branches.append(branch)

                hot_water_bypass_pipe = [PlantLoopComponent.adiabatic_pipe(model)]
                hot_water_supply_branches.append(hot_water_bypass_pipe)

                hot_water_loop = HVACTool.plant_loop(
                    model, "Hot Water Loop", 1,
                    common_pipe_simulation=2,
                    setpoint_manager=SetpointManager.outdoor_air_reset(model, ashrae_default=2),
                    supply_branches=hot_water_supply_branches,
                    demand_branches=hot_water_demand_branches)

                PlantLoopComponent.sizing(model, hot_water_loop, 2)

                # Build a chilled water loop:
                # *****************************************************************************
                chilled_water_supply_branches = []
                chillers = []
                for i in range(number_of_chiller):
                    branch = []

                    pump = PlantLoopComponent.pump_variable_speed(model)
                    chiller = PlantLoopComponent.chiller_electric(
                        model, condenser_type=chiller_condenser_type, cop=chiller_cop)

                    branch.append(pump)
                    branch.append(chiller)
                    chillers.append(chiller)

                    chilled_water_supply_branches.append(branch)

                chilled_water_bypass_pipe = [PlantLoopComponent.adiabatic_pipe(model)]
                chilled_water_supply_branches.append(chilled_water_bypass_pipe)

                chilled_water_loop = HVACTool.plant_loop(
                    model, "Chilled Water Loop", 1,
                    common_pipe_simulation=2,
                    setpoint_manager=SetpointManager.outdoor_air_reset(model, ashrae_default=2),
                    supply_branches=chilled_water_supply_branches,
                    demand_branches=cooling_coils)

                PlantLoopComponent.sizing(model, chilled_water_loop, 1)

                # Build a condenser water loop if needed:
                # *****************************************************************************
                if chiller_condenser_type == 2:
                    condenser_water_supply_branches = []
                    for i in range(number_of_cooling_tower):
                        branch = []

                        pump = PlantLoopComponent.pump_variable_speed(model)
                        tower = PlantLoopComponent.cooling_tower_variable_speed(model)

                        branch.append(pump)
                        branch.append(tower)

                        condenser_water_supply_branches.append(branch)

                    condenser_water_bypass_pipe = [PlantLoopComponent.adiabatic_pipe(model)]
                    condenser_water_supply_branches.append(condenser_water_bypass_pipe)

                    condenser_water_loop = HVACTool.plant_loop(
                        model, "Condenser Water Loop", 1,
                        common_pipe_simulation=1,
                        setpoint_manager=SetpointManager.follow_outdoor_air_temperature(model, ashrae_default=True),
                        supply_branches=condenser_water_supply_branches,
                        demand_branches=chillers)

                    PlantLoopComponent.sizing(model, condenser_water_loop, 3)

            else:
                raise ValueError(Template.zone_null_message)
        else:
            raise ValueError(Template.model_null_message)
