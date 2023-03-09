import openstudio
from PlantLoopComponents import PlantLoopComponent
from SetpointManagers import SetpointManager


class HVACTool:

    @staticmethod
    def make_chilled_water_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            chillers_electric: openstudio.openstudiomodel.ChillerElectricEIR = None,
            chillers_absorption: openstudio.openstudiomodel.ChillerAbsorption = None):

        plant = openstudio.openstudiomodel.PlantLoop(model)
        if name is not None: plant.setName(name)

        if chillers_electric is not None and len(chillers_electric) != 0:
            for chiller_electric in chillers_electric:
                plant.addSupplyBranchForComponent(chiller_electric)

        if chillers_absorption is not None and len(chillers_absorption) != 0:
            for chiller_absorption in chillers_absorption:
                plant.addSupplyBranchForComponent(chiller_absorption)

        node_supply_out = plant.supplyOutletNode()
        node_supply_in = plant.supplyInletNode()

        return plant
