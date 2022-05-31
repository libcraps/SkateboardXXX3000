import bpy
import pandas as pd
import numpy as np
    
filetricks = "C:\\Users\\Pierre\\Documents\\GitHub\\SkateboardXXX3000\\06 - Data\\Isolated_Tricks\\pop_shovit\\pop_shovit_1.csv"
df  = pd.read_csv(filetricks)

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

bpy.ops.mesh.primitive_plane_add(size=2, enter_editmode=False, location=(0, 0, 0))


print(df)
time = df['time']
gx = df['gx']
gy = df['gy']
gz = df['gz']
normGyr = df['normGyr']
n = len(time)

plane = bpy.data.objects[0]
# Go to edit mode, face selection mode and select all faces
bpy.ops.object.mode_set( mode = 'EDIT' )     # Toggle edit mode
bpy.ops.mesh.select_mode( type = 'FACE' )    # Change to face selection
bpy.ops.mesh.select_all( action = 'SELECT' ) # Select all faces

for i in range(n-1):
    ti = time[i]
    ti_1 = time[i+1]
    dt = ti_1-ti
    
    
    bpy.ops.mesh.extrude_faces_move(TRANSFORM_OT_shrink_fatten={"value":-dt*25})
    bpy.ops.transform.rotate(value=gx[i]/normGyr[i]*3.14*2, orient_axis='X')
    bpy.ops.transform.rotate(value=gz[i]/normGyr[i]*3.14*2, orient_axis='Z')
    bpy.ops.transform.rotate(value=gy[i]/normGyr[i]*3.14*2, orient_axis='Y')
    #bpy.ops.transform.rotate(value=0.594228, orient_axis='X')



