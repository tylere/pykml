import unittest
from os import path
try:  # Python2 support
    import urllib2
    URLError = urllib2.URLError
except ImportError:  # Python3 support
    import urllib.request as urllib2
    from urllib.error import URLError
try:  # Python2 support
    from StringIO import StringIO
except ImportError:  # Python3 support
    from io import StringIO

from lxml import etree
from pykml.parser import Schema
from pykml.parser import fromstring
from pykml.parser import parse


class ValidatorTestCase(unittest.TestCase):

    def test_initialize_schema(self):
        """Tests the creation Schema instance"""
        schema = Schema("ogckml22.xsd")
        self.assertTrue(isinstance(schema.schema, etree.XMLSchema))

    def test_initialize_schema_remote_url(self):
        schema = Schema("http://code.google.com/apis/kml/schema/kml22gx.xsd")
        self.assertTrue(isinstance(schema.schema, etree.XMLSchema))


class ParseKmlOgcTestCase(unittest.TestCase):
    "A collection of tests related to parsing KML OGC documents"

    def test_fromstring_kml_document(self):
        "Tests the parsing of an valid KML string"
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'
        tree = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
        self.assertEqual(etree.tostring(tree).decode(), test_kml)
        tree = fromstring(test_kml)
        self.assertEqual(etree.tostring(tree).decode(), test_kml)

    def test_fromstring_invalid_kml_document(self):
        "Tests the parsing of an invalid KML string"
        test_kml = '<bad_element />'
        try:
            tree = fromstring(test_kml, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_parse_kml_document(self):
        "Tests the parsing of an valid KML file object"
        test_kml = '<kml xmlns="http://www.opengis.net/kml/2.2"/>'
        fileobject = StringIO(test_kml)
        schema = Schema("ogckml22.xsd")
        tree = parse(fileobject, schema=schema)
        self.assertEqual(etree.tostring(tree).decode(), test_kml)
        tree = parse(fileobject, schema=schema)
        self.assertEqual(etree.tostring(tree).decode(), test_kml)

    def test_parse_invalid_kml_document(self):
        "Tests the parsing of an invalid KML document"
        fileobject = StringIO('<bad_element />')
        try:
            tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_parse_kml_url(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/KML_Samples.kml'
        #url = 'http://kml-samples.googlecode.com/svn/trunk/kml/Document/doc-with-id.kml'
        #url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        #url = 'http://code.google.com/apis/kml/documentation/kmlfiles/animatedupdate_example.kml'
        try:
            fileobject = urllib2.urlopen(url)
            tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
            self.assertEqual(
                etree.tostring(tree)[:78].decode(),
                '<kml xmlns="http://www.opengis.net/kml/2.2">'
                  '<Document>'
                    '<name>KML Samples</name>'
            )
        except URLError:
            print('Unable to access the URL. Skipping test...')

    def test_parse_kml_file_with_cdata(self):
        "Tests the parsing of a local KML file, with a CDATA description string"
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_tutorial/using_the_cdata_element.kml'
        )
        # parse with validation
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('ogckml22.xsd'))
        self.assertEqual(
            etree.tostring(doc).decode(),
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>CDATA example</name>'
                  '<description>'
                    '<![CDATA[\n'
                    '          <h1>CDATA Tags are useful!</h1>\n'
                    '          <p><font color="red">Text is <i>more readable</i> and \n'
                    '          <b>easier to write</b> when you can avoid using entity \n'
                    '          references.</font></p>\n'
                    '        ]]>'
                  '</description>'
                '<Point>'
                  '<coordinates>102.595626,14.996729</coordinates>'
                '</Point>'
              '</Placemark>'
            '</Document>'
          '</kml>'
        )
        # parse without validation
        with open(test_datafile) as f:
            doc2 = parse(f)
        self.assertEqual(
            etree.tostring(doc2).decode(),
            '<kml xmlns="http://www.opengis.net/kml/2.2">'
              '<Document>'
                '<Placemark>'
                  '<name>CDATA example</name>'
                  '<description>'
                    '<![CDATA[\n'
                    '          <h1>CDATA Tags are useful!</h1>\n'
                    '          <p><font color="red">Text is <i>more readable</i> and \n'
                    '          <b>easier to write</b> when you can avoid using entity \n'
                    '          references.</font></p>\n'
                    '        ]]>'
                  '</description>'
                '<Point>'
                  '<coordinates>102.595626,14.996729</coordinates>'
                '</Point>'
              '</Placemark>'
            '</Document>'
          '</kml>'
        )

    def test_parse_invalid_ogc_kml_document(self):
        """Tests the parsing of an invalid KML document.  Note that this KML
        document uses elements that are not in the OGC KML spec.
        """
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        try:
            fileobject = urllib2.urlopen(url)
            tree = parse(fileobject, schema=Schema("ogckml22.xsd"))
            self.assertTrue(False)
        except URLError:
            print('Unable to access the URL. Skipping test...')
        except etree.XMLSyntaxError:
            self.assertTrue(True)
        except:
            self.assertTrue(False)


class ParseKmlGxTestCase(unittest.TestCase):
    "A collection of tests related to parsing KML Google Extension documents"

    def test_parse_kml_url(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'
        try:
            fileobject = urllib2.urlopen(url)
            tree = parse(fileobject, schema=Schema('kml22gx.xsd'))
            self.assertEqual(
                etree.tostring(tree)[:185].decode(),
                '<kml xmlns="http://www.opengis.net/kml/2.2" '
                     'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                    '<!-- required when using gx-prefixed elements -->'
                    '<Placemark>'
                      '<name>gx:altitudeMode Example</name>'
            )
        except URLError:
            print('Unable to access the URL. Skipping test...')

    def test_parse_kml_file(self):
        "Tests the parsing of a local KML file, with validation"
        test_datafile = path.join(
            path.dirname(__file__),
            'testfiles',
            'google_kml_developers_guide/complete_tour_example.kml'
        )
        # parse without validation
        with open(test_datafile) as f:
            doc = parse(f)
        # parse with validation (local schema file)
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('kml22gx.xsd'))
        # parse with validation (remote schema file)
        with open(test_datafile) as f:
            doc = parse(f, schema=Schema('http://code.google.com/apis/kml/schema/kml22gx.xsd'))
        self.assertTrue(True)

    def test_parse_kml_url_2(self):
        "Tests the parsing of a KML URL"
        url = 'http://code.google.com/apis/kml/documentation/kmlfiles/animatedupdate_example.kml'
        try:
            fileobject = urllib2.urlopen(url)
            tree = parse(fileobject, schema=Schema('kml22gx.xsd'))
            self.assertEqual(
                etree.tostring(tree)[:137].decode(),
                '<kml xmlns="http://www.opengis.net/kml/2.2" '
                     'xmlns:gx="http://www.google.com/kml/ext/2.2">'
                    '<Document>'
                      '<name>gx:AnimatedUpdate example</name>'
            )
        except URLError:
            print('Unable to access the URL. Skipping test...')

if __name__ == '__main__':
    unittest.main()
