import bpy


class Add_Cells_Panel(bpy.types.Panel):
    bl_idname = "Add_Cells_Panel"
    bl_label = "Add Cells"
    bl_category = "Adding Objects"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator('object.add_cells', text="Add Cells")

