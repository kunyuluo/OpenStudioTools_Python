import openstudio
import os
# import System


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

        if check_data:
            default_folder = "C:\ladybug"
            working_dir = os.path.join(default_folder, folder_name)

        # Download from web:
        # client = System.Net.WebClient()
        webFile = os.path.join(working_dir, file_url.split('/')[-2] + '.zip')
        # client.DownloadFile(file_link, webFile)

    @staticmethod
    def set_weather_file(model: openstudio.openstudiomodel.Model, epw_path_str: str):
        epw_path = openstudio.openstudioutilitiescore.toPath(epw_path_str)
        epw_file = openstudio.openstudioutilitiesfiletypes.EpwFile(epw_path)
        openstudio.openstudiomodel.WeatherFile.setWeatherFile(model, epw_file)

    @staticmethod
    def set_site_and_design_days(
            model: openstudio.openstudiomodel.Model,
            ddy_path_str: str,
            clg_dd_threshold=".4",
            htg_dd_threshold="99.6%",):
        clg_dd_selector = "Clg" + " " + clg_dd_threshold
        htg_dd_selector = "Htg" + " " + htg_dd_threshold
        hum_dd_selector = "Hum_n" + " " + htg_dd_threshold
        wind_dd_selector = "Wind" + " " + htg_dd_threshold

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
                if clg_dd_selector in design_day.nameString()\
                        or htg_dd_selector in design_day.nameString()\
                        or hum_dd_selector in design_day.nameString()\
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
