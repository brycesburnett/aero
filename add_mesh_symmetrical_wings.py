#This code is needed for an addon as well as deleting the if __name__ statement at the bottom.
bl_info = {
    "name": "Add Symmetrical Wings",
	"author": "CSULB CECS 491 Team 4",
	"version": (1, 0),
	"description": "Generates two symmetrical wings using parametric cubic splines.",
	"category": "Object"
}

import bpy, math
import numpy as np
import csv
#location of points excel sheet
file_location = "C:/points.xlsx"

def getTauPoints():
    with open(file_location, 'rb') as f:
    	mycsv = csv.reader(f)
    	mycsv = list(mycsv)
    	tauString = ""
    	for i in range(1,7):
            if i == 6:
                tauString += mycsv[i][0]
            else:
                tauString += mycsv[i][0]+','
    return tauString;

def getZetaPoints():
    with open(file_location, 'rb') as f:
    	mycsv = csv.reader(f)
    	mycsv = list(mycsv)
    	zetaString = ""
    	for i in range(1,7):
            if i == 6:
                zetaString += mycsv[i][1]
            else:
                zetaString += mycsv[i][1]+','
    return zetaString;
    

def add_wings(delta, chi_eq, tau_points, zeta_points, washout, washout_displacement, wing_length, wing_displacement):

    #Constants
    PIRAD = 3.14159
    TWOPI = 2 * PIRAD
    RqD = PIRAD / 180

    #try to get points from excel sheet
    try:
        tau_pointsExcel = getTauPoints()
        zeta_pointsExcel = getZetaPoints()
        #split these points with , as delimiter
        tau_pointsExcel = tau_pointsExcel.split(',')
        zeta_pointsExcel = zeta_pointsExcel.split(',')
        #doesnt mean points are correct data type though
    except:
        #error finding excel file
        #so tau/zeta points arent reassigned
        pass
    #Since inputs from Blender are a string, this splits the string on commas and makes a list
    tau_points = tau_points.split(',') 
    zeta_points = zeta_points.split(',')

    Np = len(zeta_points) #Number of points
    tau_S = np.array(np.zeros(Np))
    zet_S = np.array(np.zeros(Np))
    chi_S = np.array(np.zeros(Np))

    #Fills the numpy arrays with the list values
    
    try:
        for i in range(0, len(tau_pointsExcel)):
            #using excel points
            #there could still be an error with the data type of the value so check the array of points from excel
            tau_S[i] = tau_pointsExcel[i]
            zet_S[i] = zeta_pointsExcel[i]
    except:
    	#error found in excel points, revert to original
        for i in range(0, len(tau_points)):
            #using default points if theres a problem with excel points
            tau_S[i] = tau_points[i]
            zet_S[i] = zeta_points[i]

    #Executes code from the tau_chi function
    for i in range(0, Np):
        chi_S[i] = 1 - (1 - delta) * math.sin(PIRAD * tau_S[i])

    Left_to_Right = 1
    n = Np - 1
    c = np.array(np.zeros(n))
    X = np.array(np.zeros(Np))
    Y = np.array(np.zeros(Np))

    for i in range(0,Np):
        X[i] = tau_S[i] #Probably didn't need to make a new array for these, just following the VB code
        Y[i] = zet_S[i]

    #Executes code from the polyomial function
    Xo = X[0]
    Yo = Y[0]
    Xn = X[n]
    Yn = Y[n]

    A = np.matrix(np.zeros((n,n))) #Creates the arrays to solve the matrices
    B = np.matrix(np.zeros((n,1)))

    for i in range(0, n): #The following code influences the matrices so that they can be solved for the equations
        if(Left_to_Right == 1):
            B[i] = Y[i+1] - Yo
        else:
            B[i] = Y[n-i] - Yn
        for j in range(0, n):
            if(Left_to_Right == 1):
                A[i,j] = (X[i+1] - Xo) ** (j+1)
            else:
                A[i,j] = (X[n] - Xn) ** (j+1)

    coefficient = np.linalg.solve(A,B) #Executes code from the gauss and solve functions

    #The following code turns the coefficient results into strings that can be used by Blender to generate the object.
    #There are three equations, Chi is the y axis, Zeta is the z axis, and x has its own equation that makes each cross section smaller.
    #This code makes a cross section along the y and z axis, for fuselage you'd probably want a cross section along different axes.
    x_equation = "v-" + str(wing_length)
    y_equation = "(" + chi_eq.replace("delta", str(delta))
    y_equation = y_equation + ")*" + str(washout) + "*v-" + str(washout_displacement) + "*v"
    z_equation = "("
    for i in range(1,n+1):
        z_equation = z_equation + str(coefficient.item(i-1)) + "*u**"+str(i)
        if(i != n):
            z_equation = z_equation + "+"
        else:
            z_equation = z_equation + ")*" + str(washout) + "*v"

    #This line actually creates the object
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq=x_equation, y_eq=y_equation, z_eq=z_equation, range_u_min=0, range_u_max=1, range_u_step=32, wrap_u=True, range_v_min=3, range_v_max=wing_length, close_v=True)
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="-"+x_equation+"+"+str(wing_displacement), y_eq=y_equation, z_eq=z_equation, range_u_min=0, range_u_max=1, range_u_step=32, wrap_u=True, range_v_min=3, range_v_max=wing_length, close_v=True)
    
#    User interface
#
 
from bpy.props import *
 
class SymmetricalWings(bpy.types.Operator):
    '''Symmetrical wing generator'''
    bl_idname = "mesh.symmetrical_wings_add"
    bl_label = "Add symmetrical wings"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    delta = FloatProperty(name="Delta", default=0.05)
    chi_eq = StringProperty(name="Chi parameterization", description="Equation to automatically parameterize Chi", default="1-(1-delta)*sin(pi*u)+delta*sin(3*pi*u)")
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default="0.0, 0.03, 0.19, 0.50, 0.88, 1.00")
    zeta_points = StringProperty(name="Zeta points", description="User input points", default="0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00")
    washout = FloatProperty(name="Washout", default = 0.2)
    washout_displacement = FloatProperty(name="Washout displacement", default = 0.65)
    wing_length = FloatProperty(name="Adjust wing length", default =6.0, min = 3.00)
    wing_displacement = FloatProperty(name="Adjust wing displacement", default = 12.00, min =0.00)
    
    def execute(self, context):
        ob = add_wings(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.washout, self.washout_displacement, self.wing_length, self.wing_displacement)
        ob = bpy.context.active_object
        ob["component"] = "symmetrical wings"
        ob.name = "Symmetrical Wings"
        return {'FINISHED'}
 
