import openstudio
from openstudio.openstudiomeasure import OSRunner
from measures.MyFirstMeasure import measure
from openstudio.openstudioutilitiesfiletypes import WorkflowJSON
import pathlib


# create an instance of the measure
my_measure = measure.MyFirstMeasure()

# create runner with a pre-defined OSW
seed_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\BoxModel.osm"
seed_path = openstudio.openstudioutilitiescore.toPath(seed_path_str)

epw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\files\CHN_Beijing.Beijing.545110_IWEC.epw"
epw_path = openstudio.openstudioutilitiescore.toPath(epw_path_str)

osw_path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\my_workflow2.osw"
osw_path = openstudio.openstudioutilitiescore.toPath(osw_path_str)

# osw = WorkflowJSON()
# osw.setSeedFile(seed_path)
# osw.setWeatherFile(epw_path)

# args = openstudio.measure.OSArgumentVector()
# r_value = openstudio.measure.OSArgument.makeDoubleArgument("insl_r", True)
# r_value.setDisplayName("Insulation R-value")
# r_value.setDefaultValue(44.3)
# args.append(r_value)

# m_type_1 = MeasureType("ModelMeasure")
#
# m_step_1 = MeasureStep("measure_1")
# m_step_1.setArgument("insl_r", 20)
#
# vec = MeasureStepVector()
# vec.append(m_step_1)

# osw.setMeasureSteps(m_type_1, vec)

osw = WorkflowJSON.load(osw_path).get()
# runner = OSRunner(osw)
runner = openstudio.measure.OSRunner(osw)

# Load a model for testing
path_str = "D:\Projects\OpenStudioDev\OpenStudio_py\OSW\BoxModel.osm"
path = openstudio.openstudioutilitiescore.toPath(path_str)
model = openstudio.openstudiomodel.Model.load(path).get()

arguments = my_measure.arguments(model)
argument_map = openstudio.measure.convertOSArgumentVectorToMap(arguments)

# create hash of argument values.
# args_dict = {}
# args_dict["insl_r"] = 35.0
#
# for arg in arguments:
#     temp_arg_var = arg.clone()
#     if arg.name() in args_dict:
#         assert (temp_arg_var.setValue(args_dict[arg.name()]))
#         argument_map[arg.name()] = temp_arg_var
# print("run measure:")

# run the measure
my_measure.run(model, runner, argument_map)
result = runner.result()

# show_output(result)
print(f"results: {result}")

# save the model to test output directory
output_file_path = openstudio.toPath(
    str(pathlib.Path(__file__).parent.absolute()/ "output" / "test_output.osm"))
model.save(output_file_path, True)