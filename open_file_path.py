import bpy

class filePath(bpy.types.Operator):
    bl_idname = "open.file_path"
    bl_label = "Open File Path"
    bl_options = {'INTERNAL'}
    
    def execute(self, context):
        print(bpy.types.Scene.filepath)
        #THIS CURRENTLY DOES NOTHING NEED TO FIX
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}
