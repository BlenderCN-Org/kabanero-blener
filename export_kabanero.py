import os

import bpy
import mathutils
import bpy_extras.io_utils
import json
# import logging
# logging.basicConfig(level=logging.DEBUG,format='(%(threadName)-10s) %(message)s',)

from progress_report import ProgressReport, ProgressReportSubstep

def _get_library_name(obj):
    """ gets filename from filepath eg. //testlib.blend => testlib """
    filepath = obj.dupli_group.library.filepath
    s = filepath.rfind("/") + 1
    e = filepath.rfind(".")
    return filepath[s:e]

def _get_data_dict(obj, prefab=False):
    res = {
        "name":         obj.name,
        "transform": {
            "position": {
                "x":    obj.location.x,
                "y":    obj.location.y,
                "z":    obj.location.z
            },
            "scale": {
                "x":    obj.scale.x,
                "y":    obj.scale.y,
                "z":    obj.scale.z
            },
            "rotation": {
                "w":    obj.rotation_quaternion[0],
                "x":    obj.rotation_quaternion[1],
                "y":    obj.rotation_quaternion[2],
                "z":    obj.rotation_quaternion[3]
            }
        }
    }

    if prefab:
        res["library"] = _get_library_name(obj)
        res["object"] = obj.dupli_group.name

    return res

def _is_prefab(o):
    return o.dupli_type == "GROUP"

def save(context, filepath, *, use_selection=True, global_matrix=None):
    scene = context.scene

    # Exit edit mode
    if bpy.ops.object.mode_set.poll():
        bpy.ops.object.mode_set(mode='OBJECT')

    if use_selection:
        objects = context.selected_objects
    else:
        objects = scene.objects

    map_data = {
        "prefabs": [],
        "entities": []
    }

    for o in objects:
        if _is_prefab(o):
            map_data["prefabs"].append(_get_data_dict(o, prefab=True))
        else:
            map_data["entities"].append(_get_data_dict(o, prefab=False))

    # # Prefabs
    # prefab_objects = [o for o in objects if _is_prefab(o)]
    # for p in prefab_objects:
    #     map_data["prefabs"].append(_get_data_dict(p, prefab=True))
    #
    # # Other objects
    # entity_objects = [o for o in objects if _is_prefab(o)]
    #
    # for p in prefab_objects:
    #     map_data["entities"].append(_get_data_dict(p, prefab=False))

    print(json.dumps(map_data, indent=2, sort_keys=True))

    return {'FINISHED'}
