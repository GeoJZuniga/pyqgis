import os
import re
#reload(sys)
#sys.setdefaultencoding('utf-8')
import urllib
from qgis.core import (
    QgsVectorLayer
)
import PyQt5
from PyQt5.QtGui import *

def buscarTXT(carpeta):
    lista = []
    for ruta, NombreCarpeta, fileNames in os.walk(carpeta):
        for archivo in fileNames:
            if(archivo.endswith('.txt')):
                lista.append(os.path.join(ruta, archivo))
    return lista

carpeta_in = r'F:'
carpeta_out= r'F:'

listaTXT = buscarTXT(carpeta_in)
y=1
for txt in listaTXT:
    # ARCHIVO DE SALIDA
    salida = txt.replace(carpeta_in, carpeta_out)
    # CARPETA DE salida
    outFolder = os.path.dirname(os.path.realpath(salida))
    # CREAR CARPETAS DE salida
    if not os.path.exists(outFolder):
        os.makedirs(outFolder)

    nombre_Carpeta = outFolder.split('\\')
    nombre_Carpeta = nombre_Carpeta[-1]

    print("ESTA ES LA CAPA CARGADA:", txt)
    nombre_archivo = []
    nombre_archivo = txt.split('\\')
    nombre_archivo_ext = nombre_archivo[-1]
    nombre_archivo_sext = nombre_archivo_ext.split('.')
    nombre_archivo_sext = nombre_archivo_sext[0]
    print("NOMBRE DEL ARCHIVO SIN EXTENSIÓN: ", nombre_archivo_sext)
    salida2 = salida.rstrip('.txt')
    numero_pol = nombre_archivo_sext[len(nombre_archivo_sext)-2:len(nombre_archivo_sext)]
    print("NUMERO DE POLIGONO: ", numero_pol, "\n")
    curp = nombre_archivo_sext.lstrip('POL_')
    if len(curp) == 18:
        curp_def = curp
    elif len(curp) >= 18:
        curp_def = curp.replace(curp[len(curp)-3:len(curp)],'')
    else:
        curp_def = "verificar CURP"

    ext = ".shp"
    print("ruta salida: ", salida2)
    guardar = salida2 + ext
    print('\n', guardar)

    name_vl = nombre_archivo_sext + '_crudo'

    uri = "file:{}?delimiter={}&crs={}&wktField={}".format(txt, ",","epsg:4326","WKT_geometry")
    vlayer = QgsVectorLayer(uri, name_vl, "delimitedtext")
    if not vlayer.isValid():
        print("\nError al cargar la capa: ", txt,'\n')

    project = QgsProject.instance()
    print(project.mapLayers())
    project.addMapLayer(vlayer)

    shp_file = outFolder + "\\" + nombre_archivo_sext + '.shp'

    save_options = QgsVectorFileWriter.SaveVectorOptions()
    save_options.driverName = "ESRI Shapefile"
    save_options.fileEncoding = "UTF-8"
    transform_context = QgsProject.instance().transformContext()
    error,error_string = QgsVectorFileWriter.writeAsVectorFormatV2(vlayer,
                                                  shp_file,
                                                  transform_context,
                                                  save_options)
    if error == QgsVectorFileWriter.NoError:
        print("success again!")
    else:
        print('Oh an error has happened: {details}'.format(details=error_string))

    shp_layer = QgsVectorLayer(shp_file, nombre_archivo_sext, "ogr")
    if not shp_layer.isValid():
            print("\nError al cargar la capa: ", txt,'\n')
    QgsProject.instance().addMapLayer(shp_layer)

    pv = shp_layer.dataProvider()
    myField1 = QgsField('NOMBRE', QVariant.String)
    myField2 = QgsField('CURP', QVariant.String, 'string', 18)
    myField3 = QgsField('POLIGONO', QVariant.Int, 'integer', 1)
    myField4 = QgsField('AREA', QVariant.String,'string', 8)
    myField5 = QgsField('PERIMETRO', QVariant.String,'string', 8)
    shp_layer.dataProvider().addAttributes([myField1,myField2,myField3,myField4,myField5])
    shp_layer.updateFields()

    expression1 = QgsExpression('$area')
    expression2 = QgsExpression('$perimeter')

    context = QgsExpressionContext()
    context.appendScopes(QgsExpressionContextUtils.globalProjectLayerScopes(shp_layer))

    with edit(shp_layer):
        for f in shp_layer.getFeatures():
            context.setFeature(f)
            f['NOMBRE'] = nombre_Carpeta
            f['CURP'] = curp_def
            if len(nombre_archivo_sext) == 22:
                f['POLIGONO'] = 1
            elif len(nombre_archivo_sext) > 22:
                f['POLIGONO'] = int(numero_pol)
            else:
                f['POLIGONO'] = 0
            f['AREA'] = expression1.evaluate(context)
            f['PERIMETRO'] = expression2.evaluate(context)

            shp_layer.updateFeature(f)

    layer = qgis.utils.iface.activeLayer()
    res = layer.dataProvider().deleteAttributes([0])
    layer.updateFields()
    layer.commitChanges()

    to_be_deleted = project.mapLayersByName(name_vl)[0]
    project.removeMapLayer(to_be_deleted.id())

    print('\nPOLIGONO n°: ', nombre_archivo_ext, '\n')
    print('\nPOLIGONO ELABORADO n°: ''\n')

print("\n Se cargaron todas las capas y se realizaron todos los procedimientos. \nFIN DEL PROGRAMA.\n")
