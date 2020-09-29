import os
import pandas as pd

fichero = r'archivo.xlsx'
ruta = r'' + fichero
nom_tec = ''
carpeta_in = r''
#carpeta_out = r''

# CREAR CARPETAS CON EL NOMBRE DE LA TABLA, RELACION, DATOS
try:
    tabla = pd.read_excel(ruta, header = 0)
except:
    print("NO EXISTE NINGUN FICHERO CON ESE NOMBRE O LA RUTA ESPECIFICADA ES INCORRECTA")
    print("EL PROGRAMA NO CONTINUARÁ")
    exit()

tecnico_tabla = tabla[tabla.TECNICO == nom_tec]

nombres_lista = pd.Series(tecnico_tabla['NOMBRES'])
print(nombres_lista)

for shp in nombres_lista:
    directory = shp
    parent_dir = carpeta_in
    path = os.path.join(parent_dir, directory)
    os.makedirs(path)
    print("Carpeta '%s' se ha creado" %directory)
