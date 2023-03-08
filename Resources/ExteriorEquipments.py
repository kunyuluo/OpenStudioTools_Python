import openstudio
from openstudio.openstudiomodel import ExteriorLights, ExteriorFuelEquipment, ExteriorWaterEquipment
from openstudio.openstudiomodel import ExteriorLightsDefinition, ExteriorFuelEquipmentDefinition, ExteriorWaterEquipmentDefinition


class ExteriorEquipments:

    @staticmethod
    def exterior_lights(
            model: openstudio.openstudiomodel.Model,
            name=None,
            design_level=0,
            schedule=None,
            control_option="AstronomicalClock",
            multiplier=1):
        ext_light_def = ExteriorLightsDefinition(model)
        if name is not None: ext_light_def.setName(name)
        ext_light_def.setDesignLevel(design_level)

        ext_light = ExteriorLights(ext_light_def)
        ext_light.setControlOption(control_option)
        if control_option == "ScheduleNameOnly" and schedule is not None:
            ext_light.setSchedule(schedule)
        if multiplier != 1: ext_light.setMultiplier(multiplier)

    @staticmethod
    def exterior_fuel(
            model: openstudio.openstudiomodel.Model,
            name=None,
            design_level=0,
            schedule=None,
            fuel_type="NaturalGas",
            multiplier=1):
        ext_fuel_def = ExteriorFuelEquipmentDefinition(model)
        if name is not None: ext_fuel_def.setName(name)
        ext_fuel_def.setDesignLevel(design_level)

        ext_fuel = ExteriorFuelEquipment(ext_fuel_def)
        # Alternatives of fuel type:
        # *******************************************************************
        # Electricity        NaturalGas
        # Propane            Diesel
        # FuelOilNo1         FuelOilNo2
        # Gasoline           Coal
        # *******************************************************************
        ext_fuel.setFuelType(fuel_type)
        if schedule is not None: ext_fuel.setSchedule(schedule)
        if multiplier != 1: ext_fuel.setMultiplier(multiplier)

    @staticmethod
    def exterior_water(
            model: openstudio.openstudiomodel.Model,
            name=None,
            design_level=0,
            schedule=None,
            multiplier=1):
        ext_water_def = ExteriorWaterEquipmentDefinition(model)
        if name is not None: ext_water_def.setName(name)
        ext_water_def.setDesignLevel(design_level)

        ext_water = ExteriorWaterEquipment(ext_water_def)
        if schedule is not None: ext_water.setSchedule(schedule)
        if multiplier != 1: ext_water.setMultiplier(multiplier)