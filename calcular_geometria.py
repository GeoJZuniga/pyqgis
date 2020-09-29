import os
from qgis.core import (
    QgsVectorLayer
)
import PyQt5
from PyQt5.QtGui import *

nom_tecnico = ""

def buscarSHP(carpeta):
    lista = []
    for ruta, NombreCarpeta, fileNames in os.walk(carpeta):
        for archivo in fileNames:
            if(archivo.endswith('.shp')):
                lista.append(os.path.join(ruta, archivo))
    return lista

carpeta_in  = r'F:\JZM\METLATONOC\ANTONINO'
carpeta_out = r'F:\JZM\\METLATONOC\PROCESADOS\ANTONINO'

listaSHP = buscarSHP(carpeta_in)
y=1
layer_lista = []
for shp in listaSHP:
    # ARCHIVO DE SALIDA
    salida = shp.replace(carpeta_in, carpeta_out)
    # CARPETA DE salida
    outFolder = os.path.dirname(os.path.realpath(salida))
    # CREAR CARPETAS DE salida
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    print("ESTA ES LA CAPA CARGADA:", shp)
    nombre_archivo = []
    nombre_archivo = shp.split('\\')
    nombre_archivo_ext = nombre_archivo[-1]
    nombre_archivo_sext = nombre_archivo_ext.split('.')
    nombre_archivo_sext = nombre_archivo_sext[0]
    print("NOMBRE DEL ARCHIVO SIN EXTENSIÓN: ", nombre_archivo_sext)
    salida = salida.rstrip('.shp')
    ext = ".shp"
    print("ruta salida: ", salida)
    guardar = salida + ext
    print('\n', guardar)

    vlayer = QgsVectorLayer(shp, nombre_archivo_sext, "ogr")
    if not vlayer.isValid():
        print("\nError al cargar la capa: ", shp,'\n')
    QgsProject.instance().addMapLayer(vlayer)

    crs_layer = vlayer.crs()
    print('\n', crs_layer, '\n')
    crs = crs_layer.description()
    nom_tecnicoInt =  nom_tecnico  ### SUSTITUIR ANTES DE EJECUTAR CAMBIO DE TECNICO
    num_binomio = '01'
    status = 'REVISION'

    pv = vlayer.dataProvider()
    myField1 = QgsField('area_pl', QVariant.Double, 'double', 8, 4)
    myField2 = QgsField('per_pl', QVariant.Double, 'double', 8, 4)
    myField3 = QgsField('src', QVariant.String)
    myField4 = QgsField('TECNICO', QVariant.String)
    myField5 = QgsField('BINOMIO', QVariant.String)
    myField6 = QgsField('STATUS', QVariant.String)
    myField7 = QgsField('CACs', QVariant.String)
    vlayer.dataProvider().addAttributes([myField1,myField2,myField3,myField4,myField5,myField6,myField7])
    vlayer.updateFields()

    expression1 = QgsExpression('$area')
    expression2 = QgsExpression('$perimeter')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(vlayer))

    with edit(vlayer):
        for f in vlayer.getFeatures():
            context.setFeature(f)
            f['area_pl'] = expression1.evaluate(context)
            f['per_pl'] = expression2.evaluate(context)
            f['src'] = crs
            f['TECNICO'] = nom_tecnico
            f['BINOMIO'] = num_binomio
            f['STATUS'] = status
            vlayer.updateFeature(f)

    layer_lista.append(nombre_archivo_sext)

    print('\nPOLIGONO n°: ', nombre_archivo_ext, '\n')
    y += 1

#processing.run('qgis:mergevectorlayers', layer_lista, merge_salida)
print("\n Se cargaron todas las capas y se realizaron todos los procedimientos. \nFIN DEL PROGRAMA.\n")
