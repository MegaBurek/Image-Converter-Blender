bl_info = {
    "name": "Add Cells",
    "blender": (2, 80, 0),
    "category": "Add"
}
import bpy
import convertcloud as cvc
import os
import tkinter as tk
from tkinter import filedialog


class AddCells(bpy.types.Operator):
    bl_idname = "object.add_cells"
    bl_label = "Add Cells"
    bl_options = {'REGISTER', 'UNDO'}

    
    
    fof: bpy.props.BoolProperty(name="File/Folder", default = True, description = "When disabled, you select one file. When enabled, you select a directory.")
    xyz: bpy.props.BoolProperty(name="Import XYZ files in folder", default = True, description = "If disabled, xyz files will be skipped during import")
    convert: bpy.props.BoolProperty(name="Toggle XYZ-PLY Conversion", default = True, description = "If disabled, xyz files will be imported as cubes. You can control the detail level of the imported files by changing the Mesh Resolution")
    mesh: bpy.props.BoolProperty(name="Toggle Meshing", default = True, description = "Enable Convex Hull Meshing")
    cube_number: bpy.props.IntProperty(default =100, max = 9000, min = 1, name = "Mesh Resolution", description = "every n-th coordinate of an XYZ file will be integrated into the mesh")

    def invoke(self, context, event):
        wm = context.window_manager
        return wm.invoke_props_dialog(self)


    def execute(self, context):
        root = tk.Tk()
        root.withdraw()
        conv = cvc.Converter()

        if self.fof == True:
            folder_path = filedialog.askdirectory()

            filename = ""


            foldername = os.path.basename(os.path.dirname(folder_path+'/'))

            bpy.ops.collection.create(name=foldername)

            for file in os.listdir(folder_path):
                
                if(file.endswith(".xyz")):
                    if(self.xyz == True):
                        if(self.convert == True):
                            conv.load_points(folder_path + "/" + file)

                            filename = folder_path + "/" + file + "_konvertovano.ply"
                            conv.convert(filename)
                            bpy.ops.import_mesh.ply(filepath=filename)
                            
                            if self.mesh == True:
                                bpy.ops.object.editmode_toggle()
                                bpy.ops.mesh.convex_hull()
                                bpy.ops.object.editmode_toggle()


                            ob = bpy.context.view_layer.objects.active
                            col = bpy.data.collections[foldername]
                            col.objects.link(ob)
                        
                        else:

                            f = open(folder_path + "/" + file, "r")

                            contents = f.read()

                            array = []
                            matrix = [[]]

                            array = contents.split("\n")

                            for i in range(len(array)-1):

                                subArray = array[i].split(" ")
                                newRow = []
                            
                                for j in range(len(subArray)):
                                    newRow.append(float(subArray[j]))
                            
                                matrix.append(newRow)
                                newRow = []

                            bpy.ops.mesh.primitive_cube_add(size=0.01, enter_editmode=True, location=(matrix[1][3], matrix[1][4], matrix[1][5]))
                            for i in range(1, len(matrix)-1, self.cube_number):
                                bpy.ops.mesh.primitive_cube_add(size=0.01, enter_editmode=True, location=(matrix[i][3], matrix[i][4], matrix[i][5]))

                            if (self.mesh == True):
                                bpy.ops.mesh.convex_hull()
                                bpy.ops.object.editmode_toggle()
                            
                            ob = bpy.context.view_layer.objects.active
                            col = bpy.data.collections[foldername]
                            col.objects.link(ob)




                elif file.endswith(".ply"):
                    bpy.ops.import_mesh.ply(filepath=folder_path + "/" + file)
                    
                    if self.mesh == True:
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()

                    ob = bpy.context.view_layer.objects.active
                    col = bpy.data.collections[foldername]
                    print(col)
                    col.objects.link(ob)

            

        else:
            file_path = filedialog.askopenfilename(title="Select File", filetypes=(("xyz files", "*.xyz"), ("ply files", "*.ply")))


            if file_path.endswith(".xyz"):

                if (self.convert == True):

                    conv.load_points(file_path)

                    filename = file_path + "_konvertovano.ply"
                    conv.convert(filename)
                    bpy.ops.import_mesh.ply(filepath=filename)
                            
                    if self.mesh == True:
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()

                else:

                    f = open(file_path, "r")

                    contents = f.read()

                    array = []
                    matrix = [[]]

                    array = contents.split("\n")

                    for i in range(len(array)-1):

                        subArray = array[i].split(" ")
                        newRow = []
                    
                        for j in range(len(subArray)):
                            newRow.append(float(subArray[j]))
                    
                        matrix.append(newRow)
                        newRow = []

                    bpy.ops.mesh.primitive_cube_add(size=0.01, enter_editmode=True, location=(matrix[1][3], matrix[1][4], matrix[1][5]))
                    for i in range(1, len(matrix)-1, self.cube_number):
                        bpy.ops.mesh.primitive_cube_add(size=0.01, enter_editmode=True, location=(matrix[i][3], matrix[i][4], matrix[i][5]))

                    bpy.ops.mesh.convex_hull()
                    bpy.ops.object.editmode_toggle()
                
            elif file_path.endswith(".ply"):

                bpy.ops.import_mesh.ply(filepath=filename)
                if self.mesh == True:
                        bpy.ops.object.editmode_toggle()
                        bpy.ops.mesh.convex_hull()
                        bpy.ops.object.editmode_toggle()
        
        return {'FINISHED'}


def menu_func(self, context):
    self.layout.operator(AddCells.bl_idname)

def register():
    bpy.utils.register_class(AddCells)
    bpy.types.VIEW3D_MT_add.append(menu_func)

def unregister():
    bpy.utils.unregister_class(AddCells)
    bpy.types.VIEW3D_MT_add.remove(menu_func)


if __name__ == "__main__":
    register()

    bpy.ops.object.add_cells('INVOKE_DEFAULT')