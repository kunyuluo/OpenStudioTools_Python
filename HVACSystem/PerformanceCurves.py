import openstudio


class Curves:

    @staticmethod
    def curve_biquadratic(
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
            max_out=None):
        curve = openstudio.openstudiomodel.CurveBiquadratic(model)

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
    def curve_quadratic(
            model: openstudio.openstudiomodel.Model,
            coeff_constant=None,
            coeff_x=None,
            coeff_x2=None,
            min_x=None,
            max_x=None,
            min_out=None,
            max_out=None):
        curve = openstudio.openstudiomodel.CurveQuadratic(model)

        if coeff_constant is not None: curve.setCoefficient1Constant(coeff_constant)
        if coeff_x is not None: curve.setCoefficient2x(coeff_x)
        if coeff_x2 is not None: curve.setCoefficient3xPOW2(coeff_x2)
        if min_x is not None: curve.setMinimumValueofx(min_x)
        if max_x is not None: curve.setMaximumValueofx(max_x)
        if min_out is not None: curve.setMinimumCurveOutput(min_out)
        if max_out is not None: curve.setMaximumCurveOutput(max_out)

        return curve