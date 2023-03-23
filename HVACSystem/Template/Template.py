import openstudio
from HVACSystem.AirTerminals import AirTerminal
from HVACSystem.AirLoopComponents import AirLoopComponent
from HVACSystem.PlantLoopComponents import PlantLoopComponent


class Template:

    model_null_message = "Model cannot be empty"
    zone_null_message = "Please check the validity of the input thermal zones"

    @staticmethod
    def vav_chiller_boiler(
            model: openstudio.openstudiomodel.Model,
            thermal_zones):

        # Check input validity:
        if model is not None:
            if thermal_zones is not None or len(thermal_zones) != 0:

                # Build an air loop:
                air_loops = []
                cooling_coils = []
                heating_coils = []
                reheat_coils = []
                # if the input thermal zone is a single thermal zone object:
                if isinstance(thermal_zones, openstudio.openstudiomodel.ThermalZone):
                    reheat_coil = AirLoopComponent.coil_heating_water(model)
                    terminal = AirTerminal.single_duct_vav_reheat(model, reheat_coil)
                    air_loop = AirLoopComponent.air_loop_simplified(
                        model, "VAV Loop", air_terminal=terminal, thermal_zones=[thermal_zones])
                    air_loops.append(air_loop[0])
                    if len(air_loop[1]) != 0:
                        reheat_coils.extend(air_loop[1])

                # if the input thermal zone is a list of thermal zone objects
                elif isinstance(thermal_zones, list):
                    # for 1-D list of thermal zone objects:
                    if isinstance(thermal_zones[0], openstudio.openstudiomodel.ThermalZone)\
                            and isinstance(thermal_zones[-1], openstudio.openstudiomodel.ThermalZone):
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                        terminal = AirTerminal.single_duct_vav_reheat(model, reheat_coil)
                        air_loop = AirLoopComponent.air_loop_simplified(
                            model, "VAV Loop", air_terminal=terminal, thermal_zones=thermal_zones)
                        air_loops.append(air_loop)
                        if len(air_loop[1]) != 0:
                            reheat_coils.extend(air_loop[1])
                    # for 2-D list of thermal zone objects:
                    if isinstance(thermal_zones[0], list) and isinstance(thermal_zones[-1], list):
                        for i in range(len(thermal_zones)):
                            reheat_coil = AirLoopComponent.coil_heating_water(model)
                            terminal = AirTerminal.single_duct_vav_reheat(model, reheat_coil)
                            air_loop = AirLoopComponent.air_loop_simplified(
                                model, "VAV Loop "+str(i+1), air_terminal=terminal, thermal_zones=thermal_zones[i])
                            air_loops.append(air_loop)
                            if len(air_loop[1]) != 0:
                                reheat_coils.extend(air_loop[1])

                # if the input thermal zones is a dictionary of thermal zone objects:
                elif isinstance(thermal_zones, dict):
                    for key in thermal_zones:
                        reheat_coil = AirLoopComponent.coil_heating_water(model)
                        terminal = AirTerminal.single_duct_vav_reheat(model, reheat_coil)
                        terminal.reheatCoil()
                        air_loop = AirLoopComponent.air_loop_simplified(
                            model, "VAV Loop "+str(key), air_terminal=terminal, thermal_zones=[thermal_zones])
                        air_loops.append(air_loop)
                        if len(air_loop[1]) != 0:
                            reheat_coils.extend(air_loop[1])

                # Build a hot water loop:
                hot_water_loop = PlantLoopComponent.plant_loop(
                    model, "Hot Water Loop", "Water", demand_branches=reheat_coils)

            else:
                raise ValueError(Template.zone_null_message)
        else:
            raise ValueError(Template.model_null_message)