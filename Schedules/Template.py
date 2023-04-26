import openstudio
from Schedules.ScheduleTools import ScheduleTool


# class OfficeSets:
#     @staticmethod
#     def occupancySchedule():

class Office:
    # Data Source: Title 24 Appendix 5.4B
    _occupancy = None
    _lighting = None
    _equipment = None
    _infiltration = None
    _cooling_setpoint = None
    _heating_setpoint = None
    _hvac_availability = None
    _dcv = None
    _activity_level = None

    prefix = "Office_"

    def __init__(self, model: openstudio.openstudiomodel.Model):
        self._model = model

    # Occupancy Schedule
    def occupancy(self):
        occ_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        occ_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=occ_typelimits,
                                                     name=self.prefix + "Occ_Schedule")

        occ_wd_values = [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95,
                         0.95, 0.55, 0.1, 0.05, 0.05]
        occ_sat_values = [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0,
                          0, 0]
        occ_sun_values = [0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0,
                          0, 0, 0, 0, 0]
        schedule_wd = ScheduleTool.schedule_day(self._model, occ_wd_values, type_limits=occ_typelimits,
                                                name=self.prefix + "Occ_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, occ_sat_values, type_limits=occ_typelimits,
                                                 name=self.prefix + "Occ_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, occ_sun_values, type_limits=occ_typelimits,
                                                 name=self.prefix + "Occ_Schedule_Sunday")

        occ_wd_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "Occ_Weekdays")
        occ_sat_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "Occ_Saturday")
        occ_sun_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "Occ_Sunday")

        self._occupancy = occ_schedule
        return self._occupancy

    # Lighting Schedule
    def lighting(self):
        ltg_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        ltg_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=ltg_typelimits,
                                                     name=self.prefix + "Ltg_Schedule")

        ltg_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65,
                         0.65, 0.35, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
        ltg_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15,
                          0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        ltg_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                          0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        schedule_wd = ScheduleTool.schedule_day(self._model, ltg_wd_values, type_limits=ltg_typelimits,
                                                name=self.prefix + "Ltg_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, ltg_sat_values, type_limits=ltg_typelimits,
                                                 name=self.prefix + "Ltg_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, ltg_sun_values, type_limits=ltg_typelimits,
                                                 name=self.prefix + "Ltg_Schedule_Sunday")

        ltg_wd_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "Ltg_Weekdays")
        ltg_sat_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "Ltg_Saturday")
        ltg_sun_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "Ltg_Sunday")

        self._lighting = ltg_schedule
        return self._lighting

    # Equipment Schedule
    def equipment(self):
        equip_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        equip_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=equip_typelimits,
                                                       name=self.prefix + "Equip_Schedule")
        equip_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9,
                           0.5, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
        equip_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15,
                            0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        equip_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05,
                            0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        schedule_wd = ScheduleTool.schedule_day(self._model, equip_wd_values, type_limits=equip_typelimits,
                                                name=self.prefix + "Equip_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, equip_sat_values, type_limits=equip_typelimits,
                                                 name=self.prefix + "Equip_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, equip_sun_values, type_limits=equip_typelimits,
                                                 name=self.prefix + "Equip_Schedule_Sunday")

        equip_wd_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_wd,
                                                      days=[True, True, True, True, True, False, False],
                                                      name=self.prefix + "Equip_Weekdays")
        equip_sat_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_sat,
                                                       days=[False, False, False, False, False, True, False],
                                                       name=self.prefix + "Equip_Saturday")
        equip_sun_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_sun,
                                                       days=[False, False, False, False, False, False, True],
                                                       name=self.prefix + "Equip_Sunday")

        self._equipment = equip_schedule
        return self._equipment

    def infiltration(self):
        infil_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        infil_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=infil_typelimits,
                                                       name=self.prefix + "Infil_Schedule")
        infil_wd_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                           0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        infil_sat_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                            0.25, 1, 1, 1, 1, 1]
        infil_sun_values = [1, 1, 1, 1, 1, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                            1, 1, 1, 1, 1, 1]
        schedule_wd = ScheduleTool.schedule_day(self._model, infil_wd_values, type_limits=infil_typelimits,
                                                name=self.prefix + "Infil_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, infil_sat_values, type_limits=infil_typelimits,
                                                 name=self.prefix + "Infil_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, infil_sun_values, type_limits=infil_typelimits,
                                                 name=self.prefix + "Infil_Schedule_Sunday")

        infil_wd_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_wd,
                                                      days=[True, True, True, True, True, False, False],
                                                      name=self.prefix + "Infil_Weekdays")
        infil_sat_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_sat,
                                                       days=[False, False, False, False, False, True, False],
                                                       name=self.prefix + "Infil_Saturday")
        infil_sun_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_sun,
                                                       days=[False, False, False, False, False, False, True],
                                                       name=self.prefix + "Infil_Sunday")

        self._infiltration = infil_schedule
        return self._infiltration

    def cooling_setpoint(self):
        temp_typelimits = ScheduleTool.schedule_type_limits(self._model, 2, 1, 0, 50)
        temp_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=temp_typelimits,
                                                      name=self.prefix + "ClgSP_Schedule")
        temp_wd_values = [29.4, 29.4, 29.4, 29.4, 29.4, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9,
                          23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9]
        temp_sat_values = [29.4, 29.4, 29.4, 29.4, 29.4, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9, 23.9,
                           23.9, 23.9, 23.9, 23.9, 23.9, 29.4, 29.4, 29.4, 29.4]
        temp_sun_values = [29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4,
                           29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4, 29.4]
        schedule_wd = ScheduleTool.schedule_day(self._model, temp_wd_values, type_limits=temp_typelimits,
                                                name=self.prefix + "ClgSP_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, temp_sat_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "ClgSP_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, temp_sun_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "ClgSP_Schedule_Saturday")

        temp_wd_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "ClgSP_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "ClgSP_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "ClgSP_Saturday")
        temp_schedule.setSummerDesignDaySchedule(schedule_wd)
        temp_schedule.setWinterDesignDaySchedule(schedule_wd)

        self._cooling_setpoint = temp_schedule
        return self._cooling_setpoint

    def heating_setpoint(self):
        temp_typelimits = ScheduleTool.schedule_type_limits(self._model, 2, 1, 0, 50)
        temp_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=temp_typelimits,
                                                      name=self.prefix + "HtgSP_Schedule")
        temp_wd_values = [15.6, 15.6, 15.6, 15.6, 15.6, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1,
                          21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1]
        temp_sat_values = [15.6, 15.6, 15.6, 15.6, 15.6, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1, 21.1,
                           21.1, 21.1, 21.1, 21.1, 15.6, 15.6, 15.6, 15.6, 15.6]
        temp_sun_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6,
                           15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 15.6]
        schedule_wd = ScheduleTool.schedule_day(self._model, temp_wd_values, type_limits=temp_typelimits,
                                                name=self.prefix + "HtgSP_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, temp_sat_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "HtgSP_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, temp_sun_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "HtgSP_Schedule_Sunday")

        temp_wd_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "HtgSP_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "HtgSP_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "HtgSP_Sunday")
        temp_schedule.setSummerDesignDaySchedule(schedule_wd)
        temp_schedule.setWinterDesignDaySchedule(schedule_wd)

        self._heating_setpoint = temp_schedule
        return self._heating_setpoint

    def hvac_availability(self):
        avail_typelimits = ScheduleTool.schedule_type_limits(self._model, 11, 2)
        avail_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=avail_typelimits,
                                                       name=self.prefix + "Avail_Schedule")
        avail_wd_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        avail_sat_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0]
        avail_sun_values = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        schedule_wd = ScheduleTool.schedule_day(self._model, avail_wd_values, type_limits=avail_typelimits,
                                                name=self.prefix + "Avail_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, avail_sat_values, type_limits=avail_typelimits,
                                                 name=self.prefix + "Avail_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, avail_sun_values, type_limits=avail_typelimits,
                                                 name=self.prefix + "Avail_Schedule_Sunday")

        temp_wd_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "Avail_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "Avail_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "Avail_Sunday")

        self._hvac_availability = avail_schedule
        return self._hvac_availability

    def dcv(self):
        dcv_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        dcv_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=dcv_typelimits,
                                                     name=self.prefix + "DCV_Schedule")

        dcv_wd_values = [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95,
                         0.95, 0.55, 0.1, 0.05, 0.05]
        dcv_sat_values = [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0,
                          0, 0]
        dcv_sun_values = [0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0,
                          0, 0, 0, 0, 0]
        schedule_wd = ScheduleTool.schedule_day(self._model, dcv_wd_values, type_limits=dcv_typelimits,
                                                name=self.prefix + "DCV_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, dcv_sat_values, type_limits=dcv_typelimits,
                                                 name=self.prefix + "DCV_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, dcv_sun_values, type_limits=dcv_typelimits,
                                                 name=self.prefix + "DCV_Schedule_Sunday")

        occ_wd_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "DCV_Weekdays")
        occ_sat_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "DCV_Saturday")
        occ_sun_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "DCV_Sunday")

        self._dcv = dcv_schedule
        return self._dcv

    def activity_level(self):
        act_typelimits = ScheduleTool.schedule_type_limits(self._model, 7, 1, 0, 200)
        act_schedule = ScheduleTool.schedule_ruleset(
            self._model,
            120,
            type_limits=act_typelimits,
            name=self.prefix + "Activity_Schedule")

        self._activity_level = act_schedule
        return self._activity_level


