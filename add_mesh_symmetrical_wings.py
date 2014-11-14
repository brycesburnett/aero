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
file_location = "C:/points.csv"

#constants
PIRAD = 3.14159
TWOPI = 2 * PIRAD
RqD = PIRAD / 180
TAU_DEFAULT = "0.0, 0.03, 0.19, 0.50, 0.88, 1.00"
ZETA_DEFAULT = "0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00"

def getTauPoints():
    with open(file_location, 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        tauString = ""
        for i in range(1,7):
            if i == 6:
                tauString += mycsv[i][0]
            else:
                tauString += mycsv[i][0]+', '
        print("Tau: " + tauString)
        f.close()
    return tauString;

def getZetaPoints():
    with open(file_location, 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        zetaString = ""
        for i in range(1,7):
            if i == 6:
                zetaString += mycsv[i][1]
            else:
                zetaString += mycsv[i][1]+', '
        print("Zeta: " + zetaString)
        f.close()
    return zetaString;

#returns True if points are valid 
def validateUserPoints(t_points, z_points):
    t_split = t_points.split(',')
    z_split = z_points.split(',')
    for i in range(0, len(t_split)):
        try:
            numb = float(t_split[i])
        except ValueError:
            print("Tau point '" + t_split[i] + "'' is not a float.")
            return False
    for i in range(0, len(z_split)):
        try:
            numb = float(z_split[i])
        except ValueError:
            print("Zeta point '" + z_split[i] +"'' is not a float.")
            return False
    return True
#pass in two strings (user input points) and boolean
#returns an array of two matrices (A and B)
#index 0 = A, index 1 = B
#if useExcelPoints is true then try to get excel points
#else an error most likely occurred and we can bypass trying excel
def defineMatrices(delta, t_points, z_points, useExcelPoints):
    print("")
    fail = False
    if useExcelPoints:
        try:
            #try to get points from excel sheet
            t_pointsExc = getTauPoints()
            z_pointsExc = getZetaPoints()
            #TRY because we don't know if they're valid yet
            #split these points with , as delimiter if valid
            if validateUserPoints(t_pointsExc, z_pointsExc):
                t_points = t_points.split(',')
                z_points = z_points.split(',')
                print("Excel values imported.")
            #else we dont bother using them
            else:
                fail = True
                print("Error with excel values.")
        except:
            #error finding excel file
            #so tau/zeta points arent reassigned
            print("Error with excel values or finding file.")
            fail = True
            pass

        if  fail:
            print("Using Blender input points...")
            if validateUserPoints(t_points, z_points):
                t_points = t_points.split(',')
                z_points = z_points.split(',') 
            else:
                print("Error with Blender input points.")
                print("Using default points...")
                t_points = TAU_DEFAULT.split(',')
                z_points = ZETA_DEFAULT.split(',')
    else:
        print("Using Blender input points...")
        if validateUserPoints(t_points, z_points):
            t_points = t_points.split(',')
            z_points = z_points.split(',')
        else:
            print("Error with Blender input points")
            print("Using default points...")
            t_points = TAU_DEFAULT.split(',')
            z_points = ZETA_DEFAULT.split(',')
    
    print("\nTau: " + str(t_points))
    print("Zeta: " + str(z_points)+"\n")
    Np = len(z_points)
    t_array = np.array(np.zeros(Np))
    z_array = np.array(np.zeros(Np))
    c_array = np.array(np.zeros(Np))

    #fill arrays
    for i in range(0, len(t_points)):
        t_array[i] = t_points[i]
        z_array[i] = z_points[i]
    for i in range(0, Np):
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
    #passing references of Np and n in
    AB = [A,B, Np, n]
    return AB

def add_wings(delta, chi_eq, tau_points, zeta_points, washout, washout_displacement, wing_length, wing_displacement, location, rotation, scale):
    #passing in tau and zeta points, and true to check excel file when we have capability
    AB = defineMatrices(delta, tau_points, zeta_points, False)
    A = AB[0]
    B = AB[1]
    #references of Np and n
    Np = AB[2]
    n = AB[3]
    
    try:
        #Executes code from the gauss and solve functions
        coefficient = np.linalg.solve(A,B)
    except:
        print("Problem with user inputs causing Singular Matrix error.")
        print("Now using default input points...")
        #passing in default tau and zeta points
        #False so the function knows not to waste time by
        #going through excel points
        AB = defineMatrices(delta, TAU_DEFAULT, ZETA_DEFAULT, False)
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
    #join objects together
    for obs in bpy.context.scene.objects:
        if obs.name[0:3] == 'XYZ':
            obs.select = True
            bpy.context.scene.objects.active = obs
        else:
            obs.select = False
    bpy.ops.object.join()

    bpy.context.object.rotation_euler[1] = 1.5708
    
    #LOCATION
    print(bpy.context.object.location)
    bpy.context.object.location[0] = location[0]
    bpy.context.object.location[1] = location[1]
    bpy.context.object.location[2] = location[2]

    #ROTATION
    #converts degree values into radians
    for i in range (0,3):
        rotation[i] = math.radians(rotation[i])
    bpy.context.object.rotation_euler[0] = rotation[0]
    bpy.context.object.rotation_euler[1] = rotation[1]
    bpy.context.object.rotation_euler[2] = rotation[2]

    #SCALE
    bpy.context.object.scale[0] = scale[0]
    bpy.context.object.scale[1] = scale[1]
    bpy.context.object.scale[2] = scale[2]

#---------------------------------------------------
from bpy.props import *
 
class SymmetricalWings(bpy.types.Operator):
    '''Symmetrical wing generator'''
    bl_idname = "mesh.symmetrical_wings_add"
    bl_label = "Add symmetrical wings"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    idname = StringProperty(name="Unique Identifier", default = "Symmetrical Wings")
    delta = FloatProperty(name="Delta", default=0.05)
    chi_eq = StringProperty(name="Chi parameterization", description="Equation to automatically parameterize Chi", default="1-(1-delta)*sin(pi*u)+delta*sin(3*pi*u)")
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default="0.0, 0.03, 0.19, 0.50, 0.88, 1.00")
    zeta_points = StringProperty(name="Zeta points", description="User input points", default="0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00")
    washout = FloatProperty(name="Washout", default = 0.2)
    washout_displacement = FloatProperty(name="Washout displacement", default = 0.65)
    wing_length = FloatProperty(name="Adjust wing length", default =6.0, min = 3.00)
    wing_displacement = FloatProperty(name="Adjust wing displacement", default = 12.00, min =0.00)

    location = FloatVectorProperty(name="Location", default = (0.0, 0.0, 0.0), subtype='XYZ')
    rotation = FloatVectorProperty(name="Rotation", default = (0.0, 0.0, 0.0), subtype='XYZ')
    scale = FloatVectorProperty(name="Scale", default = (1.0, 1.0, 1.0), subtype='XYZ')

    def draw(self, context):
        layout = self.layout
        col = layout.column()
        #replace this comment with input box and check box for excel filepath
        layout.prop(self, "idname")
        layout.prop(self, "delta")
        layout.prop(self, "chi_eq")
        layout.prop(self, "tau_points")
        layout.prop(self, "zeta_points")
        layout.prop(self, "washout")
        layout.prop(self, "washout_displacement")
        layout.prop(self, "wing_length")
        layout.prop(self, "location")
        layout.prop(self, "rotation")
        layout.prop(self, "scale")
        
    def execute(self, context):
        ob = add_wings(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.washout, self.washout_displacement, self.wing_length, self.wing_displacement, self.location, self.rotation, self.scale)
        ob = bpy.context.active_object
        ob["component"] = "symmetrical wings"
        ob["delta"] = self.delta
        ob["chi_eq"] = self.chi_eq
        ob["tau_points"] = self.tau_points
        ob["zeta_points"] = self.zeta_points
        ob["washout"] = self.washout
        ob["washout_displacement"] = self.washout_displacement
        ob["wing_displacement"] = self.wing_displacement
        ob["wing_length"] = self.wing_length
        ob.name = self.idname
        ob["identifier"] = self.idname
        bpy.ops.view3d.obj_search_refresh()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class updateSymmetricalWing(bpy.types.Operator):
    bl_idname = "mesh.symmetrical_wings_update"
    bl_label = "Update symmetrical wings"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager.MyProperties
        scn = context.scene
        for obj in scn.objects:
            if obj.select == True:
                ob = obj
                break
        newOb = add_wings(ob["delta"], ob["chi_eq"], ob["tau_points"], ob["zeta_points"], ob["washout"], ob["washout_displacement"], ob["wing_length"], ob["wing_displacement"], ob.location, ob.rotation_euler, ob.scale)
        newOb = bpy.context.active_object
        newOb.name = ob.name
        newOb["component"] = "symmetrical wings"
        newOb["delta"] = ob["delta"]
        newOb["chi_eq"] = ob["chi_eq"]
        newOb["tau_points"] = ob["tau_points"]
        newOb["zeta_points"] = ob["zeta_points"]
        newOb["washout"] = ob["washout"]
        newOb["wing_displacement"] = ob["wing_displacement"]
        newOb["washout_displacement"] = ob["washout_displacement"]
        newOb["wing_length"] = ob["wing_length"]
        ob.select = True
        newOb.select = False
        bpy.ops.object.delete()
        newOb = bpy.context.active_object
        wm.srch_index = -1
        bpy.ops.view3d.obj_search_refresh()
        return {'FINISHED'}

class deleteSymmetricalWings(bpy.types.Operator):
    bl_idname = "mesh.symmetrical_wings_delete"
    bl_label = "Delete symmetrical wings? (Click elsewhere to cancel.)"
    bl_options = {'INTERNAL'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

    def execute(self, context):
        wm = context.window_manager.MyProperties
        scn = context.scene
        for obj in scn.objects:
            if obj.select == True:
                ob = obj
        bpy.ops.object.delete()
        wm.srch_index = -1
        bpy.ops.view3d.obj_search_refresh()
        return {'FINISHED'}

class symmetricalWingsTexture(bpy.types.Operator):
    bl_idname = "mesh.symmetrical_wings_texture"
    bl_label = "Add Texture"
    bl_options = {'INTERNAL'}
 
