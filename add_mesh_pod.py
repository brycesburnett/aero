#This code is needed for an addon as well as deleting the if __name__ statement at the bottom.
bl_info = {
    "name": "Add Pod",
    "author": "CSULB CECS 491 Team 4",
    "version": (1, 0),
    "description": "Generates a pod using parametric cubic splines.",
    "category": "Object"
}

import bpy, math
import numpy as np
import csv

#constants
PIRAD = 3.14159
TWOPI = 2 * PIRAD
RqD = PIRAD / 180
TAU_DEFAULT = "0.0, 0.03, 0.19, 0.50, 0.88, 1.00"
ZETA_DEFAULT = "0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00"

def getTauPoints(file_location):
    with open(file_location, 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        tauString = ""
        for i in range(1,7):
            if i == 6:
                tauString += mycsv[i][0]
            else:
                tauString += mycsv[i][0]+', '
        f.close()
    return tauString;

def getZetaPoints(file_location):
    with open(file_location, 'r') as f:
        mycsv = csv.reader(f)
        mycsv = list(mycsv)
        zetaString = ""
        for i in range(1,7):
            if i == 6:
                zetaString += mycsv[i][1]
            else:
                zetaString += mycsv[i][1]+', '
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
            bpy.ops.error.message('INVOKE_DEFAULT', type = "Error", message = "Tau point '" + t_split[i] + "'' is not a float.")
            return False
    for i in range(0, len(z_split)):
        try:
            numb = float(z_split[i])
        except ValueError:
            bpy.ops.error.message('INVOKE_DEFAULT', type = "Error", message = "Zeta point '" + z_split[i] +"'' is not a float.")
            return False
    return True

def defineMatrices(delta, t_points, z_points, useExcelPoints, file_location):
    print("")
    fail = False
    if useExcelPoints:
        try:

            #try to get points from excel sheet
            t_pointsExc = getTauPoints(file_location)
            z_pointsExc = getZetaPoints(file_location)
            #TRY because we don't know if they're valid yet
            #split these points with , as delimiter if valid
            if validateUserPoints(t_pointsExc, z_pointsExc):
                t_points = t_pointsExc.split(',')
                z_points = z_pointsExc.split(',')
                print("Excel values imported from "+file_location+ ".")
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

def add_pod(delta, chi_eq, tau_points, zeta_points, smoothness, location, rotation, scale, file_location, isUpdate):

    #passing in tau and zeta points, and true to check excel file when we have capability
    AB = defineMatrices(delta, tau_points, zeta_points, True, file_location)
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
        AB = defineMatrices(delta, TAU_DEFAULT, ZETA_DEFAULT, False, file_location)
        A = AB[0]
        B = AB[1]
        coefficient = np.linalg.solve(A,B)

    #The following code turns the coefficient results into strings that can be used by Blender to generate the object.
    #There are three equations, Chi is the y axis, Zeta is the z axis, and x has its own equation that makes each cross section smaller.
    #This code makes a cross section along the y and z axis, for fuselage you'd probably want a cross section along different axes.
    x_equation = "0"
    y_equation = chi_eq.replace("delta", str(delta))
    z_equation = "("
    for i in range(1,n+1):
        z_equation = z_equation + str(coefficient.item(i-1)) + "*u**"+str(i)
        if(i != n):
            z_equation = z_equation + "+"
        else:
            z_equation = z_equation + ")"
    
    #This line actually creates the object
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq=x_equation, y_eq=y_equation, z_eq=z_equation, range_u_min=0, range_u_max=1, range_u_step=32, wrap_u=False, range_v_min=0, range_v_max=3, close_v=True)
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.spin(steps=int(smoothness), angle=6.28319, center=(0, 0, 0), axis=(0, 1, 0))
    bpy.ops.mesh.remove_doubles()
    bpy.ops.object.mode_set(mode='OBJECT')
    print("Pod created successfully.")

    #LOCATION
    bpy.context.object.location[0] = location[0]
    bpy.context.object.location[1] = location[1]
    bpy.context.object.location[2] = location[2]

    #ROTATION
    #no need to convert to euler since they have previously been converted at initial creation
    if isUpdate:
        bpy.context.object.rotation_euler[0] = rotation[0]
        bpy.context.object.rotation_euler[1] = -rotation[1]
        bpy.context.object.rotation_euler[2] = rotation[2]
    else:
        #this is the first time they're being set, must eulify!
        for i in range (0,3):
            rotation[i] = math.radians(rotation[i])
        bpy.context.object.rotation_euler[0] = rotation[0]
        bpy.context.object.rotation_euler[1] = -rotation[1]
        bpy.context.object.rotation_euler[2] = rotation[2]

    #SCALE
    bpy.context.object.scale[0] = scale[0]
    bpy.context.object.scale[1] = scale[1]
    bpy.context.object.scale[2] = scale[2]

