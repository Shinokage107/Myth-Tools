import bpy
import bpy.utils.previews

# everything meaningful currently lives in this class, the two subpanels are commented out of register(). It may be useful to turn them into their own panels if they get enough content to be worth collapsing.
class MPH_Export(bpy.types.Panel):
    bl_idname = "MPH_PT_PoseHelper"
    bl_label = "Pose Export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Myth Tools"
    bl_order = 1

    def draw(self, context):
        layout = self.layout

        scene = context.scene

        layout.prop(scene, "anamnesis_armature", text="Rig")
        layout.operator("pose.export_ana_pose", text="Export")

class MPH_RigLayers(bpy.types.Panel):
    bl_label = 'Rig Layers'
    bl_idname = 'MPH_PT_Layers'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Myth Tools'
    bl_order = 3
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return context.active_object is not None and context.active_object.type == 'ARMATURE' and context.active_object.name.startswith('Myth')

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout

        col = layout.column()
        
        row = col.row()
        row.prop(context.active_object.data.collections['Layer 1'], 'is_visible', toggle=True, text='Essential')

        row = col.row()
        row.prop(context.active_object.data.collections['Layer 2'], 'is_visible', toggle=True, text='Face')
        row.prop(context.active_object.data.collections['Layer 3'], 'is_visible', toggle=True, text='Hands')
        
        row = col.row()
        row.prop(context.active_object.data.collections['Layer 8'], 'is_visible', toggle=True, text='Tail')
        row.prop(context.active_object.data.collections['Layer 24'], 'is_visible', toggle=True, text='Ears')

        row = col.row()
        row.prop(context.active_object.data.collections['Layer 5'], 'is_visible', toggle=True, text='ClothR')
        row.prop(context.active_object.data.collections['Layer 6'], 'is_visible', toggle=True, text='ClothL')
        
        row = col.row()
        row.prop(context.active_object.data.collections['Layer 17'], 'is_visible', toggle=True, text='Adjuster')   

class MPH_RigCollection(bpy.types.Panel):
    bl_label = 'Rig Collection'
    bl_idname = 'MPH_PT_RigCollection'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Myth Tools'
    bl_order = 2
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.alert = False
        box.enabled = True
        box.active = True
        box.use_property_split = False
        box.use_property_decorate = False
        box.alignment = 'Expand'.upper()
        box.scale_x = 3.0
        box.scale_y = 3.0
        box.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        
        split = box.split(factor=0.5, align=False)
        split.alert = False
        split.enabled = True
        split.active = True
        split.use_property_split = False
        split.use_property_decorate = False
        split.scale_x = 1.0
        split.scale_y = 1.0
        split.alignment = 'Expand'.upper()
        split.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        split.popover('MPH_PT_MaleRigs', text='Male Rigs', icon_value=0)
        split.popover('MPH_PT_FemaleRigs', text='Female Rigs', icon_value=0)




class MPH_FemaleRigs(bpy.types.Panel):
    bl_label = 'Female Rigs'
    bl_idname = 'MPH_PT_FemaleRigs'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_order = 0
    bl_options = {'HIDE_HEADER', 'DEFAULT_CLOSED'}
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.alert = False
        box.enabled = True
        box.active = True
        box.use_property_split = False
        box.use_property_decorate = False
        box.alignment = 'Expand'.upper()
        box.scale_x = 1.0
        box.scale_y = 1.0
        box.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = box.operator('mph.import_miq_f', text='Miqote', icon_value=241, emboss=True, depress=False)
        op = box.operator('mph.import_aura_f', text='Aura', icon_value=241, emboss=True, depress=False)
        op = box.operator('mph.import_viera_f', text='Viera', icon_value=241, emboss=True, depress=False)
        op = box.operator('mph.import_lala_f', text='Lalafel', icon_value=241, emboss=True, depress=False)


class MPH_MaleRigs(bpy.types.Panel):
    bl_label = 'Male Rigs'
    bl_idname = 'MPH_PT_MaleRigs'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'WINDOW'
    bl_order = 0
    bl_options = {'HIDE_HEADER', 'DEFAULT_CLOSED'}
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.alert = False
        box.enabled = True
        box.active = True
        box.use_property_split = False
        box.use_property_decorate = False
        box.alignment = 'Expand'.upper()
        box.scale_x = 1.0
        box.scale_y = 1.0
        box.operator_context = "INVOKE_DEFAULT" if True else "EXEC_DEFAULT"
        op = box.operator('mph.import_miq_m', text='Miqote', icon_value=172, emboss=True, depress=False)
        op = box.operator('mph.import_aura_m', text='Aura', icon_value=172, emboss=True, depress=False)
        op = box.operator('mph.import_viera_m', text='Viera', icon_value=172, emboss=True, depress=False)
        op = box.operator('mph.import_lala_m', text='Lalafel', icon_value=172, emboss=True, depress=False)


class MPH_Utils(bpy.types.Panel):
    bl_idname = "MPH_PT_Utils"
    bl_label = "Utils"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Myth Tools"
    bl_order = 5
    bl_options = {'HEADER_LAYOUT_EXPAND'}
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout

        layout.operator("mph.skirt_toggle", text="Toggle Skirt", icon = "MATCLOTH")
        try:
            if(context.active_object is not None and context.active_object.type == "ARMATURE"):
                layout.operator("mph.pose_mode", text="Pose Mode", icon = "POSE_HLT")
                layout.operator("mph.clear_transforms", text="Reset Pose", icon = "ARMATURE_DATA")
                layout.operator("mph.delete_rig", text="Delete Rig", icon = "ERROR")
        except: 
            #This is to prevent some shitty errors happening cause python sucks and i dont want users of the plugin to be confused by random errors. 
            print("Somethin went wrong, but dw.")
        layout.operator("mph.purge_orphans", text="Clean Up File", icon = "FILE_BACKUP")
            
class MPH_ShamelessPlug(bpy.types.Panel):
    bl_label = 'Myth Tools 0.7.2'
    bl_idname = 'MPH_PT_Plug'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Myth Tools'
    bl_order = 0
    bl_ui_units_x=0

    @classmethod
    def poll(cls, context):
        return not (False)

    def draw_header(self, context):
        layout = self.layout

    def draw(self, context):
        layout = self.layout
        exec('op =' + 'layout.' + 'operator(' + "'wm.url_open'," + "text='Support me on Kofi!'," + 'icon_value=227,' + 'emboss=True,' + 'depress=False,)' + ".url = '" + 'https://ko-fi.com/mythmakerstudio' + "'")
        exec('op =' + 'layout.' + 'operator(' + "'wm.url_open'," + "text='Join Discord'," + 'icon_value=718,' + 'emboss=True,' + 'depress=False,)' + ".url = '" + 'https://discord.gg/mythmaker' + "'")

classes = [
    MPH_Export,
    MPH_RigCollection,
    MPH_FemaleRigs,
    MPH_MaleRigs,
    MPH_RigLayers,
    MPH_Utils,
    MPH_ShamelessPlug
    
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

