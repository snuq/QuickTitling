# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


import bpy
import blf
import mathutils
import os
import glob
import gpu
from gpu_extras.batch import batch_for_shader
from math import pi
from bpy_extras.io_utils import ImportHelper, ExportHelper
from bpy_extras.image_utils import load_image
import bpy.utils.previews

bl_info = {
    "name": "VSE Quick Titling",
    "description": "Enables easy creation of simple title scenes in the VSE",
    "author": "Hudson Barkley (Snu)",
    "version": (0, 6, 1),
    "blender": (2, 81, 0),
    "location": "Sequencer Panels",
    "wiki_url": "https://github.com/snuq/QuickTitling",
    "category": "Sequencer"
}

animations = [
    {
        'name': 'Fade In And Out',
        'variable': 'Alpha',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Random Flicker',
        'variable': 'Alpha',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 0.1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'RANDOM'
    },
    {
        'name': 'SPACER'
    },
    {
        'name': 'X Slide From Right',
        'variable': 'X Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 2,
        'out_amount': 2,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'X Slide From Left',
        'variable': 'X Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -2,
        'out_amount': -2,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'X Cycle Slide Across',
        'variable': 'X Slide',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 2,
        'cycle_offset': 0,
        'cycle_type': 'TANGENT'
    },
    {
        'name': 'Y Slide Up And Down',
        'variable': 'Y Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -1,
        'out_amount': -1,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Y Slide Down And Up',
        'variable': 'Y Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 1,
        'out_amount': 1,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Y Cycle Slide Up',
        'variable': 'Y Slide',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 2,
        'cycle_offset': 0,
        'cycle_type': 'TANGENT'
    },
    {
        'name': 'Z Slide Forward And Back',
        'variable': 'Z Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -2,
        'out_amount': -2,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Z Slide Back And Forward',
        'variable': 'Z Slide',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 2,
        'out_amount': 2,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Z Cycle Slide Forward',
        'variable': 'Z Slide',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 2,
        'cycle_offset': 0,
        'cycle_type': 'TANGENT'
    },
    {
        'name': 'SPACER'
    },
    {
        'name': 'X Tilt Forward And Back',
        'variable': 'X Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -90,
        'out_amount': -90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'X Tilt Backward And Forward',
        'variable': 'X Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 90,
        'out_amount': 90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'X Tilt Wobble',
        'variable': 'X Rotate',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 2,
        'cycle_offset': 0,
        'cycle_type': 'SINE'
    },
    {
        'name': 'Y Turn Forward And Back',
        'variable': 'Y Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -90,
        'out_amount': -90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Y Turn Backward And Forward',
        'variable': 'Y Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 90,
        'out_amount': 90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Y Turn Wobble',
        'variable': 'Y Rotate',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 2,
        'cycle_offset': 0,
        'cycle_type': 'SINE'
    },
    {
        'name': 'Z Spin Forward And Back',
        'variable': 'Z Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 90,
        'out_amount': 90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Z Spin Backward And Forward',
        'variable': 'Z Rotate',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': -90,
        'out_amount': -90,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Z Spin Wobble',
        'variable': 'Z Rotate',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'SINE'
    },
    {
        'name': 'SPACER'
    },
    {
        'name': 'Width Grow And Shrink',
        'variable': 'Width',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Width Random Cycle',
        'variable': 'Width',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'RANDOM'
    },
    {
        'name': 'Height Grow And Shrink',
        'variable': 'Height',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Height Random Cycle',
        'variable': 'Height',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'RANDOM'
    },
    {
        'name': 'Depth Grow And Shrink',
        'variable': 'Depth',
        'animate_in': True,
        'animate_out': True,
        'in_length': 15,
        'out_length': 15,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 1,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'NONE'
    },
    {
        'name': 'Depth Random Cycle',
        'variable': 'Depth',
        'animate_in': False,
        'animate_out': False,
        'in_length': 0,
        'out_length': 0,
        'in_offset': 0,
        'out_offset': 0,
        'in_amount': 0,
        'out_amount': 0,
        'cycle_x_scale': 2,
        'cycle_y_scale': 1,
        'cycle_offset': 0,
        'cycle_type': 'RANDOM'
    }
]

quicktitle_previews = bpy.utils.previews.new()

current_icon_id = 0

overlays = None

overlay_info = ''

keymap = None

current_bounds = {}


def find_load_image(path, load=True):
    abs_path = bpy.path.abspath(path)
    for image in bpy.data.images:
        if bpy.path.abspath(image.filepath) == abs_path:
            return image
    if load:
        return load_image(path)
    else:
        return None


def object_at_location(scene, x, y):
    #Casts a ray from the camera to the given coordinates and returns the first object in that direction, or None
    oldscene = bpy.context.window.scene
    bpy.context.window.scene = scene  #Since blender doesnt want to cast the ray properly while in another scene... bah.
    camera = scene.camera
    #since blender doesnt detect curve objects... go through and make low-poly copies of all curves, then delete them. bah.
    title_copies = []
    for title_object in scene.objects:
        if title_object.type in ['CURVE', 'FONT']:
            scale = title_object.scale
            location = title_object.location
            rotation = title_object.rotation_euler
            old_resolution_u = title_object.data.resolution_u
            old_bevel_resolution = title_object.data.bevel_resolution
            title_object.data.resolution_u = 2
            title_object.data.bevel_resolution = 0

            #mesh = title_object.to_mesh(preserve_all_data_layers=True, depsgraph=bpy.context.view_layer.depsgraph)
            mesh = bpy.data.meshes.new_from_object(title_object, preserve_all_data_layers=True, depsgraph=bpy.context.view_layer.depsgraph)
            ob = bpy.data.objects.new(mesh.name+' Raycast', mesh)
            scene.collection.objects.link(ob)
            ob.scale = scale
            ob.location = location
            ob.rotation_euler = rotation
            title_copies.append([mesh, ob, title_object])

            title_object.data.resolution_u = old_resolution_u
            title_object.data.bevel_resolution = old_bevel_resolution
    direction = (mathutils.Vector((x, y, 0)) - camera.location).normalized()
    bpy.context.view_layer.depsgraph.update()
    data = scene.ray_cast(scene.view_layers[0], camera.location, direction)
    if data[0]:
        match_object = data[4]
    else:
        match_object = None
    for copy in title_copies:
        mesh, ob, title_object = copy
        if data[0]:
            if data[4] == ob:
                match_object = title_object
        scene.collection.objects.unlink(ob)
        bpy.data.objects.remove(ob)
        bpy.data.meshes.remove(mesh)
    bpy.context.view_layer.depsgraph.update()
    bpy.context.window.scene = oldscene
    return match_object


def draw_line(sx, sy, ex, ey, width, color=(1.0, 1.0, 1.0, 1.0)):
    del width
    coords = [(sx, sy), (ex, ey)]
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {'pos': coords})
    shader.bind()
    shader.uniform_float('color', color)
    batch.draw(shader)


def draw_text(x, y, size, text, color=(1.0, 1.0, 1.0, 1.0)):
    font_id = 0
    blf.color(font_id, *color)
    blf.position(font_id, x, y, 0)
    blf.size(font_id, size, 72)
    blf.draw(font_id, text)


def draw_box(left, bottom, right, top, color=(1.0, 1.0, 0.0, 1.0)):
    coords = [(left, bottom), (left, top), (left, top), (right, top), (right, top), (right, bottom), (right, bottom), (left, bottom)]
    shader = gpu.shader.from_builtin('2D_UNIFORM_COLOR')
    batch = batch_for_shader(shader, 'LINES', {'pos': coords})
    shader.bind()
    shader.uniform_float('color', color)
    batch.draw(shader)


def add_overlay(self=None, context=None):
    global overlays
    if not overlays:
        overlays = bpy.types.SpaceSequenceEditor.draw_handler_add(quicktitling_overlay, (), 'PREVIEW', 'POST_PIXEL')
        quicktitling_overlay()
        add_keymap()


def quicktitling_overlay():
    quicktitle_sequence = titling_scene_selected()
    if not quicktitle_sequence:
        global overlays
        global overlay_info
        if overlays:
            bpy.types.SpaceSequenceEditor.draw_handler_remove(overlays, 'PREVIEW')
            overlays = None
            remove_keymap()
    else:
        frame = bpy.context.scene.frame_current
        if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
            area = bpy.context.area
            space = area.spaces[0]
            if space.display_mode == 'IMAGE':
                scene = quicktitle_sequence.scene
                preset = scene.quicktitler.current_quicktitle
                try:
                    title_object_preset = preset.objects[preset.selected_object]
                    title_object_name = title_object_preset.internal_name
                    title_object = scene.objects[title_object_name]
                except:
                    title_object = None
                if title_object:
                    new_frame = bpy.context.scene.frame_current - quicktitle_sequence.frame_start
                    if scene.frame_current != new_frame:
                        scene.frame_set(new_frame)
                    region = area.regions[2]
                    view = region.view2d
                    min_x = title_object_preset.bbleft
                    max_x = title_object_preset.bbright
                    min_y = title_object_preset.bbbottom
                    max_y = title_object_preset.bbtop
                    left, bottom = view.view_to_region(min_x, min_y, clip=False)
                    right, top = view.view_to_region(max_x, max_y, clip=False)
                    if title_object_preset.type == 'TEXT' and title_object_preset.word_wrap:
                        #display text bounding box
                        camera_width = scene.render.resolution_x
                        wrap_width_per = title_object_preset.wrap_width
                        wrap_x_per = title_object_preset.x
                        wrap_width = wrap_width_per * camera_width
                        wrap_x = (wrap_x_per * (camera_width / 2)) - (wrap_width / 2)
                        w_left, very_bottom = view.view_to_region(wrap_x, 0, clip=False)
                        w_right, very_bottom = view.view_to_region(wrap_x + wrap_width, 0, clip=False)
                        draw_box(w_left, bottom, w_right, top, color=(.5, .5, 0, 1))
                    draw_box(left, bottom, right, top)
                    draw_text(10, 10, 15, overlay_info)


def clamp(x, minimum, maximum):
    return max(minimum, min(x, maximum))


def update_bounds(title_object, title_object_preset, title_scene, scale_multiplier, pos_multiplier):
    camera = title_scene.camera
    camera_x = bpy.context.scene.render.resolution_x
    camera_y = bpy.context.scene.render.resolution_y
    bounds = camera_view_bounds_2d(title_scene, camera, title_object, title_object_preset, camera_x, camera_y, scale_multiplier, pos_multiplier)
    title_object_preset.bbleft = bounds[0]
    title_object_preset.bbbottom = bounds[1]
    title_object_preset.bbright = bounds[2]
    title_object_preset.bbtop = bounds[3]


def generate_matrix_world(ob, ob_preset):
    scale_matrix = mathutils.Matrix.Scale(ob.scale[0], 4, (1, 0, 0)) @ mathutils.Matrix.Scale(ob.scale[1], 4, (0, 1, 0)) @ mathutils.Matrix.Scale(ob.scale[2], 4, (0, 0, 1))
    rotation_matrix = mathutils.Matrix.Rotation(ob.rotation_euler[0], 4, 'X') @ mathutils.Matrix.Rotation(ob.rotation_euler[1], 4, 'Y') @ mathutils.Matrix.Rotation(ob.rotation_euler[2], 4, 'Z')
    rotation_matrix.invert()
    if ob_preset.type == 'CIRCLE':
        #position is incorrect for circles... why??
        loc_mult = 2.83
        location_matrix = mathutils.Matrix.Translation((ob.location[0] * loc_mult, ob.location[1] * loc_mult, ob.location[2] * loc_mult))
    else:
        location_matrix = mathutils.Matrix.Translation(ob.location)
    matrix = location_matrix @ scale_matrix @ rotation_matrix
    return matrix


def camera_view_bounds_2d(scene, camera, title_object, title_object_preset, camera_x, camera_y, scale_multiplier, pos_multiplier):
    if title_object.type == 'MESH':
        #forget about the bounding box and just use the mesh itself
        bbox = title_object.data.vertices
    elif title_object.type == 'FONT':
        #well what do you know, this bounding box actually works correctly!
        bbox = title_object.bound_box
    else:
        #use the curve points
        bbox = title_object.data.splines[0].points
    xs = []
    ys = []
    #matrix = title_object.matrix_world
    matrix = generate_matrix_world(title_object, title_object_preset)

    for vert in bbox:
        if title_object.type != 'FONT':
            vert = vert.co
        transformed_vert = matrix @ mathutils.Vector(vert)
        xs.append(transformed_vert[0])
        ys.append(transformed_vert[1])

    multiplier = scale_multiplier
    min_x = min(xs) / multiplier
    max_x = max(xs) / multiplier
    min_y = min(ys) / multiplier
    max_y = max(ys) / multiplier

    camera_x_half = (camera_x / 2)
    camera_y_half = (camera_y / 2)

    min_x_px = clamp(min_x * camera_x_half, -camera_x_half, camera_x_half)
    max_x_px = clamp(max_x * camera_x_half, -camera_x_half, camera_x_half)
    min_y_px = clamp(min_y * camera_x_half, -camera_y_half, camera_y_half)
    max_y_px = clamp(max_y * camera_x_half, -camera_y_half, camera_y_half)

    dimensions = [min_x_px, min_y_px, max_x_px, max_y_px]

    return dimensions


def to_bool(value):
    """Function to convert various Non-Boolean true/false values to Boolean.
    Inputs that return True are:
        'Yes', 'yes', 'True', 'True', 'T', 't', '1', 1, 'Down', 'down'
    Any other value returns a False.
    """
    return str(value).lower() in ('yes', 'true', 't', '1', 'down')


def set_default(preset):
    preset.name = get_default('name', class_type='Title')
    preset.description = get_default('description', class_type='Title')
    preset.z_scale = get_default('z_scale', class_type='Title')
    preset.objects.clear()
    preset.selected_object = 0
    preset.enable_shadows = get_default('enable_shadows', class_type='Title')
    preset.shadowlamp_internal_name = ""
    preset.lampcenter_internal_name = ""
    preset.shadowsize = get_default('shadowsize', class_type='Title')
    preset.shadowamount = get_default('shadowamount', class_type='Title')
    preset.shadowsoft = get_default('shadowsoft', class_type='Title')
    preset.shadowx = get_default('shadowx', class_type='Title')
    preset.shadowy = get_default('shadowy', class_type='Title')
    preset.length = get_default('length', class_type='Title')
    preset.lightscalex = get_default('lightscalex', class_type='Title')
    preset.lightscaley = get_default('lightscaley', class_type='Title')
    preset.lightx = get_default('lightx', class_type='Title')
    preset.lighty = get_default('lighty', class_type='Title')
    preset.lightrot = get_default('lightrot', class_type='Title')


def get_presets_directory():
    script_file = os.path.realpath(__file__)
    directory = os.path.dirname(script_file)
    return directory+os.path.sep+'QuickTitling Presets'


def list_quicktitle_presets(scene):
    presets = []
    #Load up scene presets
    for quicktitle in scene.quicktitler.quicktitles:
        presets.append([quicktitle.name, 'SCENE'])
    #load up builtin presets
    preset_dir = get_presets_directory()
    builtin_presets = glob.glob(preset_dir+os.path.sep+'*.xml')
    for preset in builtin_presets:
        preset_name = os.path.splitext(os.path.basename(preset))[0]
        if preset_name != 'QuickTitling Export Example':
            presets.append([preset_name, 'BUILTIN'])
    return presets


def scene_quicktitle_from_name(quicktitles, name):
    for quicktitle in quicktitles:
        if quicktitle.name == name:
            return quicktitle
    return None


def get_default(value, class_type='Object'):
    if class_type == 'Object':
        return QuickTitleObject.bl_rna.properties[value].default
    elif class_type == 'Animation':
        return QuickTitleAnimation.bl_rna.properties[value].default
    else:  #class_type == 'Title'
        return QuickTitle.bl_rna.properties[value].default


