# colorize

CLI utility and GIMP plug-in for sending/receiving images to
ColorfulImageColorization.

[*Colorful Image Colorization*](http://richzhang.github.io/colorization/) is a
system that takes a grayscale photograph as input and returns  a plausible color
version of the photograph. It was created by Richard Zhang, Phillip Isola and
Alexei A. Efros. The system is hosted on [Algorithmia](https://algorithmia.com/)
and you can upload your B&W images to their web site.

The Algorithmia service *is not free* but they will give you a lot of free
credits to test the service.

With the script ``colorize.py`` you can send photographs and receive results in the
command line. To use this script you need to register at
[Algorithmia](https://algorithmia.com/) and obtain a personal API key. This key
will be stored in your home directory under a ``.colorize`` file or can be hard
coded into this script as a  ``ALG_API_KEY`` constant.

With the GIMP plug-in you can send gray scale image directly and receive
results back in GUI. The plug-in is invoked by *Filters → Artistic →
Colorize...*  On your first try, you will be asked to provide your API key
which is stored in the same configuration file as described above.

## Usage

### Installation

The installation package provides Makefile, use ``make install`` to install the
script and the plug-in.

* Script installation path: ``/usr/bin/colorize.py``
* Plug-in installation path: ``/usr/lib64/gimp/2.0/plug-ins/``
* Alternative plug-in path: ``~/.gimp-2.8/plug-ins/``

You can use different directories for installation, but the GIMP plug-in uses
methods from the module ``colorize.py``, so you need to provide the path to the
directory where the file is located. In this case, update line:
``sys.path.insert(1, '/usr/bin')``.

### CLI utility

```
 Usage:  colorize.py [OPTIONS]... [FILE]...

   FILEs:
    * is a single or several image files (use shell pattern when necessary)
    * can also be a URL: http://, https://, s3://, dropbox://, data://

   -v, --verbose        ... verbose
   -s tag, --suffix tag ... download suffix (default is '-colorized')
   -t, --test-run       ... do nothing and show what will be done
   -h, --help           ... help

```

### GIMP plug-in

The plug-in is installed by default into ``/usr/lib64/gimp/2.0/plug-ins/``. Restart
GIMP and plug-in will be available in menu: *Filters → Artistic → Colorize...*

This plug-in can be used only on single layer, gray scale images. When invoked from
menu, your image is sent to the server, processed, downloaded  and displayed as
a new image in GIMP GUI. No progress bar is available because the image is processed
online and server response time differs.

## Known issues

Sometimes data processing fails and the  server returns the following error; in this
case try the command again.

```json
{u'metadata':
	{u'duration': 0},
	u'error': {
		u'message': u'Failed to start algorithm - Unable to load algorithm due to algorithm error'
	}
}
```

## Resources

* [Colorful Image Colorization, scientific paper](https://arxiv.org/abs/1603.08511v3)

