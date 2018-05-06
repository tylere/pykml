#!/usr/bin/env python
'''Example of generating transitions between camera locations using splines 

Note that this example requires the scipy package
    http://pypi.python.org/pypi/scipy

References:

'''
from datetime import time, datetime
from time import mktime
from lxml import etree
from pykml.factory import KML_ElementMaker as KML
from pykml.factory import GX_ElementMaker as GX
from scipy.interpolate import interp1d

class Location():
    '''Class for storing location and orientation information'''
    latitude = None
    longitude = None
    altitude = None
    altitudeMode = None
    heading = None
    tilt = None
    roll = None
    range = None
    def __init__(self,
            longitude=None, latitude=None, 
            altitude=None, altitude_mode=None,
            heading=None, tilt=None, roll=None, range=None,
        ):
        if latitude != None: self.latitude = latitude
        if longitude != None: self.longitude = longitude
        if altitude != None: self.altitude = altitude
        if altitude_mode != None: self.altitude_mode = altitude_mode
        if heading != None: self.heading = heading
        if tilt != None: self.tilt = tilt
        if roll != None: self.roll = roll
        if range != None: self.range = range

def create_placemarks(location):
    
    pm = KML.Placemark()
    pm.append(
        KML.description(
            '<table border="1">'
            '<tr><th>latitude</th><td>{lat}</td>'
            '<tr><th>longitude</th><td>{lon}</td>'
            '<tr><th>altitude</th><td>{alt}</td>'
            '<tr><th>heading</th><td>{head}</td>'
            '<tr><th>tilt</th><td>{tilt}</td>'
            '<tr><th>roll</th><td>{roll}</td>'
            '</table>'.format(
                lat=location['loc'].latitude,
                lon=location['loc'].longitude,
                alt=location['loc'].altitude,
                head=location['loc'].heading,
                tilt=location['loc'].tilt,
                roll=location['loc'].roll,
            )
        )
    )
    pm.append(
        KML.TimeStamp(
            KML.when(location['time'].strftime('%Y-%m-%dT%H:%M:%SZ'))
        )
    )
    coord_list = [
        str(location['loc'].longitude),
        str(location['loc'].latitude),
    ]
    if location['loc'].altitude != None:
        coord_list.append(str(location['loc'].altitude))
    pm.append(
        KML.Point(
            KML.extrude(1),
            KML.altitudeMode('relativeToGround'),
            KML.coordinates(','.join(coord_list)),
        )
    )
    return pm


def create_camera_model_placemark(location):
    
    pm = KML.Placemark(
        KML.description(
            '<table border="1">'
            '<tr><th>latitude</th><td>{lat}</td>'
            '<tr><th>longitude</th><td>{lon}</td>'
            '<tr><th>altitude</th><td>{alt}</td>'
            '<tr><th>heading</th><td>{head}</td>'
            '<tr><th>tilt</th><td>{tilt}</td>'
            '<tr><th>roll</th><td>{roll}</td>'
            '</table>'.format(
                lat=location['loc'].latitude,
                lon=location['loc'].longitude,
                alt=location['loc'].altitude,
                head=location['loc'].heading,
                tilt=location['loc'].tilt,
                roll=location['loc'].roll,
            )
        ),
        KML.Model(
            KML.altitudeMode('relativeToGround'),
            KML.Location(
              KML.latitude(location['loc'].latitude),
              KML.longitude(location['loc'].longitude),
              KML.altitude(location['loc'].altitude),
            ),
            KML.Orientation(
              KML.heading(location['loc'].heading),
              KML.tilt(-location['loc'].tilt),
              KML.roll(location['loc'].roll),
            ),
            KML.Scale(
              KML.x(10),
              KML.y(10),
              KML.z(-10),
            ),
            KML.Link(
              KML.href('models/three_unit_lines.dae'),
            )
        )
    )
    return pm


def create_flyto_camera(location):
    
    flyto = GX.FlyTo(
        GX.duration(0.5),
        GX.flyToMode('smooth'),
    )
    flyto.append(
        KML.Camera(
            KML.longitude(location['loc'].longitude),
            KML.latitude(location['loc'].latitude),
            KML.altitude(location['loc'].altitude),
            KML.heading(location['loc'].heading),
            KML.tilt(location['loc'].tilt),
            KML.roll(location['loc'].roll),
            KML.altitudeMode('relativeToGround'),
        )
    )
    return flyto