class Residential:
    # Data Source: Title 24 Appendix 5.4B
    _occupancy = None
    _lighting = None
    _equipment = None
    _infiltration = None
    _cooling_setpoint = None
    _heating_setpoint = None
    _hvac_availability = None
    _dcv = None
    _activity_level = None

    prefix = "Residential_"

    def __init__(self, model: openstudio.openstudiomodel.Model):
        self._model = model

    # Occupancy Schedule
    def occupancy(self):
        occ_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        occ_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=occ_typelimits,
                                                     name=self.prefix + "Occ_Schedule")

        occ_wd_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                         0.7, 0.7, 0.8, 0.9, 0.9]
        occ_sat_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                          0.7, 0.7, 0.8, 0.9, 0.9]
        occ_sun_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                          0.7, 0.7, 0.8, 0.9, 0.9]
        schedule_wd = ScheduleTool.schedule_day(self._model, occ_wd_values, type_limits=occ_typelimits,
                                                name=self.prefix + "Occ_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, occ_sat_values, type_limits=occ_typelimits,
                                                 name=self.prefix + "Occ_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, occ_sun_values, type_limits=occ_typelimits,
                                                 name=self.prefix + "Occ_Schedule_Sunday")

        occ_wd_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "Occ_Weekdays")
        occ_sat_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "Occ_Saturday")
        occ_sun_schrule = ScheduleTool.schedule_rule(occ_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "Occ_Sunday")

        self._occupancy = occ_schedule
        return self._occupancy

    # Lighting Schedule
    def lighting(self):
        ltg_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        ltg_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=ltg_typelimits,
                                                     name=self.prefix + "Ltg_Schedule")

        ltg_wd_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                         0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        ltg_sat_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                          0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        ltg_sun_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                          0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        schedule_wd = ScheduleTool.schedule_day(self._model, ltg_wd_values, type_limits=ltg_typelimits,
                                                name=self.prefix + "Ltg_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, ltg_sat_values, type_limits=ltg_typelimits,
                                                 name=self.prefix + "Ltg_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, ltg_sun_values, type_limits=ltg_typelimits,
                                                 name=self.prefix + "Ltg_Schedule_Sunday")

        ltg_wd_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "Ltg_Weekdays")
        ltg_sat_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "Ltg_Saturday")
        ltg_sun_schrule = ScheduleTool.schedule_rule(ltg_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "Ltg_Sunday")

        self._lighting = ltg_schedule
        return self._lighting

    # Equipment Schedule
    def equipment(self):
        equip_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        equip_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=equip_typelimits,
                                                       name=self.prefix + "Equip_Schedule")
        equip_wd_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                           0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        equip_sat_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                            0.3, 0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        equip_sun_values = [0.1, 0.1, 0.1, 0.1, 0.1, 0.3, 0.45, 0.45, 0.45, 0.45, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3, 0.3,
                            0.3, 0.6, 0.8, 0.9, 0.8, 0.6, 0.3]
        schedule_wd = ScheduleTool.schedule_day(self._model, equip_wd_values, type_limits=equip_typelimits,
                                                name=self.prefix + "Equip_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, equip_sat_values, type_limits=equip_typelimits,
                                                 name=self.prefix + "Equip_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, equip_sun_values, type_limits=equip_typelimits,
                                                 name=self.prefix + "Equip_Schedule_Sunday")

        equip_wd_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_wd,
                                                      days=[True, True, True, True, True, False, False],
                                                      name=self.prefix + "Equip_Weekdays")
        equip_sat_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_sat,
                                                       days=[False, False, False, False, False, True, False],
                                                       name=self.prefix + "Equip_Saturday")
        equip_sun_schrule = ScheduleTool.schedule_rule(equip_schedule, schedule_sun,
                                                       days=[False, False, False, False, False, False, True],
                                                       name=self.prefix + "Equip_Sunday")

        self._equipment = equip_schedule
        return self._equipment

    def infiltration(self):
        infil_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        infil_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=infil_typelimits,
                                                       name=self.prefix + "Infil_Schedule")

        infil_wd_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                           0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        infil_sat_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                            0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        infil_sun_values = [0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                            0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25]
        schedule_wd = ScheduleTool.schedule_day(self._model, infil_wd_values, type_limits=infil_typelimits,
                                                name=self.prefix + "Infil_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, infil_sat_values, type_limits=infil_typelimits,
                                                 name=self.prefix + "Infil_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, infil_sun_values, type_limits=infil_typelimits,
                                                 name=self.prefix + "Infil_Schedule_Sunday")

        infil_wd_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_wd,
                                                      days=[True, True, True, True, True, False, False],
                                                      name=self.prefix + "Infil_Weekdays")
        infil_sat_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_sat,
                                                       days=[False, False, False, False, False, True, False],
                                                       name=self.prefix + "Infil_Saturday")
        infil_sun_schrule = ScheduleTool.schedule_rule(infil_schedule, schedule_sun,
                                                       days=[False, False, False, False, False, False, True],
                                                       name=self.prefix + "Infil_Sunday")

        self._infiltration = infil_schedule
        return self._infiltration

    def cooling_setpoint(self):
        temp_typelimits = ScheduleTool.schedule_type_limits(self._model, 2, 1, 0, 50)
        temp_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=temp_typelimits,
                                                      name=self.prefix + "ClgSP_Schedule")

        temp_wd_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                          25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
        temp_sat_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                           25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
        temp_sun_values = [25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6,
                           25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6, 25.6]
        schedule_wd = ScheduleTool.schedule_day(self._model, temp_wd_values, type_limits=temp_typelimits,
                                                name=self.prefix + "ClgSP_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, temp_sat_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "ClgSP_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, temp_sun_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "ClgSP_Schedule_Saturday")

        temp_wd_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "ClgSP_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "ClgSP_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "ClgSP_Saturday")
        temp_schedule.setSummerDesignDaySchedule(schedule_wd)
        temp_schedule.setWinterDesignDaySchedule(schedule_wd)

        self._cooling_setpoint = temp_schedule
        return self._cooling_setpoint

    def heating_setpoint(self):
        temp_typelimits = ScheduleTool.schedule_type_limits(self._model, 2, 1, 0, 50)
        temp_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=temp_typelimits,
                                                      name=self.prefix + "HtgSP_Schedule")
        temp_wd_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                          20, 20, 15.6, 15.6]
        temp_sat_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                           20, 20, 15.6, 15.6]
        temp_sun_values = [15.6, 15.6, 15.6, 15.6, 15.6, 15.6, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20, 20,
                           20, 20, 15.6, 15.6]
        schedule_wd = ScheduleTool.schedule_day(self._model, temp_wd_values, type_limits=temp_typelimits,
                                                name=self.prefix + "HtgSP_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, temp_sat_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "HtgSP_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, temp_sun_values, type_limits=temp_typelimits,
                                                 name=self.prefix + "HtgSP_Schedule_Sunday")

        temp_wd_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "HtgSP_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "HtgSP_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(temp_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "HtgSP_Sunday")
        temp_schedule.setSummerDesignDaySchedule(schedule_wd)
        temp_schedule.setWinterDesignDaySchedule(schedule_wd)

        self._heating_setpoint = temp_schedule
        return self._heating_setpoint

    def hvac_availability(self):
        avail_typelimits = ScheduleTool.schedule_type_limits(self._model, 11, 2)
        avail_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=avail_typelimits,
                                                       name=self.prefix + "Avail_Schedule")

        avail_wd_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        avail_sat_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        avail_sun_values = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
        schedule_wd = ScheduleTool.schedule_day(self._model, avail_wd_values, type_limits=avail_typelimits,
                                                name=self.prefix + "Avail_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, avail_sat_values, type_limits=avail_typelimits,
                                                 name=self.prefix + "Avail_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, avail_sun_values, type_limits=avail_typelimits,
                                                 name=self.prefix + "Avail_Schedule_Sunday")

        temp_wd_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name=self.prefix + "Avail_Weekdays")
        temp_sat_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name=self.prefix + "Avail_Saturday")
        temp_sun_schrule = ScheduleTool.schedule_rule(avail_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name=self.prefix + "Avail_Sunday")

        self._hvac_availability = avail_schedule
        return self._hvac_availability

    def dcv(self):
        dcv_typelimits = ScheduleTool.schedule_type_limits(self._model, 1, 1, 0, 1)
        dcv_schedule = ScheduleTool.schedule_ruleset(self._model, type_limits=dcv_typelimits,
                                                     name=self.prefix + "DCV_Schedule")

        dcv_wd_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                         0.7, 0.7, 0.8, 0.9, 0.9]
        dcv_sat_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                          0.7, 0.7, 0.8, 0.9, 0.9]
        dcv_sun_values = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.7, 0.4, 0.4, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.3, 0.5, 0.5, 0.5,
                          0.7, 0.7, 0.8, 0.9, 0.9]
        schedule_wd = ScheduleTool.schedule_day(self._model, dcv_wd_values, type_limits=dcv_typelimits,
                                                name=self.prefix + "DCV_Schedule_Weekdays")
        schedule_sat = ScheduleTool.schedule_day(self._model, dcv_sat_values, type_limits=dcv_typelimits,
                                                 name=self.prefix + "DCV_Schedule_Saturday")
        schedule_sun = ScheduleTool.schedule_day(self._model, dcv_sun_values, type_limits=dcv_typelimits,
                                                 name=self.prefix + "DCV_Schedule_Sunday")

        occ_wd_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_wd,
                                                    days=[True, True, True, True, True, False, False],
                                                    name=self.prefix + "DCV_Weekdays")
        occ_sat_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_sat,
                                                     days=[False, False, False, False, False, True, False],
                                                     name=self.prefix + "DCV_Saturday")
        occ_sun_schrule = ScheduleTool.schedule_rule(dcv_schedule, schedule_sun,
                                                     days=[False, False, False, False, False, False, True],
                                                     name=self.prefix + "DCV_Sunday")

        self._dcv = dcv_schedule
        return self._dcv

    def activity_level(self):
        act_typelimits = ScheduleTool.schedule_type_limits(self._model, 7, 1, 0, 200)
        act_schedule = ScheduleTool.schedule_ruleset(
            self._model,
            120,
            type_limits=act_typelimits,
            name=self.prefix + "Activity_Schedule")

        self._activity_level = act_schedule
        return self._activity_level
