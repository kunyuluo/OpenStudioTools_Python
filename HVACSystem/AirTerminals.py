import openstudio
from Schedules.ScheduleTools import ScheduleTool
from HVACSystem.AirLoopComponents import AirLoopComponent


class AirTerminal:

    model_null_message = "Model cannot be empty"

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
            coil=None,
            reheat_coil_type: str = None,
            name: str = None,
            max_air_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None,
            max_reheat_air_temp=None):

        """
        -Reheat_coil_type:  \n
        1.Water 2.Gas 3.Electric
        """

        if model is not None:
            if coil is not None:
                coil_type = str(type(coil)).split('.')[-1].split("'")[0]
                if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                    reheat_coil = coil
                else:
                    match reheat_coil_type:
                        case "Water":
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                        case "Gas":
                            reheat_coil = AirLoopComponent.coil_heating_gas(model)
                        case "Electric" | _:
                            reheat_coil = AirLoopComponent.coil_heating_electric(model)
            else:
                match reheat_coil_type:
                    case "Water":
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                    case "Gas":
                        reheat_coil = AirLoopComponent.coil_heating_gas(model)
                    case "Electric" | _:
                        reheat_coil = AirLoopComponent.coil_heating_electric(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeReheat(
                model, ScheduleTool.always_on(model), reheat_coil)

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
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_vav_no_reheat(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            max_air_flow_rate=None,
            min_air_flow_input_method: str = None,
            constant_min_air_flow_fraction=None,
            fixed_min_air_flow_rate=None,
            min_air_flow_fraction_schedule=None,
            control_for_outdoor_air: bool = False,
            min_air_flow_turndown_schedule=None):

        """
        -Zone minimum Air Flow Input Method: \n
        1.Constant \n
        2.FixedFlowRate \n
        3.Scheduled
        """

        if model is not None:

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctVAVNoReheat(model, ScheduleTool.always_on(model))

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

            if control_for_outdoor_air is not None:
                terminal.setControlForOutdoorAir(control_for_outdoor_air)

            if min_air_flow_turndown_schedule is not None:
                terminal.setMinimumAirFlowTurndownSchedule(min_air_flow_turndown_schedule)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_vav_reheat(
            model: openstudio.openstudiomodel.Model,
            coil=None,
            reheat_coil_type: str = None,
            name: str = None,
            max_air_flow_rate=None,
            min_air_flow_input_method: str = None,
            constant_min_air_flow_fraction=None,
            fixed_min_air_flow_rate=None,
            min_air_flow_fraction_schedule=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None,
            reheat_control_strategy: int = 1,
            damper_heating_action: str = None,
            max_flow_per_area_reheat=None,
            max_flow_fraction_reheat=None,
            max_reheat_air_temp=None,
            control_for_outdoor_air: bool = False,
            min_air_flow_turndown_schedule=None):

        """
        -Zone minimum Air Flow Input Method: \n
        1.Constant \n
        2.FixedFlowRate \n
        3.Scheduled \n

        -Reheat_coil_type:  \n
        1.Water 2.Gas 3.Electric \n

        -Reheat_control_strategy:  \n
        1.SingleMaximum 2.DualMaximum
        """

        if model is not None:

            if coil is not None:
                coil_type = str(type(coil)).split('.')[-1].split("'")[0]
                if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                    reheat_coil = coil
                else:
                    match reheat_coil_type:
                        case "Water":
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                        case "Gas":
                            reheat_coil = AirLoopComponent.coil_heating_gas(model)
                        case "Electric" | _:
                            reheat_coil = AirLoopComponent.coil_heating_electric(model)
            else:
                match reheat_coil_type:
                    case "Water":
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                    case "Gas":
                        reheat_coil = AirLoopComponent.coil_heating_gas(model)
                    case "Electric" | _:
                        reheat_coil = AirLoopComponent.coil_heating_electric(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctVAVReheat(
                model, ScheduleTool.always_on(model), reheat_coil)

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
                if reheat_control_strategy == 1:
                    terminal.setDamperHeatingAction("Normal")
                elif reheat_control_strategy == 2:
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
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_vav_heat_and_cool_no_reheat(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            max_air_flow_rate=None,
            min_air_flow_fraction=None,
            min_air_flow_turndown_schedule=None):

        if model is not None:

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctVAVHeatAndCoolNoReheat(model)

            if name is not None:
                terminal.setName(name)

            if max_air_flow_rate is not None:
                terminal.setMaximumAirFlowRate(max_air_flow_rate)
            else:
                terminal.autosizeMaximumAirFlowRate()

            if min_air_flow_fraction is not None:
                terminal.setZoneMinimumAirFlowFraction(min_air_flow_fraction)

            if min_air_flow_turndown_schedule is not None:
                terminal.setMinimumAirFlowTurndownSchedule(min_air_flow_turndown_schedule)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_vav_heat_and_cool_reheat(
            model: openstudio.openstudiomodel.Model,
            reheat_coil_type: str = None,
            coil=None,
            name: str = None,
            max_air_flow_rate=None,
            min_air_flow_fraction=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None,
            max_reheat_air_temp=None,
            min_air_flow_turndown_schedule=None):

        """
        -Reheat_coil_type:  \n
        1.Water 2.Gas 3.Electric
        """

        if model is not None:

            if coil is not None:
                coil_type = str(type(coil)).split('.')[-1].split("'")[0]
                if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                    reheat_coil = coil
                else:
                    match reheat_coil_type:
                        case "Water":
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                        case "Gas":
                            reheat_coil = AirLoopComponent.coil_heating_gas(model)
                        case "Electric" | _:
                            reheat_coil = AirLoopComponent.coil_heating_electric(model)
            else:
                match reheat_coil_type:
                    case "Water":
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                    case "Gas":
                        reheat_coil = AirLoopComponent.coil_heating_gas(model)
                    case "Electric" | _:
                        reheat_coil = AirLoopComponent.coil_heating_electric(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctVAVHeatAndCoolReheat(model, reheat_coil)

            if name is not None:
                terminal.setName(name)

            if max_air_flow_rate is not None:
                terminal.setMaximumAirFlowRate(max_air_flow_rate)
            else:
                terminal.autosizeMaximumAirFlowRate()

            if min_air_flow_fraction is not None:
                terminal.setZoneMinimumAirFlowFraction(min_air_flow_fraction)

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

            if min_air_flow_turndown_schedule is not None:
                terminal.setMinimumAirFlowTurndownSchedule(min_air_flow_turndown_schedule)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_series_piu_reheat(
            model: openstudio.openstudiomodel.Model,
            reheat_coil_type: str = None,
            fan=None,
            coil=None,
            name: str = None,
            max_air_flow_rate=None,
            max_primary_air_flow_rate=None,
            min_primary_air_flow_rate=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            convergence_tolerance=None):

        """
        -Reheat_coil_type:  \n
        1.Water 2.Gas 3.Electric
        """

        if model is not None:
            if coil is not None:
                coil_type = str(type(coil)).split('.')[-1].split("'")[0]
                if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                    reheat_coil = coil
                else:
                    match reheat_coil_type:
                        case "Water":
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                        case "Gas":
                            reheat_coil = AirLoopComponent.coil_heating_gas(model)
                        case "Electric" | _:
                            reheat_coil = AirLoopComponent.coil_heating_electric(model)
            else:
                match reheat_coil_type:
                    case "Water":
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                    case "Gas":
                        reheat_coil = AirLoopComponent.coil_heating_gas(model)
                    case "Electric" | _:
                        reheat_coil = AirLoopComponent.coil_heating_electric(model)

            if fan is not None:
                fan_type = str(type(fan)).split('.')[-1].split("'")[0]
                fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"
                if fan_type_check:
                    terminal_fan = fan
                else:
                    terminal_fan = AirLoopComponent.fan_constant_speed(model)
            else:
                terminal_fan = AirLoopComponent.fan_constant_speed(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctSeriesPIUReheat(model, terminal_fan, reheat_coil)

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
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_parallel_piu_reheat(
            model: openstudio.openstudiomodel.Model,
            reheat_coil_type: str = None,
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

        """
        -Reheat_coil_type:  \n
        1.Water 2.Gas 3.Electric
        """

        if model is not None:
            if coil is not None:
                coil_type = str(type(coil)).split('.')[-1].split("'")[0]
                if coil_type == "CoilHeatingWater" or coil_type == "CoilHeatingElectric" or coil_type == "CoilHeatingGas":
                    reheat_coil = coil
                else:
                    match reheat_coil_type:
                        case "Water":
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                        case "Gas":
                            reheat_coil = AirLoopComponent.coil_heating_gas(model)
                        case "Electric" | _:
                            reheat_coil = AirLoopComponent.coil_heating_electric(model)
            else:
                match reheat_coil_type:
                    case "Water":
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                    case "Gas":
                        reheat_coil = AirLoopComponent.coil_heating_gas(model)
                    case "Electric" | _:
                        reheat_coil = AirLoopComponent.coil_heating_electric(model)

            if fan is not None:
                fan_type = str(type(fan)).split('.')[-1].split("'")[0]
                fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"
                if fan_type_check:
                    terminal_fan = fan
                else:
                    terminal_fan = AirLoopComponent.fan_constant_speed(model)
            else:
                terminal_fan = AirLoopComponent.fan_constant_speed(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctParallelPIUReheat(
                model, ScheduleTool.always_on(model), terminal_fan, reheat_coil)

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
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_constant_volume_four_pipe_induction(
            model: openstudio.openstudiomodel.Model,
            need_cool_coil: bool = False,
            heat_coil=None,
            cool_coil=None,
            name: str = None,
            max_air_flow_rate=None,
            induction_ratio=None,
            max_hot_water_flow_rate=None,
            min_hot_water_flow_rate=None,
            max_cold_water_flow_rate=None,
            min_cold_water_flow_rate=None,
            heating_convergence_tolerance=None,
            cooling_convergence_tolerance=None):

        if model is not None:
            # Check validity of the heating coil:
            if heat_coil is not None:
                heat_coil_type = str(type(heat_coil)).split('.')[-1].split("'")[0]
                if heat_coil_type == "CoilHeatingWater":
                    terminal_heat_coil = heat_coil
                else:
                    print("This type of heating coil is not valid for this terminal")
                    terminal_heat_coil = AirLoopComponent.coil_heating_water(model)
            else:
                terminal_heat_coil = AirLoopComponent.coil_cooling_water(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeFourPipeInduction(
                model, terminal_heat_coil)

            # Add cooling coil if needed:
            if need_cool_coil:
                if cool_coil is not None:
                    cool_coil_type = str(type(cool_coil)).split('.')[-1].split("'")[0]
                    if cool_coil_type == "CoilCoolingWater":
                        terminal_cool_coil = cool_coil
                    else:
                        print("This type of cooling coil is not valid for this terminal")
                        terminal_cool_coil = AirLoopComponent.coil_cooling_water(model)
                else:
                    terminal_cool_coil = AirLoopComponent.coil_cooling_water(model)

                terminal.setCoolingCoil(terminal_cool_coil)

            if name is not None:
                terminal.setName(name)

            if max_air_flow_rate is not None:
                terminal.setMaximumTotalAirFlowRate(max_air_flow_rate)
            else:
                terminal.autosizeMaximumTotalAirFlowRate()

            if induction_ratio is not None:
                terminal.setInductionRatio(induction_ratio)

            if max_hot_water_flow_rate is not None:
                terminal.setMaximumHotWaterFlowRate(max_hot_water_flow_rate)
            else:
                terminal.autosizeMaximumHotWaterFlowRate()
            if min_hot_water_flow_rate is not None:
                terminal.setMinimumHotWaterFlowRate(min_hot_water_flow_rate)
            if heating_convergence_tolerance is not None:
                terminal.setHeatingConvergenceTolerance(heating_convergence_tolerance)

            if max_cold_water_flow_rate is not None:
                terminal.setMaximumColdWaterFlowRate(max_cold_water_flow_rate)
            else:
                terminal.autosizeMaximumColdWaterFlowRate()
            if min_cold_water_flow_rate is not None:
                terminal.setMinimumColdWaterFlowRate(min_cold_water_flow_rate)
            if cooling_convergence_tolerance is not None:
                terminal.setCoolingConvergenceTolerance(cooling_convergence_tolerance)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_constant_volume_four_pipe_beam(
            model: openstudio.openstudiomodel.Model,
            heat_coil: openstudio.openstudiomodel.CoilHeatingFourPipeBeam = None,
            cool_coil: openstudio.openstudiomodel.CoilCoolingFourPipeBeam = None,
            name: str = None,
            primary_air_availability_schedule=None,
            cooling_availability_schedule=None,
            heating_availability_schedule=None,
            primary_air_flow_rate=None,
            chilled_water_flow_rate=None,
            hot_water_flow_rate=None,
            total_beam_length=None,
            primary_air_flow_rate_per_beam_length=None):

        if model is not None:
            # Check validity of the heating coil
            if heat_coil is not None:
                beam_heat_coil = heat_coil
            else:
                beam_heat_coil = AirLoopComponent.coil_heating_four_pipe_beam(model)

            # Check validity of the cooling coil
            if cool_coil is not None:
                beam_cool_coil = cool_coil
            else:
                beam_cool_coil = AirLoopComponent.coil_cooling_four_pipe_beam(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeFourPipeBeam(
                model, beam_cool_coil, beam_heat_coil)

            if name is not None:
                terminal.setName(name)

            if primary_air_availability_schedule is not None:
                terminal.setPrimaryAirAvailabilitySchedule(primary_air_availability_schedule)
            if cooling_availability_schedule is not None:
                terminal.setCoolingAvailabilitySchedule(cooling_availability_schedule)
            if heating_availability_schedule is not None:
                terminal.setHeatingAvailabilitySchedule(heating_availability_schedule)

            if primary_air_flow_rate is not None:
                terminal.setDesignPrimaryAirVolumeFlowRate(primary_air_flow_rate)
            else:
                terminal.autosizeDesignPrimaryAirVolumeFlowRate()

            if chilled_water_flow_rate is not None:
                terminal.setDesignChilledWaterVolumeFlowRate(chilled_water_flow_rate)
            else:
                terminal.autosizeDesignChilledWaterVolumeFlowRate()

            if hot_water_flow_rate is not None:
                terminal.setDesignHotWaterVolumeFlowRate(hot_water_flow_rate)
            else:
                terminal.autosizeDesignHotWaterVolumeFlowRate()

            if total_beam_length is not None:
                terminal.setZoneTotalBeamLength(total_beam_length)
            else:
                terminal.autosizeZoneTotalBeamLength()

            if primary_air_flow_rate_per_beam_length is not None:
                terminal.setRatedPrimaryAirFlowRateperBeamLength(primary_air_flow_rate_per_beam_length)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_constant_volume_cooled_beam(
            model: openstudio.openstudiomodel.Model,
            coil: openstudio.openstudiomodel.CoilCoolingCooledBeam = None,
            name: str = None,
            cooled_beam_type: str = None,
            supply_air_flow_rate=None,
            max_total_chilled_water_flow_rate=None,
            number_of_beams=None,
            beam_length=None,
            design_inlet_water_temp=None,
            design_outlet_water_temp=None,
            coefficient_of_induction_kin=None):

        if model is not None:

            if coil is not None:
                beam_coil = coil
            else:
                beam_coil = AirLoopComponent.coil_cooling_cooled_beam(model)

            terminal = openstudio.openstudiomodel.AirTerminalSingleDuctConstantVolumeCooledBeam(
                model, ScheduleTool.always_on(model), beam_coil)

            if name is not None:
                terminal.setName(name)

            if cooled_beam_type is not None:
                terminal.setCooledBeamType(cooled_beam_type)

            if supply_air_flow_rate is not None:
                terminal.setSupplyAirVolumetricFlowRate(supply_air_flow_rate)
            else:
                terminal.autosizeSupplyAirVolumetricFlowRate()

            if max_total_chilled_water_flow_rate is not None:
                terminal.setMaximumTotalChilledWaterVolumetricFlowRate(max_total_chilled_water_flow_rate)
            else:
                terminal.autosizeMaximumTotalChilledWaterVolumetricFlowRate()

            if number_of_beams is not None:
                terminal.setNumberofBeams(number_of_beams)
            else:
                terminal.autosizeNumberofBeams()

            if beam_length is not None:
                terminal.setBeamLength(beam_length)
            else:
                terminal.autosizeBeamLength()

            if design_inlet_water_temp is not None:
                terminal.setDesignInletWaterTemperature(design_inlet_water_temp)
            if design_outlet_water_temp is not None:
                terminal.setDesignOutletWaterTemperature(design_outlet_water_temp)

            if coefficient_of_induction_kin is not None:
                terminal.setCoefficientofInductionKin(coefficient_of_induction_kin)

            return terminal
        else:
            raise ValueError(AirTerminal.model_null_message)

    @staticmethod
    def single_duct_mixer(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            control_for_outdoor_air: bool = True,
            per_person_ventilation_rate_mode: str = None):

        """
        The air terminal mixer provides a means of supplying central system air either to air inlet or
        supply side of a ZoneHVAC equipment such as a four pipe fan coil.
        Normally the central air would be ventilation air from a dedicated outside air system (DOAS).
        """

        terminal = openstudio.openstudiomodel.AirTerminalSingleDuctInletSideMixer(model)

        if name is not None:
            terminal.setName(name)

        if control_for_outdoor_air is not None:
            terminal.setControlForOutdoorAir(control_for_outdoor_air)

        if per_person_ventilation_rate_mode is not None:
            terminal.setPerPersonVentilationRateMode(per_person_ventilation_rate_mode)

        return terminal
