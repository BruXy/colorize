# colorize
CLI utility for sending/receiving images to ColorfulImageColorization.

[*Colorful Image Colorization*](http://richzhang.github.io/colorization/) is a
system that takes a grayscale photograph as input and returns  a plausible color
version of the photograph. It was created by Richard Zhang, Phillip Isola and
Alexei A. Efros. The system is hosted on [Algorithmia](https://algorithmia.com/)
and you can upload your B&W images to their web site.

With script ``colorize.py`` you can send photographs and receive results in the
command line. To use this script you need to register at
[Algorithmia](https://algorithmia.com/) and obtain a personal API key. This key
will be stored in your home directory under a ``.colorize`` file or can be hard
coded into this script as a  ``ALG_API_KEY`` constant.

##Usage

```
 Usage:  colorize.py [OPTIONS]... [FILE]...

   FILEs:
    * is a single or several image files (use shell pattern when necessary)
    * can also be URL: http://, https://, s3://, dropbox://, data://

   -v, --verbose        ... verbose
   -s tag, --suffix tag ... download suffix (default is '-colorized')
   -t, --test-run       ... do nothing and show what will be done
   -h, --help           ... help

```

##Know errors

Sometimes data processing fails and the  server returns the following error; in this
case try the  command again.

```
{u'metadata': 
	{u'duration': 0}, 
	u'error': {
		u'message': u'Failed to start algorithm - Unable to load algorithm due to algorithm error'
	}
}
```

##Resources

* [Colorful Image Colorization, scientific paper](https://arxiv.org/abs/1603.08511v3)

