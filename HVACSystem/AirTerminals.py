import openstudio
from Schedules.ScheduleTools import ScheduleTool
from AirLoopComponents import AirLoopComponent


class AirTerminal:

    model_null_message = "Model cannot be empty"
    coil_null_message = "Coil cannot be empty"

    @staticmethod
    def single_duct_constant_volume_no_reheat(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            max_air_flow_rate=None):

        if model is not None:
            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeNoReheat(
                model, ScheduleTool.always_on(model))

            if name is not None:
                terminal.setName(name)

            if max_air_flow_rate is not None:
                terminal.setMaximumAirFlowRate(max_air_flow_rate)
            else:
                terminal.autosizeMaximumAirFlowRate()

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

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

        if model is not None:
            if coil is not None:
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
            else:
                raise ValueError(AirTerminal.coil_null_message)
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_vav_reheat(
            model: openstudio.openstudiomodel.Model,
            coil,
            name: str = None,
            max_air_flow_rate=None,
            min_air_flow_input_method: str = None,
            constant_min_air_flow_fraction=None,
            fixed_min_air_flow_rate=None,
            min_air_flow_fraction_schedule=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None,
            reheat_control_strategy: str = "SingleMaximum",
            damper_heating_action: str = None,
            max_flow_per_area_reheat=None,
            max_flow_fraction_reheat=None,
            max_reheat_air_temp=None,
            control_for_outdoor_air: bool = False,
            min_air_flow_turndown_schedule=None):

        if model is not None:
            if coil is not None:
                terminal_coil = coil
            else:
                terminal_coil = AirLoopComponent.coil_heating_electric(model)

            coil_type = str(type(terminal_coil)).split('.')[-1].split("'")[0]
            if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                terminal = openstudio.openstudiomodel.AirTerminalSingleDuctVAVReheat(model,
                                                                                     ScheduleTool.always_on(model),
                                                                                     terminal_coil)

                if name is not None:
                    terminal.setName(name)

                if max_air_flow_rate is not None:
                    terminal.setMaximumAirFlowRate(max_air_flow_rate)
                else:
                    terminal.autosizeMaximumAirFlowRate()

                if min_air_flow_input_method is not None:
                    terminal.setZoneMinimumAirFlowInputMethod(min_air_flow_input_method)
                if constant_min_air_flow_fraction is not None:
                    terminal.setConstantMinimumAirFlowFraction(constant_min_air_flow_fraction)
                if fixed_min_air_flow_rate is not None:
                    terminal.setFixedMinimumAirFlowRate(fixed_min_air_flow_rate)
                if min_air_flow_fraction_schedule is not None:
                    terminal.setMinimumAirFlowFractionSchedule(min_air_flow_fraction_schedule)

                if max_hot_water_flow_rate is not None:
                    terminal.setMaximumHotWaterOrSteamFlowRate(max_hot_water_flow_rate)
                else:
                    terminal.autosizeMaximumHotWaterOrSteamFlowRate()
                if min_hot_water_flow_rate is not None:
                    terminal.setMinimumHotWaterOrStreamFlowRate(min_hot_water_flow_rate)
                if convergence_tolerance is not None:
                    terminal.setConvergenceTolerance(convergence_tolerance)

                if reheat_control_strategy is not None:
                    if reheat_control_strategy == "SingleMaximum":
                        terminal.setDamperHeatingAction("Normal")
                    elif reheat_control_strategy == "DualMaximum":
                        terminal.setDamperHeatingAction("ReverseWithLimits")
                    else:
                        pass
                else:
                    if damper_heating_action is not None:
                        terminal.setDamperHeatingAction(damper_heating_action)

                if max_flow_per_area_reheat is not None:
                    terminal.setMaximumFlowPerZoneFloorAreaDuringReheat(max_flow_per_area_reheat)
                if max_flow_fraction_reheat is not None:
                    terminal.setMaximumFlowFractionDuringReheat(max_flow_fraction_reheat)
                if max_reheat_air_temp is not None:
                    terminal.setMaximumReheatAirTemperature(max_reheat_air_temp)

                if control_for_outdoor_air is not None:
                    terminal.setControlForOutdoorAir(control_for_outdoor_air)

                if min_air_flow_turndown_schedule is not None:
                    terminal.setMinimumAirFlowTurndownSchedule(min_air_flow_turndown_schedule)

                return terminal
            else:
                raise TypeError("Coil type can only be CoilHeatingWater, CoilHeatingElectric, or CoilHeatingGas")
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_series_piu_reheat(
            model: openstudio.openstudiomodel.Model,
            fan=None,
            coil=None,
            name: str = None,
            max_air_flow_rate=None,
            max_primary_air_flow_rate=None,
            min_primary_air_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None):

        if model is not None:
            if coil is not None and fan is not None:
                terminal_fan = fan
                terminal_coil = coil

            else:
                terminal_coil = AirLoopComponent.coil_heating_electric(model)
                terminal_fan = AirLoopComponent.fan_constant_speed(model)

            coil_type = str(type(terminal_coil)).split('.')[-1].split("'")[0]
            fan_type = str(type(terminal_fan)).split('.')[-1].split("'")[0]

            coil_type_check = coil_type == "CoilHeatingWater" \
                              or coil_type == "CoilHeatingElectric" \
                              or coil_type == "CoilHeatingGas"
            fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"

            if coil_type_check and fan_type_check:
                terminal = openstudio.openstudiomodel.AirTerminalSingleDuctSeriesPIUReheat(model, terminal_fan, terminal_coil)

                if name is not None:
                    terminal.setName(name)

                if max_air_flow_rate is not None:
                    terminal.setMaximumAirFlowRate(max_air_flow_rate)
                else:
                    terminal.autosizeMaximumAirFlowRate()

                if max_primary_air_flow_rate is not None:
                    terminal.setMaximumPrimaryAirFlowRate(max_primary_air_flow_rate)
                else:
                    terminal.autosizeMaximumPrimaryAirFlowRate()
                if min_primary_air_flow_rate is not None:
                    terminal.setMinimumPrimaryAirFlowFraction(min_primary_air_flow_rate)
                else:
                    terminal.autosizeMinimumPrimaryAirFlowFraction()

                if max_hot_water_flow_rate is not None:
                    terminal.setMaximumHotWaterorSteamFlowRate(max_hot_water_flow_rate)
                else:
                    terminal.autosizeMaximumHotWaterorSteamFlowRate()
                if min_hot_water_flow_rate is not None:
                    terminal.setMinimumHotWaterorSteamFlowRate(min_hot_water_flow_rate)
                if convergence_tolerance is not None:
                    terminal.setConvergenceTolerance(convergence_tolerance)

                return terminal
            else:
                if not coil_type_check:
                    raise TypeError(
                        "Coil type can only be CoilHeatingWater, CoilHeatingElectric, or CoilHeatingGas")
                if not fan_type_check:
                    raise TypeError("Fan type can only be FanConstantVolume or FanSystemModel")

        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_parallel_piu_reheat(
            model: openstudio.openstudiomodel.Model,
            fan=None,
            coil=None,
            name: str = None,
            max_primary_air_flow_rate=None,
            max_secondary_air_flow_rate=None,
            min_primary_air_flow_rate=None,
            fan_on_flow_fraction=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None):

        if model is not None:
            if coil is not None and fan is not None:
                terminal_fan = fan
                terminal_coil = coil

            else:
                terminal_coil = AirLoopComponent.coil_heating_electric(model)
                terminal_fan = AirLoopComponent.fan_constant_speed(model)

            coil_type = str(type(terminal_coil)).split('.')[-1].split("'")[0]
            fan_type = str(type(terminal_fan)).split('.')[-1].split("'")[0]

            coil_type_check = coil_type == "CoilHeatingWater" \
                              or coil_type == "CoilHeatingElectric" \
                              or coil_type == "CoilHeatingGas"
            fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"

            if coil_type_check and fan_type_check:
                terminal = openstudio.openstudiomodel.AirTerminalSingleDuctParallelPIUReheat(
                    model,
                    ScheduleTool.always_on(model),
                    terminal_fan,
                    terminal_coil)

                if name is not None:
                    terminal.setName(name)

                if max_primary_air_flow_rate is not None:
                    terminal.setMaximumPrimaryAirFlowRate(max_primary_air_flow_rate)
                else:
                    terminal.autosizeMaximumPrimaryAirFlowRate()

                if max_secondary_air_flow_rate is not None:
                    terminal.setMaximumSecondaryAirFlowRate(max_secondary_air_flow_rate)
                else:
                    terminal.autosizeMaximumSecondaryAirFlowRate()

                if min_primary_air_flow_rate is not None:
                    terminal.setMinimumPrimaryAirFlowFraction(min_primary_air_flow_rate)
                else:
                    terminal.autosizeMinimumPrimaryAirFlowFraction()

                if fan_on_flow_fraction is not None:
                    terminal.setFanOnFlowFraction(fan_on_flow_fraction)
                else:
                    terminal.autosizeFanOnFlowFraction()

                if max_hot_water_flow_rate is not None:
                    terminal.setMaximumHotWaterorSteamFlowRate(max_hot_water_flow_rate)
                else:
                    terminal.autosizeMaximumHotWaterorSteamFlowRate()
                if min_hot_water_flow_rate is not None:
                    terminal.setMinimumHotWaterorSteamFlowRate(min_hot_water_flow_rate)
                if convergence_tolerance is not None:
                    terminal.setConvergenceTolerance(convergence_tolerance)

                return terminal
            else:
                if not coil_type_check:
                    raise TypeError(
                        "Coil type can only be CoilHeatingWater, CoilHeatingElectric, or CoilHeatingGas")
                if not fan_type_check:
                    raise TypeError("Fan type can only be FanConstantVolume or FanSystemModel")

        else:
            raise ValueError(AirTerminal.model_null_message)