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
import bgl
from bpy.props import StringProperty
import mathutils

# Plugin details
bl_info = {
    'name': 'OpenComputers 3DM Exporter',
    'author': 'Kevin Velickovic (F0x06)',
    'version': (0, 1, 0),
    'blender': (2, 76, 0),
    'location': 'Scene properties > Minecarft OpenComputers 3D exporter',
    'description': 'Export voxel model to OpenComputers 3DM format',
    'warning': '',
    'wiki_url': '',
    'tracker_url': '',
    'support': 'COMMUNITY',
    'category': 'Exporter'}

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
def generate_mc3d_file( file_path ):

    # Open output file
    with open( file_path, "w" ) as output_file:

        # Write 3DM header
        output_file.write("{\n")
        output_file.write("    label = \"%s\",\n" % ( bpy.path.display_name_from_filepath( bpy.data.filepath ) ) )
        output_file.write("    shapes={\n")

        # Iterate over scene objects
        for _obj in bpy.data.objects:

            # Check if object is a cube
            if _obj and not _obj.hide and _obj.type == 'MESH' and _obj.data.name.startswith("Cube"):

                # Check if object is in the active layer
                if _obj.layers[ bpy.context.scene.active_layer ]:

                    #                   +------+ top_corner_pos
                    #                  /      /|
                    #                 +------+ |
                    #                 |      | +
                    #                 |      |/
                    # bot_corner_pos  +------+

                    # Compute world coordinates of corners and align them to 3DM start position
                    bot_corner_pos = get_bottom_vertex( _obj )
                    top_corner_pos = get_top_vertex( _obj )

                    # Write block data to 3DM file
                    output_file.write("        {%02d, %02d, %02d, %02d, %02d, %02d, texture=\"%s\"},\n" % (
                        bot_corner_pos[0], bot_corner_pos[1], bot_corner_pos[2],
                        top_corner_pos[0], top_corner_pos[1], top_corner_pos[2],
                        _obj.active_material.name if _obj.active_material else "planks_oak"
                    ))

        # Write footer
        output_file.write("    }\n")
        output_file.write("}\n")

# Class to handle file save dialog and 3DM file generation
class f0x_export_mc3d(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.export_mc3d"
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
        generate_mc3d_file( self.filepath )
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

# Function to find bounding box
def bb_find():

    # Iterate over scene objects
    for _obj in bpy.data.objects:

        # Check if object is a bounding box
        if _obj and "3dm_boundingbox_vtx" in _obj.data.name:

            # Check if object is in the active layer
            if _obj.layers[ bpy.context.scene.active_layer ]:

                # Return object
                return _obj

# Function to add a bounding box
class f0x_bb_add(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.bb_add"
    bl_label = "Add a bounding box"

    @classmethod
    def poll(cls, context):
        return ( bb_find() == None )

    def execute(self, context):

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
class f0x_bb_remove(bpy.types.Operator):

    # Properties
    bl_idname = "f0x.bb_remove"
    bl_label = "Remove a bounding box"

    @classmethod
    def poll(cls, context):
        return ( bb_find() != None )

    def execute(self, context):

        # Find bounding box
        bbox = bb_find()

        # If there is a bounding box
        if bbox:

            # Remove bounding box
            bbox.hide_select = False
            bbox.select = True
            bpy.ops.object.delete()

        return {'FINISHED'}

# Class to handle panel drawing
class LayoutDemoPanel(bpy.types.Panel):

    # Properties
    bl_label = "OpenComputers 3DM Exporter"
    bl_idname = "SCENE_PT_layout"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    def draw(self, context):
        layout = self.layout

        layout.label(text="Export")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("f0x.export_mc3d", text = "Export")

        layout.label(text="Bounding box")
        row = layout.row()
        row.scale_y = 1.0
        row.operator("f0x.bb_add", text = "Add")
        row.operator("f0x.bb_remove", text = "Remove")


# Function to register module
def register():
    bpy.utils.register_class(f0x_export_mc3d)
    bpy.utils.register_class(f0x_bb_add)
    bpy.utils.register_class(f0x_bb_remove)
    bpy.utils.register_class(LayoutDemoPanel)

# Function to unregister module
def unregister():
    bpy.utils.unregister_class(f0x_export_mc3d)
    bpy.utils.unregister_class(f0x_bb_add)
    bpy.utils.unregister_class(f0x_bb_remove)
    bpy.utils.unregister_class(LayoutDemoPanel)

# Entry point
if __name__ == "__main__":
    register()
