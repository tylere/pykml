#!/usr/bin/python

from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from math import cosh

text = 'Hello World!'

kmlobj = KML.kml(
    KML.Document()
)

lon1 = -90.18527061414699
lat1 = 38.62381763642669
lon2 = -90.18462877742689
lat2 = 38.62537095459039
# dimensions from: http://en.wikipedia.org/wiki/Gateway_Arch#Mathematical_elements
fc = 191     # max height of centroid [meters]
A = 68.7672
C = 3.0022
L = 91.0     # half width of centroid at base [meters]

for i in range(0,len(text)):
    char = text[i]
    x = 2*L*(1.0*(i+1)/(len(text)+1)-0.5)
    if char != ' ':
        kmlobj.Document.append(
            KML.Placemark(
                KML.name(char),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode('relativeToGround'),
                    KML.coordinates('{lon},{lat},{alt}'.format(
                            lon=lon1 + (lon2-lon1)*i/len(text),
                            lat=lat1 + (lat2-lat1)*i/len(text),
                            alt=fc-A/2*(cosh(C*x/L)-1),
                        ),
                    ),
                ),
            )
        )

print(etree.tostring(etree.ElementTree(kmlobj),pretty_print=True))
