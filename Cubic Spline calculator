import numpy as np

num_segments = 2 # number of segments
#First, create the matrix
matrix_A = np.matrix(np.zeros((4 * num_segments, 4 * num_segments)))
matrix_B = np.matrix(np.zeros((4 * num_segments, 1)))

#now, fill matrix with calculated x values
#note: for matrixes, begins at 0 index

end_constraint_left = 1
end_constraint_right = 0
#x_points = [1.0, 0.92455, 0.514817, 0.0, 0.69552]
#y_points = [0.0, 0.0007, -0.049, 0.0, 0.0488]
#x_points = [1.0, 0.92455, 0.514817]
#y_points = [0.0, 0.0007, -0.049]
x_points = [0.0, 0.69552, 1.0]
y_points = [0.0, 0.0488, 0]
#end_constraint_left = 2
#end_constraint_right = 1
#x_points = [0, 2, 5, 8]
#y_points = [1, 2, 0, 0]

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

coefficient = np.linalg.solve(matrix_A, matrix_B)

print(coefficient)
