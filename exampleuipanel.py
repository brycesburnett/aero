import bpy
from bpy.props import IntProperty, CollectionProperty
from bpy.types import Panel, UIList


class OBJECT_UL_zones(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(0.2)
        split.label(str(item.id))
        split.prop(item, "name", text="", emboss=False, translate=False, icon='BORDER_RECT')


class UIListPanelExample(Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Keith is cool"
    bl_idname = "OBJECT_PT_ui_list_example"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout
        ob = context.object

        layout.template_list("OBJECT_UL_zones", "", ob, "zones", ob, "zones_index")


class Zone(bpy.types.PropertyGroup):
    # name = StringProperty()
    id = IntProperty()


def register():
    bpy.utils.register_module(__name__)
    bpy.types.Object.zones = CollectionProperty(type=Zone)
    bpy.types.Object.zones_index = IntProperty()

def unregister():
    bpy.utils.unregister_module(__name__)
    del bpy.types.Object.zones

if __name__ == "__main__":
    register()


    # Add an example entry every time this code is executed
    ob = bpy.context.object
    item = ob.zones.add()
    item.id = len(ob.zones)
    item.name = "Keith " + chr(item.id + 64)
