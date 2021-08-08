import bpy
from bpy.types import Menu
from bpy.types import Operator


bl_info = {
    "name": "Block-In Pie Menu",
    "description": "Pie Menu for Block-In Prototyping",
    "author": "Roderick Constance",
    "version": (0, 1, 0),
    "blender": (2, 80, 0),
    "warning": "",
    "support": "TESTING",
    "category": "User Interface"
}

# START Pie Menus --->


class OriginTo(Menu):
    """Set Origin To"""
    bl_label = "Origin To"
    bl_idname = "origin.to"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Origin To")
        layout.separator()
        layout.operator(OriginToCursor.bl_idname, text="3D Cursor", icon='PIVOT_CURSOR')
        layout.operator(OriginToGeom.bl_idname, text="Geometry", icon='MESH_CUBE')


class PivotPoint(Menu):
    """Set Pivot Point"""
    bl_label = "Pivot Point"
    bl_idname = "pivot.point"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Pivot Point")
        layout.separator()
        layout.operator(PivotPointCursor.bl_idname, text="3D Cursor", icon='PIVOT_CURSOR')
        layout.operator(PivotPointIndivOrigin.bl_idname, text="Individual Origin", icon='PIVOT_INDIVIDUAL')


class SelectMode(Menu):
    """Set Selection Mode"""
    bl_label = "Select Mode"
    bl_idname = "select.mode"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Selection Mode")
        layout.separator()
        layout.operator(SelectModeVertex.bl_idname, text="Vertex", icon='VERTEXSEL')
        layout.operator(SelectModeEdge.bl_idname, text="Edge", icon='EDGESEL')
        layout.operator(SelectModeFace.bl_idname, text="Face", icon='FACESEL')
        layout.operator(SelectModeVEF.bl_idname, text="Vertex/Edges/Faces", icon='OBJECT_DATA')


class SelectType(Menu):
    """Set Select All Type"""
    bl_label = "Select Type"
    bl_idname = "select.type"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Selection Type")
        layout.separator()
        layout.operator(SelectTypeMesh.bl_idname, text="Mesh", icon='MESH_CUBE')
        layout.operator(SelectTypeEmpty.bl_idname, text="Empty", icon='OUTLINER_DATA_EMPTY')
        layout.operator(SelectTypeLight.bl_idname, text="Light", icon='LIGHT_DATA')
        layout.operator(SelectTypeCamera.bl_idname, text="Camera", icon='CAMERA_DATA')


class VIEW3D_MT_PIE_template(Menu):
    """Block-In Pie Menu"""
    bl_label = "Block-In Pie Menu"
    bl_idname = "block_in.pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # WEST
        pie.operator(ViewWireframe.bl_idname, text="View Wireframe", icon='SHADING_WIRE')
        # EAST
        pie.operator(ViewSolid.bl_idname, text="View Solid", icon='SHADING_SOLID')
        # SOUTH
        if context.mode == 'EDIT_MESH':
            pie.menu(SelectMode.bl_idname, text="Selection Mode", icon='VERTEXSEL')
        elif context.mode == 'OBJECT':
            pie.menu(SelectType.bl_idname, text="Selection Type", icon='SELECT_SET')
        # NORTH
        if context.mode == 'EDIT_MESH':
            pie.operator(CenterViewCursor.bl_idname, text="Center View Cursor", icon='TRACKER')
        elif context.mode == 'OBJECT':
            pie.operator(AlignObjs.bl_idname, text="Align Objects", icon='MOD_ARRAY')
        # NORTHWEST
        pie.menu(OriginTo.bl_idname, text="Origin To")
        # NORTHEAST
        pie.menu(PivotPoint.bl_idname, text="Pivot Point")
        # SOUTHWEST
        pie.operator(SelectAll.bl_idname, text="Select All Toggle")
        # SOUTHEAST
        pie.operator(SelectInvert.bl_idname, text="Invert Selection")


# <--- END Pie menus
# START Operators --->

class ViewWireframe(Operator):
    """View Wireframe"""
    bl_idname = "view.wireframe"
    bl_label = "ViewWireframe"

    def execute(self, context):
        bpy.context.space_data.shading.type = 'WIREFRAME'
        return {'FINISHED'}


class ViewSolid(Operator):
    """View Solid"""
    bl_idname = "view.solid"
    bl_label = "ViewSolid"

    def execute(self, context):
        bpy.context.space_data.shading.type = 'SOLID'
        return {'FINISHED'}


class OriginToCursor(Operator):
    """Origin to Cursor"""
    bl_idname = "origin_to.cursor"
    bl_label = "OriginToCursor"

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.pivot2cursor_edit()
        elif context.mode == 'OBJECT':
            bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}


