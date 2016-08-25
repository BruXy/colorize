# colorize
CLI utility for sending/receiving images to ColorfulImageColorization.

[*Colorful Image Colorization*](http://richzhang.github.io/colorization/) is a
system taking a grayscale photograph as input and returns  a plausible color
version of the photograph. It was created by Richard Zhang, Phillip Isola and
Alexei A. Efros. The system is hosted on [Algorithmia](https://algorithmia.com/)
and you can upload your B&W images on their web site.

With script ``colorize.py`` you can send photographs and receive result in
command line. To use this script you need to register at
[Algorithmia](https://algorithmia.com/) and obtain personal API key. This key
will be stored in your home directory in ``.colorize`` file or hard code it
into this script as ``ALG_API_KEY`` constant.

##Usage

```
 Usage:  colorize.py [OPTIONS]... [FILE]...

   FILEs:
    * is single or several image files (use shell pattern when necessary)
    * it can be also URL: http://, https://, s3://, dropbox://, data://

   -v, --verbose        ... verbose
   -s tag, --suffix tag ... download suffix (default is '-colorized')
   -t, --test-run       ... do nothing and show what will be done
   -h, --help           ... help

```

##Know errors

Sometimes data are not processed and server returns following error, in this
case try command again.

```
{u'metadata': 
	{u'duration': 0}, 
	u'error': {
		u'message': u'Failed to start algorithm - Unable to load algorithm due to algorithm error'
	}
}
```

