#!/usr/bin/env python3

################################################################################
                        ######  #     #  #####  #    #
                        #     #  #   #  #     # #   #
                        #     #   # #   #       #  #
         ##### #####    ######     #    #       ###       ##### #####
                        #   #      #    #       #  #
                        #    #     #    #     # #   #
                        #     #    #     #####  #    #
################################################################################
#
#   ryck.py
#   https://github.com/johanbluecreek/ryck
#
__version__ = "0.0.5"
#
################################################################################
################################################################################

################################################################################
              ### #     # ######  ####### ######  #######  #####
               #  ##   ## #     # #     # #     #    #    #     #
               #  # # # # #     # #     # #     #    #    #
               #  #  #  # ######  #     # ######     #     #####
               #  #     # #       #     # #   #      #          #
               #  #     # #       #     # #    #     #    #     #
              ### #     # #       ####### #     #    #     #####
################################################################################

import requests
import json

import copy

import random

import subprocess

import sys
import os

import base64

################################################################################
      ####### #     # #     #  #####  ####### ### ####### #     #  #####
      #       #     # ##    # #     #    #     #  #     # ##    # #     #
      #       #     # # #   # #          #     #  #     # # #   # #
      #####   #     # #  #  # #          #     #  #     # #  #  #  #####
      #       #     # #   # # #          #     #  #     # #   # #       #
      #       #     # #    ## #     #    #     #  #     # #    ## #     #
      #        #####  #     #  #####     #    ### ####### #     #  #####
################################################################################

def get_clientID():
    client_id = 'YTFoZGY2Zm4xYmNpdW0wZHUxcXJ1aGx1OGd4N2I0'
    client_id = base64.b64decode(client_id.encode()).decode()
    return client_id

def get_headers():
    client_id = get_clientID()
    headers = {'Client-ID': client_id}
    return headers

def construct_link(lang, game, limit):
    base_link = 'https://api.twitch.tv/kraken/streams'

    # start adding options
    call_link = base_link + '?'
    # language
    call_link += 'language=' + lang + '&'
    # game
    call_link += 'game=' + game + '&'
    # limit
    call_link += 'limit=' + limit + '&'
    # end the link
    call_link += 'stream_type=live'

    return call_link

def create_input(work_dir):
    input_file = work_dir + "/input.conf"

    with open(input_file, 'w') as f:
        f.write('> quit 0\n')
        f.write('q quit 4\n')
        f.write('R run "/bin/bash" "-c" "echo \\\"${path}\\\" >> ~/.ryck/remember"\n')
        f.write('i show-text "${title}"\n')
        f.write('Ctrl+o run "/bin/bash" "-c" "xdg-open \\\"${path}\\\""\n')

################################################################################
                          #     #    #    ### #     #
                          ##   ##   # #    #  ##    #
                          # # # #  #   #   #  # #   #
                          #  #  # #     #  #  #  #  #
                          #     # #######  #  #   # #
                          #     # #     #  #  #    ##
                          #     # #     # ### #     #
################################################################################

if __name__ == '__main__':

    # Build a working env for ryck
    work_dir = os.environ['HOME'] + "/.ryck"
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)

    input_file = work_dir + "/input.conf"
    gen_input = True
    if gen_input:
        create_input(work_dir)

    # Set preferences (TODO: Move to argparse)
    lang = 'en'
    game = 'irl'
    maximum = 0
    sorting = 'random'

    # Limit (TODO: Change this to a maximum set by user/default)
    limit = 100

    # Headers to auth with twitch-api
    headers = get_headers()

    # Fetch all the streams
    streams = []
    if maximum <= limit and maximum > 0:

        # For a small number of streams, just get them all at once

        call_link = construct_link(lang, game, str(maximum))

        r = requests.get(call_link, headers=headers)
        data = r.json()

        streams += copy.copy(data['streams'])

    elif maximum > limit:

        # If larger than limit we have to make several calls

        call_link = construct_link(lang, game, str(limit))

        r = requests.get(call_link, headers=headers)
        data = r.json()

        streams += copy.copy(data['streams'])

        while len(streams) <= maximum and len(data['streams']) == limit:
            r = requests.get(data['_links']['next'], headers=headers)
            data = r.json()

            streams += copy.copy(data['streams'][:maximum-len(streams)])

    else:

        # Else, just fetch them all

        call_link = construct_link(lang, game, str(limit))

        r = requests.get(call_link, headers=headers)
        data = r.json()

        streams += copy.copy(data['streams'])

        while len(data['streams']) == limit:
            r = requests.get(data['_links']['next'], headers=headers)
            data = r.json()

            streams += copy.copy(data['streams'])

    # Then we proceed to sort the streams (popularity/viewers is default sorting)
    if sorting == 'random':
        random.shuffle(streams)

    for stream in streams:
        stream_name = stream['channel']['name']
        stream_status = stream['channel']['status']
        stream_link = stream['channel']['url']
        print('Playing: ' + stream_name)
        print('Playing: ' + stream_status)
        p = subprocess.Popen(
            [
                'mpv',
                stream_link,
                '--input-conf=%s' % input_file,
                '--title=\"%s\"' % stream_status
            ]
        , shell=False)
        p.communicate()

        if p.returncode == 4:
            sys.exit()
