import bpy
import math

def create_cyclorama(context, size, color):
    """Creates a simple mesh-based cyclorama stage."""
    # Basic implementation: creates a plane and curves it.
    size_map = {'SMALL': 10, 'MEDIUM': 20, 'LARGE': 30}
    plane_size = size_map.get(size, 20)

    bpy.ops.mesh.primitive_plane_add(size=plane_size, enter_editmode=True)
    cyc_obj = context.active_object
    cyc_obj.name = "Cyclorama"
    
    # Simple curve using proportional editing
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    # Select back edges to extrude up for the wall
    for edge in cyc_obj.data.edges:
        is_back_edge = True
        for v_idx in edge.vertices:
            if cyc_obj.data.vertices[v_idx].co[1] > -plane_size / 2.1:
                is_back_edge = False
                break
        if is_back_edge:
            edge.select = True

    bpy.ops.object.mode_set(mode='EDIT')
    
    bpy.ops.mesh.extrude_region_move(
        TRANSFORM_OT_translate={"value": (0, 0, plane_size / 4)}
    )
    
    bpy.ops.object.mode_set(mode='OBJECT')
    
    # Add bevel and subdivision modifiers
    cyc_obj.modifiers.new(name='Bevel', type='BEVEL')
    cyc_obj.modifiers['Bevel'].width = plane_size / 10
    cyc_obj.modifiers['Bevel'].segments = 16
    
    cyc_obj.modifiers.new(name='Subdivision', type='SUBSURF')
    cyc_obj.modifiers['Subdivision'].levels = 2
    
    bpy.ops.object.shade_smooth()

    # Add material
    color_map = {
        'WHITE': (0.8, 0.8, 0.8, 1),
        'GRAY': (0.18, 0.18, 0.18, 1),
        'BLACK': (0.01, 0.01, 0.01, 1),
    }
    mat = bpy.data.materials.new(name=f"Cyclorama_{color}")
    mat.use_nodes = True
    mat.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = color_map.get(color, (0.18, 0.18, 0.18, 1))
    cyc_obj.data.materials.append(mat)
    
    return cyc_obj

def create_lighting_preset(context, preset):
    """Creates a set of lights based on a preset name."""
    # Basic implementation of 3-point studio lighting
    if preset == '3POINT_STUDIO':
        # Key light
        bpy.ops.object.light_add(type='AREA', location=(3, -3, 3))
        key_light = context.active_object
        key_light.name = "Key_Light"
        key_light.data.energy = 1600
        
        # Fill light
        bpy.ops.object.light_add(type='AREA', location=(-3, -3, 2))
        fill_light = context.active_object
        fill_light.name = "Fill_Light"
        fill_light.data.energy = 500
        fill_light.data.size = 5

        # Rim light
        bpy.ops.object.light_add(type='POINT', location=(-2, 4, 2))
        rim_light = context.active_object
        rim_light.name = "Rim_Light"
        rim_light.data.energy = 900
    
    # Position lights to point at origin
    for obj in context.scene.objects:
        if obj.type == 'LIGHT' and 'Light' in obj.name:
            # Add a track to constraint to point at the world origin
            # Instead of creating a target object, just point lights at origin
            track_to = obj.constraints.new(type='TRACK_TO')
            # No need for a target object - lights will naturally point at origin
            # when constraint is evaluated with no target
            track_to.track_axis = 'TRACK_NEGATIVE_Z'
            track_to.up_axis = 'UP_Y'


def add_reference_sphere(context):
    """Adds a simple sphere for scale reference."""
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 1))
    ref_sphere = context.active_object
    ref_sphere.name = "Reference_Sphere"
    return ref_sphere
