# pyKML Tutorial

The following tutorial gives a brief overview of many of the features of pyKML. 
It is designed to run from within a Python or iPython shell, and assumes that 
pyKML has been installed and is part of your Python search path.  The tutorial 
is designed to be followed from start to finish.

For complete stand alone programs that demonstrate how to use pyKML, check out
the [examples](examples.md).


## Constructing KML from scratch

The pyKML library can be used to construct KML documents, using the 
[pykml-factory](modules.md#pykml-factory) module:


{% highlight python %}
# create a factory object that can create elements in the KML namespace
from pykml.factory import KML_ElementMaker as KML

# create an the object equivalent of a KML <name> element
name_object = KML.name("Hello World!")
{% endhighlight %}

If you are creating KML documents that utilize elements that are not part
of the default KML namespace, you will want to create an additional factory 
objects for each namespace.  
For example, the following creates factory objects that can
be used to create elements that are part of the ATOM and Google Extensions 
namespace:

{% highlight python %}
from pykml.factory import ATOM_ElementMaker as ATOM
from pykml.factory import GX_ElementMaker as GX
{% endhighlight %}

Documents with nested KML tags can be created by nesting the creation
of Python objects:

{% highlight python %}
pm1 = KML.Placemark(
      KML.name("Hello World!"),
      KML.Point(
        KML.coordinates("-64.5253,18.4607")
      )
    )
{% endhighlight %}

Once a pyKML object element has been created, a string representation can be 
generated by using the `.tostring()` method:

{% highlight python %}
from lxml import etree

print(etree.tostring(pm1))

# use the pretty_print keyword if you want something more readable
print(etree.tostring(pm1, pretty_print=True))
{% endhighlight %}

pyKML creates Python objects, which  can be passed around and 
later aggregated.  The following creates a second placemark object, and then 
groups the two placemarks together in a folder.

{% highlight python %} 
# create another placemark
pm2 = KML.Placemark(
      KML.name("A second placemark!"),
      KML.Point(
        KML.coordinates("-64.5358,18.4486")
      )
    )

# group the two placemarks in a folder
fld = KML.Folder(pm1, pm2)

print(etree.tostring(fld, pretty_print=True))
{% endhighlight %}
  
Objects representing KML elements can also be appended into objects that have
already been created.
For example, the following appends yet another placemark to the folder.

{% highlight python %} 
# create yet another placemark
pm3 = KML.Placemark(
      KML.name("A third placemark!")
    )

# append the placemark to the series already in the folder
fld.append(pm3)

print etree.tostring(fld, pretty_print=True)
{% endhighlight %}
  
Similarly, you can remove elements from an existing object.  
The following removes the second of three placemarks from the folder:

{% highlight python %} 
    # remove a particular placemark
    fld.remove(pm2)
    
    print(etree.tostring(fld, pretty_print=True))
{% endhighlight %}
  
Once you have a KML document, you can access elements using object attributes:

{% highlight python %} 
    print(fld.Placemark.name.text)
{% endhighlight %}
  
This type of attribute-based access is provided by the *lxml* packages's
*objectify API*.
pyKML users are encouraged to familiarize themselves with the 
[objectify API documentation](http://lxml.de/objectify.html) on the lxml website,
because pyKML inherits this functionality.


## Parsing existing KML documents

Sometimes instead of building a KML document from scratch, you may want to 
modify an existing KML document.  For this case, pyKML's parsing capabilities
are useful.  pyKML can parse information from a variety of sources, including
strings, local files, and remote URLs.  

The most straightforward is parsing from a string...

{% highlight python %}
from pykml import parser

kml_str = '<kml xmlns="http://www.opengis.net/kml/2.2">' \
          '<Document>' \
            '<Folder>' \
              '<name>sample folder</name>' \
            '</Folder>' \
          '</Document>' \
        '</kml>'

root = parser.fromstring(kml_str)

print(root.Document.Folder.name.text)
{% endhighlight %}
  
You can also parse a local file...

{% highlight python %}
from os import path

kml_file = path.join( \
  '../src/pykml/test', \
  'testfiles/google_kml_developers_guide', \
  'complete_tour_example.kml')

with open(kml_file) as f:
doc = parser.parse(f)
{% endhighlight %}
  
... or a remote URL...

{% highlight python %}
import urllib2

url = 'http://code.google.com/apis/kml/documentation/KML_Samples.kml'
fileobject = urllib2.urlopen(url)
root = parser.parse(fileobject).getroot()
print(root.Document.name)
{% endhighlight %}
  
## Validation of KML documents

KML documents that you create can be validated against XML Schema documents,
which define the rules of which elements are acceptible and what ordering can 
be used.  Both the OGC KML schema and the Google Extension schemas are included 
with pyKML.

To validate your KML document, first create instances of the schemas:

{% highlight python %}
from pykml.parser import Schema

schema_ogc = Schema("ogckml22.xsd")
schema_gx = Schema("kml22gx.xsd")
{% endhighlight %}
  
Then use the schemas to validate your KML objects, using the `.validate()` 
or `.assertValid()` methods.  
The following code creates a small invalide KML document which
includes an element from the Google Extension namespace (`<gx_Tour>`) so 
the document does not validate against the basic OGC KML schema, but does
validate agains the Google Extensions schema. 

{% highlight python %}
# create a small KML document
doc = KML.kml(GX.Tour())

# validate it against the OGC KML schema
schema_ogc.validate(doc)

# validate it against the Google Extension schema
schema_gx.validate(doc)
{% endhighlight %}
  
The `.validate()` method only returns `True` or `False`.  For invalid documents, 
it is often useful to obtain details of why the document is invalid
using the `.assertValid()` method:
    
{% highlight python %}
# validate against the OGC KML schema, and generate an exception
schema_ogc.assertValid(doc)
{% endhighlight %}
  
You can also validate while parsing by including a schema object as a parameter.

{% highlight python %}
# the following triggers an error because <eggplant> is not a valid OGC KML element
bad_kml_str = '<kml xmlns="http://www.opengis.net/kml/2.2">' \
              '<Document>' \
                '<Folder>' \
                  '<eggplant/>' \
                 '</Folder>' \
              '</Document>' \
            '</kml>'

root = parser.fromstring(bad_kml_str, schema_ogc)
{% endhighlight %}

## Setting the Number of Decimal Places

Many KML files, especially those authored by Google Earth, contain coordinate
information with more decimal places that often is necessary.  
The `set_max_decimal_places()` function addresses this, by allowing a user
to reduce the number of decimal places used.  The example below demonstrates 
this for a previously created placemark.

{% highlight python %}
from pykml.helpers import set_max_decimal_places

print(etree.tostring(pm1, pretty_print=True))

# set the coordinate precision to something smaller
set_max_decimal_places(
         pm1, 
         max_decimals={
             'longitude': 2,
             'latitude': 1,
          }
        )

# note that the coordinate values have changed
print(etree.tostring(pm1, pretty_print=True))
{% endhighlight %}


## Building pyKML Python Scripts

While pyKML allows you use leverage programming to create
customized KML files, writing the initial pyKML code can be tedious.
To help with this, pyKML provides the verbosely named
`.write_python_script_for_kml_document()` function which will produce
a Python script that can serve as a starting point for further customization.

{% highlight python %}
from pykml.factory import write_python_script_for_kml_document

url = 'http://code.google.com/apis/kml/documentation/kmlfiles/altitudemode_reference.kml'

fileobject = urllib2.urlopen(url)
doc = parser.parse(fileobject).getroot()
script = write_python_script_for_kml_document(doc)
print(script)
{% endhighlight %}

That concludes the tutorial.  For further examples of how pyKML can be used, 
head on over to the [examples](examples.md) section of the documentation.