import os
import json
import uuid
import math
import rhinoinside
rhinoinside.load()
try:
    import Rhino
except ImportError as e:
    raise ImportError("Failed to import Rhino.\n{}".format(e))

tolerance = 0.01


def modify_rhino_unit(rhino_file_path: str):
    doc = Rhino.RhinoDoc.FromFilePath(rhino_file_path)
    unit = doc.GetUnitSystemName(True, True, True, False)
    # Rhino.RhinoDoc.AdjustModelUnitSystem(model)
    return unit


def sort_geometry_from_rhino(rhino_file_path: str, get_object: bool = False, convert_to_brep: bool = True):
    """
    :param rhino_file_path: full path of the rhino file (3dm).
    :param get_object: if True, rhino objects will be returned.
        Otherwise, the geometries linked with objects will be returned.
    :param convert_to_brep: if True, all geometries will be converted to brep
    :returns tuple( rooms, fenestration, shades, room_layer_names)
    """

    rooms = []
    room_layer_names = []
    fenestration = []
    shades = []

    try:
        model = Rhino.FileIO.File3dm.Read(rhino_file_path)

        for obj in model.Objects:
            layer = model.Layers[obj.Attributes.LayerIndex].FullPath
            geometry = obj.Geometry

            if get_object:
                if "window" in layer.lower():
                    fenestration.append(obj)
                elif "shade" in layer.lower():
                    shades.append(obj)
                else:
                    rooms.append(obj)
                    room_layer_names.append(layer)
            else:
                if "window" in layer.lower():
                    if convert_to_brep:
                        if isinstance(geometry, Rhino.Geometry.Brep):
                            fenestration.append(geometry)
                        else:
                            fenestration.append(geometry.ToBrep())
                    else:
                        fenestration.append(geometry)
                elif "shade" in layer.lower():
                    if convert_to_brep:
                        if isinstance(geometry, Rhino.Geometry.Brep):
                            shades.append(geometry)
                        else:
                            shades.append(geometry.ToBrep())
                    else:
                        shades.append(geometry)
                else:
                    room_layer_names.append(layer)
                    if convert_to_brep:
                        if isinstance(geometry, Rhino.Geometry.Brep):
                            rooms.append(geometry)
                        else:
                            rooms.append(geometry.ToBrep())
                    else:
                        rooms.append(geometry)
    except ValueError:
        print("Unable to read rhino file from given file path.")

    return rooms, fenestration, shades, room_layer_names


def get_geometry(rhino_object):

    if isinstance(rhino_object, Rhino.FileIO.File3dmObject):
        return rhino_object.Geometry
    elif isinstance(rhino_object, list):
        geometries = []
        if len(rhino_object) != 0:
            for obj in rhino_object:
                geometries.append(obj.Geometry)
        return geometries
    else:
        raise TypeError("Invalid input type of the rhino object")


def bounding_box(geometry, high_accuracy=False):
    return geometry.GetBoundingBox(high_accuracy)


def get_surface_center(surface):
    domain_u = (surface.Domain(0).Max + surface.Domain(0).Min) / 2
    domain_v = (surface.Domain(1).Max + surface.Domain(1).Min) / 2
    center = surface.PointAt(domain_u, domain_v)
    normal = surface.NormalAt(domain_u, domain_v)
    return center, normal


def overlapping_bounding_boxes(bound_box1, bound_box2):
    # Bounding box check using the Separating Axis Theorem
    bb1_width = bound_box1.Max.X - bound_box1.Min.X
    bb2_width = bound_box2.Max.X - bound_box2.Min.X
    dist_btwn_x = abs(bound_box1.Center.X - bound_box2.Center.X)
    x_gap_btwn_box = dist_btwn_x - (0.5 * bb1_width) - (0.5 * bb2_width)

    bb1_depth = bound_box1.Max.Y - bound_box1.Min.Y
    bb2_depth = bound_box2.Max.Y - bound_box2.Min.Y
    dist_btwn_y = abs(bound_box1.Center.Y - bound_box2.Center.Y)
    y_gap_btwn_box = dist_btwn_y - (0.5 * bb1_depth) - (0.5 * bb2_depth)

    bb1_height = bound_box1.Max.Z - bound_box1.Min.Z
    bb2_height = bound_box2.Max.Z - bound_box2.Min.Z
    dist_btwn_z = abs(bound_box1.Center.Z - bound_box2.Center.Z)
    z_gap_btwn_box = dist_btwn_z - (0.5 * bb1_height) - (0.5 * bb2_height)

    if x_gap_btwn_box > tolerance or y_gap_btwn_box > tolerance or \
            z_gap_btwn_box > tolerance:
        return False  # no overlap
    return True  # overlap exists