class OriginToGeom(Operator):
    """Origin to Geometry"""
    bl_idname = "origin_to.geom"
    bl_label = "OriginToGeom"

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
            bpy.ops.object.editmode_toggle()
            bpy.ops.object.origintogeometry_edit()
        elif context.mode == 'OBJECT':
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
        return {'FINISHED'}


class CenterViewCursor(Operator):
    """Center View on Cursor"""
    bl_idname = "center_view.cursor"
    bl_label = "CenterViewCursor"

    def execute(self, context):
        bpy.ops.view3d.view_center_cursor()
        return {'FINISHED'}


class AlignObjs(Operator):
    """Align Objects"""
    bl_idname = "align.objs"
    bl_label = "AlignObjs"

    def execute(self, context):
        bpy.ops.object.align()
        return {'FINISHED'}


class PivotPointCursor(Operator):
    """Pivot Point 3DCursor"""
    bl_idname = "pivot_point.cursor"
    bl_label = "PivotPiontCursor"

    def execute(self, context):
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        return {'FINISHED'}


class PivotPointIndivOrigin(Operator):
    """Pivot Point Individual Origin"""
    bl_idname = "pivot_point.indivorigin"
    bl_label = "PivotPointIndivOrigin"

    def execute(self, context):
        bpy.context.scene.tool_settings.transform_pivot_point = 'INDIVIDUAL_ORIGINS'
        return {'FINISHED'}


class SelectInvert(Operator):
    """Invert Selection"""
    bl_idname = "select.invert"
    bl_label = "SelectInvert"

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.mesh.select_all(action='INVERT')
        elif context.mode == 'OBJECT':
            bpy.ops.object.select_all(action='INVERT')
        return {'FINISHED'}


class SelectAll(Operator):
    """Select All Toggle"""
    bl_idname = "select.all"
    bl_label = "SelectAll"

    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            bpy.ops.mesh.select_all(action='TOGGLE')
        elif context.mode == 'OBJECT':
            bpy.ops.object.select_all(action='TOGGLE')
        return {'FINISHED'}


class SelectModeVertex(Operator):
    """Select Mode Vertex"""
    bl_idname = "select_mode.vertex"
    bl_label = "SelectModeVertex"

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        return {'FINISHED'}


class SelectModeEdge(Operator):
    """Select Mode Edge"""
    bl_idname = "select_mode.edge"
    bl_label = "SelectModeEdge"

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
        return {'FINISHED'}


class SelectModeFace(Operator):
    """Select Mode Face"""
    bl_idname = "select_mode.face"
    bl_label = "SelectModeFace"

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        return {'FINISHED'}


class SelectModeVEF(Operator):
    """Select Mode Vertex/Edge/Face"""
    bl_idname = "select_mode.vef"
    bl_label = "SelectModeVEF"

    def execute(self, context):
        bpy.context.tool_settings.mesh_select_mode = (True, True, True)
        return {'FINISHED'}


class SelectTypeMesh(Operator):
    """Select Type Mesh"""
    bl_idname = "select_type.mesh"
    bl_label = "SelectTypeMesh"

    def execute(self, context):
        bpy.ops.object.select_by_type(type='MESH')
        return {'FINISHED'}


class SelectTypeEmpty(Operator):
    """Select Type Empty"""
    bl_idname = "select_type.empty"
    bl_label = "SelectModeEmpty"

    def execute(self, context):
        bpy.ops.object.select_by_type(type='EMPTY')
        return {'FINISHED'}


class SelectTypeLight(Operator):
    """Select Type Light"""
    bl_idname = "select_type.light"
    bl_label = "SelectModeLight"

    def execute(self, context):
        bpy.ops.object.select_by_type(type='LIGHT')
        return {'FINISHED'}


class SelectTypeCamera(Operator):
    """Select Type Camera"""
    bl_idname = "select_type.camera"
    bl_label = "SelectModeCamera"

    def execute(self, context):
        bpy.ops.object.select_by_type(type='CAMERA')
        return {'FINISHED'}


# <--- END Operators

classes = (
    VIEW3D_MT_PIE_template,
    ViewWireframe,
    ViewSolid,
    OriginTo,
    PivotPoint,
    SelectMode,
    SelectType,
    OriginToCursor,
    OriginToGeom,
    CenterViewCursor,
    AlignObjs,
    PivotPointCursor,
    PivotPointIndivOrigin,
    SelectInvert,
    SelectAll,
    SelectModeVertex,
    SelectModeEdge,
    SelectModeFace,
    SelectModeVEF,
    SelectTypeMesh,
    SelectTypeEmpty,
    SelectTypeLight,
    SelectTypeCamera
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in classes:
        bpy.utils.register_class(cls)


if __name__ == "__main__":
    register()
    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")
