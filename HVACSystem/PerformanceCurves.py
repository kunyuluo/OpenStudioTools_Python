import openstudio


class Curve:

    # Input options:        # Output options:
    # ******************    # **********************
    # Dimensionless         # Dimensionless
    # Temperature           # Temperature
    # MassFlow              # Power
    # VolumetricFlow        # Capacity
    # Power
    # Distance

    @staticmethod
    def biquadratic(
            model: openstudio.openstudiomodel.Model,
            coeff_constant=None,
            coeff_x=None,
            coeff_x2=None,
            coeff_y=None,
            coeff_y2=None,
            coeff_xy=None,
            min_x=None,
            max_x=None,
            min_y=None,
            max_y=None,
            min_out=None,
            max_out=None,
            input_unit_type_x: str = "Dimensionless",
            input_unit_type_y: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*y + c5*y^2 + c6*x*y
        """
        curve = openstudio.openstudiomodel.CurveBiquadratic(model)

        if name is not None:
            curve.setName(name)
        if coeff_constant is not None:
            curve.setCoefficient1Constant(coeff_constant)
        if coeff_x is not None:
            curve.setCoefficient2x(coeff_x)
        if coeff_x2 is not None:
            curve.setCoefficient3xPOW2(coeff_x2)
        if coeff_y is not None:
            curve.setCoefficient4y(coeff_y)
        if coeff_y2 is not None:
            curve.setCoefficient5yPOW2(coeff_y2)
        if coeff_xy is not None:
            curve.setCoefficient6xTIMESY(coeff_xy)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_y is not None:
            curve.setMinimumValueofy(min_y)
        if max_y is not None:
            curve.setMaximumValueofy(max_y)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type_x is not None:
            curve.setInputUnitTypeforX(input_unit_type_x)
        if input_unit_type_y is not None:
            curve.setInputUnitTypeforY(input_unit_type_y)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    @staticmethod
    def quadratic(
            model: openstudio.openstudiomodel.Model,
            coeff_constant=None,
            coeff_x=None,
            coeff_x2=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type_x: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2
        """

        curve = openstudio.openstudiomodel.CurveQuadratic(model)

        if name is not None:
            curve.setName(name)
        if coeff_constant is not None:
            curve.setCoefficient1Constant(coeff_constant)
        if coeff_x is not None:
            curve.setCoefficient2x(coeff_x)
        if coeff_x2 is not None:
            curve.setCoefficient3xPOW2(coeff_x2)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type_x is not None:
            curve.setInputUnitTypeforX(input_unit_type_x)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    @staticmethod
    def quartic(
            model: openstudio.openstudiomodel.Model,
            coeff1_constant=None,
            coeff2_x=None,
            coeff3_x2=None,
            coeff4_x3=None,
            coeff5_x4=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*x^3 + c5*x^4
        """

        curve = openstudio.openstudiomodel.CurveQuartic(model)

        if name is not None:
            curve.setName(name)
        if coeff1_constant is not None:
            curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_x is not None:
            curve.setCoefficient2x(coeff2_x)
        if coeff3_x2 is not None:
            curve.setCoefficient3xPOW2(coeff3_x2)
        if coeff4_x3 is not None:
            curve.setCoefficient3xPOW2(coeff4_x3)
        if coeff5_x4 is not None:
            curve.setCoefficient3xPOW2(coeff5_x4)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type is not None:
            curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    @staticmethod
    def cubic(
            model: openstudio.openstudiomodel.Model,
            coeff1_constant=None,
            coeff2_x=None,
            coeff3_x2=None,
            coeff4_x3=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x + c3*x^2 + c4*x^3
        """

        curve = openstudio.openstudiomodel.CurveCubic(model)

        if name is not None:
            curve.setName(name)
        if coeff1_constant is not None:
            curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_x is not None:
            curve.setCoefficient2x(coeff2_x)
        if coeff3_x2 is not None:
            curve.setCoefficient3xPOW2(coeff3_x2)
        if coeff4_x3 is not None:
            curve.setCoefficient3xPOW2(coeff4_x3)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type is not None:
            curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    @staticmethod
    def exponent(
            model: openstudio.openstudiomodel.Model,
            coeff1_constant=None,
            coeff2_constant=None,
            coeff3_constant=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x^c3
        """

        curve = openstudio.openstudiomodel.CurveExponent(model)

        if name is not None:
            curve.setName(name)
        if coeff1_constant is not None:
            curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_constant is not None:
            curve.setCoefficient2Constant(coeff2_constant)
        if coeff3_constant is not None:
            curve.setCoefficient3Constant(coeff3_constant)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type is not None:
            curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

    @staticmethod
    def linear(
            model: openstudio.openstudiomodel.Model,
            coeff1_constant=None,
            coeff2_x=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2*x
        """

        curve = openstudio.openstudiomodel.CurveLinear(model)

        if name is not None:
            curve.setName(name)
        if coeff1_constant is not None:
            curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_x is not None:
            curve.setCoefficient2x(coeff2_x)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type is not None:
            curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    @staticmethod
    def sigmoid(
            model: openstudio.openstudiomodel.Model,
            coeff1=None,
            coeff2=None,
            coeff3=None,
            coeff4=None,
            coeff5=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None,
            input_unit_type: str = "Dimensionless",
            output_unit_type: str = "Dimensionless",
            name: str = None):

        """
        f(x) = c1 + c2 / (1 + e^((c3 - x) / c4))^c5
        """

        curve = openstudio.openstudiomodel.CurveSigmoid(model)

        if name is not None:
            curve.setName(name)
        if coeff1 is not None:
            curve.setCoefficient1C1(coeff1)
        if coeff2 is not None:
            curve.setCoefficient1C1(coeff2)
        if coeff3 is not None:
            curve.setCoefficient1C1(coeff3)
        if coeff4 is not None:
            curve.setCoefficient1C1(coeff4)
        if coeff5 is not None:
            curve.setCoefficient1C1(coeff5)
        if min_x is not None:
            curve.setMinimumValueofx(min_x)
        if max_x is not None:
            curve.setMaximumValueofx(max_x)
        if min_out is not None:
            curve.setMinimumCurveOutput(min_out)
        if max_out is not None:
            curve.setMaximumCurveOutput(max_out)
        if input_unit_type is not None:
            curve.setInputUnitTypeforx(input_unit_type)
        if output_unit_type is not None:
            curve.setOutputUnitType(output_unit_type)

        return curve

    # Build-in performance curve sets:
    @staticmethod
    def pump_curve_set(control_strategy: int = 0):
        """
        :param str control_strategy:
        0:"Linear",
        1:"VSD No Reset",
        2:"VSD Reset"
        :return: a list of coefficient values from C1 to C4
        """

        if control_strategy == 0:
            values = [0, 1, 0, 0]
        elif control_strategy == 1:
            values = [0.103, -0.04, 0.767, 0.1679]
        elif control_strategy == 2:
            values = [0.0273, -0.1317, 0.6642, 0.445]
        else:
            values = [0, 1, 0, 0]

        return values

    @staticmethod
    def fan_curve_set(control_strategy: int = 0):
        """
        :param str control_strategy:
        0:"ASHRAE 90.1 Baseline",
        1:"VSD Only",
        2:"VSD+StaticPressureControl (Good)",
        3:"VSD+StaticPressureControl (Perfect)"
        :return: a list of coefficient values from C1 to C4
        """

        if control_strategy == 0:
            values = [0.0013, 0.147, 0.9506, -0.0998, 0]
        elif control_strategy == 1:
            values = [0.070428852, 0.385330201, -0.460864118, 1.00920344, 0]
        elif control_strategy == 2:
            values = [0.04076, 0.08804, -0.07293, 0.94374, 0]
        elif control_strategy == 3:
            values = [0.02783, 0.02658, -0.08707, 1.03092, 0]
        else:
            values = [0, 1, 0, 0, 0]

        return values

    @staticmethod
    def chiller_performance_curve_ashrae_baseline(model: openstudio.openstudiomodel.Model):

        """
        1.Cooling Capacity Function of Temperature Curve \n
        2.Electric Input to Cooling Output Ratio Function of Temperature Curve \n
        3.Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        """
        curves = {}

        # Cooling Capacity Function of Temperature Curve
        curves["Cooling Capacity Function of Temperature Curve"] = \
            Curve.biquadratic(model, 0.258, 0.0389, -0.000217, 0.0469, -0.000943, -0.000343,
                              5, 10, 24, 35,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CoolingCapTempCurve_ASHRAE90.1")

        # Electric Input to Cooling Output Ratio Function of Temperature Curve
        curves["Electric Input to Cooling Output Ratio Function of Temperature Curve"] = \
            Curve.biquadratic(model, 0.934, -0.0582, 0.0045, 0.00243, 0.000486, -0.00122,
                              5, 10, 24, 35,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CoolingEIRRatioTempCurve_ASHRAE90.1")

        # Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        curves["Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve"] = \
            Curve.quadratic(model, 0.222903, 0.313387, 0.46371, 0, 1, name="CoolingEIRRatioPLRCurve_ASHRAE90.1")

        return curves

    @staticmethod
    def chiller_performance_curve_title24(model: openstudio.openstudiomodel.Model):

        """
        1.Cooling Capacity Function of Temperature Curve \n
        2.Electric Input to Cooling Output Ratio Function of Temperature Curve \n
        3.Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        """
        curves = {}

        # Cooling Capacity Function of Temperature Curve
        curves["Cooling Capacity Function of Temperature Curve"] = \
            Curve.biquadratic(model, 1.35608, 0.04875, -0.000888, -0.014525, -0.000286, -0.00004,
                              5, 10, 24, 35,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CoolingCapTempCurve_ASHRAE90.1")

        # Electric Input to Cooling Output Ratio Function of Temperature Curve
        curves["Electric Input to Cooling Output Ratio Function of Temperature Curve"] = \
            Curve.biquadratic(model, 0.756376, -0.015019, 0.000156, 0.00246, 0.000515, -0.000687,
                              5, 10, 24, 35,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CoolingEIRRatioTempCurve_ASHRAE90.1")

        # Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve
        curves["Electric Input to Cooling Output Ratio Function of Part Load Ratio Curve"] = \
            Curve.quadratic(model, 0.055483, 0.451866, 0.488242, 0, 1, name="CoolingEIRRatioPLRCurve_ASHRAE90.1")

        return curves

    @staticmethod
    def vrf_performance_curve_set_1(model: openstudio.openstudiomodel.Model):

        """
        1.Cooling Capacity Ratio Boundary Curve \n
        2.Cooling Capacity Ratio Modifier Function of Low Temperature Curve \n
        3.Cooling Capacity Ratio Modifier Function of High Temperature Curve \n
        4.Cooling Energy Input Ratio Boundary Curve \n
        5.Cooling Energy Input Ratio Modifier Function of Low Temperature Curve \n
        6.Cooling Energy Input Ratio Modifier Function of High Temperature Curve \n
        7.Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        8.Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        9.Cooling Combination Ratio Correction Factor Curve \n
        10.Cooling Part-Load Fraction Correlation Curve \n
        11.Heating Capacity Ratio Boundary Curve \n
        12.Heating Capacity Ratio Modifier Function of Low Temperature Curve \n
        13.Heating Capacity Ratio Modifier Function of High Temperature Curve \n
        14.Heating Energy Input Ratio Boundary Curve \n
        15.Heating Energy Input Ratio Modifier Function of Low Temperature Curve \n
        16.Heating Energy Input Ratio Modifier Function of High Temperature Curve \n
        17.Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve \n
        18.Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve \n
        19.Heating Combination Ratio Correction Factor Curve \n
        20.Heating Part-Load Fraction Correlation Curve \n
        21.Piping Correction Factor for Length in Cooling Mode Curve \n
        22.Piping Correction Factor for Length in Heating Mode Curve \n
        23.Heat Recovery Cooling Capacity Modifier Curve \n
        24.Heat Recovery Heating Capacity Modifier Curve
        """

        curves = {}

        # Cooling
        # ******************************************************************************
        # Cooling Capacity Ratio Boundary Curve
        curves["Cooling Capacity Ratio Boundary Curve"] =\
            Curve.cubic(model, 140.9991, -18.7871, 1.1756, -0.02507, 13.89, 23.89,
                        input_unit_type="Temperature", output_unit_type="Temperature",
                        name="CapRatioBoundary_Cooling")

        # Cooling Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Cooling Capacity Ratio Modifier Function of Low Temperature Curve"] =\
            Curve.biquadratic(model, -0.0901953919, 0.0505070990, 0.0003088882, 0.0031865985, -0.0000130163, -0.0001563836,
                              13.89, 23.89, 10, 39.44,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CapRatioLowTempCurve_Cooling")

        # Cooling Capacity Ratio Modifier Function of High Temperature Curve
        curves["Cooling Capacity Ratio Modifier Function of High Temperature Curve"] =\
            Curve.biquadratic(model, -3.2081703349, 0.2302688916, -0.0026585963, 0.0960582706, -0.0008516839, -0.0022864878,
                              13.89, 23.89, 21.11, 47.78,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CapRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Boundary Curve
        curves["Cooling Energy Input Ratio Boundary Curve"] =\
            Curve.cubic(model, 140.9991, -18.7871, 1.1756, -0.02507, 13.89, 23.89,
                        input_unit_type="Temperature", output_unit_type="Temperature",
                        name="EIRRatioBoundary_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Cooling Energy Input Ratio Modifier Function of Low Temperature Curve"] =\
            Curve.biquadratic(model, 0.6888245196, -0.0172281621, 0.0005241366, 0.0009858312, 0.0005792064, -0.0004213067,
                              13.89, 23.89, 10, 39.44,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="EIRRatioLowTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Cooling Energy Input Ratio Modifier Function of High Temperature Curve"] =\
            Curve.biquadratic(model, 0.4404769569, -0.0439185866, 0.0018265019, 0.0293315774, 0.0003795638, -0.0011518238,
                              13.89, 23.89, 21.11, 47.78,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="EIRRatioHighTempCurve_Cooling")

        # Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve"] =\
            Curve.cubic(model, -1.246792429, 5.155371753, -6.128396226, 3.217813168,
                        0.25, 1.0,
                        name="EIRRatioLowPLR_Cooling")

        # Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Cooling Energy Input Ratio Modifier Function of High Part-Load Ratio Curve"] =\
            Curve.cubic(model, -30.6717767898, 86.1535796412, -78.5620113444, 24.0802084930,
                        1.0, 1.152777778,
                        name="EIRRatioHighPLR_Cooling")

        # Cooling Combination Ratio Correction Factor Curve
        curves["Cooling Combination Ratio Correction Factor Curve"] =\
            Curve.cubic(model, -30.6717767898, 86.1535796412, -78.5620113444, 24.0802084930,
                        1.0, 1.152777778,
                        name="CombinationRatio_Cooling")

        # Cooling Part-Load Fraction Correlation Curve
        curves["Cooling Part-Load Fraction Correlation Curve"] =\
            Curve.linear(model, 0.85, 0.15, 0, 1, name="PLRFractionCorrelation_Cooling")

        # Heating
        # ******************************************************************************
        # Heating Capacity Ratio Boundary Curve
        curves["Heating Capacity Ratio Boundary Curve"] =\
            Curve.cubic(model, 203.8006305, -26.23815416, 1.097486087, -0.0152378, 16.11, 23.89,
                        input_unit_type="Temperature", output_unit_type="Temperature",
                        name="CapRatioBoundary_Heating")

        # Heating Capacity Ratio Modifier Function of Low Temperature Curve
        curves["Heating Capacity Ratio Modifier Function of Low Temperature Curve"] =\
            Curve.biquadratic(model, 1.0475954826, 0.0299030501, -0.0014437977, 0.0224657841, -0.0005924488, -0.0008933140,
                              16.11, 23.89, -20, 2.2,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CapRatioLowTempCurve_Heating")

        # Heating Capacity Ratio Modifier Function of High Temperature Curve
        curves["Heating Capacity Ratio Modifier Function of High Temperature Curve"] =\
            Curve.biquadratic(model, 1.2761141679, 0.0105535358, -0.0011110665, 0.0003551723, -0.0000182544, -0.0000038670,
                              16.11, 23.89, -4.4, 13.33,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="CapRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Boundary Curve
        curves["Heating Energy Input Ratio Boundary Curve"] =\
            Curve.cubic(model, 429.0791605507, -61.4939116463, 2.9055009778, -0.0455092410, 16.11, 23.89,
                        input_unit_type="Temperature", output_unit_type="Temperature",
                        name="EIRRatioBoundary_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Temperature Curve
        curves["Heating Energy Input Ratio Modifier Function of Low Temperature Curve"] =\
            Curve.biquadratic(model, 1.7317223341, -0.0994807311, 0.0032543423, -0.0232819641, 0.0004068197, -0.0010269258,
                              16.11, 23.89, -20, 2.22,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="EIRRatioLowTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of High Temperature Curve
        curves["Heating Energy Input Ratio Modifier Function of High Temperature Curve"] =\
            Curve.biquadratic(model, 1.8630353188, -0.1084122085, 0.0034798649, -0.0061726628, -0.0002882955, -0.0005421480,
                              16.11, 23.89, -4.44, 13.33,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="EIRRatioHighTempCurve_Heating")

        # Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve
        curves["Heating Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve"] =\
            Curve.cubic(model, -0.5528951749, 3.0525728816, -2.4847593777, 0.9829690708,
                        0.25, 1.0,
                        name="EIRRatioLowPLR_Heating")

        # Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve
        curves["Heating Energy Input Ratio Modifier Function of High Part-Load Ratio Curve"] =\
            Curve.cubic(model, -4.3790604236, 13.0115360115, -10.5447636312, 2.9122880433,
                        1.0, 1.212962963,
                        name="EIRRatioHighPLR_Heating")

        # Heating Combination Ratio Correction Factor Curve
        curves["Heating Combination Ratio Correction Factor Curve"] =\
            Curve.cubic(model, -15.8827160494, 42.7057613169, -36.1111111111, 10.2880658436,
                        1.0, 1.3,
                        name="CombinationRatio_Heating")

        # Heating Part-Load Fraction Correlation Curve
        curves["Heating Part-Load Fraction Correlation Curve"] =\
            Curve.linear(model, 0.85, 0.15, 0, 1, name="PLRFractionCorrelation_Heating")

        # Piping
        # ******************************************************************************
        # Piping Correction Factor for Length in Cooling Mode Curve
        curves["Piping Correction Factor for Length in Cooling Mode Curve"] = \
            Curve.cubic(model, 0.9989504106, -0.0007550999, 0.0000011566, -0.0000000029,
                        7.62, 220.07, input_unit_type="Distance",
                        name="PipingCorrectionFactorCurve_Cooling")

        # Piping Correction Factor for Length in Heating Mode Curve
        curves["Piping Correction Factor for Length in Heating Mode Curve"] = \
            Curve.cubic(model, 1.0022992262, -0.0004389003, 0.0000014007, -0.0000000042,
                        7.62, 220.07, input_unit_type="Distance",
                        name="PipingCorrectionFactorCurve_Heating")

        # Heat Recovery
        # ******************************************************************************
        # Heat Recovery Cooling Capacity Modifier Curve
        curves["Heat Recovery Cooling Capacity Modifier Curve"] =\
            Curve.biquadratic(model, 0.9, 0, 0, 0, 0, 0,
                              -100, 100, -100, 100,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="HeatRecoveryCapModifier_Cooling")

        # Heat Recovery Heating Capacity Modifier Curve
        curves["Heat Recovery Heating Capacity Modifier Curve"] =\
            Curve.biquadratic(model, 1.1, 0, 0, 0, 0, 0,
                              -100, 100, -100, 100,
                              input_unit_type_x="Temperature", input_unit_type_y="Temperature",
                              name="HeatRecoveryCapModifier_Heating")

        return curves
