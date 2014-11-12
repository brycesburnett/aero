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
        layout.label("Use the refresh button to update component list")
        layout.operator(VIEW3D_OT_refresh.bl_idname, text="", icon="FILE_REFRESH")
        layout.label("Choose component to edit:")
        # Outputfield
        layout.template_list("ObjectSearchList", "",
                             wm, "srch_objects", 
                             wm, "srch_index")

        obj = bpy.data.objects[wm.srch_objects[wm.srch_index].name]
        if(wm.srch_index == -1):
            layout.label("Choose a component")
        elif(obj["component"] == "wing"):
            layout.label("Wing Properties:")
            layout.prop(obj, '["delta"]', text = "Delta")
            layout.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            layout.prop(obj, '["tau_points"]', text = "Tau Points")
            layout.prop(obj, '["zeta_points"]', text = "Zeta Points")
            layout.prop(obj, '["washout"]', text = "Washout")
            layout.prop(obj, '["washout_displacement"]', "Washout Displacement")
            layout.prop(obj, '["wing_length"]', "Wing Length")
            layout.prop(obj, 'location')
            layout.prop(obj, 'rotation_euler')
            layout.prop(obj, 'scale')
            layout.operator("mesh.wing_update", text="Update Wing", icon='UV_SYNC_SELECT')
            layout.operator("mesh.wing_delete", text="Delete Wing", icon='UGLYPACKAGE')
        elif(obj["component"] == "symmetrical wings"):
            layout.label("Symmetrical wing properties:")
            layout.prop(obj, '["delta"]', text = "Delta")
            layout.prop(obj, '["chi_eq"]', text = "Chi Parameterization Equation")
            layout.prop(obj, '["tau_points"]', text = "Tau Points")
            layout.prop(obj, '["zeta_points"]', text = "Zeta Points")
            layout.prop(obj, '["washout"]', text = "Washout")
            layout.prop(obj, '["washout_displacement"]', "Washout Displacement")
            layout.prop(obj, '["wing_length"]', "Wing Length")
            layout.prop(obj, 'location')
            layout.prop(obj, 'rotation_euler')
            layout.prop(obj, 'scale')
            layout.operator("mesh.wing_update", text="Update Wing", icon='UV_SYNC_SELECT')
            layout.operator("mesh.wing_delete", text="Delete Wing", icon='UGLYPACKAGE')
        elif(obj["component"] == "fuselage"):
            layout.label("Show fuselage properties")
        elif(obj["component"] == "pod"):
            layout.label("Show pod properties")

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
    
    
#-----------------------------------------------------------------------------
#                                                                             
#                             Register / Unregister                         
#                                                                             
#-----------------------------------------------------------------------------
def register():
    bpy.utils.register_module(__name__)
    bpy.types.WindowManager.MyProperties = PointerProperty(type=MyProperties, options={'SKIP_SAVE'})
    
def unregister():
    del bpy.types.WindowManager.MyProperties
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()
