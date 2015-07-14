#!/usr/bin/env python2

"""
Automagically generate a nodeinfo.json file.

Searches around for cjdroute.conf and the cjdns executable, cleans the config
into proper JSON, and saves the node info to a file. By default this
is ~/nodeinfo.json, but you can specify any file you want.
"""
import json
import os
import sys
import subprocess
import getpass
import socket
import datetime

# Edit this to put where your conf is.
conflocations = ["~/cjdns/cjdroute.conf"]

# Edit this to put where your cjdroute binary is.
cjdroutelocations = ["~/cjdns"]

# This adds locations in your $PATH system variable to the list of cjdroute's possible locations.
cjdroutelocations += os.getenv("PATH").split(":")

# Decides where to save the file based on existence of an argument or not.
if len(sys.argv) == 1:
    # Write the file in the default location
    nodeinfo_path = os.path.expanduser("~/nodeinfo.json") 
else:
    # Write the file in some other location
    nodeinfo_path = sys.argv[1]

# A basic confirmation prompt.
def ask(question, default):
    while True:
        r = raw_input("%s " % question).lower() or default

        if r in "yn":
            return r == "y"
        else:
            print "Invalid response, please enter either y or n"

# Looks to confirm where cjdroute is.
def find_cjdroute_bin():
    for path in cjdroutelocations:
        path = os.path.expanduser(path) + "/cjdroute"
        if os.path.isfile(path):
            return path

    print "Failed to find cjdroute"
    print "Please tell me where it is"
    return raw_input("ie. <cjdns git>/cjdroute: ")

# Looks to confirm where cjdroute.conf is.
def find_cjdroute_conf():
    for path in conflocations:
        path = os.path.expanduser(path)
        if os.path.isfile(path):
            return path

    return raw_input("Can't find cjdroute.conf, please give the path to it here: ")

# Loads cjdroute.conf so that it can be edited
def load_cjdroute_conf(conf):
    print "Loading " + conf
    try:
        with open(conf) as conffile:
            return json.load(conffile)
    except ValueError:
        return cleanup_config(conf)
    except IOError:
        print "Error opening " + conf + ". Do we have permission to access it?"
        print "Hint: Try running this as root"
        sys.exit(1)

# This actually takes the conf and changes it from cjdson to json
def cleanup_config(conf):
    print "Making valid JSON out of " + conf
    print "First, we need to find the cleanconfig program"
    cjdroute = find_cjdroute_bin()
    print "Using " + cjdroute
    process = subprocess.Popen([cjdroute, "--cleanconf"], stdin=open(conf), stdout=subprocess.PIPE)
    try:
        return json.load(process.stdout)
    except ValueError:
        print "Failed to parse! Check:"
        print "-" * 8
        print "{} --cleanconf < {}".format(cjdroute, conf)
        print "-" * 8
        sys.exit(1)

# Loads the nodeinfo file, if it already exists.
try:
    with open(nodeinfo_path) as nodeinfo_file:
        json.load(nodeinfo_file)

    if not ask("%s appears to be a valid JSON file. Update? [Y/n]" % nodeinfo_path, "y"):
        sys.exit()
except ValueError:
    if not ask("%s appears to be a file. Overwrite? [y/N]" % nodeinfo_path, "n"):
        sys.exit()
except IOError:
    print "This script will attempt to create " + nodeinfo_path



conf = find_cjdroute_conf()
cjdrouteconf = load_cjdroute_conf(conf)
nodeinfo = {}

# gets your fcip from the conf
nodeinfo["addr"] = cjdrouteconf['ipv6']

# gets your public cjdns key from the conf
nodeinfo["key"] = cjdrouteconf['publicKey']

# gets your current hostname, may not be fully qualified!
nodeinfo["hostname"] = socket.gethostname()

# last time the file was modified
nodeinfo["last_modified"] = datetime.datetime.utcnow().isoformat()

nodeinfo["contact"] = {}

# uses the name of the current user running the script 
nodeinfo["contact"]["name"] = getpass.getuser()

nodeinfo["contact"]["email"] = raw_input("Please enter your email: ")

with open(nodeinfo_path, "w+") as adminfile:
    json.dump(nodeinfo, adminfile, indent=4)
print "\nDone! Note that this script isn't perfect, and as such, you may want to edit {} to properly reflect your services and other changes.".format(nodeinfo_path)
