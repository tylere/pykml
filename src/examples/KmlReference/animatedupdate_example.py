#!/usr/bin/env python
'''Generate a KML string that matches the animated update example.

References:
http://code.google.com/apis/kml/documentation/kmlreference.html#gxanimatedupdate
http://code.google.com/apis/kml/documentation/kmlfiles/animatedupdate_example.kml

Note that as of 12/1/2010, the KML code displayed beneath the animatedupdate_example.kml link
is not valid.
* The <scale> element should not be a subelement of <Icon>.
* The <gx:duration> element should be the first subelement of <gx:FlyTo>
'''

from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX

doc = KML.kml(
  KML.Document(
    KML.name("gx:AnimatedUpdate example"),
    KML.Style(
      KML.IconStyle(
        KML.scale(1.0),
        KML.Icon(
          KML.href("http://maps.google.com/mapfiles/kml/pushpin/ylw-pushpin.png"),
        ),
        id="mystyle"
      ),
      id="pushpin"
    ),
    KML.Placemark(
      KML.name("Pin on a mountaintop"),
      KML.styleUrl("#pushpin"),
      KML.Point(
        KML.coordinates(170.1435558771009,-43.60505741890396,0)
      ),
      id="mountainpin1"
    ),
    GX.Tour(
      KML.name("Play me!"),
      GX.Playlist(
        GX.FlyTo(
          GX.duration(3),
          GX.flyToMode("bounce"),
          KML.Camera(
            KML.longitude(170.157),
            KML.latitude(-43.671),
            KML.altitude(9700),
            KML.heading(-6.333),
            KML.tilt(33.5),
          )
        ),
        GX.AnimatedUpdate(
          GX.duration(5),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.IconStyle(
                KML.scale(10.0),
                targetId="mystyle"
              )
            )
          )
        ),
        GX.Wait(
          GX.duration(5)
        )
      )
    )
  )
)

print(etree.tostring(doc, pretty_print=True))

# output a KML file (named based on the Python script)
outfile = file(__file__.rstrip('.py')+'.kml','w')
outfile.write(etree.tostring(doc, pretty_print=True))

schema = Schema('kml22gx.xsd')
import ipdb; ipdb.set_trace()
schema.validate(doc)
