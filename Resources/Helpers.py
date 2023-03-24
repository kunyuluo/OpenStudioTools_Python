import math


class Helper:

    @staticmethod
    def infiltration_calculator(
            standard_flow_rate,
            standard_pressure: int = 75,
            target_pressure: int = 4,
            input_in_ip_unit: bool = True):

        # ASHRAE 90.1 2013: 0.4 cfm/sf@75Pa
        # Passive house: 0.1 cfm/sf@75Pa
        flow_rate_at_target_pressure = standard_flow_rate * math.pow((target_pressure/standard_pressure), 0.67)
        if input_in_ip_unit:
            # convert result from cfm/sf to m3_s/m2
            result = flow_rate_at_target_pressure * 0.00047195 * 10.76
        else:
            result = flow_rate_at_target_pressure

        return result
