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
    def building(model, name=None, northAxis=0):
        bldg = model.getBuilding()
        if name is not None: bldg.setNmae(name)
        if northAxis != 0: bldg.setNorthAxis(northAxis)

    # Make a Building Story
    @staticmethod
    def building_story(model, name=None):
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
            model,
            vertices,
            normal=None,
            surface_type=None,
            outside_boundary_condition="Surface",
            sun_exposure="Sunexposed",
            wind_exposure="Windexposed",
            construction_base=None,
            space=None):

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
            if construction_base is not None: surface.setConstruction(construction_base)
            if space is not None: surface.setSpace(space)

        else:
            raise ValueError("Not Enough Vertices to Create a Surface")

        return surface

    # Make Subsurface:
    @staticmethod
    def make_fenestration(model, vertices, surface_type="FixedWindow", construction_base=None, surface=None):

        if len(vertices) != 0 and len(vertices) > 2:
            pt_vec = Point3dVector()
            for i in range(len(vertices)):
                if len(vertices[i]) != 0:
                    pt = Point3d(vertices[i][0], vertices[i][1], vertices[i][2])
                    pt_vec.append(pt)

            subsurface = SubSurface(pt_vec, model)

            subsurface.setSubSurfaceType(surface_type)
            if construction_base is not None: subsurface.setConstruction(construction_base)
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