def interpolate_location_series(
        known_positions,
        number_of_positions,
        horizontal_interp_method='cubic',
        altitude_interp_method='linear',
        heading_interp_method='linear',
        tilt_interp_method='linear',
        roll_interp_method='linear',
        temporal_interp_method='linear',
        ):
    '''Estimate location data structures based on interpolation'''
    nKnownPositions = len(known_positions)
    x = list(range(nKnownPositions))
    x_new = [1.0*i*(nKnownPositions-1)/number_of_positions for i in range(number_of_positions)]
    
    # interpolate locations
    # create an interpolation object
    lon_new = interp1d(
        x=x, 
        y=[dict['loc'].longitude for dict in known_positions],
        kind=horizontal_interp_method
    )(x_new)
    lat_new = interp1d(
        x=x, 
        y=[dict['loc'].latitude for dict in known_positions],
        kind=horizontal_interp_method
    )(x_new)
    alt_new = interp1d(
        x=x, 
        y=[dict['loc'].altitude for dict in known_positions],
        kind=altitude_interp_method
    )(x_new)
    # interpolate orientations
    heading_new = interp1d(
        x=x, 
        y=[dict['loc'].heading for dict in known_positions],
        kind=heading_interp_method
    )(x_new)
    tilt_new = interp1d(
        x=x, 
        y=[dict['loc'].tilt for dict in known_positions],
        kind=tilt_interp_method
    )(x_new)
    roll_new = interp1d(
        x=x, 
        y=[dict['loc'].roll for dict in known_positions],
        kind=roll_interp_method
    )(x_new)
    
    # interpolate time
    # convert datetimes to timestamps (floats)
    ts = [mktime(dict['time'].timetuple())+1e-6*dict['time'].microsecond
                                                for dict in known_positions]
    ts_new = interp1d(
        x=x, 
        y=ts,
        kind=temporal_interp_method
    )(x_new)
    # convert timestamps (floats) to datetimes
    time_new = [datetime.fromtimestamp(ts) for ts in ts_new]
    
    # construct a list of the interpolated locations
    new_loc_list = []
    for i in range(len(x_new)):
        temp = {}
        temp['loc'] = Location(
            latitude=lat_new[i],
            longitude=lon_new[i],
            altitude=alt_new[i],
            heading=heading_new[i],
            tilt=tilt_new[i],
            roll=roll_new[i],
        )
        temp['time'] = time_new[i]
        new_loc_list.append(temp)
    # return interpolated series
    return new_loc_list

def main():
    known_positions=[
        # outside GWC-1
        {'loc':Location(
            longitude=-122.0916728, latitude=37.42329373, altitude=2, 
            heading=0, tilt=0, roll=0, range=25,
            ),
         'time':datetime.strptime('2011-01-01','%Y-%m-%d'),},
        # over building
        {'loc':Location(longitude=-122.0905238, latitude=37.4222005, altitude=20,
            heading=92, tilt=80, roll=0, range=25,
            ),
         'time':datetime.strptime('2011-01-02','%Y-%m-%d'),},
        # back to ground level
        {'loc':Location(longitude=-122.088513, latitude=37.4223038, altitude=2,
            heading=92, tilt=80, roll=0, range=25,
            ),
         'time':datetime.strptime('2011-01-03','%Y-%m-%d'),},
        # under arch
        {'loc':Location(longitude=-122.087676, latitude=37.422365, altitude=5,
            heading=107, tilt=80, roll=0, range=25,
            ),
         'time':datetime.strptime('2011-01-04','%Y-%m-%d'),},
        # around building
        {'loc':Location(longitude=-122.086997, latitude=37.422113, altitude=5,
            heading=179, tilt=90, roll=0, range=25,
            ),
         'time':datetime.strptime('2011-01-05','%Y-%m-%d'),},
        # around building 2
        {'loc':Location(longitude=-122.0870075, latitude=37.421748, altitude=5,
            heading=181, tilt=90, roll=-60, range=25,
            ),
         'time':datetime.strptime('2011-01-06','%Y-%m-%d'),},
                     
        # around building (south side)
        {'loc':Location(longitude=-122.0875599, latitude=37.42149516, altitude=5,
            heading=270, tilt=90, roll=-60, range=25,
            ),
         'time':datetime.strptime('2011-01-07','%Y-%m-%d'),},                     
        # around building 3
        {'loc':Location(longitude=-122.088148, latitude=37.422131, altitude=5,
            heading=369, tilt=90, roll=-60, range=25,
            ),
         'time':datetime.strptime('2011-01-08','%Y-%m-%d'),},
    ]
    interp_positions = interpolate_location_series(
        known_positions,
        number_of_positions=100,
        #horizontal_interp_method='linear',
    )
    # create a folder of original placemarks
    fld1 = KML.Folder(KML.name('original'))
    for loc in known_positions:
        fld1.append(create_placemarks(loc))
    
    # create a folder of interpolated placemarks
    fld2 = KML.Folder(KML.name('interpolated'))
    for loc in interp_positions:
        fld2.append(create_placemarks(loc))
    
    # create a folder of models showing camera positions/orientations
    fld3 = KML.Folder(KML.name('cameras'))
    for loc in interp_positions:
        fld3.append(create_camera_model_placemark(loc))
    
    # create a tour of camera positions
    playlist = GX.Playlist()
    for loc in interp_positions:
        playlist.append(create_flyto_camera(loc))
    
    fld = KML.Folder(
        fld1,
        fld2,
        fld3,
        GX.Tour(playlist),
    )
    
    print(etree.tostring(fld, pretty_print=True))

    
if __name__=='__main__':
    main()
