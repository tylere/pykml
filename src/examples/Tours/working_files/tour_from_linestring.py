#!/usr/bin/env python
'''Generate a KML document of a tour based on a KML linestring.

'''
from pykml.parser import parse
from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pykml.parser import Schema
from lxml import etree

# define variables for the namespace URL strings
kmlns = '{}' #'{' + nsmap['kml'] + '}'
gxns = '{' + nsmap['gx'] + '}'

# start with a base KML tour and playlist
tour_doc = KML.kml(
    GX.Tour(
      KML.name("Play me!"),
      GX.Playlist(),
    )
)

with open("colorado_river_linestring.kml") as f:
    linestring_doc = parse(f)

# get the coordinate string of the first KML coordinate element
coord_str = str(
    linestring_doc.getroot().find(".//{http://www.opengis.net/kml/2.2}coordinates")
).strip()

for vertex in coord_str.split(' '):
    (lon,lat,alt) = vertex.split(',')
    flyto = GX.FlyTo(
        GX.duration(2),
        GX.flyToMode("smooth"),
        KML.Camera(
          KML.longitude(lon),
          KML.latitude(lat),
          KML.altitude(0),
          KML.heading(-129.7),
          KML.tilt(90.0),
          KML.altitudeMode("relativeToGround"),
        )
    )
    tour_doc[gxns+"Tour"].Playlist.append(flyto)

assert Schema('kml22gx.xsd').validate(tour_doc)
print(etree.tostring(tour_doc, pretty_print=True))

# output a KML file (named based on the Python script)
outfile = file(__file__.rstrip('.py')+'.kml','w')
outfile.write(etree.tostring(tour_doc, pretty_print=True))
