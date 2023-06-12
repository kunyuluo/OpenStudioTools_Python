import openstudio
from Schedules.ScheduleTools import ScheduleTool
from Resources.Helpers import Helper


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
                unit_type = 2
            case 4 | 5 | 6:
                unit_type = 1
            case 7 | 8 | 9:
                unit_type = 15
            case _:
                unit_type = 1

        if constant_value is not None:
            setpoint_schedule = ScheduleTool.schedule_ruleset(model, unit_type, constant_value)
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
            control_variable: int = 1,
            setpoint_at_outdoor_low=None,
            setpoint_at_outdoor_high=None,
            outdoor_low=None,
            outdoor_high=None,
            ashrae_default: int = None):

        """
        -Control_variable: 1:Temperature 2:MaximumTemperature 3:MinimumTemperature \n
        -ASHRAE_default: 1:Cooling 2:Heating
        """

        control_variables = {1: "Temperature", 2: "MaximumTemperature", 3: "MinimumTemperature"}

        manager = openstudio.openstudiomodel.SetpointManagerOutdoorAirReset(model)

        manager.setControlVariable(control_variables[control_variable])

        if ashrae_default is not None:
            match ashrae_default:
                case 1:
                    manager.setSetpointatOutdoorLowTemperature(Helper.f_to_c(54))
                    manager.setSetpointatOutdoorHighTemperature(Helper.f_to_c(44))
                    manager.setOutdoorLowTemperature(Helper.f_to_c(60))
                    manager.setOutdoorHighTemperature(Helper.f_to_c(80))
                case 2 | _:
                    manager.setSetpointatOutdoorLowTemperature(Helper.f_to_c(180))
                    manager.setSetpointatOutdoorHighTemperature(Helper.f_to_c(150))
                    manager.setOutdoorLowTemperature(Helper.f_to_c(20))
                    manager.setOutdoorHighTemperature(Helper.f_to_c(50))
        else:
            if setpoint_at_outdoor_low is not None:
                manager.setSetpointatOutdoorLowTemperature(setpoint_at_outdoor_low)
            if setpoint_at_outdoor_high is not None:
                manager.setSetpointatOutdoorHighTemperature(setpoint_at_outdoor_high)
            if outdoor_low is not None:
                manager.setOutdoorLowTemperature(outdoor_low)
            if outdoor_high is not None:
                manager.setOutdoorHighTemperature(outdoor_high)

        return manager

    @staticmethod
    def follow_outdoor_air_temperature(
            model: openstudio.openstudiomodel.Model,
            control_variable: int = 1,
            reference_temp_type: int = 1,
            offset_temp_diff=None,
            max_setpoint_temp=None,
            min_setpoint_temp=None,
            ashrae_default: bool = False):

        """
        -Control_variable: 1:Temperature 2:MaximumTemperature 3:MinimumTemperature \n
        -Reference_temperature_type: 1:OutdoorAirWetBulb 2:OutdoorAirDryBulb
        """

        control_variables = {1: "Temperature", 2: "MaximumTemperature", 3: "MinimumTemperature"}
        reference_temp_types = {1: "OutdoorAirWetBulb", 2: "OutdoorAirDryBulb"}

        manager = openstudio.openstudiomodel.SetpointManagerFollowOutdoorAirTemperature(model)

        manager.setControlVariable(control_variables[control_variable])

        if ashrae_default:
            manager.setReferenceTemperatureType(reference_temp_types[1])
            manager.setOffsetTemperatureDifference(Helper.delta_temp_f_to_c(5))
            manager.setMaximumSetpointTemperature(Helper.f_to_c(90))
            manager.setMinimumSetpointTemperature(Helper.f_to_c(70))
        else:
            manager.setReferenceTemperatureType(reference_temp_types[reference_temp_type])
            if offset_temp_diff is not None:
                manager.setOffsetTemperatureDifference(offset_temp_diff)
            if max_setpoint_temp is not None:
                manager.setMaximumSetpointTemperature(max_setpoint_temp)
            if min_setpoint_temp is not None:
                manager.setMinimumSetpointTemperature(min_setpoint_temp)

        return manager

    @staticmethod
    def warmest(model: openstudio.openstudiomodel.Model, max_setpoint_temp=None, min_setpoint_temp=None):

        manager = openstudio.openstudiomodel.SetpointManagerWarmest(model)

        if max_setpoint_temp is not None:
            manager.setMaximumSetpointTemperature(max_setpoint_temp)
        if min_setpoint_temp is not None:
            manager.setMinimumSetpointTemperature(min_setpoint_temp)

        return manager

    @staticmethod
    def coldest(model: openstudio.openstudiomodel.Model, max_setpoint_temp=None, min_setpoint_temp=None):

        manager = openstudio.openstudiomodel.SetpointManagerColdest(model)

        if max_setpoint_temp is not None:
            manager.setMaximumSetpointTemperature(max_setpoint_temp)
        if min_setpoint_temp is not None:
            manager.setMinimumSetpointTemperature(min_setpoint_temp)

        return manager
