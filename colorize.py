#!/usr/bin/env python
#------------------------------------------------------------------------------
#
# CLI utility for sending/receiving images to ColorfulImageColorization
# via Algoritmia REST API.
#
# Author: Martin 'BruXy' Bruchanov, bruchy(at)gmail.com
#
#------------------------------------------------------------------------------
#<
#
# Usage:  colorize.py [OPTIONS]... [FILE]...
#
#   FILEs:
#    * is single or several image files (use shell pattern when necessary)
#    * it can be also URL: http://, https://, s3://, dropbox://, data://
#
#   -v, --verbose        ... verbose
#   -s tag, --suffix tag ... download suffix (default is '-colorized')
#   -t, --test-run       ... do nothing and show what will be done
#   -h, --help           ... help
#
# You need to register at https://algorithmia.com/ and obtain personal API key.
# This key will be stored in your home directory in .colorize file or hard code
# it into this script as ALG_API_KEY constant.
#
#>

###########
# Imports #
###########

from __future__ import print_function
import sys
import os
import getopt
import requests
from pprint import pprint

####################
# Global variables #
####################

ALG_BASE_URL = 'http://api.algorithmia.com/v1/'
ALG_URL_API = ALG_BASE_URL + 'algo/deeplearning/ColorfulImageColorization/1.0.0'
# + 'data/.algo/deeplearning/ColorfulImageColorization/temp/output.png'
ALG_URL_DOWNLOAD = ALG_BASE_URL + 'connector/data/'
ALG_API_KEY = ''
API_KEY_FILE = '.colorize'
PROTOCOLS = ['http', 'https', 's3', 'dropbox', 'data']

HOME = os.path.expanduser("~") + "/"
#VERBOSE = False
VERBOSE = True
TEST_RUN = False
SUFFIX = '-colorized'
OUTPUT_FORMAT = '.png'
INPUT_FILES = list()

########################
# Function definitions #
########################


def print_help():
    """Print help encoded as initial script's comment between #< and #>."""
    show_line = False
    fp = open(sys.argv[0], 'r')

    for line in fp:
        if line[0:2] == '#<':  # start token
            show_line = True
            continue
        elif line[0:2] == '#>':  # end token
            return

        if show_line == True:
            print(line.rstrip(os.linesep)[1:])

    fp.close()


def vprint(*args):
    """Print additional information when verbose option is enabled."""

    if VERBOSE == True:
        for arg in args:
            print(arg)
        print()
    else:
        return


def is_valid_api_key():
    """Check if provided API key is valid."""
    print()


def ask_for_api_key():
    print("""Please register at: https://algorithmia.com/
You need to provide your personal 'Default API key' provided after
the registraion. 
""")
    api_key = raw_input("Enter your API key: ")
    print("User provided: " + api_key)
    fp = open(HOME + API_KEY_FILE, 'w')
    fp.write("YOUR_API_KEY={0}{1}".format(api_key, os.linesep))
    fp.close()


def check_api_key():
    """Check if user API is defined, if not ask for it and provide info how to
       get it."""
    global ALG_API_KEY
    try:
        fp = open(HOME + API_KEY_FILE, 'r')
        api_key = fp.readline().rstrip(os.linesep).split('=')[1]
        vprint("API key found: '{0}'".format(api_key))
        ALG_API_KEY = api_key
    except:
        ask_for_api_key()


def basename(longpath):
    """Get base name of file when path or URL given."""
    last = longpath.rfind('/')
    basename = longpath[last + 1:]
    return basename


def output_file(file_name):
    """Put SUFFIX in the file name before the extension"""
    ldot = file_name.rfind('.')
    basename = file_name[0:ldot]
#   extension = file_name[ldot:]
    return basename + SUFFIX + OUTPUT_FORMAT


