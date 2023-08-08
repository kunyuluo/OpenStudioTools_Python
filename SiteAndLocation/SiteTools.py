import openstudio
import os
from Resources.EPW_Parser import EPW


class SiteLocationTool:

    @staticmethod
    def download_weather_data(file_url):
        if file_url and (file_url.startswith('https://') or file_url.startswith('http://')):
            if file_url.endswith('.zip') or file_url.endswith('.ZIP') or file_url.endswith('.Zip'):
                folder_name = file_url.split('/')[-1][:-4]
            else:
                folder_name = file_url.split('/')[-2]

            check_data = True
        else:
            check_data = False
            folder_name = "C:\\ladybug"

        if check_data:
            default_folder = "C:\\ladybug"
            working_dir = os.path.join(default_folder, folder_name)

            # Download from web:
            # client = System.Net.WebClient()
            webFile = os.path.join(working_dir, file_url.split('/')[-2] + '.zip')
            # client.DownloadFile(file_link, webFile)

    @staticmethod
    def set_weather_file(
            model: openstudio.openstudiomodel.Model,
            epw_path_str: str,
            clg_dd_threshold: int = 1,
            htg_dd_threshold: int = 1):

        """
        clg_dd_threshold: 1: 0.4% 2: 1% 3: 2% \n
        htg_dd_threshold: 1: 99.6% 2: 99%
        """

        assert os.path.isfile(epw_path_str), 'Cannot find an epw file at {}'.format(epw_path_str)
        assert epw_path_str.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                                     'It does not possess the .epw file extension.'.format(epw_path_str)

        # Assign epw file to the model:
        epw_path = openstudio.openstudioutilitiescore.toPath(epw_path_str)
        epw_file = openstudio.openstudioutilitiesfiletypes.EpwFile(epw_path)
        openstudio.openstudiomodel.WeatherFile.setWeatherFile(model, epw_file)

        # Parse the epw file:
        epw = EPW.import_from_existing(epw_path_str)
        location = epw["header"][0]
        heating_design_condition = epw["header"][1].heating_design_condition
        cooling_design_condition = epw["header"][1].cooling_design_condition

        clg_dd_thresholds = {1: ".4%", 2: "1%", 3: "2%"}
        htg_dd_thresholds = {1: "99.6%", 2: "99%"}

        # Assign site info to the model:
        site = model.getSite()

        if location.province != "-":
            site_name = location.city.upper() + "_" + location.province.upper() + "_" + location.country.upper() + \
                        " Design_Conditions"
        else:
            site_name = location.city.upper() + "_" + location.country.upper() + " Design_Conditions"

        site.setName(site_name)
        site.setLatitude(location.latitude)
        site.setLongitude(location.longitude)
        site.setElevation(location.elevation)
        site.setTimeZone(location.timezone)

        # Create Design Condition Object:
        # ***********************************************************************************
        # Apply selector:
        match htg_dd_threshold:
            case 1:
                # for Ann Htg Condns DB
                # ***************************************************************************
                max_dry_bulb_temp_htg = heating_design_condition.dry_bulb_temp_996
                # Ann Hum_n Condns DP=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_htg = heating_design_condition.mean_coincident_dry_bulb_temp_996
                dew_point_htg = heating_design_condition.dew_point_temp_996
                # Ann Htg Wind Condns WS=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_wind_htg = heating_design_condition.mean_coincident_dry_bulb_temp_04
                wind_speed_htg = heating_design_condition.wind_speed_04
            case 2 | _:
                # for Ann Htg Condns DB
                # ***************************************************************************
                max_dry_bulb_temp_htg = heating_design_condition.dry_bulb_temp_990
                # Ann Hum_n Condns DP=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_htg = heating_design_condition.mean_coincident_dry_bulb_temp_990
                dew_point_htg = heating_design_condition.dew_point_temp_990
                # Ann Htg Wind Condns WS=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_wind_htg = heating_design_condition.mean_coincident_dry_bulb_temp_1
                wind_speed_htg = heating_design_condition.wind_speed_1

        match clg_dd_threshold:
            case 1:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_04
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_04
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_04
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_04
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_enth
                enthalpy_clg = cooling_design_condition.enthalpy_04 * 1000
            case 2:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_1
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_1
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_1
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_1
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_enth
                enthalpy_clg = cooling_design_condition.enthalpy_1 * 1000
            case 3 | _:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_2
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_2
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_2
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_2
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_enth
                enthalpy_clg = cooling_design_condition.enthalpy_2 * 1000

        # Ann Htg Condns DB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_db_name = location.city + " Ann Htg " + htg_dd_thresholds[htg_dd_threshold] + " Condns DB"

        SiteLocationTool.design_day(
            model, dd_htg_db_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_htg,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=max_dry_bulb_temp_htg,
            wind_speed=heating_design_condition.mean_wind_speed_996,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Hum_n Condns DP=>MCDB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_hum_name = location.city + " Ann Hum_n " + htg_dd_thresholds[htg_dd_threshold] + " Condns DP=>MCDB"

        SiteLocationTool.design_day(
            model, dd_htg_hum_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_dp_htg,
            humidity_condition_type=2,
            wet_bulb_at_max_dry_bulb=dew_point_htg,
            wind_speed=heating_design_condition.mean_wind_speed_996,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Htg Wind Condns WS=>MCDB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_wind_name = location.city + " Ann Htg Wind " + htg_dd_thresholds[htg_dd_threshold] + " Condns WS=>MCDB"

        SiteLocationTool.design_day(
            model, dd_htg_wind_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_wind_htg,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=max_dry_bulb_temp_wind_htg,
            wind_speed=wind_speed_htg,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Clg Condns DB=>MWB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_db_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns DB=>MWB"

        SiteLocationTool.design_day(
            model, dd_clg_db_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=wet_bulb_at_dry_bulb_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns WB=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_wb_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns WB=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_wb_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_wb_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=wet_bulb_temp_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns DP=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_dp_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns DP=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_dp_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_dp_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=2,
            wet_bulb_at_max_dry_bulb=dew_point_temp_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns Enth=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_enth_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns Enth=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_enth_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_enth_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=4,
            enthalpy_at_max_dry_bulb=enthalpy_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

    @staticmethod
    def design_day(
            model: openstudio.openstudiomodel.Model,
            name: str,
            month: int = 1,
            day_of_month: int = 21,
            day_type: int = 1,
            max_dry_bulb_temp: float = 0.0,
            daily_dry_bulb_temp_range: float = 0.0,
            dry_bulb_temp_range_modifier_type: int = 1,
            dry_bulb_temp_range_modifier_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            humidity_condition_type: int = 1,
            wet_bulb_at_max_dry_bulb: float = None,
            humidity_indicating_day_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            humidity_ratio_at_max_dry_bulb: float = None,
            enthalpy_at_max_dry_bulb: float = None,
            daily_wet_bulb_temp_range: float = None,
            barometric_pressure: float = 101241.,
            wind_speed: float = 0.0,
            wind_direction: float = 0.0,
            rain: bool = False,
            snow_on_ground: bool = False,
            daylight_saving_time: bool = False,
            solar_model: int = 1,
            beam_solar_day_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            diffuse_solar_day_schedule: openstudio.openstudiomodel.ScheduleRuleset = None,
            ashrae_clear_sky_optical_depth_for_beam_irradiance: float = None,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance: float = None,
            sky_clearness: float = None):

        """
        -Day_type: \n
        1.WinterDesignDay 2.SummerDesignDay 3.Monday 4.Tuesday 5.Wednesday 6.Thursday 7.Friday 8.Saturday
        9.Sunday 10.Holiday \n
        -Dry-Bulb Temperature Range Modifier Type: \n
        1.DefaultMultipliers 2.MultiplierSchedule 3.DifferenceSchedule 4.TemperatureProfileSchedule \n
        -Humidity Condition Type: \n
        1.Wetbulb 2.DewPoint 3.HumidityRatio 4.Enthalpy 5.RelativeHumiditySchedule
        6.WetBulbProfileMultiplierSchedule 7.WetBulbProfileDifferenceSchedule 8.WetBulbProfileDefaultMultipliers \n
        -Solar Model: \n
        1.ASHRAEClearSky 2.ASHRAETau 3.ASHRAETau2017 4.ZhangHuang 5.Schedule
        """

        day_types = {1: "WinterDesignDay", 2: "SummerDesignDay", 3: "Monday", 4: "Tuesday", 5: "Wednesday",
                     6: "Thursday", 7: "Friday", 8: "Saturday", 9: "Sunday", 10: "Holiday"}
        modifier_types = {1: "DefaultMultipliers", 2: "MultiplierSchedule", 3: "DifferenceSchedule",
                          4: "TemperatureProfileSchedule"}
        humidity_types = {1: "Wetbulb", 2: "DewPoint", 3: "HumidityRatio", 4: "Enthalpy", 5: "RelativeHumiditySchedule",
                          6: "WetBulbProfileMultiplierSchedule", 7: "WetBulbProfileDifferenceSchedule",
                          8: "WetBulbProfileDefaultMultipliers"}
        solar_types = {1: "ASHRAEClearSky", 2: "ASHRAETau", 3: "ASHRAETau2017", 4: "ZhangHuang", 5: "Schedule"}

        dd = openstudio.openstudiomodel.DesignDay(model)

        dd.setName(name)
        dd.setMonth(month)
        dd.setDayOfMonth(day_of_month)
        dd.setDayType(day_types[day_type])
        dd.setMaximumDryBulbTemperature(max_dry_bulb_temp)
        dd.setDailyDryBulbTemperatureRange(daily_dry_bulb_temp_range)
        dd.setDryBulbTemperatureRangeModifierType(modifier_types[dry_bulb_temp_range_modifier_type])

        if dry_bulb_temp_range_modifier_type != 1 and dry_bulb_temp_range_modifier_schedule is not None:
            dd.setDryBulbTemperatureRangeModifierSchedule(dry_bulb_temp_range_modifier_schedule)

        dd.setHumidityConditionType(humidity_types[humidity_condition_type])

        if wet_bulb_at_max_dry_bulb is not None:
            dd.setWetBulbOrDewPointAtMaximumDryBulb(wet_bulb_at_max_dry_bulb)

        if humidity_indicating_day_schedule is not None:
            dd.setHumidityIndicatingDaySchedule(humidity_indicating_day_schedule)

        if humidity_ratio_at_max_dry_bulb is not None:
            dd.setHumidityRatioAtMaximumDryBulb(humidity_ratio_at_max_dry_bulb)

        if enthalpy_at_max_dry_bulb is not None:
            dd.setEnthalpyAtMaximumDryBulb(enthalpy_at_max_dry_bulb)

        if daily_wet_bulb_temp_range is not None:
            dd.setDailyWetBulbTemperatureRange(daily_wet_bulb_temp_range)

        dd.setBarometricPressure(barometric_pressure)
        dd.setWindSpeed(wind_speed)
        dd.setWindDirection(wind_direction)
        dd.setRainIndicator(rain)
        dd.setSnowIndicator(snow_on_ground)
        dd.setDaylightSavingTimeIndicator(daylight_saving_time)
        dd.setSolarModelIndicator(solar_types[solar_model])

        if solar_model == 5:
            if beam_solar_day_schedule is not None:
                dd.setBeamSolarDaySchedule(beam_solar_day_schedule)
            if diffuse_solar_day_schedule is not None:
                dd.setDiffuseSolarDaySchedule(diffuse_solar_day_schedule)

        if ashrae_clear_sky_optical_depth_for_beam_irradiance is not None:
            dd.setAshraeClearSkyOpticalDepthForBeamIrradiance(ashrae_clear_sky_optical_depth_for_beam_irradiance)

        if ashrae_clear_sky_optical_depth_for_diffuse_irradiance is not None:
            dd.setAshraeClearSkyOpticalDepthForDiffuseIrradiance(ashrae_clear_sky_optical_depth_for_diffuse_irradiance)

        if sky_clearness is not None:
            dd.setSkyClearness(sky_clearness)

        return dd

    @staticmethod
    def set_site_and_design_days(
            model: openstudio.openstudiomodel.Model,
            ddy_path_str: str,
            clg_dd_threshold: int = 1,
            htg_dd_threshold: int = 1):

        """
        clg_dd_threshold: 1: 0.4% 2: 1% 3: 2% \n
        htg_dd_threshold: 1: 99.6% 2: 99%
        """

        assert os.path.isfile(ddy_path_str), 'Cannot find an epw file at {}'.format(ddy_path_str)
        assert ddy_path_str.lower().endswith('ddy'), '{} is not an .ddy file. \n' \
                                                     'It does not possess the .ddy file extension.'.format(ddy_path_str)

        clg_dd_thresholds = {1: ".4%", 2: "1%", 3: "2%"}
        htg_dd_thresholds = {1: "99.6%", 2: "99%"}

        clg_dd_selector = "Clg" + " " + clg_dd_thresholds[clg_dd_threshold]
        htg_dd_selector = "Htg" + " " + htg_dd_thresholds[clg_dd_threshold]
        hum_dd_selector = "Hum_n" + " " + htg_dd_thresholds[htg_dd_threshold]
        wind_dd_selector = "Wind" + " " + htg_dd_thresholds[htg_dd_threshold]

        ddy_path = openstudio.openstudioutilitiescore.toPath(ddy_path_str)

        ddy_file = openstudio.openstudioutilitiesidf.IdfFile.load(ddy_path).get()
        ddy_workspace = openstudio.Workspace(ddy_file)
        reverse_translator = openstudio.energyplus.ReverseTranslator()
        ddy_model = reverse_translator.translateWorkspace(ddy_workspace)

        # Get all design days objects:
        design_days = ddy_model.getDesignDays()

        # Get site object:
        site_obj = ddy_model.getSite()

        # Assign site info to the model:
        site = model.getSite()
        site.setName(site_obj.nameString())
        site.setLatitude(site_obj.latitude())
        site.setLongitude(site_obj.longitude())
        site.setElevation(site_obj.elevation())
        site.setTimeZone(site_obj.timeZone())

        # Assign design days info to the model:
        if design_days is not None and len(design_days) != 0:
            for design_day in design_days:
                if clg_dd_selector in design_day.nameString() \
                        or htg_dd_selector in design_day.nameString() \
                        or hum_dd_selector in design_day.nameString() \
                        or wind_dd_selector in design_day.nameString():

                    dd = openstudio.openstudiomodel.DesignDay(model)

                    dd.setName(design_day.nameString())
                    dd.setMonth(design_day.month())
                    dd.setDayOfMonth(design_day.dayOfMonth())
                    dd.setDayType(design_day.dayType())
                    dd.setMaximumDryBulbTemperature(design_day.maximumDryBulbTemperature())
                    dd.setDailyDryBulbTemperatureRange(design_day.dailyDryBulbTemperatureRange())
                    dd.setDryBulbTemperatureRangeModifierType(design_day.dryBulbTemperatureRangeModifierType())
                    dd.setHumidityConditionType(design_day.humidityConditionType())
                    dd.setWetBulbOrDewPointAtMaximumDryBulb(float(design_day.wetBulbOrDewPointAtMaximumDryBulb()))
                    if float(design_day.enthalpyAtMaximumDryBulb()) != 0:
                        dd.setEnthalpyAtMaximumDryBulb(float(design_day.enthalpyAtMaximumDryBulb()))
                    dd.setBarometricPressure(design_day.barometricPressure())
                    dd.setWindSpeed(design_day.windSpeed())
                    dd.setWindDirection(design_day.windDirection())
                    dd.setRainIndicator(design_day.rainIndicator())
                    dd.setSnowIndicator(design_day.snowIndicator())
                    dd.setDaylightSavingTimeIndicator(design_day.daylightSavingTimeIndicator())
                    dd.setSolarModelIndicator(design_day.solarModelIndicator())
                    dd.setAshraeClearSkyOpticalDepthForBeamIrradiance(
                        design_day.ashraeClearSkyOpticalDepthForBeamIrradiance())
                    dd.setAshraeClearSkyOpticalDepthForDiffuseIrradiance(
                        design_day.ashraeClearSkyOpticalDepthForDiffuseIrradiance())

    @staticmethod
    def set_site_and_design_days_from_epw(
            model: openstudio.openstudiomodel.Model,
            epw_path_str: str,
            clg_dd_threshold: int = 1,
            htg_dd_threshold: int = 1):

        """
        clg_dd_threshold: 1: 0.4% 2: 1% 3: 2% \n
        htg_dd_threshold: 1: 99.6% 2: 99%
        """

        assert os.path.isfile(epw_path_str), 'Cannot find an epw file at {}'.format(epw_path_str)
        assert epw_path_str.lower().endswith('epw'), '{} is not an .epw file. \n' \
                                                     'It does not possess the .epw file extension.'.format(epw_path_str)

        clg_dd_thresholds = {1: ".4%", 2: "1%", 3: "2%"}
        htg_dd_thresholds = {1: "99.6%", 2: "99%"}

        # Parse the epw file:
        epw = EPW.import_from_existing(epw_path_str)
        location = epw["header"][0]
        heating_design_condition = epw["header"][1].heating_design_condition
        cooling_design_condition = epw["header"][1].cooling_design_condition

        # Assign site info to the model:
        site = model.getSite()

        if location.province != "-":
            site_name = location.city.upper() + "_" + location.province.upper() + "_" + location.country.upper() + \
                        " Design_Conditions"
        else:
            site_name = location.city.upper() + "_" + location.country.upper() + " Design_Conditions"

        site.setName(site_name)
        site.setLatitude(location.latitude)
        site.setLongitude(location.longitude)
        site.setElevation(location.elevation)
        site.setTimeZone(location.timezone)

        # Create Design Condition Object:
        # ***********************************************************************************
        # Apply selector:
        match htg_dd_threshold:
            case 1:
                # for Ann Htg Condns DB
                # ***************************************************************************
                max_dry_bulb_temp_htg = heating_design_condition.dry_bulb_temp_996
                # Ann Hum_n Condns DP=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_htg = heating_design_condition.mean_coincident_dry_bulb_temp_996
                dew_point_htg = heating_design_condition.dew_point_temp_996
                # Ann Htg Wind Condns WS=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_wind_htg = heating_design_condition.mean_coincident_dry_bulb_temp_04
                wind_speed_htg = heating_design_condition.wind_speed_04
            case 2 | _:
                # for Ann Htg Condns DB
                # ***************************************************************************
                max_dry_bulb_temp_htg = heating_design_condition.dry_bulb_temp_990
                # Ann Hum_n Condns DP=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_htg = heating_design_condition.mean_coincident_dry_bulb_temp_990
                dew_point_htg = heating_design_condition.dew_point_temp_990
                # Ann Htg Wind Condns WS=>MCDB
                # ***************************************************************************
                max_dry_bulb_temp_wind_htg = heating_design_condition.mean_coincident_dry_bulb_temp_1
                wind_speed_htg = heating_design_condition.wind_speed_1

        match clg_dd_threshold:
            case 1:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_04
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_04
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_04
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_04
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_04_enth
                enthalpy_clg = cooling_design_condition.enthalpy_04 * 1000
            case 2:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_1
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_1
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_1
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_1
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_1_enth
                enthalpy_clg = cooling_design_condition.enthalpy_1 * 1000
            case 3 | _:
                # Ann Clg Condns DB=>MWB
                # ***************************************************************************
                max_dry_bulb_temp_clg = cooling_design_condition.dry_bulb_temp_2
                wet_bulb_at_dry_bulb_clg = cooling_design_condition.mean_coincident_wet_bulb_temp_2
                # Ann Clg Condns WB=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_wb_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_evap
                wet_bulb_temp_clg = cooling_design_condition.wet_bulb_temp_2
                # Ann Clg Condns DP=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_dp_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_dehum
                dew_point_temp_clg = cooling_design_condition.dew_point_temp_2
                # Ann Clg Condns Enth=>MDB
                # ***************************************************************************
                max_dry_bulb_temp_enth_clg = cooling_design_condition.mean_coincident_dry_bulb_temp_2_enth
                enthalpy_clg = cooling_design_condition.enthalpy_2 * 1000

        # Ann Htg Condns DB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_db_name = location.city + " Ann Htg " + htg_dd_thresholds[htg_dd_threshold] + " Condns DB"

        SiteLocationTool.design_day(
            model, dd_htg_db_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_htg,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=max_dry_bulb_temp_htg,
            wind_speed=heating_design_condition.mean_wind_speed_996,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Hum_n Condns DP=>MCDB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_hum_name = location.city + " Ann Hum_n " + htg_dd_thresholds[htg_dd_threshold] + " Condns DP=>MCDB"

        SiteLocationTool.design_day(
            model, dd_htg_hum_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_dp_htg,
            humidity_condition_type=2,
            wet_bulb_at_max_dry_bulb=dew_point_htg,
            wind_speed=heating_design_condition.mean_wind_speed_996,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Htg Wind Condns WS=>MCDB (99.6% or 99%)
        # ***********************************************************************************
        dd_htg_wind_name = location.city + " Ann Htg Wind " + htg_dd_thresholds[htg_dd_threshold] + " Condns WS=>MCDB"

        SiteLocationTool.design_day(
            model, dd_htg_wind_name,
            month=heating_design_condition.coldest_month,
            max_dry_bulb_temp=max_dry_bulb_temp_wind_htg,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=max_dry_bulb_temp_wind_htg,
            wind_speed=wind_speed_htg,
            wind_direction=heating_design_condition.wind_direction_996,
            sky_clearness=0.0)

        # Ann Clg Condns DB=>MWB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_db_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns DB=>MWB"

        SiteLocationTool.design_day(
            model, dd_clg_db_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=wet_bulb_at_dry_bulb_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns WB=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_wb_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns WB=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_wb_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_wb_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=1,
            wet_bulb_at_max_dry_bulb=wet_bulb_temp_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns DP=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_dp_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns DP=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_dp_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_dp_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=2,
            wet_bulb_at_max_dry_bulb=dew_point_temp_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)

        # Ann Clg Condns Enth=>MDB (0.4% or 1% or 2%)
        # ***********************************************************************************
        dd_clg_enth_name = location.city + " Ann Clg " + clg_dd_thresholds[clg_dd_threshold] + " Condns Enth=>MDB"

        SiteLocationTool.design_day(
            model, dd_clg_enth_name,
            month=cooling_design_condition.hottest_month,
            day_type=2,
            max_dry_bulb_temp=max_dry_bulb_temp_enth_clg,
            daily_dry_bulb_temp_range=cooling_design_condition.hottest_month_dry_bulb_temp_range,
            humidity_condition_type=4,
            enthalpy_at_max_dry_bulb=enthalpy_clg,
            wind_speed=cooling_design_condition.mean_wind_speed_04,
            wind_direction=cooling_design_condition.wind_direction_04,
            solar_model=2,
            ashrae_clear_sky_optical_depth_for_beam_irradiance=0.899,
            ashrae_clear_sky_optical_depth_for_diffuse_irradiance=1.294)
