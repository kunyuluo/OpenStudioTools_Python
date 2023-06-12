import openstudio
from Schedules.ScheduleTools import ScheduleTool


def schedule_sets_office(model: openstudio.openstudiomodel.Model):

    """
    keys: \n
    "occupancy", "lighting", "electric_equipment", "gas_equipment", "hot_water_equipment", "steam_equipment",
    "other_equipment", "infiltration", "activity", "cooling_setpoint", "heating_setpoint", "hvac_availability", "dcv"
    """

    prefix = "Office"
    sets = {"occupancy": None, "lighting": None, "electric_equipment": None, "gas_equipment": None,
            "hot_water_equipment": None, "steam_equipment": None, "other_equipment": None,
            "infiltration": None, "activity": None, "cooling_setpoint": None, "heating_setpoint": None,
            "hvac_availability": None, "dcv": None}

    # Occupancy Schedule
    # *******************************************************************************************
    occ_wd_values = [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95,
                     0.95, 0.55, 0.1, 0.05, 0.05]
    occ_sat_values = [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0,
                      0, 0]
    occ_sun_values = [0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0,
                      0, 0, 0, 0, 0]
    occ_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, occ_wd_values, occ_sat_values, occ_sun_values, name=prefix + "_Occ_Schedule")

    sets["occupancy"] = occ_schedule

    # Lighting Schedule
    # *******************************************************************************************
    ltg_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65,
                     0.65, 0.35, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
    ltg_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15,
                      0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    ltg_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                      0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    ltg_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, ltg_wd_values, ltg_sat_values, ltg_sun_values, name=prefix + "_Ltg_Schedule")

    sets["lighting"] = ltg_schedule

    # Electric Equipment Schedule
    # *******************************************************************************************
    equip_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
                       0.5, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
    equip_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15,
                        0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    equip_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                        0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
    equip_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, equip_wd_values, equip_sat_values, equip_sun_values, name=prefix + "_Equip_Schedule")

    sets["electric_equipment"] = equip_schedule

    # Infiltration Schedule
    # *******************************************************************************************
    inf_wd_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                     0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    inf_sat_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                      0.25, 1, 1, 1, 1, 1]
    inf_sun_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                      1, 1, 1, 1, 1, 1]
    inf_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, inf_wd_values, inf_sat_values, inf_sun_values, name=prefix + "_Infiltration_Schedule")

    sets["infiltration"] = inf_schedule

    # Cooling set point schedule:
    # *******************************************************************************************
    clg_wd_values = [29.4, 29.4, 29.4, 29.4, 29.4, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9,
                     23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9]
    clg_sat_values = [29.4, 29.4, 29.4, 29.4, 29.4, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9,
                      23.9, 23.9, 23.9, 23.9, 23.9, 29.4, 29.4, 29.4, 29.4]
    clg_sun_values = [29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4,
                      29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4]
    clg_schedule = ScheduleTool.custom_annual_schedule(
        model, 2, clg_wd_values, clg_sat_values, clg_sun_values, clg_wd_values, clg_wd_values, prefix + "_CoolingSetPt")

    sets["cooling_setpoint"] = clg_schedule

    # Heating_set point schedule:
    # *******************************************************************************************
    htg_wd_values = [15.6, 15.6, 15.6, 15.6, 15.6, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1,
                     21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1]
    htg_sat_values = [15.6, 15.6, 15.6, 15.6, 15.6, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1,
                      21.1, 21.1, 21.1, 21.1, 15.6, 15.6, 15.6, 15.6, 15.6]
    htg_sun_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6,
                      15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6]
    htg_schedule = ScheduleTool.custom_annual_schedule(
        model, 2, htg_wd_values, htg_sat_values, htg_sun_values, htg_wd_values, htg_wd_values, prefix + "_HeatingSetPt")

    sets["heating_setpoint"] = htg_schedule

    # Activity schedule:
    # *******************************************************************************************
    activity = ScheduleTool.schedule_ruleset(model, 7, 200, prefix + "_Activity")

    sets["activity"] = activity

    # HVAC Availability schedule:
    # *******************************************************************************************
    avail_wd_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    avail_sat_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
    avail_sun_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]

    avail_schedule = ScheduleTool.custom_annual_schedule(
        model, 11, avail_wd_values, avail_sat_values, avail_sun_values, name=prefix + "_Availability")

    sets["hvac_availability"] = avail_schedule

    # DCV Schedule
    # *******************************************************************************************
    dcv_wd_values = [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95,
                     0.95, 0.55, 0.1, 0.05, 0.05]
    dcv_sat_values = [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0,
                      0, 0]
    dcv_sun_values = [0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0,
                      0, 0, 0, 0, 0]
    dcv_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, dcv_wd_values, dcv_sat_values, dcv_sun_values, name=prefix + "_DCV_Schedule")

    sets["dcv"] = dcv_schedule

    # Output:
    # *******************************************************************************************
    return sets


