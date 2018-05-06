#!/usr/bin/python
# a Python script that uses pyKML to create a Hello World example
from lxml import etree
from pykml.factory import KML_ElementMaker as KML

text = 'Hello World!'
# create a document element with a single label style
kmlobj = KML.kml(
    KML.Document(
        KML.Style(
            KML.LabelStyle(
                KML.scale(6)
            ),
            id="big_label"
        )
    )
)
# add placemarks to the Document element
for i in range(0,len(text)):
    if text[i] != ' ':
        kmlobj.Document.append(
            KML.Placemark(
                KML.name(text[i % len(text)]),
                KML.styleUrl('#big_label'),
                KML.Point(
                    KML.extrude(1),
                    KML.altitudeMode('relativeToGround'),
                    KML.coordinates('{lon},{lat},{alt}'.format(
                            lon=-70.0 + i*60.0/(len(text)-1),
                            lat=60.0,
                            alt=5000000,
                        ),
                    ),
                ),
            )
        )
print(etree.tostring(etree.ElementTree(kmlobj),pretty_print=True))
