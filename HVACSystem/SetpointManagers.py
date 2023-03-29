import openstudio
from Schedules.ScheduleTools import ScheduleTool


class SetpointManager:

    @staticmethod
    def scheduled(
            model: openstudio.openstudiomodel.Model,
            control_variable: int = 1,
            constant_value=None,
            schedule: openstudio.openstudiomodel.Schedule = None):

        """
        -Control variable:
        1.Temperature
        2.MaximumTemperature
        3.MinimumTemperature
        4.HumidityRatio
        5.MaximumHumidityRatio
        6.MinimumHumidityRatio
        7.MassFlowRate
        8.MaximumMassFlowRate
        9.MinimumMassFlowRate
        """

        control_variables = {1: "Temperature", 2: "MaximumTemperature", 3: "MinimumTemperature",
                             4: "HumidityRatio", 5: "MaximumHumidityRatio", 6: "MinimumHumidityRatio",
                             7: "MassFlowRate", 8: "MaximumMassFlowRate", 9: "MinimumMassFlowRate"}

        match control_variable:
            case 1 | 2 | 3:
                type_limits = ScheduleTool.schedule_type_limits(model, 2, 1, 0, 100)
            case 4 | 5 | 6:
                type_limits = ScheduleTool.schedule_type_limits(model, 1, 1, 0, 10)
            case 7 | 8 | 9:
                type_limits = ScheduleTool.schedule_type_limits(model, 15, 1, 0, 100)
            case _:
                type_limits = ScheduleTool.schedule_type_limits(model, 1, 1, 0, 1)

        if constant_value is not None:
            setpoint_schedule = ScheduleTool.schedule_ruleset(model, constant_value, type_limits)
        else:
            if schedule is not None:
                setpoint_schedule = schedule
            else:
                raise ValueError("Specify either constant value or a schedule")

        manager = openstudio.openstudiomodel.SetpointManagerScheduled(
            model, control_variables[control_variable], setpoint_schedule)

        return manager

    @staticmethod
    def outdoor_air_reset(
            model: openstudio.openstudiomodel.Model,
            control_variable=None,
            setpoint_at_outdoor_low=None,
            setpoint_at_outdoor_high=None,
            outdoor_low=None,
            outdoor_high=None, ):
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
