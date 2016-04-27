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
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint


class QGISMarkers:
    TAG = 'QGISMarkers'

    @staticmethod
    def log(message):
        QgsMessageLog.logMessage(message, QGISMarkers.TAG)

    def __init__(self, iface):
        QGISMarkers.log("__init__")
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.clickTool = QgsMapToolEmitPoint(self.canvas)

    def initGui(self):
        QGISMarkers.log("initGui")

        # Connect to map clicks
        QObject.connect(self.clickTool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.click)

        # Menu actions: Plugins->Place Markers->[menu item]
        self.action = QAction(QIcon(":/plugins/qgismarkers/qgismarkers.png"), "Log Map Clicks", self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.activate)

        # Menu: Plugins->[Place Markers]
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QGIS Markers", self.action)

    def unload(self):
        QGISMarkers.log("unload")
        self.iface.removePluginMenu("&QGIS Markers", self.action)
        self.iface.removeToolBarIcon(self.action)

    def activate(self):
        QGISMarkers.log("activate")
        self.canvas.setMapTool(self.clickTool)

    def click(self, point, button):
        crsSource = self.iface.mapCanvas().mapRenderer().destinationCrs()
        latlong = QgsCoordinateTransform(crsSource, QgsCoordinateReferenceSystem(4326)).transform(point)
        mercator = QgsCoordinateTransform(crsSource, QgsCoordinateReferenceSystem(3857)).transform(point)
        QGISMarkers.log("click %s:  4326(%f, %f)  3857(%f, %f)" %
                        (button, latlong.x(), latlong.y(), mercator.x(), mercator.y()))
