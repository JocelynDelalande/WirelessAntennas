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
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "Wireless Antennas" 
def description():
  return "Shows a raster layer of "
def version(): 
  return "Version 0.1" 
def qgisMinimumVersion():
  return "1.0"
def classFactory(iface): 
  # load WirelessAntennas class from file WirelessAntennas
  from WirelessAntennas import WirelessAntennas 
  return WirelessAntennas(iface)