def load_quicktitle(filepath, preset):
    #load a quicktitle preset from a given xml file
    preset_location = os.path.dirname(bpy.path.abspath(filepath))
    import xml.etree.cElementTree as Tree
    tree = Tree.parse(filepath)
    root = tree.getroot()
    preset.name = root.findtext('name', default=os.path.splitext(bpy.path.basename(filepath))[0])
    preset.description = root.findtext('description', default="")
    preset.z_scale = abs(float(root.findtext('z_scale', default=str(get_default('z_scale', class_type='Title')))))
    preset.length = abs(int(root.findtext('length', default=str(get_default('length', class_type='Title')))))
    preset.shadowsize = abs(float(root.findtext('shadowsize', default=str(get_default('shadowsize', class_type='Title')))))
    shadowamount = abs(float(root.findtext('shadowamount', default=str(get_default('shadowamount', class_type='Title')))))
    if shadowamount > 1:
        preset.shadowamount = 1
    else:
        preset.shadowamount = shadowamount
    preset.shadowsoft = abs(float(root.findtext('shadowsoft', default=str(get_default('shadowsoft', class_type='Title')))))
    preset.shadowx = float(root.findtext('shadowx', default=str(get_default('shadowx', class_type='Title'))))
    preset.shadowy = float(root.findtext('shadowy', default=str(get_default('shadowy', class_type='Title'))))
    preset.lightscalex = float(root.findtext('lightscalex', default=str(get_default('lightscalex', class_type='Title'))))
    preset.lightscaley = float(root.findtext('lightscaley', default=str(get_default('lightscaley', class_type='Title'))))
    preset.lightx = float(root.findtext('lightx', default=str(get_default('lightx', class_type='Title'))))
    preset.lighty = float(root.findtext('lighty', default=str(get_default('lighty', class_type='Title'))))
    preset.lightrot = float(root.findtext('lightrot', default=str(get_default('lightrot', class_type='Title'))))
    objects = root.findall('objects')
    preset.objects.clear()
    for title_object in objects:
        newobject = preset.objects.add()
        newobject.name = title_object.findtext('name', default="")
        object_type = title_object.findtext('type', default="TEXT")
        if object_type in ['IMAGE', 'BOX', 'CIRCLE', 'TEXT']:
            newobject.type = object_type
        else:
            newobject.type = 'BOX'
        newobject.x = float(title_object.findtext('x', default=str(get_default('x'))))
        newobject.y = float(title_object.findtext('y', default=str(get_default('y'))))
        newobject.z = float(title_object.findtext('z', default=str(get_default('z'))))
        newobject.rot_x = float(title_object.findtext('rot_x', default=str(get_default('rot_x'))))
        newobject.rot_y = float(title_object.findtext('rot_y', default=str(get_default('rot_y'))))
        newobject.rot_z = float(title_object.findtext('rot_z', default=str(get_default('rot_z'))))
        scale = abs(float(title_object.findtext('scale', default=str(get_default('scale')))))
        if scale > 0:
            newobject.scale = scale
        else:
            newobject.scale = 1
        width = abs(float(title_object.findtext('width', default=str(get_default('width')))))
        if width > 0:
            newobject.width = width
        else:
            newobject.width = 1
        height = abs(float(title_object.findtext('height', default=str(get_default('height')))))
        if height > 0:
            newobject.height = height
        else:
            newobject.height = 1
        shear = float(title_object.findtext('shear', default=str(get_default('shear'))))
        if shear < -1:
            shear = -1
        if shear > 1:
            shear = 1
        newobject.shear = shear
        newobject.cast_shadows = to_bool(title_object.findtext('cast_shadows', default=str(get_default('cast_shadows'))))
        newobject.set_material = to_bool(title_object.findtext('set_material', default=str(get_default('set_material'))))
        newobject.set_material_name = title_object.findtext('set_material_name', default=get_default('set_material_name'))
        newobject.material = title_object.findtext('material', default=get_default('material'))
        newobject.use_shadeless = to_bool(title_object.findtext('use_shadeless', default=str(get_default('use_shadeless'))))
        alpha = abs(float(title_object.findtext('alpha', default=str(get_default('alpha')))))
        if alpha > 1:
            newobject.alpha = 1
        else:
            newobject.alpha = alpha
        index_of_refraction = abs(float(title_object.findtext('index_of_refraction', default=str(get_default('index_of_refraction')))))
        if index_of_refraction > 50:
            newobject.index_of_refraction = 50
        else:
            newobject.index_of_refraction = index_of_refraction
        transmission = abs(float(title_object.findtext('transmission', default=str(get_default('transmission')))))
        if transmission > 1:
            newobject.transmission = 1
        else:
            newobject.transmission = transmission
        specular_intensity = abs(float(title_object.findtext('specular_intensity', default=str(get_default('specular_intensity')))))
        if specular_intensity > 1:
            newobject.specular_intensity = 1
        else:
            newobject.specular_intensity = specular_intensity
        metallic = abs(float(title_object.findtext('metallic', default=str(get_default('metallic')))))
        if metallic > 1:
            newobject.metallic = 1
        else:
            newobject.metallic = metallic
        roughness = abs(float(title_object.findtext('roughness', default=str(get_default('roughness')))))
        if roughness > 1:
            newobject.roughness = 1
        else:
            newobject.roughness = roughness
        newobject.extrude = abs(float(title_object.findtext('extrude', default=str(get_default('extrude')))))
        newobject.bevel = abs(float(title_object.findtext('bevel', default=str(get_default('bevel')))))
        newobject.bevel_resolution = abs(int(title_object.findtext('bevel_resolution', default=str(get_default('bevel_resolution')))))
        newobject.text = title_object.findtext('text', default=get_default('text'))
        newobject.font = title_object.findtext('font', default=get_default('font'))
        newobject.word_wrap = to_bool(title_object.findtext('word_wrap', default=str(get_default('word_wrap'))))
        wrap_width = abs(float(title_object.findtext('wrap_width', default=str(get_default('wrap_width')))))
        if wrap_width > 1:
            newobject.wrap_width = 1
        elif wrap_width < 0.01:
            newobject.wrap_width = 0.01
        else:
            newobject.wrap_width = wrap_width
        align = title_object.findtext('align', default=str(get_default('align')))
        if align in ['LEFT', 'CENTER', 'RIGHT', 'JUSTIFY', 'FLUSH']:
            newobject.align = align
        else:
            newobject.align = 'CENTER'
        newobject.outline = to_bool(title_object.findtext('outline', default=str(get_default('outline'))))
        newobject.outline_size = abs(float(title_object.findtext('outline_size', default=str(get_default('outline_size')))))
        outline_alpha = abs(float(title_object.findtext('outline_alpha', default=str(get_default('outline_alpha')))))
        if outline_alpha > 1:
            outline_alpha = 1
        newobject.outline_alpha = outline_alpha
        outline_color = title_object.findtext('outline_diffuse_color', "0, 0, 0").replace(' ', '').replace('(', '').replace(')', '').split(',')
        if len(outline_color) != 3:
            newobject.outline_diffuse_color = (0, 0, 0)
        else:
            newobject.outline_diffuse_color = (int(outline_color[0]) / 255.0, int(outline_color[1]) / 255.0, int(outline_color[2]) / 255.0)
        window_mapping = title_object.findtext('window_mapping', default=get_default('window_mapping'))
        newobject.window_mapping = to_bool(window_mapping)
        texture = title_object.findtext('texture', default=get_default('texture'))
        if not os.path.isfile(os.path.abspath(bpy.path.abspath(texture))):
            test_texture = os.path.join(preset_location, texture)
            if os.path.isfile(test_texture):
                texture = test_texture
        newobject.texture = texture
        alpha_texture = title_object.findtext('alpha_texture', default=get_default('alpha_texture'))
        if not os.path.isfile(os.path.abspath(bpy.path.abspath(alpha_texture))):
            test_texture = os.path.join(preset_location, alpha_texture)
            if os.path.isfile(test_texture):
                alpha_texture = test_texture
        newobject.alpha_texture = alpha_texture
        newobject.loop = to_bool(title_object.findtext('loop', default=str(get_default('loop'))))
        newobject.frame_offset = abs(int(title_object.findtext('frame_offset', default=str(get_default('frame_offset')))))
        frame_length = abs(int(title_object.findtext('frame_length', default=str(get_default('frame_length')))))
        if frame_length > 1:
            newobject.frame_length = frame_length
        else:
            newobject.frame_length = 1
        diffuse_color = title_object.findtext('diffuse_color', default="255, 255, 255").replace(' ', '').replace('(', '').replace(')', '').split(',')
        if len(diffuse_color) != 3:
            newobject.diffuse_color = (1, 1, 1)
        else:
            newobject.diffuse_color = (int(diffuse_color[0]) / 255.0, int(diffuse_color[1]) / 255.0, int(diffuse_color[2]) / 255.0)
        object_animations = title_object.findall('animations')
        for animation in object_animations:
            newanimation = newobject.animations.add()
            newanimation.variable = animation.findtext('variable', default=str(get_default('variable', class_type='Animation')))
            newanimation.animate_in = to_bool(animation.findtext('animate_in', default=str(get_default('animate_in', class_type='Animation'))))
            newanimation.animate_out = to_bool(animation.findtext('animate_out', default=str(get_default('animate_out', class_type='Animation'))))
            newanimation.in_length = abs(int(animation.findtext('in_length', default=str(get_default('in_length', class_type='Animation')))))
            newanimation.out_length = abs(int(animation.findtext('out_length', default=str(get_default('out_length', class_type='Animation')))))
            newanimation.in_offset = int(animation.findtext('in_offset', default=str(get_default('in_offset', class_type='Animation'))))
            newanimation.out_offset = int(animation.findtext('out_offset', default=str(get_default('out_offset', class_type='Animation'))))
            newanimation.in_amount = float(animation.findtext('in_amount', default=str(get_default('in_amount', class_type='Animation'))))
            newanimation.out_amount = float(animation.findtext('out_amount', default=str(get_default('out_amount', class_type='Animation'))))
            cycle_type = animation.findtext('cycle_type', default=get_default('cycle_type', class_type='Animation'))
            if cycle_type not in ['NONE', 'SINE', 'TANGENT', 'RANDOM']:
                cycle_type = 'NONE'
            newanimation.cycle_type = cycle_type
            newanimation.cycle_x_scale = abs(float(animation.findtext('cycle_x_scale', default=str(get_default('cycle_x_scale', class_type='Animation')))))
            newanimation.cycle_y_scale = float(animation.findtext('cycle_y_scale', default=str(get_default('cycle_y_scale', class_type='Animation'))))
            newanimation.cycle_offset = float(animation.findtext('cycle_offset', default=str(get_default('cycle_offset', class_type='Animation'))))
    return preset


def get_current_object(quicktitle_preset=None):
    #Get the current quicktitle preset object
    if not quicktitle_preset:
        quicktitle_preset = current_quicktitle()
    if not quicktitle_preset:
        return False
    else:
        current_object_index = quicktitle_preset.selected_object
        current_object = quicktitle_preset.objects[current_object_index]
        return current_object


def find_titling_scene():
    #If the active sequence is a title scene, return that scene, otherwise return the current scene
    selected = titling_scene_selected()
    if selected:
        return selected.scene
    else:
        return bpy.context.scene


def titling_scene_selected():
    #determines if a titling scene is selected
    sequence_editor = bpy.context.scene.sequence_editor
    if hasattr(sequence_editor, 'active_strip'):
        #there is an active strip
        active_sequence = sequence_editor.active_strip
        if active_sequence and active_sequence.select:
            if active_sequence.type == 'SCENE':
                #this is a scene strip
                if 'QuickTitle:' in active_sequence.name:
                    #strip is named properly
                    return active_sequence
    return None


def current_quicktitle(sequence=None):
    #Function to return the current QuickTitle preset depending on what is selected in the sequencer
    if not sequence:
        sequence = titling_scene_selected()
    if sequence:
        scene = sequence.scene
    else:
        scene = find_titling_scene()
    return scene.quicktitler.current_quicktitle


def copy_object(oldobject, newobject):
    newobject.name = oldobject.name
    newobject.type = oldobject.type
    newobject.x = oldobject.x
    newobject.y = oldobject.y
    newobject.z = oldobject.z
    newobject.rot_x = oldobject.rot_x
    newobject.rot_y = oldobject.rot_y
    newobject.rot_z = oldobject.rot_z
    newobject.scale = oldobject.scale
    newobject.width = oldobject.width
    newobject.height = oldobject.height
    newobject.shear = oldobject.shear
    newobject.set_material = oldobject.set_material
    newobject.set_material_name = oldobject.set_material_name
    newobject.material = oldobject.material
    newobject.cast_shadows = oldobject.cast_shadows
    newobject.use_shadeless = oldobject.use_shadeless
    newobject.alpha = oldobject.alpha
    newobject.index_of_refraction = oldobject.index_of_refraction
    newobject.transmission = oldobject.transmission
    newobject.diffuse_color = oldobject.diffuse_color
    newobject.specular_intensity = oldobject.specular_intensity
    newobject.metallic = oldobject.metallic
    newobject.roughness = oldobject.roughness
    newobject.extrude = oldobject.extrude
    newobject.bevel = oldobject.bevel
    newobject.bevel_resolution = oldobject.bevel_resolution
    newobject.text = oldobject.text
    newobject.font = oldobject.font
    newobject.word_wrap = oldobject.word_wrap
    newobject.wrap_width = oldobject.wrap_width
    newobject.align = oldobject.align
    newobject.outline = oldobject.outline
    newobject.outline_size = oldobject.outline_size
    newobject.outline_alpha = oldobject.outline_alpha
    newobject.outline_diffuse_color = oldobject.outline_diffuse_color
    newobject.window_mapping = oldobject.window_mapping
    newobject.texture = oldobject.texture
    newobject.alpha_texture = oldobject.alpha_texture
    newobject.loop = oldobject.loop
    newobject.frame_offset = oldobject.frame_offset
    newobject.frame_length = oldobject.frame_length
    newobject.animations.clear()
    for oldanimation in oldobject.animations:
        newanimation = newobject.animations.add()
        copy_animation(oldanimation, newanimation)


def copy_animation(oldanimation, newanimation):
    newanimation.variable = oldanimation.variable
    newanimation.animate_in = oldanimation.animate_in
    newanimation.animate_out = oldanimation.animate_out
    newanimation.in_length = oldanimation.in_length
    newanimation.out_length = oldanimation.out_length
    newanimation.in_offset = oldanimation.in_offset
    newanimation.out_offset = oldanimation.out_offset
    newanimation.in_amount = oldanimation.in_amount
    newanimation.out_amount = oldanimation.out_amount
    newanimation.cycle_x_scale = oldanimation.cycle_x_scale
    newanimation.cycle_y_scale = oldanimation.cycle_y_scale
    newanimation.cycle_offset = oldanimation.cycle_offset
    newanimation.cycle_type = oldanimation.cycle_type


def copy_title_preset(old_title, title):
    #Function to copy one QuickTitle preset to another
    title.name = old_title.name
    title.description = old_title.description
    title.z_scale = old_title.z_scale
    title.shadowsize = old_title.shadowsize
    title.shadowamount = old_title.shadowamount
    title.shadowsoft = old_title.shadowsoft
    title.shadowx = old_title.shadowx
    title.shadowy = old_title.shadowy
    title.lightscalex = old_title.lightscalex
    title.lightscaley = old_title.lightscaley
    title.lightx = old_title.lightx
    title.lighty = old_title.lighty
    title.lightrot = old_title.lightrot
    title.length = old_title.length
    title.objects.clear()
    for oldobject in old_title.objects:
        newobject = title.objects.add()
        copy_object(oldobject, newobject)


def quicktitle_autoupdate(self=None, context=None):
    #Auto update function called when changing settings
    #will update a selected title if autoupdate is enabled, should only update objects that are needed
    quicktitle = titling_scene_selected()
    if quicktitle:
        preset = quicktitle.scene.quicktitler.current_quicktitle
        quicktitle.scene.quicktitler.current_edited = True
        if bpy.context.scene.quicktitler.autoupdate:
            quicktitle_update(quicktitle, preset)
    else:
        bpy.context.scene.quicktitler.current_edited = True


def quicktitle_autoupdate_all(self=None, context=None):
    #Auto update function
    #will update a selected title if autoupdate is enabled, will update all objects in the scene
    quicktitle = titling_scene_selected()
    if quicktitle:
        preset = quicktitle.scene.quicktitler.current_quicktitle
        quicktitle.scene.quicktitler.current_edited = True
        if bpy.context.scene.quicktitler.autoupdate:
            quicktitle_update(quicktitle, preset, update_all=True)
    else:
        bpy.context.scene.quicktitler.current_edited = True


def isimageloaded(filepath):
    #Function to check if an image is already loaded
    for image in bpy.data.images:
        if image.filepath == filepath:
            return image
    return None


def istexture(image):
    #Function to check if a texture with a specific image exists
    for texture in bpy.data.textures:
        if hasattr(texture, 'image'):
            if texture.image == image:
                return texture
    return False


def iscorrecttype(title_object, object_type):
    #Function to test if an object is the correct blender type for what the script thinks it is
    if object_type == 'TEXT' and title_object.type == 'FONT':
        return True
    if (object_type == 'BOX' and title_object.type == 'CURVE') or (object_type == 'CIRCLE' and title_object.type == 'CURVE'):
        return True
    if object_type == 'IMAGE' and title_object.type == 'MESH':
        return True
    return False


def quicktitle_create(quicktitle=False):
    #Function to create QuickTitle scenes and sequences
    scene = bpy.context.scene
    if not quicktitle:
        quicktitle = scene.quicktitler.current_quicktitle

    #Basic scene setup
    bpy.ops.scene.new(type='EMPTY')
    title_scene = bpy.context.scene
    title_scene.frame_start = 1
    title_scene.frame_end = quicktitle.length
    title_scene.render.film_transparent = True
    title_scene.render.image_settings.file_format = 'PNG'
    title_scene.render.image_settings.color_mode = 'RGBA'

    #setup eevee
    title_scene.render.engine = 'BLENDER_EEVEE'
    title_scene.eevee.use_soft_shadows = True
    title_scene.eevee.use_ssr = True
    title_scene.eevee.use_ssr_refraction = True
    title_scene.eevee.shadow_cube_size = '1024'
    title_scene.eevee.shadow_cascade_size = '512'
    title_scene.eevee.taa_render_samples = 32

    copy_title_preset(quicktitle, title_scene.quicktitler.current_quicktitle)
    quicktitle_preset = title_scene.quicktitler.current_quicktitle
    if quicktitle.name:
        name = "QuickTitle: "+quicktitle.name
    else:
        name = "QuickTitle"
    title_scene.name = name

    bpy.ops.object.empty_add(type='PLAIN_AXES', location=(0, 0, 0))
    lampcenter = bpy.context.active_object
    basename = 'QuickTitlerLampCenter'
    if basename in bpy.data.objects:
        name = 'QuickTitlerLampCenter.001'
        index = 1
        while name in bpy.data.objects:
            index = index+1
            name = basename+str(index).zfill(3)
    else:
        name = basename
    lampcenter.name = name
    quicktitle_preset.lampcenter_internal_name = lampcenter.name

    #Camera setup
    bpy.ops.object.camera_add()
    camera = bpy.context.active_object
    title_scene.camera = camera
    camera.location = (0, 0, 2.17)
    camera.name = "QuickTitlerCamera"
    camera.data.lens = 39.2

    #Basic lamps setup
    lamp_energy = 50
    bpy.ops.object.light_add(location=(-1.1, -.6, .5))
    lamp1 = bpy.context.active_object
    lamp1.data.energy = lamp_energy
    lamp1.data.use_shadow = False
    lamp1.parent = lampcenter
    bpy.ops.object.light_add(location=(1.1, -.6, .5))
    lamp2 = bpy.context.active_object
    lamp2.data.energy = lamp_energy
    lamp2.data.use_shadow = False
    lamp2.parent = lampcenter
    bpy.ops.object.light_add(location=(-1.1, .6, .5))
    lamp3 = bpy.context.active_object
    lamp3.data.energy = lamp_energy
    lamp3.data.use_shadow = False
    lamp3.parent = lampcenter
    bpy.ops.object.light_add(location=(1.1, .6, .5))
    lamp4 = bpy.context.active_object
    lamp4.data.energy = lamp_energy
    lamp4.data.use_shadow = False
    lamp4.parent = lampcenter

    #Shadow lamp setup
    bpy.ops.object.light_add(type='SPOT', location=(0, 0, 1))
    shadow_lamp = bpy.context.active_object
    basename = 'QuickTitlerLamp'
    if basename in bpy.data.objects:
        name = 'QuickTitlerLamp.001'
        index = 1
        while name in bpy.data.objects:
            index = index+1
            name = basename+str(index).zfill(3)
    else:
        name = basename
    shadow_lamp.name = name
    quicktitle_preset.shadowlamp_internal_name = shadow_lamp.name
    #shadow_lamp.parent = lampcenter
    shadow_lamp.data.specular_factor = 0
    shadow_lamp.data.shadow_soft_size = 0
    shadow_lamp.data.falloff_type = 'CONSTANT'
    shadow_lamp.data.use_shadow = True
    shadow_lamp.data.shadow_buffer_bias = 0.1
    shadow_lamp.data.shadow_buffer_samples = 4
    shadow_lamp.data.shadow_buffer_clip_start = 0.01
    shadow_lamp.data.spot_size = 2.6
    shadow_lamp.data.use_square = True

    bpy.ops.object.light_add(type='SPOT', location=(0, 0, 1))
    shadow_lamp = bpy.context.active_object
    basename = 'QuickTitlerLampInverse'
    if basename in bpy.data.objects:
        name = 'QuickTitlerLampInverse.001'
        index = 1
        while name in bpy.data.objects:
            index = index+1
            name = basename+str(index).zfill(3)
    else:
        name = basename
    shadow_lamp.name = name
    quicktitle_preset.shadowlamp_inverse_internal_name = shadow_lamp.name
    #shadow_lamp.parent = lampcenter
    shadow_lamp.data.specular_factor = 0
    shadow_lamp.data.shadow_soft_size = 0
    shadow_lamp.data.falloff_type = 'CONSTANT'
    shadow_lamp.data.use_shadow = False
    shadow_lamp.data.spot_size = 2.6
    shadow_lamp.data.use_square = True

    #Add scene to sequencer
    bpy.context.window.scene = scene
    bpy.ops.sequencer.scene_strip_add(frame_start=scene.frame_current, scene=title_scene.name)
    sequence = bpy.context.scene.sequence_editor.active_strip
    sequence.name = name
    sequence.blend_type = 'ALPHA_OVER'


