# -*- coding: utf-8 -*-
"""
Volume calcs

"""
#Defines path to TIF and draws the layer
path_to_tif = "C:/Users/61428/Documents/MajorProj/DSM.tif"
iface.addRasterLayer(path_to_tif, "DSM")

#Changes the symbology to a gradient from brown to white with 30 categories (to make the surface easy to see)
raster = QgsProject.instance().mapLayersByName('DSM')[0]
colRamp = QgsGradientColorRamp (QColor(92,48,4), QColor(255,255,255), False)
renderer = QgsSingleBandPseudoColorRenderer(raster.dataProvider(), 1)
renderer.createShader(colRamp, QgsColorRampShader.Discrete, QgsColorRampShader.Quantile, 30)
raster.setRenderer(renderer)
raster.triggerRepaint()


#Draws contours on the DSM at 150m 
raster = [l for l in QgsProject().instance().mapLayers().values() if isinstance(l, QgsRasterLayer) and 'DSM' in l.name()][0]

#The interval value can be changed depending on the range of the used DSM
processing.runAndLoadResults("gdal:contour", 
    {'INPUT':raster,
    'BAND':1,
    'INTERVAL':150,
    'FIELD_NAME':'ELEV',
    'OUTPUT':'TEMPORARY_OUTPUT'})

#Volume calculation 
processing.run("qgis:rastersurfacevolume",
{ 'BAND' : 1,
'INPUT' : 'DSM',
#Level referes to elevation above/below that is used in the volume calculation
'LEVEL' : 0,
#Method, 0 = volume above base level, 1 = volume below base level
'METHOD' : 0,
'OUTPUT_HTML_FILE' : 'C:/Users/61428/Documents/MajorProj/VolumeReport.html',
})

#Greater than and less than raster (Shows portion of land used in volume calculation)
input_raster = QgsRasterLayer('C:/Users/61428/Documents/MajorProj/DSM.tif', 'raster')      
output_raster = 'C:/Users/61428/Documents/MajorProj/DSMCALC.tif'

#The ratser caclulator is used to create a new raster with all the areas >150m appearing in white and <150m appearing in black
parameters = {'INPUT_A' : input_raster,
        'BAND_A' : 1,
        'FORMULA' : '(A > 150)', 
        'OUTPUT' : output_raster}

processing.runAndLoadResults('gdal:rastercalculator', parameters)
