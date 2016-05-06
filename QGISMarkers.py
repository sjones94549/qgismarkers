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
        self.actions = {}

    @staticmethod
    def log(message):
        QgsMessageLog.logMessage(message, QGISMarkers.LOG_TAG)

    def initGui(self):
        self.log("initGui")
        self.create_place_marker_action()
        self.create_jump_to_feature_action()

    def create_place_marker_action(self):
        # Menu actions: Plugins->Markers->[Temporary Markers]
        action = QAction(QIcon(":/plugins/qgismarkers/place.png"), "Temporary Markers", self.iface.mainWindow())
        action.setObjectName("placeMarkerAction")
        action.setWhatsThis("Places a marker at the clicked location.")
        action.setStatusTip("Places a marker and logs `longitude,latitude` to the Log Panel.")
        QObject.connect(action, SIGNAL("triggered()"), self.activate_place_marker_action)

        # Menu: Plugins->[Markers]
        self.iface.addToolBarIcon(action)
        self.iface.addPluginToMenu("&Markers", action)

        # Connect to map clicks
        QObject.connect(self.map_click_tool, SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.click)

        self.actions['place_marker'] = action

    def activate_place_marker_action(self):
        self.log("activate_place_marker_action")
        self.iface.mapCanvas().setMapTool(self.map_click_tool)

    def create_jump_to_feature_action(self):
        # Menu actions: Plugins->Markers->[Temporary Markers]
        action = QAction(QIcon(":/plugins/qgismarkers/jump.png"), "Jump to Feature", self.iface.mainWindow())
        action.setObjectName("jumpToFeatureAction")
        action.setWhatsThis("Jumps to a feature in a given layer.")
        action.setStatusTip("Jumps to a feature in a given layer.")
        QObject.connect(action, SIGNAL("triggered()"), self.activate_jump_to_feature_action)

        # Menu: Plugins->[Markers]
        self.iface.addToolBarIcon(action)
        self.iface.addPluginToMenu("&Markers", action)

        self.actions['jump_to_feature'] = action

    def activate_jump_to_feature_action(self):
        self.log("activate_jump_to_feature_action")
        JumpToFeatureDialog.jump_to_feature(iface=self.iface, parent=self.iface.mainWindow())

    def unload(self):
        self.log("unload")
        if not self.actions or self.actions is None:
            return
        for name, action in self.actions.items():
            self.iface.removePluginMenu("&Markers", action)
            self.iface.removeToolBarIcon(action)

    def create_layer(self):
        if self.layer is not None:
            return
        self.log("create_layer")
        path = "Point?crs=epsg:3857&field=id:integer&field=label:string(120)&field=longlat:string(120)&field=xy:string(120)&field=url:string(120)&field=x:double&field=y:double&field=longitude:double&field=latitude:double&index=yes"
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
        xy = "%.010f,%.010f" % (point_mercator.x(), point_mercator.y())
        url = "https://www.google.com/maps?q=%.010f,%.010f&z=%d" % (point_latlong.y(), point_latlong.x(), 18)
        marker = QgsFeature()
        marker.setGeometry(QgsGeometry.fromPoint(point_mercator))

        # Set attributes in the order specified by the layer `path`
        marker.setAttributes([id, label, longlat, xy, url,
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


last_jump_dialog_values = {
    'layer': None
}


class JumpToFeatureDialog(QDialog):
    def __init__(self, iface=None, parent=None, last_values=None):
        super(JumpToFeatureDialog, self).__init__(parent)
        self.setWindowTitle("Jump to Feature")
        self.iface = iface
        self.selected_layer = None
        self.selected_attribute = None

        layout = QFormLayout()

        # Layers
        box = QComboBox()
        self.layer_combo_box = box
        self._populate_layers()
        box.currentIndexChanged.connect(self._layer_selected)
        layout.addRow(box)

        # Attributes
        box = QComboBox()
        self.attribute_combo_box = box
        self._populate_attributes()
        box.currentIndexChanged.connect(self._attribute_selected)
        layout.addRow(box)

        # Value
        edit = QLineEdit()
        self.attribute_edit = edit
        layout.addRow(edit)

        # Jump
        button = QPushButton("Jump to Feature")
        self.jump_button = button
        button.clicked.connect(self._jump)
        layout.addRow(button)

        self._layer_selected(0)  # TODO
        # self.attribute_selected(0)  # TODO

        self.setLayout(layout)

    def _populate_layers(self):
        layers = QgsMapLayerRegistry.instance().mapLayers()
        self.layer_combo_box.clear()
        for name, layer in layers.iteritems():
            if hasattr(layer, 'attributeList'):
                self.layer_combo_box.addItem(layer.name(), name)

    def _populate_attributes(self):
        self.attribute_combo_box.clear()
        if self.selected_layer is None:
            return
        for i in self.selected_layer.attributeList():
            name = self.selected_layer.attributeDisplayName(i)
            self.attribute_combo_box.addItem(name, name)

    def _layer_selected(self, i):
        data = self.layer_combo_box.itemData(i)
        layer = QgsMapLayerRegistry.instance().mapLayers()[data]
        self.selected_layer = layer
        self._populate_attributes()

    def _attribute_selected(self, i):
        data = self.attribute_combo_box.itemData(i)
        self.selected_attribute = data

    def _jump(self):
        layer = self.selected_layer
        print("Layer: %s" % str(layer))
        if layer is None:
            return
        attribute = self.selected_attribute
        print("Attribute: %s" % str(attribute))
        if attribute is None:
            return
        value = self.attribute_edit.text()
        print("Value: %s" % str(value))
        if value is None:
            return
        request = QgsFeatureRequest(QgsExpression("%s = %s" % (attribute, value)))
        extent = None
        for feature in layer.dataProvider().getFeatures(request):
            print("Found feature %s" % str(feature.id()))
            if extent is None:
                extent = feature.geometry().boundingBox()
            else:
                extent.combineExtentWith(feature.geometry().boundingBox())
        if extent is None:
            return
        source_crs = layer.crs()
        canvas_crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
        extent = QgsCoordinateTransform(source_crs, canvas_crs).transformBoundingBox(extent)
        self.iface.mapCanvas().setExtent(extent)
        self.iface.mapCanvas().zoomScale(self.iface.mapCanvas().scale() * 1.1)
        self.iface.mapCanvas().refresh()

    @staticmethod
    def jump_to_feature(iface=None, parent=None):
        dialog = JumpToFeatureDialog(iface=iface, parent=parent)
        result = dialog.exec_()
