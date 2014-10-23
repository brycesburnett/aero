import bpy
from bpy.types import Menu, Panel

class View3DPanel():
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'

class VIEW3D_PT_tools_add_object(View3DPanel, Panel):
    bl_category = "Create"
    bl_context = "objectmode"
    bl_label = "Add components"

    @staticmethod
    def draw_add_mesh(layout, label=False):
        if label:
            layout.label(text="Primitives:")
        layout.operator("mesh.symmetrical_wings_add", text="Add Symmetrical Wings", icon='BOIDS')
        layout.separator()
        layout.operator("mesh.wing_add", text="Add Wing", icon='BOIDS')
        layout.separator()
        layout.operator("mesh.fuselage_add", text="Add Fuselage", icon='ZOOMOUT')
        layout.separator()
        layout.operator("mesh.pod_add", text="Add Pod", icon='WIRE')



    @staticmethod
    def draw_add_curve(layout, label=False):
        if label:
            layout.label(text="Bezier:")
        layout.operator("curve.primitive_bezier_curve_add", text="Bezier", icon='CURVE_BEZCURVE')
        layout.operator("curve.primitive_bezier_circle_add", text="Circle", icon='CURVE_BEZCIRCLE')

        if label:
            layout.label(text="Nurbs:")
        else:
            layout.separator()
        layout.operator("curve.primitive_nurbs_curve_add", text="Nurbs Curve", icon='CURVE_NCURVE')
        layout.operator("curve.primitive_nurbs_circle_add", text="Nurbs Circle", icon='CURVE_NCIRCLE')
        layout.operator("curve.primitive_nurbs_path_add", text="Path", icon='CURVE_PATH')

    @staticmethod
    def draw_add_surface(layout):
        layout.operator("surface.primitive_nurbs_surface_curve_add", text="Nurbs Curve", icon='SURFACE_NCURVE')
        layout.operator("surface.primitive_nurbs_surface_circle_add", text="Nurbs Circle", icon='SURFACE_NCIRCLE')
        layout.operator("surface.primitive_nurbs_surface_surface_add", text="Nurbs Surface", icon='SURFACE_NSURFACE')
        layout.operator("surface.primitive_nurbs_surface_cylinder_add", text="Nurbs Cylinder", icon='SURFACE_NCYLINDER')
        layout.operator("surface.primitive_nurbs_surface_sphere_add", text="Nurbs Sphere", icon='SURFACE_NSPHERE')
        layout.operator("surface.primitive_nurbs_surface_torus_add", text="Nurbs Torus", icon='SURFACE_NTORUS')

    @staticmethod
    def draw_add_mball(layout):
        layout.operator_enum("object.metaball_add", "type")

    @staticmethod
    def draw_add_lamp(layout):
        layout.operator_enum("object.lamp_add", "type")

    @staticmethod
    def draw_add_other(layout):
        layout.operator("object.text_add", text="Text", icon='OUTLINER_OB_FONT')
        layout.operator("object.armature_add", text="Armature", icon='OUTLINER_OB_ARMATURE')
        layout.operator("object.add", text="Lattice", icon='OUTLINER_OB_LATTICE').type = 'LATTICE'
        layout.operator("object.empty_add", text="Empty", icon='OUTLINER_OB_EMPTY').type = 'PLAIN_AXES'
        layout.operator("object.speaker_add", text="Speaker", icon='OUTLINER_OB_SPEAKER')
        layout.operator("object.camera_add", text="Camera", icon='OUTLINER_OB_CAMERA')

    def draw(self, context):
        layout = self.layout

        col = layout.column(align=True)
        self.draw_add_mesh(col)

		
if __name__ == "__main__":  # only for live edit.
    bpy.utils.register_module(__name__)
