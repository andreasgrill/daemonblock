#!/usr/bin/env python

import subprocess
import os
import json
import getpass
from os.path import expanduser
from optparse import OptionParser

def load_config(config_files):
    """ loads json configuration files
    the latter configs overwrite the previous configs
    """

    config = dict()

    for f in config_files:
        with open(f, 'rt') as cfg:
            config.update(json.load(cfg))

    return config

def run(config):
    """ blocks daemons by unloading and removing them """
    for d in config["daemon_blacklist"]:
        if os.path.exists(d):
            try:
                subprocess.call(["launchctl", "unload", "-w", d])
                os.remove(d)
            except:
                pass


def install(config):
    """ installs daemonblock """
    launchplist_path = "/Library/LaunchDaemons/com.parrotbytes.daemonblock.plist"

    launchplist_script = '''<?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
        <key>Label</key>
        <string>com.parrotbytes.daemonblock</string>
        <key>ProgramArguments</key>
        <array>
            <string>{path}</string>
            <string>-r</string>
        </array>
        <key>StartCalendarInterval</key>
        <dict>
            <key>Minute</key>
            <integer>0</integer>
            <key>Hour</key>
            <integer>22</integer>
        </dict>
        <key>RunAtLoad</key>
        <true/>
    </dict>
    </plist>'''.format(path=os.path.realpath(__file__))

    with open(launchplist_path, 'w') as myfile:
        myfile.write(launchplist_script)

    subprocess.call(["launchctl", "load", "-w", launchplist_path])

    print("> Installed\n")
    print("> Execute for the first time\n")
    run(config)

if __name__ == "__main__":
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    parser = OptionParser()
    parser.add_option("-r" , "--run", action="store_true",                                                                                   
                      dest="run", default=False)
    (opts,args) = parser.parse_args()
    config = load_config([os.path.join(__location__,"config.json")])

    if opts.run:
        run(config)
    else:
        install(config)
