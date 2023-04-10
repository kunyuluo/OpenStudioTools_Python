import openstudio
from Resources.Helpers import Helper
from HVACSystem.SetpointManagers import SetpointManager


class PlantLoopComponent:

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

        if zone_timesteps_in_averaging_window is not None:
            sizing.setZoneTimestepsinAveragingWindow(zone_timesteps_in_averaging_window)

        if coincident_sizing_factor_mode is not None:
            sizing.setCoincidentSizingFactorMode(sizing_factor_modes[coincident_sizing_factor_mode])

    # ***************************************************************************************************
    # Cooling Equipments
    @staticmethod
    def chiller_electric(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            condenser_type: int = 1,
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
            chiller_flow_mode: int = 2,
            sizing_factor=None,
            capacity_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_temperature_curve: openstudio.openstudiomodel.CurveBiquadratic = None,
            cop_plr_curve: openstudio.openstudiomodel.CurveQuadratic = None,
            plant_loop: openstudio.openstudiomodel.PlantLoop = None):

        """
        -Condenser_type: 1:AirCooled 2:WaterCooled 3:EvapCooled \n
        -Chiller_flow_mode: 1:NotModulated 2:LeavingSetpointModulated 3:ConstantFlow
        """

        condenser_types = {1: "AirCooled", 2: "WaterCooled", 3: "EvapCooled"}
        flow_modes = {1: "NotModulated", 2: "LeavingSetpointModulated", 3: "ConstantFlow"}

        chiller = openstudio.openstudiomodel.ChillerElectricEIR(model)
        chiller.setReferenceCOP(cop)
        if name is not None:
            chiller.setName(name)

        chiller.setCondenserType(condenser_types[condenser_type])

        if leaving_chilled_water_temp is not None:
            chiller.setReferenceLeavingChilledWaterTemperature(leaving_chilled_water_temp)
        if entering_condenser_water_temp is not None:
            chiller.setReferenceEnteringCondenserFluidTemperature(entering_condenser_water_temp)

        chiller.setChillerFlowMode(flow_modes[chiller_flow_mode])

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

        if plant_loop is not None:
            plant_loop.addSupplyBranchForComponent(chiller)

        return chiller

    @staticmethod
    def district_cooling(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            nominal_capacity=None):

        district = openstudio.openstudiomodel.DistrictCooling(model)

        if name is not None:
            district.setName(name)

        if nominal_capacity is not None:
            district.setNominalCapacity(nominal_capacity)
        else:
            district.autosizeNominalCapacity()

        return district

    # ***************************************************************************************************
    # Heating Equipments
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
            boiler_flow_mode: int = 3,
            parasitic_electric_load=None,
            sizing_factor=None):

        """
        -Fuel_type: \n
        1:NaturalGas 2:Electricity 3:Propane 4:FuelOilNo1
        5:FuelOilNo2 6:Coal 7:Diesel 8:Gasoline 9:OtherFuel1 10:OtherFuel2 \n

        -Efficiency_curve_temp_eval_variable: \n
        1:LeavingBoiler 2:EnteringBoiler
        (This field is only used if type of curve is one that uses temperature as a independent variable.) \n

        -Boiler_flow_mode: \n
        1:NotModulated 2:ConstantFlow 3:LeavingSetpointModulated \n

        -Boiler_efficiency_curve: \n
        When a boiler efficiency curve is used, the curve may be any valid curve object with 1 (PLR) or
        2 (PLR and boiler outlet water temperature) independent variables.
        The linear, quadratic, and cubic curve types may be used when the boiler efficiency is
        solely a function of boiler part-load ratio (PLR).
        Other curve types may be used when the boiler efficiency is a function of
        both PLR and boiler water temperature.
        For all curve types PLR is always the x independent variable. When using 2 independent variables,
        the boiler outlet water temperature (Toutlet) is always the y independent variable.
        """

        fuel_types = {1: "NaturalGas", 2: "Electricity", 3: "Propane", 4: "FuelOilNo1", 5: "FuelOilNo2",
                      6: "Coal", 7: "Diesel", 8: "Gasoline", 9: "OtherFuel1", 10: "OtherFuel2"}
        curve_eval_variables = {1: "LeavingBoiler", 2: "EnteringBoiler"}
        flow_modes = {1: "NotModulated", 2: "ConstantFlow", 3: "LeavingSetpointModulated"}

        boiler = openstudio.openstudiomodel.BoilerHotWater(model)

        if name is not None:
            boiler.setName(name)

        if fuel_type != 1:
            boiler.setFuelType(fuel_types[fuel_type])

        if nominal_capacity is not None:
            boiler.setNominalCapacity(nominal_capacity)
        else:
            boiler.autosizeNominalCapacity()

        if efficiency is not None:
            boiler.setNominalThermalEfficiency(efficiency)

        if efficiency_curve_temp_eval_variable != 1:
            boiler.setEfficiencyCurveTemperatureEvaluationVariable(
                curve_eval_variables[efficiency_curve_temp_eval_variable])

        if boiler_efficiency_curve is not None:
            boiler.setNormalizedBoilerEfficiencyCurve(boiler_efficiency_curve)

        if design_water_flow_rate is not None:
            boiler.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            boiler.autosizeDesignWaterFlowRate()

        if min_part_load_ratio is not None:
            boiler.setMinimumPartLoadRatio(min_part_load_ratio)

        if max_part_load_ratio is not None:
            boiler.setMaximumPartLoadRatio(max_part_load_ratio)

        if optimal_part_load_ratio is not None:
            boiler.setOptimumPartLoadRatio(optimal_part_load_ratio)

        if water_outlet_upper_temp_limit is not None:
            boiler.setWaterOutletUpperTemperatureLimit(water_outlet_upper_temp_limit)

        if boiler_flow_mode != 1:
            boiler.setBoilerFlowMode(flow_modes[boiler_flow_mode])

        if parasitic_electric_load is not None:
            boiler.setParasiticElectricLoad(parasitic_electric_load)

        if sizing_factor is not None:
            boiler.setSizingFactor(sizing_factor)

        return boiler

    @staticmethod
    def district_heating(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            nominal_capacity=None):

        district = openstudio.openstudiomodel.DistrictHeating(model)

        if name is not None:
            district.setName(name)

        if nominal_capacity is not None:
            district.setNominalCapacity(nominal_capacity)
        else:
            district.autosizeNominalCapacity()

        return district

    # ***************************************************************************************************
    # Service Hot Water Equipments
    @staticmethod
    def water_heater_mixed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            fuel_type: int = 1,
            thermal_efficiency=0.8,
            tank_volume=None,
            setpoint_temp_schedule=None,
            deadband_temp_diff=None,
            max_temp_limit=None,
            heater_control_type: int = 1,
            heater_max_capacity=None,
            heater_min_capacity=None,
            heater_ignition_min_flow_rate=None,
            heater_ignition_delay=None,
            part_load_factor_curve=None,
            off_cycle_parasitic_fuel_consumption_rate=None,
            off_cycle_parasitic_fuel_type: int = 1,
            off_cycle_parasitic_heat_fraction_to_tank=None,
            on_cycle_parasitic_fuel_consumption_rate=None,
            on_cycle_parasitic_fuel_type: int = 1,
            on_cycle_parasitic_heat_fraction_to_tank=None,
            ambient_temp_indicator: int = 1,
            ambient_temp_schedule=None,
            ambient_temp_thermal_zone=None,
            off_cycle_loss_coefficient_to_ambient=None,
            off_cycle_loss_fraction_to_thermal_zone=None,
            on_cycle_loss_coefficient_to_ambient=None,
            on_cycle_loss_fraction_to_thermal_zone=None,
            peak_use_flow_rate=None,
            use_flow_rate_fraction_schedule=None,
            cold_water_supply_temp_schedule=None,
            use_side_effectiveness=None,
            source_side_effectiveness=None,
            use_side_design_flow_rate=None,
            source_side_design_flow_rate=None,
            indirect_water_heating_recovery_time=None,
            source_side_flow_control_mode: int = 1,
            indirect_alternate_setpoint_temp_schedule=None,
            sizing={}):

        """
        -Fuel_type: \n
        1:NaturalGas 2:Electricity 3:Propane 4:FuelOilNo1
        5:FuelOilNo2 6:Coal 7:Diesel 8:Gasoline 9:OtherFuel1 10:OtherFuel2 \n

        -Heater control types: 1:Cycle 2:Modulate \n

        -Ambient temperature indicator: 1:Schedule 2:ThermalZone 3:Outdoors \n

        -Source side control mode: 1:StorageTank 2:IndirectHeatPrimarySetpoint 3:IndirectHeatAlternateSetpoint
        """

        fuel_types = {1: "NaturalGas", 2: "Electricity", 3: "Propane", 4: "FuelOilNo1", 5: "FuelOilNo2",
                      6: "Coal", 7: "Diesel", 8: "Gasoline", 9: "OtherFuel1", 10: "OtherFuel2"}
        control_types = {1: "Cycle", 2: "Modulate"}
        ambient_types = {1: "Schedule", 2: "ThermalZone", 3: "Outdoors"}
        source_control_types = {1: "StorageTank", 2: "IndirectHeatPrimarySetpoint", 3: "IndirectHeatAlternateSetpoint"}

        heater = openstudio.openstudiomodel.WaterHeaterMixed(model)

        if name is not None:
            heater.setName(name)

        heater.setHeaterFuelType(fuel_types[fuel_type])
        heater.setHeaterThermalEfficiency(thermal_efficiency)

        if tank_volume is not None:
            heater.setTankVolume(tank_volume)
        else:
            heater.autosizeTankVolume()

        if setpoint_temp_schedule is not None:
            heater.setSetpointTemperatureSchedule(setpoint_temp_schedule)

        if deadband_temp_diff is not None:
            heater.setDeadbandTemperatureDifference(deadband_temp_diff)

        if max_temp_limit is not None:
            heater.setMaximumTemperatureLimit(max_temp_limit)

        heater.setHeaterControlType(control_types[heater_control_type])

        if heater_max_capacity is not None:
            heater.setHeaterMaximumCapacity(heater_max_capacity)
        else:
            heater.autosizeHeaterMaximumCapacity()

        if heater_min_capacity is not None:
            heater.setHeaterMinimumCapacity(heater_min_capacity)

        if heater_ignition_min_flow_rate is not None:
            heater.setHeaterIgnitionMinimumFlowRate(heater_ignition_min_flow_rate)
        if heater_ignition_delay is not None:
            heater.setHeaterIgnitionDelay(heater_ignition_delay)

        if part_load_factor_curve is not None:
            heater.setPartLoadFactorCurve(part_load_factor_curve)

        if off_cycle_parasitic_fuel_consumption_rate is not None:
            heater.setOffCycleParasiticFuelConsumptionRate(off_cycle_parasitic_fuel_consumption_rate)

        heater.setOffCycleParasiticFuelType(fuel_types[off_cycle_parasitic_fuel_type])

        if off_cycle_parasitic_heat_fraction_to_tank is not None:
            heater.setOffCycleParasiticHeatFractiontoTank(off_cycle_parasitic_heat_fraction_to_tank)

        if on_cycle_parasitic_fuel_consumption_rate is not None:
            heater.setOnCycleParasiticFuelConsumptionRate(on_cycle_parasitic_fuel_consumption_rate)

        heater.setOnCycleParasiticFuelType(fuel_types[on_cycle_parasitic_fuel_type])

        if on_cycle_parasitic_heat_fraction_to_tank is not None:
            heater.setOnCycleParasiticHeatFractiontoTank(on_cycle_parasitic_heat_fraction_to_tank)

        heater.setAmbientTemperatureIndicator(ambient_types[ambient_temp_indicator])

        if ambient_temp_schedule is not None:
            heater.setAmbientTemperatureSchedule(ambient_temp_schedule)

        if ambient_temp_thermal_zone is not None:
            heater.setAmbientTemperatureThermalZone(ambient_temp_thermal_zone)

        if off_cycle_loss_coefficient_to_ambient is not None:
            heater.setOffCycleLossCoefficienttoAmbientTemperature(off_cycle_loss_coefficient_to_ambient)

        if off_cycle_loss_fraction_to_thermal_zone is not None:
            heater.setOffCycleLossFractiontoThermalZone(off_cycle_loss_fraction_to_thermal_zone)

        if on_cycle_loss_coefficient_to_ambient is not None:
            heater.setOnCycleLossCoefficienttoAmbientTemperature(on_cycle_loss_coefficient_to_ambient)

        if on_cycle_loss_fraction_to_thermal_zone is not None:
            heater.setOnCycleLossFractiontoThermalZone(on_cycle_loss_fraction_to_thermal_zone)

        if peak_use_flow_rate is not None:
            heater.setPeakUseFlowRate(peak_use_flow_rate)

        if use_flow_rate_fraction_schedule is not None:
            heater.setUseFlowRateFractionSchedule(use_flow_rate_fraction_schedule)

        if cold_water_supply_temp_schedule is not None:
            heater.setColdWaterSupplyTemperatureSchedule(cold_water_supply_temp_schedule)

        if source_side_effectiveness is not None:
            heater.setSourceSideEffectiveness(source_side_effectiveness)

        if use_side_effectiveness is not None:
            heater.setUseSideEffectiveness(use_side_effectiveness)

        if use_side_design_flow_rate is not None:
            heater.setUseSideDesignFlowRate(use_side_design_flow_rate)
        else:
            heater.autosizeUseSideDesignFlowRate()

        if source_side_design_flow_rate is not None:
            heater.setSourceSideDesignFlowRate(source_side_design_flow_rate)
        else:
            heater.autosizeSourceSideDesignFlowRate()

        if indirect_water_heating_recovery_time is not None:
            heater.setIndirectWaterHeatingRecoveryTime(indirect_water_heating_recovery_time)

        heater.setSourceSideFlowControlMode(source_control_types[source_side_flow_control_mode])

        if indirect_alternate_setpoint_temp_schedule is not None:
            heater.setIndirectAlternateSetpointTemperatureSchedule(indirect_alternate_setpoint_temp_schedule)

        # Sizing parameters
        heater_sizing = heater.waterHeaterSizing()
        if isinstance(sizing, dict):
            try:
                heater_sizing.setDesignMode(sizing["Design Mode"])
            except ValueError:
                pass
            try:
                heater_sizing.setTimeStorageCanMeetPeakDraw(sizing["Time Storage Can Meet Peak Draw"])
            except ValueError:
                pass
            try:
                heater_sizing.setTimeforTankRecovery(sizing["Time for Tank Recovery"])
            except ValueError:
                pass
            try:
                heater_sizing.setNominalTankVolumeforAutosizingPlantConnections(
                    sizing["Nominal Tank Volume for Autosizing Plant Connections"])
            except ValueError:
                pass
            try:
                heater_sizing.setNumberofBedrooms(sizing["Number of Bedrooms"])
            except ValueError:
                pass
            try:
                heater_sizing.setNumberofBathrooms(sizing["Number of Bathrooms"])
            except ValueError:
                pass
            try:
                heater_sizing.setStorageCapacityperPerson(sizing["Storage Capacity per Person"])
            except ValueError:
                pass
            try:
                heater_sizing.setRecoveryCapacityperPerson(sizing["Recovery Capacity per Person"])
            except ValueError:
                pass
            try:
                heater_sizing.setStorageCapacityperFloorArea(sizing["Storage Capacity per Floor Area"])
            except ValueError:
                pass
            try:
                heater_sizing.setRecoveryCapacityperFloorArea(sizing["Recovery Capacity per Floor Area"])
            except ValueError:
                pass
            try:
                heater_sizing.setNumberofUnits(sizing["Number of Units"])
            except ValueError:
                pass
            try:
                heater_sizing.setStorageCapacityperUnit(sizing["Storage Capacity per Unit"])
            except ValueError:
                pass
            try:
                heater_sizing.setRecoveryCapacityPerUnit(sizing["Recovery Capacity per Unit"])
            except ValueError:
                pass
            try:
                heater_sizing.setStorageCapacityperCollectorArea(sizing["Storage Capacity per Collector Area"])
            except ValueError:
                pass
            try:
                heater_sizing.setHeightAspectRatio(sizing["Height Aspect Ratio"])
            except ValueError:
                pass
        else:
            raise TypeError("Invalid input for water heater sizing.")

        return heater

    @staticmethod
    def water_heater_sizing(
            design_mode: int = 1,
            time_storage_can_meet_peak_draw: float = 0.6,
            time_for_tank_recovery: float = 0,
            nominal_tank_volume_autosizing_plant_connection: float = 1,
            number_of_bedrooms: int = 0,
            number_of_bathrooms: int = 0,
            storage_capacity_per_person: float = 0,
            recovery_capacity_per_person: float = 0,
            storage_capacity_per_floor_area: float = 0,
            recovery_capacity_per_floor_area: float = 0,
            number_of_units: int = 0,
            storage_capacity_per_unit: float = 0,
            recovery_capacity_per_unit: float = 0,
            storage_capacity_per_collector_area: float = 0,
            height_aspect_ratio: float = 0):

        """
        -Design_mode: \n
        1:PeakDraw \n
        2:ResidentialHUD-FHAMinimum \n
        3:PerPerson \n
        4:PerFloorArea \n
        5:PerUnit \n
        6:PerSolarCollectorArea
        """

        design_modes = {1: "PeakDraw", 2: "ResidentialHUD-FHAMinimum", 3: "PerPerson",
                        4: "PerFloorArea", 5: "PerUnit", 6: "PerSolarCollectorArea"}

        sizing = {}

        sizing["Design Mode"] = design_modes[design_mode]
        sizing["Time Storage Can Meet Peak Draw"] = time_storage_can_meet_peak_draw
        sizing["Time for Tank Recovery"] = time_for_tank_recovery
        sizing["Nominal Tank Volume for Autosizing Plant Connections"] = nominal_tank_volume_autosizing_plant_connection
        sizing["Number of Bathrooms"] = number_of_bathrooms
        sizing["Number of Bedrooms"] = number_of_bedrooms
        sizing["Storage Capacity per Person"] = storage_capacity_per_person
        sizing["Recovery Capacity per Person"] = recovery_capacity_per_person
        sizing["Storage Capacity per Floor Area"] = storage_capacity_per_floor_area
        sizing["Recovery Capacity per Floor Area"] = recovery_capacity_per_floor_area
        sizing["Number of Units"] = number_of_units
        sizing["Storage Capacity per Unit"] = storage_capacity_per_unit
        sizing["Recovery Capacity per Unit"] = recovery_capacity_per_unit
        sizing["Storage Capacity per Collector Area"] = storage_capacity_per_collector_area
        sizing["Height Aspect Ratio"] = height_aspect_ratio

        return sizing

    @staticmethod
    def water_use_connection(
            model: openstudio.openstudiomodel.Model,
            water_use_equipment=None,
            name: str = None,
            hot_water_supply_temp_schedule=None,
            cold_water_supply_temp_schedule=None,
            drain_water_heat_exchanger_type: int = 1,
            drain_water_heat_exchanger_destination: int = 1,
            drain_water_heat_exchanger_u_factor_times_area=None):

        """
        -Drain_water_heat_exchanger_type:  \n
        1:None 2:Ideal 3:CounterFlow 4:CrossFlow \n

        -Drain_water_heat_exchanger_destination: \n
        1:Plant 2:Equipment 3:PlantAndEquipment
        """

        exchanger_types = {1: "None", 2: "Ideal", 3: "CounterFlow", 4: "CrossFlow"}
        exchanger_destinations = {1: "Plant", 2: "Equipment", 3: "PlantAndEquipment"}

        connection = openstudio.openstudiomodel.WaterUseConnections(model)

        if name is not None:
            connection.setName(name)

        if hot_water_supply_temp_schedule is not None:
            connection.setHotWaterSupplyTemperatureSchedule(hot_water_supply_temp_schedule)
        if cold_water_supply_temp_schedule is not None:
            connection.setColdWaterSupplyTemperatureSchedule(cold_water_supply_temp_schedule)

        connection.setDrainWaterHeatExchangerType(exchanger_types[drain_water_heat_exchanger_type])
        connection.setDrainWaterHeatExchangerDestination(exchanger_destinations[drain_water_heat_exchanger_destination])

        if drain_water_heat_exchanger_u_factor_times_area is not None:
            connection.setDrainWaterHeatExchangerUFactorTimesArea(drain_water_heat_exchanger_u_factor_times_area)

        # Add water use equipment:
        connection.addWaterUseEquipment(water_use_equipment)

        return connection

    # ***************************************************************************************************
    # Condenser Equipments
    @staticmethod
    def cooling_tower_single_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_water_flow_rate=None,
            design_air_flow_rate=None,
            fan_power_at_design_air_flow=None,
            u_factor_area_at_design_air_flow=None,
            air_flow_rate_in_free_convection=None,
            u_factor_area_at_free_convection=None,
            performance_input_method: int = 1,
            nominal_capacity=None,
            free_convection_capacity=None,
            basin_heater_capacity=None,
            basin_heater_setpoint_temp=None,
            basin_heater_schedule=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=None,
            drift_loss_percent=None,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=None,
            blowdown_markup_water_schedule=None,
            capacity_control: int = 1,
            number_of_cells=None,
            cell_control: int = 1,
            cell_min_water_flow_fraction=None,
            cell_max_water_flow_fraction=None,
            sizing_factor=None,
            free_convection_sizing_factor=None,
            free_convection_u_factor_area_sizing_factor=None,
            heat_rejection_cap_nominal_cap_ratio=None,
            free_convection_nominal_cap_sizing_factor=None,
            design_inlet_air_dry_bulb_temp=None,
            design_inlet_air_wet_bulb_temp=None,
            design_approach_temp=None,
            design_range_temp=None):

        """
        -Performance_input_method: 1:UFactorTimesAreaAndDesignWaterFlowRate 2:NominalCapacity
        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit
        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate
        -Capacity_control: 1:FanCycling 2:FluidBypass
        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        performance_methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}
        capacity_controls = {1: "FanCycling", 2: "FluidBypass"}
        cell_controls = {1: "MinimalCell", 2: "MaximalCell"}

        tower = openstudio.openstudiomodel.CoolingTowerSingleSpeed(model)

        if name is not None:
            tower.setName(name)

        if design_water_flow_rate is not None:
            tower.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            tower.autosizeDesignWaterFlowRate()

        if design_air_flow_rate is not None:
            tower.setDesignAirFlowRate(design_air_flow_rate)
        else:
            tower.autosizeDesignAirFlowRate()

        if fan_power_at_design_air_flow is not None:
            tower.setFanPoweratDesignAirFlowRate(fan_power_at_design_air_flow)
        else:
            tower.autosizeFanPoweratDesignAirFlowRate()

        if u_factor_area_at_design_air_flow is not None:
            tower.setUFactorTimesAreaValueatDesignAirFlowRate(u_factor_area_at_design_air_flow)
        else:
            tower.autosizeUFactorTimesAreaValueatDesignAirFlowRate()

        if air_flow_rate_in_free_convection is not None:
            tower.setAirFlowRateinFreeConvectionRegime(air_flow_rate_in_free_convection)
        else:
            tower.autosizeAirFlowRateinFreeConvectionRegime()

        if u_factor_area_at_free_convection is not None:
            tower.setUFactorTimesAreaValueatFreeConvectionAirFlowRate(u_factor_area_at_free_convection)
        else:
            tower.autosizeUFactorTimesAreaValueatFreeConvectionAirFlowRate()

        if performance_input_method != 1:
            tower.setPerformanceInputMethod(performance_methods[performance_input_method])

        if nominal_capacity is not None:
            tower.setNominalCapacity(nominal_capacity)

        if free_convection_capacity is not None:
            tower.setFreeConvectionCapacity(free_convection_capacity)

        if basin_heater_capacity is not None:
            tower.setBasinHeaterCapacity(basin_heater_capacity)

        if basin_heater_setpoint_temp is not None:
            tower.setBasinHeaterSetpointTemperature(basin_heater_setpoint_temp)

        if basin_heater_schedule is not None:
            tower.setBasinHeaterOperatingSchedule(basin_heater_schedule)

        if evaporation_loss_mode != 1:
            tower.setEvaporationLossMode(evap_loss_modes[evaporation_loss_mode])

        if evaporation_loss_factor is not None:
            tower.setEvaporationLossFactor(evaporation_loss_factor)

        if drift_loss_percent is not None:
            tower.setDriftLossPercent(drift_loss_percent)

        if blowdown_calculation_mode != 1:
            tower.setBlowdownCalculationMode(blowdown_modes[blowdown_calculation_mode])

        if blowdown_concentration_ratio is not None:
            tower.setBlowdownConcentrationRatio(blowdown_concentration_ratio)

        if blowdown_markup_water_schedule is not None:
            tower.setBlowdownMakeupWaterUsageSchedule(blowdown_markup_water_schedule)

        if capacity_control != 1:
            tower.setCapacityControl(capacity_controls[capacity_control])

        if number_of_cells is not None:
            tower.setNumberofCells(number_of_cells)

        if cell_control != 1:
            tower.setCellControl(cell_controls[cell_control])

        if cell_min_water_flow_fraction is not None:
            tower.setCellMinimumWaterFlowRateFraction(cell_min_water_flow_fraction)

        if cell_max_water_flow_fraction is not None:
            tower.setCellMaximumWaterFlowRateFraction(cell_max_water_flow_fraction)

        if sizing_factor is not None:
            tower.setSizingFactor(sizing_factor)

        if free_convection_sizing_factor is not None:
            tower.setFreeConvectionAirFlowRateSizingFactor(free_convection_sizing_factor)

        if free_convection_u_factor_area_sizing_factor is not None:
            tower.setFreeConvectionUFactorTimesAreaValueSizingFactor(free_convection_u_factor_area_sizing_factor)

        if heat_rejection_cap_nominal_cap_ratio is not None:
            tower.setHeatRejectionCapacityAndNominalCapacitySizingRatio(heat_rejection_cap_nominal_cap_ratio)

        if free_convection_nominal_cap_sizing_factor is not None:
            tower.setFreeConvectionNominalCapacitySizingFactor(free_convection_nominal_cap_sizing_factor)

        if design_inlet_air_dry_bulb_temp is not None:
            tower.setDesignInletAirDryBulbTemperature(design_inlet_air_dry_bulb_temp)

        if design_inlet_air_wet_bulb_temp is not None:
            tower.setDesignInletAirWetBulbTemperature(design_inlet_air_wet_bulb_temp)

        if design_approach_temp is not None:
            tower.setDesignApproachTemperature(design_approach_temp)
        else:
            tower.autosizeDesignApproachTemperature()

        if design_range_temp is not None:
            tower.setDesignRangeTemperature(design_range_temp)
        else:
            tower.autosizeDesignRangeTemperature()

        return tower

    @staticmethod
    def cooling_tower_two_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_water_flow_rate=None,
            high_fan_speed_air_flow_rate=None,
            high_fan_speed_fan_power=None,
            high_fan_speed_u_factor_area=None,
            low_fan_speed_air_flow_rate=None,
            low_fan_speed_fan_power=None,
            low_fan_speed_air_flow_sizing_factor=None,
            low_fan_speed_power_sizing_factor=None,
            low_fan_speed_u_factor_area=None,
            air_flow_rate_in_free_convection=None,
            u_factor_area_at_free_convection=None,
            performance_input_method: int = 1,
            high_speed_nominal_capacity=None,
            low_speed_nominal_capacity=None,
            low_speed_nominal_capacity_sizing_factor=None,
            free_convection_capacity=None,
            basin_heater_capacity=None,
            basin_heater_setpoint_temp=None,
            basin_heater_schedule=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=None,
            drift_loss_percent=None,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=None,
            blowdown_markup_water_schedule=None,
            number_of_cells=None,
            cell_control: int = 1,
            cell_min_water_flow_fraction=None,
            cell_max_water_flow_fraction=None,
            sizing_factor=None,
            free_convection_sizing_factor=None,
            free_convection_u_factor_area_sizing_factor=None,
            heat_rejection_cap_nominal_cap_ratio=None,
            free_convection_nominal_cap_sizing_factor=None,
            design_inlet_air_dry_bulb_temp=None,
            design_inlet_air_wet_bulb_temp=None,
            design_approach_temp=None,
            design_range_temp=None):

        """
        -Performance_input_method: 1:UFactorTimesAreaAndDesignWaterFlowRate 2:NominalCapacity
        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit
        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate
        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        performance_methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}
        cell_controls = {1: "MinimalCell", 2: "MaximalCell"}

        tower = openstudio.openstudiomodel.CoolingTowerTwoSpeed(model)

        if name is not None:
            tower.setName(name)

        if design_water_flow_rate is not None:
            tower.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            tower.autosizeDesignWaterFlowRate()

        if high_fan_speed_air_flow_rate is not None:
            tower.setHighFanSpeedAirFlowRate(high_fan_speed_air_flow_rate)
        else:
            tower.autosizeHighFanSpeedAirFlowRate()

        if high_fan_speed_fan_power is not None:
            tower.setHighFanSpeedFanPower(high_fan_speed_fan_power)
        else:
            tower.autosizeHighFanSpeedFanPower()

        if high_fan_speed_u_factor_area is not None:
            tower.setHighFanSpeedUFactorTimesAreaValue(high_fan_speed_u_factor_area)
        else:
            tower.autosizeHighFanSpeedUFactorTimesAreaValue()

        if low_fan_speed_air_flow_rate is not None:
            tower.setLowFanSpeedAirFlowRate(low_fan_speed_air_flow_rate)
        else:
            tower.autosizeLowFanSpeedAirFlowRate()

        if low_fan_speed_fan_power is not None:
            tower.setLowFanSpeedFanPower(low_fan_speed_fan_power)
        else:
            tower.autosizeLowFanSpeedFanPower()

        if low_fan_speed_air_flow_sizing_factor is not None:
            tower.setLowFanSpeedAirFlowRateSizingFactor(low_fan_speed_air_flow_sizing_factor)

        if low_fan_speed_power_sizing_factor is not None:
            tower.setLowFanSpeedFanPowerSizingFactor(low_fan_speed_power_sizing_factor)

        if low_fan_speed_u_factor_area is not None:
            tower.setLowFanSpeedUFactorTimesAreaValue(low_fan_speed_u_factor_area)
        else:
            tower.autosizeLowFanSpeedUFactorTimesAreaValue()

        if high_speed_nominal_capacity is not None:
            tower.setHighSpeedNominalCapacity(high_speed_nominal_capacity)

        if low_speed_nominal_capacity is not None:
            tower.setLowSpeedNominalCapacity(low_speed_nominal_capacity)
        else:
            tower.autosizeLowSpeedNominalCapacity()

        if low_speed_nominal_capacity_sizing_factor is not None:
            tower.setLowSpeedNominalCapacitySizingFactor(low_speed_nominal_capacity_sizing_factor)

        if air_flow_rate_in_free_convection is not None:
            tower.setFreeConvectionRegimeAirFlowRate(air_flow_rate_in_free_convection)
        else:
            tower.autosizeFreeConvectionRegimeAirFlowRate()

        if u_factor_area_at_free_convection is not None:
            tower.setFreeConvectionRegimeUFactorTimesAreaValue(u_factor_area_at_free_convection)
        else:
            tower.autosizeFreeConvectionRegimeUFactorTimesAreaValue()

        if performance_input_method != 1:
            tower.setPerformanceInputMethod(performance_methods[performance_input_method])

        if free_convection_capacity is not None:
            tower.setFreeConvectionNominalCapacity(free_convection_capacity)

        if basin_heater_capacity is not None:
            tower.setBasinHeaterCapacity(basin_heater_capacity)

        if basin_heater_setpoint_temp is not None:
            tower.setBasinHeaterSetpointTemperature(basin_heater_setpoint_temp)

        if basin_heater_schedule is not None:
            tower.setBasinHeaterOperatingSchedule(basin_heater_schedule)

        if evaporation_loss_mode != 1:
            tower.setEvaporationLossMode(evap_loss_modes[evaporation_loss_mode])

        if evaporation_loss_factor is not None:
            tower.setEvaporationLossFactor(evaporation_loss_factor)

        if drift_loss_percent is not None:
            tower.setDriftLossPercent(drift_loss_percent)

        if blowdown_calculation_mode != 1:
            tower.setBlowdownCalculationMode(blowdown_modes[blowdown_calculation_mode])

        if blowdown_concentration_ratio is not None:
            tower.setBlowdownConcentrationRatio(blowdown_concentration_ratio)

        if blowdown_markup_water_schedule is not None:
            tower.setBlowdownMakeupWaterUsageSchedule(blowdown_markup_water_schedule)

        if number_of_cells is not None:
            tower.setNumberofCells(number_of_cells)

        if cell_control != 1:
            tower.setCellControl(cell_controls[cell_control])

        if cell_min_water_flow_fraction is not None:
            tower.setCellMinimumWaterFlowRateFraction(cell_min_water_flow_fraction)

        if cell_max_water_flow_fraction is not None:
            tower.setCellMaximumWaterFlowRateFraction(cell_max_water_flow_fraction)

        if sizing_factor is not None:
            tower.setSizingFactor(sizing_factor)

        if free_convection_sizing_factor is not None:
            tower.setFreeConvectionRegimeAirFlowRateSizingFactor(free_convection_sizing_factor)

        if free_convection_u_factor_area_sizing_factor is not None:
            tower.setFreeConvectionUFactorTimesAreaValueSizingFactor(free_convection_u_factor_area_sizing_factor)

        if heat_rejection_cap_nominal_cap_ratio is not None:
            tower.setHeatRejectionCapacityandNominalCapacitySizingRatio(heat_rejection_cap_nominal_cap_ratio)

        if free_convection_nominal_cap_sizing_factor is not None:
            tower.setFreeConvectionNominalCapacitySizingFactor(free_convection_nominal_cap_sizing_factor)

        if design_inlet_air_dry_bulb_temp is not None:
            tower.setDesignInletAirDryBulbTemperature(design_inlet_air_dry_bulb_temp)

        if design_inlet_air_wet_bulb_temp is not None:
            tower.setDesignInletAirWetBulbTemperature(design_inlet_air_wet_bulb_temp)

        if design_approach_temp is not None:
            tower.setDesignApproachTemperature(design_approach_temp)
        else:
            tower.autosizeDesignApproachTemperature()

        if design_range_temp is not None:
            tower.setDesignRangeTemperature(design_range_temp)
        else:
            tower.autosizeDesignRangeTemperature()

        return tower

    @staticmethod
    def cooling_tower_variable_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            model_type: int = 1,
            model_coefficient=None,
            design_inlet_air_wet_bulb_temp=None,
            design_approach_temp=None,
            design_range_temp=None,
            design_water_flow_rate=None,
            design_air_flow_rate=None,
            design_fan_power=None,
            fan_power_ratio_air_flow_ratio_curve=None,
            basin_heater_capacity=None,
            basin_heater_setpoint_temp=None,
            basin_heater_schedule=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=None,
            drift_loss_percent=None,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=None,
            blowdown_markup_water_schedule=None,
            number_of_cells=None,
            cell_control: int = 1,
            cell_min_water_flow_fraction=None,
            cell_max_water_flow_fraction=None,
            sizing_factor=None):

        """
        -Model_type: 1:CoolToolsCrossFlow 2:CoolToolsUserDefined 3:YorkCalc 4:YorkCalcUserDefined
        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit
        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate
        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        model_types = {1: "CoolToolsCrossFlow", 2: "CoolToolsUserDefined", 3: "YorkCalc", 4: "YorkCalcUserDefined"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}
        cell_controls = {1: "MinimalCell", 2: "MaximalCell"}

        tower = openstudio.openstudiomodel.CoolingTowerVariableSpeed(model)

        if name is not None:
            tower.setName(name)

        if model_type != 1:
            tower.setModelType(model_types[model_type])

        match model_type:
            case 2:
                if model_coefficient is not None:
                    # Check type:
                    cool_tool_type = str(type(model_coefficient)).split('.')[-1].split("'")[0]
                    if cool_tool_type == "CoolingTowerPerformanceCoolTools":
                        tower.setModelCoefficient(model_coefficient)
                    else:
                        raise TypeError("Type of model coefficient must be CoolingTowerPerformanceCoolTools")
                else:
                    cool_tools = openstudio.openstudiomodel.CoolingTowerPerformanceCoolTools(model)
                    tower.setModelCoefficient(cool_tools)
            case 4:
                if model_coefficient is not None:
                    # Check type:
                    cool_tool_type = str(type(model_coefficient)).split('.')[-1].split("'")[0]
                    if cool_tool_type == "CoolingTowerPerformanceYorkCalc":
                        tower.setModelCoefficient(model_coefficient)
                    else:
                        raise TypeError("Type of model coefficient must be CoolingTowerPerformanceYorkCalc")
                else:
                    cool_tools = openstudio.openstudiomodel.CoolingTowerPerformanceYorkCalc(model)
                    tower.setModelCoefficient(cool_tools)
            case _:
                pass

        if design_inlet_air_wet_bulb_temp is not None:
            tower.setDesignInletAirWetBulbTemperature(design_inlet_air_wet_bulb_temp)

        if design_approach_temp is not None:
            tower.setDesignApproachTemperature(design_approach_temp)

        if design_range_temp is not None:
            tower.setDesignRangeTemperature(design_range_temp)

        if design_water_flow_rate is not None:
            tower.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            tower.autosizeDesignWaterFlowRate()

        if design_air_flow_rate is not None:
            tower.setDesignAirFlowRate(design_air_flow_rate)
        else:
            tower.autosizeDesignAirFlowRate()

        if design_fan_power is not None:
            tower.setDesignFanPower(design_fan_power)
        else:
            tower.autosizeDesignFanPower()

        if fan_power_ratio_air_flow_ratio_curve is not None:
            tower.setFanPowerRatioFunctionofAirFlowRateRatioCurve(fan_power_ratio_air_flow_ratio_curve)

        if basin_heater_capacity is not None:
            tower.setBasinHeaterCapacity(basin_heater_capacity)

        if basin_heater_setpoint_temp is not None:
            tower.setBasinHeaterSetpointTemperature(basin_heater_setpoint_temp)

        if basin_heater_schedule is not None:
            tower.setBasinHeaterOperatingSchedule(basin_heater_schedule)

        if evaporation_loss_mode != 1:
            tower.setEvaporationLossMode(evap_loss_modes[evaporation_loss_mode])

        if evaporation_loss_factor is not None:
            tower.setEvaporationLossFactor(evaporation_loss_factor)

        if drift_loss_percent is not None:
            tower.setDriftLossPercent(drift_loss_percent)

        if blowdown_calculation_mode != 1:
            tower.setBlowdownCalculationMode(blowdown_modes[blowdown_calculation_mode])

        if blowdown_concentration_ratio is not None:
            tower.setBlowdownConcentrationRatio(blowdown_concentration_ratio)

        if blowdown_markup_water_schedule is not None:
            tower.setBlowdownMakeupWaterUsageSchedule(blowdown_markup_water_schedule)

        if number_of_cells is not None:
            tower.setNumberofCells(number_of_cells)

        if cell_control != 1:
            tower.setCellControl(cell_controls[cell_control])

        if cell_min_water_flow_fraction is not None:
            tower.setCellMinimumWaterFlowRateFraction(cell_min_water_flow_fraction)

        if cell_max_water_flow_fraction is not None:
            tower.setCellMaximumWaterFlowRateFraction(cell_max_water_flow_fraction)

        if sizing_factor is not None:
            tower.setSizingFactor(sizing_factor)

        return tower

    @staticmethod
    def evaporative_fluid_cooler_single_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_air_flow_rate=None,
            fan_power_at_design_air_flow=None,
            design_water_flow_rate=None,
            design_spray_water_flow_rate=None,
            u_factor_area_at_design_air_flow=None,
            performance_input_method: int = 1,
            standard_design_capacity=None,
            user_specified_design_capacity=None,
            design_entering_water_temp=None,
            design_entering_air_temp=None,
            design_entering_air_web_bulb_temp=None,
            capacity_control: int = 1,
            sizing_factor=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=None,
            drift_loss_percent=None,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=None,
            blowdown_markup_water_schedule=None):

        """
        -Performance_input_method: \n
        1:UFactorTimesAreaAndDesignWaterFlowRate \n
        2:StandardDesignCapacity \n
        3:UserSpecifiedDesignCapacity \n

        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit

        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate

        -Capacity_control: 1:FanCycling 2:FluidBypass

        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        performance_methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity",
                               3: "UserSpecifiedDesignCapacity"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}
        capacity_controls = {1: "FanCycling", 2: "FluidBypass"}
        cell_controls = {1: "MinimalCell", 2: "MaximalCell"}

        tower = openstudio.openstudiomodel.EvaporativeFluidCoolerSingleSpeed(model)

        if name is not None:
            tower.setName(name)

        if design_water_flow_rate is not None:
            tower.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            tower.autosizeDesignWaterFlowRate()

        if design_spray_water_flow_rate is not None:
            tower.setDesignSprayWaterFlowRate(design_spray_water_flow_rate)

        if design_air_flow_rate is not None:
            tower.setDesignAirFlowRate(design_air_flow_rate)
        else:
            tower.autosizeDesignAirFlowRate()

        if fan_power_at_design_air_flow is not None:
            tower.setFanPoweratDesignAirFlowRate(fan_power_at_design_air_flow)
        else:
            tower.autosizeFanPoweratDesignAirFlowRate()

        if u_factor_area_at_design_air_flow is not None:
            tower.setUfactorTimesAreaValueatDesignAirFlowRate(u_factor_area_at_design_air_flow)
        else:
            tower.autosizeUfactorTimesAreaValueatDesignAirFlowRate()

        if performance_input_method != 1:
            tower.setPerformanceInputMethod(performance_methods[performance_input_method])

        if standard_design_capacity is not None:
            tower.setStandardDesignCapacity(standard_design_capacity)

        if user_specified_design_capacity is not None:
            tower.setUserSpecifiedDesignCapacity(user_specified_design_capacity)

        if design_entering_water_temp is not None:
            tower.setDesignEnteringWaterTemperature(design_entering_water_temp)
        if design_entering_air_temp is not None:
            tower.setDesignEnteringAirTemperature(design_entering_air_temp)
        if design_entering_air_web_bulb_temp is not None:
            tower.setDesignEnteringAirWetbulbTemperature(design_entering_air_web_bulb_temp)

        if capacity_control != 1:
            tower.setCapacityControl(capacity_controls[capacity_control])

        if sizing_factor is not None:
            tower.setSizingFactor(sizing_factor)

        if evaporation_loss_mode != 1:
            tower.setEvaporationLossMode(evap_loss_modes[evaporation_loss_mode])

        if evaporation_loss_factor is not None:
            tower.setEvaporationLossFactor(evaporation_loss_factor)

        if drift_loss_percent is not None:
            tower.setDriftLossPercent(drift_loss_percent)

        if blowdown_calculation_mode != 1:
            tower.setBlowdownCalculationMode(blowdown_modes[blowdown_calculation_mode])

        if blowdown_concentration_ratio is not None:
            tower.setBlowdownConcentrationRatio(blowdown_concentration_ratio)

        if blowdown_markup_water_schedule is not None:
            tower.setBlowdownMakeupWaterUsageSchedule(blowdown_markup_water_schedule)

        return tower

    @staticmethod
    def evaporative_fluid_cooler_two_speed(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            high_fan_speed_air_flow_rate=None,
            high_fan_speed_fan_power=None,
            low_fan_speed_air_flow_rate=None,
            low_fan_speed_fan_power=None,
            low_fan_speed_air_flow_sizing_factor=None,
            low_fan_speed_power_sizing_factor=None,
            design_water_flow_rate=None,
            design_spray_water_flow_rate=None,
            performance_input_method: int = 1,
            heat_rejection_cap_nominal_cap_ratio=None,
            high_speed_standard_design_capacity=None,
            low_speed_standard_design_capacity=None,
            low_speed_standard_capacity_sizing_factor=None,
            high_speed_u_factor_area=None,
            low_speed_u_factor_area=None,
            high_speed_user_specified_design_capacity=None,
            low_speed_user_specified_design_capacity=None,
            low_speed_user_specified_capacity_sizing_factor=None,
            design_entering_water_temp=None,
            design_entering_air_temp=None,
            design_entering_air_web_bulb_temp=None,
            high_speed_sizing_factor=None,
            evaporation_loss_mode: int = 1,
            evaporation_loss_factor=None,
            drift_loss_percent=None,
            blowdown_calculation_mode: int = 1,
            blowdown_concentration_ratio=None,
            blowdown_markup_water_schedule=None):

        """
        -Performance_input_method: \n
        1:UFactorTimesAreaAndDesignWaterFlowRate \n
        2:StandardDesignCapacity \n
        3:UserSpecifiedDesignCapacity \n

        -Evaporation_loss_mode: 1:LossFactor 2:SaturatedExit

        -Blowdown_calculation_mode: 1:ConcentrationRatio 2:ScheduledRate

        -Capacity_control: 1:FanCycling 2:FluidBypass

        -Cell_control: 1:MinimalCell 2:MaximalCell
        """

        performance_methods = {1: "UFactorTimesAreaAndDesignWaterFlowRate", 2: "NominalCapacity",
                               3: "UserSpecifiedDesignCapacity"}
        evap_loss_modes = {1: "LossFactor", 2: "SaturatedExit"}
        blowdown_modes = {1: "ConcentrationRatio", 2: "ScheduledRate"}

        tower = openstudio.openstudiomodel.EvaporativeFluidCoolerTwoSpeed(model)

        if name is not None:
            tower.setName(name)

        if design_water_flow_rate is not None:
            tower.setDesignWaterFlowRate(design_water_flow_rate)
        else:
            tower.autosizeDesignWaterFlowRate()

        if design_spray_water_flow_rate is not None:
            tower.setDesignSprayWaterFlowRate(design_spray_water_flow_rate)

        if high_fan_speed_air_flow_rate is not None:
            tower.setHighFanSpeedAirFlowRate(high_fan_speed_air_flow_rate)
        else:
            tower.autosizeHighFanSpeedAirFlowRate()

        if high_fan_speed_fan_power is not None:
            tower.setHighFanSpeedFanPower(high_fan_speed_fan_power)
        else:
            tower.autosizeHighFanSpeedFanPower()

        if high_speed_u_factor_area is not None:
            tower.setHighFanSpeedUfactorTimesAreaValue(high_speed_u_factor_area)
        else:
            tower.autosizeHighFanSpeedUfactorTimesAreaValue()

        if low_fan_speed_air_flow_rate is not None:
            tower.setLowFanSpeedAirFlowRate(low_fan_speed_air_flow_rate)
        else:
            tower.autosizeLowFanSpeedAirFlowRate()

        if low_fan_speed_fan_power is not None:
            tower.setLowFanSpeedFanPower(low_fan_speed_fan_power)
        else:
            tower.autosizeLowFanSpeedFanPower()

        if low_fan_speed_air_flow_sizing_factor is not None:
            tower.setLowFanSpeedAirFlowRateSizingFactor(low_fan_speed_air_flow_sizing_factor)

        if low_fan_speed_power_sizing_factor is not None:
            tower.setLowFanSpeedFanPowerSizingFactor(low_fan_speed_power_sizing_factor)

        if low_speed_u_factor_area is not None:
            tower.setLowFanSpeedUfactorTimesAreaValue(low_speed_u_factor_area)
        else:
            tower.autosizeLowFanSpeedUfactorTimesAreaValue()

        if performance_input_method != 1:
            tower.setPerformanceInputMethod(performance_methods[performance_input_method])

        if heat_rejection_cap_nominal_cap_ratio is not None:
            tower.setHeatRejectionCapacityandNominalCapacitySizingRatio(heat_rejection_cap_nominal_cap_ratio)

        if high_speed_standard_design_capacity is not None:
            tower.setHighSpeedStandardDesignCapacity(high_speed_standard_design_capacity)

        if low_speed_standard_design_capacity is not None:
            tower.setLowSpeedStandardDesignCapacity(low_speed_standard_design_capacity)
        else:
            tower.autosizeLowSpeedStandardDesignCapacity()

        if low_speed_standard_capacity_sizing_factor is not None:
            tower.setLowSpeedStandardCapacitySizingFactor(low_speed_standard_capacity_sizing_factor)

        if high_speed_user_specified_design_capacity is not None:
            tower.setHighSpeedUserSpecifiedDesignCapacity(high_speed_user_specified_design_capacity)

        if low_speed_user_specified_design_capacity is not None:
            tower.setLowSpeedUserSpecifiedDesignCapacity(low_speed_user_specified_design_capacity)
        else:
            tower.autosizeLowSpeedUserSpecifiedDesignCapacity()

        if low_speed_user_specified_capacity_sizing_factor is not None:
            tower.setLowSpeedUserSpecifiedDesignCapacitySizingFactor(low_speed_user_specified_capacity_sizing_factor)

        if design_entering_water_temp is not None:
            tower.setDesignEnteringWaterTemperature(design_entering_water_temp)
        if design_entering_air_temp is not None:
            tower.setDesignEnteringAirTemperature(design_entering_air_temp)
        if design_entering_air_web_bulb_temp is not None:
            tower.setDesignEnteringAirWetbulbTemperature(design_entering_air_web_bulb_temp)

        if high_speed_sizing_factor is not None:
            tower.setHighSpeedSizingFactor(high_speed_sizing_factor)

        if evaporation_loss_mode != 1:
            tower.setEvaporationLossMode(evap_loss_modes[evaporation_loss_mode])

        if evaporation_loss_factor is not None:
            tower.setEvaporationLossFactor(evaporation_loss_factor)

        if drift_loss_percent is not None:
            tower.setDriftLossPercent(drift_loss_percent)

        if blowdown_calculation_mode != 1:
            tower.setBlowdownCalculationMode(blowdown_modes[blowdown_calculation_mode])

        if blowdown_concentration_ratio is not None:
            tower.setBlowdownConcentrationRatio(blowdown_concentration_ratio)

        if blowdown_markup_water_schedule is not None:
            tower.setBlowdownMakeupWaterUsageSchedule(blowdown_markup_water_schedule)

        return tower

    # ***************************************************************************************************
    # Distribution Equipments
    @staticmethod
    def pump_variable_speed(
            model: openstudio.openstudiomodel.Model,
            name=None,
            rated_head=None,
            rated_flow_rate=None,
            min_flow_rate=None,
            rated_power=None,
            motor_efficiency=None,
            control_type: int = 1,
            vfd_control_type: int = 1,
            power_sizing_method: int = 1,
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
            skin_loss_radiative_fraction=None,
            pump_curve_coeff=None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -VFD_control_type: 1:PressureSetPointControl 2:ManualControl \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        vfd_control_types = {1: "PressureSetPointControl", 2: "ManualControl"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

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
        if control_type != 1:
            pump.setPumpControlType(control_types[control_type])
        if power_sizing_method != 1:
            pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)
        if vfd_control_type != 1:
            pump.setVFDControlType(vfd_control_types[vfd_control_type])

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
            control_type: int = 1,
            power_sizing_method: int = 1,
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

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
        if control_type != 1:
            pump.setPumpControlType(control_types[control_type])
        if power_sizing_method != 1:
            pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)

        if thermal_zone is not None:
            pump.setZone(thermal_zone)

        return pump

    @staticmethod
    def headered_pumps_variable_speed(
            model: openstudio.openstudiomodel.Model,
            name=None,
            rated_flow_rate=None,
            number_of_pumps_in_bank: int = 2,
            rated_head=None,
            rated_power=None,
            motor_efficiency=None,
            fraction_motor_inefficiencies_to_fluid_stream=None,
            min_flow_rate_fraction=None,
            control_type: int = 1,
            pump_flow_schedule=None,
            power_sizing_method: int = 1,
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
            skin_loss_radiative_fraction=None,
            pump_curve_coeff=None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        pump = openstudio.openstudiomodel.HeaderedPumpsVariableSpeed(model)

        if name is not None:
            pump.setName(name)
        if rated_head is not None:
            pump.setRatedPumpHead(rated_head)

        if rated_flow_rate is not None:
            pump.setTotalRatedFlowRate(rated_flow_rate)
        else:
            pump.autosizeTotalRatedFlowRate()

        pump.setNumberofPumpsinBank(number_of_pumps_in_bank)

        if min_flow_rate_fraction is not None:
            pump.setMinimumFlowRateFraction(min_flow_rate_fraction)

        if rated_power is not None:
            pump.setRatedPowerConsumption(rated_power)
        else:
            pump.autosizeRatedPowerConsumption()

        if motor_efficiency is not None:
            pump.setMotorEfficiency(motor_efficiency)
        if fraction_motor_inefficiencies_to_fluid_stream is not None:
            pump.setFractionofMotorInefficienciestoFluidStream(fraction_motor_inefficiencies_to_fluid_stream)
        if control_type != 1:
            pump.setPumpControlType(control_types[control_type])
        if pump_flow_schedule is not None:
            pump.setPumpFlowRateSchedule(pump_flow_schedule)
        if power_sizing_method != 1:
            pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)

        if thermal_zone is not None:
            pump.setThermalZone(thermal_zone)
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
    def headered_pumps_constant_speed(
            model: openstudio.openstudiomodel.Model,
            name=None,
            rated_flow_rate=None,
            number_of_pumps_in_bank: int = 2,
            rated_head=None,
            rated_power=None,
            motor_efficiency=None,
            fraction_motor_inefficiencies_to_fluid_stream=None,
            control_type: int = 1,
            pump_flow_schedule=None,
            power_sizing_method: int = 1,
            power_per_flow_rate=None,
            power_per_flow_rate_per_head=None,
            thermal_zone: openstudio.openstudiomodel.ThermalZone = None,
            skin_loss_radiative_fraction=None):

        """
        -Control_type: 1:Intermittent 2:Continuous \n
        -Power_sizing_method: 1:PowerPerFlowPerPressure 2:PowerPerFlow
        """

        control_types = {1: "Intermittent", 2: "Continuous"}
        sizing_methods = {1: "PowerPerFlowPerPressure", 2: "PowerPerFlow"}

        pump = openstudio.openstudiomodel.HeaderedPumpsConstantSpeed(model)

        if name is not None:
            pump.setName(name)
        if rated_head is not None:
            pump.setRatedPumpHead(rated_head)

        if rated_flow_rate is not None:
            pump.setTotalRatedFlowRate(rated_flow_rate)
        else:
            pump.autosizeTotalRatedFlowRate()

        pump.setNumberofPumpsinBank(number_of_pumps_in_bank)

        if rated_power is not None:
            pump.setRatedPowerConsumption(rated_power)
        else:
            pump.autosizeRatedPowerConsumption()

        if motor_efficiency is not None:
            pump.setMotorEfficiency(motor_efficiency)
        if fraction_motor_inefficiencies_to_fluid_stream is not None:
            pump.setFractionofMotorInefficienciestoFluidStream(fraction_motor_inefficiencies_to_fluid_stream)
        if control_type != 1:
            pump.setPumpControlType(control_types[control_type])
        if pump_flow_schedule is not None:
            pump.setPumpFlowRateSchedule(pump_flow_schedule)
        if power_sizing_method != 1:
            pump.setDesignPowerSizingMethod(sizing_methods[power_sizing_method])
        if power_per_flow_rate is not None:
            pump.setDesignElectricPowerPerUnitFlowRate(power_per_flow_rate)
        if power_per_flow_rate_per_head is not None:
            pump.setDesignShaftPowerPerUnitFlowRatePerUnitHead(power_per_flow_rate_per_head)

        if thermal_zone is not None:
            pump.setThermalZone(thermal_zone)
        if skin_loss_radiative_fraction is not None:
            pump.setSkinLossRadiativeFraction(skin_loss_radiative_fraction)

        return pump

    # ***************************************************************************************************
    # Others
    @staticmethod
    def adiabatic_pipe(model: openstudio.openstudiomodel.Model):
        pipe = openstudio.openstudiomodel.PipeAdiabatic(model)
        return pipe
