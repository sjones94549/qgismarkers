# Makefile for QGIS Markers

RESOURCE_FILES = resources_rc.py

default: compile
	
compile: $(RESOURCE_FILES)

%_rc.py : %.qrc
	pyrcc4 -o $*_rc.py  $<

clean:
	rm -f $(RESOURCE_FILES)
	rm -f *.pyc
