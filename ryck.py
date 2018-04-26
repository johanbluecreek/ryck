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
#   https://github.com/johanbluecreek/reddytt
#
__version__ = "0.0.1"
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
    client_id = ''
    with open('./client_id.txt', 'r') as f:
        client_id = f.readline()
    client_id = client_id.strip()
    return client_id

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

    # Fetch Client-ID from file
    client_id = get_clientID()
    # construct header
    header = {'Client-ID': client_id}

    # Set preferences (TODO: Move to argparse)
    lang = 'en'
    limit = '100'
    game = 'irl'

    # Construct the link to call (TODO: Move to function)
    base_link = 'https://api.twitch.tv/kraken/streams'

    call_link = base_link + '?'

    call_link += 'language=' + lang + '&'
    call_link += 'game=' + game + '&'
    call_link += 'limit=' + limit + '&'

    call_link += 'stream_type=live'

    # Perform the call
    r = requests.get(call_link, headers=header)
    data = r.json()

    # Store what we want to keep
    # and keep calling until all streams are fetched.
    streams = copy.copy(data['streams'])
    while len(data['streams']) == int(limit):
        r = requests.get(data['_links']['next'], headers=header)
        data = r.json()

        streams += copy.copy(data['streams'])

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
                stream_link
            ]
        , shell=False)
        p.communicate()
