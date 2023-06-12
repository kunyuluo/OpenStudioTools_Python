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

    # clg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 24, "Open_Office_CoolingSetPoint")
    clg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [24] * 24, [24] * 24, [24] * 24, [24] * 24, [24] * 24, name="Open_Office_CoolingSetPoint")
    schedule_office.set_cooling_setpoint(schedule=clg_setpt_office)

    # htg_setpt_office = ScheduleTool.schedule_ruleset(model, 2, 20, "Open_Office_HeatingSetPoint")
    htg_setpt_office = ScheduleTool.custom_annual_schedule(
        model, 2, [20] * 24, [20] * 24, [20] * 24, [20] * 24, [20] * 24, name="Open_Office_HeatingSetPoint")
    schedule_office.set_heating_setpoint(schedule=htg_setpt_office)

    schedule_office.set_infiltration(schedule=schedule_template["infiltration"])

    # Cafeteria:
    # *****************************************************************************************************
    schedule_cafe = ScheduleSets(model)
    occupancy_cafe = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.36, 0.36, 0.35, 0.34, 0.34, 0.38, 0.43, 0.5, 0.63, 0.89, 1.0, 0.97, 0.9, 0.88, 0.96, 0.95, 1.0, 0.94, 0.84,
         0.77, 0.71, 0.67, 0.64, 0.52],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        name="Cafeteria_Occupancy")
    schedule_cafe.set_occupancy(schedule=occupancy_cafe)
    schedule_cafe.set_activity_level(schedule=schedule_template["activity"])

    lighting_cafe = ScheduleTool.custom_annual_schedule(
        model, 1,
        [0.36, 0.36, 0.35, 0.34, 0.34, 0.38, 0.43, 0.5, 0.63, 0.89, 1.0, 0.97, 0.9, 0.88, 0.96, 0.95, 1.0, 0.94, 0.84,
         0.77, 0.71, 0.67, 0.64, 0.52],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        [0.34, 0.33, 0.33, 0.32, 0.31, 0.31, 0.32, 0.34, 0.35, 0.37, 0.4, 0.42, 0.44, 0.45, 0.45, 0.46, 0.46, 0.46,
         0.46, 0.46, 0.41, 0.41, 0.4, 0.35],
        name="Cafeteria_Lighting")
    schedule_cafe.set_lighting(schedule=lighting_cafe)
    schedule_cafe.set_electric_equipment(schedule=lighting_cafe)

    # clg_setpt_cafe = ScheduleTool.schedule_ruleset(model, 2, 26, "Cafeteria_CoolingSetPoint")
    clg_setpt_cafe = ScheduleTool.custom_annual_schedule(
        model, 2, [26] * 24, [26] * 24, [26] * 24, [26] * 24, [26] * 24, name="Cafeteria_CoolingSetPoint")
    schedule_cafe.set_cooling_setpoint(schedule=clg_setpt_cafe)

    # htg_setpt_cafe = ScheduleTool.schedule_ruleset(model, 2, 18, "Cafeteria_HeatingSetPoint")
    htg_setpt_cafe = ScheduleTool.custom_annual_schedule(
        model, 2, [18] * 24, [18] * 24, [18] * 24, [18] * 24, [18] * 24, name="Cafeteria_HeatingSetPoint")
    schedule_cafe.set_heating_setpoint(schedule=htg_setpt_cafe)

    schedule_cafe.set_infiltration(schedule=schedule_template["infiltration"])

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
        name="Corridor_Occupancy")
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
        name="Corridor_Lighting")
    schedule_corridor.set_lighting(schedule=lighting_corridor)
    schedule_corridor.set_electric_equipment(schedule=lighting_corridor)

    # clg_setpt_corridor = ScheduleTool.schedule_ruleset(model, 2, 26, "Corridor_CoolingSetPoint")
    clg_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 2, [26] * 24, [26] * 24, [26] * 24, [26] * 24, [26] * 24, name="Corridor_CoolingSetPoint")
    schedule_corridor.set_cooling_setpoint(schedule=clg_setpt_corridor)

    # htg_setpt_corridor = ScheduleTool.schedule_ruleset(model, 2, 19, "Corridor_HeatingSetPoint")
    htg_setpt_corridor = ScheduleTool.custom_annual_schedule(
        model, 2, [19] * 24, [19] * 24, [19] * 24, [19] * 24, [19] * 24, name="Corridor_HeatingSetPoint")
    schedule_corridor.set_heating_setpoint(schedule=htg_setpt_corridor)

    schedule_corridor.set_infiltration(schedule=schedule_template["infiltration"])

    # Others:
    # *****************************************************************************************************
    schedule_conference = ScheduleSets(model)
    schedule_conference.set_occupancy(schedule=schedule_template["occupancy"])
    schedule_conference.set_activity_level(schedule=schedule_template["activity"])
    schedule_conference.set_lighting(schedule=schedule_template["lighting"])
    schedule_conference.set_electric_equipment(schedule=schedule_template["electric_equipment"])
    schedule_conference.set_infiltration(schedule=schedule_template["infiltration"])
    schedule_conference.set_cooling_setpoint(schedule=schedule_template["cooling_setpoint"])
    schedule_conference.set_heating_setpoint(schedule=schedule_template["heating_setpoint"])

    # Assignment:
    # *****************************************************************************************************
    for space in space_types:
        if "Office" in space:
            schedule_sets[space] = schedule_office
        elif "Corridor" in space:
            schedule_sets[space] = schedule_corridor
        elif "Conference" in space:
            schedule_sets[space] = schedule_conference
        elif "Cafeteria" in space:
            schedule_sets[space] = schedule_cafe
        else:
            schedule_sets[space] = schedule_conference

    # Output:
    # *****************************************************************************************************
    return schedule_sets
