import math
import openstudio
from openstudio.openstudiomodelgeometry import Surface, SubSurface, ShadingSurface
from openstudio.openstudioutilitiesgeometry import Vector3d, Point3dVector, Point3d


class GeometryTool:
    roof_threshold = math.pi / 4
    tolerance = 0.0001

    # def __init__(self, roof_threshold = math.pi/4):
    #     self._roof_threshold = roof_threshold

    # Set up building:
    @staticmethod
    def building(model: openstudio.openstudiomodel.Model, name=None, north_axis=0):
        bldg = model.getBuilding()
        if name is not None: bldg.setName(name)
        if north_axis != 0: bldg.setNorthAxis(north_axis)
        return bldg

    # Make a Building Story
    @staticmethod
    def building_story(model, name=None, number_of_story: int = None):
        if number_of_story is not None:
            stories = []
            for i in range(number_of_story):
                story = openstudio.openstudiomodel.BuildingStory(model)
                story.setName("Building Story " + str(i+1))
                stories.append(story)
            return stories
        else:
            story = openstudio.openstudiomodel.BuildingStory(model)
            if name is not None: story.setName(name)
            return story

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
            surface_type=None,
            outside_boundary_condition="Surface",
            sun_exposure="Sunexposed",
            wind_exposure="Windexposed",
            construction: openstudio.openstudiomodel.Construction = None,
            space: openstudio.openstudiomodel.Space = None):

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
                # normal = Vector3d(1.0, 0.0, 0.0)
            z_axis = Vector3d(0.0, 0.0, 1.0)

            angle_rad = math.acos(z_axis.dot(normal) / (z_axis.length() * normal.length()))

            if surface_type is None:
                if angle_rad < GeometryTool.roof_threshold:
                    surface.setSurfaceType("RoofCeiling")
                elif GeometryTool.roof_threshold <= angle_rad < math.pi:
                    surface.setSurfaceType("Wall")
                else:
                    surface.setSurfaceType("Floor")

            surface.setOutsideBoundaryCondition(outside_boundary_condition)
            surface.setSunExposure(sun_exposure)
            surface.setWindExposure(wind_exposure)
            if construction is not None: surface.setConstruction(construction)
            if space is not None: surface.setSpace(space)

        else:
            raise ValueError("Not Enough Vertices to Create a Surface")

        return surface

    # Make Subsurface:
    @staticmethod
    def make_fenestration(model, vertices, surface_type="FixedWindow", construction=None, surface=None):

        if len(vertices) != 0 and len(vertices) > 2:
            pt_vec = Point3dVector()
            for i in range(len(vertices)):
                if len(vertices[i]) != 0:
                    pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                    pt_vec.append(pt)

            subsurface = SubSurface(pt_vec, model)

            subsurface.setSubSurfaceType(surface_type)
            if construction is not None: subsurface.setConstruction(construction)
            if surface is not None: subsurface.setSurface(surface)
        else:
            raise ValueError("Not Enough Vertices to Create a Surface")

        return subsurface

    # Create a shading surface:
    @staticmethod
    def make_shading(model, vertices, construction=None, transmittance_schedule=None):
        if len(vertices) != 0 and len(vertices) > 2:
            pt_vec = Point3dVector()
            for i in range(len(vertices)):
                if len(vertices[i]) != 0:
                    pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                    pt_vec.append(pt)

            shading = ShadingSurface(pt_vec, model)
            if construction is not None: shading.setConstruction(construction)
            if transmittance_schedule is not None: shading.setTransmittanceSchedule(transmittance_schedule)

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
    def solve_adjacency(surfaces, adiabatic=False):
        surfaces_adj = []

        if len(surfaces) < 2:
            raise ValueError("Not enough surfaces to solve adjacency")
        else:
            srfs_remain = surfaces
            for srf in surfaces:
                srf_curr = srf
                srfs_remain.remove(srf)
                # First, find normal vector and centroid:
                normal_curr = GeometryTool.newell_method(srf_curr)
                centroid_curr = GeometryTool.centroid(srf_curr)

                for srf_rest in srfs_remain:
                    normal_rest = GeometryTool.newell_method(srf_rest)
                    centroid_rest = GeometryTool.centroid(srf_rest)
                    angle = math.acos(normal_curr.dot(normal_rest) / (normal_curr.length() * normal_rest.length()))
                    dist = GeometryTool.distance(centroid_curr, centroid_rest)

                    if math.fabs(angle - math.pi) < GeometryTool.tolerance and dist < GeometryTool.tolerance:
                        surfaces_adj.append(srf_curr)
                        surfaces_adj.append(srf_rest)
                        srf_curr.setAdjacentSurface(srf_rest)
                        srfs_remain.remove(srf_rest)

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

        # return surfaces_adj
