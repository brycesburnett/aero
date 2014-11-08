#This code is needed for an addon as well as deleting the if __name__ statement at the bottom.
bl_info = {
    "name": "Add Fuselage",
    "author": "CSULB CECS 491 Team 4",
    "version": (1, 0),
    "description": "Generates a single fuselage using parametric cubic splines.",
    "category": "Object"
}

import bpy, math
import numpy as np
import xlrd
#location of points excel sheet
file_location = "C:/points.xlsx"
   
#time = ttt, station = xxx, snake = dyy, width/2 = www, upper = zuu, equator = zee, lower = zLL
#these data points correspond to columns 3-9 on Barnes' excel sheet (not in respective order)
def add_fuselage(delta, time_points, station_points, snake_points, width_points, upper_points, equator_points, lower_points, x_location, y_location, z_location):
    #do some magic
   

 
from bpy.props import *
 
class Fuselage(bpy.types.Operator):
    '''Single Fuselage generator'''
    bl_idname = "mesh.fuselage_add"
    bl_label = "Add a fuselage"
    bl_options = {'REGISTER', 'UNDO'}
 
    #Input variables go here
    delta = FloatProperty(name="Delta", default=0.05)
    time_points = StringProperty(name="Time points", description="Independent variable 'Time'", default="0, 0.5, 0.8366, 1, 1")
    station_points = StringProperty(name="Station points (x)", description="User input points (x)", default="0, 0, 0.25, 0.7, 1, 1")
    width_points = StringProperty(name="Width points (w)", description="User input points (width)", default="1, 0.005, 0.08, 0.04, 0.005, -0.5")
    upper_points = StringProperty(name="Upper points (zu)", description="User input points (z upper)", default="1, 0, 0.2, 0.19, 0.16, -0.6")
    snake_points = StringProperty(name="Snake points (dyy", description="User input points (dyy)", default="1, 0, 0, 0, 0, 1")
    equator_points = StringProperty(name = "Equator points (ze)", description="User input points (z equator)", default="0, 0, 0.05, 0.15, 0.15, 1")
    lower_points = StringProperty(name = "Lower points (zL)", description="User input points (z lower)", default="1, 0, 0, 0, 0.11, 0.14, 0.4")
    
    x_location = FloatProperty(name="X location", default = 0)
    y_location = FloatProperty(name="Y location", default = 0)
    z_location = FloatProperty(name="Z location", default = 0)
    
    def execute(self, context):
        ob = add_fuselage(self.delta, self.time_points, self.station_points, self.snake_points, self.width_points, self.upper_points, self.equator_points, self.lower_points, self.x_location, self.y_location, self.z_location)
        #context.scene.objects.link(ob)
        #context.scene.objects.active = ob
        return {'FINISHED'}
 
#
#    Registration
#    Makes it possible to access the script from the Add > Mesh menu
#    Right now this is just a script, later on we will convert it into an addon
 
def menu_func(self, context):
    self.layout.operator("mesh.fuselage_add", 
        text="Fuselage")
 
def register():
   bpy.utils.register_module(__name__)
   bpy.types.INFO_MT_mesh_add.prepend(menu_func)
 
def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)
