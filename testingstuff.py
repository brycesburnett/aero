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
import xlrd
#location of points excel sheet
file_location = "C:/points.xlsx"

#constants
PIRAD = 3.14159
TWOPI = 2 * PIRAD
RqD = PIRAD / 180
TAU_DEFAULT = "0.0, 0.03, 0.19, 0.50, 0.88, 1.00"
ZETA_DEFAULT = "0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00"

def getTauPoints():
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)
    tauString = ""
    for i in range(1,7):
        if i == 6:
            tauString += str(sheet.cell_value(i,0))
        else:
            tauString += str(sheet.cell_value(i,0))+','
    return tauString;

def getZetaPoints():
    workbook = xlrd.open_workbook(file_location)
    sheet = workbook.sheet_by_index(0)
    zetaString =""
    for i in range(1,7):
        if i == 6:
            zetaString += str(sheet.cell_value(i,1))
        else:
            zetaString += str(sheet.cell_value(i,1))+','
    return zetaString;

#returns True if points are valid 
def validateUserPoints(t_points, z_points):
    for i in range(0, len(t_points)):
        try:
            numb = float(t_points[i])
        except:
            return False
    return True

#pass in two strings (user input points) and boolean
#returns an array of two matrices (A and B)
#index 0 = A, index 1 = B
#if useExcelPoints is true then try to get excel points
#else an error most likely occurred and we can bypass trying excel
def defineMatrices(t_points, z_points, useExcelPoints):
    if useExcelPoints:
         #try to get points from excel sheet
        try:
            t_pointsExc = getTauPoints()
            z_pointsExc = getZetaPoints()
            #split these points with , as delimiter if valid
            if validateUserPoints(t_pointsExc, z_pointsExc):
                t_points = t_pointsExc.split(',')
                z_points = z_pointsExc.split(',')
                print("Excel values imported.")
            #else we dont bother using them
            
        except:
            #error finding excel file
            #so tau/zeta points arent reassigned
            print("Error with excel values or finding file")
            t_points = t_points.split(',')
            z_points = z_points.split(',')
            pass
    else:
        t_points = t_points.split(',')
        z_points = z_points.split(',')

    Np = len(z_points)
    t_array = np.array(np.zeros(Np))
    z_array = np.array(np.zeros(Np))
    c_array = np.array(np.zeros(Np))

    #fill arrays
    for i in range(0, len(t_points)):
        t_array[i] = t_points[i]
        z_array[i] = z_points[i]
	delta = 0.5
        c_array[i] = 1 - (1 - delta) * math.sin(PIRAD * t_array[i])

    Left_to_Right = 1
    n = Np - 1
    c = np.array(np.zeros(n))
    X = np.array(np.zeros(Np))
    Y = np.array(np.zeros(Np))
    for i in range(0,Np):
        X[i] = t_array[i]
        Y[i] = z_array[i]

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
    #place A and B matrices into an array to be accessed later
    AB = [A,B]
    return AB

def add_wings(delta, chi_eq, tau_points, zeta_points, washout, washout_displacement, wing_length, wing_displacement):
    #passing in tau and zeta points, and true to check excel file
    Np = len(zeta_points)
    n = Np - 1
    AB = defineMatrices(tau_points, zeta_points, True)
    A = AB[0]
    B = AB[1]
    try:
        coefficient = np.linalg.solve(A,B) #Executes code from the gauss and solve functions
    except:
        print("Problem with user inputs causing Singular matrix error")
        print("Now using default input points...")
        #passing in default tau and zeta points
        #False so the function knows not to waste time by
        #going through excel points
        AB = defineMatrices(TAU_DEFAULT, ZETA_DEFAULT, False)
        A = AB[0]
        B = AB[1]
        coefficient = np.linalg.solve(A,B)
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
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default=TAU_DEFAULT)
    zeta_points = StringProperty(name="Zeta points", description="User input points", default=ZETA_DEFAULT)
    washout = FloatProperty(name="Washout", default = 0.2)
    washout_displacement = FloatProperty(name="Washout displacement", default = 0.65)
    wing_length = FloatProperty(name="Adjust wing length", default =6.0, min = 3.00)
    wing_displacement = FloatProperty(name="Adjust wing displacement", default = 12.00, min =0.00)
    
    def execute(self, context):
        ob = add_wings(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.washout, self.washout_displacement, self.wing_length, self.wing_displacement)
        #context.scene.objects.link(ob)
        #context.scene.objects.active = ob
        return {'FINISHED'}
 
