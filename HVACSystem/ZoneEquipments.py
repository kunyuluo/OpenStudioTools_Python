import openstudio
from Schedules.ScheduleTools import ScheduleTool
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent


class ZoneEquipment:
    model_null_message = "Model cannot be empty"

    # @staticmethod
    # def ideal_load_air_system(
    #         model: openstudio.openstudiomodel.Model,
    #         name: str = None,
    #         schedule=None,
    #         max_heating_supply_air_temp=None,
    #         min_cooling_supply_air_temp=None,
    #         max_heating_supply_air_humidity_ratio=None,
    #         min_cooling_supply_air_humidity_ratio=None,
    #         heating_limit: str = None,
    #         cooling_limit: str = None,
    #         max_heating_air_flow_rate=None,
    #         max_sensible_heating_capacity=None,
    #         max_cooling_air_flow_rate=None,
    #         max_total_cooling_capacity=None,
    #         dehumidification_control_type: str = None,
    #         cooling_sensible_heat_ratio=None,
    #         humidification_control_type: str = None,
    #         design_specification_outdoor_air: openstudio.openstudiomodel.DesignSpecificationOutdoorAir = None,
    #         dcv_type: str = None,
    #         economizer_type: str = None,
    #         heat_recovery_type: str = None,
    #         sensible_heat_recovery_effectiveness=None,
    #         latent_heat_recovery_effectiveness=None):
    #
    #     ideal_sys = openstudio.openstudiomodel.ZoneHVACIdealLoadsAirSystem(model)
    #     if name is not None:
    #         ideal_sys.setName(name)
    #
    #     if schedule is not None:
    #         ideal_sys.setAvailabilitySchedule(schedule)
    #
    #     return ideal_sys

    @staticmethod
    def zone_equipment_group(
            thermal_zone: openstudio.openstudiomodel.ThermalZone,
            zone_equipments: list,
            load_sequence_fractions: list = None,
            load_distribution_scheme: int = 1):

        """
        -Load_distribution_scheme: \n
        1.SequentialLoad 2.UniformLoad 3.UniformPLR 4.SequentialUniformPLR
        """

        distribution_schemes = {1: "SequentialLoad", 2: "UniformLoad", 3: "UniformPLR", 4: "SequentialUniformPLR"}

        group = openstudio.openstudiomodel.ZoneHVACEquipmentList(thermal_zone)

        if len(zone_equipments) != 0:
            fraction = 1 / len(zone_equipments)
            for i, equipment in enumerate(zone_equipments):
                group.addEquipment(equipment)

                group.setCoolingPriority(equipment, i + 1)
                group.setHeatingPriority(equipment, i + 1)

                if load_sequence_fractions is not None and len(load_sequence_fractions) == len(zone_equipments):
                    group.setSequentialCoolingFraction(equipment, load_sequence_fractions[i])
                    group.setSequentialHeatingFraction(equipment, load_sequence_fractions[i])
                else:
                    group.setSequentialCoolingFraction(equipment, fraction)
                    group.setSequentialHeatingFraction(equipment, fraction)

        group.setLoadDistributionScheme(distribution_schemes[load_distribution_scheme])

    @staticmethod
    def packaged_terminal_air_conditioner(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            fan=None,
            heating_coil=None,
            cooling_coil=None,
            thermal_zone=None):

        if model is not None:
            if schedule is not None:
                equip_schedule = schedule
            else:
                equip_schedule = ScheduleTool.always_on(model)
            if fan is not None:
                equip_fan = fan
            else:
                equip_fan = AirLoopComponent.fan_constant_speed(model)
            if heating_coil is not None:
                equip_heating_coil = heating_coil
            else:
                equip_heating_coil = AirLoopComponent.coil_heating_electric(model)
            if cooling_coil is not None:
                equip_cooling_coil = cooling_coil
            else:
                equip_cooling_coil = AirLoopComponent.coil_cooling_dx_single_speed(model)

            heating_coil_type = str(type(equip_heating_coil)).split('.')[-1].split("'")[0]
            cooling_coil_type = str(type(equip_cooling_coil)).split('.')[-1].split("'")[0]
            fan_type = str(type(equip_fan)).split('.')[-1].split("'")[0]

            heating_coil_type_check = heating_coil_type == "CoilHeatingWater" \
                                      or heating_coil_type == "CoilHeatingElectric" \
                                      or heating_coil_type == "CoilHeatingGas"

            cooling_coil_type_check = cooling_coil_type == "CoilCoolingDXHeatExchangerAssisted" \
                                      or cooling_coil_type == "CoilCoolingDX" \
                                      or cooling_coil_type == "CoilCoolingDXSingleSpeed" \
                                      or cooling_coil_type == "CoilCoolingDXVariableSpeed"
            fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"

            type_check_list = {
                "heating": heating_coil_type_check,
                "cooling": cooling_coil_type_check,
                "fan": fan_type_check}

            type_error_message = {
                "heating": "Heating coil type can only be CoilHeatingWater, CoilHeatingElectric, or CoilHeatingGas",
                "cooling": "Cooling coil type can only be CoilCoolingDXHeatExchangerAssisted, CoilCoolingDX, "
                           "CoilCoolingDXSingleSpeed or CoilCoolingDXVariableSpeed",
                "fan": "Fan type can only be FanConstantVolume or FanSystemModel"}

            if fan_type_check and cooling_coil_type_check and heating_coil_type_check:
                equipment = openstudio.openstudiomodel.ZoneHVACPackagedTerminalAirConditioner(
                    model,
                    equip_schedule,
                    equip_fan,
                    equip_heating_coil,
                    equip_cooling_coil)

                if name is not None:
                    equipment.setName(name)

                if thermal_zone is not None:
                    equipment.addToThermalZone(thermal_zone)

                return equipment
            else:
                for key in type_check_list.keys():
                    if not type_check_list[key]:
                        raise TypeError(type_error_message[key])
        else:
            raise ValueError(ZoneEquipment.model_null_message)

    @staticmethod
    def vrf_terminal(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            supply_air_flow_rate_cooling=None,
            supply_air_flow_rate_no_cooling=None,
            supply_air_flow_rate_heating=None,
            supply_air_flow_rate_no_heating=None,
            need_outdoor_air: bool = False,
            outdoor_air_flow_rate_cooling=None,
            outdoor_air_flow_rate_heating=None,
            outdoor_air_flow_rate_no_cooling_heating=None,
            supply_air_fan_schedule=None,
            terminal_on_parasitic_electric_energy=None,
            terminal_off_parasitic_electric_energy=None,
            heating_capacity_sizing_ratio=None,
            max_supply_air_temp_from_supplemental_heater=None,
            max_outdoor_air_temp_for_supplemental_heater=None,
            thermal_zone=None,
            outdoor_unit: openstudio.openstudiomodel.AirConditionerVariableRefrigerantFlow = None):

        terminal = openstudio.openstudiomodel.ZoneHVACTerminalUnitVariableRefrigerantFlow(model)

        if name is not None:
            terminal.setName(name)

        if schedule is not None:
            terminal.setTerminalUnitAvailabilityschedule(schedule)

        if supply_air_flow_rate_cooling is not None:
            terminal.setSupplyAirFlowRateDuringCoolingOperation(supply_air_flow_rate_cooling)
        else:
            terminal.autosizeSupplyAirFlowRateDuringCoolingOperation()
        if supply_air_flow_rate_no_cooling is not None:
            terminal.setSupplyAirFlowRateWhenNoCoolingisNeeded(supply_air_flow_rate_no_cooling)
        else:
            terminal.autosizeSupplyAirFlowRateWhenNoCoolingisNeeded()
        if supply_air_flow_rate_heating is not None:
            terminal.setSupplyAirFlowRateDuringHeatingOperation(supply_air_flow_rate_heating)
        else:
            terminal.autosizeSupplyAirFlowRateDuringHeatingOperation()
        if supply_air_flow_rate_no_heating is not None:
            terminal.setSupplyAirFlowRateWhenNoHeatingisNeeded(supply_air_flow_rate_no_heating)
        else:
            terminal.autosizeSupplyAirFlowRateWhenNoHeatingisNeeded()

        if need_outdoor_air:
            if outdoor_air_flow_rate_cooling is not None:
                terminal.setOutdoorAirFlowRateDuringCoolingOperation(outdoor_air_flow_rate_cooling)
            else:
                terminal.autosizeOutdoorAirFlowRateDuringCoolingOperation()
            if outdoor_air_flow_rate_heating is not None:
                terminal.setOutdoorAirFlowRateDuringHeatingOperation(outdoor_air_flow_rate_heating)
            else:
                terminal.autosizeOutdoorAirFlowRateDuringHeatingOperation()
            if outdoor_air_flow_rate_no_cooling_heating is not None:
                terminal.setOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded(outdoor_air_flow_rate_no_cooling_heating)
            else:
                terminal.autosizeOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded()
        else:
            terminal.setOutdoorAirFlowRateDuringCoolingOperation(0)
            terminal.setOutdoorAirFlowRateDuringHeatingOperation(0)
            terminal.setOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded(0)

        if supply_air_fan_schedule is not None:
            terminal.setSupplyAirFanOperatingModeSchedule(supply_air_fan_schedule)

        if terminal_on_parasitic_electric_energy is not None:
            terminal.setZoneTerminalUnitOnParasiticElectricEnergyUse(terminal_on_parasitic_electric_energy)
        if terminal_off_parasitic_electric_energy is not None:
            terminal.setZoneTerminalUnitOffParasiticElectricEnergyUse(terminal_off_parasitic_electric_energy)

        if heating_capacity_sizing_ratio is not None:
            terminal.setRatedTotalHeatingCapacitySizingRatio(heating_capacity_sizing_ratio)

        if max_supply_air_temp_from_supplemental_heater is not None:
            terminal.setMaximumSupplyAirTemperaturefromSupplementalHeater(max_supply_air_temp_from_supplemental_heater)
        else:
            terminal.autosizeMaximumSupplyAirTemperaturefromSupplementalHeater()

        if max_outdoor_air_temp_for_supplemental_heater is not None:
            terminal.setMaximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation(
                max_outdoor_air_temp_for_supplemental_heater)

        if thermal_zone is not None:
            terminal.setControllingZoneorThermostatLocation(thermal_zone)
            terminal.addToThermalZone(thermal_zone)

        if outdoor_unit is not None:
            outdoor_unit.addTerminal(terminal)

        return terminal

    @staticmethod
    def vrf_terminal_adv(
            model: openstudio.openstudiomodel.Model,
            cooling_coil: openstudio.openstudiomodel.CoilCoolingDXVariableRefrigerantFlow,
            heating_coil: openstudio.openstudiomodel.CoilHeatingDXVariableRefrigerantFlow,
            fan,
            name: str = None,
            schedule=None,
            supply_air_flow_rate_cooling=None,
            supply_air_flow_rate_no_cooling=None,
            supply_air_flow_rate_heating=None,
            supply_air_flow_rate_no_heating=None,
            need_outdoor_air: bool = False,
            outdoor_air_flow_rate_cooling=None,
            outdoor_air_flow_rate_heating=None,
            outdoor_air_flow_rate_no_cooling_heating=None,
            supply_air_fan_schedule=None,
            terminal_on_parasitic_electric_energy=None,
            terminal_off_parasitic_electric_energy=None,
            heating_capacity_sizing_ratio=None,
            max_supply_air_temp_from_supplemental_heater=None,
            max_outdoor_air_temp_for_supplemental_heater=None,
            thermal_zone=None,
            outdoor_unit: openstudio.openstudiomodel.AirConditionerVariableRefrigerantFlow = None):

        fan_type = str(type(fan)).split('.')[-1].split("'")[0]
        fan_type_check = fan_type == "FanConstantVolume" \
                         or fan_type == "FanSystemModel" \
                         or fan_type == "FanOnOff"

        if fan_type_check:
            terminal_fan = fan
        else:
            terminal_fan = AirLoopComponent.fan_constant_speed(model)

        terminal = openstudio.openstudiomodel.ZoneHVACTerminalUnitVariableRefrigerantFlow(
            model, cooling_coil, heating_coil, terminal_fan)

        if name is not None:
            terminal.setName(name)

        if schedule is not None:
            terminal.setTerminalUnitAvailabilityschedule(schedule)

        if supply_air_flow_rate_cooling is not None:
            terminal.setSupplyAirFlowRateDuringCoolingOperation(supply_air_flow_rate_cooling)
        else:
            terminal.autosizeSupplyAirFlowRateDuringCoolingOperation()
        if supply_air_flow_rate_no_cooling is not None:
            terminal.setSupplyAirFlowRateWhenNoCoolingisNeeded(supply_air_flow_rate_no_cooling)
        else:
            terminal.autosizeSupplyAirFlowRateWhenNoCoolingisNeeded()
        if supply_air_flow_rate_heating is not None:
            terminal.setSupplyAirFlowRateDuringHeatingOperation(supply_air_flow_rate_heating)
        else:
            terminal.autosizeSupplyAirFlowRateDuringHeatingOperation()
        if supply_air_flow_rate_no_heating is not None:
            terminal.setSupplyAirFlowRateWhenNoHeatingisNeeded(supply_air_flow_rate_no_heating)
        else:
            terminal.autosizeSupplyAirFlowRateWhenNoHeatingisNeeded()

        if need_outdoor_air:
            if outdoor_air_flow_rate_cooling is not None:
                terminal.setOutdoorAirFlowRateDuringCoolingOperation(outdoor_air_flow_rate_cooling)
            else:
                terminal.autosizeOutdoorAirFlowRateDuringCoolingOperation()
            if outdoor_air_flow_rate_heating is not None:
                terminal.setOutdoorAirFlowRateDuringHeatingOperation(outdoor_air_flow_rate_heating)
            else:
                terminal.autosizeOutdoorAirFlowRateDuringHeatingOperation()
            if outdoor_air_flow_rate_no_cooling_heating is not None:
                terminal.setOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded(outdoor_air_flow_rate_no_cooling_heating)
            else:
                terminal.autosizeOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded()
        else:
            terminal.setOutdoorAirFlowRateDuringCoolingOperation(0)
            terminal.setOutdoorAirFlowRateDuringHeatingOperation(0)
            terminal.setOutdoorAirFlowRateWhenNoCoolingorHeatingisNeeded(0)

        if supply_air_fan_schedule is not None:
            terminal.setSupplyAirFanOperatingModeSchedule(supply_air_fan_schedule)

        if terminal_on_parasitic_electric_energy is not None:
            terminal.setZoneTerminalUnitOnParasiticElectricEnergyUse(terminal_on_parasitic_electric_energy)
        if terminal_off_parasitic_electric_energy is not None:
            terminal.setZoneTerminalUnitOffParasiticElectricEnergyUse(terminal_off_parasitic_electric_energy)

        if heating_capacity_sizing_ratio is not None:
            terminal.setRatedTotalHeatingCapacitySizingRatio(heating_capacity_sizing_ratio)

        if max_supply_air_temp_from_supplemental_heater is not None:
            terminal.setMaximumSupplyAirTemperaturefromSupplementalHeater(max_supply_air_temp_from_supplemental_heater)
        else:
            terminal.autosizeMaximumSupplyAirTemperaturefromSupplementalHeater()

        if max_outdoor_air_temp_for_supplemental_heater is not None:
            terminal.setMaximumOutdoorDryBulbTemperatureforSupplementalHeaterOperation(
                max_outdoor_air_temp_for_supplemental_heater)

        if thermal_zone is not None:
            terminal.setControllingZoneorThermostatLocation(thermal_zone)

        if outdoor_unit is not None:
            outdoor_unit.addTerminal(terminal)

        return terminal

    @staticmethod
    def fan_coil_unit(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            capacity_control_method: int = 0,
            heating_coil_type: int = 1,
            fan_pressure_rise=None,
            max_supply_air_flow_rate=None,
            low_speed_supply_air_flow_ratio=None,
            medium_speed_supply_air_flow_ratio=None,
            max_outdoor_air_flow_rate=None,
            outdoor_air_schedule=None,
            max_cold_water_flow_rate=None,
            min_cold_water_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            supply_air_fan_operating_mode_schedule=None,
            min_supply_air_temp_cooling=None,
            max_supply_air_temp_heating=None,
            chilled_water_loop: openstudio.openstudiomodel.PlantLoop = None,
            hot_water_loop: openstudio.openstudiomodel.PlantLoop = None):

        """
        -Options for "capacity_control_method":
            0:"ConstantFanVariableFlow",
            1:"VariableFanVariableFlow",
            2:"VariableFanConstantFlow",
            3:"CyclingFan",
            4:"MultiSpeedFan",
            5:"ASHRAE90VariableFan" \n

        -Heating coil type:
            1:Water,
            2:Electric
        """

        # Create a fan object based on control method:
        match capacity_control_method:
            case 0:
                fan = AirLoopComponent.fan_constant_speed(model, pressure_rise=fan_pressure_rise)
            case [1, 2]:
                fan = AirLoopComponent.fan_variable_speed(model, pressure_rise=fan_pressure_rise)
            case [3, 4, 5] | _:
                fan = AirLoopComponent.fan_on_off(model, pressure_rise=fan_pressure_rise)

        # Create a heating coil object based on control method:
        match heating_coil_type:
            case 1:
                heating_coil = AirLoopComponent.coil_heating_water(model)
            case 2 | _:
                heating_coil = AirLoopComponent.coil_heating_electric(model)

        # Create a cooling coil object:
        cooling_coil = AirLoopComponent.coil_cooling_water(model)

        equipment = openstudio.openstudiomodel.ZoneHVACFourPipeFanCoil(
            model, ScheduleTool.always_on(model), fan, cooling_coil, heating_coil)

        if name is not None:
            equipment.setName(name)

        if capacity_control_method is not None:
            equipment.setCapacityControlMethod(capacity_control_method)

        if max_supply_air_flow_rate is not None:
            equipment.setMaximumSupplyAirFlowRate(max_supply_air_flow_rate)
        else:
            equipment.autosizeMaximumSupplyAirFlowRate()

        if low_speed_supply_air_flow_ratio is not None:
            equipment.setLowSpeedSupplyAirFlowRatio(low_speed_supply_air_flow_ratio)

        if medium_speed_supply_air_flow_ratio is not None:
            equipment.setMediumSpeedSupplyAirFlowRatio(medium_speed_supply_air_flow_ratio)

        if max_outdoor_air_flow_rate is not None:
            equipment.setMaximumOutdoorAirFlowRate(max_outdoor_air_flow_rate)
        else:
            equipment.autosizeMaximumOutdoorAirFlowRate()

        if outdoor_air_schedule is not None:
            equipment.setOutdoorAirSchedule(outdoor_air_schedule)

        if max_cold_water_flow_rate is not None:
            equipment.setMaximumColdWaterFlowRate(max_cold_water_flow_rate)
        else:
            equipment.autosizeMaximumColdWaterFlowRate()

        if min_cold_water_flow_rate is not None:
            equipment.setMinimumColdWaterFlowRate(min_cold_water_flow_rate)

        if max_hot_water_flow_rate is not None:
            equipment.setMaximumHotWaterFlowRate(max_hot_water_flow_rate)
        else:
            equipment.autosizeMaximumColdWaterFlowRate()

        if min_hot_water_flow_rate is not None:
            equipment.setMinimumHotWaterFlowRate(min_hot_water_flow_rate)

        if supply_air_fan_operating_mode_schedule is not None:
            equipment.setSupplyAirFanOperatingModeSchedule(supply_air_fan_operating_mode_schedule)

        if min_supply_air_temp_cooling is not None:
            equipment.setMinimumSupplyAirTemperatureInCoolingMode(min_supply_air_temp_cooling)
        else:
            equipment.autosizeMinimumSupplyAirTemperatureInCoolingMode()

        if max_supply_air_temp_heating is not None:
            equipment.setMaximumSupplyAirTemperatureInHeatingMode(max_supply_air_temp_heating)
        else:
            equipment.autosizeMaximumSupplyAirTemperatureInHeatingMode()

        # Add cooling coil to the chilled water loop if applicable:
        if chilled_water_loop is not None:
            chilled_water_loop.addDemandBranchForComponent(cooling_coil)

        # Add heating coil to the chilled water loop if applicable:
        if heating_coil_type == "Water" and hot_water_loop is not None:
            hot_water_loop.addDemandBranchForComponent(heating_coil)

        return equipment

    @staticmethod
    def low_temperature_radiant_electric(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            max_electrical_power=None,
            radiant_surface_type: int = 1,
            temperature_control_type: int = 1,
            setpoint_control_type: int = 2,
            availability_schedule=None,
            heating_setpoint_schedule=None,
            heating_throttling_range=None):

        """
        Radiant_surface_type: \n
        1.Ceilings 2.Floors 3.CeilingsAndFloors 4.AllSurfaces \n

        Temperature_control_type: \n
        1.MeanAirTemperature 2.MeanRadiantTemperature 3.OperativeTemperature
        4.OutdoorDryBulbTemperature 5.OutdoorWetBulbTemperature 6.SurfaceFaceTemperature 7.SurfaceInteriorTemperature \n

        Setpoint_control_type: \n
        1.ZeroFlowPower 2.HalfFlowPower \n
        """

        surface_types = {1: "Ceilings", 2: "Floors", 3: "CeilingsAndFloors", 4: "AllSurfaces"}
        temp_control_types = {1: "MeanAirTemperature", 2: "MeanRadiantTemperature", 3: "OperativeTemperature",
                              4: "OutdoorDryBulbTemperature", 5: "OutdoorWetBulbTemperature",
                              6: "SurfaceFaceTemperature", 7: "SurfaceInteriorTemperature"}
        setpoint_control_types = {1: "ZeroFlowPower", 2: "HalfFlowPower"}

        if availability_schedule is not None:
            schedule = availability_schedule
        else:
            schedule = ScheduleTool.always_on(model)

        if heating_setpoint_schedule is not None:
            heating_schedule = heating_setpoint_schedule
        else:
            type_limit = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 50)
            heating_schedule = ScheduleTool.schedule_ruleset(model, 21, type_limit, "Low Temp Rad Elec Htg Sch")

        equip = openstudio.openstudiomodel.ZoneHVACLowTemperatureRadiantElectric(model, schedule, heating_schedule)

        if name is not None:
            equip.setName(name)

        if max_electrical_power is not None:
            equip.setMaximumElectricalPowertoPanel(max_electrical_power)
        else:
            equip.autosizeMaximumElectricalPowertoPanel()

        equip.setRadiantSurfaceType(surface_types[radiant_surface_type])
        equip.setTemperatureControlType(temp_control_types[temperature_control_type])
        equip.setSetpointControlType(setpoint_control_types[setpoint_control_type])

        if heating_throttling_range is not None:
            equip.setHeatingThrottlingRange(heating_throttling_range)

        return equip

    @staticmethod
    def low_temperature_radiant_variable_flow(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            radiant_cooling_coil: openstudio.openstudiomodel.CoilCoolingLowTempRadiantVarFlow = None,
            radiant_heating_coil: openstudio.openstudiomodel.CoilHeatingLowTempRadiantVarFlow = None,
            radiant_surface_type: int = 1,
            fluid_to_surface_heat_transfer_model: int = 1,
            temperature_control_type: int = 1,
            setpoint_control_type: int = 2,
            availability_schedule=None,
            hydronic_tube_inside_diameter=None,
            hydronic_tube_outside_diameter=None,
            hydronic_tube_length=None,
            hydronic_tube_conductivity=None,
            number_of_circuits: int = None,
            circuit_length=None,
            changeover_delay_schedule=None,):

        """
        Radiant_surface_type: \n
        1.Ceilings 2.Floors 3.CeilingsAndFloors 4.AllSurfaces \n

        Fluid_to_radiant_surface_heat_transfer_model: \n
        1.ConvectionOnly 2.ISOStandard \n

        Temperature_control_type: \n
        1.MeanAirTemperature 2.MeanRadiantTemperature 3.OperativeTemperature
        4.OutdoorDryBulbTemperature 5.OutdoorWetBulbTemperature 6.SurfaceFaceTemperature 7.SurfaceInteriorTemperature \n

        Setpoint_control_type: \n
        1.ZeroFlowPower 2.HalfFlowPower \n

        Number of Circuits: \n
        1.OnePerSurface 2.CalculateFromCircuitLength
        """

        surface_types = {1: "Ceilings", 2: "Floors", 3: "CeilingsAndFloors", 4: "AllSurfaces"}
        heat_transfer_models = {1: "ConvectionOnly", 2: "ISOStandard"}
        temp_control_types = {1: "MeanAirTemperature", 2: "MeanRadiantTemperature", 3: "OperativeTemperature",
                              4: "OutdoorDryBulbTemperature", 5: "OutdoorWetBulbTemperature",
                              6: "SurfaceFaceTemperature", 7: "SurfaceInteriorTemperature"}
        setpoint_control_types = {1: "ZeroFlowPower", 2: "HalfFlowPower"}
        circuits = {1: "OnePerSurface", 2: "CalculateFromCircuitLength"}

        if availability_schedule is not None:
            schedule = availability_schedule
        else:
            schedule = ScheduleTool.always_on(model)

        if radiant_cooling_coil is not None:
            cooling_coil = radiant_cooling_coil
        else:
            cooling_coil = AirLoopComponent.coil_cooling_low_temperature_radiant_variable_flow(model)

        if radiant_heating_coil is not None:
            heating_coil = radiant_heating_coil
        else:
            heating_coil = AirLoopComponent.coil_heating_low_temperature_radiant_variable_flow(model)

        equip = openstudio.openstudiomodel.ZoneHVACLowTempRadiantVarFlow(model, schedule, heating_coil, cooling_coil)

        if name is not None:
            equip.setName(name)

        equip.setRadiantSurfaceType(surface_types[radiant_surface_type])
        equip.setFluidtoRadiantSurfaceHeatTransferModel(heat_transfer_models[fluid_to_surface_heat_transfer_model])
        equip.setTemperatureControlType(temp_control_types[temperature_control_type])
        equip.setSetpointControlType(setpoint_control_types[setpoint_control_type])
        if number_of_circuits is not None:
            equip.setNumberofCircuits(circuits[number_of_circuits])

        if circuit_length is not None:
            equip.setCircuitLength(circuit_length)

        if hydronic_tube_inside_diameter is not None:
            equip.setHydronicTubingInsideDiameter(hydronic_tube_inside_diameter)

        if hydronic_tube_outside_diameter is not None:
            equip.setHydronicTubingOutsideDiameter(hydronic_tube_outside_diameter)

        if hydronic_tube_length is not None:
            equip.setHydronicTubingLength(hydronic_tube_length)

        if hydronic_tube_conductivity is not None:
            equip.setHydronicTubingConductivity(hydronic_tube_conductivity)

        if changeover_delay_schedule is not None:
            equip.setChangeoverDelayTimePeriodSchedule(changeover_delay_schedule)

        return equip

    @staticmethod
    def low_temperature_radiant_constant_flow(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            radiant_cooling_coil: openstudio.openstudiomodel.CoilCoolingLowTempRadiantConstFlow = None,
            radiant_heating_coil: openstudio.openstudiomodel.CoilHeatingLowTempRadiantConstFlow = None,
            radiant_surface_type: int = 1,
            fluid_to_surface_heat_transfer_model: int = 1,
            temperature_control_type: int = 1,
            availability_schedule=None,
            hydronic_tube_inside_diameter=None,
            hydronic_tube_outside_diameter=None,
            hydronic_tube_length=None,
            hydronic_tube_conductivity=None,
            rated_flow_rate=None,
            pump_flow_schedule=None,
            rated_pump_head=None,
            rated_power_consumption=None,
            motor_efficiency=None,
            fraction_of_motor_to_fluid=None,
            number_of_circuits: int = None,
            circuit_length=None,
            changeover_delay_schedule=None):

        """
        Radiant_surface_type: \n
        1.Ceilings 2.Floors 3.CeilingsAndFloors 4.AllSurfaces \n

        Fluid_to_radiant_surface_heat_transfer_model: \n
        1.ConvectionOnly 2.ISOStandard \n

        Temperature_control_type: \n
        1.MeanAirTemperature 2.MeanRadiantTemperature 3.OperativeTemperature
        4.OutdoorDryBulbTemperature 5.OutdoorWetBulbTemperature 6.SurfaceFaceTemperature 7.SurfaceInteriorTemperature \n

        Number of Circuits: \n
        1.OnePerSurface 2.CalculateFromCircuitLength
        """

        surface_types = {1: "Ceilings", 2: "Floors", 3: "CeilingsAndFloors", 4: "AllSurfaces"}
        heat_transfer_models = {1: "ConvectionOnly", 2: "ISOStandard"}
        temp_control_types = {1: "MeanAirTemperature", 2: "MeanRadiantTemperature", 3: "OperativeTemperature",
                              4: "OutdoorDryBulbTemperature", 5: "OutdoorWetBulbTemperature",
                              6: "SurfaceFaceTemperature", 7: "SurfaceInteriorTemperature"}
        circuits = {1: "OnePerSurface", 2: "CalculateFromCircuitLength"}

        if availability_schedule is not None:
            schedule = availability_schedule
        else:
            schedule = ScheduleTool.always_on(model)

        if radiant_cooling_coil is not None:
            cooling_coil = radiant_cooling_coil
        else:
            cooling_coil = AirLoopComponent.coil_cooling_low_temperature_radiant_constant_flow(model)

        if radiant_heating_coil is not None:
            heating_coil = radiant_heating_coil
        else:
            heating_coil = AirLoopComponent.coil_heating_low_temperature_radiant_constant_flow(model)

        equip = openstudio.openstudiomodel.ZoneHVACLowTempRadiantVarFlow(model, schedule, heating_coil, cooling_coil)

        if name is not None:
            equip.setName(name)

        equip.setRadiantSurfaceType(surface_types[radiant_surface_type])
        equip.setFluidtoRadiantSurfaceHeatTransferModel(heat_transfer_models[fluid_to_surface_heat_transfer_model])
        equip.setTemperatureControlType(temp_control_types[temperature_control_type])
        if number_of_circuits is not None:
            equip.setNumberofCircuits(circuits[number_of_circuits])

        if circuit_length is not None:
            equip.setCircuitLength(circuit_length)

        if hydronic_tube_inside_diameter is not None:
            equip.setHydronicTubingInsideDiameter(hydronic_tube_inside_diameter)

        if hydronic_tube_outside_diameter is not None:
            equip.setHydronicTubingOutsideDiameter(hydronic_tube_outside_diameter)

        if hydronic_tube_length is not None:
            equip.setHydronicTubingLength(hydronic_tube_length)

        if hydronic_tube_conductivity is not None:
            equip.setHydronicTubingConductivity(hydronic_tube_conductivity)

        if changeover_delay_schedule is not None:
            equip.setChangeoverDelayTimePeriodSchedule(changeover_delay_schedule)

        return equip


