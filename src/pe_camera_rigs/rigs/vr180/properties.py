import bpy

class PE_VR180RigSettings(bpy.types.PropertyGroup):
    """Rig-specific settings for the VR180 camera rig controller."""
    ipd: bpy.props.FloatProperty(
        name="IPD",
        description="Interpupillary distance (stereo separation)",
        default=64.0,
        min=0.0,
        max=120.0,
        subtype='DISTANCE',
        unit='LENGTH'
    )

class PE_VR180SceneSettings(bpy.types.PropertyGroup):
    """Scene-level settings for the VR180 workflow."""

    # -- IPD initial setting --
    ipd: bpy.props.FloatProperty(
        name="IPD",
        description="Initial Interpupillary distance (stereo separation)",
        default=64.0,
        min=0.0,
        max=120.0,
        subtype='DISTANCE',
        unit='LENGTH'
    )

    # -- Resolution Presets --
    resolution_preset: bpy.props.EnumProperty(
        name="Resolution Preset",
        items=[
            ('CUSTOM', "Custom", "Use custom resolution settings"),
            ('YOUTUBE_4K', "YouTube 4K (3840x1920)", "Standard 4K 360/VR resolution"),
            ('YOUTUBE_5_7K', "YouTube 5.7K (5760x2880)", "Common high-res VR180"),
            ('YOUTUBE_8K', "YouTube 8K (7680x3840)", "Highest resolution for YouTube VR"),
        ],
        default='YOUTUBE_5_7K',
        description="Choose a common resolution preset for YouTube VR. This is the combined SBS resolution."
    )
    resolution_x: bpy.props.IntProperty(
        name="Resolution X",
        subtype='PIXEL',
        default=5760,
        min=1, max=8192,
        description="Horizontal resolution for the combined Side-by-Side (SBS) image."
    )
    resolution_y: bpy.props.IntProperty(
        name="Resolution Y",
        subtype='PIXEL',
        default=2880,
        min=1, max=4096,
        description="Vertical resolution for the combined Side-by-Side (SBS) image."
    )

    # -- Render Quality --
    render_quality: bpy.props.EnumProperty(
        name="Render Quality",
        items=[
            ('PREVIEW', "Preview", "Lower samples for faster feedback"),
            ('PRODUCTION', "Production", "Balanced quality and render time"),
            ('FINAL', "Final", "High samples for best quality"),
        ],
        default='PRODUCTION',
        description="Sets the Cycles render samples and other quality-related settings."
    )

    # -- Step 1 Settings (Lighting, Cyclorama, Reference - Initial values for operators) --
    lighting_preset: bpy.props.EnumProperty(
        name="Lighting Preset",
        items=[
            ('NONE', "None", "No lights added"),
            ('3POINT_STUDIO', "3-Point (Studio)", "Professional 3-point studio lighting"),
            ('3POINT_OUTDOOR', "3-Point (Outdoor)", "Outdoor 3-point with sun"),
            # ... more presets could go here
        ],
        default='3POINT_STUDIO',
        description="Select a lighting setup to automatically add to the scene."
    )

    include_cyclorama: bpy.props.BoolProperty(
        name="Include Procedural Cyclorama",
        default=True,
        description="Generate a procedural cyclorama stage for the background."
    )
    cyclorama_size: bpy.props.EnumProperty(
        name="Cyclorama Size",
        items=[
            ('SMALL', "Small (10m)", "10x10m floor"),
            ('MEDIUM', "Medium (20m)", "20x20m floor"),
            ('LARGE', "Large (30m)", "30x30m floor"),
        ],
        default='MEDIUM',
        description="Size of the procedural cyclorama."
    )
    cyclorama_color: bpy.props.EnumProperty(
        name="Cyclorama Color",
        items=[
            ('WHITE', "White", "High-key, bright"),
            ('GRAY', "Neutral Gray", "Balanced"),
            ('BLACK', "Black", "Low-key, dramatic"),
        ],
        default='GRAY',
        description="Color of the procedural cyclorama material."
    )

    include_reference: bpy.props.BoolProperty(
        name="Include Person-Scale Reference",
        default=True,
        description="Generate a 1.8m tall capsule for scale reference."
    )

    # -- Output Settings --
    output_path: bpy.props.StringProperty(
        name="Output Path",
        subtype='DIR_PATH',
        default="//renders/vr180/",
        description="Directory to save EXR sequences and final video. Use '//' for project root."
    )

    # -- Step 4 Settings --
    auto_inject_metadata: bpy.props.BoolProperty(
        name="Auto-inject VR180 Metadata",
        default=True,
        description="Automatically inject spatial VR180 metadata into the final MP4 for YouTube."
    )
    verify_metadata: bpy.props.BoolProperty(
        name="Verify Metadata after Render",
        default=True,
        description="Check if metadata injection was successful after rendering."
    )
    cleanup_sequences: bpy.props.BoolProperty(
        name="Cleanup EXR Sequences",
        default=False,
        description="Delete the intermediate EXR sequences after the final MP4 is rendered and metadata injected."
    )

