import openstudio


class SetpointManager:

    @staticmethod
    def scheduled(
            model: openstudio.openstudiomodel.Model,
            control_variable="Temperature",
            schedule: openstudio.openstudiomodel.Schedule = None):
        # Alternatives of control variable:
        # *******************************************************************
        # Temperature
        # MaximumTemperature
        # MinimumTemperature
        # HumidityRatio
        # MaximumHumidityRatio
        # MinimumHumidityRatio
        # MassFlowRate
        # MaximumMassFlowRate
        # MinimumMassFlowRate
        # *******************************************************************
        manager = openstudio.openstudiomodel.SetpointManagerScheduled(model, control_variable, schedule)
        return manager

    @staticmethod
    def outdoor_air_reset(
            model: openstudio.openstudiomodel.Model,
            control_variable=None,
            setpoint_at_outdoor_low=None,
            setpoint_at_outdoor_high=None,
            outdoor_low=None,
            outdoor_high=None,):
        # Alternatives of control variable:
        # *******************************************************************
        # Temperature
        # MaximumTemperature
        # MinimumTemperature
        # *******************************************************************
        manager = openstudio.openstudiomodel.SetpointManagerOutdoorAirReset(model)
        if control_variable is not None:
            manager.setControlVariable(control_variable)
        if setpoint_at_outdoor_low is not None:
            manager.setSetpointatOutdoorLowTemperature(setpoint_at_outdoor_low)
        if setpoint_at_outdoor_high is not None:
            manager.setSetpointatOutdoorHighTemperature(setpoint_at_outdoor_high)
        if outdoor_low is not None:
            manager.setOutdoorLowTemperature(outdoor_low)
        if outdoor_high is not None:
            manager.setOutdoorHighTemperature(outdoor_high)

        return manager
