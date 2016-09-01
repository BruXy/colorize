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
sys.path.insert(1, '/usr/bin') # location of colorize.py
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

def gui_ask_for_api():
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
    
    # process buttong click immediately
    message.destroy()
    while gtk.events_pending():
        gtk.main_iteration()
     

def gui_message(text, message_type):
    """Gtk dialog for error message display"""
    message = gtk.MessageDialog(type=message_type, buttons=gtk.BUTTONS_CLOSE)
    message.set_markup(text)
    message.run()
    message.destroy()
    while gtk.events_pending():
        gtk.main_iteration()

def save_tmp_file(image, layer, fullpath):
    """Save current image to temporary folder in PNG format.

          Return: saved file path
    """
    if fullpath == None: # is not set for new images
        filename = 'temp.png'
    else:
        filename = os.path.basename(fullpath) + ".png"

    fullpath = os.path.join(TEMP, filename)
    gimpfu.pdb.file_png_save(image, layer, fullpath, filename, 0, 9, 1, 1, 1, 1, 1)
    return fullpath


def python_colorize(image, layer):
    """Colorize plugin"""
    image.disable_undo()
    print(image, layer)
    colorize.check_api_key()

    # 1. Save actual image to GIMP TEMP direcotry as PNG
    bw_photo = save_tmp_file(image, layer, image.filename)
    print("Temp file saved in: " + bw_photo)
    gimpfu.gimp.progress_init("Uploading image for processing.")

    # 2. Upload file to the server
#    gui_message(
#        "Image is being processed at <u>{0}</u>.\nIt may take a while.".format(colorize.URL), 
#        gtk.MESSAGE_INFO
#    )
# TODO: information window that data are uploaded. 
    download_url =  colorize.upload_image(bw_photo)
    if download_url == '': # if empty => error
        gui_message(colorize.ALG_API_ERR, gtk.MESSAGE_ERROR)
        gimpfu.gimp.quit()
    else:
        print("download_url: " + download_url)

    # 3. Download it from the server
    if download_url:
         color_photo = colorize.download_image(download_url, bw_photo)

    # 4. Display result as a new image
    if color_photo:
        gimpfu.gimp.Display(
            gimpfu.pdb.file_png_load(color_photo, color_photo)
        )
        gimpfu.gimp.progress_init("Colorized data received...")

    image.enable_undo()


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
        "GNU GPLv3",
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
colorize.ask_for_api_key = gui_ask_for_api

# execute plugin
gimpfu.main()

