class EnergyObject:
    def __init__(self, name):
        self._name = name
        self.geometry = self.Geometry()

    # Getter:
    @property
    def name(self):
        return self._name

    # def geometry(self):
    #     return self._geometry

    class Geometry:
        def __init__(self):
            self._geo_type = "geo_type"
            self._plane = "plane"
            self._boundary = "boundary"

        # Getter:
        def geo_type(self):
            return self._geo_type

        def plane(self):
            return self._plane

        def boundary(self):
            return self._boundary


# obj = EnergyObject("model", "nima")
# geo2 = obj.geometry
# print(geo2.geo_type())