def schedule_sets_residential(model: openstudio.openstudiomodel.Model):

    prefix = "Residential"
    sets = {"occupancy": None, "number_of_people": None, "lighting": None, "electric_equipment": None,
            "gas_equipment": None, "hot_water_equipment": None, "steam_equipment": None, "other_equipment": None,
            "infiltration": None, "activity": None, "cooling_setpoint": None, "heating_setpoint": None,
            "hvac_availability": None, "dcv": None}

    # Occupancy Schedule
    # *******************************************************************************************
    occ_wd_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                     0.7, 0.7, 0.8, 0.9, 0.9]
    occ_sat_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                      0.7, 0.7, 0.8, 0.9, 0.9]
    occ_sun_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                      0.7, 0.7, 0.8, 0.9, 0.9]
    occ_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, occ_wd_values, occ_sat_values, occ_sun_values, name=prefix + "_Occ_Schedule")

    sets["occupancy"] = occ_schedule

    # Lighting Schedule
    # *******************************************************************************************
    ltg_wd_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                     0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    ltg_sat_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                      0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    ltg_sun_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                      0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    ltg_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, ltg_wd_values, ltg_sat_values, ltg_sun_values, name=prefix + "_Ltg_Schedule")

    sets["lighting"] = ltg_schedule

    # Electric Equipment Schedule
    # *******************************************************************************************
    equip_wd_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                       0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    equip_sat_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                        0.3, 0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    equip_sun_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                        0.3, 0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
    equip_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, equip_wd_values, equip_sat_values, equip_sun_values, name=prefix + "_Equip_Schedule")

    sets["electric_equipment"] = equip_schedule

    # Infiltration Schedule
    # *******************************************************************************************
    inf_wd_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                     0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    inf_sat_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                      0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    inf_sun_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                      0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
    inf_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, inf_wd_values, inf_sat_values, inf_sun_values, name=prefix + "_Infiltration_Schedule")

    sets["infiltration"] = inf_schedule

    # Cooling set point schedule:
    # *******************************************************************************************
    clg_wd_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                     25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
    clg_sat_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                      25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
    clg_sun_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                      25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
    clg_schedule = ScheduleTool.custom_annual_schedule(
        model, 2, clg_wd_values, clg_sat_values, clg_sun_values, clg_wd_values, clg_wd_values, prefix + "_CoolingSetPt")

    sets["cooling_setpoint"] = clg_schedule

    # Heating_set point schedule:
    # *******************************************************************************************
    htg_wd_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                     20, 20, 15.6, 15.6]
    htg_sat_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                      20, 20, 15.6, 15.6]
    htg_sun_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                      20, 20, 15.6, 15.6]
    htg_schedule = ScheduleTool.custom_annual_schedule(
        model, 2, htg_wd_values, htg_sat_values, htg_sun_values, htg_wd_values, htg_wd_values, prefix + "_HeatingSetPt")

    sets["heating_setpoint"] = htg_schedule

    # Activity schedule:
    # *******************************************************************************************
    activity = ScheduleTool.schedule_ruleset(model, 7, 120, prefix + "_Activity")

    sets["activity"] = activity

    # HVAC Availability schedule:
    # *******************************************************************************************
    avail_wd_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    avail_sat_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    avail_sun_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]

    avail_schedule = ScheduleTool.custom_annual_schedule(
        model, 11, avail_wd_values, avail_sat_values, avail_sun_values, name=prefix + "_Availability")

    sets["hvac_availability"] = avail_schedule

    # DCV Schedule
    # *******************************************************************************************
    dcv_wd_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                     0.7, 0.7, 0.8, 0.9, 0.9]
    dcv_sat_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                      0.7, 0.7, 0.8, 0.9, 0.9]
    dcv_sun_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                      0.7, 0.7, 0.8, 0.9, 0.9]
    dcv_schedule = ScheduleTool.custom_annual_schedule(
        model, 1, dcv_wd_values, dcv_sat_values, dcv_sun_values, name=prefix + "_DCV_Schedule")

    sets["dcv"] = dcv_schedule

    # Output:
    # *******************************************************************************************
    return sets
