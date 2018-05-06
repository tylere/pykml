#!/usr/bin/python

from lxml import etree
from pykml.factory import KML_ElementMaker as KML

doc = KML.kml(
    KML.Placemark(
        KML.name('Hello World!'),
        KML.Point(
            KML.coordinates('-91.35,0,0'),
        ),
    ),
)
print(etree.tostring(etree.ElementTree(doc),pretty_print=True))

