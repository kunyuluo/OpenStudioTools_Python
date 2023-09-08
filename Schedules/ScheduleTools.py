import openstudio.openstudioutilitiestime


class ScheduleTool:
    year = 2023
    model_null_message = "Model cannot be empty"

    # Schedule Type Limits
    @staticmethod
    def schedule_type_limits(
            model,
            unit_type: int = None,
            numeric_type: int = None,
            lower_limit=-9999,
            upper_limit=-9999,
            name: str = None):
        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate

        -Numeric_type: 1.Continuous 2.Discrete
        """

        unit_types = {1: "Dimensionless", 2: "Temperature", 3: "DeltaTemperature", 4: "PrecipitationRate",
                      5: "Angle", 6: "ConvectionCoefficient", 7: "ActivityLevel", 8: "Velocity",
                      9: "Capacity", 10: "Power", 11: "Availability", 12: "Percent",
                      13: "Control", 14: "Mode", 15: "MassFlowRate"}

        numeric_types = {1: "Continuous", 2: "Discrete"}

        if model is not None:
            type_limits = openstudio.openstudiomodel.ScheduleTypeLimits(model)

            # Assign unit type:
            if unit_type is not None:
                try:
                    type_limits.setUnitType(unit_types[unit_type])
                except ValueError:
                    print("Index out of range. Valid options are from 1 to 15.")
            else:
                type_limits.setUnitType(unit_types[1])

            # Assign numeric type:
            if numeric_type is not None:
                try:
                    type_limits.setNumericType(numeric_types[numeric_type])
                except ValueError:
                    print("Index out of range. Valid options are 1 and 2.")
            else:
                type_limits.setNumericType(numeric_types[1])

            if name is not None:
                type_limits.setName(name)
            if lower_limit != -9999:
                type_limits.setLowerLimitValue(lower_limit)
            if upper_limit != -9999:
                type_limits.setUpperLimitValue(upper_limit)

            return type_limits
        else:
            raise ValueError(ScheduleTool.model_null_message)

    # Day Schedule
    @staticmethod
    def schedule_day(model, value, type_limits=None, name=None):
        schedule = openstudio.openstudiomodel.ScheduleDay(model)

        if isinstance(value, float) or isinstance(value, int):
            schedule.addValue(openstudio.Time(0, 24, 0), value)
        elif isinstance(value, list):
            if len(value) == 0:
                schedule.addValue(openstudio.Time(0, 24, 0), 0.0)
            elif len(value) != 24:
                schedule.addValue(openstudio.Time(0, 8, 0), 0.0)
                schedule.addValue(openstudio.Time(0, 18, 0), 1.0)
                schedule.addValue(openstudio.Time(0, 24, 0), 0.0)
            else:
                for i in range(len(value)):
                    schedule.addValue(openstudio.Time(0, i + 1, 0), value[i])
        else:
            schedule.addValue(openstudio.Time(0, 24, 0), 0)
            raise TypeError("Invalid input type of schedule value.")

        if type_limits is not None:
            schedule.setScheduleTypeLimits(type_limits)
        if name is not None:
            schedule.setName(name)

        return schedule

    @staticmethod
    def schedule_year(
            model,
            unit_type: int,
            name: str = None):

        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate
        """

        match unit_type:
            case 1 | 4 | 6 | 11:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 1)
            case 2 | 3:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 60)
            case 7:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 300)
            case _:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 100)

        schedule = openstudio.openstudiomodel.ScheduleYear(model)
        schedule.setScheduleTypeLimits(type_limit)

        if name is not None:
            schedule.setName(name)

        schedule_week1 = openstudio.openstudiomodel.ScheduleWeek(model)
        # schedule.addScheduleWeek(openstudio.Date(openstudio.MonthOfYear(start_m), start_d, ScheduleTool.year))

        return schedule

    # Schedule Rule
    @staticmethod
    def schedule_rule(
            schedule_ruleset,
            schedule_day,
            start_m=1,
            start_d=1,
            end_m=12,
            end_d=31,
            all_week=False,
            days=None,
            name=None):

        schedule_rule = openstudio.openstudiomodel.ScheduleRule(schedule_ruleset, schedule_day)

        if name is not None:
            schedule_rule.setName(name)

        if all_week:
            schedule_rule.setApplyAllDays(True)
        else:
            if days is not None and len(days) == 7:
                schedule_rule.setApplyMonday(days[0])
                schedule_rule.setApplyTuesday(days[1])
                schedule_rule.setApplyWednesday(days[2])
                schedule_rule.setApplyThursday(days[3])
                schedule_rule.setApplyFriday(days[4])
                schedule_rule.setApplySaturday(days[5])
                schedule_rule.setApplySunday(days[6])
            else:
                schedule_rule.setApplyWeekdays(True)
                schedule_rule.setApplyWeekends(True)

        schedule_rule.setStartDate(openstudio.Date(openstudio.MonthOfYear(start_m), start_d, ScheduleTool.year))
        schedule_rule.setEndDate(openstudio.Date(openstudio.MonthOfYear(end_m), end_d, ScheduleTool.year))

        return schedule_rule

    @staticmethod
    def custom_annual_schedule(
            model: openstudio.openstudiomodel.Model,
            unit_type: int,
            weekday_value,
            saturday_value=None,
            sunday_value=None,
            summer_design_day_value=None,
            winter_design_day_value=None,
            name: str = "Default"):

        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate
        """

        match unit_type:
            case 1 | 4 | 6 | 11:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 1)
            case 2 | 3:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 60)
            case 7:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 300)
            case _:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 100)

        schedule = ScheduleTool.schedule_ruleset(model, unit_type, name=name)

        schedule_wd = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                name=name + "_Schedule_Weekdays")
        if saturday_value is not None:
            schedule_sat = ScheduleTool.schedule_day(model, saturday_value, type_limits=type_limit,
                                                     name=name + "_Schedule_Saturday")
        else:
            schedule_sat = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                     name=name + "_Schedule_Saturday")
        if sunday_value is not None:
            schedule_sun = ScheduleTool.schedule_day(model, sunday_value, type_limits=type_limit,
                                                     name=name + "_Schedule_Sunday")
        else:
            schedule_sun = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                     name=name + "_Schedule_Sunday")

        ScheduleTool.schedule_rule(schedule, schedule_wd,
                                   days=[True, True, True, True, True, False, False], name=name + "_Weekdays")
        ScheduleTool.schedule_rule(schedule, schedule_sat,
                                   days=[False, False, False, False, False, True, False], name=name + "_Saturday")
        ScheduleTool.schedule_rule(schedule, schedule_sun,
                                   days=[False, False, False, False, False, False, True], name=name + "_Sunday")

        # Daily Schedule for Design Day:
        if summer_design_day_value is not None:
            schedule_summer = ScheduleTool.schedule_day(model, summer_design_day_value, type_limits=type_limit,
                                                        name=name + "_Schedule_Summer_Design_Day")
            schedule.setSummerDesignDaySchedule(schedule_summer)
        else:
            schedule_summer = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                        name=name + "_Schedule_Summer_Design_Day")
            schedule.setSummerDesignDaySchedule(schedule_summer)

        if winter_design_day_value is not None:
            schedule_winter = ScheduleTool.schedule_day(model, winter_design_day_value, type_limits=type_limit,
                                                        name=name + "_Schedule_Winter_Design_Day")
            schedule.setWinterDesignDaySchedule(schedule_winter)
        else:
            schedule_winter = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                        name=name + "_Schedule_Winter_Design_Day")
            schedule.setWinterDesignDaySchedule(schedule_winter)

        return schedule

    # Schedule Ruleset
    @staticmethod
    def schedule_ruleset(model, unit_type: int, value=-9999.0, name=None):

        """
        -Unit_type: \n
        1.Dimensionless
        2.Temperature
        3.DeltaTemperature
        4.PrecipitationRate
        5.Angle
        6.Convection Coefficient
        7.Activity Level
        8.Velocity
        9.Capacity
        10.Power
        11.Availability
        12.Percent
        13.Control
        14.Mode
        15.MassFlowRate
        """

        match unit_type:
            case 1 | 4 | 6 | 11:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 1)
            case 2 | 3:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 60)
            case 7:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 300)
            case _:
                type_limit = ScheduleTool.schedule_type_limits(model, unit_type, 1, 0, 100)

        if value != -9999:
            schedule_ruleset = openstudio.openstudiomodel.ScheduleRuleset(model, value)

            if unit_type == 2:
                if name is not None:
                    name = name
                else:
                    name = "Temperature"

                summer_values = [value] * 24
                winter_values = [value] * 24
                summer_design_day = ScheduleTool.schedule_day(model, summer_values, type_limit, name + "_Summer")
                winter_design_day = ScheduleTool.schedule_day(model, winter_values, type_limit, name + "_Winter")
                bool1 = schedule_ruleset.setSummerDesignDaySchedule(summer_design_day)
                bool2 = schedule_ruleset.setWinterDesignDaySchedule(winter_design_day)
                # print(bool1)
        else:
            schedule_ruleset = openstudio.openstudiomodel.ScheduleRuleset(model)

        schedule_ruleset.setScheduleTypeLimits(type_limit)

        if name is not None:
            schedule_ruleset.setName(name)

        return schedule_ruleset

    @staticmethod
    def schedule_set(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            occupancy_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            num_of_people_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            people_activity_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            lighting_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            electric_equipment_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            gas_equipment_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            hot_water_equipment_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            steam_equipment_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            other_equipment_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            infiltration_schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        sets = openstudio.openstudiomodel.DefaultScheduleSet(model)

        if name is not None:
            sets.setName(name)

        if occupancy_schedule is not None:
            sets.setHoursofOperationSchedule(occupancy_schedule)

        if num_of_people_schedule is not None:
            sets.setNumberofPeopleSchedule(num_of_people_schedule)

        if people_activity_schedule is not None:
            sets.setPeopleActivityLevelSchedule(people_activity_schedule)

        if lighting_schedule is not None:
            sets.setLightingSchedule(lighting_schedule)

        if electric_equipment_schedule is not None:
            sets.setElectricEquipmentSchedule(electric_equipment_schedule)

        if gas_equipment_schedule is not None:
            sets.setGasEquipmentSchedule(gas_equipment_schedule)

        if hot_water_equipment_schedule is not None:
            sets.setHotWaterEquipmentSchedule(hot_water_equipment_schedule)

        if steam_equipment_schedule is not None:
            sets.setSteamEquipmentSchedule(steam_equipment_schedule)

        if other_equipment_schedule is not None:
            sets.setOtherEquipmentSchedule(other_equipment_schedule)

        if infiltration_schedule is not None:
            sets.setInfiltrationSchedule(infiltration_schedule)

        return sets

    @staticmethod
    def always_on(model):
        schedule = ScheduleTool.schedule_ruleset(model, 11, 1, name="AlwaysOn")

        return schedule

    @staticmethod
    def always_off(model):
        schedule = ScheduleTool.schedule_ruleset(model, 11, 0, name="AlwaysOff")

        return schedule

    @staticmethod
    def dhw_flow_fraction_schedule(model):
        type_limit = ScheduleTool.schedule_type_limits(model, 1, 1, 0, 1)

        schedule = ScheduleTool.schedule_ruleset(
            model, 1, 0, name="ESTAR MFHR DHW Fraction Schedule")

        fraction_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.3, 0.5, 0.4, 0.4, 0.3, 0.35, 0.4, 0.4, 0.35, 0.35, 0.3,
                           0.3, 0.5, 0.4, 0.35, 0.45, 0.3, 0.05]
        schedule_day = ScheduleTool.schedule_day(model, fraction_values, type_limits=type_limit,
                                                 name="ESTAR MFHR DHW Fraction Schedule Day")

        occ_wd_schrule = ScheduleTool.schedule_rule(schedule, schedule_day, all_week=True)

        return schedule

    @staticmethod
    def schedule_set_input_json(space_type=None, schedule_set=None):

        """
        schedule_set: a single ScheduleSets object or a list of ScheduleSets
        """

        schedule_sets = {}

        if space_type is not None and isinstance(space_type, list):
            if schedule_set is not None:
                if isinstance(schedule_set, ScheduleSets):
                    for i, space in enumerate(space_type):
                        schedule_sets[space] = schedule_set.get_schedule_sets()
                elif isinstance(schedule_set, list):
                    if len(schedule_set) == len(space_type):
                        for i, space in enumerate(space_type):
                            schedule_sets[space] = schedule_set[i].get_schedule_sets()
                    else:
                        raise IndexError("Number of space types and number of schedule sets don't match.")
                else:
                    raise TypeError("Invalid input type of schedule set.")

        return schedule_sets


class ScheduleSets:
    def __init__(
            self,
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            occupancy: openstudio.openstudiomodel.ScheduleRuleset = None,
            lighting: openstudio.openstudiomodel.ScheduleRuleset = None,
            electric_equipment: openstudio.openstudiomodel.ScheduleRuleset = None,
            gas_equipment: openstudio.openstudiomodel.ScheduleRuleset = None,
            hot_water_equipment: openstudio.openstudiomodel.ScheduleRuleset = None,
            steam_equipment: openstudio.openstudiomodel.ScheduleRuleset = None,
            other_equipment: openstudio.openstudiomodel.ScheduleRuleset = None,
            infiltration: openstudio.openstudiomodel.ScheduleRuleset = None,
            cooling_setpoint: openstudio.openstudiomodel.ScheduleRuleset = None,
            heating_setpoint: openstudio.openstudiomodel.ScheduleRuleset = None,
            humidify_setpoint: openstudio.openstudiomodel.ScheduleRuleset = None,
            dehumidify_setpoint: openstudio.openstudiomodel.ScheduleRuleset = None,
            hvac_availability: openstudio.openstudiomodel.ScheduleRuleset = None,
            dcv: openstudio.openstudiomodel.ScheduleRuleset = None,
            activity_level: openstudio.openstudiomodel.ScheduleRuleset = None):

        self._model = model
        self._name = name
        self._occupancy = occupancy
        self._lighting = lighting
        self._electric_equipment = electric_equipment
        self._gas_equipment = gas_equipment
        self._hot_water_equipment = hot_water_equipment
        self._steam_equipment = steam_equipment
        self._other_equipment = other_equipment
        self._infiltration = infiltration
        self._cooling_setpoint = cooling_setpoint
        self._heating_setpoint = heating_setpoint
        self._humidify_setpoint = humidify_setpoint
        self._dehumidify_setpoint = dehumidify_setpoint
        self._hvac_availability = hvac_availability
        self._dcv = dcv
        self._activity_level = activity_level

    # ***********************************************************************************************
    # Occupancy schedule getter:
    def occupancy(self):
        return self._occupancy

    # Occupancy schedule setter:
    def set_occupancy(
            self,
            occ_wd_values: list = None,
            occ_sat_values: list = None,
            occ_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            occ_schedule = schedule
        else:
            if occ_wd_values is not None and occ_sat_values is not None and occ_sun_values is not None:
                occ_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, occ_wd_values, occ_sat_values, occ_sun_values, self._name + "_Occupancy")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._occupancy = occ_schedule

    # ***********************************************************************************************
    # Lighting schedule getter:
    def lighting(self):
        return self._lighting

    # Lighting schedule setter:
    def set_lighting(
            self,
            ltg_wd_values: list = None,
            ltg_sat_values: list = None,
            ltg_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            ltg_schedule = schedule
        else:
            if ltg_wd_values is not None and ltg_sat_values is not None and ltg_sun_values is not None:
                ltg_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, ltg_wd_values, ltg_sat_values, ltg_sun_values, self._name + "_Lighting")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._lighting = ltg_schedule

    # ***********************************************************************************************
    # electric equipment schedule getter:
    def electric_equipment(self):
        return self._electric_equipment

    # equipment schedule setter:
    def set_electric_equipment(
            self,
            equip_wd_values: list = None,
            equip_sat_values: list = None,
            equip_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            equip_schedule = schedule
        else:
            if equip_wd_values is not None and equip_sat_values is not None and equip_sun_values is not None:
                equip_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, equip_wd_values, equip_sat_values, equip_sun_values,
                    self._name + "_ElectricEquipment")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._electric_equipment = equip_schedule

    # ***********************************************************************************************
    # electric equipment schedule getter:
    def gas_equipment(self):
        return self._gas_equipment

    # equipment schedule setter:
    def set_gas_equipment(
            self,
            equip_wd_values: list = None,
            equip_sat_values: list = None,
            equip_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            equip_schedule = schedule
        else:
            if equip_wd_values is not None and equip_sat_values is not None and equip_sun_values is not None:
                equip_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, equip_wd_values, equip_sat_values, equip_sun_values,
                    self._name + "_GasEquipment")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._gas_equipment = equip_schedule

    # ***********************************************************************************************
    # electric equipment schedule getter:
    def hot_water_equipment(self):
        return self._hot_water_equipment

    # equipment schedule setter:
    def set_hot_water_equipment(
            self,
            equip_wd_values: list = None,
            equip_sat_values: list = None,
            equip_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            equip_schedule = schedule
        else:
            if equip_wd_values is not None and equip_sat_values is not None and equip_sun_values is not None:
                equip_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, equip_wd_values, equip_sat_values, equip_sun_values,
                    self._name + "_HotWaterEquipment")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._hot_water_equipment = equip_schedule

    # ***********************************************************************************************
    # electric equipment schedule getter:
    def steam_equipment(self):
        return self._steam_equipment

    # equipment schedule setter:
    def set_steam_equipment(
            self,
            equip_wd_values: list = None,
            equip_sat_values: list = None,
            equip_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            equip_schedule = schedule
        else:
            if equip_wd_values is not None and equip_sat_values is not None and equip_sun_values is not None:
                equip_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, equip_wd_values, equip_sat_values, equip_sun_values,
                    self._name + "_SteamEquipment")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._steam_equipment = equip_schedule

    # ***********************************************************************************************
    # electric equipment schedule getter:
    def other_equipment(self):
        return self._other_equipment

    # equipment schedule setter:
    def set_other_equipment(
            self,
            equip_wd_values: list = None,
            equip_sat_values: list = None,
            equip_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            equip_schedule = schedule
        else:
            if equip_wd_values is not None and equip_sat_values is not None and equip_sun_values is not None:
                equip_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, equip_wd_values, equip_sat_values, equip_sun_values,
                    self._name + "_OtherEquipment")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._other_equipment = equip_schedule

    # ***********************************************************************************************
    # infiltration schedule getter:
    def infiltration(self):
        return self._infiltration

    # infiltration schedule setter:
    def set_infiltration(
            self,
            inf_wd_values: list = None,
            inf_sat_values: list = None,
            inf_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            inf_schedule = schedule
        else:
            if inf_wd_values is not None and inf_sat_values is not None and inf_sun_values is not None:
                inf_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 1, inf_wd_values, inf_sat_values, inf_sun_values, self._name + "_Infiltration")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._infiltration = inf_schedule

    # ***********************************************************************************************
    # cooling_set point schedule getter:
    def cooling_setpoint(self):
        return self._cooling_setpoint

    # cooling_set point schedule setter:
    def set_cooling_setpoint(
            self,
            cooling_wd_values: list = None,
            cooling_sat_values: list = None,
            cooling_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            cooling_schedule = schedule
        else:
            if cooling_wd_values is not None and cooling_sat_values is not None and cooling_sun_values is not None:
                cooling_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 2, cooling_wd_values, cooling_sat_values, cooling_sun_values,
                    self._name + "_CoolingSetPt")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._cooling_setpoint = cooling_schedule

    # ***********************************************************************************************
    # heating_set point schedule getter:
    def heating_setpoint(self):
        return self._heating_setpoint

    # heating_set point schedule setter:
    def set_heating_setpoint(
            self,
            heating_wd_values: list = None,
            heating_sat_values: list = None,
            heating_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            heating_schedule = schedule
        else:
            if heating_wd_values is not None and heating_sat_values is not None and heating_sun_values is not None:
                heating_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 2, heating_wd_values, heating_sat_values, heating_sun_values,
                    self._name + "_HeatingSetPt")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._heating_setpoint = heating_schedule

    # ***********************************************************************************************
    # humidify set point schedule getter:
    def humidify_setpoint(self):
        return self._humidify_setpoint

    # humidify set point schedule setter:
    def set_humidify_setpoint(
            self,
            humidify_wd_values: list = None,
            humidify_sat_values: list = None,
            humidify_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            humidify_schedule = schedule
        else:
            if humidify_wd_values is not None and humidify_sat_values is not None and humidify_sun_values is not None:
                humidify_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 2, humidify_wd_values, humidify_sat_values, humidify_sun_values,
                    self._name + "_HumidifySetPt")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._humidify_setpoint = humidify_schedule

    # ***********************************************************************************************
    # dehumidify_set point schedule getter:
    def dehumidify_setpoint(self):
        return self._dehumidify_setpoint

    # dehumidify set point schedule setter:
    def set_dehumidify_setpoint(
            self,
            dehumidify_wd_values: list = None,
            dehumidify_sat_values: list = None,
            dehumidify_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            dehumidify_schedule = schedule
        else:
            if dehumidify_wd_values is not None and dehumidify_sat_values is not None and dehumidify_sun_values is not None:
                dehumidify_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 2, dehumidify_wd_values, dehumidify_sat_values, dehumidify_sun_values,
                    self._name + "_DehumidifySetPt")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._dehumidify_setpoint = dehumidify_schedule

    # ***********************************************************************************************
    # hvac_availability schedule getter:
    def hvac_availability(self):
        return self._hvac_availability

    # hvac_availability schedule setter:
    def set_hvac_availability(
            self,
            avail_wd_values: list = None,
            avail_sat_values: list = None,
            avail_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            avail_schedule = schedule
        else:
            if avail_wd_values is not None and avail_sat_values is not None and avail_sun_values is not None:
                avail_schedule = ScheduleTool.custom_annual_schedule(
                    self._model, 11, avail_wd_values, avail_sat_values, avail_sun_values, self._name + "_Availability")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._hvac_availability = avail_schedule

    # ***********************************************************************************************
    # dcv schedule getter:
    def dcv(self):
        return self._dcv

    # dcv schedule setter:
    def set_dcv(
            self,
            dcv_wd_values: list = None,
            dcv_sat_values: list = None,
            dcv_sun_values: list = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            dcv = schedule
        else:
            if dcv_wd_values is not None and dcv_sat_values is not None and dcv_sun_values is not None:
                dcv = ScheduleTool.custom_annual_schedule(
                    self._model, 11, dcv_wd_values, dcv_sat_values, dcv_sun_values, self._name + "_DCV")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._dcv = dcv

    # ***********************************************************************************************
    # activity_level schedule getter:
    def activity_level(self):
        return self._activity_level

    # activity_level schedule setter:
    def set_activity_level(
            self,
            activity_value: float = None,
            schedule: openstudio.openstudiomodel.ScheduleRuleset = None):

        if schedule is not None:
            activity = schedule
        else:
            if activity_value is not None:
                activity = ScheduleTool.schedule_ruleset(self._model, 7, activity_value, self._name + "_Activity")
            else:
                raise ValueError("Weekly schedule values cannot be empty.")

        self._activity_level = activity

    # ***********************************************************************************************
    # Get Schedule Set:
    def get_schedule_sets(self):

        """
        keys: \n
        "occupancy", "lighting", "electric_equipment", "gas_equipment", "hot_water_equipment", "steam_equipment",
        "other_equipment", "infiltration", "activity", "cooling_setpoint", "heating_setpoint",
        "humidify_setpoint", "dehumidify_setpoint", "hvac_availability", "dcv"
        """

        sets = {"occupancy": self._occupancy, "lighting": self._lighting,
                "electric_equipment": self._electric_equipment, "gas_equipment": self._gas_equipment,
                "hot_water_equipment": self._hot_water_equipment, "steam_equipment": self._steam_equipment,
                "other_equipment": self._other_equipment, "infiltration": self._infiltration,
                "cooling_setpoint": self._cooling_setpoint, "heating_setpoint": self._heating_setpoint,
                "humidify_setpoint": self._humidify_setpoint, "dehumidify_setpoint": self._dehumidify_setpoint,
                "dcv": self._dcv, "activity": self._activity_level, "hvac_availability": self._hvac_availability}

        return sets
