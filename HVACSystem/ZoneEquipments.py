import openstudio
from Schedules.ScheduleTools import ScheduleTool
from AirLoopComponents import AirLoopComponent


class ZoneEquipment:
    model_null_message = "Model cannot be empty"

    # @staticmethod
    # def ideal_load_air_system(
    #         model: openstudio.openstudiomodel.Model,
    #         name: str = None,
    #         schedule=None,
    #         max_heating_supply_air_temp=None,
    #         min_cooling_supply_air_temp=None,
    #         max_heating_supply_air_humidity_ratio=None,
    #         min_cooling_supply_air_humidity_ratio=None,
    #         heating_limit: str = None,
    #         cooling_limit: str = None,
    #         max_heating_air_flow_rate=None,
    #         max_sensible_heating_capacity=None,
    #         max_cooling_air_flow_rate=None,
    #         max_total_cooling_capacity=None,
    #         dehumidification_control_type: str = None,
    #         cooling_sensible_heat_ratio=None,
    #         humidification_control_type: str = None,
    #         design_specification_outdoor_air: openstudio.openstudiomodel.DesignSpecificationOutdoorAir = None,
    #         dcv_type: str = None,
    #         economizer_type: str = None,
    #         heat_recovery_type: str = None,
    #         sensible_heat_recovery_effectiveness=None,
    #         latent_heat_recovery_effectiveness=None):
    #
    #     ideal_sys = openstudio.openstudiomodel.ZoneHVACIdealLoadsAirSystem(model)
    #     if name is not None:
    #         ideal_sys.setName(name)
    #
    #     if schedule is not None:
    #         ideal_sys.setAvailabilitySchedule(schedule)
    #
    #     return ideal_sys

    @staticmethod
    def packaged_terminal_air_conditioner(
            model: openstudio.openstudiomodel.Model,
            name: str = None,
            schedule=None,
            fan=None,
            heating_coil=None,
            cooling_coil=None,
            thermal_zone=None):

        if model is not None:
            if schedule is not None:
                equip_schedule = schedule
            else:
                equip_schedule = ScheduleTool.always_on(model)
            if fan is not None:
                equip_fan = fan
            else:
                equip_fan = AirLoopComponent.fan_constant_speed(model)
            if heating_coil is not None:
                equip_heating_coil = heating_coil
            else:
                equip_heating_coil = AirLoopComponent.coil_heating_electric(model)
            if cooling_coil is not None:
                equip_cooling_coil = cooling_coil
            else:
                equip_cooling_coil = AirLoopComponent.coil_cooling_DX_single_speed(model)

            heating_coil_type = str(type(equip_heating_coil)).split('.')[-1].split("'")[0]
            cooling_coil_type = str(type(equip_cooling_coil)).split('.')[-1].split("'")[0]
            fan_type = str(type(equip_fan)).split('.')[-1].split("'")[0]

            heating_coil_type_check = heating_coil_type == "CoilHeatingWater" \
                                      or heating_coil_type == "CoilHeatingElectric" \
                                      or heating_coil_type == "CoilHeatingGas"

            cooling_coil_type_check = cooling_coil_type == "CoilCoolingWater" \
                                      or cooling_coil_type == "CoilCoolingDX" \
                                      or cooling_coil_type == "CoilCoolingDXSingleSpeed" \
                                      or cooling_coil_type == "CoilCoolingDXVariableSpeed"
            fan_type_check = fan_type == "FanConstantVolume" or fan_type == "FanSystemModel"

            type_check_list = {
                "heating": heating_coil_type_check,
                "cooling": cooling_coil_type_check,
                "fan": fan_type_check}

            type_error_message = {
                "heating": "Heating coil type can only be CoilHeatingWater, CoilHeatingElectric, or CoilHeatingGas",
                "cooling": "Cooling coil type can only be CoilCoolingWater, CoilCoolingDX, CoilCoolingDXSingleSpeed, "
                           "or CoilCoolingDXVariableSpeed",
                "fan": "Fan type can only be FanConstantVolume or FanSystemModel"}

            if fan_type_check and cooling_coil_type_check and heating_coil_type_check:
                equipment = openstudio.openstudiomodel.ZoneHVACPackagedTerminalAirConditioner(
                    model,
                    equip_schedule,
                    equip_fan,
                    equip_heating_coil,
                    equip_cooling_coil)

                if name is not None:
                    equipment.setName(name)

                if thermal_zone is not None:
                    equipment.addToThermalZone(thermal_zone)

                return equipment
            else:
                for key in type_check_list.keys():
                    if not type_check_list[key]:
                        raise TypeError(type_error_message[key])
        else:
            raise ValueError(ZoneEquipment.model_null_message)

    # @staticmethod
    # def fan_coil_unit(
    #         model: openstudio.openstudiomodel.Model,
    #         name: str = None,):

    # equipment = openstudio.openstudiomodel.ZoneHVACFourPipeFanCoil()
