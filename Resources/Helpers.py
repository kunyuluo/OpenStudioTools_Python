import math
import openstudio
import matplotlib.pyplot as plt
from HVACSystem.PerformanceCurves import Curve


class Helper:

    # Calculator:
    # *************************************************************************************
    @staticmethod
    def infiltration_calculator(
            standard_flow_rate,
            standard_pressure: int = 75,
            target_pressure: int = 4,
            input_in_ip_unit: bool = True):

        # ASHRAE 90.1 2013: 0.4 cfm/sf@75Pa
        # Passive house: 0.1 cfm/sf@75Pa
        flow_rate_at_target_pressure = standard_flow_rate * math.pow((target_pressure / standard_pressure), 0.67)
        if input_in_ip_unit:
            # convert result from cfm/sf to m3_s/m2
            result = flow_rate_at_target_pressure * 0.00047195 * 10.76
        else:
            result = flow_rate_at_target_pressure

        return result

    @staticmethod
    def pump_power_calculator_ip(head, flow, motor_efficiency=0.9, pump_efficiency=0.7):
        """
        :param head: pump head in ft
        :param flow: pump water flow rate in gpm
        :param motor_efficiency: default is 0.9
        :param pump_efficiency: default is 0.7
        :return: pump power in watts (W)
        """
        hp = head * flow * 8.33 / (33000 * motor_efficiency * pump_efficiency)
        return hp * 745.7

    @staticmethod
    def pump_power_calculator_si(head, flow, motor_efficiency=0.9, pump_efficiency=0.7):
        """
        :param head: pump head in meter
        :param flow: pump water flow rate in m3/h
        :param motor_efficiency: default is 0.9
        :param pump_efficiency: default is 0.7
        :return: pump power in watts (W)
        """
        kw = head * flow * 1000 * 9.81 / (3600000 * motor_efficiency * pump_efficiency)
        return kw * 1000

    # Convertor:
    # *************************************************************************************
    @staticmethod
    def f_to_c(temperature):
        return (temperature - 32) / 1.8

    @staticmethod
    def c_to_f(temperature):
        return temperature * 1.8 + 32

    @staticmethod
    def delta_temp_f_to_c(delta):
        return delta / 1.8

    @staticmethod
    def delta_temp_c_to_f(delta):
        return delta * 1.8

    @staticmethod
    def cfm_to_m3s(flow):
        return flow * 0.0004719474

    @staticmethod
    def gpm_to_m3s(flow):
        return flow * 0.0000630902

    @staticmethod
    def u_ip_to_si(u_value):
        """
        Convert U-Values in IP (BTU/hft2F) to U-Values in SI (W/Km2)
        """
        return u_value * 5.678263337

    @staticmethod
    def u_si_to_ip(u_value):
        """
        Convert U-Values in SI (W/Km2) to U-Values in IP (BTU/hft2F)
        """
        return u_value / 5.678263337

    # Visualizer:
    # *************************************************************************************
    @staticmethod
    def visualize_curve(
            curve: openstudio.openstudiomodel.Curve,
            variable_1=range(0, 11, 1),
            variable_2=None,
            normalize: bool = True,
            show_reference_curve: bool = True,
            reference_curve: openstudio.openstudiomodel.Curve = None,
            y_axis_limits=None):

        """
        :param curve: openstudio curve object
        :param variable_1: By default is a range from 0 to 10. Could be any number range (e.g. temperature)
        :param variable_2: Will be used when the curve type is biquadratic. Could be a single number or a number range
        :param normalize: if True, the input variable will be normalized into 0 to 1
        :param show_reference_curve: if True, a default curve will display in the graph for comparison
        :param reference_curve: instead of using default reference curve, you can input your own curve here for comparison
        :param y_axis_limits: the value range of y-axis. Input list here. By default, it's [0, 1]
        """

        curve_type = str(type(curve)).split('.')[-1].split("'")[0].split("Curve")[1]

        data_points = []
        reference_data_points = []
        try:
            match curve_type:
                case "Cubic":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2x()
                        c3 = reference_curve.coefficient3xPOW2()
                        c4 = reference_curve.coefficient4xPOW3()
                    else:
                        c1, c2, c3, c4 = 0, 0, 0, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + \
                                     curve.coefficient2x() * i + \
                                     curve.coefficient3xPOW2() * math.pow(i, 2) + \
                                     curve.coefficient4xPOW3() * math.pow(i, 3)
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2) + c4 * math.pow(i, 3)
                        reference_data_points.append(reference_data_point)

                case "Quartic":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2x()
                        c3 = reference_curve.coefficient3xPOW2()
                        c4 = reference_curve.coefficient4xPOW3()
                        c5 = reference_curve.coefficient5xPOW4()
                    else:
                        c1, c2, c3, c4, c5 = 0, 0, 0, 0, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + \
                                     curve.coefficient2x() * i + \
                                     curve.coefficient3xPOW2() * math.pow(i, 2) + \
                                     curve.coefficient4xPOW3() * math.pow(i, 3) + \
                                     curve.coefficient5xPOW4() * math.pow(i, 4)
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2) + c4 * math.pow(i, 3) + c5 * math.pow(
                            i, 4)
                        reference_data_points.append(reference_data_point)

                case "Exponent":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2Constant()
                        c3 = reference_curve.coefficient3Constant()
                    else:
                        c1, c2, c3 = 0, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + \
                                     curve.coefficient2Constant() * \
                                     math.pow(i, curve.coefficient3Constant())
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * math.pow(i, c3)
                        reference_data_points.append(reference_data_point)

                case "Quadratic":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2x()
                        c3 = reference_curve.coefficient3xPOW2()
                    else:
                        c1, c2, c3 = 0, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + \
                                     curve.coefficient2x() * i + \
                                     curve.coefficient3xPOW2() * math.pow(i, 2)
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2)
                        reference_data_points.append(reference_data_point)

                case "Biquadratic":
                    # Check validity of variable 2:
                    if variable_2 is not None:
                        if isinstance(variable_2, float):
                            variable_2 = [variable_2] * 11
                        elif isinstance(variable_2, range):
                            pass
                        else:
                            raise TypeError('"variable_2" can either be a float number or a range')
                    else:
                        raise ValueError('"variable_2" is needed to construct a biquadratic curve')

                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2x()
                        c3 = reference_curve.coefficient3xPOW2()
                        c4 = reference_curve.coefficient4y()
                        c5 = reference_curve.coefficient5yPOW2()
                        c6 = reference_curve.coefficient6xTIMESY()
                    else:
                        c1, c2, c3, c4, c5, c6 = 0, 1, 1, 1, 1, 1

                    for xy_tuple in zip(variable_1, variable_2):
                        if normalize:
                            x = xy_tuple[0] / 10
                            y = xy_tuple[1] / 10
                        else:
                            x = xy_tuple[0]
                            y = xy_tuple[1]
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + \
                                     curve.coefficient2x() * x + \
                                     curve.coefficient3xPOW2() * math.pow(x, 2) + \
                                     curve.coefficient4y() * y + \
                                     curve.coefficient5yPOW2() * math.pow(y, 2) + \
                                     curve.coefficient6xTIMESY() * x * y
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * x + c3 * math.pow(x, 2) + \
                                               c4 * y + c5 * math.pow(y, 2) + c6 * x * y
                        reference_data_points.append(reference_data_point)

                case "Linear":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1Constant()
                        c2 = reference_curve.coefficient2x()
                    else:
                        c1, c2 = 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1Constant() + curve.coefficient2x() * i
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i
                        reference_data_points.append(reference_data_point)

                case "Sigmoid":
                    # setup coefficients for reference curve
                    if reference_curve is not None:
                        c1 = reference_curve.coefficient1C1()
                        c2 = reference_curve.coefficient2C2()
                        c3 = reference_curve.coefficient3C3()
                        c4 = reference_curve.coefficient4C4()
                        c5 = reference_curve.coefficient5C5()
                    else:
                        c1, c2, c3, c4, c5 = 0, 1, 1, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        data_point = curve.coefficient1C1() + \
                                     curve.coefficient2C2() / \
                                     (math.pow((1 + math.pow(math.e, (curve.coefficient3C3() - i) /
                                                             curve.coefficient4C4())), curve.coefficient5C5()))
                        data_points.append(data_point)

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 / (math.pow((1 + math.pow(math.e, (c3 - i) / c4)), c5))
                        reference_data_points.append(reference_data_point)

                case _:
                    raise TypeError("This type of curve is not supported")

            # Make the graph:
            # *******************************************************************
            # Normalize input data if needed:
            x_labels = []
            for i in variable_1:
                if normalize:
                    x_labels.append(i / 10)
                else:
                    x_labels.append(i)

            # Plot the input data points:
            fig, ax = plt.subplots()
            ax.plot(x_labels, data_points, label='Input Curve', color='#c52af5')

            # Plot reference data points if needed:
            if show_reference_curve:
                ax.plot(x_labels, reference_data_points, label='Reference Curve', color='#c9c9c9')

            ax.set_title(curve_type + " Curve")
            ax.legend(loc=0)

            # Set y-axis limits if applicable:
            if isinstance(y_axis_limits, list):
                plt.ylim(y_axis_limits)
            plt.show()

        except TypeError:
            print("The type of input curve and reference curve don't match.")

    @staticmethod
    def visualize_curve_numeric(
            curve_type: str,
            curve=None,
            variable_1=range(0, 11, 1),
            variable_2=None,
            normalize: bool = True,
            show_reference_curve: bool = True,
            reference_curve=None):

        """
        :param curve_type: type of curve
        :param curve: a list of coefficients from C1 to Cn
        :param variable_1: By default is a range from 0 to 10. Could be any number range (e.g. temperature)
        :param variable_2: Will be used when the curve type is biquadratic. Could be a single number or a number range
        :param normalize: if True, the input variable will be normalized into 0 to 1
        :param show_reference_curve: if True, a default curve will display in the graph for comparison
        :param reference_curve: instead of using default reference curve,
                you can input your own curve coefficients from C1 to Cn
        """

        curve_type = curve_type.lower()

        data_points = []
        reference_data_points = []
        try:
            match curve_type:
                case "cubic":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                            c4 = reference_curve[3]
                        except ValueError:
                            print("Not enough values in the list to construct a cubic curve.")
                            c1, c2, c3, c4 = 0, 0, 0, 1
                    else:
                        c1, c2, c3, c4 = 0, 0, 0, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + \
                                         curve[1] * i + \
                                         curve[2] * math.pow(i, 2) + \
                                         curve[3] * math.pow(i, 3)
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a cubic curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2) + c4 * math.pow(i, 3)
                        reference_data_points.append(reference_data_point)

                case "quartic":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                            c4 = reference_curve[3]
                            c5 = reference_curve[4]
                        except ValueError:
                            print("Not enough values in the list to construct a quartic curve.")
                            c1, c2, c3, c4, c5 = 0, 0, 0, 0, 1
                    else:
                        c1, c2, c3, c4, c5 = 0, 0, 0, 0, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + \
                                         curve[1] * i + \
                                         curve[2] * math.pow(i, 2) + \
                                         curve[3] * math.pow(i, 3) + \
                                         curve[4] * math.pow(i, 4)
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a quartic curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2) + c4 * math.pow(i, 3) + c5 * math.pow(
                            i, 4)
                        reference_data_points.append(reference_data_point)

                case "exponent":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                        except ValueError:
                            print("Not enough values in the list to construct an exponent curve.")
                            c1, c2, c3 = 0, 1, 1
                    else:
                        c1, c2, c3 = 0, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + \
                                         curve[1] * \
                                         math.pow(i, curve[2])
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct an exponent curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * math.pow(i, c3)
                        reference_data_points.append(reference_data_point)

                case "quadratic":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                        except ValueError:
                            print("Not enough values in the list to construct a quadratic curve.")
                            c1, c2, c3 = 0, 1, 1
                    else:
                        c1, c2, c3 = 0, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + \
                                         curve[1] * i + \
                                         curve[2] * math.pow(i, 2)
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a quadratic curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i + c3 * math.pow(i, 2)
                        reference_data_points.append(reference_data_point)

                case "biquadratic":
                    # Check validity of variable 2:
                    if variable_2 is not None:
                        if isinstance(variable_2, float):
                            variable_2 = [variable_2] * 11
                        elif isinstance(variable_2, range):
                            pass
                        else:
                            raise TypeError('"variable_2" can either be a float number or a range')
                    else:
                        raise ValueError('"variable_2" is needed to construct a biquadratic curve')

                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                            c4 = reference_curve[3]
                            c5 = reference_curve[4]
                            c6 = reference_curve[5]
                        except ValueError:
                            print("Not enough values in the list to construct a biquartic curve.")
                            c1, c2, c3, c4, c5, c6 = 0, 1, 1, 1, 1, 1
                    else:
                        c1, c2, c3, c4, c5, c6 = 0, 1, 1, 1, 1, 1

                    for xy_tuple in zip(variable_1, variable_2):
                        if normalize:
                            x = xy_tuple[0] / 10
                            y = xy_tuple[1] / 10
                        else:
                            x = xy_tuple[0]
                            y = xy_tuple[1]
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + \
                                         curve[1] * x + \
                                         curve[2] * math.pow(x, 2) + \
                                         curve[3] * y + \
                                         curve[4] * math.pow(y, 2) + \
                                         curve[5] * x * y
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a biquadratic curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * x + c3 * math.pow(x, 2) + \
                                               c4 * y + c5 * math.pow(y, 2) + c6 * x * y
                        reference_data_points.append(reference_data_point)

                case "Linear":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                        except ValueError:
                            print("Not enough values in the list to construct a linear curve.")
                            c1, c2 = 1, 1
                    else:
                        c1, c2 = 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + curve[1] * i
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a linear curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 * i
                        reference_data_points.append(reference_data_point)

                case "Sigmoid":
                    # setup coefficients for reference curve
                    if isinstance(reference_curve, list):
                        try:
                            c1 = reference_curve[0]
                            c2 = reference_curve[1]
                            c3 = reference_curve[2]
                            c4 = reference_curve[3]
                            c5 = reference_curve[4]
                        except ValueError:
                            print("Not enough values in the list to construct a sigmoid curve.")
                            c1, c2, c3, c4, c5 = 0, 1, 1, 1, 1
                    else:
                        c1, c2, c3, c4, c5 = 0, 1, 1, 1, 1

                    for i in variable_1:
                        if normalize:
                            i = i / 10
                        # Custom curve to visualize:
                        try:
                            data_point = curve[0] + curve[1] / \
                                         (math.pow((1 + math.pow(math.e, (curve[2] - i) / curve[3])), curve[4]))
                            data_points.append(data_point)
                        except ValueError:
                            print("Not enough values in the list to construct a sigmoid curve.")

                        # Default cubic curve for reference:
                        reference_data_point = c1 + c2 / (math.pow((1 + math.pow(math.e, (c3 - i) / c4)), c5))
                        reference_data_points.append(reference_data_point)

                case _:
                    raise TypeError("This type of curve is not supported")

            # Make the graph:
            # *******************************************************************
            # Normalize input data if needed:
            x_labels = []
            for i in variable_1:
                if normalize:
                    x_labels.append(i / 10)
                else:
                    x_labels.append(i)

            # Plot the input data points:
            fig, ax = plt.subplots()
            ax.plot(x_labels, data_points, label='Input Curve', color='#c52af5')

            # Plot reference data points if needed:
            if show_reference_curve:
                ax.plot(x_labels, reference_data_points, label='Reference Curve', color='#c9c9c9')

            ax.set_title(curve_type + " Curve")
            ax.legend(loc=0)
            plt.show()

        except TypeError:
            print("The type of input curve and reference curve don't match.")
