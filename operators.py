import bpy
import json
import os
from os import path
from mathutils import *
from bpy_extras.io_utils import ExportHelper

#Export of Poses from A6kA6k Pose Helper
class LoadAnaPose(bpy.types.Operator):
    """Load an Anamnesis .pose file to the current armature"""
    bl_idname = "pose.load_ana_pose"
    bl_label = "Import"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob: bpy.props.StringProperty(
        default='*.pose',
        options={'HIDDEN'}
    )

    # don't enable the button if we don't have an armature set
    @classmethod
    def poll(cls, context):
        return context.scene.anamnesis_armature is not None
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        # support for proper bone orientations: get diff from original
        arm.bones['n_throw'].matrix_basis = Matrix()
        # axis-angle form of the diff quaternion we want to pass to each individual bone operation. shorthand to pack into a float vector property; this seems silly?
        aa = Quaternion([1,0,0,0]).rotation_difference(arm.bones['n_throw'].matrix.to_quaternion()).to_axis_angle()
        diff = [aa[0][0], aa[0][1], aa[0][2], aa[1]]

        for bone in arm.bones:
            bpy.ops.pose.load_ana_bone('EXEC_DEFAULT', bone=bone.name, path=self.filepath, diff=diff)
        # rotate the whole thing to be upright, otherwise it can turn based on the transform of the armature object
        arm.bones['n_throw'].rotation_quaternion = Quaternion([1,0,0,0])
        return {'FINISHED'}

    # don't forget this so we can get the file select popup
    def invoke(self, context, event):
        bpy.context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}        
        
class LoadAnaBone(bpy.types.Operator):
    """Load a single bone from the current Anamnesis .pose file to the current armature"""
    bl_idname = "pose.load_ana_bone"
    bl_label = "Load Anamnesis Bone"
    bl_options = {'REGISTER'}
    
    bone: bpy.props.StringProperty()
    path: bpy.props.StringProperty()
    diff: bpy.props.FloatVectorProperty(size=4)
    
    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        with open(path.join(path.dirname(__file__), 'map.json'), 'r') as f:
            name_map = json.load(f)

        with open(self.path, 'r') as f:
            pose = json.load(f)['Bones']

        # check if the first bone in the pose file is in the map to determine legacy
        legacy = False
        if list(pose.keys())[0] in name_map.values():
            legacy = True

        # !!! The meat.
        bone = arm.bones[self.bone]
        # fucky legacy check switch thing to avoid redundant code
        rot = False
        if legacy and bone.name in name_map and name_map[bone.name] in pose:
            rot = pose[name_map[bone.name]]
        elif bone.name in pose:
            rot = pose[bone.name]

        if rot:
            rot = rot["Rotation"].split(", ")
            rot = [float(x) for x in rot]
            # .pose is XYZW, we need to switch to WXYZ
            rot.insert(0, rot.pop())
            diff = Quaternion(self.diff[0:3], self.diff[3])
            rot = Quaternion(rot) @ diff
            # key blender function for transforming from the character's space to the bone's space relative to rest.
            bone.rotation_quaternion = context.scene.anamnesis_armature.convert_space(pose_bone = bone, matrix = rot.to_matrix().to_4x4(), from_space = 'POSE', to_space = 'LOCAL').to_quaternion()
        
        return {'FINISHED'}

class ExportAnaPose(bpy.types.Operator, ExportHelper):
    """Export an Anamnesis .pose file from the current armature's pose"""
    bl_idname = "pose.export_ana_pose"
    bl_label = "Export"
    bl_options = {'REGISTER', 'UNDO'}

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")
    filename_ext='.pose'
    filter_glob: bpy.props.StringProperty(
        default='*.pose',
        options={'HIDDEN'}
    )

    #don't enable the button if we don't have an armature set
    @classmethod
    def poll(cls, context):
        return context.scene.anamnesis_armature is not None

    def execute(self, context):
        arm = context.scene.anamnesis_armature.pose

        hara = arm.bones['n_throw'].matrix_basis
        arm.bones['n_throw'].matrix_basis = Matrix()
        diff = Quaternion([1,0,0,0]).rotation_difference(arm.bones['n_throw'].matrix.to_quaternion())
        arm.bones['n_throw'].matrix_basis = hara

        with open(self.filepath, 'w') as f:
            json_dict = {
                "FileExtension": ".pose",
                "TypeName": "Anamnesis Pose",
                "Bones": {}
            }

            for bone in arm.bones:
                quat = bone.matrix.to_quaternion() @ diff
                rot = "{0}, {1}, {2}, {3}".format(quat.x, quat.y, quat.z, quat.w)
                bone_dict = {
                    bone.name: {
                        "Rotation": rot
                    }
                }
                json_dict['Bones'].update(bone_dict)
            
            json.dump(json_dict, f)
            return {'FINISHED'}

