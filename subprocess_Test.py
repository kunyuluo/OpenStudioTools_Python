import subprocess
import os

script_path = os.path.dirname(__file__)
workflow_path = script_path + "\OSW\my_workflow2.osw"

# setup string for CLI:
# cli_string = "openstudio run -w " + workflow_path
cmd = ['openstudio', 'run', '-w', workflow_path]

# subprocess.Popen(["Notepad.exe","D:\Projects\OpenStudioDev\OpenStudio_py\myFile.txt"])
# subprocess.Popen(["OpenStudioApp.exe", "D:\Projects\OpenStudioDev\OpenStudio_py\BoxModel.osm"])
# subprocess.Popen(["EXCEL.EXE", "D:\Projects\OpenStudioDev\OpenStudio_py\data.xlsx"])
# print(cmd)

# subprocess.run("openstudio run -w MedOfficeSeed\modified.osw")
process = subprocess.Popen(cmd, shell=False)
process.communicate()