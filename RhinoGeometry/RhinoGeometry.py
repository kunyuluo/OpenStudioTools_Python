import json
import uuid
import Rhino
import Rhino.Geometry as rg

tolerance = 0.01


def bounding_box(geometry, high_accuracy=False):
    return geometry.GetBoundingBox(high_accuracy)


def get_surface_center(surface):
    domain_u = (surface.GetBoundingBox(False).Max.X - surface.GetBoundingBox(False).Min.X) / 2
    domain_v = (surface.GetBoundingBox(False).Max.Y - surface.GetBoundingBox(False).Min.Y) / 2
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


def intersect_solid(solid, other_solid):
    intersection_exists = False
    temp_brep = solid.Split(other_solid, tolerance)

    if len(temp_brep) != 0:
        solid = rg.Brep.JoinBreps(temp_brep, tolerance)[0]
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


def check_story_validity(breps):
    tolerance = 0.0001
    valid_threshold = 1.0

    # Get bottom position of each brep:
    bottom_z_values = []
    for brep in breps:
        bottom_z = brep.GetBoundingBox(False).Min.Z
        bottom_z_values.append(bottom_z)

    # Get unique values from the value list:
    stories = list(set(bottom_z_values))
    stories.sort()

    # Count number of brep at each vertical position:
    story_count = []
    for story in stories:
        count = 0
        for value in bottom_z_values:
            if abs(value - story) < tolerance:
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

            elif height_below < valid_threshold and height_above >= valid_threshold:

                if story_count[i] >= story_count[i - 1]:
                    valid_stories.append(stories[i])
                    invalid_stories.append(stories[i - 1])
                else:
                    valid_stories.append(stories[i - 1])
                    invalid_stories.append(stories[i])

                if i == len(stories) - 2:
                    valid_stories.append(stories[i + 1])

            elif height_below >= valid_threshold and height_above < valid_threshold:

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
        for brep in breps:
            bottom_z = brep.GetBoundingBox(False).Min.Z
            if abs(bottom_z - value) < tolerance:
                invalid_breps.append(brep)

    return valid_stories, invalid_stories, invalid_breps


def match_story(brep, stories):
    tolerance = 0.5
    bottom_z = brep.GetBoundingBox(False).Min.Z

    for i, value in enumerate(stories, 1):
        if abs(value - bottom_z) < tolerance:
            story = i
            story_z = value
    return story, story_z


def room_dict(breps, ids, apertures=None, default_space_type="Office"):
    rooms = []
    names = []
    stories = []

    # Get all valid stories of the input geometries:
    valid_stories = check_story_validity(breps)[0]

    # Get guid of each input brep:
    if ids is not None and isinstance(ids, list):
        #        sc.doc = Rhino.RhinoDoc.ActiveDoc

        for i, brep in enumerate(breps):
            obj = sc.doc.Objects.Find(ids[i])
            layer_name = sc.doc.Layers[obj.Attributes.LayerIndex].FullPath

            if "::" in layer_name:
                try:
                    name = layer_name.split('::')[2]
                    try:
                        story = int(layer_name.split('::')[1].split("F")[0])
                    except:
                        story = match_story(brep, valid_stories)[0]
                except:
                    name = layer_name.split('::')[1]
                    try:
                        story = int(layer_name.split('::')[0].split("F")[0])
                    except:
                        story = match_story(brep, valid_stories)[0]
            else:
                name = default_space_type
                story = match_story(brep, valid_stories)[0]

            names.append(name)
            stories.append(story)

    # Construct room dictionary for each input brep:
    if breps is not None and isinstance(breps, list):
        for i, brep in enumerate(breps):
            story_z = match_story(brep, valid_stories)[1]
            room_dict = {"space_type": None, "identifier": None, "story": None, "surfaces": None, "subsurfaces": None}

            if len(names) != 0:
                room_dict["space_type"] = names[i]
            else:
                room_dict["space_type"] = default_space_type

            if len(stories) != 0:
                room_dict["story"] = stories[i]

            room_dict["identifier"] = str(uuid.uuid4())

            # Surface:
            faces = []
            surfaces = brep.Surfaces
            for j, surface in enumerate(surfaces):
                surface_dict = {"name": None, "vertices": None}

                srf_vertices = list(surface.ToBrep().Vertices)

                center_z = get_surface_center(surface)[0].Z
                normal_z = get_surface_center(surface)[1].Z
                if abs(center_z - story_z) < 0.0001 and normal_z > 0:
                    srf_vertices.reverse()

                points = []
                for vertice in srf_vertices:
                    point = [vertice.Location.X, vertice.Location.Y, vertice.Location.Z]
                    points.append(point)
                surface_dict["vertices"] = points
                surface_dict["name"] = "surface_{}".format(j + 1)

                faces.append(surface_dict)
            room_dict["surfaces"] = faces

            # SubSurfaces:
            subsurfaces = []
            if apertures is not None:
                for aperture in apertures:
                    subsurface_dict = {"name": None, "vertices": None}
                    srf_vertices = aperture.ToBrep().Vertices

            room_dict["subsurfaces"] = subsurfaces

            rooms.append(room_dict)

    return rooms


def get_current_directory():
    file_path = Rhino.RhinoDoc.ActiveDoc.Path.split('\\')
    del file_path[-1]
    dire_path = ""
    for i in range(len(file_path)):
        item = file_path[i] + "\\"
        dire_path += item
    return dire_path


b_boxes = [bounding_box(brep) for brep in breps]
new_breps = intersect_solids(breps, b_boxes) if len(breps) > 1 else breps
building_dict = {"building_name": None, "number_of_stories": len(check_story_validity(breps)[0]), "rooms": room_dict(new_breps, ids)}

if bldg_name is not None:
    building_dict["building_name"] = bldg_name
else:
    building_dict["building_name"] = "Building"

json_out = json.dumps(building_dict, sort_keys=True, indent=4)

if write_json:
    script_path = get_current_directory()
    if bldg_name is not None:
        path = script_path + "{}.json".format(bldg_name)
    else:
        path = script_path + "Building.json"
    with open(path, "w") as outfile:
        outfile.write(json_out)

