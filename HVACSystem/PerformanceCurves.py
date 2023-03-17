import openstudio


class Curve:

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
            name: str = None):
        curve = openstudio.openstudiomodel.CurveBiquadratic(model)

        if name is not None: curve.setName(name)
        if coeff_constant is not None: curve.setCoefficient1Constant(coeff_constant)
        if coeff_x is not None: curve.setCoefficient2x(coeff_x)
        if coeff_x2 is not None: curve.setCoefficient3xPOW2(coeff_x2)
        if coeff_y is not None: curve.setCoefficient4y(coeff_y)
        if coeff_y2 is not None: curve.setCoefficient5yPOW2(coeff_y2)
        if coeff_xy is not None: curve.setCoefficient6xTIMESY(coeff_xy)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_y is not None: curve.setMinimumValueofy(min_y)
        if max_y is not None: curve.setMaximumValueofy(max_y)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

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
            name: str = None):
        curve = openstudio.openstudiomodel.CurveQuadratic(model)

        if name is not None: curve.setName(name)
        if coeff_constant is not None: curve.setCoefficient1Constant(coeff_constant)
        if coeff_x is not None: curve.setCoefficient2x(coeff_x)
        if coeff_x2 is not None: curve.setCoefficient3xPOW2(coeff_x2)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

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

        if name is not None: curve.setName(name)
        if coeff1_constant is not None: curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_x is not None: curve.setCoefficient2x(coeff2_x)
        if coeff3_x2 is not None: curve.setCoefficient3xPOW2(coeff3_x2)
        if coeff4_x3 is not None: curve.setCoefficient3xPOW2(coeff4_x3)
        if coeff5_x4 is not None: curve.setCoefficient3xPOW2(coeff5_x4)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

        # Input options:        # Output options:
        # ******************    # **********************
        # Dimensionless         # Dimensionless
        # Temperature           # Temperature
        # MassFlow              # Power
        # VolumetricFlow        # Capacity
        # Power
        # Distance
        if input_unit_type is not None: curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None: curve.setOutputUnitType(output_unit_type)

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

        if name is not None: curve.setName(name)
        if coeff1_constant is not None: curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_x is not None: curve.setCoefficient2x(coeff2_x)
        if coeff3_x2 is not None: curve.setCoefficient3xPOW2(coeff3_x2)
        if coeff4_x3 is not None: curve.setCoefficient3xPOW2(coeff4_x3)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

        # Input options:        # Output options:
        # ******************    # **********************
        # Dimensionless         # Dimensionless
        # Temperature           # Temperature
        # MassFlow              # Power
        # VolumetricFlow        # Capacity
        # Power
        # Distance
        if input_unit_type is not None: curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None: curve.setOutputUnitType(output_unit_type)

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

        if name is not None: curve.setName(name)
        if coeff1_constant is not None: curve.setCoefficient1Constant(coeff1_constant)
        if coeff2_constant is not None: curve.setCoefficient2Constant(coeff2_constant)
        if coeff3_constant is not None: curve.setCoefficient3Constant(coeff3_constant)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

        # Input options:        # Output options:
        # ******************    # **********************
        # Dimensionless         # Dimensionless
        # Temperature           # Temperature
        # MassFlow              # Power
        # VolumetricFlow        # Capacity
        # Power
        # Distance
        if input_unit_type is not None: curve.setInputUnitTypeforX(input_unit_type)
        if output_unit_type is not None: curve.setOutputUnitType(output_unit_type)

