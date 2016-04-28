# Overview

**QGIS Markers** is a [QGIS](http://www.qgis.org/en/site/) plugin for placing markers.  Markers contain useful metadata when inspected, and the `QGIS Markers` log lists `longitude,latitude` pairs for easy copying.

# Installation

1. Install [QGIS](http://www.qgis.org/en/site/).
2. Clone this repo into `~/.qgis2/python/plugins/`.
3. Start QGIS.
4. Check `Plugins->Manage and Install Plugins...->QGIS Markers`.

# Usage

Enable the marker tool as you would the built-in panning tool -- either click the marker tool icon (![marker tool](/icons/place.png?raw=true "Marker Tool icon")), or enable it through `Plugins->Markers->Temporary Markers`.

View marker metadata with the Identify Feature tool.

View logged `longitude,latitude` pairs through `View->Panels->Log Messages Panel` under the `QGISMarkers` tab.

# Compiling Resources
If icon PNGs change, rebuild `resources_rc.py` with:
```
make clean
make compile
```

# Links

- [QGIS API](https://qgis.org/api/annotated.html)
- [Developing Python QGIS Plugins](http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html)
- [World Geodesic System](https://en.wikipedia.org/wiki/World_Geodetic_System): WGS 84 / EPSG:4326
- [EPSG:4326](http://www.epsg-registry.org/report.htm?type=selection&entity=urn:ogc:def:crs:EPSG::4326&reportDetail=short&style=urn:uuid:report-style:default-with-code&style_name=OGP%20Default%20With%20Code&title=EPSG:4326)
- [EPSG:3857](http://www.epsg-registry.org/report.htm?type=selection&entity=urn:ogc:def:crs:EPSG::3857&reportDetail=short&style=urn:uuid:report-style:default-with-code&style_name=OGP%20Default%20With%20Code&title=EPSG:3857)
