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
    occupancy_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.36, 0.36, 0.35, 0.34, 0.34, 0.38, 0.43, 0.5, 0.63, 0.89, 1.0, 0.97, 0.9, 0.88, 0.96, 0.95, 1.0, 0.94, 0.84,
         0.77, 0.71, 0.67, 0.64, 0.52],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        name="Open_Office_Occupancy")
    schedule_office.set_occupancy(schedule=occupancy_office)
    schedule_office.set_activity_level(schedule=schedule_template["activity"])

    lighting_office = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.36, 0.36, 0.35, 0.34, 0.34, 0.38, 0.43, 0.5, 0.63, 0.89, 1.0, 0.97, 0.9, 0.88, 0.96, 0.95, 1.0, 0.94, 0.84,
         0.77, 0.71, 0.67, 0.64, 0.52],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        name="Open_Office_Lighting")
    schedule_office.set_lighting(schedule=lighting_office)
    schedule_office.set_electric_equipment(schedule=lighting_office)

    clg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [24] * 24, [24] * 24, [24] * 24, name="Open_Office_CoolingSetPoint")
    schedule_office.set_cooling_setpoint(schedule=clg_setpt_office)

    htg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [20] * 24, [20] * 24, [20] * 24, name="Open_Office_HeatingSetPoint")
    schedule_office.set_heating_setpoint(schedule=htg_setpt_office)

    hum_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 12, [30] * 24, [30] * 24, [30] * 24, name="Open_Office_HumidifySetPoint")
    schedule_office.set_humidify_setpoint(schedule=hum_setpt_office)

    dehum_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 12, [50] * 24, [50] * 24, [50] * 24, name="Open_Office_DehumidifySetPoint")
    schedule_office.set_dehumidify_setpoint(schedule=dehum_setpt_office)

    schedule_office.set_infiltration(schedule=schedule_template["infiltration"])

    # Corridor:
    # *****************************************************************************************************
    schedule_corridor = ScheduleSets(model)
    occupancy_corridor = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.45, 0.46, 0.45, 0.43, 0.37, 0.36, 0.46, 0.59, 0.75, 1.0, 0.75, 0.62, 0.63, 0.66, 0.64, 0.63, 0.61, 0.56,
         0.55, 0.51, 0.5, 0.49, 0.48, 0.48],
        [0.41, 0.4, 0.38, 0.35, 0.34, 0.34, 0.39, 0.47, 0.44, 0.46, 0.49, 0.48, 0.46, 0.47, 0.47, 0.47, 0.46, 0.45,
         0.45, 0.46, 0.44, 0.44, 0.44, 0.41],
        [0.41, 0.4, 0.38, 0.35, 0.34, 0.34, 0.39, 0.47, 0.44, 0.46, 0.49, 0.48, 0.46, 0.47, 0.47, 0.47, 0.46, 0.45,
         0.45, 0.46, 0.44, 0.44, 0.44, 0.41],
        name="Conference_Occupancy")
    schedule_corridor.set_occupancy(schedule=occupancy_corridor)
    schedule_corridor.set_activity_level(schedule=schedule_template["activity"])

    lighting_corridor = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.45, 0.46, 0.45, 0.43, 0.37, 0.36, 0.46, 0.59, 0.75, 1.0, 0.75, 0.62, 0.63, 0.66, 0.64, 0.63, 0.61, 0.56,
         0.55, 0.51, 0.5, 0.49, 0.48, 0.48],
        [0.41, 0.4, 0.38, 0.35, 0.34, 0.34, 0.39, 0.47, 0.44, 0.46, 0.49, 0.48, 0.46, 0.47, 0.47, 0.47, 0.46, 0.45,
         0.45, 0.46, 0.44, 0.44, 0.44, 0.41],
        [0.41, 0.4, 0.38, 0.35, 0.34, 0.34, 0.39, 0.47, 0.44, 0.46, 0.49, 0.48, 0.46, 0.47, 0.47, 0.47, 0.46, 0.45,
         0.45, 0.46, 0.44, 0.44, 0.44, 0.41],
        name="Conference_Lighting")
    schedule_corridor.set_lighting(schedule=lighting_corridor)
    schedule_corridor.set_electric_equipment(schedule=lighting_corridor)

    clg_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 2, [26] * 24, [26] * 24, [26] * 24, name="Conference_CoolingSetPoint")
    schedule_corridor.set_cooling_setpoint(schedule=clg_setpt_corridor)

    htg_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 2, [19] * 24, [19] * 24, [19] * 24, name="Conference_HeatingSetPoint")
    schedule_corridor.set_heating_setpoint(schedule=htg_setpt_corridor)

    hum_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 12, [30] * 24, [30] * 24, [30] * 24, name="Conference_HumidifySetPoint")
    schedule_corridor.set_humidify_setpoint(schedule=hum_setpt_corridor)

    dehum_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 12, [50] * 24, [50] * 24, [50] * 24, name="Conference_DehumidifySetPoint")
    schedule_corridor.set_dehumidify_setpoint(schedule=dehum_setpt_corridor)

    schedule_corridor.set_infiltration(schedule=schedule_template["infiltration"])

    # Assignment:
    # *****************************************************************************************************
    for space in space_types:
        if "Office" in space:
            schedule_sets[space] = schedule_office
        else:
            schedule_sets[space] = schedule_corridor

    # Output:
    # *****************************************************************************************************
    return schedule_sets
