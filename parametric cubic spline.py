import math
import numpy as np

number_of_points = 4

#THESE ARE JUST STRINGS
#tau_points = "0.0, 0.5, 0.83666, 1.0"
#x_points_string = "0.0, 0.25, 0.7, 1.0"
w = "0.005, 0.08, 0.04, 0.005"
upper_points = "0.0, 0.2, 0.19, 0.16"
equator_points = "0.0, 0.05, 0.15, 0.15"
lower_points = "0.0, 0.0, 0.11, 0.14"

#TEST TAU and X
tau_points = "0.0, 0.3333, 0.6666, 1.0"
x_points_string = "0.0, 0.6, 0.4, 1.0"

#THESE ARE THE ARRAYS TO BE USED IN GENERATION
time = np.array(np.zeros(number_of_points))
xx = np.array(np.zeros(number_of_points))

tau_points = tau_points.split(',')
x_points_string = x_points_string.split(',')
for i in range(0, len(tau_points)):
    time[i] = tau_points[i]
    xx[i] = x_points_string[i]

left_end_constraint = 0
right_end_constraint = 4.5

#Call CS_solve(np, t_s(), x_s(), dxdt_s(), d2xdt2_s(), exL, exR) ' solve for 2nd derivatives x(t)

velocity = np.array(np.zeros(number_of_points))
acceleration = np.array(np.zeros(number_of_points))

number_of_splines = number_of_points - 1

DEL = np.array(np.zeros(number_of_splines))
eps = np.array(np.zeros(number_of_splines))

for i in range(0, number_of_splines):
    DEL[i] = time[i+1] - time[i]
    eps[i] = xx[i+1] - xx[i]


FF = np.matrix(np.zeros((number_of_points,number_of_points)))
BB = np.array(np.zeros(number_of_points))

if(number_of_points < 4 and left_end_constraint == 2):
    left_end_constraint = 1
if(number_of_points < 4 and right_end_constraint == 2):
    right_end_constraint = 1

vL = 0
vR = 0

#INFLUENCE COEFFICIENT MATRIX
if(left_end_constraint != 0 and left_end_constraint != 1 and left_end_constraint != 2):
    vL = left_end_constraint
    left_end_constraint = 3
if(right_end_constraint != 0 and right_end_constraint != 1 and right_end_constraint != 2):
    vR = right_end_constraint
    right_end_constraint = 3

for i in range(0, number_of_points):
    for j in range(0, number_of_points):
        FF[i,j] = 0
        if(left_end_constraint == 1 and i == 0 and j == 0):
            FF[i,j] = 1
        elif((left_end_constraint == 3 or left_end_constraint == 0) and i == 0 and j == 0):
            FF[i,j] = DEL[0] / 3
        elif((left_end_constraint == 3 or left_end_constraint == 0) and i == 0 and j == 1):
            FF[i,j] = DEL[0] / 6
        elif(left_end_constraint == 2 and i == 0 and j == 0):
            FF[i,j] = 1
        elif(left_end_constraint == 2 and i == 0 and j == 1):
            FF[i,j] = -1 - DEL[0] / DEL[1]
        elif(left_end_constraint == 2 and i == 0 and j == 2):
            FF[i,j] = DEL[0] / DEL[1]
        elif(i > 0 and i < number_of_points - 1):
            if(j == i-1):
                FF[i,j] = DEL[i-1] / 6
            elif(j == i):
                FF[i,j] = (DEL[i-1] + DEL[i]) / 3
            elif(j == i+1):
                FF[i,j] = DEL[i] / 6
        elif(right_end_constraint == 1 and i == number_of_points - 1 and j == number_of_points - 1):
            FF[i,j] = 1
        elif((right_end_constraint == 3 or right_end_constraint == 0) and i == number_of_points - 1 and j == number_of_points - 2):
            FF[i,j] = -DEL[number_of_splines - 1] / 6
        elif((right_end_constraint == 3 or right_end_constraint == 0) and i == number_of_points - 1 and j == number_of_points - 1):
            FF[i,j] = -DEL[number_of_splines - 1] / 3
        elif(right_end_constraint == 2 and i == number_of_points - 1 and j == number_of_points - 1):
            FF[i,j] = 1
        elif(right_end_constraint == 2 and i == number_of_points - 1 and j == number_of_points - 2):
            FF[i,j] = -1 - DEL[number_of_points - 2] / DEL[number_of_points - 3]
        elif(right_end_constraint == 2 and i == number_of_points - 1 and j == number_of_points - 3):
            FF[i,j] = DEL[number_of_points - 2] / DEL[number_of_points - 3]
    BB[i] = 0
    if(left_end_constraint == 1 and i == 0):
        BB[i] = 0
    elif((left_end_constraint == 3 or left_end_constraint == 0) and i == 0):
        BB[i] = eps[0] / DEL[0] - vL
    elif(left_end_constraint == 2 and i == 0):
        BB[i] = 0
    elif(i > 0 and i < number_of_points - 1):
        BB[i] = eps[i] / DEL[i] - eps[i - 1] / DEL[i - 1]
    elif(right_end_constraint == 1 and i == number_of_points - 1):
        BB[i] = 0
    elif((right_end_constraint == 3 or right_end_constraint == 0) and i == number_of_points - 1):
        BB[i] = eps[number_of_splines - 1] / DEL[number_of_splines - 1] - vR
    elif(right_end_constraint == 2 and i == number_of_splines - 1):
        BB[i] = 0

acceleration = np.linalg.solve(FF,BB)
#1st derivatives
for i in range(0, number_of_points):
    if(i < number_of_points - 1):
        velocity[i] = eps[i] / DEL[i] - acceleration[i] * DEL[i] / 3 - acceleration[i+1] * DEL[i] / 6
    else:
        velocity[i] = velocity[number_of_splines-1] + acceleration[number_of_splines-1] * DEL[number_of_splines-1] / 2 + acceleration[number_of_points-1] * DEL[number_of_splines-1] / 2
        
#interp
vert = 41
holder = np.array(np.zeros(number_of_points))
for i in range(0, vert):
    to_ = i / (vert - 1)
    if (to_ < time[0]):
        xo_ = xx[0] + velocity[0] * (to_ - time[0])
        vvo = velocity[0] + acceleration[0] * (to_ - time[0])
        d3xdt3 = (acceleration[1] - acceleration[0]) / DEL[0]
        aao = acceleration[0] + d3xdt3 * (to_ - time[0])
    elif(to_ > time[number_of_points-1]):
        xo_ = xx[number_of_points-1] + velocity[number_of_points-1] * (to_ - time[number_of_points - 1])
        vvo = velocity[number_of_points - 1] + acceleration[number_of_points-1] * (to_ - time[number_of_points - 1])
        d3xdt3 = (acceleration[number_of_points - 1] - acceleration[number_of_points - 2]) / DEL[number_of_splines-1]
        aao = acceleration[0] + d3xdt3 * (to_ - time[0])
    else:
        for j in range(0, number_of_splines):
            if(time[j+1] >= to_):
                tmti = to_ - time[j]
                epsi = eps[j]
                DELI = DEL[j]
                xxi = xx[j]
                aai = acceleration[j]
                dxdti = velocity[j]
                aip1 = acceleration[j+1]
                xo_ = xxi + dxdti * tmti + aai * tmti ** 2 / 2 + (aip1 - aai) * tmti ** 3 / (6 * DELI)
                vvo = dxdti + aai * tmti + (aip1 - aai) * tmti ** 2 / (2 * DELI)                                                                   
                aao = aai + (aip1 - aai) * tmti / DELI
                break
    print(vvo)

