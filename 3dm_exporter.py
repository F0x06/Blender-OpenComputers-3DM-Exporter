#
# Blender-OpenComputers-3DM-Exporter - Blender Minecraft OpenComputers 3DM (print3d) Exporter
#
# Copyright (c) 2016 Kevin Velickovic
#
#
# Author(s):
#
#      Kevin Velickovic <k.velickovic@gmail.com>
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
# Additional Terms:
#
#      You are required to preserve legal notices and author attributions in
#      that material or in the Appropriate Legal Notices displayed by works
#      containing it.
#

# Imports
import bpy
from bpy.props import ( StringProperty, BoolProperty, IntProperty )

# Plugin details
bl_info = {
    'name': 'OpenComputers 3DM Exporter',
    'author': 'Kevin Velickovic (F0x06)',
    'version': (1, 2, 0),
    'blender': (2, 76, 0),
    'location': 'Scene properties > Minecarft OpenComputers 3D exporter',
    'description': 'Export voxel model to OpenComputers 3DM format',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'support': 'COMMUNITY',
    'category': 'Exporter'}
    
# Function to initialize properties
def initProps():
    
    # Object export settings
    bpy.types.Scene.f0x_3dm_tint_param = BoolProperty(
        name="Export tints ( diffuse color )",
        description="",
        default = True )  
    bpy.types.Scene.f0x_3dm_export_all_layers_param = BoolProperty(
        name="Export all layers",
        description="",
        default = False )        

    # 3DM model export settings
    bpy.types.Scene.f0x_3dm_label_param = StringProperty(
        name="Label",
        default = "" )
    bpy.types.Scene.f0x_3dm_tooltip_param = StringProperty(
        name="Tooltip",
        default = "" )  
    bpy.types.Scene.f0x_3dm_lightlevel_param = IntProperty(
        name="Light level",
        default = 0,
        min = 0,
        max = 8 )  
    bpy.types.Scene.f0x_3dm_emitredstone_param = BoolProperty(
        name="Emit redstone",
        default = False )  
    bpy.types.Scene.f0x_3dm_buttonmode_param = BoolProperty(
        name="Button mode",
        default = False )  
    bpy.types.Scene.f0x_3dm_collidable_param = BoolProperty(
        name="Collidable",
        default = True )  
        
    # Object properties
    bpy.types.Object.f0x_3dm_state_prop = BoolProperty(
                name="Display only when on",
                default = False )
                
    # State settings
    bpy.types.Scene.f0x_3dm_state_settings_show_all_param = BoolProperty(
    name="Show all layers",
    description="",
    default = False )     
        
# Function to unload properties
def unloadProps():
    
    # Object export settings
    del bpy.types.Scene.f0x_3dm_tint_param
    del bpy.types.Scene.f0x_3dm_export_all_layers_param

    # 3DM model export settings
    del bpy.types.Scene.f0x_3dm_label_param
    del bpy.types.Scene.f0x_3dm_tooltip_param 
    del bpy.types.Scene.f0x_3dm_lightlevel_param  
    del bpy.types.Scene.f0x_3dm_emitredstone_param 
    del bpy.types.Scene.f0x_3dm_buttonmode_param
    del bpy.types.Scene.f0x_3dm_collidable_param
    
    # Object properties
    del bpy.types.Object.f0x_3dm_state_prop
    
# Function to get all exportable objects
def get_exportables( show_all=False ):

    # Results container
    results = []

    # Iterate over scene objects
    for _obj in bpy.data.objects:

        # Check if object is a cube
        if _obj and _obj.type == 'MESH' and _obj.data.name.startswith("Cube"):

            # Check if object is in the active layer
            if _obj.layers[ bpy.context.scene.active_layer ] or show_all:
                
                # Add result
                results.append( _obj )
                
    return results

# Function to calculate bottom vertex coordinates
def get_bottom_vertex( _obj ):

    # Compute arrays
    x_values = []
    y_values = []
    z_values = []

    # Iterate over object verticles
    for v in _obj.data.vertices:

        # Get verticle world coordinates
        coords = ( _obj.matrix_world * v.co )

        # Append values to compute arrays
        x_values.append( coords[ 0 ] )
        y_values.append( coords[ 1 ] )
        z_values.append( coords[ 2 ] )

    # Build result
    return [
        round( min( x_values ) + 8 ),
        round( min( z_values ) + 0 ),
        round( min( y_values ) + 8 )
    ]

# Function to calculate top vertex coordinates
def get_top_vertex( _obj ):

    # Compute arrays
    x_values = []
    y_values = []
    z_values = []

    # Iterate over object verticles
    for v in _obj.data.vertices:

        # Get verticle world coordinates
        coords = ( _obj.matrix_world * v.co )

        # Append values to compute arrays
        x_values.append( coords[ 0 ] )
        y_values.append( coords[ 1 ] )
        z_values.append( coords[ 2 ] )

    # Build result
    return [
        round( max( x_values ) + 8 ),
        round( max( z_values ) + 0 ),
        round( max( y_values ) + 8 )
    ]

