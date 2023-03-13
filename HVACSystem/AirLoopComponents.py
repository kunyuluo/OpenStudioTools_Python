import openstudio


class AirLoopComponent:

    @staticmethod
    def air_loop(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            design_air_flow_rate=None,
            design_return_air_flow_fraction=None):

        loop = openstudio.openstudiomodel.AirLoopHVAC(model)
        if name is not None: loop.setName(name)
        if design_air_flow_rate is not None:
            loop.setDesignSupplyAirFlowRate(design_air_flow_rate)
        else:
            loop.autosizeDesignSupplyAirFlowRate()

        if design_return_air_flow_fraction is not None:
            loop.setDesignReturnAirFlowFractionofSupplyAirFlow(design_return_air_flow_fraction)

        supply_inlet_node = loop.supplyInletNode()
        supply_outlet_node = loop.supplyOutletNode()

        # Add outdoor air system to the loop
        controller = openstudio.openstudiomodel.ControllerOutdoorAir(model)
        outdoor_air_system = openstudio.openstudiomodel.AirLoopHVACOutdoorAirSystem(model, controller)
        outdoor_air_system.addToNode(supply_inlet_node)


        return loop
