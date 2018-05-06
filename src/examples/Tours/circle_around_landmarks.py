#!/usr/bin/env python
'''Generate a KML document of a tour based on rotating around locations.

'''
from pykml.factory import nsmap
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from pykml.parser import Schema
from lxml import etree

# define a variable for the Google Extensions namespace URL string
gxns = '{' + nsmap['gx'] + '}'

feature_list = [
    {
        'name':"Half Dome",
        'desc':'Northern Territory, central Australia',
        'lon':-119.53417,'lat':37.744728, 'tilt':45, 'range':3000,
    },
    {
        'name':"Ayers Rock",
        'desc':'Northern Territory, central Australia',
        'lon':131.035,'lat':-25.345, 'tilt':88, 'range':5000,
    },
    {
        'name':"Landscape Arch",
        'desc':'Arches National Park, Utah, USA',
        'lon':-109.607,'lat':38.791, 'tilt':60, 'range':500,
    },
    {
        'name':"Manicouagan Crater",
        'desc':'Quebec, Canada',
        'lon':-68.7, 'lat':51.38, 'tilt':45, 'range':100000,
    },
    {
        'name':"Upheaval Dome",
        'desc':'Canyonlands National Park, Utah, USA',
        'lon':-109.929, 'lat':38.437, 'tilt':60, 'range':4000,
    },
    {
        'name':"Racetrack Playa",
        'desc':'Death Valley, California, USA',
        'lon':-117.56, 'lat':36.679, 'tilt':45, 'range':8000
    },
    {
        'name':"Matterhorn",
        'desc':'Pennine Alps, Switzerland/Italy',
        'lon':7.6584, 'lat':45.9766, 'tilt':60, 'range':6000,
    },
]
# start with a base KML tour and playlist
tour_doc = KML.kml(
    KML.Document(
      GX.Tour(
        KML.name("Play me!"),
        GX.Playlist(),
      ),
      KML.Folder(
        KML.name('Features'),
        id='features',
      ),
    )
)
for feature in feature_list:
    #import ipdb; ipdb.set_trace()
    # fly to a space viewpoint
    tour_doc.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(5),
        GX.flyToMode("smooth"),
        KML.LookAt(
          KML.longitude(feature['lon']),
          KML.latitude(feature['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(0),
          KML.range(10000000.0),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )
    # fly to the feature
    tour_doc.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(5),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(feature['lon']),
          KML.latitude(feature['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(feature['tilt']),
          KML.range(feature['range']),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )
    # spin around the feature
    for aspect in range(0,360,10):
        tour_doc.Document[gxns+"Tour"].Playlist.append(
          GX.FlyTo(
            GX.duration(0.25),
            GX.flyToMode("smooth"),
            KML.LookAt(
              KML.longitude(feature['lon']),
              KML.latitude(feature['lat']),
              KML.altitude(0),
              KML.heading(aspect),
              KML.tilt(feature['tilt']),
              KML.range(feature['range']),
              KML.altitudeMode("relativeToGround"),
            )
          )
        )
    tour_doc.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(1.0)))
    
#    tour_doc.Document[gxns+"Tour"].Playlist.append(
#        GX.TourControl(GX.playMode("pause"))
#    )
    
    # add a placemark for the feature
    tour_doc.Document.Folder.append(
      KML.Placemark(
        KML.name("?"),
        KML.description(
            "<h1>{name}</h1><br/>{desc}".format(
                    name=feature['name'],
                    desc=feature['desc'],
            )
        ),
        KML.Point(
          KML.extrude(1),
          KML.altitudeMode("relativeToGround"),
          KML.coordinates("{lon},{lat},{alt}".format(
                  lon=feature['lon'],
                  lat=feature['lat'],
                  alt=50,
              )
          )
        ),
        id=feature['name'].replace(' ','_')
      )
    )
    # show the placemark balloon
    tour_doc.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(2.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                KML.visibility(1),
                GX.balloonVisibility(1),
                targetId=feature['name'].replace(' ','_')
              )
            )
          )
        )
    )
    
    tour_doc.Document[gxns+"Tour"].Playlist.append(GX.Wait(GX.duration(2.0)))
    
    tour_doc.Document[gxns+"Tour"].Playlist.append(
        GX.AnimatedUpdate(
          GX.duration(2.0),
          KML.Update(
            KML.targetHref(),
            KML.Change(
              KML.Placemark(
                GX.balloonVisibility(0),
                targetId=feature['name'].replace(' ','_')
              )
            )
          )
        )
    )
    # fly to a space viewpoint
    tour_doc.Document[gxns+"Tour"].Playlist.append(
      GX.FlyTo(
        GX.duration(5),
        GX.flyToMode("bounce"),
        KML.LookAt(
          KML.longitude(feature['lon']),
          KML.latitude(feature['lat']),
          KML.altitude(0),
          KML.heading(0),
          KML.tilt(0),
          KML.range(10000000.0),
          KML.altitudeMode("relativeToGround"),
        )
      ),
    )

# check that the KML document is valid using the Google Extension XML Schema
assert(Schema("kml22gx.xsd").validate(tour_doc))

print(etree.tostring(tour_doc, pretty_print=True))

# output a KML file (named based on the Python script)
outfile = file(__file__.rstrip('.py')+'.kml','w')
outfile.write(etree.tostring(tour_doc, pretty_print=True))
