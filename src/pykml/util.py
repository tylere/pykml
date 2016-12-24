""" pyKML Utility Module

The pykml.utility module provides utility functions that operate on KML 
documents
"""
import re

def clean_xml_string(input_string):
    '''removes invalid characters from an XML string'''
    from curses import ascii
    return ''.join(c for c in input_string if ascii.isascii(c))

def format_xml_with_cdata(
        obj, 
        cdata_elements = ['description', 'text', 'linkDescription', 'displayName']
    ):
    from lxml import etree

    # Convert Objectify document to lxml.etree (is there a better way?)
    root = etree.fromstring(etree.tostring(etree.ElementTree(obj)))
    
    #Create an xpath expression to search for all desired cdata elements
    xpath = '|'.join(map(lambda tag: '//kml:' + tag, cdata_elements))
    
    results = root.xpath(
        xpath,
        namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}
    )
    for element in results:
        element.text = etree.CDATA(element.text)
    return root

def count_elements(doc):
    "Counts the number of times each element is used in a document"
    summary = {}
    for el in doc.iter():
        try:
            namespace, element_name = re.search('^{(.+)}(.+)$', el.tag).groups()
        except:
            namespace = None
            element_name = el.tag
        if not summary.has_key(namespace):
            summary[namespace] = {}
        if not summary[namespace].has_key(element_name):
            summary[namespace][element_name] = 1
        else:
            summary[namespace][element_name] += 1
    return summary

def wrap_angle180(angle):
    # returns an angle such that -180 < angle <= 180
    try:
        # if angle is a sequence
        return [((a+180) % 360 ) - 180 for a in angle]
    except TypeError:
        return ((angle+180) % 360 ) - 180

def to_wkt_list(doc):
    '''converts all geometries to Well Know Text format'''
    from lxml import etree
    
    def ring_coords_to_wkt(ring):
        '''converts LinearRing coordinates to WKT style coordinates'''
        return(
            (
               ring.coordinates.text.strip()
            ).replace(' ','@@').replace(',',' ').replace('@@',', ')
        )
    
    ring_wkt_list = []
    context = etree.iterwalk(
             doc,
             events=("start",)
    )
    for action, elem in context:
        if elem.tag in ['{http://www.opengis.net/kml/2.2}Polygon',
                        '{http://www.opengis.net/kml/2.2}MultiPolygon']:
            #print("%s: %s" % (action, elem.tag))
            if elem.tag == '{http://www.opengis.net/kml/2.2}Polygon':
                
                # outer boundary
                ringlist = [
                    '({0})'.format(
                        ring_coords_to_wkt(elem.outerBoundaryIs.LinearRing)
                    )
                ]
                for obj in elem.findall('{http://www.opengis.net/kml/2.2}innerBoundaryIs'):
                    ringlist.append(
                        '({0})'.format(
                            ring_coords_to_wkt(obj.LinearRing)
                        )
                    )
                
                wkt = 'POLYGON ({rings})'.format(rings=', '.join(ringlist))
                ring_wkt_list.append(wkt)
    return(ring_wkt_list)


def convert_csv_to_kml(
        fileObj,
        latitude_field='latitude',
        longitude_field='longitude',
        altitude_field='altitude',
        name_field='name',
        description_field='description',
        snippet_field='snippet',
    ):
    '''Reads a CSV document from a file-like object and converts it to KML'''
    
    import csv
    #import urllib2
    from pykml.factory import KML_ElementMaker as KML
    
    # create a basic KML document
    kmldoc = KML.kml(KML.Document(
        KML.Folder(
            KML.name("KmlFile"))
        )
    )
    
    csvdoc = csv.DictReader(fileObj)
    
    # if field is not found, check for other common field names
    if latitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['latitude','lat']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            latitude_field = match_field
    if longitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['longitude','lon','long']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            longitude_field = match_field
    if altitude_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['altitude','alt']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            altitude_field = match_field
    if name_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['name']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            name_field = match_field
    if snippet_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['snippet']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            snippet_field = match_field
    if description_field not in csvdoc.fieldnames:
        match_field = None
        for name in ['description','desc']:
            try:
                match_field = csvdoc.fieldnames[[s.lower() for s in csvdoc.fieldnames].index(name)]
                break
            except:
                pass
        if match_field is not None:
            description_field = match_field

    # check that latitude and longitude columns can be found
    if latitude_field not in csvdoc.fieldnames:
        raise KeyError(
            'Latitude field ({0}) was not found in the CSV file '
            'column names {1}'.format(latitude_field,csvdoc.fieldnames)
        )
    if longitude_field not in csvdoc.fieldnames:
        raise KeyError(
            'Longitude field ({0}) was not found in the CSV file '
            'column names {1}'.format(longitude_field,csvdoc.fieldnames)
        )    
    for row in csvdoc:
        pm = KML.Placemark()
        if row.has_key(name_field):
            pm.append(
                KML.name(clean_xml_string(row[name_field]))
            )
        if row.has_key(snippet_field):
            pm.append(
                KML.Snippet(clean_xml_string(row[snippet_field]),maxLines="2")
            )
        if row.has_key(description_field):
            pm.append(
                KML.description(clean_xml_string(row[description_field]))
            )
        else:
            desc = '<table border="1"'
            for key,val in row.iteritems():
                desc += '<tr><th>{0}</th><td>{1}</td></tr>'.format(key,val)
            desc += '</table>'
            pm.append(KML.description(clean_xml_string(desc)))
        
        coord_list = [row[longitude_field], row[latitude_field]]
        if row.has_key(altitude_field):
            coord_list += [row[altitude_field]]
        pm.append(
            KML.Point(
                KML.coordinates(','.join(coord_list))
            )
        )
        kmldoc.Document.Folder.append(pm)
    return kmldoc


def csv2kml():
    """Parse a CSV file and generates a KML document
    
    Example: csv2kml test.csv
    """
    import sys
    import urllib2
    from optparse import OptionParser
    from lxml import etree
    
    parser = OptionParser(
        usage="usage: %prog FILENAME_or_URL",
        version="%prog 0.1",
    )
    parser.add_option("--longitude_field", dest="longitude_field",
                  help="name of the column that contains longitude data")
    parser.add_option("--latitude_field", dest="latitude_field",
                  help="name of the column that contains latitude data")
    parser.add_option("--altitude_field", dest="altitude_field",
                  help="name of the column that contains altitude data")
    parser.add_option("--name_field", dest="name_field",
                  help="name of the column used for the placemark name")
    parser.add_option("--description_field", dest="description_field",
                  help="name of the column used for the placemark description")
    parser.add_option("--snippet_field", dest="snippet_field",
                  help="name of the column used for the placemark snippet text")
    (options, args) = parser.parse_args()
    if len(args) != 1:
        parser.error("wrong number of arguments")
    else:
        uri = args[0]
    
    # try to open the URI as both a local file and a remote URL
    try:
        f = open(uri)
    except IOError:
        try:
            f = urllib2.urlopen(uri)
        except ValueError:
            raise ValueError('unable to load URI {0}'.format(uri))
    except:
        raise
    
    kmldoc = convert_csv_to_kml(f,
        latitude_field = options.latitude_field,
        longitude_field = options.longitude_field,
        altitude_field = options.altitude_field,
        name_field = options.name_field,
        description_field = options.description_field,
        snippet_field = options.snippet_field,
    )

    # close the fileobject, if needed
    try:
        f
    except NameError:
        pass #variable was not defined
    else:
        f.close
    
    kmlstr = format_as_cdata(etree.tostring(kmldoc, pretty_print=True))
    sys.stdout.write(kmlstr)