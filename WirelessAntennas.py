"""
/***************************************************************************
Name			 	 : Wireless Antennas
Description          : Shows a raster layer of 
Date                 : 09/May/11 
copyright            : (C) 2011 by Jocelyn Delalande
email                : jocelyn (resides at) crapouillou.net 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from WirelessAntennasDialog import WirelessAntennasDialog
from rasterlang.layers import layerAsArray, writeGeoTiff
from random import randint

import numpy
import math

def createPowerLayer(antenna, antenna_layer_size):
  fn =  "/tmp/rsum.tiff"
  ant_x,ant_y = antenna.geometry().asPoint()
  colors_nb = 256
  #print "---------------"
  #print antenna.attributeIndexes()
  #print "---------------"
  try:
    gain = antenna.attributeMap()[1].toInt()[0]
  except KeyError:
    raise "Antennas must have a gain attribute"

  mat = numpy.zeros((antenna_layer_size,antenna_layer_size), int)

  # How far do we go, in geographic units, (projection dependent...)
  neighb = 700
  # Coordinates of area arround the antenna where we do compute the values.
  around = [ant_x-neighb, ant_y-neighb,
             ant_x+neighb, ant_y+neighb]

  half_width = antenna_layer_size/2
  for i in range(antenna_layer_size):
    for j in range(antenna_layer_size):
      # The following is a total fake isotropic antenna
      norm = math.sqrt((half_width-i)**2 + (half_width-j)**2)
      color = colors_nb*(1-norm/half_width)*gain/20
      if color >= colors_nb:
        color = colors_nb-1
      # numpy indexes matrix[y][x], beware...
      mat[j][i] = color
  return mat, around

class WirelessAntennas: 
  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

  def initGui(self):  
    # Create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/WirelessAntennas/icon.png"), \
        "Wireless Antennas", self.iface.mainWindow())
    # connect the action to the run method
    QObject.connect(self.action, SIGNAL("activated()"), self.run) 

    # Add toolbar button and menu item
    self.iface.addToolBarIcon(self.action)
    self.iface.addPluginToMenu("&Wireless Antennas", self.action)

    # Bind F6 to the computing of antennas
    self.keyAction = QAction("Compute antennas", self.iface.mainWindow())
    self.iface.registerMainWindowAction(self.keyAction, "F6") 
    self.iface.addPluginToMenu("&Compute antennas", self.keyAction)
    QObject.connect(self.keyAction, SIGNAL("triggered()"),self.drawCoverages)

  def unload(self):
    # Remove the plugin menu item and icon
    self.iface.removePluginMenu("&Wireless Antennas",self.action)
    self.iface.removeToolBarIcon(self.action)
    self.iface.unregisterMainWindowAction(self.keyAction)
    self.iface.removePluginMenu("&Compute antennas",self.keyAction)

  # run method that performs all the real work
  def run(self): 
    # create and show the dialog 
    dlg = WirelessAntennasDialog()
    # show the dialog
    dlg.show()
    result = dlg.exec_()
    # See if OK was pressed
    if result == 1:
      self.drawCoverages()

  def drawCoverages(self):
    # Hack to avoid prompting projection
    settings = QSettings()
    prjSetting = settings.value("/Projections/defaultBehaviour").toString()
    settings.setValue("/Projections/defaultBehaviour","useGlobal")

    antenna_layer_size = 200
    antennas = self.iface.activeLayer()
    
    provider = antennas.dataProvider()
    
    feat = QgsFeature()
    allAttrs = provider.attributeIndexes()
    
    # start data retreival: fetch geometry and all attributes for each feature
    provider.select(allAttrs)      

    layers = []

    while provider.nextFeature(feat):
      # fetch geometry
      geom = feat.geometry()
      print "Feature ID %d: " % feat.id() ,
      # show some information about the feature
      if geom.type() == QGis.Point:
        x = geom.asPoint()
        print "Point: " + str(x)
      else:
        print "Unknown"

      # fetch map of attributes
      attrs = feat.attributeMap()

      # attrs is a dictionary: key = field index, value = QgsFeatureAttribute
      # show all attributes and their values
      for (k,attr) in attrs.iteritems():
        print "%d: %s" % (k, attr.toString())

      filename = "antenna%i" % feat.id()
      print filename
      matrix, around = createPowerLayer(feat, antenna_layer_size)
      writeGeoTiff(matrix, around, filename)

      rl = QgsRasterLayer(filename,filename)
      rl.setCrs(antennas.crs())
      layers.append(rl)
        
    globExtent = addExtents(layers)

    # Raster (pixels) dimensions of the global layer 
    # (Keep the same resolution for the global layer)
    resx = antenna_layer_size/(layers[0].extent().width())
    resy = antenna_layer_size/(layers[0].extent().height())
    print "point dimensions are : %f %f" % (resx, resy)

    globPWidth = globExtent.width()*resx
    globPHeight = globExtent.height()*resy

    globMat  = numpy.zeros((globPHeight, globPWidth), int)
    print "global mat is %ix%i" % (globPWidth, globPHeight)

    for layer in layers:
      # Uncomment to display each antenna layer.
      #layer.setContrastEnhancementAlgorithm("StretchToMinimumMaximum")
      #QgsMapLayerRegistry.instance().addMapLayer(layer)
      #layer.setInvertHistogram(True)
      #layer.setContrastEnhancementAlgorithm("StretchToMinimumMaximum")
      antennaMat = layerAsArray(layer)

      lext = layer.extent()
      # get the coordinates as : xleft, ytop, xright, ybottom
      axmin, aymin, axmax, aymax = lext.xMinimum(), lext.yMaximum(), lext.xMaximum(), lext.yMinimum()
      gxmin, gymin, gxmax, gymax = globExtent.xMinimum(), globExtent.yMaximum(), globExtent.xMaximum(), globExtent.yMinimum()

      # Computes the position in pixels of one antenna layer inside the global array.
      dx = (axmin - gxmin) * resx
      dy = -(aymin - gymin) * resy
      dx, dy = int(dx), int(dy)
      
      print "dx is %i, dy is %i" % (dx, dy)

      for i in range(antenna_layer_size):
        for j in range(antenna_layer_size):
          if i < 10 and j < 10:
            print "%ix%i" % (dx+i, dy+j)
          color = max(antennaMat[j][i], globMat[dy+j][dx+i])
          globMat[dy+j][dx+i] = color

    # Create
    writeGeoTiff(globMat, (gxmin, gymax, gxmax, gymin), "/tmp/global_ant.tif")
    globalRaster = QgsRasterLayer("/tmp/global_ant.tif", "Antennas coverage")
    globalRaster.setCrs(antennas.crs())
    globalRaster.setContrastEnhancementAlgorithm("StretchToMinimumMaximum")
    QgsMapLayerRegistry.instance().addMapLayer(globalRaster)
    
    if prjSetting:
      settings.setValue("/Projections/defaultBehaviour",prjSetting)
    print "done"


def addExtents(rasterList):
  """ Gets a list of QgsLayer as argument and returns the smallest extent
  containing them all.
  """
  max_extent = rasterList[0].extent()
  for layer in rasterList[1:]:
    max_extent.combineExtentWith(layer.extent())
  return max_extent
