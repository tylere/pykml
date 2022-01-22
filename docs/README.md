---
layout: default
title: Home
---

## Welcome to pyKML

*pyKML* is a Python package for creating, parsing, manipulating, and validating 
[KML](http://code.google.com/apis/kml/documentation/), a language for encoding
and annotating geographic data. KML is used by [Google Earth](https://earth.google.com/)
and other geospatial software packages.

*pyKML* is based on the [lxml.objectify](https://lxml.de/objectify.html) API
which provides a Pythonic API for working with XML documents.
*pyKML* adds additional functionality specific to the KML language.

KML comes in several flavors. *pyKML* can be used with KML documents that 
follow the base [OGC KML](http://www.opengeospatial.org/standards/kml/)
specification, the
[Google Extensions Namespace](http://code.google.com/apis/kml/documentation/kmlreference.html#kmlextensions), 
or a user-supplied extension to the base KML specification (defined by an XML
Schema document).

*pyKML* is open source and [available on GitHub](https://github.com/tylere/pykml/). 
[Bug reports, enhancement requests](https://github.com/tylere/pykml/issues) and
examples of using pyKML are appreciated.
[Packaged releases](http://pypi.python.org/pypi/pykml) can be found on the 
Python Package Index (PyPI). 