def get_brep_face_vertex(face):
    poly = face.Loops[0].To3dCurve().ToPolyline(0.01, 0.01, 0.01, 100).ToPolyline()
    poly.MergeColinearSegments(0.01, False)
    segments = poly.GetSegments()

    vertices = []
    for segment in segments:
        point = segment.From
        vertices.append(point)

    return vertices


def intersect_solid(solid, other_solid):
    intersection_exists = False
    temp_brep = solid.Split(other_solid, tolerance)

    if len(temp_brep) != 0:
        solid = Rhino.Geometry.Brep.JoinBreps(temp_brep, tolerance)[0]
        solid.Faces.ShrinkFaces()
        intersection_exists = True
    return solid, intersection_exists


def intersect_solids(solids, bound_boxes):
    new_solids = solids[:]

    for i, bb_1 in enumerate(bound_boxes):
        for j, bb_2 in enumerate(bound_boxes[i + 1:]):
            if not overlapping_bounding_boxes(bb_1, bb_2):
                continue  # no overlap in bounding box; intersection impossible

            # split the first solid with the second one
            split_brep1, int_exists = intersect_solid(
                new_solids[i], new_solids[i + j + 1])
            new_solids[i] = split_brep1

            # split the second solid with the first one if an intersection was found
            if int_exists:
                split_brep2, int_exists = intersect_solid(
                    new_solids[i + j + 1], new_solids[i])
                new_solids[i + j + 1] = split_brep2

    return new_solids


def check_story_validity(rooms):
    value_tolerance = 0.0001
    valid_threshold = 1.0

    # Get bottom position of each brep:
    bottom_z_values = []
    for room in rooms:
        bottom_z = room.GetBoundingBox(False).Min.Z
        bottom_z_values.append(bottom_z)

    # Get unique values from the value list:
    stories = list(set(bottom_z_values))
    stories.sort()

    # Count number of brep at each vertical position:
    story_count = []
    for story in stories:
        count = 0
        for value in bottom_z_values:
            if abs(value - story) < value_tolerance:
                count += 1
        story_count.append(count)

    # Check validity of each story based on its value:
    valid_stories = []
    invalid_stories = []
    invalid_breps = []
    if len(stories) == 1:
        valid_stories = stories[:]
    elif len(stories) == 2:
        height = stories[1] - stories[0]
        if height >= valid_threshold:
            valid_stories.append(stories[0])
            valid_stories.append(stories[1])
        else:
            if story_count[0] >= story_count[1]:
                valid_stories.append(stories[0])
                invalid_stories.append(stories[1])
            else:
                valid_stories.append(stories[1])
                invalid_stories.append(stories[0])
    elif len(stories) == 3:
        height_below = stories[1] - stories[0]
        height_above = stories[2] - stories[1]

        if height_below >= valid_threshold and height_above >= valid_threshold:
            valid_stories = stories[:]

        elif height_below < valid_threshold <= height_above:

            if story_count[1] >= story_count[0]:
                valid_stories.append(stories[1])
                invalid_stories.append(stories[0])
            else:
                valid_stories.append(stories[0])
                invalid_stories.append(stories[1])
            valid_stories.append(stories[2])

        elif height_below >= valid_threshold > height_above:
            valid_stories.append(stories[0])
            if story_count[1] >= story_count[2]:
                valid_stories.append(stories[1])
                invalid_stories.append(stories[2])
            else:
                valid_stories.append(stories[2])
                invalid_stories.append(stories[1])

        else:
            counts = [story_count[0], story_count[1], story_count[2]]
            max_count = max(counts)
            max_index = counts.index(max_count)

            if max_index == 0:
                valid_stories.append(stories[0])
                invalid_stories.append(stories[1])
                invalid_stories.append(stories[2])
            elif max_index == 1:
                valid_stories.append(stories[1])
                invalid_stories.append(stories[0])
                invalid_stories.append(stories[2])
            else:
                valid_stories.append(stories[2])
                invalid_stories.append(stories[1])
                invalid_stories.append(stories[0])

    else:
        for i in range(1, len(stories) - 1):
            height_below = stories[i] - stories[i - 1]
            height_above = stories[i + 1] - stories[i]

            if height_below >= valid_threshold and height_above >= valid_threshold:

                if i == 1:
                    valid_stories.append(stories[i - 1])
                    valid_stories.append(stories[i])
                elif i == len(stories) - 2:
                    valid_stories.append(stories[i])
                    valid_stories.append(stories[i + 1])
                else:
                    valid_stories.append(stories[i])

            elif height_below < valid_threshold <= height_above:

                if story_count[i] >= story_count[i - 1]:
                    valid_stories.append(stories[i])
                    invalid_stories.append(stories[i - 1])
                else:
                    valid_stories.append(stories[i - 1])
                    invalid_stories.append(stories[i])

                if i == len(stories) - 2:
                    valid_stories.append(stories[i + 1])

            elif height_below >= valid_threshold > height_above:

                if story_count[i] >= story_count[i + 1]:
                    valid_stories.append(stories[i])
                    invalid_stories.append(stories[i + 1])
                else:
                    valid_stories.append(stories[i + 1])
                    invalid_stories.append(stories[i])

                if i == 1:
                    valid_stories.append(stories[i - 1])

            else:

                counts = [story_count[i - 1], story_count[i], story_count[i + 1]]
                max_count = max(counts)
                max_index = counts.index(max_count)

                if max_index == 0:
                    valid_stories.append(stories[i - 1])
                    invalid_stories.append(stories[i])
                    invalid_stories.append(stories[i + 1])
                elif max_index == 1:
                    valid_stories.append(stories[i])
                    invalid_stories.append(stories[i - 1])
                    invalid_stories.append(stories[i + 1])
                else:
                    valid_stories.append(stories[i + 1])
                    invalid_stories.append(stories[i])
                    invalid_stories.append(stories[i - 1])

    # Get all breps with invalid story height value:
    valid_stories = list(set(valid_stories))
    valid_stories.sort()
    invalid_stories = list(set(invalid_stories))
    for value in invalid_stories:
        for room in rooms:
            bottom_z = room.GetBoundingBox(False).Min.Z
            if abs(bottom_z - value) < tolerance:
                invalid_breps.append(room)

    return valid_stories, invalid_stories, invalid_breps


