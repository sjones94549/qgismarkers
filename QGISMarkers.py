"""
    Basic QGIS plugin to ease copying lat/long from QGIS.
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint
import resources_rc


class QGISMarkers:
    LOG_TAG = "QGISMarkers"

    def __init__(self, iface):
        self.log("__init__")
        self.iface = iface
        self.map_click_tool = QgsMapToolEmitPoint(iface.mapCanvas())

    @staticmethod
    def log(message):
        QgsMessageLog.logMessage(message, QGISMarkers.LOG_TAG)

    def initGui(self):
        self.log("initGui")

        # Menu actions: Plugins->QGIS Markers->[Log Coordinates]
        self.action = QAction(QIcon(":/plugins/qgismarkers/icons/log.png"), "Log Coordinates", self.iface.mainWindow())
        self.action.setObjectName("logClickedCoordinatesAction")
        self.action.setWhatsThis("Logs clicked coordinates to the QGIS log")
        self.action.setStatusTip("Logs map clicks to the `%s` tab.  View in the Log panel." % QGISMarkers.LOG_TAG)
        QObject.connect(self.action, SIGNAL("triggered()"), self.activate)

        # Menu: Plugins->[QGIS Markers]
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&QGIS Markers", self.action)

        # Connect to map clicks
        QObject.connect(self.map_click_tool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.click)

    def unload(self):
        self.log("unload")
        self.iface.removePluginMenu("&QGIS Markers", self.action)
        self.iface.removeToolBarIcon(self.action)

    def activate(self):
        self.log("activate")
        self.iface.mapCanvas().setMapTool(self.map_click_tool)

    def click(self, point, button):
        # Convert from current coordinate reference system to lat/long and Mercator.
        crs_source = self.iface.mapCanvas().mapRenderer().destinationCrs()
        point_latlong = QgsCoordinateTransform(crs_source, QgsCoordinateReferenceSystem(4326)).transform(point)
        point_mercator = QgsCoordinateTransform(crs_source, QgsCoordinateReferenceSystem(3857)).transform(point)

        # Take actions based on mouse button.
        if button == 1:
            self.log("(%.010f, %.010f) (%.010f, %.010f)" %
                     (point_latlong.x(), point_latlong.y(), point_mercator.x(), point_mercator.y()))
        elif button == 2:
            self.log("https://www.google.com/maps/@%.010f,%.010f,18z" % (point_latlong.y(), point_latlong.x()))
        else:
            self.log("click %s" % button)