# Function to generate 3DM file
def generate_3dm_file( file_path ):

    # Scene container
    scene = bpy.context.scene

    # Open output file
    with open( file_path, "w" ) as output_file:

        # Write 3DM header
        output_file.write("{\n")
        output_file.write("    label = \"%s\",\n"    % ( scene.f0x_3dm_label_param ) )
        output_file.write("    tooltip = \"%s\",\n"  % ( scene.f0x_3dm_tooltip_param ) )
        output_file.write("    lightLevel = %d,\n"   % ( scene.f0x_3dm_lightlevel_param ) )
        output_file.write("    emitRedstone = %s,\n" % ( "true" if scene.f0x_3dm_emitredstone_param else "false" ) )
        output_file.write("    buttonMode = %s,\n"   % ( "true" if scene.f0x_3dm_buttonmode_param else "false" ) )
        output_file.write("    collidable = %s,\n"   % ( "true" if scene.f0x_3dm_collidable_param else "false" ) )
        
        output_file.write("    shapes={\n")

        # Iterate over scene objects
        for _obj in get_exportables( bpy.context.scene.f0x_3dm_export_all_layers_param ):

            #                   +------+ top_corner_pos
            #                  /      /|
            #                 +------+ |
            #                 |      | +
            #                 |      |/
            # bot_corner_pos  +------+

            # Compute world coordinates of corners and align them to 3DM start position
            bot_corner_pos = get_bottom_vertex( _obj )
            top_corner_pos = get_top_vertex( _obj )
            
            # Tint variable
            object_tint = '0x000000'
            
            # Check if object have material
            if _obj.active_material:
                
                # Check for default diffuse color
                if _obj.active_material.diffuse_color.hsv != (0.0, 0.0, 0.800000011920929):
                    
                    # Get object tint ( diffuse color )
                    object_tint = '0x%02x%02x%02x' % ( round( _obj.active_material.diffuse_color.r * 255.0 ),
                    round( _obj.active_material.diffuse_color.g * 255.0 ),
                    round( _obj.active_material.diffuse_color.b * 255.0 ) )

            # Write block data to 3DM file
            output_file.write("        {%02d, %02d, %02d, %02d, %02d, %02d, texture=\"%s\", tint = %s, state = %s},\n" % (
                bot_corner_pos[0], bot_corner_pos[1], bot_corner_pos[2],
                top_corner_pos[0], top_corner_pos[1], top_corner_pos[2],
                _obj.active_material.name.split( '.' )[ 0 ] if _obj.active_material else "planks_oak",
                object_tint if scene.f0x_3dm_tint_param else '0x000000',
                'true' if _obj.f0x_3dm_state_prop else 'false'
            ))

        # Write footer
        output_file.write("    }\n")
        output_file.write("}\n")