def match_story(brep, stories):
    height_tolerance = 0.5
    bottom_z = brep.GetBoundingBox(False).Min.Z

    story_index = 0
    story_z = 0
    for i, value in enumerate(stories, 1):
        if abs(value - bottom_z) < height_tolerance:
            story_index = i
            story_z = value
    return story_index, story_z


def find_child_surface(surface, sub_surfaces):
    children = []
    if isinstance(sub_surfaces, list):
        for subsurface in sub_surfaces:
            if isinstance(subsurface, Rhino.Geometry.Brep):
                curves = Rhino.Geometry.Intersect.Intersection.BrepSurface(subsurface, surface, tolerance)[1]
            elif isinstance(subsurface, Rhino.Geometry.Surface):
                curves = Rhino.Geometry.Intersect.Intersection.SurfaceSurface(subsurface, surface, tolerance)[1]
            else:
                curves = Rhino.Geometry.Intersect.Intersection.BrepBrep(
                    subsurface.ToBrep(), surface.ToBrep(), tolerance)[1]

            try:
                if len(curves) > 1:
                    children.append(subsurface)
            except ValueError:
                if len(curves) > 0:
                    children.append(subsurface)

        return children
    else:
        raise TypeError("Invalid input type of sub-surfaces. It should be a list")


def shades_dict(geometries):
    shades = []
    if len(geometries) != 0:
        for i, geometry in enumerate(geometries, 1):
            faces = geometry.Faces
            for j, face in enumerate(faces, 1):
                surface_dict = {"name": None, "vertices": None}

                srf_vertices = get_brep_face_vertex(face)

                # Shade geometry:
                points = []
                for vertex in srf_vertices:
                    point = [vertex.X, vertex.Y, vertex.Z]
                    points.append(point)
                surface_dict["vertices"] = points
                surface_dict["name"] = "surface_{}_{}".format(i, j)

                shades.append(surface_dict)
    return shades


