"""
Blender-specific utility functions for the CGT Camera Rigs addon.

Provides helpers for GPU detection, render optimization, and other
Blender API convenience functions.
"""

import bpy
import os
from pathlib import Path


def detect_and_enable_gpu():
    """
    Detect and enable GPU rendering if available.

    Attempts to find and enable GPU compute devices (CUDA, OptiX, HIP, Metal)
    for Cycles rendering. This function is safe to call even if no GPU is
    available - it will simply return None without errors.

    Returns:
        str: Name of the enabled GPU device, or None if no GPU found

    Example:
        >>> gpu_name = detect_and_enable_gpu()
        >>> if gpu_name:
        ...     print(f"GPU rendering enabled: {gpu_name}")
        ... else:
        ...     print("No GPU available, using CPU")
    """
    try:
        # Get Cycles preferences
        prefs = bpy.context.preferences
        cycles_prefs = prefs.addons['cycles'].preferences

        # Refresh device list to detect new hardware
        cycles_prefs.refresh_devices()
        devices = cycles_prefs.devices

        # Try to find and enable a GPU device
        for device in devices:
            if device.type in {'CUDA', 'OPTIX', 'HIP', 'METAL', 'ONEAPI'}:
                device.use = True
                bpy.context.scene.cycles.device = 'GPU'
                return device.name

        # No GPU found
        return None

    except (AttributeError, KeyError):
        # Cycles addon not available or preferences not accessible
        return None


def validate_output_path(filepath, scene=None):
    """
    Validates that a render output path is writable and has sufficient disk space.

    Args:
        filepath (str): The render output path to validate (supports Blender path tokens like ///)
        scene (bpy.types.Scene, optional): Scene to use for path expansion. Defaults to current scene.

    Returns:
        tuple: (is_valid: bool, error_message: str)
            - is_valid: True if path is writable, False otherwise
            - error_message: Empty string if valid, descriptive error if invalid

    Example:
        >>> valid, error = validate_output_path("//renders/output.png")
        >>> if not valid:
        ...     print(f"Invalid path: {error}")
    """
    if scene is None:
        scene = bpy.context.scene

    try:
        # Expand Blender path tokens (///, //, etc.)
        expanded = bpy.path.abspath(filepath, start=scene.render.filepath if scene else None)
        path = Path(expanded)

        # Check parent directory exists
        parent = path.parent
        if not parent.exists():
            return False, f"Directory does not exist: {parent}"

        # Check directory is writable
        if not os.access(parent, os.W_OK):
            return False, f"Directory not writable: {parent}"

        # Check disk space (warn if less than 1GB available)
        try:
            stat = os.statvfs(parent)
            free_space_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
            if free_space_gb < 1.0:
                return False, f"Low disk space: {free_space_gb:.1f}GB available (recommend at least 1GB)"
        except (AttributeError, OSError):
            # statvfs not available on Windows, skip disk space check
            pass

        return True, ""

    except (OSError, PermissionError) as e:
        return False, f"Cannot access path: {str(e)}"


def get_active_camera_or_create(context):
    """
    Get the active scene camera, or create one if none exists.

    Args:
        context: Blender context

    Returns:
        bpy.types.Object: The active camera object
    """
    if context.scene.camera:
        return context.scene.camera

    # No camera exists, create a default one
    cam_data = bpy.data.cameras.new("Camera")
    cam_obj = bpy.data.objects.new("Camera", cam_data)
    context.collection.objects.link(cam_obj)
    context.scene.camera = cam_obj

    return cam_obj


def safe_object_delete(obj, do_unlink=True):
    """
    Safely delete an object with existence checking.

    Args:
        obj (bpy.types.Object): Object to delete (can be None)
        do_unlink (bool): Whether to unlink from all collections

    Returns:
        bool: True if deleted, False if object was None or already deleted
    """
    if obj and obj.name in bpy.data.objects:
        bpy.data.objects.remove(obj, do_unlink=do_unlink)
        return True
    return False


def set_modifier_input(modifier, socket_name, value):
    """
    Safely set a Geometry Nodes modifier input by socket name.

    This function provides a robust way to set modifier inputs by name
    rather than index, making it more maintainable when node groups change.

    Args:
        modifier: The Geometry Nodes modifier
        socket_name (str): Name of the input socket
        value: Value to set (type depends on socket)

    Returns:
        bool: True if successful, False otherwise

    Example:
        >>> modifier = obj.modifiers.get('GeometryNodes')
        >>> success = set_modifier_input(modifier, 'Radius', 2.5)
        >>> if success:
        ...     print("Modifier input updated")
    """
    # Validate modifier has node_group
    if not hasattr(modifier, 'node_group') or not modifier.node_group:
        return False

    # Find socket by name (more robust than index)
    for input_socket in modifier.node_group.inputs:
        if input_socket.name == socket_name:
            modifier[input_socket.identifier] = value
            return True
    return False