#Rig Imports    
class ImportMiqF(bpy.types.Operator):
    bl_idname = "mph.import_miq_f"
    bl_label = "Import_MiqF"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='MiqoF', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)

class ImportMiqM(bpy.types.Operator):
    bl_idname = "mph.import_miq_m"
    bl_label = "Import_MiqM"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='MiqoM', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)         

class ImportAuraF(bpy.types.Operator):
    bl_idname = "mph.import_aura_f"
    bl_label = "Import_AuraF"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='AuraF', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class ImportAuraM(bpy.types.Operator):
    bl_idname = "mph.import_aura_m"
    bl_label = "Import_AuraM"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='AuraM', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class ImportVieraF(bpy.types.Operator):
    bl_idname = "mph.import_viera_f"
    bl_label = "Import_VieraF"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='VieraF', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context)   

class ImportVieraM(bpy.types.Operator):
    bl_idname = "mph.import_viera_m"
    bl_label = "Import_VieraM"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='VieraM', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class ImportLalaF(bpy.types.Operator):
    bl_idname = "mph.import_lala_f"
    bl_label = "Import_LalaF"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='LalaM', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class ImportLalaM(bpy.types.Operator):
    bl_idname = "mph.import_lala_m"
    bl_label = "Import_LalaM"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        before_data = list(bpy.data.collections)
        bpy.ops.wm.append(directory=os.path.join(os.path.dirname(__file__), 'assets', 'Rig Collection.blend') + r'\Collection', filename='LalaM', link=False)
        new_data = list(filter(lambda d: not d in before_data, list(bpy.data.collections)))
        appended = None if not new_data else new_data[0]
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class SkirtToggle(bpy.types.Operator):
    bl_idname = "mph.skirt_toggle"
    bl_label = "Skirt_Toggle"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        scene = context.scene

        params = ["Skirt"] #add your list of search parameters

        for obj in scene.objects:
            if any(x in obj.name for x in params): #search for params items in object name
                obj.hide_viewport = not obj.hide_viewport
                obj.hide_render = obj.hide_viewport
        
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 
    
class ClearTransforms(bpy.types.Operator):
    bl_idname = "mph.clear_transforms"
    bl_label = "Clear_Transforms"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'POSE')
        bpy.ops.pose.select_all(action="SELECT")
        bpy.ops.pose.transforms_clear()
        bpy.ops.pose.select_all(action="DESELECT")

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 

class PoseMode(bpy.types.Operator):
    bl_idname = "mph.pose_mode"
    bl_label = "Pose_Mode"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'POSE')

        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 
    
class DeleteRig(bpy.types.Operator):
    bl_idname = "mph.delete_rig"
    bl_label = "Delete_Rig"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        def del_collection(coll):
            for c in coll.children:
                del_collection(c)
                try:
                    bpy.data.collections.remove(coll,do_unlink=True)
                except:
                    print("Some StructRNA errors. This is normal because im lazy.")

        coll_name = bpy.context.active_object.users_collection[0].name
        del_collection(bpy.data.collections[coll_name])
            
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 
    
class PurgeOrphans(bpy.types.Operator):
    bl_idname = "mph.purge_orphans"
    bl_label = "Purge_Orphans"
    bl_options = {"REGISTER", "UNDO"}

    @classmethod
    def poll(cls, context):
        return not False

    def execute(self, context):

        bpy.data.orphans_purge(True, True, True)
            
        return {"FINISHED"}

    def invoke(self, context, event):
        return self.execute(context) 
    

classes = [
    LoadAnaPose,
    LoadAnaBone,
    ExportAnaPose, 
    ImportMiqF,
    ImportMiqM,
    ImportAuraF,
    ImportAuraM,
    ImportVieraF,
    ImportVieraM,
    ImportLalaF,
    ImportLalaM,
    SkirtToggle,
    ClearTransforms,
    DeleteRig,
    PoseMode,
    PurgeOrphans
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)