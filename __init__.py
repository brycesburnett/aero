bl_info = {
    "name": "Aircraft Components",
    "author": "CSULB CECS 491 Team 4",
    "version": (1, 0),
    "blender": (2, 70, 0),
    "location": "View3D > Add > Mesh > Aircraft Components",
    "description": "Add aircraft components",
    "category": "Add Mesh",
}

if "bpy" in locals():
    import imp
    imp.reload(add_mesh_wing)
    imp.reload(add_mesh_symmetrical_wings)
    imp.reload(add_mesh_pod)
    imp.reload(add_mesh_fuselage)
else:
    from . import add_mesh_wing
    from . import add_mesh_symmetrical_wings
    from . import add_mesh_pod
    from . import add_mesh_fuselage

import bpy

class mesh_aircraft_components_add(bpy.types.Menu):
    bl_idname = "mesh_aircraft_components_add"
    bl_label = "Aircraft Components"

    def draw(self, context):
        layout = self.layout
        layout.operator_context = 'INVOKE_REGION_WIN'
        layout.operator("mesh.wing_add", text="Wing")
        layout.operator("mesh.symmetrical_wings_add", text="Symmetrical Wing")
        layout.operator("mesh.pod_add", text="Pod")
        layout.operator("mesh.fuselage_add", text="Fuselage")

class aircraft_component_panel(bpy.types.Panel):
    """Aircraft Component_Panel"""
    bl_idname = "panel_aircraft_components_add"
    bl_label = "Aircraft Components"
    
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Aircraft Generator'
    
    #Panels in ImageEditor are using .poll() instead of bl_context.
    #@classmethod
    #def poll(cls, context):
    #    return context.space_data.show_paint
    
    def draw(self, context):
        layout = self.layout
        layout.operator("mesh.wing_add", text="Wing")
        layout.operator("mesh.symmetrical_wings_add", text="Symmetrical Wing")
        layout.operator("mesh.pod_add", text="Pod")
        layout.operator("mesh.fuselage_add", text="Fuselage")


def menu_func(self, context):
    self.layout.menu("mesh_aircraft_components_add", icon="PLUGIN")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func)

def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()