def create_object(scene, object_type, name):
    scene.cursor.location = (0.0, 0.0, 0.0)
    if object_type == 'IMAGE':
        #create image
        mesh = bpy.data.meshes.new(name=name)
        verts = [(-1, 1, 0.0), (1, 1, 0.0), (1, -1, 0.0), (-1, -1, 0.0)]
        faces = [(3, 2, 1, 0)]
        mesh.from_pydata(verts, [], faces)
        uvmap = mesh.uv_layers.new()
        title_object = bpy.data.objects.new(name=name, object_data=mesh)
        scene.collection.objects.link(title_object)

    elif object_type == 'CIRCLE':
        #create circle
        curve = bpy.data.curves.new(name=name, type='CURVE')
        curve.dimensions = '2D'
        curve.fill_mode = 'BOTH'
        curve.resolution_u = 12
        curve.twist_mode = 'MINIMUM'
        spline = curve.splines.new('NURBS')
        spline.points.add(7)
        w = 0.354
        c = 0.707
        spline.points[0].co = (-c, c, 0, w)
        spline.points[1].co = (0, 1, 0, w)
        spline.points[2].co = (c, c, 0, w)
        spline.points[3].co = (1, 0, 0, w)
        spline.points[4].co = (c, -c, 0, w)
        spline.points[5].co = (0, -1, 0, w)
        spline.points[6].co = (-c, -c, 0, w)
        spline.points[7].co = (-1, 0, 0, w)

        spline.use_cyclic_u = True
        spline.resolution_u = 12
        spline.order_u = 4
        title_object = bpy.data.objects.new(name=name, object_data=curve)
        scene.collection.objects.link(title_object)

    elif object_type == 'BOX':
        #create box
        curve = bpy.data.curves.new(name=name, type='CURVE')
        curve.dimensions = '2D'
        curve.fill_mode = 'BOTH'
        curve.resolution_u = 1
        curve.twist_mode = 'MINIMUM'
        spline = curve.splines.new('NURBS')
        spline.points.add(3)
        w = 1
        spline.points[0].co = (-1, 1, 0, w)
        spline.points[1].co = (1, 1, 0, w)
        spline.points[2].co = (1, -1, 0, w)
        spline.points[3].co = (-1, -1, 0, w)
        spline.use_cyclic_u = True
        spline.resolution_u = 1
        spline.order_u = 2
        title_object = bpy.data.objects.new(name=name, object_data=curve)
        scene.collection.objects.link(title_object)

    else:
        #create text
        text = bpy.data.curves.new(name=name, type='FONT')
        text.size = 0.1
        title_object = bpy.data.objects.new(name=name, object_data=text)
        scene.collection.objects.link(title_object)

    return title_object


def set_animations(title_object, object_preset, material, scene, z_offset, pos_multiplier, shaders, parent=None):
    #look for and clear animations that are no longer set

    #clear old animations
    animation_types = []
    for animation in object_preset.animations:
        animation_types.append(animation.variable)
    if material:
        transparency_factor = shaders[4]
        if material.node_tree.animation_data:
            if material.node_tree.animation_data.action:
                if material.node_tree.animation_data.action.fcurves:
                    fcurves = material.node_tree.animation_data.action.fcurves
                    for curve in fcurves:
                        if curve.data_path == 'nodes["'+transparency_factor.name+'"].inputs[1].default_value':
                            if 'Alpha' not in animation_types:
                                fcurves.remove(curve)
    if title_object.animation_data:
        if title_object.animation_data.action:
            if title_object.animation_data.action.fcurves:
                fcurves = title_object.animation_data.action.fcurves
                for curve in fcurves:
                    if curve.data_path == 'location':
                        if curve.array_index == 0:
                            if 'X Slide' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 1:
                            if 'Y Slide' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 2:
                            if 'Z Slide' not in animation_types:
                                fcurves.remove(curve)
                    elif curve.data_path == 'rotation_euler':
                        if curve.array_index == 0:
                            if 'X Rotate' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 1:
                            if 'Y Rotate' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 2:
                            if 'Z Rotate' not in animation_types:
                                fcurves.remove(curve)
                    elif curve.data_path == 'scale':
                        if curve.array_index == 0:
                            if 'Width' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 1:
                            if 'Height' not in animation_types:
                                fcurves.remove(curve)
                        elif curve.array_index == 2:
                            if 'Depth' not in animation_types:
                                fcurves.remove(curve)

    #if animations are on this object, update them
    start_frame = scene.frame_start
    end_frame = scene.frame_end
    for animation_preset in object_preset.animations:
        if animation_preset.variable == 'Alpha':
            if not material:
                continue
            if not material.node_tree.animation_data:
                animation = material.node_tree.animation_data_create()
            else:
                animation = material.node_tree.animation_data
        else:
            if not title_object.animation_data:
                animation = title_object.animation_data_create()
            else:
                animation = title_object.animation_data
        if not animation.action:
            action = bpy.data.actions.new(title_object.name)
            animation.action = action
        else:
            action = animation.action
        fcurves = action.fcurves

        in_amount = animation_preset.in_amount
        out_amount = animation_preset.out_amount
        variable = animation_preset.variable
        fcurve, value = get_fcurve(fcurves, variable, shaders, material=material, on_object=title_object if not parent else parent)
        offsetvalue = value
        scalevalue = 1
        if 'Rotate' in variable:
            in_amount = in_amount / 180 * pi
            out_amount = out_amount / 180 * pi
        if 'Slide' in variable:
            scalevalue = 1 + (z_offset * .457)
            offsetvalue = offsetvalue / pos_multiplier
            if parent:
                offsetvalue = offsetvalue - .001
                value = value - .001
        if variable == 'Alpha':
            offsetvalue = 0
        if variable == 'Width' or variable == 'Height' or variable == 'Depth':
            offsetvalue = 0
        if fcurve:
            points = []
            if animation_preset.animate_in:
                points.append((start_frame + animation_preset.in_offset, (offsetvalue + in_amount) * scalevalue))
                points.append((start_frame + animation_preset.in_offset + animation_preset.in_length, value))
            else:
                points.append((start_frame, value))
            if animation_preset.animate_out:
                points.append((end_frame + animation_preset.out_offset - animation_preset.out_length, value))
                points.append((end_frame + animation_preset.out_offset, (offsetvalue + out_amount) * scalevalue))
            else:
                points.append((end_frame, value))
            clear_keyframes(fcurve)
            for index, point in enumerate(points):
                fcurve.keyframe_points.add(count=1)
                fcurve.keyframe_points[index].co = point

            #Set cyclic animations
            if animation_preset.cycle_type != 'NONE':
                cycle_type = animation_preset.cycle_type
                x_scale = animation_preset.cycle_x_scale
                y_scale = animation_preset.cycle_y_scale
                offset = animation_preset.cycle_offset
                if len(fcurve.modifiers) > 0:
                    for modifier in reversed(fcurve.modifiers):
                        fcurve.modifiers.remove(modifier)
                if cycle_type == 'RANDOM':
                    modifier = fcurve.modifiers.new(type='NOISE')
                    modifier.scale = x_scale * 10
                    modifier.strength = y_scale
                    modifier.offset = offset
                if cycle_type == 'SINE':
                    modifier = fcurve.modifiers.new(type='FNGENERATOR')
                    modifier.function_type = 'SIN'
                    modifier.use_additive = True
                    modifier.amplitude = y_scale / 4
                    if x_scale > 0:
                        modifier.phase_multiplier = 1 / x_scale / 10
                    else:
                        modifier.phase_multiplier = 0
                    modifier.phase_offset = -offset
                if cycle_type == 'TANGENT':
                    modifier = fcurve.modifiers.new(type='FNGENERATOR')
                    modifier.function_type = 'TAN'
                    modifier.use_additive = True
                    modifier.amplitude = y_scale / 20
                    if x_scale > 0:
                        modifier.phase_multiplier = 1 / x_scale / 10
                    else:
                        modifier.phase_multiplier = 0
                    modifier.phase_offset = -offset
                modifier.use_restricted_range = True
                if animation_preset.animate_in:
                    modifier.frame_start = start_frame + animation_preset.in_offset
                    modifier.blend_in = animation_preset.in_length
                else:
                    modifier.frame_start = start_frame
                    modifier.blend_in = 0
                if animation_preset.animate_out:
                    modifier.frame_end = end_frame + animation_preset.out_offset
                    modifier.blend_out = animation_preset.out_length
                else:
                    modifier.frame_end = end_frame
                    modifier.blend_out = 0
            fcurve.update()


def setup_object(title_object, object_preset, scale_multiplier):
    #settings for different title_object types
    #shaders = [shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node]
    shear = object_preset.shear
    if object_preset.type == 'IMAGE':
        image = None
        #set up image type
        if object_preset.set_material:
            texture = None
        else:
            texture = object_preset.texture
        if texture:
            #image texture is set
            path = os.path.abspath(bpy.path.abspath(texture))
            image = find_load_image(path)
            if image:
                #set plane size based on image aspect ratio
                ix = 1
                iy = (image.size[1] / image.size[0])
                title_object.data.vertices[0].co = (-ix + shear, iy, 0)
                title_object.data.vertices[1].co = (ix + shear, iy, 0)
                title_object.data.vertices[2].co = (ix - shear, -iy, 0)
                title_object.data.vertices[3].co = (-ix - shear, -iy, 0)
        if image is None:
            #image texture is not set or has been unset, remove it from material if needed and set plane back to original dimensions
            title_object.data.vertices[0].co = (-1 + shear, 1, 0)
            title_object.data.vertices[1].co = (1 + shear, 1, 0)
            title_object.data.vertices[2].co = (1 - shear, -1, 0)
            title_object.data.vertices[3].co = (-1 - shear, -1, 0)

    if object_preset.type in ['CIRCLE', 'BOX', 'TEXT']:
        #set up the circle, box and text settings
        title_object.data.extrude = object_preset.extrude / 10.0
        title_object.data.bevel_depth = object_preset.bevel / 10.0
        title_object.data.bevel_resolution = object_preset.bevel_resolution

    if object_preset.type == 'BOX':
        #set up the box settings
        title_object.data.splines[0].points[0].co[0] = -1 + object_preset.shear
        title_object.data.splines[0].points[1].co[0] = 1 + object_preset.shear
        title_object.data.splines[0].points[2].co[0] = 1 - object_preset.shear
        title_object.data.splines[0].points[3].co[0] = -1 - object_preset.shear

    if object_preset.type == 'CIRCLE':
        c = 0.707
        s_shear = shear * c
        title_object.data.splines[0].points[0].co[0] = -c + s_shear
        title_object.data.splines[0].points[1].co[0] = shear
        title_object.data.splines[0].points[2].co[0] = c + s_shear
        title_object.data.splines[0].points[3].co[0] = 1
        title_object.data.splines[0].points[4].co[0] = c - s_shear
        title_object.data.splines[0].points[5].co[0] = -shear
        title_object.data.splines[0].points[6].co[0] = -c - s_shear
        title_object.data.splines[0].points[7].co[0] = -1

    if object_preset.type == 'TEXT':
        #set up the text settings
        text_formatted = object_preset.text.encode().decode('unicode_escape').encode('latin1').decode('utf-8')
        title_object.data.body = text_formatted
        title_object.data.align_x = object_preset.align
        title_object.data.shear = object_preset.shear
        if object_preset.font in bpy.data.fonts:
            title_object.data.font = bpy.data.fonts[object_preset.font]
        if object_preset.word_wrap:
            x_scale = title_object.scale[0]
            if x_scale == 0:
                x_scale = 0.001
            box_size = (1.0/x_scale)*scale_multiplier*2
            title_object.data.text_boxes[0].width = box_size * object_preset.wrap_width
            title_object.data.text_boxes[0].x = -(box_size / 2) * object_preset.wrap_width
        else:
            title_object.data.text_boxes[0].width = 0
            title_object.data.text_boxes[0].x = 0


def input_name(node, name):
    for socket in node.inputs:
        if socket.name == name:
            return socket
    return None


def get_output_node(material):
    #for a material, returns the socket for the material output node, while ensuring that such node exists
    material.use_nodes = True
    output_node = None
    for check_node in material.node_tree.nodes:
        #find the output node
        if check_node.type == 'OUTPUT_MATERIAL':
            output_node = check_node
            break
    return output_node


def clear_material(material):
    for node in material.node_tree.nodes:
        material.node_tree.nodes.remove(node)


def connect_material_texture(material, shaders, connect=True):
    shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node = shaders
    tree = material.node_tree
    if connect:
        tree.links.new(image_node.outputs[0], shader.inputs[0])
    else:
        for link in tree.links:
            if link.from_node == image_node and link.to_node == shader:
                tree.links.remove(link)
                break


def connect_texture_coords(material, shaders, mode='UV'):
    shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node = shaders
    tree = material.node_tree

    #delete old links
    for link in reversed(tree.links):
        if link.from_node == texture_map_node and link.to_node == image_node:
            tree.links.remove(link)

    #add new link
    if mode == 'UV':
        tree.links.new(texture_map_node.outputs['UV'], image_node.inputs[0])
    else:
        tree.links.new(texture_map_node.outputs['Window'], image_node.inputs[0])


def setup_material(material, use_shadeless, mat_type):
    #recreates a material
    clear_material(material)
    tree = material.node_tree
    nodes = tree.nodes

    #create nodes
    image_node = None
    alpha_image_node = None
    alpha_mix_node = None
    texture_map_node = None
    output_node = nodes.new('ShaderNodeOutputMaterial')
    mix_shader = nodes.new('ShaderNodeMixShader')
    transparency_factor = nodes.new('ShaderNodeMath')
    transparent_shader = nodes.new('ShaderNodeBsdfTransparent')
    if use_shadeless:
        shader = nodes.new('ShaderNodeEmission')
    else:
        shader = nodes.new('ShaderNodeBsdfPrincipled')
    if mat_type == 'IMAGE':
        #setup image material nodes
        image_node = nodes.new('ShaderNodeTexImage')
        alpha_image_node = nodes.new('ShaderNodeTexImage')
        alpha_mix_node = nodes.new('ShaderNodeMixRGB')
        alpha_mix_node.inputs[0].default_value = 0
        texture_map_node = nodes.new('ShaderNodeTexCoord')
        tree.links.new(alpha_mix_node.outputs[0], transparency_factor.inputs[0])
        #tree.links.new(image_node.outputs[0], shader.inputs[0])
        tree.links.new(image_node.outputs[1], alpha_mix_node.inputs[1])
        tree.links.new(alpha_image_node.outputs[0], alpha_mix_node.inputs[2])

    #connect nodes
    tree.links.new(mix_shader.outputs[0], output_node.inputs['Surface'])
    tree.links.new(transparent_shader.outputs[0], mix_shader.inputs[1])
    tree.links.new(shader.outputs[0], mix_shader.inputs[2])
    tree.links.new(transparency_factor.outputs[0], mix_shader.inputs[0])

    #set up basic values on nodes
    transparent_shader.inputs[0].default_value[3] = 0
    transparency_factor.inputs[0].default_value = 1
    transparency_factor.inputs[1].default_value = 1
    transparency_factor.operation = 'MULTIPLY'
    transparency_factor.use_clamp = True
    mix_shader.inputs[0].default_value = 1
    return [shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node]


def get_connected_node(node, socket_name):
    socket = node.inputs[socket_name]
    if len(socket.links) > 0:
        return socket.links[0].from_node
    return None


def check_material(material, mat_type):
    #checks if the material node setup is correct for the type
    output_node = get_output_node(material)
    if not output_node:
        return None
    mix_shader = get_connected_node(output_node, 'Surface')
    if not mix_shader:
        return None
    if mix_shader.type != 'MIX_SHADER':
        return None
    transparency_factor = get_connected_node(mix_shader, 0)
    if not transparency_factor:
        return None
    if transparency_factor.type != 'MATH':
        return None
    transparent_shader = get_connected_node(mix_shader, 1)
    if not transparent_shader:
        return None
    if transparent_shader.type != 'BSDF_TRANSPARENT':
        return None
    shader = get_connected_node(mix_shader, 2)
    if not shader:
        return None
    if mat_type == 'IMAGE':
        alpha_mix_node = get_connected_node(transparency_factor, 0)
        if not alpha_mix_node:
            return None
        if alpha_mix_node.type != 'MIX_RGB':
            return None
        image_node = get_connected_node(alpha_mix_node, 1)
        if not image_node:
            return None
        if image_node.type != 'TEX_IMAGE':
            return None
        alpha_image_node = get_connected_node(alpha_mix_node, 2)
        if not alpha_image_node:
            return None
        if alpha_image_node.type != 'TEX_IMAGE':
            return None
        texture_map_node = get_connected_node(image_node, 0)
        if not texture_map_node:
            return None
        if texture_map_node.type != 'TEX_COORD':
            return None
    else:
        image_node = None
        alpha_image_node = None
        alpha_mix_node = None
        texture_map_node = None
    return [shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node]


def check_shader(material, shaders, use_shadeless):
    #checks the output shader type and ensures it is correct

    shader, transparent_shader, mix_shader, output_node, transparency_factor, image_node, alpha_image_node, alpha_mix_node, texture_map_node = shaders
    if use_shadeless:
        if shader.type != 'EMISSION':
            material.node_tree.nodes.remove(shader)
            shader = material.node_tree.nodes.new('ShaderNodeEmission')
            material.node_tree.links.new(shader.outputs[0], mix_shader.inputs[2])
    else:
        if shader.type != 'BSDF_PRINCIPLED':
            material.node_tree.nodes.remove(shader)
            shader = material.node_tree.nodes.new('ShaderNodeBsdfPrincipled')
            material.node_tree.links.new(shader.outputs[0], mix_shader.inputs[2])
    shaders[0] = shader
    return shaders


def get_shaders(material, use_shadeless=False, mat_type=None):
    #given a material, returns the shader node of the correct type, while ensuring it exists and is properly connected

    shaders = check_material(material, mat_type)
    if not shaders:
        shaders = setup_material(material, use_shadeless, mat_type)
    shaders = check_shader(material, shaders, use_shadeless)
    return shaders


def update_material(object_preset, material):
    shaders = get_shaders(material, use_shadeless=object_preset.use_shadeless, mat_type=object_preset.type)
    shader = shaders[0]
    transparency_factor = shaders[4]
    socket = transparency_factor.inputs[1]
    socket.default_value = object_preset.alpha

    if shader.type == 'BSDF_PRINCIPLED':
        socket = input_name(shader, 'Specular')
        socket.default_value = object_preset.specular_intensity
        socket = input_name(shader, 'Metallic')
        socket.default_value = object_preset.metallic
        socket = input_name(shader, 'Transmission')
        socket.default_value = object_preset.transmission
        socket = input_name(shader, 'Base Color')
        socket.default_value[0] = object_preset.diffuse_color[0]
        socket.default_value[1] = object_preset.diffuse_color[1]
        socket.default_value[2] = object_preset.diffuse_color[2]
        socket = input_name(shader, 'Roughness')
        socket.default_value = object_preset.roughness
        socket = input_name(shader, 'IOR')
        socket.default_value = object_preset.index_of_refraction

    else:
        socket = input_name(shader, 'Color')
        socket.default_value[0] = object_preset.diffuse_color[0]
        socket.default_value[1] = object_preset.diffuse_color[1]
        socket.default_value[2] = object_preset.diffuse_color[2]
        socket = input_name(shader, 'Strength')
        socket.default_value = 1

    material.use_screen_refraction = True
    material.blend_method = 'BLEND'
    material.show_transparent_back = False

    if object_preset.cast_shadows:
        material.shadow_method = 'CLIP'

    else:
        material.shadow_method = 'NONE'

    if object_preset.type == 'IMAGE':
        #set up image type
        image_node = shaders[5]
        alpha_image_node = shaders[6]
        alpha_mix_node = shaders[7]
        if object_preset.texture:
            #image texture is set
            connect_material_texture(material, shaders, connect=True)
            if object_preset.window_mapping:
                map_mode = 'Window'
            else:
                map_mode = 'UV'
            connect_texture_coords(material, shaders, mode=map_mode)
            path = os.path.abspath(bpy.path.abspath(object_preset.texture))
            extension = os.path.splitext(path)[1].lower()
            if extension in bpy.path.extensions_movie:
                #The file is a known video file type, load it
                video = True
            else:
                video = False
            if os.path.isfile(path) and (extension in bpy.path.extensions_image or video):
                #The file is a known file type, load it
                image = find_load_image(path)
                image.update()
                image_node.image = image
                if video:
                    #set video defaults
                    object_preset.frame_length = image.frame_duration
                    object_preset.frame_offset = 0
                    image_node.image_user.frame_duration = image.frame_duration
                    image_node.image_user.frame_start = 1
                    image_node.image_user.frame_offset = 0
                    image_node.image_user.use_cyclic = object_preset.loop
                    image_node.image_user.use_auto_refresh = True

        else:
            #image texture is not set or has been unset, remove it from material if needed and set plane back to original dimensions
            connect_material_texture(material, shaders, connect=False)
            image_node.image = None

        alpha_mix_node.inputs[0].default_value = 0

        if object_preset.alpha_texture:
            #alpha texture is set
            path = os.path.abspath(bpy.path.abspath(object_preset.alpha_texture))
            extension = os.path.splitext(path)[1].lower()
            if extension in bpy.path.extensions_movie:
                #The file is a known video file type, load it
                video = True
            else:
                video = False
            if os.path.isfile(path) and (extension in bpy.path.extensions_image or video):
                #The file is a known file type, load it
                image = find_load_image(path)
                image.update()
                alpha_image_node.image = image
                alpha_mix_node.inputs[0].default_value = 1
                if video:
                    #set video defaults
                    object_preset.frame_length = image.frame_duration
                    object_preset.frame_offset = 0
                    alpha_image_node.image_user.frame_duration = image.frame_duration
                    alpha_image_node.image_user.frame_start = 1
                    alpha_image_node.image_user.frame_offset = 0
                    alpha_image_node.image_user.use_cyclic = object_preset.loop
                    alpha_image_node.image_user.use_auto_refresh = True
        else:
            #alpha texture is not set or has been unset, remove it from material
            alpha_image_node.image = None
    return shaders


