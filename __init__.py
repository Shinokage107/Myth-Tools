bl_info = {
    "name" : "Myth Tools",
    "author" : "Shino Mythmaker (Alexander Braun)", 
    "description" : "Supportive plugin that combines Rig control and Export of FFXIV Poses.",
    "blender" : (3, 6, 0),
    "version" : (0, 7, 0),
    "category" : "3D View" 
}

import bpy
from . import ui
from . import operators

def armature_poll(self, object):
    return object.type == 'ARMATURE'

def register():

    bpy.types.Scene.anamnesis_armature = bpy.props.PointerProperty(
        type=bpy.types.Object,
        poll=armature_poll
    )

    ui.register()
    operators.register()
    

def unregister():
    ui.unregister()
    operators.unregister()
 
if __name__ == "__main__":
    register()
