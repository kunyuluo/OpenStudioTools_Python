from openstudio.openstudiomodel import Space, SpaceType, ThermalZone
from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate


class ZoneTool:

    # Create a thermal zone
    @staticmethod
    def thermal_zone(model, name):
        zone = ThermalZone(model)
        zone.setName(name)

        return zone

    # Create a space:
    @staticmethod
    def space(
            model,
            name,
            program,
            thermal_zone=None,
            story=None,
            lighting_power=0,
            equipment_power=0,
            people_density=0,
            outdoor_air_per_floor_area=0,
            outdoor_air_per_person=0,
            lighting_schedule=None,
            equipment_schedule=None,
            occupancy_schedule=None,
            activity_schedule=None,
            infiltration_schedule=None):
        space = Space(model)
        space.setName(name)
        if thermal_zone is not None: space.setThermalZone(thermal_zone)
        if story is not None: space.setBuildingStory(story)

        # Define internal load objects:
        # Lighting:
        lighting_def = LightsDefinition(model)
        lighting_def.setWattsperSpaceFloorArea(lighting_power)
        light = Lights(lighting_def)
        if lighting_schedule is not None: light.setSchedule(lighting_schedule)
        light.setSpace(space)

        # Equipment:
        equipment_def = ElectricEquipmentDefinition(model)
        equipment_def.setWattsperSpaceFloorArea(equipment_power)
        equipment = ElectricEquipment(equipment_def)
        if equipment_schedule is not None: equipment.setSchedule(equipment_schedule)
        equipment.setSpace(space)

        # People:
        people_def = PeopleDefinition(model)
        people_def.setPeopleperSpaceFloorArea(people_density)
        people = People(people_def)
        if occupancy_schedule is not None: people.setNumberofPeopleSchedule(occupancy_schedule)
        if activity_schedule is not None: people.setActivityLevelSchedule(activity_schedule)
        people.setSpace(space)

        # Space Type:
        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        # Outdoor Air:
        outdoor_air = DesignSpecificationOutdoorAir(model)
        outdoor_air.setName(name + "_DSOA")
        outdoor_air.setOutdoorAirMethod("Sum")
        outdoor_air.setOutdoorAirFlowperFloorArea(outdoor_air_per_floor_area)
        outdoor_air.setOutdoorAirFlowperPerson(outdoor_air_per_person)
        if occupancy_schedule is not None: outdoor_air.setOutdoorAirFlowRateFractionSchedule(occupancy_schedule)

        space_type.setDesignSpecificationOutdoorAir(outdoor_air)

        # Infiltration Flow Rate:
        infiltration = SpaceInfiltrationDesignFlowRate(model)
        infiltration.setSpaceType(space_type)
        infiltration.setFlowperExteriorSurfaceArea(0.000226568446)
        if infiltration_schedule is not None: infiltration.setSchedule(infiltration_schedule)

        # Apply space type:
        space.setSpaceType(space_type)

        return space