def set_material(title_object, material):
    title_object.active_material = material
    for material_slot in title_object.material_slots:
        material_slot.link = 'OBJECT'
    if len(title_object.material_slots) >= 1:
        title_object.material_slots[0].material = material


def get_material(title_object):
    if len(title_object.material_slots) >= 1:
        return title_object.material_slots[0].material
    return None


def quicktitle_update(sequence, quicktitle, update_all=False):
    #Function to update a QuickTitle sequence
    scene = sequence.scene
    oldscene = bpy.context.window.scene
    bpy.context.window.scene = scene
    scenename = "QuickTitle: "+quicktitle.name

    #Update scene length, if changed, update all objects
    if scene.frame_end != quicktitle.length:
        scene.frame_end = quicktitle.length
        update_all = True

    #Fix sequence length if needed
    if sequence.frame_offset_start != 0:
        sequence.frame_start = sequence.frame_start + sequence.frame_offset_start
        sequence.frame_offset_start = 0
    if sequence.frame_offset_end != 0:
        sequence.frame_offset_end = 0

    #attempt to find and update the shadow lamp
    if quicktitle.shadowlamp_internal_name in scene.objects and quicktitle.shadowlamp_inverse_internal_name in scene.objects:
        shadow_lamp = scene.objects[quicktitle.shadowlamp_internal_name]
        shadow_lamp_inverse = scene.objects[quicktitle.shadowlamp_inverse_internal_name]
        softshadow = quicktitle.shadowsoft * .25
        shadow_multiplier = 120
        shadow_lamp.data.energy = quicktitle.shadowamount * shadow_multiplier
        shadow_lamp_inverse.data.energy = -(quicktitle.shadowamount * shadow_multiplier)
        shadow_lamp.data.shadow_soft_size = softshadow
        shadow_lamp_inverse.data.shadow_soft_size = softshadow
        shadow_lamp.location = (quicktitle.shadowx, quicktitle.shadowy, quicktitle.shadowsize)
        shadow_lamp_inverse.location = (quicktitle.shadowx, quicktitle.shadowy, quicktitle.shadowsize)
        if quicktitle.shadowamount > 0:
            shadow_lamp.data.use_shadow = True
        else:
            shadow_lamp.data.use_shadow = False
    else:
        #shadow_lamp = None
        print('Selected Title Scene Is Incomplete: Missing Shadow Lamp')

    #attempt to update the lamp center
    if quicktitle.lampcenter_internal_name in scene.objects:
        lampcenter = scene.objects[quicktitle.lampcenter_internal_name]
        lampcenter.scale[0] = quicktitle.lightscalex
        lampcenter.scale[1] = quicktitle.lightscaley
        lampcenter.location = (quicktitle.lightx, quicktitle.lighty, 0)
        lampcenter.rotation_euler[2] = -quicktitle.lightrot/180.0*pi
    else:
        print('Selected Title Scene Is Incomplete: missing Lamp Center')

    #update individual scene objects
    for object_layer, object_preset in enumerate(quicktitle.objects):
        if object_layer == quicktitle.selected_object:
            selected_object = True
        else:
            selected_object = False

        #get or create object name used for internal naming
        if object_preset.name:
            name = object_preset.type+':'+object_preset.name
        else:
            name = object_preset.type

        #determine if object needs to be created
        if object_preset.internal_name not in scene.objects:
            #object is not found or doesnt exist
            title_object = False
        else:
            #object exists
            title_object = scene.objects[object_preset.internal_name]
            if not iscorrecttype(title_object, object_preset.type):
                #title_object exists but its not the correct type, need to recreate title_object
                title_object = False
            else:
                if object_preset.type == 'IMAGE':
                    if len(title_object.data.vertices) != 4:
                        title_object = False
                if object_preset.type == 'BOX':
                    if len(title_object.data.splines[0].points) != 4:
                        title_object = False
                if object_preset.type == 'CIRCLE':
                    if len(title_object.data.splines[0].points) != 8:
                        title_object = False
        if not title_object:
            #create title_object
            title_object = create_object(scene, object_preset.type, name)

            object_preset.internal_name = title_object.name
            created_object = True

        else:
            created_object = False

        #General title_object settings
        offset_multiplier = 0.462
        z_index = object_layer
        z_scale = quicktitle.z_scale / 10.0
        scale_multiplier = (z_scale * (z_index * offset_multiplier)) + 1
        pos_multiplier = 1 + (z_scale * (z_index * offset_multiplier))
        z_offset = z_index * z_scale

        #detailed settings need to be updated for this object
        if selected_object or created_object or update_all:
            material = None
            shaders = []
            title_object.location = (pos_multiplier * object_preset.x, pos_multiplier * object_preset.y, object_preset.z - z_offset)
            title_object.scale = (scale_multiplier * object_preset.scale * object_preset.width, scale_multiplier * object_preset.scale * object_preset.height, scale_multiplier * object_preset.scale)
            title_object.rotation_euler = (object_preset.rot_x/180.0*pi, object_preset.rot_y/180.0*pi, -object_preset.rot_z/180.0*pi)

            #Material settings
            if object_preset.set_material:
                #material is set manually
                if object_preset.set_material_name == 'No Preset':
                    #material is unset, disable manual setting
                    pass
                    #object_preset.set_material = False

                else:
                    if object_preset.set_material_name in bpy.data.materials:
                        #material exists
                        material = bpy.data.materials[object_preset.set_material_name]
                        set_material(title_object, material)
                        material = None

                    else:
                        #material doesnt exist, create it
                        material = bpy.data.materials.new(object_preset.set_material_name)
                        shaders = update_material(object_preset, material)

            if not object_preset.set_material:
                #material is determined automatically
                material = get_material(title_object)
                if material:
                    if material.name != object_preset.material:
                        set_material(title_object, None)
                        material = None
                if not material:
                    name = 'QuickTitler '+object_preset.type+' Material'
                    material = bpy.data.materials.new(name)
                    object_preset.material = material.name
                    set_material(title_object, material)

                shaders = update_material(object_preset, material)

            setup_object(title_object, object_preset, scale_multiplier)

            set_animations(title_object, object_preset, material, scene, z_offset, pos_multiplier, shaders)

            update_bounds(title_object, object_preset, scene, scale_multiplier, pos_multiplier)

            outline_object_name = title_object.name+'outline'
            outline_object = None
            if outline_object_name in scene.objects:
                outline_object = scene.objects[outline_object_name]
                if not object_preset.outline:
                    #delete outline object
                    scene.collection.objects.unlink(outline_object)
                    bpy.data.objects.remove(outline_object, do_unlink=True)
                    outline_object = None
            else:
                if object_preset.outline:
                    #create outline object
                    outline_object = create_object(scene, object_preset.type, outline_object_name)

            if outline_object:
                #set up material
                if outline_object_name in bpy.data.materials:
                    material = bpy.data.materials[outline_object_name]
                else:
                    material = bpy.data.materials.new(outline_object_name)
                set_material(outline_object, material)

                shaders = get_shaders(material, use_shadeless=True)
                shader = shaders[0]
                transparency_factor = shaders[4]
                socket = transparency_factor.inputs[1]
                socket.default_value = object_preset.outline_alpha

                socket = input_name(shader, 'Color')
                socket.default_value[0] = object_preset.outline_diffuse_color[0]
                socket.default_value[1] = object_preset.outline_diffuse_color[1]
                socket.default_value[2] = object_preset.outline_diffuse_color[2]
                socket = input_name(shader, 'Strength')
                socket.default_value = 1

                material.blend_method = 'BLEND'
                if object_preset.cast_shadows:
                    material.shadow_method = 'CLIP'
                else:
                    material.shadow_method = 'NONE'

                #adjust object
                outline_object.location = (pos_multiplier * object_preset.x, pos_multiplier * object_preset.y, object_preset.z - z_offset - .001)
                outline_object.scale = (scale_multiplier * object_preset.scale * object_preset.width, scale_multiplier * object_preset.scale * object_preset.height, object_preset.scale)
                outline_object.rotation_euler = (object_preset.rot_x / 180.0 * pi, object_preset.rot_y / 180.0 * pi, -object_preset.rot_z / 180.0 * pi)
                setup_object(outline_object, object_preset, scale_multiplier)
                set_animations(outline_object, object_preset, material, scene, z_offset, pos_multiplier, shaders, parent=title_object)
                #outline_object.data.offset = object_preset.outline_size / 100
                outline_object.data.extrude = 0
                outline_object.data.bevel_depth = object_preset.outline_size / 100
                outline_object.scale[2] = 0
                outline_object.data.fill_mode = 'FRONT'

    #update scene and sequence
    scene.name = scenename
    sequence.name = scenename
    bpy.context.window.scene = oldscene
    scene.update_tag()
    bpy.ops.sequencer.reload(adjust_length=True)
    bpy.ops.sequencer.refresh_all()


def get_fcurve(fcurves, variable, shaders, material=None, on_object=None):
    #find or create and return an fcurve matching the given internal script variable name
    fcurve = None
    value = None
    if variable == 'Alpha':
        if shaders:
            transparency_factor = shaders[4]
            data_path = 'nodes["'+transparency_factor.name+'"].inputs[1].default_value'
            if transparency_factor:
                value = transparency_factor.inputs[1].default_value
            fcurve = fcurves.find(data_path)
            if not fcurve:
                fcurve = fcurves.new(data_path)
    elif variable == 'X Slide':
        data_path = 'location'
        if on_object:
            value = on_object.location[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=0)
    elif variable == 'Y Slide':
        data_path = 'location'
        if on_object:
            value = on_object.location[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=1)
    elif variable == 'Z Slide':
        data_path = 'location'
        if on_object:
            value = on_object.location[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=2)
    elif variable == 'X Rotate':
        data_path = 'rotation_euler'
        if on_object:
            value = on_object.rotation_euler[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=0)
    elif variable == 'Y Rotate':
        data_path = 'rotation_euler'
        if on_object:
            value = on_object.rotation_euler[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=1)
    elif variable == 'Z Rotate':
        data_path = 'rotation_euler'
        if on_object:
            value = on_object.rotation_euler[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=2)
    elif variable == 'Width':
        data_path = 'scale'
        if on_object:
            value = on_object.scale[0]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 0:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=0)
    elif variable == 'Height':
        data_path = 'scale'
        if on_object:
            value = on_object.scale[1]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 1:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=1)
    elif variable == 'Depth':
        data_path = 'scale'
        if on_object:
            value = on_object.scale[2]
        for curve in fcurves:
            if curve.data_path == data_path and curve.array_index == 2:
                fcurve = curve
                break
        if not fcurve:
            fcurve = fcurves.new(data_path, index=2)
    return [fcurve, value]


def clear_keyframes(fcurve):
    #Removes all points on a curve
    index = len(fcurve.keyframe_points) - 1
    while index >= 0:
        fcurve.keyframe_points.remove(fcurve.keyframe_points[index], fast=True)
        index = index-1


def quicktitle_object_icon(object_type):
    #returns an icon name for a given internal object type
    if object_type == "TEXT":
        return "FONT_DATA"
    elif object_type == "BOX":
        return "MESH_PLANE"
    elif object_type == "CIRCLE":
        return "MESH_CIRCLE"
    elif object_type == "IMAGE":
        return "IMAGE_DATA"
    else:
        return "DOT"


def quicktitle_animation_icon(animation_type):
    #returns an icon name for a ganimation_typeiven internal animation type
    if animation_type == "Alpha":
        return "IMAGE_RGB_ALPHA"
    elif animation_type == "X Slide":
        return "EMPTY_ARROWS"
    elif animation_type == "Y Slide":
        return "EMPTY_ARROWS"
    elif animation_type == "Z Slide":
        return "EMPTY_ARROWS"
    elif animation_type == "X Rotate":
        return "NDOF_TURN"
    elif animation_type == "Y Rotate":
        return "NDOF_TURN"
    elif animation_type == "Z Rotate":
        return "NDOF_TURN"
    elif animation_type == "Width":
        return "FULLSCREEN_ENTER"
    elif animation_type == "Height":
        return "FULLSCREEN_ENTER"
    elif animation_type == "Depth":
        return "FULLSCREEN_ENTER"
    else:
        return "DOT"


class QuickTitleAnimation(bpy.types.PropertyGroup):
    #animation object stored in quicktitle objects
    variable: bpy.props.StringProperty(
        name="Animation Variable Name",
        default='Alpha')
    animate_in: bpy.props.BoolProperty(
        name="Animate Variable In",
        default=True,
        description="This will determine if this animation will change this variable from the beginning of the title.",
        update=quicktitle_autoupdate)
    animate_out: bpy.props.BoolProperty(
        name="Animate Variable Out",
        default=True,
        description="This will determine if this animation will change this variable at the end of the title.",
        update=quicktitle_autoupdate)
    in_length: bpy.props.IntProperty(
        name="Length Of In Animation",
        default=15,
        min=0,
        description="Length in frames of the animation applied to the beginning of the title.",
        update=quicktitle_autoupdate)
    out_length: bpy.props.IntProperty(
        name="Length Of Out Animation",
        default=15,
        min=0,
        description="Length in frames of the animation applied to the ending of the title.",
        update=quicktitle_autoupdate)
    in_offset: bpy.props.IntProperty(
        name="Frame Offset Of In Animation",
        default=0,
        description="Distance in frames the animation will be offset from the beginning of the title.  Positive values result in a delayed animation, negative values result in an animation beginning before the start of the title.",
        update=quicktitle_autoupdate)
    out_offset: bpy.props.IntProperty(
        name="Frame Offset Of Out Animation",
        default=0,
        description="Distance in frames the animation will be offset from the end of the title.  Positive values result in a delayed animation, negative values result in an animation beginning before the start of the title.",
        update=quicktitle_autoupdate)
    in_amount: bpy.props.FloatProperty(
        name="Amount Of In Animation",
        default=1,
        description="Beginning value of the starting animation.  This is a float with any value allowed, but depending on the variable being animated, some values will not make sense.",
        update=quicktitle_autoupdate)
    out_amount: bpy.props.FloatProperty(
        name="Amount Of Out Animation",
        default=1,
        description="Ending value of the end animation.  This is a float with any value allowed, but depending on the variable being animated, some values will not make sense.",
        update=quicktitle_autoupdate)
    cycle_x_scale: bpy.props.FloatProperty(
        name="X Scale",
        default=1,
        min=0,
        description="Horizontal scale of the cyclic animation.",
        update=quicktitle_autoupdate)
    cycle_y_scale: bpy.props.FloatProperty(
        name="Y Scale",
        default=1,
        description="Vertical scale of the cyclic animation.",
        update=quicktitle_autoupdate)
    cycle_offset: bpy.props.FloatProperty(
        name="Offset",
        default=0,
        description="Horizontal offset of the cyclic animation.",
        update=quicktitle_autoupdate)
    cycle_type: bpy.props.EnumProperty(
        name="Cycle Type",
        default="NONE",
        items=[('NONE', 'None', '', 1), ('SINE', 'Sine', '', 2), ('TANGENT', 'Tangent', '', 3), ('RANDOM', 'Random', '', 4)],
        description="Type of the cyclic animation.",
        update=quicktitle_autoupdate)