def rooms_dict(solids=None, solid_names=None, apertures=None, default_space_type="Office"):
    rooms = []
    names = []
    stories = []

    if solids is not None and len(solids) != 0:
        # Convert object to brep geometry:
        # solids = get_geometry(room_objects)

        # Get all valid stories of the input geometries:
        valid_stories = check_story_validity(solids)[0]

        if solid_names is not None and len(solid_names) == len(solids):

            for i, brep in enumerate(solids):
                layer_name = solid_names[i]

                if "::" in layer_name:
                    try:
                        name = layer_name.split('::')[2]
                        try:
                            story = int(layer_name.split('::')[1].split("F")[0])
                        except ValueError:
                            story = match_story(brep, valid_stories)[0]
                    except IndexError:
                        name = layer_name.split('::')[1]
                        try:
                            story = int(layer_name.split('::')[0].split("F")[0])
                        except ValueError:
                            story = match_story(brep, valid_stories)[0]
                else:
                    name = default_space_type
                    story = match_story(brep, valid_stories)[0]

                names.append(name)
                stories.append(story)

                # Construct room dictionary for each input brep:
                story_z = match_story(brep, valid_stories)[1]
                room_dict = {"name": name, "space_type": None, "identifier": None, "story": None, "surfaces": None}

                if len(names) != 0:
                    room_dict["space_type"] = names[i]
                else:
                    room_dict["space_type"] = default_space_type

                if len(stories) != 0:
                    room_dict["story"] = stories[i]

                room_dict["identifier"] = str(uuid.uuid4())

                # Surface:
                surfaces = []
                faces = brep.Faces
                for j, face in enumerate(faces, 1):
                    surface_dict = {"name": None, "normal": None, "vertices": None, "fenestrations": None}

                    srf_vertices = get_brep_face_vertex(face)

                    # Flip floor surface if needed:
                    center_z = get_surface_center(face)[0].Z
                    normal = get_surface_center(face)[1]
                    normal_z = get_surface_center(face)[1].Z
                    if abs(center_z - story_z) < 0.0001 and normal_z > 0:
                        srf_vertices.reverse()
                        normal.Reverse()

                    surface_dict["normal"] = [normal.X, normal.Y, normal.Z]

                    # Wall geometry:
                    points = []
                    for vertice in srf_vertices:
                        point = [vertice.X, vertice.Y, vertice.Z]
                        points.append(point)
                    surface_dict["vertices"] = points
                    surface_dict["name"] = "surface_{}".format(j)

                    surfaces.append(surface_dict)

                    # Fenstration geometry:
                    fenestrations = []
                    try:
                        children = find_child_surface(face, apertures)
                        if len(children) != 0:
                            for k, child in enumerate(children, 1):
                                fenestration = {"name": None, "normal": None, "vertices": None}

                                srf_vertices = get_brep_face_vertex(child.Faces[0])

                                # Flip fenestration surface if needed (based on parent surface normal direction):
                                fen_normal = get_surface_center(child.Faces[0])[1]
                                angle = Rhino.Geometry.Vector3d.VectorAngle(normal, fen_normal)
                                if abs(angle - math.pi) < tolerance:
                                    srf_vertices.reverse()
                                    fen_normal.Reverse()

                                fenestration["normal"] = [fen_normal.X, fen_normal.Y, fen_normal.Z]

                                points = []
                                for vertice in srf_vertices:
                                    point = [vertice.X, vertice.Y, vertice.Z]
                                    points.append(point)
                                fenestration["vertices"] = points
                                fenestration["name"] = "surface_{}_window_{}".format(j, k)
                                fenestrations.append(fenestration)

                    except ValueError:
                        pass
                    surface_dict["fenestrations"] = fenestrations

                room_dict["surfaces"] = surfaces

                rooms.append(room_dict)

    return rooms


def building_dict(room_geos=None, solid_names=None, fenestration_geos=None, shade_geos=None, name: str = None):

    building = {"building_name": None, "number_of_stories": None, "rooms": [], "shades": None}

    if room_geos is not None:
        b_boxes = [bounding_box(room) for room in room_geos]
        new_room_geos = intersect_solids(room_geos, b_boxes) if len(room_geos) > 1 else room_geos

        building["number_of_stories"] = len(check_story_validity(room_geos)[0])
        building["rooms"] = rooms_dict(new_room_geos, solid_names, fenestration_geos)

    if shade_geos is not None:
        building["shades"] = shades_dict(shade_geos)

    if name is not None:
        building["building_name"] = name
    else:
        building["building_name"] = "Building"

    json_out = json.dumps(building, sort_keys=True, indent=4)

    return json_out


def write_to_json(json_out=None):
    dir_path = os.path.dirname(__file__)
    try:
        building = json.loads(json_out)
        file_name = building["building_name"]
        file_path = dir_path + "\\{}.json".format(file_name)
    except ValueError:
        file_path = dir_path + "\\Building.json"

    try:
        with open(file_path, "w") as outfile:
            outfile.write(json_out)
        return file_path
    except ValueError:
        print("Cannot write to json file")


def load_rhino_model(rhino_file_path: str, building_name: str = "Building"):
    all_geos = sort_geometry_from_rhino(rhino_file_path)

    rooms = all_geos[0]
    room_names = all_geos[3]
    windows = all_geos[1]
    shades = all_geos[2]

    building = building_dict(rooms, room_names, windows, shades, building_name)
    json_path = write_to_json(building)

    return json_path