def process_cli_options():
    global INPUT_FILES, VERBOSE, SUFFIX, TEST_RUN
    vprint("Input arguments:", sys.argv[1:])
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:], 'vs:df:th',
            ['verbose', 'suffix=', 'delete', 'remote-folder=', 'test-run', 'help'])
    except getopt.GetoptError as err:
        print("Error: ", str(err))
        print_help()
        sys.exit(1)

    for opt, arg in options:
        if opt in ("-h", "--help"):
            print_help()
            sys.exit(0)
        elif opt in ("-v", "--verbose"):
            VERBOSE = True
            vprint("Verbose output enabled.")
        elif opt in ("-t", "--test-run"):
            TEST_RUN = True
            print("Test run enabled, nothing will be done.")
        elif opt in ("-s", "--suffix"):
            SUFFIX = arg
        else:
            assert False, "Unhandled option"

    if len(remainder) == 0:
        print_help()
        sys.exit(1)
    else:
        INPUT_FILES = list(remainder)


def http_header(mime_type):
    """HTTP header is used for authentization"""
    return {
        'Content-Type': mime_type,
        'Authorization': 'Simple ' + ALG_API_KEY
    }
# return "{{ 'Content-Type' : '{0}', 'Authorization': 'Simple  {1}'
# }}".format(mime_type, ALG_API_KEY)


def upload_image(name):
    """Upload image file to the server, get response from API and return download
       URL."""

    print("Processing: {0}".format(name))
    if TEST_RUN == True:
        return ''

    # Upload data
    try:
        upload_img = open(name, 'rb')
    except IOError as err:
        print("{0}: Warning: Unable to open file: {1}".format(
            sys.argv[0], err))
        return ''

    vprint("Sending:\n{0}\nto: {1}".format(http_header(), ALG_URL_API))
    vprint(upload_img)

    # Important: image must be send as a stream not as multi-part file!
    response = requests.post(ALG_URL_API, data=upload_img,
                             headers=http_header()).json()
    vprint("HTTP response:\n{0}".format(response))
    upload_img.close()

    if "error" in response:
        print("ERROR from API: " + r.json()["error"]["message"])
        return ''
    else:
        # Example of good response:
        # u'{"result":
        #    {"output":"data://.algo/deeplearning/ColorfulImageColorization/temp/output.png"},
        #    "metadata":{
        #       "content_type":"json",
        #        "duration":1.659112994}
        #  }'
        print("Response path: ", response["result"]["output"])
        print("Processing time: {0} sec".format(
            response["metadata"]["duration"]))
        # Format URL for download
        return ALG_URL_DOWNLOAD + response["result"]["output"].replace('data://', '')


def provide_url(url):
    """Send JSON object with image URL."""
    print("Processing remote file: {0}".format(url))
    response = requests.post(
        ALG_URL_API, json={"image": url}, headers=http_header('application/json'))
    vprint("HTTP response:\n{0}".format(response.json()))

    if response.status_code == 200:
        data_url = response.json()["result"]["output"]
        return ALG_URL_DOWNLOAD + data_url.replace('data://', '')
    else:
        print('Error when accessing URL!', file=sys.stderr)
        sys.exit(1)


def download_image(url, filename):
    """Download output image and save it to file with the same name as input +
       suffix SUFFIX, output is in PNG format."""

    # Download URL is usually:
    # https://api.algorithmia.com/v1/connector/data/.algo/deeplearning/ColorfulImageColorization/temp/output.png
    name = output_file(filename)

    try:  # Open file to save output
        fw = open(name, 'wb')
    except IOError as err:
        print("{0}: Error: Unable to write: {1}".format(sys.argv[0], err))
        sys.exit(1)

    # Download
    vprint('HTTP get from: {0}'.format(url))
    response = requests.get(
        url, stream=True, headers=http_header('application/octet-stream'))
    vprint('HTTP status code: {0}'.format(response.status_code))
    vprint('HTTP header:\n{0}'.format(response.headers))

    if response.status_code == 200:
        for chunk in response:
            fw.write(chunk)
        fw.close()
        vprint("Output saved to: '{0}'".format(name))
    else:
        print('Error when accessing URL!', file=sys.stderr)
        sys.exit(1)
        fw.close()


########
# Main #
########

def main(argv):
    process_cli_options()  # file list in INPUT_FILES
    check_api_key()
    for filename in INPUT_FILES:
        if filename.split('://')[0] in PROTOCOLS:
            # provided filename is URL
            download_url = provide_url(filename)
            if download_url:
                download_image(download_url, basename(download_url))
        else:
            # provided filename is disk file
            download_url = upload_image(filename)
            if download_url:
                download_image(download_url, filename)

    quit()

if __name__ == "__main__":
    main(sys.argv)
