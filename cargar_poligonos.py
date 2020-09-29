import os
from qgis.core import (
    QgsVectorLayer
)
import PyQt5
from PyQt5.QtGui import *

def buscarSHP(carpeta):
    lista = []
    for ruta, NombreCarpeta, fileNames in os.walk(carpeta):
        for archivo in fileNames:
            if(archivo.endswith('.gpx')):
                lista.append(os.path.join(ruta, archivo))
    return lista

#carpeta_in = arcpy.GetParameterAsText(0)
#shpCortar  = arcpy.GetParameterAsText(1)
#carpeta_out= arcpy.GetParameterAsText(2)

carpeta_in = r'C:\Users\user\Documents\JZM\CRUDOS'
carpeta_out= r'C:\Users\user\Documents\JZM\PROCESADOS'

listaSHP = buscarSHP(carpeta_in)
y=1
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
    salida = salida.rstrip('.gpx')
    ext = ".shp"
    print("ruta salida: ", salida)
    guardar = salida + ext
    print('\n', guardar)
    #vlayer = QgsVectorLayer(shp + '|layername=route_points', nombre_archivo_sext, "ogr") #+ '|layername=route_points'
    #if not vlayer.isValid():
    #    print("Error al cargar la capa")

    vlayer = QgsVectorLayer(shp + '|layername=track_points', nombre_archivo_sext, "ogr") #+ '|layername=route_points'
    if not vlayer.isValid():
        print("Error al cargar la capa")
    QgsProject.instance().addMapLayer(vlayer)
    #uri = shp + "?type=route_points"
    #vlayer = iface.addVectorLayer(uri, "capa_"+ str(y), "gpx") #'+ |layername=route_points'
    #if not vlayer:
    #    print("Error al visualizar la capa")

    #uri1 = r'C:\Users\user\Documents\JZM\POLIGONOS\01_LINEAS' + r"\lineas_" + nombre_archivo_sext +'.shp'
    processing.run("qgis:pointstopath", {'INPUT':shp +'|layername=track_points',
                     'ORDER_FIELD':'track_seg_point_id','GROUP_FIELD':None,
                     'DATE_FORMAT':'','OUTPUT': guardar}) #'TEMPORARY_OUTPUT',  'ORDER_FIELD':'track_seg_point_id' 'route_points'
                     
    # uri2 = r'C:\Users\user\Documents\JZM\POLIGONOS\02_POLIGONOS' + r"\POL_" + nombre_archivo_sext +".shp"
    # input2 = " "
    guardar2 = salida +'_pol'+ ext
    processing.run("qgis:linestopolygons", {'INPUT':guardar, 'OUTPUT':guardar2})

    # REPROYECCIÓN
    # uri3 = r'C:\Users\user\Documents\JZM\POLIGONOS\03_POL_REPROYECTADOS' + r"\\" + nombre_archivo_sext + ".shp"
    guardar3 = salida + '_pol_repr' + ext
    processing.run("native:reprojectlayer",{'INPUT':guardar2,'TARGET_CRS':QgsCoordinateReferenceSystem('EPSG:32614'),'OUTPUT': guardar3})
    #
    # # AGREGAR GEOMETRIA (AREA, PERIMETRO)
    # uri4 = r'C:\Users\user\Documents\JZM\POLIGONOS\04_POL_GEOMETRIA' + r"\\" + nombre_archivo_sext + ".shp"
    # input_pol = r'C:\Users\user\Documents\JZM\POLIGONOS\03_POL_REPROYECTADOS' + r'\\' + nombre_archivo_sext + '.shp'
    # processing.run("qgis:exportaddgeometrycolumns",{'INPUT':input_pol,'CALC_METHOD':0,'OUTPUT':uri4})
    # # AGREGAR ATRIBUTOS (CAMPOS) DE CURP Y POLIGONO, AUTOMATIZAR PARA OBTENER
    # # LA CURP DEL NOMBRE DEL ARCHIVO"""
    #
    # vlayer_pol = QgsVectorLayer(uri4, "capa_"+str(y), "ogr") #+ '|layername=route_points'
    # if not vlayer_pol.isValid():
    #     print("Error al cargar la capa")
    # myField1 = QgsField('CURP', QVariant.String ,len=18)
    # myField2 = QgsField('POLIGONO', QVariant.Int ,len=2)
    # vlayer_pol.dataProvider().addAttributes([myField1,myField2])
    # vlayer_pol.updateFields()
    # QgsProject.instance().addMapLayer(vlayer_pol)
    # #idx = vlayer_pol.fieldNameIndex( 'newColumn' )
    #
    # features = vlayer_pol.getFeatures()
    #
    # #print(features[1])
    #
    # print('\nPOLIGONO n°: ', nombre_archivo_ext, '\n')
    # y += 1
    # #arcpy.Clip_analysis(shp, shpCortar, salida)
    # #QgsProject.instance().removeMapLayer(vlayer) #PARA ELIMINAR LAS CAPAS QUE SE VAN GENERANDO

print("\n Se cargaron todas las capas y se realizaron todos los procedimientos. \nFIN DEL PROGRAMA.\n")
# nombres_campo = [QgsField("FID", QVariant.Int),
# QgsField("EXPEDIENTE",  QVariant.String),
# QgsField("BITACORA", QVariant.String),
# QgsField("TRAMITE", QVariant.String),
# QgsField("SIT JURIDICA", QVariant.String),
# QgsField("Area_C", QVariant.Double),
# QgsField("STATUS", QVariant.String)]
