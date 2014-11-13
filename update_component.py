bl_info = {
    "name": "Update Component",
    "author": "CSULB CECS 491 Team 4",
    "version": (1, 0),
    "description": "Provides functionality to update the selected component.",
    "category": "Add Mesh"
    }
    
import bpy
from bpy.props import *

#
#   globals
#
obj_list = []

#
#   classes for the template lists
#
class ObjectSearchList(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        layout.label(icon="OBJECT_DATA", text=item.name)

class VIEW3D_PT_search_and_replace(bpy.types.Panel):
    bl_label = "Update Component"
    bl_category = "Aircraft Generator"
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    
    @classmethod
    def poll(self, context):
        return context.mode == "OBJECT"
        
    def draw(self, context):
        layout = self.layout
        split = layout.split()
        col = split.column()

        wm = context.window_manager.MyProperties
        row = layout.row()
        row.alignment = 'CENTER'
        row.operator(VIEW3D_OT_refresh.bl_idname, text="Refresh Component List", icon="FILE_REFRESH")
        layout.label("Choose component to edit:")
        # Outputfield
        layout.template_list("ObjectSearchList", "",
                             wm, "srch_objects", 
                             wm, "srch_index")

        obj = bpy.data.objects[wm.srch_objects[wm.srch_index].name]
        if(wm.srch_index == -1):
            layout.label("Choose a component")
        elif(obj["component"] == "wing"):
            layout.label("Wing Geometry:")
            row = layout.row()
            box = row.box()
            box.prop(obj, '["delta"]', text = "Delta")
            box.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            box.prop(obj, '["tau_points"]', text = "Tau Points")
            box.prop(obj, '["zeta_points"]', text = "Zeta Points")
            box.prop(obj, '["washout"]', text = "Washout")
            box.prop(obj, '["washout_displacement"]', "Washout Displacement")
            box.prop(obj, '["wing_length"]', "Wing Length")

            layout.separator()
            layout.label("Transformations:")
            row = layout.row()
            box = row.box()
            box.prop(obj, 'location')
            box.prop(obj, 'rotation_euler')
            box.prop(obj, 'scale')
            layout.separator()
            layout.separator()
            row = layout.row()
            row.alignment = 'EXPAND'
            row.operator("mesh.wing_update", text="Update Wing", icon='UV_SYNC_SELECT')
            row.operator("mesh.wing_delete", text="Delete Wing", icon='UGLYPACKAGE')
        elif(obj["component"] == "symmetrical wings"):
            layout.label("Symmetrical Wing Geometry:")
            row = layout.row()
            box = row.box()
            box.prop(obj, '["delta"]', text = "Delta")
            box.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            box.prop(obj, '["tau_points"]', text = "Tau Points")
            box.prop(obj, '["zeta_points"]', text = "Zeta Points")
            box.prop(obj, '["washout"]', text = "Washout")
            box.prop(obj, '["washout_displacement"]', "Washout Displacement")
            box.prop(obj, '["wing_length"]', "Wing Length")

            layout.separator()
            layout.label("Transformations:")
            row = layout.row()
            box = row.box()
            box.prop(obj, 'location')
            box.prop(obj, 'rotation_euler')
            box.prop(obj, 'scale')
            layout.separator()
            layout.separator()
            row = layout.row()
            row.alignment = 'EXPAND'
            row.operator("mesh.symmetrical_wings_update", text="Update Wings", icon='UV_SYNC_SELECT')
            row.operator("mesh.symmetrical_wings_delete", text="Delete Wings", icon='UGLYPACKAGE')
        elif(obj["component"] == "fuselage"):
            layout.label("Fuselage Geometry:")
            row = layout.row()
            box = row.box()
            box.prop(obj, '["delta"]', text = "Delta")
            box.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            box.prop(obj, '["tau_points"]', text = "Tau Points")
            box.prop(obj, '["zeta_points"]', text = "Zeta Points")
            box.prop(obj, '["smoothness"]', text = "Smoothness")

            layout.separator()
            layout.label("Transformations:")
            row = layout.row()
            box = row.box()
            box.prop(obj, 'location')
            box.prop(obj, 'rotation_euler')
            box.prop(obj, 'scale')
            layout.separator()
            layout.separator()
            row = layout.row()
            row.alignment = 'EXPAND'
            row.operator("mesh.fuselage_update", text="Update Fuselage", icon='UV_SYNC_SELECT')
            row.operator("mesh.fuselage_delete", text="Delete Fuselage", icon='UGLYPACKAGE')
        elif(obj["component"] == "pod"):
            layout.label("Pod Geometry")
            row = layout.row()
            box = row.box()
            box.label("Show fuselage properties")
            box.prop(obj, '["delta"]', text = "Delta")
            box.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            box.prop(obj, '["tau_points"]', text = "Tau Points")
            box.prop(obj, '["zeta_points"]', text = "Zeta Points")
            box.prop(obj, '["smoothness"]', text = "Smoothness")

            layout.separator()
            layout.label("Transformations:")
            row = layout.row()
            box = row.box()
            box.prop(obj, 'location')
            box.prop(obj, 'rotation_euler')
            box.prop(obj, 'scale')
            layout.separator()
            layout.separator()
            row = layout.row()
            row.alignment = 'EXPAND'
            row.operator("mesh.pod_update", text="Update Pod", icon='UV_SYNC_SELECT')
            row.operator("mesh.pod_delete", text="Delete Pod", icon='UGLYPACKAGE')

#
#   Refresh Button
#   
class VIEW3D_OT_refresh(bpy.types.Operator):
    """Refresh all"""
    bl_idname = "view3d.obj_search_refresh"
    bl_label = "Refresh objects list"
    
    def execute(self, context):
        update_objects(context.window_manager.MyProperties, context)
        return {'FINISHED'}

#-----------------------------------------------------------------------------
#
#                               Jump To Object Functions
#
#-----------------------------------------------------------------------------
#
#   [Object-Menu] select the object and focus the view on it
#
def jump_to_object(scene, ob):    
    try:     
        deselect_all_objects(scene)
        ob.select = True
        scene.objects.active = ob
        return bpy.ops.view3d.view_selected('EXEC_REGION_WIN') == {'FINISHED'}
    except:
        return False 

    
#-----------------------------------------------------------------------------
#
#                               Update Functions
#
#-----------------------------------------------------------------------------
#
#   Update Objects - gets called when a refresh button or the list was clicked 
#
def update_objects(self, context):
  
    self.srch_index = -1
    self.srch_objects.clear()
 
    for ob in context.scene.objects:
        if (ob.type == 'MESH'):
            try:
                if(ob["component"] == "wing" or ob["component"] == "fuselage" or ob["component"] == "pod" or ob["component"] == "symmetrical wings"):
                    obj_list.append(ob.name)
                    item = self.srch_objects.add()
                    item.name = ob.name
            except:
                pass
        
       
def update_obj_search_index(self, context):
    
    if len(self.srch_objects) < 1 or self.srch_index < 0:
        return
    try:
        ob_name = self.srch_objects[self.srch_index].name
    except IndexError:
        print("Object Search: Bad objects list index")
        return
    
    ob = context.scene.objects.get(ob_name)
    if ob is not None:
        jump_to_object(context.scene, ob)

def deselect_all_objects(scn):
    for obj in scn.objects:
        obj.select = False

#-----------------------------------------------------------------------------
#
#                               Properties
#
#-----------------------------------------------------------------------------

class MyProperties(bpy.types.PropertyGroup):
    select = BoolProperty(default=True)
    object = StringProperty(update=update_objects)
    srch_objects = CollectionProperty(type=bpy.types.PropertyGroup)
    srch_index = IntProperty(update=update_obj_search_index)
    
bpy.utils.register_class(MyProperties)    

bpy.types.WindowManager.MyProperties = PointerProperty(type=MyProperties, options={'SKIP_SAVE'})
    
