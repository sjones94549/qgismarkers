"""
/***************************************************************************
Name			 	 : Markers on maps
Description          : Puts markers on maps!
Date                 : 27/Apr/16 
copyright            : (C) 2016 by Steven Jones
email                : sdjones@sdjones.org 
****************************************************************************/

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
  return "Markers on maps" 
def description():
  return "Puts markers on maps!"
def version(): 
  return "Version 0.0.0.1" 
def qgisMinimumVersion():
  return "2.0"
def classFactory(iface): 
  # load QGISMarkers class from file QGISMarkers
  from QGISMarkers import QGISMarkers 
  return QGISMarkers(iface)
