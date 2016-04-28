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
        self.layer = None

    @staticmethod
    def log(message):
        QgsMessageLog.logMessage(message, QGISMarkers.LOG_TAG)

    def initGui(self):
        self.log("initGui")

        # Menu actions: Plugins->Markers->[Temporary Markers]
        self.action = QAction(QIcon(":/plugins/qgismarkers/icons/place.png"), "Temporary Markers",
                              self.iface.mainWindow())
        self.action.setObjectName("placeMarkerAction")
        self.action.setWhatsThis("Places a marker at the clicked location.")
        self.action.setStatusTip("Places a marker and logs `longitude,latitude` to the Log Panel.")
        QObject.connect(self.action, SIGNAL("triggered()"), self.activate)

        # Menu: Plugins->[Markers]
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Markers", self.action)

        # Connect to map clicks
        QObject.connect(self.map_click_tool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.click)

    def unload(self):
        self.log("unload")
        self.iface.removePluginMenu("&Markers", self.action)
        self.iface.removeToolBarIcon(self.action)

    def activate(self):
        self.log("activate")
        self.iface.mapCanvas().setMapTool(self.map_click_tool)

    def create_layer(self):
        if self.layer is not None:
            return
        self.log("create_layer")
        path = "Point?crs=epsg:3857&field=id:integer&field=label:string(120)&field=longlat:string(120)&field=url:string(120)&field=x:double&field=y:double&field=longitude:double&field=latitude:double&index=yes"
        self.layer = QgsVectorLayer(path=path, baseName="Temporary Markers", providerLib="memory")
        self.layer.setDisplayField("label")
        QgsMapLayerRegistry.instance().addMapLayer(self.layer)
        QObject.connect(self.layer, SIGNAL("layerDeleted()"), self.delete_layer)

    def delete_layer(self):
        self.log("delete_layer")
        self.layer = None

    def next_marker_id(self):
        if self.layer is None:
            return 0
        return int(self.layer.dataProvider().featureCount())

    def click(self, point, button):
        # Convert from current coordinate reference system to lat/long and Mercator.
        crs_source = self.iface.mapCanvas().mapRenderer().destinationCrs()
        point_latlong = QgsCoordinateTransform(crs_source, QgsCoordinateReferenceSystem(4326)).transform(point)
        point_mercator = QgsCoordinateTransform(crs_source, QgsCoordinateReferenceSystem(3857)).transform(point)

        # Create marker
        id = self.next_marker_id()
        label = "Marker %d" % id
        longlat = "%.010f,%.010f" % (point_latlong.x(), point_latlong.y())
        url = "https://www.google.com/maps?q=%.010f,%.010f&z=%d" % (point_latlong.y(), point_latlong.x(), 18)
        marker = QgsFeature()
        marker.setGeometry(QgsGeometry.fromPoint(point_mercator))

        # Set attributes in the order specified by the layer `path`
        marker.setAttributes([id, label, longlat, url,
                              point_mercator.x(), point_mercator.y(), point_latlong.x(), point_latlong.y()])

        # Add marker to layer
        self.create_layer()
        self.layer.startEditing()
        self.layer.addFeature(marker, True)
        self.layer.commitChanges()

        # Refresh layer
        self.layer.setCacheImage(None)
        self.layer.triggerRepaint()

        self.log(longlat)
