import math
import numpy as np

# print('1')
# curve_data = np.loadtxt('graphs/x_scale - 0.7y_scale - 1.7')
# print('2')
#
# def load_qoecurve(x_filename, y_filename):
#
#     # x = np.load("x_amazon.npy")
#     # y = np.load("y_amazon.npy")
#     x = np.load(x_filename)
#     y = np.load(y_filename)
#     x = x * 1000
#
#     return x, y


# def qoe_latency_test1(e2e_latency):
#
#     QoE = 0.0
#     Slope = 0.0
#
#     if (e2e_latency < 1000.0):
#
#         QoE = -0.00005 * e2e_latency + 1.0
#         Slope = -0.00005
#
#     elif (e2e_latency >= 1000.0 and e2e_latency < 1500):
#
#         QoE = -0.0002999999999998 * e2e_latency + 1.249999999998
#         Slope = -0.0002999999999998
#
#     elif (e2e_latency <= 2400 and e2e_latency >= 1500):
#
#         QoE = -0.0008666666666667 * e2e_latency + 2.1
#         Slope = -0.0008666666666667
#
#     elif (e2e_latency <= 7200):
#
#         QoE = -0.00000416666666666667 * e2e_latency + 0.03
#         Slope = -0.00000416666666666667
#     else:
#         QoE = 0
#         Slope = 0

    # n = np.shape(x)[0]
    # zone_flag = 0
    # for i in range(n):
    #     if e2e_latency > x[i]: zone_flag = zone_flag + 1
    #     else: break
    # if zone_flag == 0:
    #     QoE = y[0]
    #     Slope = 0
    # elif zone_flag == n:
    #     QoE = y[n-1]
    #     Slope = 0
    # else:
    #     Slope = (y[zone_flag] - y[zone_flag - 1]) / (x[zone_flag] - x[zone_flag - 1])
    #     b = (x[zone_flag]*y[zone_flag - 1] - x[zone_flag - 1]*y[zone_flag]) / (x[zone_flag] - x[zone_flag - 1])
    #     QoE = Slope * e2e_latency + b

    #return QoE, Slope


    # return QoE

def qoe_latency(e2elatency):
    qoe = 0.0
    if e2elatency <= 300:
        qoe = 1.0
    elif e2elatency <= 500.0:
        qoe = 0.3 + (500 - e2elatency) * (0.7/(500-300))
    elif e2elatency <= 700.0:
        qoe = (700 - e2elatency) * (0.3/(700-500))
    else:
        qoe = 0.0
    return qoe

def qoe_latency_slope(e2elatency):
    qoe = 0.0
    if e2elatency <= 300:
        qoe = 0.0
    elif e2elatency <= 500.0:
        qoe = (0.7/(500-300))
    elif e2elatency <= 700.0:
        qoe = (0.3/(700-500))
    else:
        qoe = 0.0
    return qoe

def qoe_latency_test(e2elatency):
    qoe = 0.0
    if e2elatency <= 300:
        qoe = 1.0
    elif e2elatency <= 550.0:
        qoe = 0.2 + (550 - e2elatency) * (0.8/(550-300))
    elif e2elatency <= 900.0:
        qoe = 0.1 + (900 - e2elatency) * (0.1/(900-550))
    else:
        qoe = 0.1
    return qoe

# def qoe_latency(e2elatency):
#     qoe = 0.0
#     if e2elatency <= 300:
#         qoe = 1.0
#     elif e2elatency <= 500.0:
#         qoe = 0.3 + (500 - e2elatency) * (0.7/(500-300))
#     elif e2elatency <= 700.0:
#         qoe = 0.1 + (700 - e2elatency) * (0.2/(700-500))
#     else:
#         qoe = 0.1
#     return qoe


#
# def qoe_latency(e2elatency):
#
#     for i in range(0, 15): #21 for desktop-SR, 29 for mobile-SR, 90 for desktop-GAMEPDP, 56 for mobile-GAMEPDP, #20 for qoe_curve_final, #15 for qoe_bins
#         if(curve_data[i][0] > int(e2elatency)):
#             break
#     diffXTotal = curve_data[i][0] - curve_data[i-1][0]
#     diffYTotal = curve_data[i-1][1] - curve_data[i][1]
#     diffX = int(e2elatency) - curve_data[i-1][0]
#     session = curve_data[i-1][1] - (diffX/diffXTotal*diffYTotal) + 0.0
#
#     return session