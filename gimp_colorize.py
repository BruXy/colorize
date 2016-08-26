#!/usr/bin/env python
#------------------------------------------------------------------------------
#
# GIMP plugin for accessing ColorfulImageColorization
#
# Author: Martin 'BruXy' Bruchanov, bruchy(at)gmail.com
#
# Additional info:
#   https://algorithmia.com/algorithms/deeplearning/ColorfulImageColorization
#   http://gimp.org
#
#------------------------------------------------------------------------------

###########
# Imports #
###########

import sys
import os
sys.path.insert(1, '/home/bruxy/Documents/Algoritmia/colorize/')
sys.path.insert(2, '/usr/lib64/gimp/2.0/python/')

import colorize
import gtk
import gimpfu

####################
# Global variables #
####################

colorize.VERBOSE = True
TEMP = os.path.join(colorize.HOME, '.gimp-2.8', 'tmp') # TODO detect gimp_dir in home

########################
# Function definitions #
########################

def _gui_ask_for_api():
    """Gtk dialog for API key insert."""
    message = gtk.MessageDialog(type=gtk.MESSAGE_QUESTION, buttons=gtk.BUTTONS_OK_CANCEL)
    message.set_markup(colorize.MSG_ASK_API.replace(colorize.URL,"<u>" + colorize.URL +"</u>"))

    entry = gtk.Entry(max=64)
    entry.set_text("Enter your API key")
    entry.show()
    message.vbox.pack_end(entry)
    entry.connect("activate", lambda _: d.response(gtk.RESPONSE_OK))
    message.set_default_response(gtk.RESPONSE_OK)
    message.run()

    api_key = entry.get_text().decode('utf8')
    fp = open(colorize.HOME + colorize.API_KEY_FILE, 'w')
    fp.write("YOUR_API_KEY={0}{1}".format(api_key, os.linesep))
    fp.close()


def save_tmp_file(image, layer, fullpath):
    """Save current image to temporary folder in PNG format.

          Return: saved file path
    """
    filename = colorize.basename(fullpath) + ".png"
    fullpath = os.path.join(TEMP, filename) 
    gimpfu.pdb.file_png_save(image, layer, fullpath, filename, 0, 9, 1, 1, 1, 1, 1)
    return fullpath


def python_colorize(image, layer):
    """Colorize plugin """
    image.disable_undo()
    print(image, layer)
    colorize.check_api_key()
    # 1. Save actual image to $TEMP/.colorize/ as PNG
    bw_photo = save_tmp_file(image, layer, image.filename)

    print("Temp file saved in: " + bw_photo)

    # 2. Upload it to the server
    download_url =  colorize.upload_image(bw_photo)

    print("download_url: " + download_url)
    
#    download_url = colorize.ALG_URL_DOWNLOAD + '.algo/deeplearning/ColorfulImageColorization/temp/output.png'

    # 3. Download it to the server
    if download_url:
         color_photo = colorize.download_image(download_url, bw_photo)
     
    print("color_photo: " + color_photo) 
    # 4. Display result as new image

    if color_photo:
        gimpfu.gimp.Display(
            gimpfu.pdb.file_png_load(color_photo, color_photo)
       ) 

    image.enable_undo()

#gimp.Image(width, height, "RGB")
#gimp.Display(img)

#gimp.progress_init("Mapping colors...")


####################
# Plug-in register #
####################

gimpfu.register(
        # proc_name
        "python_fu_colorize",
        # blurb
        "Colorize black and white photography with ColorfulImageColorization",
        # help
        "Colorize black and white photography with ColorfulImageColorization",
        # author
        "Martin (BruXy) Bruchanov",
        # copyright
        "Martin (BruXy) Bruchanov",
        # date
        "2016",
        # menupath
        "<Image>/Filters/Artistic/_Colorize...",
        # imagetypes
        "GRAY",
        # params
        [],
        # results
        [],
        # function
        python_colorize,
        # domain
        domain=()
        )


########
# Main #
########

# instead of console input invoke GUI window
colorize.ask_for_api_key = _gui_ask_for_api

# execute plugin
gimpfu.main()

