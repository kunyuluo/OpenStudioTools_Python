import openstudio
from Schedules.ScheduleTools import ScheduleTool


class AirTerminal:

    @staticmethod
    def single_duct_constant_volume_no_reheat(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            max_air_flow_rate=None):

        type_limit = ScheduleTool.schedule_type_limits(model, "Availability", 0, 1)
        schedule = ScheduleTool.schedule_ruleset(model, 1, type_limits=type_limit, name="AlwaysOn")

        terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeNoReheat(model, schedule)

        if name is not None:
            terminal.setName(name)

        if max_air_flow_rate is not None:
            terminal.setMaximumAirFlowRate(max_air_flow_rate)
        else:
            terminal.autosizeMaximumAirFlowRate()

        return terminal

    @staticmethod
    def single_duct_constant_volume_reheat(
            model: openstudio.openstudiomodel.Model,
            coil,
            name: str = None,
            max_air_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None,
            max_reheat_air_temp=None):

        type_limit = ScheduleTool.schedule_type_limits(model, "Availability", 0, 1)
        schedule = ScheduleTool.schedule_ruleset(model, 1, type_limits=type_limit, name="AlwaysOn")

        terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeReheat(model, schedule, coil)

        if name is not None:
            terminal.setName(name)

        if max_air_flow_rate is not None:
            terminal.setMaximumAirFlowRate(max_air_flow_rate)
        else:
            terminal.autosizeMaximumAirFlowRate()

        if max_hot_water_flow_rate is not None:
            terminal.setMaximumHotWaterorSteamFlowRate(max_hot_water_flow_rate)
        else:
            terminal.autosizeMaximumHotWaterorSteamFlowRate()

        if min_hot_water_flow_rate is not None:
            terminal.setMinimumHotWaterorSteamFlowRate(min_hot_water_flow_rate)

        if convergence_tolerance is not None:
            terminal.setConvergenceTolerance(convergence_tolerance)

        if max_reheat_air_temp is not None:
            terminal.setMaximumReheatAirTemperature(max_reheat_air_temp)

        return terminal