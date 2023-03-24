import openstudio
from Constructions.ConstructionTools import ConstructionTool


class ConstructionSet:
    _construction_set = None

    def __init__(self, model: openstudio.openstudiomodel.Model, name=None):
        self._model = model
        self._name = name

    def get(self):
        cons_set = openstudio.openstudiomodel.DefaultConstructionSet(self._model)
        if self._name is not None: cons_set.setName(self._name)

        # Exterior Surfaces:
        # *******************************************************************************************************
        exterior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(self._model)
        # Wall:
        # ***************************************************************************************
        exterior_wall_cons = ConstructionTool.construction(self._model, "My Exterior Wall")
        exterior_wall_mat_vec = openstudio.openstudiomodel.MaterialVector()

        exterior_wall_mat1 = ConstructionTool.opaque_standard_material(self._model, "M01 100mm brick", 0.1016, 0.89,
                                                                       1920, 790, "MediumRough")
        exterior_wall_mat_vec.append(exterior_wall_mat1)
        exterior_wall_mat2 = ConstructionTool.opaque_standard_material(self._model, "M15 200mm heavyweight concrete",
                                                                       0.2032, 1.95, 2240, 900, "MediumRough")
        exterior_wall_mat_vec.append(exterior_wall_mat2)
        exterior_wall_mat3 = ConstructionTool.opaque_standard_material(self._model, "I02 50mm insulation board",
                                                                       0.0508, 0.03, 43, 1210, "MediumRough")
        exterior_wall_mat_vec.append(exterior_wall_mat3)
        exterior_wall_mat4 = ConstructionTool.air_gap(self._model, "Air Gap", 0.15)
        exterior_wall_mat_vec.append(exterior_wall_mat4)
        exterior_wall_mat5 = ConstructionTool.opaque_standard_material(self._model, "G01a 19mm gypsum board", 0.019,
                                                                       0.16, 800, 1090, "MediumRough")
        exterior_wall_mat_vec.append(exterior_wall_mat5)

        exterior_wall_cons.setLayers(exterior_wall_mat_vec)
        exterior_surfaces.setWallConstruction(exterior_wall_cons)

        # Roof:
        # ***************************************************************************************
        exterior_roof_cons = ConstructionTool.construction(self._model, "My Exterior Roof")
        exterior_roof_mat_vec = openstudio.openstudiomodel.MaterialVector()

        exterior_roof_mat1 = ConstructionTool.opaque_standard_material(self._model, "M11 100mm lightweight concrete",
                                                                       0.1016, 0.53, 1280, 840, "MediumRough", 0.9, 0.5,
                                                                       0.5)
        exterior_roof_mat_vec.append(exterior_roof_mat1)
        exterior_roof_mat_vec.append(exterior_wall_mat4)
        exterior_roof_mat2 = ConstructionTool.opaque_standard_material(self._model, "F16 Acoustic tile", 0.0191,
                                                                       0.06, 368, 590, "MediumSmooth", 0.9, 0.3, 0.3)
        exterior_roof_mat_vec.append(exterior_roof_mat2)

        exterior_roof_cons.setLayers(exterior_roof_mat_vec)
        exterior_surfaces.setRoofCeilingConstruction(exterior_roof_cons)

        # Floor:
        # ***************************************************************************************
        exterior_floor_cons = ConstructionTool.construction(self._model, "Exterior Floor")
        exterior_floor_mat_vec = openstudio.openstudiomodel.MaterialVector()

        exterior_floor_mat1 = ConstructionTool.opaque_standard_material(self._model, "MAT-CC05 4 HW CONCRETE", 0.1016,
                                                                        1.311, 2240, 836.8, "Rough", 0.9, 0.85, 0.85)
        exterior_floor_mat_vec.append(exterior_floor_mat1)
        exterior_floor_mat2 = ConstructionTool.opaque_no_mass_material(self._model, "CP02 CARPET PAD", 0.1, "Smooth",
                                                                       0.9, 0.8, 0.8)
        exterior_floor_mat_vec.append(exterior_floor_mat2)

        exterior_floor_cons.setLayers(exterior_floor_mat_vec)
        exterior_surfaces.setFloorConstruction(exterior_floor_cons)

        cons_set.setDefaultExteriorSurfaceConstructions(exterior_surfaces)

        # Interior Surfaces:
        # *******************************************************************************************************
        interior_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(self._model)
        # Wall:
        # ***************************************************************************************
        interior_wall_cons = ConstructionTool.construction(self._model, "Interior Wall")
        interior_wall_mat_vec = openstudio.openstudiomodel.MaterialVector()

        interior_wall_mat_vec.append(exterior_wall_mat5)
        interior_wall_mat_vec.append(exterior_wall_mat4)
        interior_wall_mat_vec.append(exterior_wall_mat5)

        interior_wall_cons.setLayers(interior_wall_mat_vec)
        interior_surfaces.setWallConstruction(interior_wall_cons)

        # Ceiling:
        # ***************************************************************************************
        interior_roof_cons = ConstructionTool.construction(self._model, "My Interior Roof")
        interior_roof_mat_vec = openstudio.openstudiomodel.MaterialVector()

        interior_roof_mat_vec.append(exterior_roof_mat1)
        interior_roof_mat_vec.append(exterior_wall_mat4)
        interior_roof_mat_vec.append(exterior_roof_mat2)

        interior_roof_cons.setLayers(interior_roof_mat_vec)
        interior_surfaces.setRoofCeilingConstruction(interior_roof_cons)

        # Floor:
        # ***************************************************************************************
        interior_floor_cons = ConstructionTool.construction(self._model, "Interior Floor")
        interior_floor_mat_vec = openstudio.openstudiomodel.MaterialVector()

        interior_floor_mat_vec.append(exterior_roof_mat2)
        interior_floor_mat_vec.append(exterior_wall_mat4)
        interior_floor_mat_vec.append(exterior_roof_mat1)

        interior_floor_cons.setLayers(interior_floor_mat_vec)
        interior_surfaces.setFloorConstruction(interior_floor_cons)

        cons_set.setDefaultInteriorSurfaceConstructions(interior_surfaces)

        # Exterior SubSurfaces:
        # *******************************************************************************************************
        exterior_subsurfaces = openstudio.openstudiomodel.DefaultSubSurfaceConstructions(self._model)
        # Operable window:
        # ***************************************************************************************
        exterior_window_cons = ConstructionTool.construction(self._model, "Exterior Window")
        exterior_window_mat_vec = openstudio.openstudiomodel.MaterialVector()

        exterior_window_mat1 = ConstructionTool.glazing_material(self._model, "Theoretical Glass")
        exterior_window_mat_vec.append(exterior_window_mat1)

        exterior_window_cons.setLayers(exterior_floor_mat_vec)
        exterior_subsurfaces.setOperableWindowConstruction(exterior_window_cons)
        exterior_subsurfaces.setFixedWindowConstruction(exterior_window_cons)

        cons_set.setDefaultExteriorSubSurfaceConstructions(exterior_subsurfaces)

        # Ground Surfaces:
        # *******************************************************************************************************
        ground_surfaces = openstudio.openstudiomodel.DefaultSurfaceConstructions(self._model)
        # Wall:
        # ***************************************************************************************
        ground_wall_cons = ConstructionTool.construction(self._model, "Underground Wall")

        ground_wall_cons.setLayers(exterior_wall_mat_vec)
        ground_surfaces.setWallConstruction(ground_wall_cons)

        # Ceiling:
        # ***************************************************************************************
        ground_surfaces.setRoofCeilingConstruction(exterior_roof_cons)

        # Floor:
        # ***************************************************************************************
        ground_floor_cons = ConstructionTool.construction(self._model, "Slab On Ground")
        ground_floor_cons.setLayers(exterior_floor_mat_vec)
        ground_surfaces.setFloorConstruction(ground_floor_cons)

        cons_set.setDefaultGroundContactSurfaceConstructions(ground_surfaces)

        # Output:
        # *******************************************************************************************************
        self._construction_set = cons_set
        return self._construction_set
