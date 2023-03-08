import openstudio


def output_variables(
        model: openstudio.openstudiomodel.Model,
        variables=[],
        frequency="hourly",
        clear_current=True):

    if clear_current:
        current_variables = model.getOutputVariables()
        for variable in current_variables:
            variable.remove()

    if variables is not None and len(variables) != 0:
        for var in variables:
            output_var = openstudio.openstudiomodel.OutputVariable(var, model)
            # Alternatives of frequency:
            # *******************************************************************
            # Detailed        Daily
            # Timestep        Monthly
            # Runperiod       Annual
            #                 Hourly
            # *******************************************************************
            output_var.setReportingFrequency(frequency.lower())