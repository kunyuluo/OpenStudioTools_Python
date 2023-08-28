import openstudio
from Schedules.Template import schedule_sets_office
from Schedules.ScheduleTools import ScheduleSets, ScheduleTool


def add_schedules(model: openstudio.openstudiomodel.Model, space_types: list):
    schedule_sets = {}

    # Define schedules set for each space type
    schedule_template = schedule_sets_office(model)

    # Open Office:
    # *****************************************************************************************************
    schedule_office = ScheduleSets(model)

    schedule_office.set_occupancy(schedule=schedule_template["occupancy"])
    schedule_office.set_activity_level(schedule=schedule_template["activity"])
    schedule_office.set_lighting(schedule=schedule_template["lighting"])
    schedule_office.set_electric_equipment(schedule=schedule_template["electric_equipment"])

    # clg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 24, "Open_Office_CoolingSetPoint")
    clg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [26] * 24, [26] * 24, [26] * 24, [26] * 24, [26] * 24, name="Open_Office_CoolingSetPoint")
    schedule_office.set_cooling_setpoint(schedule=clg_setpt_office)

    # htg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 20, "Open_Office_HeatingSetPoint")
    htg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [20] * 24, [20] * 24, [20] * 24, [20] * 24, [20] * 24, name="Open_Office_HeatingSetPoint")
    schedule_office.set_heating_setpoint(schedule=htg_setpt_office)

    schedule_office.set_infiltration(schedule=schedule_template["infiltration"])

    # Others:
    # *****************************************************************************************************
    schedule_other = ScheduleSets(model)
    schedule_other.set_occupancy(schedule=schedule_template["occupancy"])
    schedule_other.set_activity_level(schedule=schedule_template["activity"])
    schedule_other.set_lighting(schedule=schedule_template["lighting"])
    schedule_other.set_electric_equipment(schedule=schedule_template["electric_equipment"])
    schedule_other.set_infiltration(schedule=schedule_template["infiltration"])
    schedule_other.set_cooling_setpoint(schedule=schedule_template["cooling_setpoint"])
    schedule_other.set_heating_setpoint(schedule=schedule_template["heating_setpoint"])

    # Assignment:
    # *****************************************************************************************************
    for space in space_types:
        if "Office" in space:
            schedule_sets[space] = schedule_office
        else:
            schedule_sets[space] = schedule_other

    # Output:
    # *****************************************************************************************************
    return schedule_sets
