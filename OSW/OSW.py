import os.path
import openstudio
from openstudio.openstudioutilitiesfiletypes import WorkflowJSON
import pathlib


seed_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\BoxModel.osm"
seed_path = openstudio.openstudioutilitiescore.toPath(seed_path_str)

epw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\CHN_Beijing.Beijing.545110_IWEC.epw"
epw_path = openstudio.openstudioutilitiescore.toPath(epw_path_str)

osw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\my_workflow2.osw"
osw_path = openstudio.openstudioutilitiescore.toPath(osw_path_str)

osw = WorkflowJSON()
osw.setSeedFile(seed_path)
osw.setWeatherFile(epw_path)

# Get the current directory:
curr_dir = pathlib.Path(seed_path_str).parent.absolute()
target_dir = os.path.join(curr_dir, "measures")
print(target_dir)
if os.path.isdir(target_dir):
    print("You got it!")
else:
    print("No such directory is found!")
# print(curr_dir)
osw.saveAs(osw_path)
