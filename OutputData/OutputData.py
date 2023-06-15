import openstudio


def output_variables(
        model: openstudio.openstudiomodel.Model,
        variables=None,
        frequency: int = 1,
        clear_current=True):

    """
    Frequency: 1.Hourly 2.Daily 3.Monthly 4.Annual 5.Detailed 6.Timestep 7.Runperiod
    """

    frecuencies = {1: "Hourly", 2: "Daily", 3: "Monthly", 4: "Annual", 5: "Detailed", 6: "Timestep", 7: "Runperiod"}

    if clear_current:
        current_variables = model.getOutputVariables()
        for variable in current_variables:
            variable.remove()

    if isinstance(variables, str):
        output_var = openstudio.openstudiomodel.OutputVariable(variables, model)
        output_var.setReportingFrequency(frecuencies[frequency].lower())
    elif isinstance(variables, list) and len(variables) != 0:
        for var in variables:
            output_var = openstudio.openstudiomodel.OutputVariable(var, model)
            output_var.setReportingFrequency(frecuencies[frequency].lower())
    else:
        raise TypeError("Invalid input type of variables")
