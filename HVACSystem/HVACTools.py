import openstudio


class HVACTool:

    @staticmethod
    def plant_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None):

        plant = openstudio.openstudiomodel.PlantLoop(model)
        if name is not None: plant.setName(name)

        node_supply_out = plant.supplyOutletNode()
        node_supply_in = plant.supplyInletNode()

        return plant

    @staticmethod
    def chiller_electric(
            model: openstudio.openstudiomodel.Model,
            cop=5.5):
        chiller = openstudio.openstudiomodel.ChillerElectricEIR(model)
        chiller.setReferenceCOP(cop)
        
        return chiller

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
