import openstudio
from ConstructionTools import ConstructionTool


class ConstructionSet:

    _exterior_wall = None
    _exterior_roof = None
    _exterior_floor = None
    _exterior_window = None
    _interior_wall = None
    _interior_floor = None
    _interior_ceiling = None
    _interior_window = None
    _underground_wall = None
    _underground_floor = None
    _underground_ceiling = None

    def __init__(self, model: openstudio.openstudiomodel.Model):
        self._model = model

    def exterior_wall(self):
        cons = ConstructionTool.opaque_no_mass_cons(self._model, "R-10 Wall", 10.0)
        self._exterior_wall = cons
        return self._exterior_wall
