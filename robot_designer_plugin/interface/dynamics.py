# #####
# This file is part of the RobotDesigner of the Neurorobotics subproject (SP10)
# in the Human Brain Project (HBP).
# It has been forked from the RobotEditor (https://gitlab.com/h2t/roboteditor)
# developed at the Karlsruhe Institute of Technology in the
# High Performance Humanoid Technologies Laboratory (H2T).
# #####

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

# #####
#
# Copyright (c) 2015, Karlsruhe Institute of Technology (KIT)
# Copyright (c) 2016, FZI Forschungszentrum Informatik
#
# Changes:
#   2015:       Stefan Ulbrich (FZI), Gui redesigned
#   2015-01-16: Stefan Ulbrich (FZI), Major refactoring. Integrated into complex plugin framework.
#
# ######

# Blender imports
import bpy

# RobotDesigner imports
from ..operators import dynamics
from . import menus
from .model import check_armature
from ..properties.globals import global_properties
from ..core.gui import InfoBox
from .helpers import getSingleSegment, getSingleObject


def draw(layout, context):
    """
    Draws the user interface for modifying the dynamic properties of a segment.

    :param layout: Current GUI element (e.g., collapsible box, row, etc.)
    :param context: Blender context
    """
    if not check_armature(layout, context):
        return

    settings = layout.row()
    global_properties.display_physics_selection.prop(context.scene, settings)

    box = layout.box()
    box.label("Edit Mass Object")
    infoBox = InfoBox(box)
    row = box.row()

    single_segment = getSingleSegment(context)

    #menus.MassObjectMenu.putMenu(column, context)
    # create_geometry_selection(column, context)
    row = box.column(align=True)

    dynamics.CreatePhysical.place_button(row,infoBox=infoBox)
    dynamics.ComputePhysical.place_button(row,infoBox=infoBox)

    #dynamics.AssignPhysical.place_button(row,infoBox=infoBox)
    #dynamics.DetachPhysical.place_button(row,infoBox=infoBox)

    objs = [ o for o in context.active_object.children if o.RobotEditor.tag=='PHYSICS_FRAME' and o.parent_bone == single_segment.name ]
    print (objs)
    try:
        obj, = objs
        #obj = getSingleObject(context)
        if obj and obj.RobotEditor.tag=="PHYSICS_FRAME":
            frame_name = obj.name
            box = layout.box()
            box.label("Mass properties (" + single_segment.name + ")", icon="MODIFIER")
            frame = bpy.data.objects[frame_name]
            box.prop(frame.RobotEditor.dynamics, "mass")
            box.separator()

            row_t = box.row(align=True)
            row_r = box.row(align=True)

            row_t.prop(bpy.data.objects[frame_name], 'location', text="Translation")
            row_r.prop(bpy.data.objects[frame_name], 'rotation_euler', text="Rotation")

            row0 = box.row(align=True)
            row1 = box.row(align=True)
            row2 = box.row(align=True)
            row3 = box.row(align=True)
            row0.label("Inertia Matrix")
            row1.prop(frame.RobotEditor.dynamics, "inertiaXX")
            row2.prop(frame.RobotEditor.dynamics, "inertiaXY")
            row3.prop(frame.RobotEditor.dynamics, "inertiaXZ")
            row1.prop(frame.RobotEditor.dynamics, "inertiaXY")
            row2.prop(frame.RobotEditor.dynamics, "inertiaYY")
            row3.prop(frame.RobotEditor.dynamics, "inertiaYZ")
            row1.prop(frame.RobotEditor.dynamics, "inertiaXZ")
            row2.prop(frame.RobotEditor.dynamics, "inertiaYZ")
            row3.prop(frame.RobotEditor.dynamics, "inertiaZZ")
    except:
        pass

    infoBox.draw_info()
