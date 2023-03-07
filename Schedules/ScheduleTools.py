# import openstudio as os
import openstudio.openstudiomodel as osModel
import openstudio.openstudioutilitiestime


class ScheduleTool:

    year = 2023

    # Schedule Type Limits
    @staticmethod
    def scheduleTypeLimits(model, unit_type, lower_limit=-9999, upper_limit=-9999, numeric_type=None, name=None):
        type_limits = osModel.ScheduleTypeLimits(model)
        type_limits.setUnitType(unit_type)
        if name is not None: type_limits.setName(name)
        if lower_limit != -9999: type_limits.setLowerLimitValue(lower_limit)
        if upper_limit != -9999: type_limits.setUpperLimitValue(upper_limit)
        if numeric_type is not None: type_limits.setNumericType(numeric_type)

        return type_limits

    # Day Schedule
    @staticmethod
    def scheduleDay(model, values=None, constant=-9999, type_limits=None, name=None):
        schedule = osModel.ScheduleDay(model)

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
                        schedule.addValue(openstudio.Time(0, i+1, 0), values[i])

        if type_limits is not None: schedule.setScheduleTypeLimits(type_limits)
        if name is not None: schedule.setName(name)

        return schedule

    # Schedule Rule
    @staticmethod
    def scheduleRule(
            schedule_ruleset,
            schedule_day,
            start_m=1,
            start_d=1,
            end_m=12,
            end_d=31,
            all_week=False,
            days=None,
            name=None):
        schedule_rule = osModel.ScheduleRule(schedule_ruleset, schedule_day)

        if name is not None: schedule_rule.setName(name)

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
    def scheduleRuleset(model, value=-9999, type_limits=None, name=None):
        if value != -9999:
            schedule_ruleset = osModel.ScheduleRuleset(model, value)
        else:
            schedule_ruleset = osModel.ScheduleRuleset(model)

        if type_limits is not None: schedule_ruleset.setScheduleTypeLimits(type_limits)
        if name is not None: schedule_ruleset.setName(name)

        return schedule_ruleset
