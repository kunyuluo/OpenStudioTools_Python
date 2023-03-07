from Schedules.ScheduleTools import ScheduleTool

class Office:

    def __init__(
            self,
            model,
            occupancy=None,
            lighting=None,
            equipment=None,
            infiltration=None,
            coolingsetpoint=None,
            heatingsetpoint=None,
            hvacavailability=None,
            dcv=None,
            activitylevel=None):
        self._model = model
        self._occupancy = occupancy
        self._lighting = lighting
        self._equipment = equipment
        self._infiltration = infiltration
        self._coolingsetpoint = coolingsetpoint
        self._heatingsetpoint = heatingsetpoint
        self._hvacavailability = hvacavailability
        self._dcv = dcv
        self._activitylevel = activitylevel

    # Occupancy Schedule
    @classmethod
    def occupancy(self):
        occ_typelimits = ScheduleTool.ScheduleTypeLimits(self._model, "Dimensionless", 0, 1, "Continuous")
        occ_schedule = ScheduleTool.ScheduleRuleset(self._model,typelimits=occ_typelimits, name="Office_Occ_Schedule")

        occ_wd_values = [0, 0, 0, 0, 0, 0, 0.1, 0.2, 0.95, 0.95, 0.95, 0.95, 0.5, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.95, 0.55, 0.1, 0.05, 0.05]
        occ_sat_values = [0, 0, 0, 0, 0, 0, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05, 0.05, 0, 0, 0, 0, 0]
        occ_sun_values = [0, 0, 0, 0, 0, 0, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0, 0, 0, 0, 0, 0]
        schedule_wd = ScheduleTool.ScheduleDay(self._model, occ_wd_values, typelimits=occ_typelimits)
        schedule_sat = ScheduleTool.ScheduleDay(self._model, occ_sat_values, typelimits=occ_typelimits)
        schedule_sun = ScheduleTool.ScheduleDay(self._model, occ_sun_values, typelimits=occ_typelimits)

        occ_wd_schrule = ScheduleTool.ScheduleRule(occ_schedule, schedule_wd,
                                                   days=[True, True, True, True, True, False, False],
                                                   name="Schedule Rule Weekdays")
        occ_sat_schrule = ScheduleTool.ScheduleRule(occ_schedule, schedule_sat,
                                                    days=[False, False, False, False, False, True, False],
                                                    name="Schedule Rule Saturday")
        occ_sun_schrule = ScheduleTool.ScheduleRule(occ_schedule, schedule_sun,
                                                    days=[False, False, False, False, False, False, True],
                                                    name="Schedule Rule Sunday")

        self._occupancy = occ_schedule
        return self._occupancy

    # Lighting Schedule
    @classmethod
    def lighting(self):
        ltg_typelimits = ScheduleTool.ScheduleTypeLimits(self._model, "Dimensionless", 0, 1, "Continuous")
        ltg_schedule = ScheduleTool.ScheduleRuleset(self._model, typelimits=ltg_typelimits, name="Office_Occ_Schedule")

        ltg_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.65, 0.35, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
        ltg_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        ltg_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        schedule_wd = ScheduleTool.ScheduleDay(self._model, ltg_wd_values, typelimits=ltg_typelimits)
        schedule_sat = ScheduleTool.ScheduleDay(self._model, ltg_sat_values, typelimits=ltg_typelimits)
        schedule_sun = ScheduleTool.ScheduleDay(self._model, ltg_sun_values, typelimits=ltg_typelimits)

        ltg_wd_schrule = ScheduleTool.ScheduleRule(ltg_schedule, schedule_wd,
                                                   days=[True, True, True, True, True, False, False],
                                                   name="Schedule Rule Weekdays")
        ltg_sat_schrule = ScheduleTool.ScheduleRule(ltg_schedule, schedule_sat,
                                                    days=[False, False, False, False, False, True, False],
                                                    name="Schedule Rule Saturday")
        ltg_sun_schrule = ScheduleTool.ScheduleRule(ltg_schedule, schedule_sun,
                                                    days=[False, False, False, False, False, False, True],
                                                    name="Schedule Rule Sunday")

        self._lighting = ltg_schedule
        return self._lighting

    # Equipment Schedule
    @classmethod
    def equipment(self):
        equip_typelimits = ScheduleTool.ScheduleTypeLimits(self._model, "Dimensionless", 0, 1, "Continuous")
        equip_schedule = ScheduleTool.ScheduleRuleset(self._model, typelimits=equip_typelimits,
                                                      name="Office_Occ_Schedule")
        equip_wd_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.5, 0.3, 0.3, 0.2, 0.2, 0.1, 0.05]
        equip_sat_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.15, 0.15, 0.15, 0.15, 0.15, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        equip_sun_values = [0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05]
        schedule_wd = ScheduleTool.ScheduleDay(self._model, equip_wd_values, typelimits=equip_typelimits)
        schedule_sat = ScheduleTool.ScheduleDay(self._model, equip_sat_values, typelimits=equip_typelimits)
        schedule_sun = ScheduleTool.ScheduleDay(self._model, equip_sun_values, typelimits=equip_typelimits)

        equip_wd_schrule = ScheduleTool.ScheduleRule(equip_schedule, schedule_wd,
                                                     days=[True, True, True, True, True, False, False],
                                                     name="Schedule Rule Weekdays")
        equip_sat_schrule = ScheduleTool.ScheduleRule(equip_schedule, schedule_sat,
                                                      days=[False, False, False, False, False, True, False],
                                                      name="Schedule Rule Saturday")
        equip_sun_schrule = ScheduleTool.ScheduleRule(equip_schedule, schedule_sun,
                                                      days=[False, False, False, False, False, False, True],
                                                      name="Schedule Rule Sunday")

        self._equipment = equip_schedule
        return self._equipment