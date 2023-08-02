import os
import numpy as np
from Resources.EPW_Parse import Location, GroundTemperature


class EPW:
    def __init__(
            self,
            location: Location = None,
            ground_temp: GroundTemperature = None):
        self._location = location
        self._ground_temp = ground_temp
