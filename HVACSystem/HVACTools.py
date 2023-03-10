import openstudio
from PlantLoopComponents import PlantLoopComponent
from SetpointManagers import SetpointManager


class ChilledWaterLoop:

    def __init__(self, model, name=None, condenser_type="WaterCooled", number_of_chillers=1, secondary_pump_system=False):
        self._model = model
        self._name = name
        self._condenser_type = condenser_type
        self._number_of_chillers = number_of_chillers
        self._secondary_pump_system = secondary_pump_system

    def make_loop(self):

        plant = openstudio.openstudiomodel.PlantLoop(self._model)
        if self._name is not None: plant.setName(self._name)

        for i in range(self._number_of_chillers):
            if self._condenser_type == "WaterCooled":
                chiller = PlantLoopComponent.chiller_electric(self._model,condenser_type=self._condenser_type)

        node_supply_out = plant.supplyOutletNode()
        node_supply_in = plant.supplyInletNode()

        return plant
