bl_info = {
    "name": "Kabanero Map Format",
    "author": "Toni Pesola",
    "version": (0, 1, 0),
    "blender": (2, 77, 0),
    "location": "File > Import-Export",
    "category": "Import-Export"}

if "bpy" in locals():
    import importlib
    if "export_kabanero" in locals():
        importlib.reload(export_kabanero)


import bpy
from bpy.props import (
        BoolProperty,
        FloatProperty,
        StringProperty,
        EnumProperty,
        )
from bpy_extras.io_utils import (
        ImportHelper,
        ExportHelper,
        orientation_helper_factory,
        path_reference_mode,
        axis_conversion,
        )

IOKBOrientationHelper = orientation_helper_factory("IOKBOrientationHelper", axis_forward='-Z', axis_up='Y')

class ExportKabanero(bpy.types.Operator, ExportHelper, IOKBOrientationHelper):
    """Save a Kabanero map file"""

    bl_idname = "export_scene.kbmap"
    bl_label = 'Export Kabanero Map'
    bl_options = {'PRESET'}

    filename_ext = ".kbmap"
    filter_glob = StringProperty(
            default="*.kbmap",
            options={'HIDDEN'},
            )

    # context group
    use_selection = BoolProperty(
            name="Selection Only",
            description="Export selected objects only",
            default=False,
            )

    global_scale = FloatProperty(
            name="Scale",
            min=0.01, max=1000.0,
            default=1.0,
            )

    # path_mode = path_reference_mode

    check_extension = True

    def execute(self, context):
        from . import export_kabanero

        from mathutils import Matrix
        keywords = self.as_keywords(ignore=("axis_forward",
                                            "axis_up",
                                            "global_scale",
                                            "check_existing",
                                            "filter_glob",
                                            ))

        global_matrix = (Matrix.Scale(self.global_scale, 4) *
                         axis_conversion(to_forward=self.axis_forward,
                                         to_up=self.axis_up,
                                         ).to_4x4())

        keywords["global_matrix"] = global_matrix
        return export_kabanero.save(context, **keywords)


def menu_func_export(self, context):
    self.layout.operator(ExportKabanero.bl_idname, text="Kabanero Map (.kbmap)")


def register():
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_file_export.append(menu_func_export)


def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_file_export.remove(menu_func_export)

if __name__ == "__main__":
    register()
