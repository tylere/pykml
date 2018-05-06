#!/usr/bin/python

# example virtual base jump
import math
from lxml import etree
from pykml.parser import Schema
from pykml.factory import KML_ElementMaker as kml
from pykml.factory import ATOM_ElementMaker as atom
from pykml.factory import GX_ElementMaker as gx

GX_ns = "{http://www.google.com/kml/ext/2.2}"

def drange(start, stop, step):
    "create a decimal range list"
    r = start
    while r < stop:
        yield r
        r += step

# top of half dome
loc0 = {
    'latitude': 37.74594,     #37.745,
    'longitude': -119.53385,   #-119.53500,
    'altitude': 2676,
    'tilt': 90,
    'heading': -93,
    'roll': 0,
}
# bottom of half dome
loc1 = {
    'latitude': 37.74829,
    'longitude': -119.543987,
    'altitude': 1400,
    'tilt': 0,
    'heading': -93,
    'roll': 0,
}

g = -9.8  # vertical acceleration m/s2
t0 = 0
vz = 20  # initial vertical velocity (m/s)

# determine how long it takes to get to alt1
z0 = loc0['altitude']
z1 = loc1['altitude']
deltat = (-vz - math.sqrt(vz**2 - 2*g*(z0-z1))) / g
deltat = 30  # set manually, not sure what is wrong with the previous eqn

#import ipdb; ipdb.set_trace()

# calculate the horizontal and rotational velocities
vy = (loc1['latitude'] - loc0['latitude']) / deltat
vx = (loc1['longitude'] - loc0['longitude']) / deltat
vh = (loc1['heading'] - loc0['heading']) / deltat
vt = (loc1['tilt'] - loc0['tilt']) / deltat

# create a tour object
tour_doc = kml.kml(
    kml.Folder(
        gx.Tour(
          kml.name("Play me!"),
          gx.Playlist(),
        )
    )
)

tstep = 0.1
for t in drange(0,15,tstep):
    pm = kml.Placemark(
        kml.name(str(t)),
        kml.Point(
            kml.altitudeMode("absolute"),
            kml.coordinates("{lon},{lat},{alt}".format(
                lon=loc0['longitude'] + vx*t,
                lat=loc0['latitude'] + vy*t,
                alt=loc0['altitude'] + vz*t + 0.5*g*t**2,
            )),
            
        )
    )
    tour_doc.Folder.append(pm)
    
    flyto = gx.FlyTo(
        gx.duration(tstep),
        gx.flyToMode("smooth"),
        kml.Camera(
          kml.longitude(loc0['longitude'] + vx*t),
          kml.latitude(loc0['latitude'] + vy*t),
          kml.altitude(loc0['altitude'] + vz*t + 0.5*g*t**2),
          kml.heading(loc0['heading'] + vh*t),
          kml.tilt(loc0['tilt'] + vt*t),
          kml.altitudeMode("absolute"),
        )
    )
    tour_doc.Folder[GX_ns+"Tour"].Playlist.append(flyto)
    

assert Schema('kml22gx.xsd').validate(tour_doc)
print(etree.tostring(tour_doc, pretty_print=True))

# output a KML file (named based on the Python script)
outfile = file(__file__.rstrip('.py')+'.kml','w')
outfile.write(etree.tostring(tour_doc, pretty_print=True))