class QuickTitleObject(bpy.types.PropertyGroup):
    #Preset for objects stored in a title scene

    #Basic variables for all object types:
    name: bpy.props.StringProperty(
        name="Object Name",
        description="Name to identify this object.")
    internal_name: bpy.props.StringProperty(
        name="Blender Name",
        description="Reference name to this object used by Blender.")
    type: bpy.props.EnumProperty(
        name="Object Type",
        items=[('TEXT', 'Text', '', 1), ('IMAGE', 'Image', '', 2), ('BOX', 'Box', '', 3), ('CIRCLE', 'Circle', '', 4)],
        description="Type of object")
    x: bpy.props.FloatProperty(
        name="Object X Location",
        default=0,
        description="Horizontal location of this object.  0 is centered, 1 is the right side of screen, -1 is the left side of screen.",
        update=quicktitle_autoupdate)
    y: bpy.props.FloatProperty(
        name="Object Y Location",
        default=0,
        description="Vertical location of this object.  0 is centered, top and bottom vary depending on the aspect ratio of the screen, 0.56 will usually be at the top, -0.56 at the bottom.",
        update=quicktitle_autoupdate)
    z: bpy.props.FloatProperty(
        name="Object Z Position",
        default=0,
        description="Offset for 3d positioning of this object.  This value will affect the position and size of this object, as well as position above or below other objects.",
        update=quicktitle_autoupdate)
    rot_x: bpy.props.FloatProperty(
        name='X Rotation',
        default=0,
        description='Object rotation around the X axis (forward and back tilting).',
        update=quicktitle_autoupdate)
    rot_y: bpy.props.FloatProperty(
        name='Y Rotation',
        default=0,
        description='Object rotation around the Y axis (left and right wobble).',
        update=quicktitle_autoupdate)
    rot_z: bpy.props.FloatProperty(
        name='Z Rotation',
        default=0,
        description='Object rotation around the Z axis (spin).',
        update=quicktitle_autoupdate)
    scale: bpy.props.FloatProperty(
        name="Overall Object Scale",
        default=1,
        min=0,
        description="Overall scaling of this object.  1 is the original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    width: bpy.props.FloatProperty(
        name="Object Width Multiplier",
        default=1,
        min=0,
        description="Multiplies the size of the object on the width axis.  1 is original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    height: bpy.props.FloatProperty(
        name="Object Height Multiplier",
        default=1,
        min=0,
        description="Multiplies the size of the object on the height axis.  1 is the original size, 0.5 is half size, 2 is double size.",
        update=quicktitle_autoupdate)
    shear: bpy.props.FloatProperty(
        name="Shearing",
        default=0,
        min=-1,
        max=1,
        description="Creates an italic effect by shearing the object.  0 is no shearing, 1 is full forward lean, -1 is full backward lean.",
        update=quicktitle_autoupdate)
    set_material: bpy.props.BoolProperty(
        name="Set Material",
        default=False,
        description="When unchecked, this object will use a default material, when checked, you may set the material manually.",
        update=quicktitle_autoupdate)
    set_material_name: bpy.props.StringProperty(
        name="Object Material",
        default="No Preset",
        update=quicktitle_autoupdate)
    material: bpy.props.StringProperty(
        name="Object Material",
        default="No Preset",
        update=quicktitle_autoupdate)
    internal_material: bpy.props.StringProperty(
        name="Internal Object Material Name",
        default="No Preset")
    cast_shadows: bpy.props.BoolProperty(
        name="Cast Shadows",
        default=True,
        description="Allow this object to cast shadows on objects behind it.",
        update=quicktitle_autoupdate)
    use_shadeless: bpy.props.BoolProperty(
        name="Shadeless",
        default=False,
        description="Give this material a solid color with no shading or specularity.",
        update=quicktitle_autoupdate)
    alpha: bpy.props.FloatProperty(
        name="Alpha",
        default=1,
        min=0,
        max=1,
        description="Controls the transparency of this object.  1 is fully visible, 0.5 is somewhat transparent, 0 is invisible.",
        update=quicktitle_autoupdate)
    transmission: bpy.props.FloatProperty(
        name="Transmission",
        default=0,
        min=0,
        max=1,
        description="Controls the glass transparency of this object, only interacts with other objects in the title.  0 is full opacity, 1 is perfect glass transparency.",
        update=quicktitle_autoupdate)
    index_of_refraction: bpy.props.FloatProperty(
        name="Index Of Refraction",
        default=1,
        min=0,
        max=50,
        description="Controls how zoomed in and blurred the transparent background is.  1 is no zoom, 1.4 is medium.",
        update=quicktitle_autoupdate)
    diffuse_color: bpy.props.FloatVectorProperty(
        name="Color Of The Material",
        size=3,
        default=(1, 1, 1),
        min=0,
        max=1,
        subtype='COLOR',
        description="Basic color of this object.",
        update=quicktitle_autoupdate)
    specular_intensity: bpy.props.FloatProperty(
        name="Material Specularity",
        default=0.5,
        min=0,
        max=1,
        description="Controls the specularity, or shininess of this material.",
        update=quicktitle_autoupdate)
    metallic: bpy.props.FloatProperty(
        name="Metallic",
        default=0,
        min=0,
        max=1,
        description="Controls how metallic the material appears.",
        update=quicktitle_autoupdate)
    roughness: bpy.props.FloatProperty(
        name="Roughness",
        default=0.3,
        min=0,
        max=1,
        description="Controls the sharpness of the shinyness of this material.",
        update=quicktitle_autoupdate)
    animations: bpy.props.CollectionProperty(
        type=QuickTitleAnimation)
    selected_animation: bpy.props.IntProperty(
        name='Selected Animation')

    #Variables specific to the Box and Text types:
    extrude: bpy.props.FloatProperty(
        name="Extrude Amount",
        default=0,
        min=0,
        description="Amount of 3d extrusion to apply to this object.",
        update=quicktitle_autoupdate)
    bevel: bpy.props.FloatProperty(
        name="Bevel Size",
        default=0,
        min=0,
        description="Size of the added beveled edge.",
        update=quicktitle_autoupdate)
    bevel_resolution: bpy.props.IntProperty(
        name="Bevel Resolution",
        default=0,
        min=0,
        description="Number of subdivisions on the beveled edge.",
        update=quicktitle_autoupdate)

    #Variables specific to the Text type:
    text: bpy.props.StringProperty(
        name="Text",
        default="None",
        update=quicktitle_autoupdate)
    font: bpy.props.StringProperty(
        name="Font",
        default="Bfont",
        description="Selected font for this text object",
        update=quicktitle_autoupdate)
    word_wrap: bpy.props.BoolProperty(
        name="Word Wrapping",
        default=True,
        description="Enables word-wrapping on text objects to limit the text line width.",
        update=quicktitle_autoupdate)
    wrap_width: bpy.props.FloatProperty(
        name="Word Wrap Width",
        default=.9,
        min=.01,
        description="If word-wrap is enabled, this will determine the width of the text box.  The actual size varies based on object scale.  At a scale of 1, 1 is the full width of the screen, 0.5 is half width, 0.01 will result in one word per line.",
        update=quicktitle_autoupdate)
    align: bpy.props.EnumProperty(
        name="Text Alignment",
        items=[('LEFT', 'Left', '', 1), ('CENTER', 'Center', '', 2), ('RIGHT', 'Right', '', 3), ('JUSTIFY', 'Justify', '', 4), ('FLUSH', 'Flush', '', 5)],
        default='CENTER',
        description="Determines the position of the text within the wrapping box.",
        update=quicktitle_autoupdate)

    #Variables specific to all but Image type:
    outline: bpy.props.BoolProperty(
        name="Enable Outline",
        default=False,
        description="Add an outline around this object",
        update=quicktitle_autoupdate)
    outline_size: bpy.props.FloatProperty(
        name="Outline Size",
        default=1,
        min=0,
        max=100,
        description="Size of the displayed outline",
        update=quicktitle_autoupdate)
    outline_alpha: bpy.props.FloatProperty(
        name="Opacity",
        default=1,
        min=0,
        max=1,
        description="Opacity controls the transparency of this object.  1 is fully visible, 0.5 is half transparent, 0 is invisible.",
        update=quicktitle_autoupdate)
    outline_diffuse_color: bpy.props.FloatVectorProperty(
        name="Color Of The Material",
        size=3,
        default=(0, 0, 0),
        min=0,
        max=1,
        subtype='COLOR',
        description="Basic color of this object.",
        update=quicktitle_autoupdate)
    window_mapping: bpy.props.BoolProperty(
        name="Map Image To View",
        default=False,
        description="Activates 'Window' mapping mode for the image, making it the size of the entire camera view regardless of the image size",
        update=quicktitle_autoupdate)

    #Variables specific to the Image type:
    texture: bpy.props.StringProperty(
        name="Image Texture",
        default="",
        description="File path to the image or video texture.",
        subtype='FILE_PATH',
        update=quicktitle_autoupdate)
    alpha_texture: bpy.props.StringProperty(
        name="Alpha Transparent Texture",
        default="",
        description="File path to the image used for transparency.",
        subtype='FILE_PATH',
        update=quicktitle_autoupdate)
    #Variables specific to video textures
    loop: bpy.props.BoolProperty(
        name="Loop Video",
        default=True,
        description="Enables looping of a video texture",
        update=quicktitle_autoupdate)
    frame_offset: bpy.props.IntProperty(
        name="Frame Offset",
        default=0,
        min=0,
        description="Number of frames to cut off from the beginning of the video.",
        update=quicktitle_autoupdate)
    frame_length: bpy.props.IntProperty(
        name="Frame Length",
        default=1,
        min=1,
        description="Length of video to display in frames",
        update=quicktitle_autoupdate)
    #bounding box
    bbleft: bpy.props.FloatProperty(
        name="Bounding Box Left")
    bbright: bpy.props.FloatProperty(
        name="Bounding Box Right")
    bbtop: bpy.props.FloatProperty(
        name="Bounding Box Top")
    bbbottom: bpy.props.FloatProperty(
        name="Bounding Box Bottom")


class QuickTitle(bpy.types.PropertyGroup):
    #preset for a QuickTitle scene
    name: bpy.props.StringProperty(
        name="Preset Name",
        default="Default",
        description="Name to identify this preset.",
        update=quicktitle_autoupdate)
    description: bpy.props.StringProperty(
        name="Description",
        default="",
        description="Use this text area to describe the preset in detail.")
    z_scale: bpy.props.FloatProperty(
        name="Z Depth Scale",
        default=1,
        min=0,
        description="Determines the depth distance between objects in the title.  This affects the size of the shadows as well.  A value of 0 will place all objects on the same level, 1 is default.",
        update=quicktitle_autoupdate_all)
    objects: bpy.props.CollectionProperty(
        type=QuickTitleObject)
    selected_object: bpy.props.IntProperty(
        name="Selected Object",
        default=0,
        min=0)
    enable_shadows: bpy.props.BoolProperty(
        name="Shadows",
        default=True,
        description="Enables shadows in this title.",
        update=quicktitle_autoupdate)
    lampcenter_internal_name: bpy.props.StringProperty(
        name="Internal Name For The Lamp Center Object",
        default='')
    shadowlamp_internal_name: bpy.props.StringProperty(
        name="Internal Name For The Shadow Lamp",
        default='')
    shadowlamp_inverse_internal_name: bpy.props.StringProperty(
        name="Internal Name For The Inverted Shadow Lamp",
        default='')
    shadowsize: bpy.props.FloatProperty(
        name="Shadow Distance",
        default=1,
        min=0,
        description="Distance of the shadow casting lamp, determines the overall size of the shadows.",
        update=quicktitle_autoupdate)
    shadowamount: bpy.props.FloatProperty(
        name="Shadow Amount",
        default=.5,
        min=0,
        description="Overall opacity of the shadow.  0 is no shadows, 1 is full shadows.",
        update=quicktitle_autoupdate)
    shadowsoft: bpy.props.FloatProperty(
        name="Shadow Softness",
        default=1,
        min=0,
        description="The amount of blur applied to the shadow.  A value of 0 results in fully sharp shadows.",
        update=quicktitle_autoupdate)
    shadowx: bpy.props.FloatProperty(
        name="Shadow Lamp X Position",
        default=0,
        description="Horizontal position of the shadow casting lamp.  -1 is the left side of the screen, 0 is centered, and 1 is the right side of the screen.",
        update=quicktitle_autoupdate)
    shadowy: bpy.props.FloatProperty(
        name="Shadow Lamp Y Position",
        default=0,
        description="Vertical position of the shadow casting lamp.  Values depend on the image aspect ratio, 0.56 will usually be around the top of the screen, 0 at the center, and -0.56 around the bottom.",
        update=quicktitle_autoupdate)
    lightx: bpy.props.FloatProperty(
        name="Lamps X Position",
        default=0,
        update=quicktitle_autoupdate)
    lighty: bpy.props.FloatProperty(
        name="Lamps Y Position",
        default=0,
        update=quicktitle_autoupdate)
    lightrot: bpy.props.FloatProperty(
        name="Lamps Rotation",
        default=0,
        update=quicktitle_autoupdate)
    lightscalex: bpy.props.FloatProperty(
        name="Lamp Position Width",
        default=1,
        min=0,
        max=10,
        update=quicktitle_autoupdate)
    lightscaley: bpy.props.FloatProperty(
        name="Lamp Position Height",
        default=1,
        min=0,
        max=10,
        update=quicktitle_autoupdate)
    length: bpy.props.IntProperty(
        name="Scene Length",
        default=300,
        description="Length of the title preset in frames.  Change this value to automatically adjust animations and scene length.",
        update=quicktitle_autoupdate)


class QUICKTITLING_UL_ObjectListItem(bpy.types.UIList):
    #Draw an object in the object list in the QuickTitler panel

    def draw_filter(self, context, layout):
        #prevent filter options from being visible
        pass

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.9)
        split.label(text=item.name, icon=quicktitle_object_icon(item.type))
        split.operator('quicktitler.delete_object', icon="X", text="").index = index


class QUICKTITLING_UL_AnimationListItem(bpy.types.UIList):
    #Draw an animation in the animation list

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        split = layout.split(factor=0.9)
        split.label(text=item.variable, icon=quicktitle_animation_icon(item.variable))
        split.operator('quicktitler.delete_animation', icon="X", text="").index = index


class QUICKTITLING_PT_Panel(bpy.types.Panel):
    #Panel for QuickTitling settings and operators
    bl_label = "Quick Titling"
    bl_space_type = 'SEQUENCE_EDITOR'
    bl_region_type = 'UI'
    bl_category = 'QuickTitling'

    def draw(self, context):
        layout = self.layout
        quicktitle_sequence = titling_scene_selected()
        quicktitle_preset = current_quicktitle(quicktitle_sequence)
        box = layout.box()
        if not quicktitle_sequence:
            #no title selected, display preset manager
            current_edited = context.scene.quicktitler.current_edited
            row = box.row()
            row.label(text="Select Preset:")
            row.menu('QUICKTITLING_MT_preset_menu', text=quicktitle_preset.name)
            row = box.row()
            row.operator('quicktitler.preset_import', text='Import Preset')
            row = box.row()
            row.operator('quicktitler.create', text='Create New Title').action = 'create'
        else:
            add_overlay()
            #title is selected, only show copy preset back to main button
            current_edited = quicktitle_sequence.scene.quicktitler.current_edited
            row = box.row()
            row.operator('quicktitler.replace_image', text='Render To Image')
            row = box.row()
            row.operator('quicktitler.create', text='Update Title').action = 'update_all'

        row = box.row()
        row.prop(context.scene.quicktitler, 'autoupdate')
        row = layout.row()
        row.separator()

        bottom = layout.box()
        row = bottom.row()
        modified = " (Modified)" if current_edited else ""
        if not quicktitle_sequence:
            row.label(text="Edit This Preset:"+modified)
            row = bottom.row()
            split = row.split()
            split.operator('quicktitler.save_preset')
            split.enabled = current_edited
            row.operator('quicktitler.preset_export', text='Export')

        else:
            row.label(text="Edit Selected Title:"+modified)
            row = bottom.row()
            split = row.split()
            split.operator('quicktitler.save_preset')
            split.enabled = current_edited
            row.operator('quicktitler.preset_export', text='Export')

        row = bottom.row()
        row.prop(quicktitle_preset, 'name')

        row = bottom.row()
        row.prop(quicktitle_preset, 'description')

        row = bottom.row()
        row.prop(quicktitle_preset, 'length')
        row.prop(quicktitle_preset, 'z_scale')

        row = bottom.row()
        row.label(text="Objects:")
        preset_objects = quicktitle_preset.objects
        current_object_index = quicktitle_preset.selected_object
        if len(preset_objects) >= current_object_index + 1:
            current_object = preset_objects[current_object_index]
        else:
            current_object = None

        row = bottom.row()
        row.template_list("QUICKTITLING_UL_ObjectListItem", "", quicktitle_preset, 'objects', quicktitle_preset, 'selected_object', rows=2)
        col = row.column(align=True)
        col.operator("quicktitler.object_up", text="", icon="TRIA_UP").index = quicktitle_preset.selected_object
        col.operator("quicktitler.object_down", text="", icon="TRIA_DOWN").index = quicktitle_preset.selected_object

        row = bottom.row(align=True)
        row.label(text="Add:")
        row.operator('quicktitler.add_object', text='Text', icon=quicktitle_object_icon('TEXT')).type = 'TEXT'
        row.operator('quicktitler.add_object', text='Image', icon=quicktitle_object_icon('IMAGE')).type = 'IMAGE'
        row.operator('quicktitler.add_object', text='Box', icon=quicktitle_object_icon('BOX')).type = 'BOX'
        row.operator('quicktitler.add_object', text='Circle', icon=quicktitle_object_icon('CIRCLE')).type = 'CIRCLE'

        if current_object:
            row = bottom.row()
            row.operator('quicktitler.add_object', text='Duplicate Selected').type = 'DUPLICATE'

            # Object settings
            outline = bottom.box()

            row = outline.row()
            row.prop(current_object, 'name', text='Object Name', icon=quicktitle_object_icon(current_object.type))

            if current_object.type == 'TEXT':
                subarea = outline.box()

                row = subarea.row()
                row.prop(current_object, 'text')

                row = subarea.row()
                split = row.split(factor=0.9, align=True)
                split.menu('QUICKTITLING_MT_fonts_menu', text=current_object.font)
                split.operator('quicktitler.load_font', text='+')

                row = subarea.row()
                row.prop(current_object, 'word_wrap', text='Wrapping')
                row.prop(current_object, 'wrap_width', text='Width')

                row = subarea.row()
                row.prop(current_object, 'align', expand=True)

            row = outline.row(align=True)
            split = row.split(factor=.15, align=True)
            split.label(text='Pos:')
            split.prop(current_object, 'x', text='X')
            split.prop(current_object, 'y', text='Y')
            split.prop(current_object, 'z', text='Z')

            row = outline.row(align=True)
            split = row.split(factor=.15, align=True)
            split.label(text='Rot:')
            split.prop(current_object, 'rot_x', text='X')
            split.prop(current_object, 'rot_y', text='Y')
            split.prop(current_object, 'rot_z', text='Z')

            row = outline.row()
            row.prop(current_object, 'shear', text='Shearing')
            row.prop(current_object, 'scale', text='Scale')

            row = outline.row(align=True)
            row.prop(current_object, 'width', text='Width')
            row.prop(current_object, 'height', text='Height')

            if current_object.type == 'TEXT' or current_object.type == 'BOX' or current_object.type == 'CIRCLE':
                subarea = outline.box()

                row = subarea.row()
                row.label(text='Thickness', icon="MESH_CUBE")
                row.prop(current_object, 'extrude', text='Amount')

                row = subarea.row(align=True)
                row.prop(current_object, 'bevel', text='Bevel')
                row.prop(current_object, 'bevel_resolution', text='Resolution')

                subarea = outline.box()
                row = subarea.row()
                row.label(text="Outline", icon="MOD_SKIN")
                row.prop(current_object, 'outline', text="Enable")
                row = subarea.row()
                split = row.split(factor=.85)
                subsplit = split.split()
                subsplit.prop(current_object, 'outline_size', text='Size')
                subsplit.prop(current_object, 'outline_alpha', text='Alpha')
                split.prop(current_object, 'outline_diffuse_color', text="")

            subarea = outline.box()

            row = subarea.row()
            row.label(text='Material:', icon="MATERIAL_DATA")
            row.prop(current_object, 'set_material', text='Set Material')
            row.operator('quicktitler.new_material', text='New')

            if current_object.set_material:
                row = subarea.row()
                row.menu('QUICKTITLING_MT_materials_menu', text=current_object.set_material_name)

            else:
                row = subarea.row()
                row.label(text=current_object.material)
                row = subarea.row()
                split = row.split(factor=.85)
                subsplit = split.split()
                subsplit.prop(current_object, 'use_shadeless', text='Use No Shading')
                subsplit.prop(current_object, 'cast_shadows', text='Cast Shadows')
                split.prop(current_object, 'diffuse_color', text='')
                if not current_object.use_shadeless:
                    row = subarea.row()
                    row.prop(current_object, 'metallic', text="Metallic")

                    row = subarea.row(align=True)
                    row.prop(current_object, 'specular_intensity', text="Specular")
                    row.prop(current_object, 'roughness', text="Roughness")

                if current_object.type == 'IMAGE':
                    row = subarea.row()
                    row.prop(current_object, 'alpha', text='Alpha Multiply')
                    row = subarea.row()
                    row.prop(current_object, 'texture', text='Texture', icon="IMAGE_RGB")
                    row = subarea.row()
                    row.prop(current_object, 'window_mapping')

                    row = subarea.row()
                    row.prop(current_object, 'alpha_texture', text='Alpha Texture', icon="IMAGE_ALPHA")
                    texture_extension = os.path.splitext(current_object.texture)[1].lower()
                    alpha_extension = os.path.splitext(current_object.alpha_texture)[1].lower()
                    if texture_extension in bpy.path.extensions_movie or alpha_extension in bpy.path.extensions_movie:
                        row = subarea.row()
                        row.prop(current_object, 'loop')
                        row = subarea.row()
                        row.prop(current_object, 'frame_offset')
                        row.prop(current_object, 'frame_length')
                else:
                    row = subarea.row(align=True)
                    row.prop(current_object, 'alpha', text='Alpha')
                    if not current_object.use_shadeless:
                        row = subarea.row(align=True)
                        row.prop(current_object, 'transmission', text='Transmission')
                        row.prop(current_object, 'index_of_refraction', text='IOR')

            subarea = outline.box()

            row = subarea.row()
            row.menu('QUICKTITLING_MT_animations_menu', text='Add Animation', icon="ANIM_DATA")

            if current_object.animations:
                row = subarea.row()
                row.operator('quicktitler.apply_animations', text='Apply To All Objects')

                row = subarea.row()
                row.template_list("QUICKTITLING_UL_AnimationListItem", "", current_object, 'animations', current_object, 'selected_animation', rows=2)

                if current_object.selected_animation < len(current_object.animations):
                    animation = current_object.animations[current_object.selected_animation]

                    row = subarea.row()
                    row.prop(animation, 'animate_in', text='Animate In')
                    row.prop(animation, 'animate_out', text='Animate Out')

                    row = subarea.row()
                    row.prop(animation, 'in_length', text='In Length')
                    row.prop(animation, 'out_length', text='Out Length')

                    row = subarea.row()
                    row.prop(animation, 'in_offset', text='In Frame Offset')
                    row.prop(animation, 'out_offset', text='Out Frame Offset')

                    row = subarea.row()
                    row.prop(animation, 'in_amount', text='In Amount')
                    row.prop(animation, 'out_amount', text='Out Amount')

                    row = subarea.row()
                    row.prop(animation, 'cycle_type', text='Animation Cycle')
                    if animation.cycle_type != 'NONE':
                        row = subarea.row(align=True)
                        row.prop(animation, 'cycle_x_scale')
                        row.prop(animation, 'cycle_y_scale')
                        row = subarea.row()
                        row.prop(animation, 'cycle_offset')

        # Shadow section
        outline = bottom.box()

        row = outline.row()
        split = row.split(factor=.1)
        split.prop(quicktitle_preset, 'enable_shadows', icon="TRIA_DOWN" if quicktitle_preset.enable_shadows else "TRIA_RIGHT", icon_only=True, emboss=True)
        split.label(text='Title Lighting', icon="LIGHT")

        if quicktitle_preset.enable_shadows:
            suboutline = outline.box()
            row = suboutline.row(align=True)
            row.prop(quicktitle_preset, 'lightscalex', text='Lighting Width')
            row.prop(quicktitle_preset, 'lightscaley', text='Lighting Height')

            row = suboutline.row(align=True)
            row.prop(quicktitle_preset, 'lightx', text='Lights X Offset')
            row.prop(quicktitle_preset, 'lighty', text='Lights Y Offset')

            row = suboutline.row()
            row.prop(quicktitle_preset, 'lightrot', text='Lights Rotation')

            suboutline = outline.box()
            row = suboutline.row()
            row.prop(quicktitle_preset, 'shadowamount')

            row = suboutline.row()
            row.prop(quicktitle_preset, 'shadowsize', text='Shadow Distance')
            row.prop(quicktitle_preset, 'shadowsoft', text='Shadow Soft')

            row = suboutline.row(align=True)
            row.prop(quicktitle_preset, 'shadowx', text='Shadow X Offset')
            row.prop(quicktitle_preset, 'shadowy', text='Shadow Y Offset')


