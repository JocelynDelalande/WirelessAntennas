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
from PyQt4 import QtCore, QtGui 
from Ui_WirelessAntennas import Ui_WirelessAntennas
# create the dialog for WirelessAntennas
class WirelessAntennasDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_WirelessAntennas ()
    self.ui.setupUi(self)
