import numpy as np
import pyvista as pv
import pandas as pd
import matplotlib.pyplot as plt

def coordenadas_disponibles(lista_de_coordenadas):
    coordenadas_disp=[]
    for i in lista_de_coordenadas:
        if i not in coordenadas_disp:
            coordenadas_disp.append(i)
    coordenadas_disp= sorted(coordenadas_disp)
    return coordenadas_disp

def crear_matriz_3d(n_filas, n_columnas,cotas):
    longitud_fila=[np.nan]*len(cotas)
    matriz=[]
    i=0
    while i<len(n_columnas):
        matriz.append(longitud_fila)
        i=i+1
    
    matriz_3d = []
    z=0
    while z<len(n_filas):
        matriz_3d.append(matriz)
        z+=1
    
    matriz_3d = np.array(matriz_3d)
    return matriz_3d

data_modelo= pd.read_csv('ModeloBloques_insitu.csv')
coord_x= list(data_modelo['x_center'])
coord_y= list(data_modelo['y_center'])
coord_z= list(data_modelo['z_center'])
cut= list(data_modelo['Cut'])

disp_x = coordenadas_disponibles(coord_x)
disp_y = coordenadas_disponibles(coord_y)
disp_z = coordenadas_disponibles(coord_z)

dim_x = int(disp_x[1]-disp_x[0])
dim_y = int(disp_y[1]-disp_y[0])
dim_z = int(disp_z[1]-disp_z[0])

matrix = crear_matriz_3d(disp_x,disp_y,disp_z)

i=0
while i<len(coord_x):
    pos_z = int((coord_z[i] - disp_z[0])/dim_z)
    pos_y = int((coord_y[i] - disp_y[0])/dim_y)
    pos_x = int((coord_x[i] - disp_x[0])/dim_x)
    matrix[pos_x][pos_y][pos_z] = cut[i]
    i+=1



pv.set_plot_theme("Paraview") # "Night"  "Default" "Paraview"
p = pv.Plotter()

grid = pv.UniformGrid()
grid.dimensions = np.array(matrix.shape) + 1
grid.spacing = (20, 20, 18)
grid.origin = (2910,3290,1832)
grid.cell_arrays["Cut"] = matrix.flatten(order="F")

cmap = plt.cm.get_cmap("jet")

threshed= grid.threshold([-9999,9999])
# surf = pv.read('topografia.vtk')

# p.add_mesh(surf,color='brown',lighting=10)
p.add_mesh(threshed,cmap=cmap,show_edges=False)
p.show_grid()
p.show_axes_all()
p.show()