class QuickTitlingSavePreset(bpy.types.Operator):
    #Operator to save the current editing title to the scene quicktitles
    bl_idname = 'quicktitler.save_preset'
    bl_label = 'Save To Custom Titles'
    bl_description = 'Saves the current editing title to the scene quicktitles'

    def execute(self, context):
        scene = context.scene
        copy_from = current_quicktitle()
        copy_to = None
        for preset in scene.quicktitler.quicktitles:
            if preset.name == copy_from.name:
                copy_to = preset
                break
        if not copy_to:
            copy_to = scene.quicktitler.quicktitles.add()
        copy_title_preset(copy_from, copy_to)
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            quicktitle_sequence.scene.quicktitler.current_edited = False
        else:
            scene.quicktitler.current_edited = False
        return {'FINISHED'}


class QuickTitlingReplaceWithImage(bpy.types.Operator, ExportHelper):
    #operator that renders out the middle frame of a title scene to an image, then mutes the original sequence and loads that image in
    bl_idname = 'quicktitler.replace_image'
    bl_label = 'Replace With Image'
    bl_description = 'Renders out an image of the quicktitle scene, and places it on the timeline while muting the original.'

    filepath: bpy.props.StringProperty()
    filename_ext = ".png"
    filter_glob: bpy.props.StringProperty(default="*.png", options={'HIDDEN'})
    check_extension = True

    def invoke(self, context, event):
        #set the default filename
        quicktitle = current_quicktitle()
        if quicktitle:
            self.filepath = quicktitle.name
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        #after the file browser is closed, save the image
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            if self.filepath.endswith('.png'):
                imagepath = self.filepath
            else:
                imagepath = self.filepath+'.png'
            scene = quicktitle_sequence.scene
            scene.render.filepath = imagepath
            oldscene = bpy.context.scene
            scene.frame_current = scene.frame_end / 2
            bpy.context.window.scene = scene
            bpy.ops.render.render(write_still=True)
            bpy.context.window.scene = oldscene
            self.report({'INFO'}, "Rendered QuickTitle as: "+imagepath)

            #load the image into the sequencer
            start_frame = quicktitle_sequence.frame_final_start
            end_frame = quicktitle_sequence.frame_final_start + quicktitle_sequence.frame_final_duration - 1
            quicktitle_sequence.mute = True
            path, file = os.path.split(imagepath)
            bpy.ops.sequencer.image_strip_add(directory=path, files=[{'name': file}], frame_start=start_frame, frame_end=end_frame)
            bpy.context.scene.sequence_editor.active_strip.blend_type = 'ALPHA_OVER'
        return {'FINISHED'}


class QuickTitlingObjectMoveUp(bpy.types.Operator):
    #Operator to move a specific object up in the list of objects, object index must be specified
    bl_idname = 'quicktitler.object_up'
    bl_label = 'Move Up'
    bl_description = 'Moves an object up in the current QuickTitling preset.'

    index: bpy.props.IntProperty()
    current: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        scene = find_titling_scene()
        quicktitle = scene.quicktitler.current_quicktitle
        objects = quicktitle.objects
        if self.current:
            quicktitle_sequence = titling_scene_selected()
            frame = bpy.context.scene.frame_current
            if not quicktitle_sequence or not (frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end):
                return {'CANCELLED'}
            self.index = quicktitle.selected_object
        if self.index > 0:
            objects.move(self.index, self.index - 1)
            if quicktitle.selected_object == self.index:
                quicktitle.selected_object = self.index - 1
            elif quicktitle.selected_object == self.index - 1:
                quicktitle.selected_object = self.index
        quicktitle_autoupdate_all()
        return {'FINISHED'}


class QuickTitlingObjectMoveDown(bpy.types.Operator):
    #Operator to move a specific object down in the list of objects, object index must be specified
    bl_idname = 'quicktitler.object_down'
    bl_label = 'Move Down'
    bl_description = 'Moves an object down in the current QuickTitling preset.'

    index: bpy.props.IntProperty()
    current: bpy.props.BoolProperty(default=False)

    def execute(self, context):
        scene = find_titling_scene()
        quicktitle = scene.quicktitler.current_quicktitle
        objects = quicktitle.objects
        if self.current:
            quicktitle_sequence = titling_scene_selected()
            frame = bpy.context.scene.frame_current
            if not quicktitle_sequence or not (frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end):
                return {'CANCELLED'}
            self.index = quicktitle.selected_object
        if self.index+1 < len(objects):
            objects.move(self.index, self.index + 1)
            if quicktitle.selected_object == self.index:
                quicktitle.selected_object = self.index + 1
            elif quicktitle.selected_object == self.index + 1:
                quicktitle.selected_object = self.index
        quicktitle_autoupdate_all()
        return {'FINISHED'}


class QuickTitlingObjectAdd(bpy.types.Operator):
    #Operator to add an object in the current QuickTitler preset, type must be specified
    bl_idname = 'quicktitler.add_object'
    bl_label = 'Add Object'
    bl_description = 'Add an object in the current QuickTitling preset'

    #can be: TEXT, IMAGE, BOX, CIRCLE, DUPLICATE
    type: bpy.props.StringProperty()

    def execute(self, context):
        scene = find_titling_scene()
        quicktitle = scene.quicktitler.current_quicktitle
        if self.type == 'DUPLICATE':
            preset_objects = quicktitle.objects
            current_object_index = quicktitle.selected_object
            if len(preset_objects) >= current_object_index + 1:
                current_object = preset_objects[current_object_index]
            else:
                current_object = None
            if current_object:
                title_object = quicktitle.objects.add()
                copy_object(current_object, title_object)
                title_object.name = title_object.name + ' COPY'
                index = len(quicktitle.objects) - 1
                newindex = current_object_index
                quicktitle.objects.move(index, newindex)
                quicktitle.selected_object = newindex
                quicktitle_autoupdate_all()
                return {'FINISHED'}
            else:
                return {'CANCELLED'}
        else:
            title_object = quicktitle.objects.add()
            title_object.type = self.type
            title_object.name = self.type.capitalize()
            if title_object.type == 'IMAGE':
                title_object.specular_intensity = 0
                title_object.cast_shadows = False
                title_object.use_shadeless = True
            index = len(quicktitle.objects) - 1
            quicktitle.objects.move(index, 0)
            quicktitle.selected_object = 0
            quicktitle_autoupdate_all()
            return {'FINISHED'}


class QuickTitlingObjectSelect(bpy.types.Operator):
    #Operator to select an object in the current QuickTitler preset, index must be specified
    bl_idname = 'quicktitler.select_object'
    bl_label = 'Select Object'
    bl_description = 'Select an object in the current QuickTitling preset'

    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = find_titling_scene()
        scene.quicktitler.current_quicktitle.selected_object = self.index
        return {'FINISHED'}


class QuickTitlingObjectDelete(bpy.types.Operator):
    #Operator to delete an object in the current QuickTitler preset, index must be specified
    bl_idname = 'quicktitler.delete_object'
    bl_label = 'Delete Object'
    bl_description = 'Delete an object in the current QuickTitling preset'

    index: bpy.props.IntProperty()

    def execute(self, context):
        quicktitle_sequence = titling_scene_selected()
        scene = find_titling_scene()
        if quicktitle_sequence:
            objectinfo = scene.quicktitler.current_quicktitle.objects[self.index]
            if objectinfo.internal_name in scene.objects:
                title_object = scene.objects[objectinfo.internal_name]
                outline_object_name = title_object.name+'outline'
                if outline_object_name in scene.objects:
                    outline_object = scene.objects[outline_object_name]
                    scene.collection.objects.unlink(outline_object)
                    bpy.data.objects.remove(outline_object, do_unlink=True)
                scene.collection.objects.unlink(title_object)
                bpy.data.objects.remove(title_object, do_unlink=True)

        scene.quicktitler.current_quicktitle.objects.remove(self.index)
        quicktitle_autoupdate_all()
        return {'FINISHED'}


class QuickTitlingAnimationApply(bpy.types.Operator):
    #Operator to apply the current object's animations to all objects in the QuickTitler preset
    bl_idname = 'quicktitler.apply_animations'
    bl_label = 'Apply Animations'
    bl_description = "Applies the current object's animations to all objects in the current QuickTitler preset"

    def execute(self, context):
        current_object = get_current_object()
        quicktitle = current_quicktitle()
        for title_object in quicktitle.objects:
            if title_object != current_object:
                title_object.animations.clear()
                for animation in current_object.animations:
                    new_animation = title_object.animations.add()
                    new_animation.variable = animation.variable
                    new_animation.animate_in = animation.animate_in
                    new_animation.animate_out = animation.animate_out
                    new_animation.in_length = animation.in_length
                    new_animation.out_length = animation.out_length
                    new_animation.in_offset = animation.in_offset
                    new_animation.out_offset = animation.out_offset
                    new_animation.in_amount = animation.in_amount
                    new_animation.out_amount = animation.out_amount
                    new_animation.cycle_x_scale = animation.cycle_x_scale
                    new_animation.cycle_y_scale = animation.cycle_y_scale
                    new_animation.cycle_offset = animation.cycle_offset
                    new_animation.cycle_type = animation.cycle_type
        quicktitle_autoupdate_all()
        return {'FINISHED'}


class QuickTitlingAnimationAdd(bpy.types.Operator):
    #Operator to add an animation to the current object in the current QuickTitler preset.  Animation preset index must be specified
    bl_idname = 'quicktitler.add_animation'
    bl_label = 'Add Animation'
    bl_description = 'Add an animation to the current object in the current QuickTitling preset'

    index: bpy.props.IntProperty()

    def execute(self, context):
        title_object = get_current_object()
        animation_preset = animations[self.index]
        animation = False
        for animation_set in title_object.animations:
            if animation_set.variable == animation_preset['variable']:
                #an animation of this type already exists, overwrite it
                animation = animation_set
        if not animation:
            animation = title_object.animations.add()

        #update all animation variables
        animation.variable = animation_preset['variable']
        animation.animate_in = animation_preset['animate_in']
        animation.animate_out = animation_preset['animate_out']
        animation.in_length = animation_preset['in_length']
        animation.out_length = animation_preset['out_length']
        animation.in_offset = animation_preset['in_offset']
        animation.out_offset = animation_preset['out_offset']
        animation.in_amount = animation_preset['in_amount']
        animation.out_amount = animation_preset['out_amount']
        animation.cycle_x_scale = animation_preset['cycle_x_scale']
        animation.cycle_y_scale = animation_preset['cycle_y_scale']
        animation.cycle_offset = animation_preset['cycle_offset']
        animation.cycle_type = animation_preset['cycle_type']
        title_object.selected_animation = len(title_object.animations) - 1
        quicktitle_autoupdate()
        return {'FINISHED'}


class QuickTitlingAnimationDelete(bpy.types.Operator):
    #Operator to delete an animation in the current selected object of the current QuickTitler preset.  Animation index must be specified
    bl_idname = 'quicktitler.delete_animation'
    bl_label = 'Delete Animation'
    bl_description = 'Delete an animation from the current object in the current QuickTitling preset'

    index: bpy.props.IntProperty()

    def execute(self, context):
        object_preset = get_current_object()
        object_preset.animations.remove(self.index)
        quicktitle_autoupdate()
        return {'FINISHED'}


class QuickTitlingAnimationMenu(bpy.types.Menu):
    #Menu for listing animation types
    bl_idname = 'QUICKTITLING_MT_animations_menu'
    bl_label = 'List of animations'

    def draw(self, context):
        layout = self.layout
        for index, animation in enumerate(animations):
            if animation['name'] == 'SPACER':
                layout.separator()
            else:
                layout.operator('quicktitler.add_animation', text=animation['name'], icon=quicktitle_animation_icon(animation['variable'])).index = index


class QuickTitlingNewMaterial(bpy.types.Operator):
    #Makes a new default material for the selected object
    bl_idname = 'quicktitler.new_material'
    bl_label = 'New Material'
    bl_description = "Makes a new default material"

    def execute(self, context):
        scene = context.scene
        object_preset = get_current_object()
        if object_preset:
            object_preset.material = 'No Preset'
        return {"FINISHED"}


class QuickTitlingPresetDelete(bpy.types.Operator):
    #Operator to delete a QuickTitler preset.  Preset index must be specified
    bl_idname = 'quicktitler.preset_delete'
    bl_label = 'Delete Presets'
    bl_description = 'Delete A Specific QuickTitling Preset'

    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.quicktitler.quicktitles.remove(self.index)
        return {'FINISHED'}


