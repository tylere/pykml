import unittest
from os import path
from lxml import etree
from pykml.parser import Schema
from pykml.parser import parse
from pykml.factory import KML_ElementMaker as KML

class KmlUtilTestCase(unittest.TestCase):
    
    def test_count_elements(self):
        """Tests the counting of elements in a KML document."""
        from pykml.util import count_elements
        
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('kml22gx.xsd'))
        summary = count_elements(doc)
        
        self.assertTrue('http://www.opengis.net/kml/2.2' in summary)
        self.assertEqual(4,
            summary['http://www.opengis.net/kml/2.2']['Placemark']
        )
        self.assertTrue('http://www.google.com/kml/ext/2.2' in summary)
        self.assertEqual(5,
            summary['http://www.google.com/kml/ext/2.2']['FlyTo']
        )
        self.assertEqual(2,
            summary['http://www.google.com/kml/ext/2.2']['Wait']
        )
    
    def test_wrap_angle180(self):
        """Tests the wrap_angle180 utility function."""
        from pykml.util import wrap_angle180
        
        self.assertEqual(wrap_angle180(0), 0)
        self.assertEqual(wrap_angle180(180), -180)
        self.assertEqual(wrap_angle180(361), 1)
        # test passing an array
        self.assertEqual(wrap_angle180([0,180,361,]), [0,-180,1,])

    def test_to_wkt_list_simple_polygon(self):
        """Tests the to_wkt_list function for a polygon with inner rings."""
        from pykml.util import to_wkt_list
        
        # create a polygon
        poly = KML.Polygon(
            KML.extrude('1'),
            KML.altitudeMode('relativeToGround'),
            KML.outerBoundaryIs(
              KML.LinearRing(
                KML.coordinates(
                '-122.366278,37.818844,30 '
                '-122.365248,37.819267,30 '
                '-122.365640,37.819861,30 '
                '-122.366669,37.819429,30 '
                '-122.366278,37.818844,30 '
                ),
              ),
            ),
          )
        
        poly_wkt_list = to_wkt_list(poly)
        
        self.assertEqual(len(poly_wkt_list), 1)
        self.assertEqual(
            poly_wkt_list[0], 
            ('POLYGON ((-122.366278 37.818844 30, '
                       '-122.365248 37.819267 30, '
                       '-122.365640 37.819861 30, '
                       '-122.366669 37.819429 30, '
                       '-122.366278 37.818844 30))')
        )

    
    def test_to_wkt_list_complex_polygon(self):
        """Tests the to_wkt_list function for a polygon with inner rings."""
        from pykml.util import to_wkt_list
        
        # create a polygon
        poly = KML.Polygon(
            KML.extrude('1'),
            KML.altitudeMode('relativeToGround'),
            KML.outerBoundaryIs(
              KML.LinearRing(
                KML.coordinates(
                '-122.366278,37.818844,30 '
                '-122.365248,37.819267,30 '
                '-122.365640,37.819861,30 '
                '-122.366669,37.819429,30 '
                '-122.366278,37.818844,30 '
                ),
              ),
            ),
            KML.innerBoundaryIs(
              KML.LinearRing(
                KML.coordinates(
                '-122.366212,37.818977,30 '
                '-122.365424,37.819294,30 '
                '-122.365704,37.819731,30 '
                '-122.366212,37.818977,30 '
                ),
              ),
            ),
            KML.innerBoundaryIs(
              KML.LinearRing(
                KML.coordinates(
                '-122.366212,37.818977,30 '
                '-122.365704,37.819731,30 '
                '-122.366488,37.819402,30 '
                '-122.366212,37.818977,30 '
                ),
              ),
            ),
          )
        
        poly_wkt_list = to_wkt_list(poly)
        
        self.assertEqual(len(poly_wkt_list), 1)
        self.assertEqual(
            poly_wkt_list[0], 
            ('POLYGON ((-122.366278 37.818844 30, '
                       '-122.365248 37.819267 30, '
                       '-122.365640 37.819861 30, '
                       '-122.366669 37.819429 30, '
                       '-122.366278 37.818844 30), '
                      '(-122.366212 37.818977 30, '
                       '-122.365424 37.819294 30, '
                       '-122.365704 37.819731 30, '
                       '-122.366212 37.818977 30), '
                      '(-122.366212 37.818977 30, '
                       '-122.365704 37.819731 30, '
                       '-122.366488 37.819402 30, '
                       '-122.366212 37.818977 30))')
        )
    
    def test_getXmlWithCDATA(self):
        '''tests the format_as_cdata function'''
        from pykml.util import format_xml_with_cdata
        
        kmlobj = KML.kml(
            KML.Document(
                KML.Placemark(
                    KML.name('foobar'),
                    KML.styleUrl('#big_label'),
                    KML.description('<html>'),
                    KML.text('<html>'),
                    KML.linkDescription('<html>'),
                    KML.displayName('<html>')
                )
            )
        )
        self.assertEqual(
            etree.tostring(format_xml_with_cdata(kmlobj)),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2"'
                          ' xmlns:atom="http://www.w3.org/2005/Atom"'
                          ' xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>foobar</name>'
                  '<styleUrl>#big_label</styleUrl>'
                  '<description><![CDATA[<html>]]></description>'
                  '<text><![CDATA[<html>]]></text>'
                  '<linkDescription><![CDATA[<html>]]></linkDescription>'
                  '<displayName><![CDATA[<html>]]></displayName>'
                '</Placemark>'
              '</Document>'
            '</kml>'
        )
    
    def test_convert_csv_to_kml(self):
        """Tests the convert_csv_to_kml function"""
        import tempfile
        from pykml.util import convert_csv_to_kml
        from pykml.util import format_xml_with_cdata
        
        # create a CSV file for testing
        csvfile = tempfile.TemporaryFile()
        csvfile.write('name,snippet,lat,lon\n')
        csvfile.write('first,The first one,45.0,-90.0\n')
        csvfile.write('second,The second one,46.0,-89.0\n')
        csvfile.write('third,"The third one (with quotes)",45.0,-88.0\n')
        csvfile.seek(0)
        
        kmldoc = convert_csv_to_kml(csvfile)
        
        csvfile.close()
        
        self.assertEqual(
            etree.tostring(format_xml_with_cdata(kmldoc)),
            '<kml xmlns:gx="http://www.google.com/kml/ext/2.2" '
                 'xmlns:atom="http://www.w3.org/2005/Atom" '
                 'xmlns="http://www.opengis.net/kml/2.2">'
                 '<Document>'
                    '<Folder>'
                        '<name>KmlFile</name>'
                        '<Placemark>'
                            '<name>first</name>'
                            '<Snippet maxLines="2">The first one</Snippet>'
                            '<description>'
                                '<![CDATA['
                                  '<table border="1"'
                                    '<tr><th>snippet</th><td>The first one</td></tr>'
                                    '<tr><th>lat</th><td>45.0</td></tr>'
                                    '<tr><th>lon</th><td>-90.0</td></tr>'
                                    '<tr><th>name</th><td>first</td></tr>'
                                  '</table>'
                                ']]>'
                            '</description>'
                            '<Point>'
                                '<coordinates>-90.0,45.0</coordinates>'
                            '</Point>'
                        '</Placemark>'
                        '<Placemark>'
                            '<name>second</name>'
                            '<Snippet maxLines="2">The second one</Snippet>'
                            '<description><![CDATA[<table border="1"<tr><th>snippet</th><td>The second one</td></tr><tr><th>lat</th><td>46.0</td></tr><tr><th>lon</th><td>-89.0</td></tr><tr><th>name</th><td>second</td></tr></table>]]></description>'
                            '<Point>'
                                '<coordinates>-89.0,46.0</coordinates>'
                            '</Point>'
                        '</Placemark>'
                        '<Placemark>'
                            '<name>third</name>'
                            '<Snippet maxLines="2">The third one (with quotes)</Snippet>'
                            '<description><![CDATA[<table border="1"<tr><th>snippet</th><td>The third one (with quotes)</td></tr><tr><th>lat</th><td>45.0</td></tr><tr><th>lon</th><td>-88.0</td></tr><tr><th>name</th><td>third</td></tr></table>]]></description>'
                            '<Point>'
                                '<coordinates>-88.0,45.0</coordinates>'
                            '</Point>'
                        '</Placemark>'
                    '</Folder>'
                '</Document>'
            '</kml>'
        )
    
    def test_convert_csv_to_kml_missing_coordinate_fields(self):
        """Tests the convert_csv_to_kml function"""
        import tempfile
        from pykml.util import convert_csv_to_kml
        
        # create a CSV file for testing
        csvfile = tempfile.TemporaryFile()
        csvfile.write('name,snippet,y,x\n')
        csvfile.write('first,The first one,45.0,-90.0\n')
        csvfile.write('second,The second one,46.0,-89.0\n')
        csvfile.seek(0)
        
        try:
            convert_csv_to_kml(csvfile)
        except KeyError:
            self.assertTrue(True)
        except:
            raise
        finally:
            csvfile.close()

    def test_clean_xml_string(self):
        from pykml.util import clean_xml_string
        self.assertEqual(clean_xml_string('\xce'),'')
        #self.assertEqual(clean_xml_string('Grande-\xcele'),'Grande-le')
