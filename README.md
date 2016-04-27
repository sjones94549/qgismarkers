# Overview

**QGIS Markers** is a plugin for [QGIS](http://www.qgis.org/en/site/) that adds a tool for logging clicked coordinates.  You can then copy and paste those coordinates elsewhere, or enjoy them as is.

# Installation

1. Clone this repo into `~/.qgis2/python/plugins/`.
2. Start QGIS.
3. Check `Plugins->Manage and Install Plugins...->QGIS Markers`.

# Usage

Enable the log tool as you would the scroll tool -- either click the log tool icon, or enable it through `Plugins->QGIS Markers->Log Map Clicks`.

View logged clicks through `View->Panels->Log Messages Panel` under the `QGISMarkers` tab.

# Compiling Resources
If icon PNGs change, rebuild `resources_rc.py` with:
```
make clean
make compile
```

# Links

- [Developing Python QGIS Plugins](http://docs.qgis.org/testing/en/docs/pyqgis_developer_cookbook/plugins.html)
- [World Geodesic System](https://en.wikipedia.org/wiki/World_Geodetic_System): WGS 84 / EPSG:4326
- [EPSG:4326](http://www.epsg-registry.org/report.htm?type=selection&entity=urn:ogc:def:crs:EPSG::4326&reportDetail=short&style=urn:uuid:report-style:default-with-code&style_name=OGP%20Default%20With%20Code&title=EPSG:4326)
- [EPSG:3857](http://www.epsg-registry.org/report.htm?type=selection&entity=urn:ogc:def:crs:EPSG::3857&reportDetail=short&style=urn:uuid:report-style:default-with-code&style_name=OGP%20Default%20With%20Code&title=EPSG:3857)