class QuickTitlingPresetExport(bpy.types.Operator, ExportHelper):
    #Operator to export the current QuickTitler preset to a file.
    bl_idname = 'quicktitler.preset_export'
    bl_label = 'Export Preset'
    bl_description = 'Exports the current selected QuickTitling preset to a file'

    filename_ext = ".xml"
    filter_glob: bpy.props.StringProperty(default="*.xml", options={'HIDDEN'})
    filepath: bpy.props.StringProperty()
    check_extension = True

    def invoke(self, context, event):
        #Set up the default filename
        quicktitle = current_quicktitle()
        if quicktitle:
            self.filepath = quicktitle.name
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        #a file has been selected, save to that file
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            #render out a preview image
            if self.filepath.endswith('.xml'):
                imagepath = self.filepath[:-4]
            else:
                imagepath = self.filepath
            if imagepath.endswith('.jpg'):
                imagepath = self.filepath
            else:
                imagepath = imagepath+'.jpg'
            scene = quicktitle_sequence.scene
            scene.render.filepath = imagepath
            old_file_format = scene.render.image_settings.file_format
            old_quality = scene.render.image_settings.quality
            old_resolution_percentage = scene.render.resolution_percentage
            old_color_mode = scene.render.image_settings.color_mode
            old_res_x = scene.render.resolution_x
            old_res_y = scene.render.resolution_y
            aspect = scene.render.resolution_x / scene.render.resolution_y
            res = 300
            scene.render.resolution_x = res
            scene.render.resolution_y = int(res / aspect)
            scene.render.image_settings.file_format = 'JPEG'
            scene.render.image_settings.quality = 80
            scene.render.resolution_percentage = 100
            scene.render.image_settings.color_mode = 'RGB'

            oldscene = bpy.context.scene
            scene.frame_current = scene.frame_end / 2
            bpy.context.window.scene = scene
            bpy.ops.render.render(write_still=True)
            bpy.context.window.scene = oldscene
            self.report({'INFO'}, "Rendered QuickTitle Preview As: "+imagepath)

            scene.render.resolution_x = old_res_x
            scene.render.resolution_y = old_res_y
            scene.render.image_settings.file_format = old_file_format
            scene.render.image_settings.quality = old_quality
            scene.render.resolution_percentage = old_resolution_percentage
            scene.render.image_settings.color_mode = old_color_mode

        preset = current_quicktitle()
        if not preset:
            return {'CANCELED'}
        import xml.etree.cElementTree as Tree
        root = Tree.Element("preset")
        Tree.SubElement(root, 'name').text = preset.name
        if preset.description:
            Tree.SubElement(root, 'description').text = preset.description
        if preset.z_scale != get_default('z_scale', class_type='Title'):
            Tree.SubElement(root, 'z_scale').text = str(preset.z_scale)
        if preset.length != get_default('length', class_type='Title'):
            Tree.SubElement(root, 'length').text = str(preset.length)
        if preset.shadowsize != get_default('shadowsize', class_type='Title'):
            Tree.SubElement(root, 'shadowsize').text = str(preset.shadowsize)
        if preset.shadowamount != get_default('shadowamount', class_type='Title'):
            Tree.SubElement(root, 'shadowamount').text = str(preset.shadowamount)
        if preset.shadowsoft != get_default('shadowsoft', class_type='Title'):
            Tree.SubElement(root, 'shadowsoft').text = str(preset.shadowsoft)
        if preset.shadowx != get_default('shadowx', class_type='Title'):
            Tree.SubElement(root, 'shadowx').text = str(preset.shadowx)
        if preset.shadowy != get_default('shadowy', class_type='Title'):
            Tree.SubElement(root, 'shadowy').text = str(preset.shadowy)
        if preset.lightscalex != get_default('lightscalex', class_type='Title'):
            Tree.SubElement(root, 'lightscalex').text = str(preset.lightscalex)
        if preset.lightscaley != get_default('lightscaley', class_type='Title'):
            Tree.SubElement(root, 'lightscaley').text = str(preset.lightscaley)
        if preset.lightx != get_default('lightx', class_type='Title'):
            Tree.SubElement(root, 'lightx').text = str(preset.lightx)
        if preset.lighty != get_default('lighty', class_type='Title'):
            Tree.SubElement(root, 'lighty').text = str(preset.lighty)
        if preset.lightrot != get_default('lightrot', class_type='Title'):
            Tree.SubElement(root, 'lightrot').text = str(preset.lightrot)
        for title_object in preset.objects:
            objects = Tree.SubElement(root, 'objects')
            Tree.SubElement(objects, 'name').text = title_object.name
            Tree.SubElement(objects, 'type').text = title_object.type
            if title_object.x != get_default('x'):
                Tree.SubElement(objects, 'x').text = str(title_object.x)
            if title_object.y != get_default('y'):
                Tree.SubElement(objects, 'y').text = str(title_object.y)
            if title_object.z != get_default('z'):
                Tree.SubElement(objects, 'z').text = str(title_object.z)
            if title_object.rot_x != get_default('rot_x'):
                Tree.SubElement(objects, 'rot_x').text = str(title_object.rot_x)
            if title_object.rot_y != get_default('rot_y'):
                Tree.SubElement(objects, 'rot_y').text = str(title_object.rot_y)
            if title_object.rot_z != get_default('rot_z'):
                Tree.SubElement(objects, 'rot_z').text = str(title_object.rot_z)
            if title_object.scale != get_default('scale'):
                Tree.SubElement(objects, 'scale').text = str(title_object.scale)
            if title_object.width != get_default('width'):
                Tree.SubElement(objects, 'width').text = str(title_object.width)
            if title_object.height != get_default('height'):
                Tree.SubElement(objects, 'height').text = str(title_object.height)
            if title_object.shear != get_default('shear'):
                Tree.SubElement(objects, 'shear').text = str(title_object.shear)
            if title_object.cast_shadows != get_default('cast_shadows'):
                Tree.SubElement(objects, 'cast_shadows').text = str(title_object.cast_shadows)
            if title_object.set_material != get_default('set_material'):
                Tree.SubElement(objects, 'set_material').text = str(title_object.set_material)
            if title_object.material != get_default('material'):
                Tree.SubElement(objects, 'material').text = title_object.material
            if title_object.use_shadeless != get_default('use_shadeless'):
                Tree.SubElement(objects, 'use_shadeless').text = str(title_object.use_shadeless)
            if title_object.alpha != get_default('alpha'):
                Tree.SubElement(objects, 'alpha').text = str(title_object.alpha)
            if title_object.index_of_refraction != get_default('index_of_refraction'):
                Tree.SubElement(objects, 'index_of_refraction').text = str(title_object.index_of_refraction)
            if title_object.transmission != get_default('transmission'):
                Tree.SubElement(objects, 'transmission').text = str(title_object.transmission)
            if title_object.diffuse_color != get_default('diffuse_color'):
                diffuse_color = str(round(title_object.diffuse_color[0] * 255))+', '+str(round(title_object.diffuse_color[1] * 255))+', '+str(round(title_object.diffuse_color[2] * 255))
                Tree.SubElement(objects, 'diffuse_color').text = diffuse_color
            if title_object.specular_intensity != get_default('specular_intensity'):
                Tree.SubElement(objects, 'specular_intensity').text = str(title_object.specular_intensity)
            if title_object.metallic != get_default('metallic'):
                Tree.SubElement(objects, 'metallic').text = str(title_object.metallic)
            if title_object.roughness != get_default('roughness'):
                Tree.SubElement(objects, 'roughness').text = str(title_object.roughness)
            if title_object.extrude != get_default('extrude'):
                Tree.SubElement(objects, 'extrude').text = str(title_object.extrude)
            if title_object.bevel != get_default('bevel'):
                Tree.SubElement(objects, 'bevel').text = str(title_object.bevel)
            if title_object.bevel_resolution != get_default('bevel_resolution'):
                Tree.SubElement(objects, 'bevel_resolution').text = str(title_object.bevel_resolution)
            if title_object.text != get_default('text'):
                Tree.SubElement(objects, 'text').text = title_object.text
            if title_object.font != get_default('font'):
                Tree.SubElement(objects, 'font').text = title_object.font
            if title_object.word_wrap != get_default('word_wrap'):
                Tree.SubElement(objects, 'word_wrap').text = str(title_object.word_wrap)
            if title_object.wrap_width != get_default('wrap_width'):
                Tree.SubElement(objects, 'wrap_width').text = str(title_object.wrap_width)
            if title_object.align != get_default('align'):
                Tree.SubElement(objects, 'align').text = title_object.align
            if title_object.outline != get_default('outline'):
                Tree.SubElement(objects, 'outline').text = str(title_object.outline)
            if title_object.outline_size != get_default('outline_size'):
                Tree.SubElement(objects, 'outline_size').text = str(title_object.outline_size)
            if title_object.outline_alpha != get_default('outline_alpha'):
                Tree.SubElement(objects, 'outline_alpha').text = str(title_object.outline_alpha)
            if title_object.outline_diffuse_color != get_default('outline_diffuse_color'):
                outline_color = str(round(title_object.outline_diffuse_color[0] * 255))+', '+str(round(title_object.outline_diffuse_color[1] * 255))+', '+str(round(title_object.outline_diffuse_color[2] * 255))
                Tree.SubElement(objects, 'outline_diffuse_color').text = outline_color
            if title_object.window_mapping != get_default('window_mapping'):
                Tree.SubElement(objects, 'window_mapping').text = str(title_object.window_mapping)
            if title_object.texture != get_default('texture'):
                Tree.SubElement(objects, 'texture').text = title_object.texture
            if title_object.alpha_texture != get_default('alpha_texture'):
                Tree.SubElement(objects, 'alpha_texture').text = title_object.alpha_texture
            if title_object.loop != get_default('loop'):
                Tree.SubElement(objects, 'loop').text = str(title_object.loop)
            if title_object.frame_offset != get_default('frame_offset'):
                Tree.SubElement(objects, 'frame_offset').text = str(title_object.frame_offset)
            if title_object.frame_length != get_default('frame_length'):
                Tree.SubElement(objects, 'frame_length').text = str(title_object.frame_length)

            for animation in title_object.animations:
                object_animations = Tree.SubElement(objects, 'animations')
                Tree.SubElement(object_animations, 'variable').text = animation.variable
                if animation.animate_in != get_default('animate_in', class_type='Animation'):
                    Tree.SubElement(object_animations, 'animate_in').text = str(animation.animate_in)
                if animation.animate_out != get_default('animate_out', class_type='Animation'):
                    Tree.SubElement(object_animations, 'animate_out').text = str(animation.animate_out)
                if animation.in_length != get_default('in_length', class_type='Animation'):
                    Tree.SubElement(object_animations, 'in_length').text = str(animation.in_length)
                if animation.out_length != get_default('out_length', class_type='Animation'):
                    Tree.SubElement(object_animations, 'out_length').text = str(animation.out_length)
                if animation.in_offset != get_default('in_offset', class_type='Animation'):
                    Tree.SubElement(object_animations, 'in_offset').text = str(animation.in_offset)
                if animation.out_offset != get_default('out_offset', class_type='Animation'):
                    Tree.SubElement(object_animations, 'out_offset').text = str(animation.out_offset)
                if animation.in_amount != get_default('in_amount', class_type='Animation'):
                    Tree.SubElement(object_animations, 'in_amount').text = str(animation.in_amount)
                if animation.out_amount != get_default('out_amount', class_type='Animation'):
                    Tree.SubElement(object_animations, 'out_amount').text = str(animation.out_amount)
                if animation.cycle_type != get_default('cycle_type', class_type='Animation'):
                    Tree.SubElement(object_animations, 'cycle_type').text = animation.cycle_type
                if animation.cycle_x_scale != get_default('cycle_x_scale', class_type='Animation'):
                    Tree.SubElement(object_animations, 'cycle_x_scale').text = str(animation.cycle_x_scale)
                if animation.cycle_y_scale != get_default('cycle_y_scale', class_type='Animation'):
                    Tree.SubElement(object_animations, 'cycle_y_scale').text = str(animation.cycle_y_scale)
                if animation.cycle_offset != get_default('cycle_offset', class_type='Animation'):
                    Tree.SubElement(object_animations, 'cycle_offset').text = str(animation.cycle_offset)
        tree = Tree.ElementTree(root)
        indent(root)
        if not self.filepath.endswith('.xml'):
            self.filepath = self.filepath + '.xml'
        tree.write(self.filepath)
        self.report({'INFO'}, "Saved file to: "+self.filepath)
        return {'FINISHED'}


def indent(elem, level=0):
    i = "\n" + level*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i


class QuickTitlingPresetImport(bpy.types.Operator, ImportHelper):
    #Operator to import a QuickTitler preset from a file
    bl_idname = 'quicktitler.preset_import'
    bl_label = 'Import Preset'
    bl_description = 'Imports a QuickTitling preset from a file'

    filename_ext = ".xml"
    filter_glob: bpy.props.StringProperty(default="*.xml", options={'HIDDEN'})
    filepath: bpy.props.StringProperty()

    def execute(self, context):
        #the file has been selected, attempt to parse it as a preset
        preset = load_quicktitle(self.filepath, context.scene.quicktitler.current_quicktitle)
        if preset:
            return {'FINISHED'}
        else:
            print("Failed to import file, not a valid preset: "+self.filepath)
            self.report({'WARNING'}, "Failed to import file, not a valid preset: "+self.filepath)
            return {'CANCELLED'}


