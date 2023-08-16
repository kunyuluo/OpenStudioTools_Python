import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# Curve fit function
def linear(t, a, b):
    return a * t + b


def func_2(t, a, b, c):
    return a * pow(t, 2) + b * t + c


def func_3(t, a, b, c, d):
    return a * pow(t, 3) + b * pow(t, 2) + c * t + d


def func_4(t, a, b, c, d, e):
    return a * pow(t, 4) + b * pow(t, 3) + c * pow(t, 2) + d * t + e
