import bpy, math
import numpy as np

def addWing(X1,X2,X3,Y1,Y2,Y3):

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

    #call tau_chi

    for i in range(0, Np):
        chi_S[i] = 1 - (1 - delta) * math.sin(PIRAD * tau_S[i])

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
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq=y_equation, z_eq=z_equation, range_u_min=0, range_u_max=1, range_u_step=32, wrap_u=True, range_v_max=3, close_v=True)
    
    
#
#    User interface
#
 
from bpy.props import *
 
class MESH_OT_primitive_wing_add(bpy.types.Operator):
    '''Add a wing'''
    bl_idname = "mesh.primitive_wing_add"
    bl_label = "Add wing"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    X1 = FloatProperty(name="X1", default=0.92455)
    X2 = FloatProperty(name="X2", default=0.514817)
    X3 = FloatProperty(name="X3", default=0.69552)
    Y1 = FloatProperty(name="Y1", default=0.0007)
    Y2 = FloatProperty(name="Y2", default=-0.049)
    Y3 = FloatProperty(name="Y3", default=0.0488)
    
 
    def execute(self, context):
        ob = addWing(self.X1,self.X2,self.X3,self.Y1,self.Y2,self.Y3)
        #context.scene.objects.link(ob)
        #context.scene.objects.active = ob
        return {'FINISHED'}
 
#
#    Registration
#    Makes it possible to access the script from the Add > Mesh menu
#
 
def menu_func(self, context):
    self.layout.operator("mesh.primitive_wing_add", 
        text="Wing", 
        icon='MESH_TORUS')
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.INFO_MT_mesh_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
 
if __name__ == "__main__":
    register()

