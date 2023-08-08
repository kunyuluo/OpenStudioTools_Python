import openstudio
from Geometry.GeometryTools import GeometryTool
from SiteAndLocation.SiteTools import SiteLocationTool
from SimulationSettings.SimulationSettings import SimulationSettingTool


def create_model(
        epw_file_path: str,
        # ddy_file_path: str,
        target_os_file_path: str = None,
        building_name: str = "Building",
        north_axis: float = 0,
        solar_distribution: int = 2):

    """
    Solar_distribution: \n
    1.MinimalShadowing \n
    2.FullExterior \n
    3.FullInteriorAndExterior \n
    4.FullExteriorWithReflections \n
    5.FullInteriorAndExteriorWithReflections
    """

    # Create a new openstudio model
    # **************************************************************************************
    model = openstudio.openstudiomodel.Model()

    # File Path:
    # **************************************************************************************
    if target_os_file_path is not None:
        path = openstudio.openstudioutilitiescore.toPath(target_os_file_path)
    else:
        path = None

    # Create a building in the model:
    # **************************************************************************************
    building = GeometryTool.building(model, building_name, north_axis)

    # Weather file:
    # **************************************************************************************
    SiteLocationTool.set_weather_file(model, epw_file_path)
    # SiteLocationTool.set_site_and_design_days(model, ddy_file_path)

    # Run period:
    # **************************************************************************************
    SimulationSettingTool.set_run_period(model)
    SimulationSettingTool.simulation_controls(model, solar_distribution)

    return model, path
