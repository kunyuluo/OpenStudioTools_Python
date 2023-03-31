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
    def schedule_day(model, values=None, constant=-9999, type_limits=None, name=None):
        schedule = openstudio.openstudiomodel.ScheduleDay(model)

        if constant != -9999:
            schedule.addValue(openstudio.Time(0, 24, 0), constant)
        else:
            if values is not None:
                if len(values) == 0:
                    schedule.addValue(openstudio.Time(0, 24, 0), 0.0)
                elif len(values) != 24:
                    schedule.addValue(openstudio.Time(0, 8, 0), 0.0)
                    schedule.addValue(openstudio.Time(0, 18, 0), 1.0)
                    schedule.addValue(openstudio.Time(0, 24, 0), 0.0)
                else:
                    for i in range(len(values)):
                        schedule.addValue(openstudio.Time(0, i + 1, 0), values[i])

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

        fraction_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5,
                           0.5, 0.7, 0.7, 0.8, 0.9, 0.9]
        schedule_day = ScheduleTool.schedule_day(model, fraction_values, type_limits=type_limit,
                                                 name="ESTAR MFHR DHW Fraction Schedule Day")

        occ_wd_schrule = ScheduleTool.schedule_rule(schedule, schedule_day, all_week=True)

        return schedule
