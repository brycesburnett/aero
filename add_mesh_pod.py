#This code is needed for an addon as well as deleting the if __name__ statement at the bottom.
bl_info = {
    "name": "Add Pod",
	"author": "CSULB CECS 491 Team 4",
	"version": (1, 0),
	"description": "Generates a pod based on the input points.",
	"category": "Object"
}

import bpy, math
import numpy as np

def add_pod(delta, chi_eq, tau_points, zeta_points, smoothness):

    #Constants
    PIRAD = 3.14159
    TWOPI = 2 * PIRAD
    RqD = PIRAD / 180

    tau_points = tau_points.split(',') #Since inputs from Blender are a string, this splits the string on commas and makes a list
    zeta_points = zeta_points.split(',')
    Np = len(zeta_points) #Number of points
    tau_S = np.array(np.zeros(Np))
    zet_S = np.array(np.zeros(Np))
    chi_S = np.array(np.zeros(Np))

    #Fills the numpy arrays with the list values
    for i in range(0, len(tau_points)):
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
    bpy.context.object.scale[0] = 0.3
    bpy.context.object.scale[1] = 0.3
    bpy.context.object.scale[2] = 0.3


#    User interface
#
 
from bpy.props import *
 
class AddPod(bpy.types.Operator):
    '''Pod generator'''
    bl_idname = "mesh.pod_add"
    bl_label = "Add a pod"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    delta = FloatProperty(name="Delta", default=0.05)
    chi_eq = StringProperty(name="Chi Parameterization", description="Equation to automatically parameterize Chi", default="1-(1-delta)*sin(pi*u)+delta*sin(3*pi*u)")
    tau_points = StringProperty(name="Tau points", description="Independent variable 'Time'", default="0.0, 0.03, 0.19, 0.50, 0.88, 1.00")
    zeta_points = StringProperty(name="Zeta points", description="User input points", default="0.00, 0.0007, -0.049, 0.00, 0.0488, 0.00")
    smoothness = StringProperty(name="Smoothness", description="Smoothness of the pod", default = "32")
    
    def execute(self, context):
        ob = add_pod(self.delta, self.chi_eq, self.tau_points, self.zeta_points, self.smoothness)
        #context.scene.objects.link(ob)
        #context.scene.objects.active = ob
        return {'FINISHED'}
 
#
#    Registration
#    Makes it possible to access the script from the Add > Mesh menu
#    Right now this is just a script, later on we will convert it into an addon
 
def menu_func(self, context):
    self.layout.operator("mesh.pod_add", 
        text="Pod")
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.INFO_MT_mesh_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
