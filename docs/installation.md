# Installing pyKML

## Linux Installation

### Installing the Dependencies

pyKML depends on the [lxml](http://codespeak.net/lxml) Python library, which in turn depends on two 
C libraries:
[libxml2](http://xmlsoft.org/) and [libxslt](http://xmlsoft.org/XSLT/).
Given this, the first step to installing pyKML is to get `lxml` running on your system. 
Refer to the `lxml` website for
[instructions on how to install lxml](http://lxml.de/installation.html).

To verify that the lxml library has been installed correctly, 
open up a Python shell and type:

{% highlight python %}
import lxml
{% endhighlight %}

If you don't get back an error message, lxml has been installed and you are 
ready to proceed.


### Installing the pyKML package

pyKML itself can be installed from the Python Package Index, 
using [pip](http://pypi.python.org/pypi/pip):

{% highlight shell %}
pip install pykml
{% endhighlight %}

To verify that the pyKML library has been installed correctly, 
open up a Python shell and type:

{% highlight python %}
import pykml
{% endhighlight %}

Once again, if you don't get back an error, pyKML has been installed correctly. 
To learn how to start using pyKML, head on over to the [tutorial](tutorial.md).
