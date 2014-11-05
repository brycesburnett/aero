#This code is needed for an addon as well as deleting the if __name__ statement at the bottom.
bl_info = {
    "name": "Add Wing",
	"author": "CSULB CECS 491 Team 4",
	"version": (1, 0),
	"description": "Generates a single wing using parametric cubic splines.",
	"category": "Object"
}

import bpy, math
import numpy as np
import xlrd
#location of points excel sheet
file_location = "C:/points.xlsx"

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
    

def add_wing(delta, chi_eq, tau_points, zeta_points, washout, washout_displacement, wing_length, x_location, y_location, z_location):

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
    bpy.context.object.rotation_euler[1] = 1.5708
    bpy.context.space_data.cursor_location[0] = x_location
    bpy.context.object.location[0] = x_location
    bpy.context.space_data.cursor_location[0] = y_location
    bpy.context.object.location[0] = y_location
    bpy.context.space_data.cursor_location[0] = z_location
    bpy.context.object.location[0] = z_location


#    User interface
#
 
from bpy.props import *
 
class Wing(bpy.types.Operator):
    '''Single Wing generator'''
    bl_idname = "mesh.wing_add"
    bl_label = "Add a wing"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    delta = FloatProperty(name="Delta", default=0.05)
    chi_eq = StringProperty(name="Chi parameterization", description="Equation to automatically parameterize Chi", default="1-(1-delta)*sin(pi*u)+delta*sin(3*pi*u)")
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default="0.0, 0.03, 0.19, 0.50, 0.88, 1.00")
    zeta_points = StringProperty(name="Zeta points", description="User input points", default="0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00")
    washout = FloatProperty(name="Washout", default = 0.16)
    washout_displacement = FloatProperty(name="Washout Displacement", default = 0.65)
    wing_length = FloatProperty(name="Adjust wing length", default =3.5, min = 3.00)
    x_location = FloatProperty(name="X location", default = 0)
    y_location = FloatProperty(name="Y location", default = 0)
    z_location = FloatProperty(name="Z location", default = 0)
    
    def execute(self, context):
        ob = add_wing(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.washout, self.washout_displacement, self.wing_length, self.x_location, self.y_location, self.z_location)
        #context.scene.objects.link(ob)
        #context.scene.objects.active = ob
        return {'FINISHED'}
 
#
#    Registration
#    Makes it possible to access the script from the Add > Mesh menu
#    Right now this is just a script, later on we will convert it into an addon
 
def menu_func(self, context):
    self.layout.operator("mesh.wing_add", 
        text="Wing")
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.INFO_MT_mesh_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)