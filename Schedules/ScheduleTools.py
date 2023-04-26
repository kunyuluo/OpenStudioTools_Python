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
            saturday_value,
            sunday_value,
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

        schedule = ScheduleTool.schedule_ruleset(model, type_limits=type_limit, name=name)

        schedule_wd = ScheduleTool.schedule_day(model, weekday_value, type_limits=type_limit,
                                                name=name + "_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(model, saturday_value, type_limits=type_limit,
                                                 name=name + "_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(model, sunday_value, type_limits=type_limit,
                                                 name=name + "_Schedule_Sunday")

        ScheduleTool.schedule_rule(schedule, schedule_wd,
                                   days=[True, True, True, True, True, False, False], name=name + "_Weekdays")
        ScheduleTool.schedule_rule(schedule, schedule_sat,
                                   days=[False, False, False, False, False, True, False], name=name + "_Saturday")
        ScheduleTool.schedule_rule(schedule, schedule_sun,
                                   days=[False, False, False, False, False, False, True], name=name + "_Sunday")

        return schedule

    # Schedule Ruleset
    @staticmethod
    def schedule_ruleset(model, value=-9999, type_limits=None, name=None):
        if value != -9999:
            schedule_ruleset = openstudio.openstudiomodel.ScheduleRuleset(model, value)
        else:
            schedule_ruleset = openstudio.openstudiomodel.ScheduleRuleset(model)

        if type_limits is not None:
            schedule_ruleset.setScheduleTypeLimits(type_limits)
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
        type_limit = ScheduleTool.schedule_type_limits(model, 11, 2, 0, 1, "always on limits")
        schedule = ScheduleTool.schedule_ruleset(model, 1, type_limits=type_limit, name="AlwaysOn")

        return schedule

    @staticmethod
    def always_off(model):
        type_limit = ScheduleTool.schedule_type_limits(model, 11, 2, 0, 1, "always off limits")
        schedule = ScheduleTool.schedule_ruleset(model, 0, type_limits=type_limit, name="AlwaysOff")

        return schedule

    @staticmethod
    def dhw_flow_fraction_schedule(model):
        type_limit = ScheduleTool.schedule_type_limits(model, 1, 1, 0, 1)

        schedule = ScheduleTool.schedule_ruleset(
            model, 0, type_limits=type_limit, name="ESTAR MFHR DHW Fraction Schedule")

        fraction_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.3, 0.5, 0.4, 0.4, 0.3, 0.35, 0.4, 0.4, 0.35, 0.35, 0.3,
                           0.3, 0.5, 0.4, 0.35, 0.45, 0.3, 0.05]
        schedule_day = ScheduleTool.schedule_day(model, fraction_values, type_limits=type_limit,
                                                 name="ESTAR MFHR DHW Fraction Schedule Day")

        occ_wd_schrule = ScheduleTool.schedule_rule(schedule, schedule_day, all_week=True)

        return schedule
