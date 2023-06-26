import openstudio


class SimulationSettingTool:

    @staticmethod
    def set_run_period(
            model: openstudio.openstudiomodel.Model,
            begin_month=1,
            begin_day_of_month=1,
            end_month=12,
            end_day_of_month=31):

        run_period = model.getRunPeriod()
        run_period.setBeginMonth(begin_month)
        run_period.setBeginDayOfMonth(begin_day_of_month)
        run_period.setEndMonth(end_month)
        run_period.setEndDayOfMonth(end_day_of_month)

    @staticmethod
    def set_timestep(model: openstudio.openstudiomodel.Model, time_step=1):
        timestep = model.getTimestep()
        timestep.setNumberOfTimestepsPerHour(time_step)

    @staticmethod
    def simulation_controls(
            model: openstudio.openstudiomodel.Model,
            solar_distribution: int = 2,
            do_zone_sizing=True,
            do_system_sizing=True,
            do_plant_sizing=True,
            run_sizing_period=False,
            run_weather_period=True,
            max_warmup_days=25,
            min_warmup_days=1):

        """
        Solar_distribution: \n
        1.MinimalShadowing \n
        2.FullExterior \n
        3.FullInteriorAndExterior \n
        4.FullExteriorWithReflections \n
        5.FullInteriorAndExteriorWithReflections
        """

        solar_methods = {1: "MinimalShadowing", 2: "FullExterior", 3: "FullInteriorAndExterior",
                         4: "FullExteriorWithReflections", 5: "FullInteriorAndExteriorWithReflections"}

        simulation_control = model.getSimulationControl()
        simulation_control.setDoZoneSizingCalculation(do_zone_sizing)
        simulation_control.setDoSystemSizingCalculation(do_system_sizing)
        simulation_control.setDoPlantSizingCalculation(do_plant_sizing)
        simulation_control.setRunSimulationforSizingPeriods(run_sizing_period)
        simulation_control.setRunSimulationforWeatherFileRunPeriods(run_weather_period)
        simulation_control.setSolarDistribution(solar_methods[solar_distribution])

        if max_warmup_days != 25:
            simulation_control.setMaximumNumberofWarmupDays(max_warmup_days)
        if min_warmup_days != 1:
            simulation_control.setMinimumNumberofWarmupDays(min_warmup_days)

    @staticmethod
    def sizing_parameters(
            model: openstudio.openstudiomodel.Model,
            cooling_sizing_factor=1.15,
            heating_sizing_factor=1.25):

        sizing_parameter = model.getSizingParameters()
        sizing_parameter.setCoolingSizingFactor(cooling_sizing_factor)
        sizing_parameter.setHeatingSizingFactor(heating_sizing_factor)

    @staticmethod
    def convergence_limits(
            model: openstudio.openstudiomodel.Model,
            max_hvac_iteration=20,
            max_plant_iteration=8,
            min_plant_iteration=2,
            min_system_timestep=1):

        convergence = model.getConvergenceLimits()
        if max_hvac_iteration != 20:
            convergence.setMaximumHVACIterations(max_hvac_iteration)
        if max_plant_iteration != 8:
            convergence.setMaximumPlantIterations(max_plant_iteration)
        if min_plant_iteration != 2:
            convergence.setMinimumPlantIterations(min_plant_iteration)
        if min_system_timestep != 1:
            convergence.setMinimumSystemTimestep(min_system_timestep)

    @staticmethod
    def heat_balance_algorithm(
            model: openstudio.openstudiomodel.Model,
            srf_temp_upper_limit: int = 200):

        balance = model.getHeatBalanceAlgorithm()

        balance.setSurfaceTemperatureUpperLimit(srf_temp_upper_limit)
