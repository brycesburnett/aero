import bpy, math
import numpy as np

def addWing(X1,X2,X3,Y1,Y2,Y3):

    num_segments = 2 # number of segments
    #First, create the matrix
    matrix_A = np.matrix(np.zeros((4 * num_segments, 4 * num_segments)))
    matrix_B = np.matrix(np.zeros((4 * num_segments, 1)))

    #now, fill matrix with calculated x values
    #note: for matrixes, begins at 0 index

    end_constraint_left = 1
    end_constraint_right = 0
    x_points = [0.0, X3, 1.0]
    y_points = [0.0, Y3, 0.0]

    #first and last segment are special cases
    #first, calculate bound function
    #equation in the form: b + c(x) + 2d(x^2)
    matrix_A[0,0] = 0 #note: a is always 0
    matrix_A[0,1] = 1 #note: b is always 1
    matrix_A[0,2] = x_points[0]
    matrix_A[0,3] = 2 * x_points[0] ** 2
    matrix_B[0,0] = end_constraint_left

    #next, work on segment 0

    #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
    #curve through first point
    matrix_A[1,0] = 1 #note: a is always 1
    matrix_A[1,1] = x_points[0]
    matrix_A[1,2] = x_points[0] ** 2
    matrix_A[1,3] = x_points[0] ** 3
    matrix_B[1,0] = y_points[0]

    #curve through second point
    matrix_A[2,0] = 1 #note: a is always 1
    matrix_A[2,1] = x_points[1]
    matrix_A[2,2] = x_points[1] ** 2
    matrix_A[2,3] = x_points[1] ** 3
    matrix_B[2,0] = y_points[1]

    #slope match between first and second points, first derivative
    #equation in the form: b_i + 2c_i(x_i_1) + 3d_i(x_i_1^2) - b_i_1 - 2c_i_1(x_i_1)  3d_i_1(x_i_1^2) = 0
    matrix_A[3,0] = 0 #note: a is always 0
    matrix_A[3,1] = 1 #note: b is always 1
    matrix_A[3,2] = 2 * x_points[1]
    matrix_A[3,3] = 3 * x_points[1] ** 2
    matrix_A[3,4] = 0 #note: a is always 0
    matrix_A[3,5] = -1 #note: b is always -1
    matrix_A[3,6] = -2 * x_points[1]
    matrix_A[3,7] = -3 * x_points[1] ** 2
    matrix_B[3,0] = 0

    #curve match between first and second points, second derivative
    #equation in the form 2c_i + 6d_i(x_i_1) - 2c_i_1 - 6d_i_1(x_i_1) = 0
    matrix_A[4,0] = 0 #note: a is always 0
    matrix_A[4,1] = 0 #note: b is always 0
    matrix_A[4,2] = 2
    matrix_A[4,3] = 6 * x_points[1]
    matrix_A[4,4] = 0 #note: a is always 0
    matrix_A[4,5] = 0 #note: b is always 0
    matrix_A[4,6] = -2
    matrix_A[4,7] = -6 * x_points[1]
    matrix_B[4,0] = 0


    #for middle functions
    repeat = num_segments - 2
    row = 5
    column = 4
    iteration = 2
    for i in range(0, repeat):
        print(row,column)
        #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
        #curve through first point
        matrix_A[row,column] = 1 #note: a is always 1
        matrix_A[row,column+1] = x_points[iteration-1]
        matrix_A[row,column+2] = x_points[iteration-1] ** 2
        matrix_A[row,column+3] = x_points[iteration-1] ** 3
        matrix_B[row,0] = y_points[iteration-1]

        #curve through second point
        matrix_A[row+1,column] = 1 #note: a is always 1
        matrix_A[row+1,column+1] = x_points[iteration]
        matrix_A[row+1,column+2] = x_points[iteration] ** 2
        matrix_A[row+1,column+3] = x_points[iteration] ** 3
        matrix_B[row+1,0] = y_points[iteration]

        #slope match between first and second points, first derivative
        #equation in the form: b_i + 2c_i(x_i_1) + 3d_i(x_i_1^2) - b_i_1 - 2c_i_1(x_i_1)  3d_i_1(x_i_1^2) = 0
        matrix_A[row+2,column] = 0 #note: a is always 0
        matrix_A[row+2,column+1] = 1 #note: b is always 1
        matrix_A[row+2,column+2] = 2 * x_points[iteration]
        matrix_A[row+2,column+3] = 3 * x_points[iteration] ** 2
        matrix_A[row+2,column+4] = 0 #note: a is always 0
        matrix_A[row+2,column+5] = -1 #note: b is always -1
        matrix_A[row+2,column+6] = -2 * x_points[iteration]
        matrix_A[row+2,column+7] = -3 * x_points[iteration] ** 2
        matrix_B[row+2,0] = 0

        #curve match between first and second points, second derivative
        #equation in the form 2c_i + 6d_i(x_i_1) - 2c_i_1 - 6d_i_1(x_i_1) = 0
        matrix_A[row+3,column] = 0 #note: a is always 0
        matrix_A[row+3,column+1] = 0 #note: b is always 0
        matrix_A[row+3,column+2] = 2
        matrix_A[row+3,column+3] = 6 * x_points[iteration]
        matrix_A[row+3,column+4] = 0 #note: a is always 0
        matrix_A[row+3,column+5] = 0 #note: b is always 0
        matrix_A[row+3,column+6] = -2
        matrix_A[row+3,column+7] = -6 * x_points[iteration]
        matrix_B[row+3,0] = 0
        row = row + 4
        column = column + 4
        iteration = iteration + 1

    #work on last segments
    #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
    #curve through second to last point
    matrix_A[4*num_segments - 3, 4*num_segments - 4] = 1
    matrix_A[4*num_segments - 3, 4*num_segments - 3] = x_points[len(x_points)-2]
    matrix_A[4*num_segments - 3, 4*num_segments - 2] = x_points[len(x_points)-2] ** 2
    matrix_A[4*num_segments - 3, 4*num_segments - 1] = x_points[len(x_points)-2] ** 3
    matrix_B[4*num_segments - 3, 0] = y_points[len(y_points)-2]

    #curve through last point
    matrix_A[4*num_segments - 2, 4*num_segments - 4] = 1
    matrix_A[4*num_segments - 2, 4*num_segments - 3] = x_points[len(x_points)-1]
    matrix_A[4*num_segments - 2, 4*num_segments - 2] = x_points[len(x_points)-1] ** 2
    matrix_A[4*num_segments - 2, 4*num_segments - 1] = x_points[len(x_points)-1] ** 3
    matrix_B[4*num_segments - 2, 0] = y_points[len(y_points)-1]

    matrix_A[4*num_segments - 1, 4*num_segments - 4] = 0
    matrix_A[4*num_segments - 1, 4*num_segments - 3] = 1
    matrix_A[4*num_segments - 1, 4*num_segments - 2] = x_points[len(x_points)-1]
    matrix_A[4*num_segments - 1, 4*num_segments - 1] = 2* x_points[len(x_points)-1] ** 2
    matrix_B[4*num_segments - 1,0] = end_constraint_right

    coefficient_upper = np.linalg.solve(matrix_A, matrix_B)


    #------------------------------------------------------------------------------------

    num_segments = 3 # number of segments
    #First, create the matrix
    matrix_A = np.matrix(np.zeros((4 * num_segments, 4 * num_segments)))
    matrix_B = np.matrix(np.zeros((4 * num_segments, 1)))

    #now, fill matrix with calculated x values
    #note: for matrixes, begins at 0 index

    end_constraint_left = 0
    end_constraint_right = 0
    x_points = [1.0, X1, X2, 0.0]
    y_points = [0.0, Y1, Y2, 0.0]

    #first and last segment are special cases
    #first, calculate bound function
    #equation in the form: b + c(x) + 2d(x^2)
    matrix_A[0,0] = 0 #note: a is always 0
    matrix_A[0,1] = 1 #note: b is always 1
    matrix_A[0,2] = x_points[0]
    matrix_A[0,3] = 2 * x_points[0] ** 2
    matrix_B[0,0] = end_constraint_left

    #next, work on segment 0

    #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
    #curve through first point
    matrix_A[1,0] = 1 #note: a is always 1
    matrix_A[1,1] = x_points[0]
    matrix_A[1,2] = x_points[0] ** 2
    matrix_A[1,3] = x_points[0] ** 3
    matrix_B[1,0] = y_points[0]

    #curve through second point
    matrix_A[2,0] = 1 #note: a is always 1
    matrix_A[2,1] = x_points[1]
    matrix_A[2,2] = x_points[1] ** 2
    matrix_A[2,3] = x_points[1] ** 3
    matrix_B[2,0] = y_points[1]

    #slope match between first and second points, first derivative
    #equation in the form: b_i + 2c_i(x_i_1) + 3d_i(x_i_1^2) - b_i_1 - 2c_i_1(x_i_1)  3d_i_1(x_i_1^2) = 0
    matrix_A[3,0] = 0 #note: a is always 0
    matrix_A[3,1] = 1 #note: b is always 1
    matrix_A[3,2] = 2 * x_points[1]
    matrix_A[3,3] = 3 * x_points[1] ** 2
    matrix_A[3,4] = 0 #note: a is always 0
    matrix_A[3,5] = -1 #note: b is always -1
    matrix_A[3,6] = -2 * x_points[1]
    matrix_A[3,7] = -3 * x_points[1] ** 2
    matrix_B[3,0] = 0

    #curve match between first and second points, second derivative
    #equation in the form 2c_i + 6d_i(x_i_1) - 2c_i_1 - 6d_i_1(x_i_1) = 0
    matrix_A[4,0] = 0 #note: a is always 0
    matrix_A[4,1] = 0 #note: b is always 0
    matrix_A[4,2] = 2
    matrix_A[4,3] = 6 * x_points[1]
    matrix_A[4,4] = 0 #note: a is always 0
    matrix_A[4,5] = 0 #note: b is always 0
    matrix_A[4,6] = -2
    matrix_A[4,7] = -6 * x_points[1]
    matrix_B[4,0] = 0


    #for middle functions
    repeat = num_segments - 2
    row = 5
    column = 4
    iteration = 2
    for i in range(0, repeat):
        print(row,column)
        #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
        #curve through first point
        matrix_A[row,column] = 1 #note: a is always 1
        matrix_A[row,column+1] = x_points[iteration-1]
        matrix_A[row,column+2] = x_points[iteration-1] ** 2
        matrix_A[row,column+3] = x_points[iteration-1] ** 3
        matrix_B[row,0] = y_points[iteration-1]

        #curve through second point
        matrix_A[row+1,column] = 1 #note: a is always 1
        matrix_A[row+1,column+1] = x_points[iteration]
        matrix_A[row+1,column+2] = x_points[iteration] ** 2
        matrix_A[row+1,column+3] = x_points[iteration] ** 3
        matrix_B[row+1,0] = y_points[iteration]

        #slope match between first and second points, first derivative
        #equation in the form: b_i + 2c_i(x_i_1) + 3d_i(x_i_1^2) - b_i_1 - 2c_i_1(x_i_1)  3d_i_1(x_i_1^2) = 0
        matrix_A[row+2,column] = 0 #note: a is always 0
        matrix_A[row+2,column+1] = 1 #note: b is always 1
        matrix_A[row+2,column+2] = 2 * x_points[iteration]
        matrix_A[row+2,column+3] = 3 * x_points[iteration] ** 2
        matrix_A[row+2,column+4] = 0 #note: a is always 0
        matrix_A[row+2,column+5] = -1 #note: b is always -1
        matrix_A[row+2,column+6] = -2 * x_points[iteration]
        matrix_A[row+2,column+7] = -3 * x_points[iteration] ** 2
        matrix_B[row+2,0] = 0

        #curve match between first and second points, second derivative
        #equation in the form 2c_i + 6d_i(x_i_1) - 2c_i_1 - 6d_i_1(x_i_1) = 0
        matrix_A[row+3,column] = 0 #note: a is always 0
        matrix_A[row+3,column+1] = 0 #note: b is always 0
        matrix_A[row+3,column+2] = 2
        matrix_A[row+3,column+3] = 6 * x_points[iteration]
        matrix_A[row+3,column+4] = 0 #note: a is always 0
        matrix_A[row+3,column+5] = 0 #note: b is always 0
        matrix_A[row+3,column+6] = -2
        matrix_A[row+3,column+7] = -6 * x_points[iteration]
        matrix_B[row+3,0] = 0
        row = row + 4
        column = column + 4
        iteration = iteration + 1

    #work on last segments
    #equation in the form: a + b(x) + c(x^2) + d(x^3) = y
    #curve through second to last point
    matrix_A[4*num_segments - 3, 4*num_segments - 4] = 1
    matrix_A[4*num_segments - 3, 4*num_segments - 3] = x_points[len(x_points)-2]
    matrix_A[4*num_segments - 3, 4*num_segments - 2] = x_points[len(x_points)-2] ** 2
    matrix_A[4*num_segments - 3, 4*num_segments - 1] = x_points[len(x_points)-2] ** 3
    matrix_B[4*num_segments - 3, 0] = y_points[len(y_points)-2]

    #curve through last point
    matrix_A[4*num_segments - 2, 4*num_segments - 4] = 1
    matrix_A[4*num_segments - 2, 4*num_segments - 3] = x_points[len(x_points)-1]
    matrix_A[4*num_segments - 2, 4*num_segments - 2] = x_points[len(x_points)-1] ** 2
    matrix_A[4*num_segments - 2, 4*num_segments - 1] = x_points[len(x_points)-1] ** 3
    matrix_B[4*num_segments - 2, 0] = y_points[len(y_points)-1]

    matrix_A[4*num_segments - 1, 4*num_segments - 4] = 0
    matrix_A[4*num_segments - 1, 4*num_segments - 3] = 1
    matrix_A[4*num_segments - 1, 4*num_segments - 2] = x_points[len(x_points)-1]
    matrix_A[4*num_segments - 1, 4*num_segments - 1] = 2* x_points[len(x_points)-1] ** 2
    matrix_B[4*num_segments - 1,0] = end_constraint_right

    coefficient_lower = np.linalg.solve(matrix_A, matrix_B)
    a1 = coefficient_upper.item(4)
    b1 = coefficient_upper.item(5)
    c1 = coefficient_upper.item(6)
    d1 = coefficient_upper.item(7)
    a2 = coefficient_upper.item(0)
    b2 = coefficient_upper.item(1)
    c2 = coefficient_upper.item(2)
    d2 = coefficient_upper.item(3)
    eq1 = str(a1) + "+" + str(b1) + "*u+" + str(c1) + "*u**2+" + str(d1) + "*u**3"
    eq2 = str(a2) + "+" + str(b2) + "*u+" + str(c2) + "*u**2+" + str(d2) + "*u**3"
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq="u", z_eq=eq1, range_u_min=X3, range_u_max=1, range_u_step=32, wrap_u=False, range_v_max=3)
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq="u", z_eq=eq2, range_u_min=0, range_u_max=X3, range_u_step=32, wrap_u=False, range_v_max=3)
    
    a3 = coefficient_lower.item(0)
    b3 = coefficient_lower.item(1)
    c3 = coefficient_lower.item(2)
    d3 = coefficient_lower.item(3)
    a4 = coefficient_lower.item(4)
    b4 = coefficient_lower.item(5)
    c4 = coefficient_lower.item(6)
    d4 = coefficient_lower.item(7)
    a5 = coefficient_lower.item(8)
    b5 = coefficient_lower.item(9)
    c5 = coefficient_lower.item(10)
    d5 = coefficient_lower.item(11)
    eq3 = str(a3) + "+" + str(b3) + "*u+" + str(c3) + "*u**2+" + str(d3) + "*u**3"
    eq4 = str(a4) + "+" + str(b4) + "*u+" + str(c4) + "*u**2+" + str(d4) + "*u**3"
    eq5 = str(a5) + "+" + str(b5) + "*u+" + str(c5) + "*u**2+" + str(d5) + "*u**3"

    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq="u", z_eq=eq3, range_u_min=X1, range_u_max=1, range_u_step=32, wrap_u=False, range_v_max=3)
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq="u", z_eq=eq4, range_u_min=X2, range_u_max=X1, range_u_step=32, wrap_u=False, range_v_max=3)
    bpy.ops.mesh.primitive_xyz_function_surface(x_eq="v", y_eq="u", z_eq=eq5, range_u_min=0, range_u_max=X2, range_u_step=32, wrap_u=False, range_v_max=3)
    
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