def split_list(alist, parts=1):
    length = len(alist)
    return [alist[i*length // parts: (i+1)*length // parts] for i in range(parts)]


class QuickTitlingPresetMenuAdd(bpy.types.Menu):
    bl_idname = 'QUICKTITLING_MT_preset_menu_add'
    bl_label = 'QuickTitles'

    icon: bpy.props.EnumProperty("")

    def draw(self, context):
        draw_preset_menu(self, context, add=True)


class QuickTitlingPresetMenu(bpy.types.Menu):
    #Menu to list the QuickTitler Presets in the scene
    bl_idname = 'QUICKTITLING_MT_preset_menu'
    bl_label = 'List of saved presets'

    icon: bpy.props.EnumProperty("")

    def draw(self, context):
        draw_preset_menu(self, context)


def draw_preset_menu(self, context, add=False):
    presets = list_quicktitle_presets(context.scene)
    layout = self.layout

    global quicktitle_previews
    global current_icon_id

    split = layout.split()

    column = split.column()
    column.label(text="Custom Titles:")
    column.scale_y = 3
    for index, preset in enumerate(presets):
        if preset[1] != 'BUILTIN':
            if add:
                column.operator('quicktitler.select_and_add', text=preset[0]).preset = 'custom,'+preset[0]
            else:
                column.operator('quicktitler.preset_select', text=preset[0]).preset = preset[0]

    column = split.column()
    column.scale_y = 3
    column.label(text=" ")
    for index, preset in enumerate(presets):
        if preset[1] != 'BUILTIN':
            column.operator("quicktitler.preset_delete", text="", icon="X").index = index

    column = split.column()
    column.label(text=" ")

    split_presets = split_list(presets, 2)
    for index, presets in enumerate(split_presets):
        column = split.column()
        column.scale_y = 3
        if index == 0:
            column.label(text="Built-in Titles:")
            if add:
                column.operator('quicktitler.select_and_add', text='Default').preset = 'builtin,'+'Default'
            else:
                column.operator('quicktitler.preset_load', text='Default').preset = 'Default'
        else:
            column.label(text="")
        for preset in presets:
            if preset[1] == 'BUILTIN':
                if add:
                    column.operator('quicktitler.select_and_add', text=preset[0]).preset = 'builtin,'+preset[0]
                else:
                    column.operator('quicktitler.preset_load', text=preset[0]).preset = preset[0]

        column = split.column()
        column.scale_y = .5
        column.scale_x = .5
        current_icon_id = 0
        column.template_icon_view(context.scene.quicktitler, 'current_icon')
        if index == 0:
            #display a blank icon for the default setting
            column.template_icon_view(context.scene.quicktitler, 'current_icon')
        for preset in presets:
            if preset[1] == 'BUILTIN':
                image = get_presets_directory()+os.path.sep+preset[0]+'.jpg'
                if preset[0]+'BUILTIN' not in quicktitle_previews:
                    quicktitle_previews.load(preset[0]+'BUILTIN', image, 'IMAGE')
                current_icon_id = quicktitle_previews[preset[0]+'BUILTIN'].icon_id
                column.template_icon_view(context.scene.quicktitler, 'current_icon')


class QuickTitlingPresetSelectAdd(bpy.types.Operator):
    bl_idname = 'quicktitler.select_and_add'
    bl_label = 'Select And Add Preset'

    #Preset type,name
    preset: bpy.props.StringProperty()

    def execute(self, context):
        preset_type, name = self.preset.split(',', 1)
        bpy.ops.sequencer.select_all(action='DESELECT')
        if preset_type == 'custom':
            bpy.ops.quicktitler.preset_select(preset=name)
            bpy.ops.quicktitler.create(action='create')
        else:
            bpy.ops.quicktitler.preset_load(preset=name)
            bpy.ops.quicktitler.create(action='create')
        return {'FINISHED'}


class QuickTitlingPresetSelect(bpy.types.Operator):
    #Operator to select a QuickTitling preset so it can be displayed.  Preset name must be specified
    bl_idname = 'quicktitler.preset_select'
    bl_label = 'Set Preset'
    bl_description = 'Select A QuickTitling Scene Preset'

    #Preset name
    preset: bpy.props.StringProperty()

    def execute(self, context):
        if not self.preset:
            return {'FINISHED'}
        scene = context.scene
        preset = scene_quicktitle_from_name(scene.quicktitler.quicktitles, self.preset)
        copy_title_preset(preset, scene.quicktitler.current_quicktitle)
        scene.quicktitler.current_edited = False
        return {'FINISHED'}


class QuickTitlingPresetLoad(bpy.types.Operator):
    #Operator to select a QuickTitling preset so it can be displayed.  Preset name must be specified
    bl_idname = 'quicktitler.preset_load'
    bl_label = 'Set Preset'
    bl_description = 'Select A QuickTitling Builtin Preset'

    #Preset name
    preset: bpy.props.StringProperty()

    def execute(self, context):
        if not self.preset:
            return {'FINISHED'}
        scene = context.scene
        if self.preset == 'Default':
            set_default(scene.quicktitler.current_quicktitle)
        else:
            basename = get_presets_directory()+os.path.sep+self.preset
            file = basename + '.xml'
            load_quicktitle(file, scene.quicktitler.current_quicktitle)
        scene.quicktitler.current_edited = False
        return {'FINISHED'}


class QuickTitlingLoadFont(bpy.types.Operator):
    #Operator to load a new font into Blender and select it
    bl_idname = 'quicktitler.load_font'
    bl_label = 'Load Font'
    bl_description = 'Load A New Font'

    #font file to be loaded
    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def execute(self, context):
        #When the file browser finishes, this is called
        #Try to load font file
        try:
            font = bpy.data.fonts.load(self.filepath)
            current_object = get_current_object()
            if current_object:
                current_object.font = font.name
        except:
            print("Not a valid font file: "+self.filepath)
            self.report({'WARNING'}, "Not a valid font file: "+self.filepath)

        return {'FINISHED'}

    def invoke(self, context, event):
        #Open a file browser
        context.window_manager.fileselect_add(self)

        return{'RUNNING_MODAL'}


class QuickTitlingFontMenu(bpy.types.Menu):
    #Menu for listing and changing QuickTitler fonts
    bl_idname = 'QUICKTITLING_MT_fonts_menu'
    bl_label = 'List of loaded fonts'

    def draw(self, context):
        fonts = bpy.data.fonts
        layout = self.layout

        #Ensure that the default font is always displayed
        if 'Bfont' not in fonts:
            layout.operator('quicktitler.change_font', text='Bfont').font = 'Bfont'

        for font in fonts:
            layout.operator('quicktitler.change_font', text=font.name).font = font.name


class QuickTitlingChangeFont(bpy.types.Operator):
    #Operator for changing the QuickTitler font on the current preset.  The font variable must be specified
    bl_idname = 'quicktitler.change_font'
    bl_label = 'Change Font'

    font: bpy.props.StringProperty()

    def execute(self, context):
        current_object = get_current_object()
        if current_object:
            current_object.font = self.font

        return {'FINISHED'}


class QuickTitlingMaterialMenu(bpy.types.Menu):
    #Menu to list all Materials in blend file, and assign them to QuickTitler objects
    bl_idname = 'QUICKTITLING_MT_materials_menu'
    bl_label = 'List of loaded materials'

    def draw(self, context):
        materials = bpy.data.materials
        layout = self.layout
        layout.operator('quicktitler.change_material', text='No Preset').material = 'No Preset'
        for material in materials:
            layout.operator('quicktitler.change_material', text=material.name).material = material.name


class QuickTitlingChangeMaterial(bpy.types.Operator):
    #Operator to assign a material name to the material of the current object.  The material variable must be set
    bl_idname = 'quicktitler.change_material'
    bl_label = 'Change material on the current object'

    material: bpy.props.StringProperty()

    def execute(self, context):
        current_object = get_current_object()
        if current_object:
            if self.material == 'No Preset':
                current_object.set_material = False
            current_object.set_material_name = self.material

        return {'FINISHED'}


class QuickTitlingCreate(bpy.types.Operator):
    #Operator to create QuickTitle scenes from the current quicktitle preset.  Can be used to just update titles as well.
    bl_idname = 'quicktitler.create'
    bl_label = 'Create QuickTitling Scene'
    bl_description = 'Creates or updates a titler scene'

    #Should be set to 'create', 'update' or 'update-all'
    action: bpy.props.StringProperty()

    def execute(self, context):
        quicktitle = current_quicktitle()
        if not quicktitle:
            print('No QuickTitle Preset Found')
            self.report({'WARNING'}, 'No QuickTitle Preset Found')
            return {'CANCELLED'}
        if self.action == 'create':
            quicktitle_create(quicktitle)

        sequence = bpy.context.scene.sequence_editor.active_strip
        if self.action == 'update_all':
            update_all = True
        else:
            update_all = False

        quicktitle_update(sequence, sequence.scene.quicktitler.current_quicktitle, update_all)
        if self.action == 'create':
            sequence.scene.quicktitler.current_edited = context.scene.quicktitler.current_edited
        return {'FINISHED'}


def current_icon_enum(self, context):
    global current_icon_id
    return [(str(current_icon_id), 'ICON', "", current_icon_id, 0)]


class QuickTitleSettings(bpy.types.PropertyGroup):
    autoupdate: bpy.props.BoolProperty(
        name="Auto-Update Titles",
        default=True)
    current_icon: bpy.props.EnumProperty(
        name='Current Icon',
        items=current_icon_enum)
    current_edited: bpy.props.BoolProperty(
        name='Selected Title Is Edited',
        default=False)
    current_quicktitle: bpy.props.PointerProperty(type=QuickTitle)
    quicktitles: bpy.props.CollectionProperty(type=QuickTitle)


class QuickTitlingGrab(bpy.types.Operator):
    #Operator for moving title elements in the preview area
    bl_idname = 'quicktitle.grab'
    bl_label = "Grab/Move Title Object"

    lamp: bpy.props.BoolProperty(default=False)
    feedback = ''
    value = ''
    constrain = False
    mouse_x = 0
    mouse_y = 0
    object_preset = None
    scene = None
    preset = None
    start_x = 0
    start_y = 0
    start_z = 0
    mouse_scale = 500

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                return True
        return False

    def modal(self, context, event):
        global overlay_info
        if event.value == 'PRESS':
            self.value = add_to_value(self.value, event.type)
        if event.type == 'X' and event.value == 'PRESS':
            if self.constrain == 'X':
                self.constrain = False
            else:
                self.constrain = 'X'
        if event.type == 'Y' and event.value == 'PRESS':
            if self.constrain == 'Y':
                self.constrain = False
            else:
                self.constrain = 'Y'
        if event.type == 'Z' and event.value == 'PRESS':
            if self.constrain == 'Z':
                self.constrain = False
            else:
                self.constrain = 'Z'
        mouse_x_delta = (self.mouse_x - event.mouse_x) / self.mouse_scale
        mouse_y_delta = (self.mouse_y - event.mouse_y) / self.mouse_scale
        if event.shift:
            mouse_x_delta = mouse_x_delta / 4
            mouse_y_delta = mouse_y_delta / 4
        mouse_delta = (mouse_x_delta + mouse_y_delta) / 2
        if self.constrain == 'X':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_x_delta = -float_value
                except:
                    pass
            if self.lamp:
                self.preset.shadowx = self.start_x - mouse_x_delta
                self.preset.shadowy = self.start_y
                self.preset.shadowsize = self.start_z
                self.feedback = 'Move Shadow (X): '+str(round(-mouse_x_delta, 4))
            else:
                self.object_preset.x = self.start_x - mouse_x_delta
                self.object_preset.y = self.start_y
                self.object_preset.z = self.start_z
                self.feedback = 'Move (X): '+str(round(-mouse_x_delta, 4))
        elif self.constrain == 'Y':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_y_delta = -float_value
                except:
                    pass
            if self.lamp:
                self.preset.shadowx = self.start_x
                self.preset.shadowy = self.start_y - mouse_y_delta
                self.preset.shadowsize = self.start_z
                self.feedback = 'Move Shadow (Y): '+str(round(-mouse_y_delta, 4))
            else:
                self.object_preset.x = self.start_x
                self.object_preset.y = self.start_y - mouse_y_delta
                self.object_preset.z = self.start_z
                self.feedback = 'Move (Y): '+str(round(-mouse_y_delta, 4))
        elif self.constrain == 'Z':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_delta = -float_value
                except:
                    pass
            if self.lamp:
                self.preset.shadowx = self.start_x
                self.preset.shadowy = self.start_y
                self.preset.shadowsize = self.start_z - mouse_delta
                self.feedback = 'Move Shadow (Z): '+str(round(-mouse_delta, 4))
            else:
                self.object_preset.x = self.start_x
                self.object_preset.y = self.start_y
                self.object_preset.z = self.start_z - mouse_delta
                self.feedback = 'Move (Z): '+str(round(-mouse_delta, 4))
        else:
            if self.lamp:
                self.preset.shadowx = self.start_x - mouse_x_delta
                self.preset.shadowy = self.start_y - mouse_y_delta
                self.preset.shadowsize = self.start_z
                self.feedback = 'Move Shadow: X: '+str(round(-mouse_x_delta, 4))+', Y: '+str(round(-mouse_y_delta, 4))
            else:
                self.object_preset.x = self.start_x - mouse_x_delta
                self.object_preset.y = self.start_y - mouse_y_delta
                self.object_preset.z = self.start_z
                self.feedback = 'Move: X: '+str(round(-mouse_x_delta, 4))+', Y: '+str(round(-mouse_y_delta, 4))
        if event.type in {'LEFTMOUSE', 'RET'}:
            overlay_info = ''
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            if self.lamp:
                self.preset.shadowx = self.start_x
                self.preset.shadowy = self.start_y
                self.preset.shadowsize = self.start_z
            else:
                self.object_preset.x = self.start_x
                self.object_preset.y = self.start_y
                self.object_preset.z = self.start_z
            overlay_info = ''
            return {'CANCELLED'}

        overlay_info = self.feedback
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.feedback = ''
        self.value = ''
        self.constrain = False
        titling_sequence = titling_scene_selected()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        self.scene = titling_sequence.scene
        self.preset = self.scene.quicktitler.current_quicktitle
        if self.lamp:
            self.start_x = self.preset.shadowx
            self.start_y = self.preset.shadowy
            self.start_z = self.preset.shadowsize
            region = context.region
            left, bottom = region.view2d.region_to_view(0, 0)
            right, top = region.view2d.region_to_view(region.width, region.height)
            width = right - left
            scale = width / region.width
            self.mouse_scale = 1000 / scale
            context.window_manager.modal_handler_add(self)
            return {'RUNNING_MODAL'}
        else:
            if len(self.preset.objects) > self.preset.selected_object:
                self.object_preset = self.preset.objects[self.preset.selected_object]
                self.start_x = self.object_preset.x
                self.start_y = self.object_preset.y
                self.start_z = self.object_preset.z
                object_name = self.object_preset.internal_name
                if object_name in self.scene.objects:
                    region = context.region
                    left, bottom = region.view2d.region_to_view(0, 0)
                    right, top = region.view2d.region_to_view(region.width, region.height)
                    width = right - left
                    scale = width / region.width
                    self.mouse_scale = 1000 / scale
                    context.window_manager.modal_handler_add(self)
                    return {'RUNNING_MODAL'}

        return {'CANCELLED'}


class QuickTitlingRotate(bpy.types.Operator):
    #Operator for rotating title elements in the preview area
    bl_idname = 'quicktitle.rotate'
    bl_label = "Rotate Title Object"

    feedback = ''
    value = ''
    constrain = False
    mouse_x = 0
    mouse_y = 0
    title_object = None
    object_preset = None
    scene = None
    preset = None
    start_x = 0
    start_y = 0
    start_z = 0
    mouse_scale = 500

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                return True
        return False

    def modal(self, context, event):
        global overlay_info
        if event.value == 'PRESS':
            self.value = add_to_value(self.value, event.type)
        if event.type == 'X' and event.value == 'PRESS':
            if self.constrain == 'X':
                self.constrain = False
            else:
                self.constrain = 'X'
        if event.type == 'Y' and event.value == 'PRESS':
            if self.constrain == 'Y':
                self.constrain = False
            else:
                self.constrain = 'Y'
        if event.type == 'Z' and event.value == 'PRESS':
            if self.constrain == 'Z':
                self.constrain = False
            else:
                self.constrain = 'Z'
        mouse_x_delta = (self.mouse_x - event.mouse_x) / self.mouse_scale
        mouse_y_delta = (self.mouse_y - event.mouse_y) / self.mouse_scale
        mouse_delta = (mouse_x_delta + mouse_y_delta) / 2
        if event.shift:
            mouse_x_delta = mouse_x_delta / 4
            mouse_y_delta = mouse_y_delta / 4
            mouse_delta = mouse_delta / 4

        if self.constrain == 'X':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_y_delta = float_value
                except:
                    pass
            self.object_preset.rot_x = self.start_x + mouse_y_delta
            self.object_preset.rot_y = self.start_y
            self.object_preset.rot_z = self.start_z
            self.feedback = 'Rotate (X Axis): '+str(mouse_y_delta)
        elif self.constrain == 'Y':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_x_delta = -float_value
                except:
                    pass
            self.object_preset.rot_x = self.start_x
            self.object_preset.rot_y = self.start_y - mouse_x_delta
            self.object_preset.rot_z = self.start_z
            self.feedback = 'Rotate (Y Axis): '+str(-mouse_x_delta)
        elif self.constrain == 'Z':
            if self.value:
                try:
                    float_value = float(self.value)
                    mouse_delta = float_value
                except:
                    pass
            self.object_preset.rot_x = self.start_x
            self.object_preset.rot_y = self.start_y
            self.object_preset.rot_z = self.start_z + mouse_delta
            self.feedback = 'Rotate (Z Axis): '+str(mouse_delta)
        else:
            self.object_preset.rot_x = self.start_x + mouse_y_delta
            self.object_preset.rot_y = self.start_y - mouse_x_delta
            self.object_preset.rot_z = self.start_z
            self.feedback = 'Rotate: X Axis: '+str(mouse_y_delta)+', Y Axis: '+str(-mouse_x_delta)

        if event.type in {'LEFTMOUSE', 'RET'}:
            overlay_info = ''
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.object_preset.rot_x = self.start_x
            self.object_preset.rot_y = self.start_y
            self.object_preset.rot_z = self.start_z
            overlay_info = ''
            return {'CANCELLED'}

        overlay_info = self.feedback
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.feedback = ''
        self.value = ''
        self.constrain = False
        titling_sequence = titling_scene_selected()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        self.scene = titling_sequence.scene
        self.preset = self.scene.quicktitler.current_quicktitle
        if len(self.preset.objects) > self.preset.selected_object:
            self.object_preset = self.preset.objects[self.preset.selected_object]
            self.start_x = self.object_preset.rot_x
            self.start_y = self.object_preset.rot_y
            self.start_z = self.object_preset.rot_z
            object_name = self.object_preset.internal_name
            if object_name in self.scene.objects:
                self.title_object = self.scene.objects[object_name]
                self.mouse_scale = 2
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

        return {'CANCELLED'}


class QuickTitlingScale(bpy.types.Operator):
    #Operator for scaling title elements in the preview area
    bl_idname = 'quicktitle.scale'
    bl_label = "Scale Title Object"

    feedback = ''
    value = ''
    constrain = False
    mouse_x = 0
    mouse_y = 0
    title_object = None
    object_preset = None
    scene = None
    preset = None
    start_scale = 1
    start_x = 1
    start_y = 1
    start_z = 0
    mouse_scale = 500

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                return True
        return False

    def modal(self, context, event):
        global overlay_info
        if event.value == 'PRESS':
            self.value = add_to_value(self.value, event.type)
        if event.type == 'X' and event.value == 'PRESS':
            if self.constrain == 'X':
                self.constrain = False
            else:
                self.constrain = 'X'
        if event.type == 'Y' and event.value == 'PRESS':
            if self.constrain == 'Y':
                self.constrain = False
            else:
                self.constrain = 'Y'
        if event.type == 'Z' and event.value == 'PRESS':
            if self.constrain == 'Z':
                self.constrain = False
            else:
                self.constrain = 'Z'
        mouse_x_delta = -(self.mouse_x - event.mouse_x) / self.mouse_scale
        mouse_y_delta = -(self.mouse_y - event.mouse_y) / self.mouse_scale
        mouse_delta = (mouse_x_delta + mouse_y_delta) / 2
        if event.shift:
            mouse_delta = mouse_delta / 4
        scaler = abs(1 + mouse_delta)
        if self.value:
            try:
                float_value = abs(float(self.value))
                scaler = float_value
            except:
                pass
        if self.constrain == 'X':
            self.feedback = 'Scale X (Width): '+str(scaler)
            self.object_preset.scale = self.start_scale
            self.object_preset.width = self.start_x * scaler
            self.object_preset.height = self.start_y
            self.object_preset.extrude = self.start_z
        elif self.constrain == 'Y':
            self.feedback = 'Scale Y (Height): '+str(scaler)
            self.object_preset.scale = self.start_scale
            self.object_preset.width = self.start_x
            self.object_preset.height = self.start_y * scaler
            self.object_preset.extrude = self.start_z
        elif self.constrain == 'Z':
            self.feedback = 'Scale Z (Extrude): '+str(scaler)
            self.object_preset.scale = self.start_scale
            self.object_preset.width = self.start_x
            self.object_preset.height = self.start_y
            self.object_preset.extrude = self.start_z + scaler
        else:
            self.feedback = 'Scale: '+str(scaler)
            self.object_preset.scale = self.start_scale * scaler
            self.object_preset.width = self.start_x
            self.object_preset.height = self.start_y
            self.object_preset.extrude = self.start_z

        if event.type in {'LEFTMOUSE', 'RET'}:
            overlay_info = ''
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            self.object_preset.scale = self.start_scale
            self.object_preset.width = self.start_x
            self.object_preset.height = self.start_y
            self.object_preset.extrude = self.start_z
            overlay_info = ''
            return {'CANCELLED'}

        overlay_info = self.feedback
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.feedback = ''
        self.value = ''
        self.constrain = False
        titling_sequence = titling_scene_selected()
        self.mouse_x = event.mouse_x
        self.mouse_y = event.mouse_y
        self.scene = titling_sequence.scene
        self.preset = self.scene.quicktitler.current_quicktitle
        if len(self.preset.objects) > self.preset.selected_object:
            self.object_preset = self.preset.objects[self.preset.selected_object]
            self.start_scale = self.object_preset.scale
            self.start_x = self.object_preset.width
            self.start_y = self.object_preset.height
            self.start_z = self.object_preset.extrude
            object_name = self.object_preset.internal_name
            if object_name in self.scene.objects:
                self.title_object = self.scene.objects[object_name]
                self.mouse_scale = 40
                context.window_manager.modal_handler_add(self)
                return {'RUNNING_MODAL'}

        return {'CANCELLED'}


class QuickTitlingSelect(bpy.types.Operator):
    bl_idname = 'quicktitle.select'
    bl_label = 'Select Title Object'

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                return True
        return False

    def invoke(self, context, event):
        quicktitle_sequence = titling_scene_selected()
        scene = quicktitle_sequence.scene
        render_x = scene.render.resolution_x
        mouse_x = event.mouse_region_x
        mouse_y = event.mouse_region_y
        loc_x, loc_y = context.region.view2d.region_to_view(mouse_x, mouse_y)
        x = (loc_x / render_x) * 2
        y = (loc_y / render_x) * 2
        title_object = object_at_location(scene, x, y)
        if title_object:
            title_object_presets = scene.quicktitler.current_quicktitle.objects
            for index, object_preset in enumerate(title_object_presets):
                if object_preset.internal_name == title_object.name:
                    scene.quicktitler.current_quicktitle.selected_object = index
                    #quicktitle_autoupdate()
                    break
        return {'FINISHED'}


class QuickTitlingAddObject(bpy.types.Menu):
    bl_idname = 'QUICKTITLING_MT_add_object_menu'
    bl_label = 'Add Title Object'

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                return True
        return False

    def draw(self, context):
        layout = self.layout
        quicktitle_sequence = titling_scene_selected()
        quicktitle_preset = current_quicktitle(quicktitle_sequence)
        preset_objects = quicktitle_preset.objects
        current_object_index = quicktitle_preset.selected_object
        if len(preset_objects) >= current_object_index + 1:
            current_object = preset_objects[current_object_index]
        else:
            current_object = None

        layout.operator('quicktitler.add_object', text='Text', icon=quicktitle_object_icon('TEXT')).type = 'TEXT'
        layout.operator('quicktitler.add_object', text='Image', icon=quicktitle_object_icon('IMAGE')).type = 'IMAGE'
        layout.operator('quicktitler.add_object', text='Box', icon=quicktitle_object_icon('BOX')).type = 'BOX'
        layout.operator('quicktitler.add_object', text='Circle', icon=quicktitle_object_icon('CIRCLE')).type = 'CIRCLE'
        if current_object:
            layout.operator('quicktitler.add_object', text='Duplicate Selected').type = 'DUPLICATE'


class QuickTitlingDeleteMenu(bpy.types.Menu):
    bl_idname = 'QUICKTITLING_MT_delete_menu'
    bl_label = 'Delete Selected Title Object'

    @classmethod
    def poll(cls, context):
        quicktitle_sequence = titling_scene_selected()
        if quicktitle_sequence:
            frame = bpy.context.scene.frame_current
            if frame >= quicktitle_sequence.frame_final_start and frame <= quicktitle_sequence.frame_final_end:
                preset = quicktitle_sequence.scene.quicktitler.current_quicktitle
                if len(preset.objects) > preset.selected_object:
                    return True
        return False

    def draw(self, context):
        layout = self.layout
        quicktitle_sequence = titling_scene_selected()
        preset = quicktitle_sequence.scene.quicktitler.current_quicktitle
        to_delete = preset.selected_object
        layout.operator('quicktitler.delete_object', text='Delete Selected').index = to_delete


def add_to_value(value, character):
    if character in ['ZERO', 'NUMPAD_0']:
        value = value + '0'
    if character in ['ONE', 'NUMPAD_1']:
        value = value + '1'
    if character in ['TWO', 'NUMPAD_2']:
        value = value + '2'
    if character in ['THREE', 'NUMPAD_3']:
        value = value + '3'
    if character in ['FOUR', 'NUMPAD_4']:
        value = value + '4'
    if character in ['FIVE', 'NUMPAD_5']:
        value = value + '5'
    if character in ['SIX', 'NUMPAD_6']:
        value = value + '6'
    if character in ['SEVEN', 'NUMPAD_7']:
        value = value + '7'
    if character in ['EIGHT', 'NUMPAD_8']:
        value = value + '8'
    if character in ['NINE', 'NUMPAD_9']:
        value = value + '9'
    if character in ['PERIOD', 'NUMPAD_PERIOD']:
        if '.' not in value:
            value = value + '.'
    if character in ['MINUS', 'NUMPAD_MINUS']:
        if '-' in value:
            value = value[1:]
        else:
            value = '-' + value
    if character == 'BACK_SPACE':
        value = value[:-1]
    return value


def add_keymap():
    global keymap
    if keymap is not None:
        remove_keymap()
        keymapitems = keymap.keymap_items
        for keymapitem in keymapitems:
            #Iterate through keymaps and delete old shortcuts
            if keymapitem.type in ['G', 'R', 'S', 'LEFTMOUSE', 'A', 'X', 'DEL', 'L', 'PAGE_UP', 'PAGE_DOWN']:
                keymapitems.remove(keymapitem)
        keymapitems.new('quicktitle.grab', 'G', 'PRESS')
        keymapitems.new('quicktitle.rotate', 'R', 'PRESS')
        keymapitems.new('quicktitle.scale', 'S', 'PRESS')
        keymapitems.new('quicktitle.select', 'LEFTMOUSE', 'PRESS')
        add_menu = keymapitems.new('wm.call_menu', 'A', 'PRESS', shift=True)
        add_menu.properties.name = 'QUICKTITLING_MT_add_object_menu'
        delete_menu = keymapitems.new('wm.call_menu', 'X', 'PRESS')
        delete_menu.properties.name = 'QUICKTITLING_MT_delete_menu'
        delete_menu2 = keymapitems.new('wm.call_menu', 'DEL', 'PRESS')
        delete_menu2.properties.name = 'QUICKTITLING_MT_delete_menu'
        grab_lamp = keymapitems.new('quicktitle.grab', 'L', 'PRESS')
        grab_lamp.properties.lamp = True
        current_up = keymapitems.new('quicktitler.object_up', 'PAGE_UP', 'PRESS')
        current_up.properties.current = True
        current_down = keymapitems.new('quicktitler.object_down', 'PAGE_DOWN', 'PRESS')
        current_down.properties.current = True


def remove_keymap():
    global keymap
    if keymap is not None:
        keymapitems = keymap.keymap_items
        for keymapitem in keymapitems:
            #Iterate through keymaps and delete old shortcuts
            if keymapitem.type in ['G', 'R', 'S', 'LEFTMOUSE', 'A', 'X', 'DEL', 'L', 'PAGE_UP', 'PAGE_DOWN']:
                keymapitems.remove(keymapitem)


def draw_preset_add_menu(self, context):
    layout = self.layout
    layout.menu('QUICKTITLING_MT_preset_menu_add', text='QuickTitle')


classes = [QuickTitlingGrab, QuickTitleAnimation, QuickTitleObject, QuickTitle, QUICKTITLING_UL_ObjectListItem,
           QUICKTITLING_UL_AnimationListItem, QUICKTITLING_PT_Panel, QuickTitlingSavePreset, QuickTitlingReplaceWithImage,
           QuickTitlingObjectMoveUp, QuickTitlingObjectMoveDown, QuickTitlingObjectAdd, QuickTitlingObjectSelect,
           QuickTitlingObjectDelete, QuickTitlingAnimationApply, QuickTitlingAnimationAdd, QuickTitlingAnimationDelete,
           QuickTitlingAnimationMenu, QuickTitlingPresetDelete, QuickTitlingPresetExport, QuickTitlingPresetImport,
           QuickTitlingPresetMenu, QuickTitlingPresetSelect, QuickTitlingPresetLoad, QuickTitlingLoadFont,
           QuickTitlingFontMenu, QuickTitlingChangeFont, QuickTitlingMaterialMenu, QuickTitlingChangeMaterial,
           QuickTitlingCreate, QuickTitleSettings, QuickTitlingRotate, QuickTitlingScale, QuickTitlingSelect,
           QuickTitlingAddObject, QuickTitlingDeleteMenu, QuickTitlingPresetSelectAdd, QuickTitlingPresetMenuAdd,
           QuickTitlingNewMaterial]


def register():
    #Register classes
    for cls in classes:
        bpy.utils.register_class(cls)

    #Group properties
    bpy.types.Scene.quicktitler = bpy.props.PointerProperty(type=QuickTitleSettings)

    global keymap
    #Register shortcuts
    if bpy.context.window_manager.keyconfigs.addon:
        keymaps = bpy.context.window_manager.keyconfigs.addon.keymaps
        keymap = keymaps.new(name='SequencerPreview', space_type='SEQUENCE_EDITOR', region_type='WINDOW')

        second_keymap = keymaps.new(name='Sequencer', space_type='SEQUENCE_EDITOR', region_type='WINDOW')
        add_menu = second_keymap.keymap_items.new('wm.call_menu', 'T', 'PRESS', shift=True)
        add_menu.properties.name = 'QUICKTITLING_MT_preset_menu_add'
    bpy.types.SEQUENCER_MT_add.append(draw_preset_add_menu)
    #add_keymap()


def unregister():
    #Unregister classes
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    #keymap = bpy.context.window_manager.keyconfigs.addon.keymaps['SequencerPreview']
    remove_keymap()


if __name__ == "__main__":
    register()
