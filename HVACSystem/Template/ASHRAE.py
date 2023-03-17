import openstudio
from Schedules.ScheduleTools import ScheduleTool


class ASHRAEBaseline:

    @staticmethod
    def system_list():
        systems = {1: "PTAC",
                   2: "PTHP",
                   3: "PSZ-AC",
                   4: "PSZ-HP",
                   5: "Packaged VAV with Reheat",
                   6: "Packaged VAV with PFP Boxes",
                   7: "VAV with Reheat",
                   8: "VAV with PFP Boxes",
                   9: "Heating and Ventilation",
                   10: "Heating and Ventilation"}
        print(systems)
    @staticmethod
    def system_1(
            model: openstudio.openstudiomodel.Model,
            thermal_zones=[]):

        ptac = openstudio.openstudiomodel.ZoneHVACPackagedTerminalAirConditioner(model, ScheduleTool.always_on(model))

        if thermal_zones is not None and len(thermal_zones) != 0:
            for zone in thermal_zones:
                ptac.addToThermalZone(zone)

