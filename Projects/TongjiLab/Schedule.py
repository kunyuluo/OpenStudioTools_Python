import openstudio
from Schedules.Template import schedule_sets_office
from Schedules.ScheduleTools import ScheduleSets, ScheduleTool


def add_schedules(model: openstudio.openstudiomodel.Model, space_types: list):
    schedule_sets = {}

    # Define schedules set for each space type
    schedule_template = schedule_sets_office(model)

    # Office:
    # *****************************************************************************************************
    schedule_office = ScheduleSets(model)

    occupancy_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        name="Office_Occupancy")
    schedule_office.set_occupancy(schedule=occupancy_office)

    activity_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.49, 0.68, 0.74, 0.79, 0.82, 0.85, 0.87, 0.89, 0.44, 0.26,
         0.21, 0.17, 0.14, 0.12, 0.1, 0.08],
        [0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.49, 0.68, 0.74, 0.79, 0.82, 0.85, 0.87, 0.89, 0.44, 0.26,
         0.21, 0.17, 0.14, 0.12, 0.1, 0.08],
        [0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.03, 0.03, 0.49, 0.68, 0.74, 0.79, 0.82, 0.85, 0.87, 0.89, 0.44, 0.26,
         0.21, 0.17, 0.14, 0.12, 0.1, 0.08],
        name="Office_Activity")
    schedule_office.set_activity_level(123)

    lighting_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.38, 0.59, 0.67, 0.73, 0.77, 0.81, 0.84, 0.86, 0.54, 0.34,
         0.27, 0.22, 0.18, 0.15, 0.13, 0.11],
        [0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.38, 0.59, 0.67, 0.73, 0.77, 0.81, 0.84, 0.86, 0.54, 0.34,
         0.27, 0.22, 0.18, 0.15, 0.13, 0.11],
        [0.09, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.03, 0.38, 0.59, 0.67, 0.73, 0.77, 0.81, 0.84, 0.86, 0.54, 0.34,
         0.27, 0.22, 0.18, 0.15, 0.13, 0.11],
        name="Office_Lighting")
    schedule_office.set_lighting(schedule=lighting_office)

    equipment_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.77, 0.87, 0.89, 0.91, 0.93, 0.94, 0.95, 0.95, 0.2, 0.1,
         0.08, 0.07, 0.06, 0.05, 0.04, 0.04],
        [0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.77, 0.87, 0.89, 0.91, 0.93, 0.94, 0.95, 0.95, 0.2, 0.1,
         0.08, 0.07, 0.06, 0.05, 0.04, 0.04],
        [0.03, 0.03, 0.02, 0.02, 0.02, 0.01, 0.01, 0.01, 0.77, 0.87, 0.89, 0.91, 0.93, 0.94, 0.95, 0.95, 0.2, 0.1,
         0.08, 0.07, 0.06, 0.05, 0.04, 0.04],
        name="Office_Equipment")
    schedule_office.set_electric_equipment(schedule=equipment_office)

    # clg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 24, "Open_Office_CoolingSetPoint")
    clg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [26] * 24, [26] * 24, [26] * 24, name="Office_CoolingSetPoint")
    schedule_office.set_cooling_setpoint(schedule=clg_setpt_office)

    # htg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 20, "Open_Office_HeatingSetPoint")
    htg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [18] * 24, [18] * 24, [18] * 24, name="Office_HeatingSetPoint")
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
        if "Office" in space or "Lab" in space or "Mech" in space:
            schedule_sets[space] = schedule_office
        else:
            schedule_sets[space] = schedule_other

    # Output:
    # *****************************************************************************************************
    return schedule_sets
