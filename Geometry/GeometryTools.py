import math
import openstudio
import json
from openstudio.openstudiomodelgeometry import Surface, SubSurface, ShadingSurface
from openstudio.openstudioutilitiesgeometry import Vector3d, Point3dVector, Point3d
from Schedules.Template import schedule_sets_office
from Schedules.ScheduleTools import ScheduleSets
from Resources.ZoneTools import ZoneTool
from Resources.InternalLoad import InternalLoad
from Constructions.ConstructionTools import ConstructionTool


class GeometryTool:

    roof_threshold = math.pi / 4
    tolerance = 0.0001

    # Set up building:
    @staticmethod
    def building(model: openstudio.openstudiomodel.Model, name=None, north_axis=0):
        bldg = model.getBuilding()
        if name is not None:
            bldg.setName(name)
        if north_axis != 0:
            bldg.setNorthAxis(north_axis)
        return bldg

    # Make a Building Story
    @staticmethod
    def building_story(model, number_of_story: int = 1):
        stories = []
        for i in range(number_of_story):
            story = openstudio.openstudiomodel.BuildingStory(model)
            story.setName("Building Story " + str(i+1))
            stories.append(story)
        return stories

    # Make Vector3d
    @staticmethod
    def make_vector3d(vector):
        if len(vector) != 3 or len(vector) == 0:
            raise ValueError("Length of vector must be 3")
        else:
            vector3d = Vector3d(vector[0], vector[1], vector[2])

        return vector3d

    # Make Surface
    @staticmethod
    def make_surface(
            model: openstudio.openstudiomodel.Model,
            vertices,
            normal=None,
            surface_type: int = None,
            outside_boundary_condition: int = None,
            sun_exposure="Sunexposed",
            wind_exposure="Windexposed",
            construction: openstudio.openstudiomodel.Construction = None,
            space: openstudio.openstudiomodel.Space = None,
            name: str = None):

        """
        -Surface types: \n
        1.Wall 2.Floor 3.RoofCeiling \n

        -Outside_boundary_condition: \n
        1.Adiabatic
        2.Surface
        3.Outdoors
        4.Foundation
        5.Ground
        6.GroundFCfactorMethod
        7.OtherSideCoefficients
        8.OtherSideConditionsModel
        9.GroundSlabPreprocessorAverage
        10.GroundSlabPreprocessorCore
        """

        surface_types = {1: "Wall", 2: "Floor", 3: "RoofCeiling"}
        boundaries = {1: "Adiabatic", 2: "Surface", 3: "Outdoors", 4: "Foundation", 5: "Ground",
                      6: "GroundFCfactorMethod", 7: "OtherSideCoefficients", 8: "OtherSideConditionsModel",
                      9: "GroundSlabPreprocessorAverage", 10: "GroundSlabPreprocessorCore"}

        if isinstance(vertices, list):
            if len(vertices) != 0 and len(vertices) > 2:
                pt_vec = Point3dVector()
                for i in range(len(vertices)):
                    if len(vertices[i]) != 0:
                        pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                        pt_vec.append(pt)

                surface = Surface(pt_vec, model)

                # Calculate the angle between normal vector and z-axis (by Dot Product):
                if normal is None:
                    normal = GeometryTool.newell_method(surface)

                z_axis = Vector3d(0.0, 0.0, 1.0)

                angle_rad = math.acos(z_axis.dot(normal) / (z_axis.length() * normal.length()))
                centroid_z = GeometryTool.centroid(surface).z()

                # Assign surface type based on its orientation:
                # Assign boundary type based on its position:
                if angle_rad < GeometryTool.roof_threshold:
                    if surface_type is None:
                        surface.setSurfaceType("RoofCeiling")
                    else:
                        surface.setSurfaceType(surface_types[surface_type])

                    if outside_boundary_condition is None:
                        surface.setOutsideBoundaryCondition(boundaries[3])
                    else:
                        surface.setOutsideBoundaryCondition(boundaries[outside_boundary_condition])

                elif GeometryTool.roof_threshold <= angle_rad < 3 * GeometryTool.roof_threshold:
                    if surface_type is None:
                        surface.setSurfaceType("Wall")
                    else:
                        surface.setSurfaceType(surface_types[surface_type])

                    if outside_boundary_condition is None:
                        if centroid_z > GeometryTool.tolerance:
                            surface.setOutsideBoundaryCondition(boundaries[3])
                        else:
                            surface.setOutsideBoundaryCondition(boundaries[5])
                    else:
                        surface.setOutsideBoundaryCondition(boundaries[outside_boundary_condition])

                else:
                    if surface_type is None:
                        surface.setSurfaceType("Floor")
                    else:
                        surface.setSurfaceType(surface_types[surface_type])

                    if outside_boundary_condition is None:
                        if centroid_z > GeometryTool.tolerance:
                            surface.setOutsideBoundaryCondition(boundaries[3])
                        else:
                            surface.setOutsideBoundaryCondition(boundaries[5])
                    else:
                        surface.setOutsideBoundaryCondition(boundaries[outside_boundary_condition])

                surface.setSunExposure(sun_exposure)
                surface.setWindExposure(wind_exposure)
                if construction is not None:
                    surface.setConstruction(construction)
                if space is not None:
                    surface.setSpace(space)
                if name is not None:
                    surface.setName(name)

                return surface

            else:
                raise ValueError("Not Enough Vertices to Create a Surface")
        else:
            raise TypeError("Invalid input type of vertex list")

    # Make Subsurface:
    @staticmethod
    def make_fenestration(
            model,
            vertices,
            surface_type="FixedWindow",
            construction=None,
            surface=None,
            name: str = None):

        if len(vertices) != 0 and len(vertices) > 2:
            pt_vec = Point3dVector()
            for i in range(len(vertices)):
                if len(vertices[i]) != 0:
                    pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                    pt_vec.append(pt)

            subsurface = SubSurface(pt_vec, model)

            subsurface.setSubSurfaceType(surface_type)
            if construction is not None:
                subsurface.setConstruction(construction)
            if surface is not None:
                subsurface.setSurface(surface)
            if name is not None:
                subsurface.setName(name)
        else:
            raise ValueError("Not Enough Vertices to Create a Surface")

        return subsurface

    # Create a shading surface:
    @staticmethod
    def make_shading(model, vertices, construction=None, transmittance_schedule=None, name: str = None):
        if len(vertices) != 0 and len(vertices) > 2:
            pt_vec = Point3dVector()
            for i in range(len(vertices)):
                if len(vertices[i]) != 0:
                    pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                    pt_vec.append(pt)

            shading = ShadingSurface(pt_vec, model)
            if construction is not None:
                shading.setConstruction(construction)
            if transmittance_schedule is not None:
                shading.setTransmittanceSchedule(transmittance_schedule)
            if name is not None:
                shading.setName(name)

            return shading

    # Create a room from extrusion
    @staticmethod
    def space_from_extrusion(model, floor_plan, room_height: float = 3.0, wwr=None,
                             space: openstudio.openstudiomodel.Space = None,
                             construction_set: openstudio.openstudiomodel.DefaultConstructionSet = None,
                             building_story: openstudio.openstudiomodel.BuildingStory = None):

        room_surfaces = []
        if len(floor_plan) != 0 and len(floor_plan) > 2:
            # upward_normal = None
            # Floor surface:
            # *********************************************************
            # First check normal vector (cross product):
            vector_12 = Vector3d(floor_plan[1][0] - floor_plan[0][0],
                                 floor_plan[1][1] - floor_plan[0][1],
                                 floor_plan[1][2] - floor_plan[0][2])
            vector_23 = Vector3d(floor_plan[2][0] - floor_plan[1][0],
                                 floor_plan[2][1] - floor_plan[1][1],
                                 floor_plan[2][2] - floor_plan[1][2])
            normal = vector_12.cross(vector_23)
            normal.normalize()
            z_axis = Vector3d(0.0, 0.0, -1.0)

            # Calculate angle between minus z-axis and floor surface normal:
            angle_rad = math.acos(z_axis.dot(normal) / (z_axis.length() * normal.length()))

            floor_pts = []
            for i in range(len(floor_plan)):
                if len(floor_plan[i]) != 0:
                    floor_pt = Point3d(floor_plan[i][0], floor_plan[i][1], floor_plan[i][2])
                    floor_pts.append(floor_pt)
            if angle_rad > math.pi/4:
                floor_pts.reverse()
                upward_normal = normal
            else:
                upward_normal = normal.reverseVector()

            floor_pt_vec = Point3dVector(floor_pts)
            floor_surface = Surface(floor_pt_vec, model)
            room_surfaces.append(floor_surface)
            upward_normal.normalize()

            # roof surface:
            # *********************************************************
            roof_pts = []
            for i in range(len(floor_plan)):
                if len(floor_plan[i]) != 0:
                    roof_pt = Point3d(floor_plan[i][0] + room_height * upward_normal.x(),
                                      floor_plan[i][1] + room_height * upward_normal.y(),
                                      floor_plan[i][2] + room_height * upward_normal.z())
                    roof_pts.append(roof_pt)
            if angle_rad <= math.pi/4:
                roof_pts.reverse()

            roof_pt_vec = Point3dVector(roof_pts)
            roof_surface = Surface(roof_pt_vec, model)
            room_surfaces.append(roof_surface)

            # Wall surfaces:
            # *********************************************************
            for i in range(len(floor_plan)):
                wall_pts = []
                index_1 = i
                index_2 = (i + 1) % len(floor_plan)
                if len(floor_plan[index_1]) != 0 and len(floor_plan[index_2]) != 0:
                    wall_pt1 = Point3d(floor_plan[index_1][0], floor_plan[index_1][1], floor_plan[index_1][2])
                    wall_pt2 = Point3d(floor_plan[index_2][0], floor_plan[index_2][1], floor_plan[index_2][2])
                    wall_pt3 = Point3d(floor_plan[index_2][0] + room_height * upward_normal.x(),
                                       floor_plan[index_2][1] + room_height * upward_normal.y(),
                                       floor_plan[index_2][2] + room_height * upward_normal.z())
                    wall_pt4 = Point3d(floor_plan[index_1][0] + room_height * upward_normal.x(),
                                       floor_plan[index_1][1] + room_height * upward_normal.y(),
                                       floor_plan[index_1][2] + room_height * upward_normal.z())
                    wall_pts.append(wall_pt1)
                    wall_pts.append(wall_pt2)
                    wall_pts.append(wall_pt3)
                    wall_pts.append(wall_pt4)

                    if angle_rad <= math.pi/4:
                        wall_pts.reverse()

                    wall_pt_vec = Point3dVector(wall_pts)
                    wall_surface = Surface(wall_pt_vec, model)
                    if wwr is not None:
                        wall_surface.setWindowToWallRatio(wwr)
                    room_surfaces.append(wall_surface)

        # Assign surface to a space
        if space is not None:
            for surface in room_surfaces:
                surface.setSpace(space)

        # Assign default construction set to the space
        if construction_set is not None:
            space.setDefaultConstructionSet(construction_set)

        # Assign building story
        if building_story is not None:
            space.setBuildingStory(building_story)

        return room_surfaces

    @staticmethod
    def geometry_from_json(
            model: openstudio.openstudiomodel.Model,
            json_path: str,
            internal_load: str = None,
            construction_sets: openstudio.openstudiomodel.DefaultConstructionSet = None,
            schedule_sets=None,
            story_multipliers=None):

        """
        :param model: an openstudio model object.
        :param json_path: a file path of json. Use output from method "load_from_rhino" here.
        :param internal_load: a json file. Use output from method "internal_load_input_json" here.
        :param construction_sets: a DefaultConstructionSet object.
        :param schedule_sets: a dictionary. Use output from method "schedule_set_input_json" here.
        """

        with open(json_path, 'r') as openfile:
            # Reading from json file
            json_object = json.load(openfile)

        rooms = json_object["rooms"]
        number_of_stories = int(json_object["number_of_stories"])
        stories = GeometryTool.building_story(model, number_of_stories)

        # Construction sets:
        if construction_sets is not None:
            cons_set = construction_sets
        else:
            # cons_set = ConstructionSet(model, "ASHRAE Default Set").get()
            cons_set = ConstructionTool.construction_set_simple(
                model, "Chinese Code Compliance Set", False,
                0.6, 0.4, 0.7, 2.2, 0.35, 0.8, 0.6, 0.4, 0.6, 0.4, 0.7)

        # Internal load data:
        loads = {}
        schedules = {}
        if internal_load is not None:
            internal_loads = json.loads(internal_load)
            space_types = internal_loads.keys()

            for i, space in enumerate(space_types):
                # space = space.lower()
                load_dict = {"lighting": None, "electric_equip": None, "people": None,
                             "gas_equip": None, "space_type": None, "conditioned": None}
                load_of_space = internal_loads[space]
                people_cal_method = internal_loads[space]["people_density_method"]

                # Schedule set for this space type:
                if schedule_sets is not None:
                    if isinstance(schedule_sets, ScheduleSets):
                        schedules[space] = schedule_sets.get_schedule_sets()
                    elif isinstance(schedule_sets, dict):
                        # print(space)
                        schedules[space] = schedule_sets[space].get_schedule_sets()
                    else:
                        schedules[space] = schedule_sets_office(model)
                else:
                    schedules[space] = schedule_sets_office(model)

                # Lighting Definition:
                light = InternalLoad.light_definition(
                    model, lighting_power=load_of_space["lighting"], name=space + "_Light_Definition")
                load_dict["lighting"] = light

                # Electric Equipment Definition:
                electric_equip = InternalLoad.electric_equipment_definition(
                    model, power=load_of_space["equipment"], name=space + "_Equipment_Definition")
                load_dict["electric_equip"] = electric_equip

                # People Definition:
                match people_cal_method:
                    case "People":
                        people = InternalLoad.people_definition(
                            model, 1, load_of_space["people_density"], name=space + "_People_Definition")
                    case "Area/Person":
                        people = InternalLoad.people_definition(
                            model, 2, load_of_space["people_density"], name=space + "_People_Definition")
                    case "Person/Area" | _:
                        people = InternalLoad.people_definition(
                            model, 3, load_of_space["people_density"], name=space + "_People_Definition")
                load_dict["people"] = people

                # Gas Equipment Definition:
                if load_of_space["gas_power"] is not None:
                    gas_equip = InternalLoad.gas_equipment_definition(
                        model, load_of_space["gas_power"], name=space + "_Gas_Definition")
                    load_dict["gas_equip"] = gas_equip

                # Outdoor Air:
                if schedules[space]["occupancy"] is not None:
                    outdoor_air = InternalLoad.outdoor_air(
                        model, outdoor_air_per_floor_area=load_of_space["outdoor_air_per_area"],
                        outdoor_air_per_person=load_of_space["outdoor_air_per_person"],
                        schedule=schedules[space]["occupancy"], name=space + "_DSOA")
                else:
                    outdoor_air = InternalLoad.outdoor_air(
                        model, outdoor_air_per_floor_area=load_of_space["outdoor_air_per_area"],
                        outdoor_air_per_person=load_of_space["outdoor_air_per_person"], name=space + "_DSOA")

                if schedules[space]["infiltration"] is not None:
                    infiltration = InternalLoad.infiltration(
                        model, schedule=schedules[space]["infiltration"], name=space + "_Infiltration")
                else:
                    infiltration = InternalLoad.infiltration(model, name=space + "_Infiltration")

                space_type = ZoneTool.space_type(model, space, space, outdoor_air, infiltration)
                load_dict["space_type"] = space_type

                load_dict["conditioned"] = load_of_space["conditioned"]

                loads[space] = load_dict

        # Rooms in the building
        thermal_zones = []
        oriented_walls = {"east": [], "west": [], "north": [], "south": [], "other": []}
        oriented_subsurfaces = {"east": [], "west": [], "north": [], "south": [], "other": []}

        if len(rooms) != 0:

            all_surfaces = []
            all_subsurfaces = []

            for i, room in enumerate(rooms, 1):
                room_type = room["space_type"]

                # Define internal load object for each space:
                # People:
                if schedules[room_type]["occupancy"] is not None and schedules[room_type]["activity"] is not None:
                    people = InternalLoad.people(
                        loads[room_type]["people"],
                        schedule=schedules[room_type]["occupancy"], activity_schedule=schedules[room_type]["activity"])
                else:
                    people = InternalLoad.people(loads[room_type]["people"])

                # Electric Equipment:
                if schedules[room_type]["electric_equipment"] is not None:
                    electric_equip = InternalLoad.electric_equipment(
                        loads[room_type]["electric_equip"], schedule=schedules[room_type]["electric_equipment"])
                else:
                    electric_equip = InternalLoad.electric_equipment(loads[room_type]["electric_equip"])

                # Light:
                if schedules[room_type]["lighting"] is not None:
                    light = InternalLoad.light(
                        loads[room_type]["lighting"], schedule=schedules[room_type]["lighting"])
                else:
                    light = InternalLoad.light(loads[room_type]["lighting"])

                name = str(room["story"]) + "F_" + room_type + "_{}".format(i)

                # Create space object:
                space = ZoneTool.space(
                    model,
                    space_type=loads[room_type]["space_type"],
                    name=name,
                    story=stories[int(room["story"])-1],
                    lights=light,
                    people=people,
                    electric_equipment=electric_equip)

                space.setDefaultConstructionSet(cons_set)

                # Thermal zones:
                # Conditioned Zones:
                conditioned = loads[room_type]["conditioned"]
                if conditioned:
                    if schedules[room_type]["cooling_setpoint"] is not None and \
                            schedules[room_type]["heating_setpoint"] is not None:
                        temp_control = True
                    else:
                        temp_control = False

                    if schedules[room_type]["humidify_setpoint"] is not None and \
                            schedules[room_type]["dehumidify_setpoint"] is not None:
                        hum_control = True
                    else:
                        hum_control = False

                    if temp_control and hum_control:
                        thermal_zone = ZoneTool.thermal_zone_from_space(
                            model, space,
                            schedules[room_type]["cooling_setpoint"], schedules[room_type]["heating_setpoint"],
                            schedules[room_type]["dehumidify_setpoint"], schedules[room_type]["humidify_setpoint"])
                    elif temp_control and not hum_control:
                        thermal_zone = ZoneTool.thermal_zone_from_space(
                            model, space,
                            schedules[room_type]["cooling_setpoint"], schedules[room_type]["heating_setpoint"])
                    else:
                        thermal_zone = ZoneTool.thermal_zone_from_space(model, space)

                # Unconditioned Zones:
                else:
                    # print(room_type + " is unconditioned")
                    thermal_zone = ZoneTool.thermal_zone_from_space(model, space)

                # Multiplier if applicable:
                # thermal_zone.setMultiplier(1)

                thermal_zone_dict = {
                    "zone": thermal_zone, "name": name, "story": room["story"],
                    "space_type": room_type, "conditioned": conditioned}

                thermal_zones.append(thermal_zone_dict)

                # Create surfaces and subsurface:
                surfaces = room["surfaces"]
                for srf in surfaces:
                    vertices = srf["vertices"]
                    name = srf["name"]

                    surface = GeometryTool.make_surface(model, vertices, space=space, name=name)

                    all_surfaces.append(surface)

                    if len(srf["fenestrations"]) != 0:
                        for fenestration in srf["fenestrations"]:
                            fen_srf = GeometryTool.make_fenestration(
                                model, fenestration["vertices"], surface=surface, name=fenestration["name"])
                            all_subsurfaces.append(fen_srf)

                            win_normal = fenestration["normal"]
                            win_orient = GeometryTool.check_orientation(
                                Vector3d(win_normal[0], win_normal[1], win_normal[2]))

                            match win_orient:
                                case "east":
                                    oriented_subsurfaces["east"].append(fen_srf)
                                case "west":
                                    oriented_subsurfaces["west"].append(fen_srf)
                                case "north":
                                    oriented_subsurfaces["north"].append(fen_srf)
                                case "south":
                                    oriented_subsurfaces["south"].append(fen_srf)
                                case _:
                                    oriented_subsurfaces["other"].append(fen_srf)

            updated_surfaces = GeometryTool.solve_adjacency(all_surfaces, True, cons_set)
            # GeometryTool.adiabatic_by_type(updated_surfaces, 2)

            for srf in updated_surfaces:
                srf_type = srf.surfaceType()
                boundary = srf.outsideBoundaryCondition()
                if srf_type == "Wall" and boundary == "Outdoors":
                    srf_orient = GeometryTool.check_orientation(GeometryTool.newell_method(srf))

                    match srf_orient:
                        case "east":
                            oriented_walls["east"].append(srf)
                        case "west":
                            oriented_walls["west"].append(srf)
                        case "north":
                            oriented_walls["north"].append(srf)
                        case "south":
                            oriented_walls["south"].append(srf)
                        case _:
                            oriented_walls["other"].append(srf)

            # Shading Objects:
            shades = json_object["shades"]
            all_shades = []
            if len(shades) != 0:
                for shade in shades:
                    shade_srf = GeometryTool.make_shading(model, shade["vertices"], name=shade["name"])
                    all_shades.append(shade_srf)

        return thermal_zones, oriented_walls, oriented_subsurfaces

    # Newell's Algorithm (find normal vector from an arbitrary polygon)
    @staticmethod
    def newell_method(surface):
        nx, ny, nz = 0, 0, 0
        vertices = surface.vertices()
        for i in range(len(vertices)):
            p0 = vertices[i]
            p1 = vertices[(i + 1) % len(vertices)]

            nx += (p0.y() - p1.y()) * (p0.z() + p1.z())
            ny += (p0.z() - p1.z()) * (p0.x() + p1.x())
            nz += (p0.x() - p1.x()) * (p0.y() + p1.y())

        normal = Vector3d(nx, ny, nz)
        normal.normalize()

        return normal

    # Find centroid of a polygon:
    @staticmethod
    def centroid(surface):
        vertices = surface.vertices()
        cx = sum(pt.x() for pt in vertices)
        cy = sum(pt.y() for pt in vertices)
        cz = sum(pt.z() for pt in vertices)

        centroid = Point3d(cx, cy, cz)
        return centroid

    # Distance between two points:
    @staticmethod
    def distance(point1, point2):
        dx = math.pow((point1.x() - point2.x()), 2)
        dy = math.pow((point1.y() - point2.y()), 2)
        dz = math.pow((point1.z() - point2.z()), 2)
        dist = math.sqrt(dx + dy + dz)
        return dist

    # Find Adjacent Surfaces:
    @staticmethod
    def solve_adjacency(
            surfaces,
            adiabatic: bool = False,
            construction_sets: openstudio.openstudiomodel.DefaultConstructionSet = None):

        surfaces_adj = []
        updated_surfaces = []

        if len(surfaces) < 2:
            raise ValueError("Not enough surfaces to solve adjacency")
        else:
            for i, srf_curr in enumerate(surfaces):

                # First, find normal vector and centroid:
                normal_curr = GeometryTool.newell_method(srf_curr)
                centroid_curr = GeometryTool.centroid(srf_curr)

                for j, srf_rest in enumerate(surfaces[i+1:]):
                    normal_rest = GeometryTool.newell_method(srf_rest)
                    centroid_rest = GeometryTool.centroid(srf_rest)
                    dot = normal_curr.dot(normal_rest) / (normal_curr.length() * normal_rest.length())

                    # Normalize the dot value to avoid ValueError of math.acos:
                    if dot > 1.0:
                        dot = 1.0
                    if dot < -1.0:
                        dot = -1.0

                    angle = math.acos(dot)
                    dist = GeometryTool.distance(centroid_curr, centroid_rest)

                    if math.fabs(angle - math.pi) < GeometryTool.tolerance and dist < GeometryTool.tolerance:
                        surfaces_adj.append(srf_curr)
                        surfaces_adj.append(srf_rest)
                        srf_curr.setAdjacentSurface(srf_rest)

                        interior_wall = construction_sets.defaultInteriorSurfaceConstructions().get().wallConstruction().get()
                        interior_floor = construction_sets.defaultInteriorSurfaceConstructions().get().floorConstruction().get()

                        if srf_curr.surfaceType() == "Wall":
                            srf_curr.setConstruction(interior_wall)
                            srf_rest.setConstruction(interior_wall)
                        else:
                            srf_curr.setConstruction(interior_floor)
                            srf_rest.setConstruction(interior_floor)

                        if adiabatic:
                            srf_curr.setOutsideBoundaryCondition("Adiabatic")
                            srf_rest.setOutsideBoundaryCondition("Adiabatic")
                        else:
                            srf_curr.setOutsideBoundaryCondition("Surface")
                            srf_rest.setOutsideBoundaryCondition("Surface")

                        srf_curr.setSunExposure("NoSun")
                        srf_rest.setSunExposure("NoSun")
                        srf_curr.setWindExposure("NoWind")
                        srf_rest.setWindExposure("NoWind")

                updated_surfaces.append(srf_curr)

        return updated_surfaces

    @staticmethod
    def check_orientation(normal: Vector3d):

        angle_threshold = math.pi / 4
        orientation = "east"

        orient_vectors = {
            "east": Vector3d(1, 0, 0),
            "west": Vector3d(-1, 0, 0),
            "north": Vector3d(0, 1, 0),
            "south": Vector3d(0, -1, 0)}

        for key in orient_vectors.keys():
            angle = math.acos(normal.dot(orient_vectors[key]) / (normal.length() * orient_vectors[key].length()))

            if angle <= angle_threshold:
                orientation = key
                break
            else:
                orientation = "other"

        return orientation

    @staticmethod
    def adiabatic_by_type(surfaces: list, surface_type: int = 0):
        """
        Surface_type: \n

        """
        surface_types = {0: "None", 1: "walls", 2: "interiorWalls", 3: "airWalls", 4: "windows", 5: "interiorWindows",
                         6: "roofs", 7: "ceilings", 8: "floors", 9: "exposedFloors", 10: "groundFloors",
                         11: "undergroundWalls", 12: "undergroundSlabs", 13: "undergroundCeilings"}

        for surface in surfaces:
            srf_type = surface.surfaceType()
            boundary_type = surface.outsideBoundaryCondition()

            match surface_type:
                case 0:
                    pass
                case 1:
                    if srf_type == "Wall" and boundary_type == "Outdoors":
                        surface.setOutsideBoundaryCondition("Adiabatic")
                case 2 | 3:
                    if srf_type == "Wall" and boundary_type == "Surface":
                        surface.setOutsideBoundaryCondition("Adiabatic")
                case _:
                    pass
