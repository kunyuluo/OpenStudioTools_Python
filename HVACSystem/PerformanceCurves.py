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
    def vrf_performance_curve_set_1(model: openstudio.openstudiomodel.Model):

        curves = {}

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
        curves["Cooling Energy Input Ratio Boundary Curve"] = \
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
        curves["Cooling Energy Input Ratio Modifier Function of Low Part-Load Ratio Curve"] = \
            Curve.cubic(model, 140.9991, -18.7871, 1.1756, -0.02507, 13.89, 23.89,
                        name="EIRRatioLowPLR_Cooling")












        return curves