#    User interface
#
 
from bpy.props import *
 
class Pod(bpy.types.Operator):
    '''Pod generator'''
    bl_idname = "mesh.pod_add"
    bl_label = "Add a pod"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    
    idname = StringProperty(name="Unique identifier", default="Pod")
    file_location = StringProperty(name="File Location", default = "C:/points.csv")
    delta = FloatProperty(name="Delta", default=0.05)
    chi_eq = StringProperty(name="Chi parameterization", description="Equation to automatically parameterize Chi", default="1-(1-delta)*sin(pi*u)+delta*sin(3*pi*u)")
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default="0.0, 0.03, 0.19, 0.50, 0.88, 1.00")
    zeta_points = StringProperty(name="Zeta points", description="User input points", default="0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00")
    smoothness = StringProperty(name="Smoothness", description="Smoothness of the pod", default = "32")

    location = FloatVectorProperty(name="Location", default = (0.0, 0.0, 0.0), subtype='XYZ')
    rotation = FloatVectorProperty(name="Rotation", default = (0.0, 0.0, 0.0), subtype='XYZ')
    scale = FloatVectorProperty(name="Scale", default = (1.0, 1.0, 1.0), subtype='XYZ')

    
    def draw(self, context):
       layout = self.layout
       col = layout.column()
       #replace this comment with input box and check box for excel filepath
       layout.prop(self, "idname")
       layout.prop(self, "file_location")
       layout.prop(self, "delta")
       layout.prop(self, "chi_eq")
       layout.prop(self, "tau_points")
       layout.prop(self, "zeta_points")
       layout.prop(self, "smoothness")
       layout.prop(self, "location")
       layout.prop(self, "rotation")
       layout.prop(self, "scale")
 
                
    def execute(self, context):
        ob = add_pod(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.smoothness, self.location, self.rotation, self.scale, self.file_location, False)
        ob = bpy.context.active_object
        ob["component"] = "pod"
        ob["file_location"] = self.file_location
        ob["delta"] = self.delta
        ob["chi_eq"] = self.chi_eq
        ob["tau_points"] = self.tau_points
        ob["zeta_points"] = self.zeta_points
        ob["smoothness"] = self.smoothness
        ob.name = self.idname
        bpy.ops.view3d.obj_search_refresh()
        return {'FINISHED'}

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)

class updatePod(bpy.types.Operator):
    bl_idname = "mesh.pod_update"
    bl_label = "Update a pod"
    bl_options = {'INTERNAL'}

    def execute(self, context):
        wm = context.window_manager.MyProperties
        scn = context.scene
        for obj in scn.objects:
            if obj.select == True:
                ob = obj
        newOb = add_pod(ob["delta"], ob["chi_eq"], ob["tau_points"], ob["zeta_points"], ob["smoothness"], ob.location, ob.rotation_euler, ob.scale, ob["file_location"], True)
        newOb = bpy.context.active_object
        newOb.name = ob.name
        newOb["component"] = "pod"
        newOb["delta"] = ob["delta"]
        newOb["chi_eq"] = ob["chi_eq"]
        newOb["tau_points"] = ob["tau_points"]
        newOb["zeta_points"] = ob["zeta_points"]
        newOb["smoothness"] = ob["smoothness"]
        newOb["file_location"] = ob["file_location"]
        ob.select = True
        newOb.select = False
        bpy.ops.object.delete()
        newOb = bpy.context.active_object
        wm.srch_index = -1
        bpy.ops.view3d.obj_search_refresh()
        return {'FINISHED'}

class deletePod(bpy.types.Operator):
    bl_idname = "mesh.pod_delete"
    bl_label = "Delete pod? (Click elsewhere to cancel.)"
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

#Add texture - doesn't do anything yet 
class podTexture(bpy.types.Operator):
    bl_idname = "mesh.pod_texture"
    bl_label = "Add Texture"
    bl_options = {'INTERNAL'}



class MessageOperator(bpy.types.Operator):
    bl_idname = "error.message"
    bl_label = "Message"
    type = StringProperty()
    message = StringProperty()
 
    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_popup(self, width=400, height=200)
 
    def draw(self, context):
        self.layout.label("A message has arrived")
        row = self.layout.split(0.25)
        row.prop(self, "type")
        row.prop(self, "message")
        row = self.layout.split(0.80)
        row.label("") 
        row.operator("error.ok")
 
#
#   The OK button in the error dialog
#
class OkOperator(bpy.types.Operator):
    bl_idname = "error.ok"
    bl_label = "OK"
    def execute(self, context):
        return {'FINISHED'}

bpy.utils.register_class(OkOperator)
bpy.utils.register_class(MessageOperator)