# Class to handle file save dialog and 3DM file generation
class f0x_export_3dm(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.export_3dm"
    bl_label = "Export 3DM file"
    filepath = bpy.props.StringProperty(subtype="FILE_PATH")
    filter_glob = StringProperty(
        default="*.3dm",
        options={'HIDDEN'},
    )

    @classmethod
    def poll(cls, context):
        return ( len( bpy.context.scene.objects ) > 0 )

    def execute(self, context):
        generate_3dm_file( self.filepath )
        return {'FINISHED'}

    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

# Function to get selected object
def get_selected():
    
    # Iterate over scene objects
    for _obj in bpy.data.objects:
        
        # Check if object is valid and selected
        if _obj and _obj.select:
            
            # Return result
            return _obj

# Function to deselect all object
def deselect_all():
    
    # Iterate over scene objects
    for _obj in bpy.data.objects:
        
        # Check if object is valid
        if _obj:
            
            # Deselect object
            _obj.select = False

# Function to find bounding box
def boundingbox_find():

    # Iterate over scene objects
    for _obj in bpy.data.objects:

        # Check if object is a bounding box
        if _obj and "3dm_boundingbox_vtx" in _obj.data.name:

            # Check if object is in the active layer
            if _obj.layers[ bpy.context.scene.active_layer ]:

                # Return object
                return _obj

# Function to add a bounding box
class f0x_boundingbox_add(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.boundingbox_add"
    bl_label = "Add a bounding box"

    @classmethod
    def poll(cls, context):
        return ( boundingbox_find() == None ) and ( bpy.context.mode == 'OBJECT' )

    def execute(self, context):
        
        # Deselect all objects
        deselect_all()
        
        # Create a cube
        bpy.ops.mesh.primitive_cube_add(location=(0,0,8))
        added_cube = get_selected()

        # Cube settings
        added_cube.dimensions = [ 16, 16, 16 ]
        added_cube.draw_type = 'WIRE'
        added_cube.hide_select = True
        added_cube.hide_render = True
        added_cube.name = '3dm_boundingbox'
        added_cube.data.name = '3dm_boundingbox_vtx'

        # Move cube origin
        saved_location = bpy.context.scene.cursor_location.copy()
        bpy.context.scene.cursor_location = ( -8, -8, 0 )
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = saved_location

        # Deselect cube
        added_cube.select = False

        return {'FINISHED'}

# Function to remove a bounding box
class f0x_boundingbox_remove(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.boundingbox_remove"
    bl_label = "Remove a bounding box"

    @classmethod
    def poll(cls, context):
        return ( boundingbox_find() != None ) and ( bpy.context.mode == 'OBJECT' )

    def execute(self, context):

        # Deselect all objects
        deselect_all()

        # Find bounding box
        bbox = boundingbox_find()

        # If there is a bounding box
        if bbox:

            # Remove bounding box
            bbox.hide_select = False
            bbox.select = True
            bpy.ops.object.delete()

        return {'FINISHED'}

# Function to change objects state to on        
class f0x_state_on(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.state_on"
    bl_label = "On"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        # Iterate over scene objects
        for obj in get_exportables( True ):
            
            # Check state
            if obj.f0x_3dm_state_prop:
                
                # Show object
                obj.hide = False
                
            else:
                
                # Hide object
                obj.hide = True
        
        return {'FINISHED'}

# Function to change objects state to off            
class f0x_state_off(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.state_off"
    bl_label = "Off"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):

        # Iterate over scene objects
        for obj in get_exportables( True ):
            
            # Check state
            if obj.f0x_3dm_state_prop:
                
                # Hide object
                obj.hide = True
                
            else:
                
                # Show object
                obj.hide = False

        return {'FINISHED'}

# Function to reset objects state
class f0x_state_reset(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.state_reset"
    bl_label = "Reset"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        # Iterate over scene objects
        for obj in get_exportables( True ):
            
            # Show object
            obj.hide = False
        
        return {'FINISHED'}
        
# Class to handle panel drawing
class MainPanel(bpy.types.Panel):

    # Properties
    bl_label = "OpenComputers 3DM Exporter"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
    
        # Create layout
        layout = self.layout
        
        # Object export settings
        layout.label(text="Object export settings:")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_tint_param")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_export_all_layers_param")
        
        # 3DM model settings
        layout.label(text="3DM model settings:")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_label_param")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_tooltip_param")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_lightlevel_param")
        row = layout.row()
        row.prop(context.scene, "f0x_3dm_emitredstone_param")
        row.prop(context.scene, "f0x_3dm_buttonmode_param")
        row.prop(context.scene, "f0x_3dm_collidable_param")
        row = layout.row()
        
        # State settings
        row.label(text="State settings:")
        row = layout.row()
        row.prop( context.scene, "f0x_3dm_state_settings_show_all_param" )
        box = layout.box()
        row = box.row()
        
        for obj in get_exportables( bpy.context.scene.f0x_3dm_state_settings_show_all_param ):
         
            row.label( obj.name )
            row.prop( obj, "f0x_3dm_state_prop" )
            row = box.row()
        
        # State simulation
        layout.label("State simulation")
        row = layout.row(align=True)
        row.alignment = 'EXPAND'
        row.operator("f0x.state_on")
        row.operator("f0x.state_off")
        row.operator("f0x.state_reset")
        
        # Bounding box
        layout.label(text="Bounding box")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("f0x.boundingbox_add", text = "Add")
        row.operator("f0x.boundingbox_remove", text = "Remove")
        
        # Export
        layout.label(text="Export")
        row = layout.row()
        row.scale_y = 2.0
        row.operator("f0x.export_3dm", text = "Export")

# Function to register module
def register():
    initProps()
    bpy.utils.register_class(f0x_export_3dm)
    bpy.utils.register_class(f0x_boundingbox_add)
    bpy.utils.register_class(f0x_boundingbox_remove)
    bpy.utils.register_class(f0x_state_on)
    bpy.utils.register_class(f0x_state_off)
    bpy.utils.register_class(f0x_state_reset)
    bpy.utils.register_class(MainPanel)

# Function to unregister module
def unregister():
    unloadProps()
    bpy.utils.unregister_class(f0x_export_3dm)
    bpy.utils.unregister_class(f0x_boundingbox_add)
    bpy.utils.unregister_class(f0x_boundingbox_remove)
    bpy.utils.unregister_class(f0x_state_on)
    bpy.utils.unregister_class(f0x_state_off)
    bpy.utils.unregister_class(f0x_state_reset)
    bpy.utils.unregister_class(MainPanel)

# Entry point
if __name__ == "__main__":
    register()
