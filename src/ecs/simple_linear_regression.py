# coding: utf-8
from math import pow

def cal_mean(readings):
    """
    Function to calculate the mean value of the input readings
    """
    readings_total = sum(readings)
    number_of_readings = len(readings)
    mean = readings_total / float(number_of_readings)
    return mean

def cal_variance(readings):
    """
    Calculating the variance of the readings
    """
    if len(readings) <= 1:
        return 0
    # To calculate the variance we need the mean value
    readings_mean = cal_mean(readings)
    # mean difference squared readings
    mean_difference_squared_readings = [pow((reading - readings_mean), 2) for reading in readings]
    variance = sum(mean_difference_squared_readings)
    return variance / float(len(readings) - 1)

def cal_covariance(readings_1, readings_2):
    """
    Calculate the covariance between two different list of readings
    """
    readings_1_mean = cal_mean(readings_1)
    readings_2_mean = cal_mean(readings_2)
    readings_size = len(readings_1)
    covariance = 0.0
    for i in xrange(0, readings_size):
        covariance += (readings_1[i] - readings_1_mean) * (readings_2[i] - readings_2_mean)
    return covariance / float(readings_size - 1)


def cal_simple_linear_regression_coefficients(x_readings, y_readings):
    """
    Calculating the simple linear regression coefficients (B0, B1)
    """
    # Coefficient W1 = covariance of x_readings and y_readings divided by variance of x_readings
    if cal_variance(x_readings) == 0:
        w1 = 0
    else:
        w1 = cal_covariance(x_readings, y_readings) / float(cal_variance(x_readings))

    # Coefficient W0 = mean of y_readings - ( W1 * the mean of the x_readings )
    w0 = cal_mean(y_readings) - (w1 * cal_mean(x_readings))
    return w0, w1

def predict_target_value(x, w0, w1):
    """
    Calculating the target (y) value using the input x and the coefficients b0, b1
    """
    return w0 + w1 * x


