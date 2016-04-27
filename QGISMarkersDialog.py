"""
/***************************************************************************
Name			 	 : Markers on maps
Description          : Puts markers on maps!
Date                 : 27/Apr/16 
copyright            : (C) 2016 by Steven Jones
email                : sdjones@sdjones.org 
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
from Ui_QGISMarkers import Ui_QGISMarkers
# create the dialog for QGISMarkers
class QGISMarkersDialog(QtGui.QDialog):
  def __init__(self): 
    QtGui.QDialog.__init__(self) 
    # Set up the user interface from Designer. 
    self.ui = Ui_QGISMarkers ()
    self.ui.setupUi(self)