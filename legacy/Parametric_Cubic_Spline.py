import math
import numpy as np

delta = 0.05 #shifts initial max thickness aft
PIRAD = 3.14159
TWOPI = 2 * PIRAD
RqD = PIRAD / 180

Np = 6 #number of points
tau_S = np.array(np.zeros(Np)) #plus one because 1 to n is preferred
zet_S = np.array(np.zeros(Np))
chi_S = np.array(np.zeros(Np))

#these points are USER INPUTS
tau_S[0] = 0.00
tau_S[1] = 0.03
tau_S[2] = 0.19
tau_S[3] = 0.50
tau_S[4] = 0.88
tau_S[5] = 1.00

zet_S[0] = 0.00
zet_S[1] = 0.0007
zet_S[2] = -0.049
zet_S[3] = 0.00
zet_S[4] = 0.0488
zet_S[5] = 0.00

Left_to_Right = 1
n = Np - 1
c = np.array(np.zeros(n))
X = np.array(np.zeros(Np))
Y = np.array(np.zeros(Np))

for i in range(0,Np):
    X[i] = tau_S[i]
    Y[i] = zet_S[i]

#call polynomial
Xo = X[0]
Yo = Y[0]
Xn = X[n]
Yn = Y[n]

A = np.matrix(np.zeros((n,n)))
B = np.matrix(np.zeros((n,1)))

for i in range(0, n):
    if(Left_to_Right == 1):
        B[i] = Y[i+1] - Yo
    else:
        B[i] = Y[n-i] - Yn
    for j in range(0, n):
        if(Left_to_Right == 1):
            A[i,j] = (X[i+1] - Xo) ** (j+1)
        else:
            A[i,j] = (X[n] - Xn) ** (j+1)

#call gauss and solve

coefficient = np.linalg.solve(A,B)
y_equation = "1-(1-"+str(delta)+")*sin(pi*u)+"+str(delta)+"*sin(3*pi*u)"

z_equation = ""
for i in range(1,n+1):
    z_equation = z_equation + str(coefficient.item(i-1)) + "*u**"+str(i)
    if(i != n):
        z_equation = z_equation + "+"

print(z_equation)
print(y_equation)
