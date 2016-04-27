# Makefile for QGIS Markers

default: compile
	
compile:

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<