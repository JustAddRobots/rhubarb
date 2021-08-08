import bpy
from bpy.types import Menu
from bpy.types import Operator


bl_info = {
    "name": "RapidProto Pie Menu",
    "description": "Pie Menu for Rapid Prototyping",
    "author": "Roderick Constance",
    "version": (0, 0, 1, 0),
    "blender": (2, 80, 0),
    "warning": "",
    "category": "3D View",
    "support": "TESTING"
}


class OriginTo(Menu):
    bl_label = "Origin To"
    bl_idname = "origin.to"

    def draw(self, context):
        layout = self.layout
        layout.label("Origin To")
        layout.separator()
        layout.operator(OriginToCursor.bl_idname, icon='PIVOT_CURSOR')
        layout.operator(OriginToGeom.bl_idname, text="Origin to Geometry", icon='MESH_CUBE')


class PivotPoint(Menu):
    bl_label = "Pivot Point"
    bl_idname = "pivot.point"

    def draw(self, context):
        layout = self.layout
        layout.label("Pivot Point")
        layout.separator()
        layout.operator(PivotPointCursor.bl_idname, icon='PIVOT_CURSOR')
        layout.operator(PivotPointIndivOrigin.bl_idname, icon='PIVOT_INDIVIDUAL')


class SelectMode(Menu):
    bl_label = "Select Mode"
    bl_idname = "select.mode"

    def draw(self, context):
        layout = self.layout
        layout.label("Select Mode")
        layout.separator()
        layout.operator(SelectModeVertex.bl_idname, icon='VERTEXSEL')
        layout.operator(SelectModeEdge.bl_idname, icon='EDGESEL')
        layout.operator(SelectModeFace.bl_idname, icon='FACESEL')
        layout.operator(SelectModeVEF.bl_idname, icon='OBJECT_DATA')


class SelectType(Menu):
    bl_label = "Select Type"
    bl_idname = "select.type"

    def draw(self, context):
        layout = self.layout
        layout.label("Select Type")
        layout.separator()
        layout.operator(SelectTypeMesh.bl_idname, icon='MESH_CUBE')
        layout.operator(SelectTypeEmpty.bl_idname, icon='OUTLINER_DATA_EMPTY')
        layout.operator(SelectTypeLight.bl_idname, icon='LIGHT_DATA')
        layout.operator(SelectTypeCamera.bl_idname, icon='CAMERA_DATA')


class VIEW3D_MT_PIE_template(Menu):
    bl_label = "Rapid Proto Pie Menu"
    bl_idname = "rapid_proto.pie"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        pie.operator(OriginTo.bl_idname, text="Origin To")
        pie.operator(AlignObjs.bl_idname, text="Align Objects")
        pie.operator(PivotPoint.bl_idname, text="Pivot Point")
        pie.operator(SelectInvert.bl_idname, text="Invert Selection")
        if context.mode == 'EDIT_MESH':
            pie.operator(SelectMode.bl_idname, text="Selection Mode", icon='VERTEXSEL')
        elif context.mode == 'OBJECT':
            pie.operator(SelectType.bl_idname, text="Selection Type", icon='SELECT_SET')
        pie.operator(SelectAll.bl_idname, text="Select All Toggle")


class OriginToCursor(Operator):  # icon
    """Origin to Cursor"""
    bl_idname = "origin_to.cursor"
    bl_label = "OriginToCursor"

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}


class OriginToGeom(Operator):
    """Origin to Geometry"""
    bl_idname = "origin_to.geom"
    bl_label = "OriginToGeom"

    def execute(self, context):
        bpy.ops.object.origintogeometry_edit()
        return {'FINISHED'}


class AlignObjs(Operator):
    """Align Objects"""
    bl_idname = "align.objs"
    bl_label = "AlignObjs"

    def execute(self, context):
        bpy.ops.object.align
        return {'FINISHED'}


class PivotPointCursor(Operator):  # icon
    """Pivot Point 3DCursor"""
    bl_idname = "pivot_point.cursor"
    bl_label = "PivotPiontCursor"

    def execute(self, context):
        bpy.context.scene.tool_settings.transform_pivot_point = 'CURSOR'
        return {'FINISHED'}


class PivotPointIndivOrigin(Operator):  # icon
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
        bpy.ops.object.select_all(action='INVERT')
        return {'FINISHED'}


class SelectAll(Operator):
    """Select All Toggle"""
    bl_idname = "select.all"
    bl_label = "SelectAll"

    def execute(self, context):
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


classes = (
    OriginTo,
    PivotPoint,
    SelectMode,
    OriginToCursor,
    OriginToGeom,
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


register, unregister = bpy.utils.register_classes_factory(classes)


if __name__ == "__main__":
    register()
    bpy.ops.wm.call_menu_pie(name="VIEW3D_MT_PIE_template")
