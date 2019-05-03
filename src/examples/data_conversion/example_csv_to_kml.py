#!/usr/bin/env python
'''Example of generating KML from data in a CSV file 

References:

'''
import csv
from datetime import datetime
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

def makeExtendedDataElements(datadict):
    '''Converts a dictionary to ExtendedData/Data elements'''
    edata = KML.ExtendedData()
    for key, value in datadict.items():
        edata.append(KML.Data(KML.value(value), name=key + "_"))
    return edata

# create a KML document with a folder and a default style
stylename = "earthquake-balloon-style"
balloonstyle = KML.BalloonStyle(
    KML.text("""
<table Border=1>
  <tr><th>Earthquake ID</th><td>$[Eqid_]</td></tr>
  <tr><th>Magnitude</th><td>$[Magnitude_]</td></tr>
  <tr><th>Depth</th><td>$[Depth_]</td></tr>
  <tr><th>Datetime</th><td>$[Datetime_]</td></tr>
  <tr><th>Coordinates</th><td>($[Lat_],$[Lat_])</td></tr>
  <tr><th>Region</th><td>$[Region_]</td></tr>
</table>"""
    ),
)

doc = KML.Document()

iconstyles = [
    [2,'ff000000'],
    [3,'ffff0000'],
    [4,'ff00ff55'],
    [5,'ffff00aa'],
    [6,'ff00ffff'],
    [7,'ff0000ff'],
]

# create a series of Icon Styles
for threshold,color in iconstyles:
    doc.append(
        KML.Style(
            KML.IconStyle(
                KML.color(color),
                KML.scale(threshold/2.),
                KML.Icon(
                    KML.href("http://maps.google.com/mapfiles/kml/shapes/earthquake.png"),
                ),
                KML.hotSpot(x="0.5",y="0",xunits="fraction",yunits="fraction"),
            ),
            balloonstyle,
            id="earthquake-style-{threshold}".format(threshold=threshold),
        )
    )

doc.append(KML.Folder())

# read in a csv file, and create a placemark for each record
#url="http://earthquake.usgs.gov/earthquakes/catalogs/eqs7day-M2.5.txt"
with open('eqs7day-M2.5.txt', 'r') as fd:
  for row in csv.DictReader(fd):
    timestamp = datetime.strptime(row["Datetime"], "%A, %B %d, %Y %H:%M:%S %Z")
    pm = KML.Placemark(
        KML.name("Magnitude={0}".format(row['Magnitude'])),
        KML.TimeStamp(
            KML.when(timestamp.strftime('%Y-%m-%dT%H:%M:%SZ')),
        ),
        KML.styleUrl(
            "#earthquake-style-{thresh}".format(
                thresh=int(float(row['Magnitude']))
            )
        ),
        makeExtendedDataElements(row),
        KML.Point(
            KML.coordinates("{0},{1}".format(row["Lon"],row["Lat"]))
        )
    )
    doc.Folder.append(pm)

# check if the schema is valid
from pykml.parser import Schema
schema_gx = Schema("kml22gx.xsd")
schema_gx.assertValid(doc)

print(etree.tostring(doc, pretty_print=True).decode())
