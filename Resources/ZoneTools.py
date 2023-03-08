import openstudio
from openstudio.openstudiomodel import Space, SpaceType, ThermalZone, BuildingStory
from openstudio.openstudiomodel import Lights, ElectricEquipment, People
from openstudio.openstudiomodel import GasEquipment, InternalMass
from openstudio.openstudiomodel import LightsDefinition, ElectricEquipmentDefinition, PeopleDefinition
from openstudio.openstudiomodel import GasEquipmentDefinition, InternalMassDefinition
from openstudio.openstudiomodel import DesignSpecificationOutdoorAir, SpaceInfiltrationDesignFlowRate
from Schedules.Templates.Office import Office


class ZoneTool:

    # Create a thermal zone
    @staticmethod
    def thermal_zone(model, name):
        zone = ThermalZone(model)
        zone.setName(name)

        return zone

    # Create a space with full set of information:
    @staticmethod
    def space_simplified(
            model,
            name,
            program,
            thermal_zone=None,
            story=None,
            lighting_power=0,
            equipment_power=0,
            people_density=0,
            gas_power=0,
            outdoor_air_per_floor_area=0,
            outdoor_air_per_person=0,
            internal_mass: InternalMass = None,
            lighting_schedule=None,
            equipment_schedule=None,
            occupancy_schedule=None,
            activity_schedule=None,
            infiltration_schedule=None,
            gas_schedule=None):

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

        # Gas Equipment:
        gas_def = GasEquipmentDefinition(model)
        gas_def.setWattsperSpaceFloorArea(gas_power)
        gas = GasEquipment(gas_def)
        if gas_schedule is not None: gas.setSchedule(gas_schedule)
        gas.setSpace(space)

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

    @staticmethod
    def space(
            model: openstudio.openstudiomodel.Model,
            name: str,
            program: str,
            thermal_zone: ThermalZone = None,
            story: BuildingStory = None,
            lights: Lights = None,
            people: People = None,
            electric_equipment: ElectricEquipment = None,
            gas_equipment: GasEquipment = None,
            internal_mass: InternalMass = None,
            outdoor_air: DesignSpecificationOutdoorAir = None,
            infiltration:SpaceInfiltrationDesignFlowRate = None):

        space = Space(model)
        space.setName(name)
        if thermal_zone is not None: space.setThermalZone(thermal_zone)
        if story is not None: space.setBuildingStory(story)

        # Space Type:
        space_type = SpaceType(model)
        space_type.setName(program + ":" + name)

        if lights is not None: lights.setSpace(space)
        if people is not None: people.setSpace(space)
        if electric_equipment is not None: electric_equipment.setSpace(space)
        if gas_equipment is not None: gas_equipment.setSpace(space)
        if internal_mass is not None: internal_mass.setSpace(space)
        if outdoor_air is not None:
            space_type.setDesignSpecificationOutdoorAir(outdoor_air)
        if infiltration is not None:
            infiltration.setSpaceType(space_type)
