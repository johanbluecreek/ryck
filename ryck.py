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
__version__ = "0.0.6"
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

from datetime import date
import time
from shutil import copyfile

import argparse as ap

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
    # XXX: There is also a 'broadcaster_language', but 'language' seems accurate enough
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

    if os.path.isfile(input_file):
        backup_file = input_file + "-" + date.today().isoformat() + "-" + str(int(time.time()))
        print("Ryck: Creating backup of old `input.conf`: %s" % backup_file)
        copyfile(input_file, backup_file)

    with open(input_file, 'w') as f:
        f.write('> quit 0\n')
        f.write('q quit 4\n')
        f.write('R run "/bin/bash" "-c" "echo \\\"${path}\\\" >> ~/.ryck/remember"\n')
        f.write('i show-text "${title}"\n')
        f.write('Ctrl+o run "/bin/bash" "-c" "xdg-open \\\"${path}\\\""\n')

def allowed_game(game):
    # Because we do not want the 'game' option to be misused (like using this
    # script to call the twitch-api in an unintended way) we will have to check
    # that the game given is an acceptable one. So here we list all the allowed
    # games, and verify that the given game name is in that list.
    # This is annying, because people would have to request having their games
    # added but with twitch's way of handling things, this is the more
    # comfrotable for me.
    supported_games = {'',
        'Anna',
        'Casino',
        'Counter-Strike: Global Offensive',
        'Crossout',
        'Dead by Daylight',
        'Destiny 2',
        'Dota 2',
        'Escape From Tarkov',
        'FIFA 18',
        'Fallout: New Vegas',
        'Fortnite',
        'Frostpunk',
        'God of War',
        'Grand Theft Auto V',
        'Hand Simulator',
        'Hearthstone',
        'IRL',
        'Jikkyou Powerful Pro Yakyuu 2018',
        'League of Legends',
        'Magic: The Gathering',
        'Murderous Pursuits',
        'Music',
        'Overwatch',
        "PLAYERUNKNOWN'S BATTLEGROUNDS",
        'Pillars of Eternity',
        'Poker',
        'Rust',
        "Sherlock Holmes: The Devil's Daughter",
        'StarCraft II',
        'Terraria',
        'Total War Saga: Thrones of Britannia',
        'World of Tanks',
        'World of Warcraft'
    }
    #TODO: Also figure out how to escape all the spaces ('+' instead of spaces)
    # to get these to a acceptable url form. Ex: 'Pillars of Eternity' ->
    # 'pillars+of+eternity'

    return game in supported_games

def known_langs():
    {'english': 'en', 'swedish': 'sv'}


################################################################################
                #     #  #####  #######    #     #####  #######
                #     # #     # #         # #   #     # #
                #     # #       #        #   #  #       #
                #     #  #####  #####   #     # #  #### #####
                #     #       # #       ####### #     # #
                #     # #     # #       #     # #     # #
                 #####   #####  ####### #     #  #####  #######
################################################################################


#    # ###### #    #  ####  #####  #   #
##  ## #      ##  ## #    # #    #  # #
# ## # #####  # ## # #    # #    #   #
#    # #      #    # #    # #####    #
#    # #      #    # #    # #   #    #
#    # ###### #    #  ####  #    #   #

def play_remember(work_dir, input_file, mpv_args):
    remember_file = work_dir + "/remember"
    memorised_streams = []
    if play_memory:
        if os.path.isfile(remember_file):
            with open(remember_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    memorised_streams.append(line)
            for stream in memorised_streams:
                p = subprocess.Popen(
                    [
                        'mpv',
                        stream,
                        '--input-conf=%s' % input_file,
                        '--title=\"%s\"' % stream
                    ] + mpv_args
                , shell=False)
                p.communicate()

                if p.returncode == 4:
                    sys.exit()
            print("Ryck: All memorised links consumed. Exiting.")
            sys.exit()
        else:
            print("Ryck: No `remember` file found. Exiting.")
            sys.exit()


#####  ###### ######   ##   #    # #      #####
#    # #      #       #  #  #    # #        #
#    # #####  #####  #    # #    # #        #
#    # #      #      ###### #    # #        #
#    # #      #      #    # #    # #        #
#####  ###### #      #    #  ####  ######   #

def play_default(input_file, lang, game, maximum, sorting, mpv_args):
    # Hard coded limit of what the twitch-api accepts
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
        print('')
        print('Ryck now playing: ' + stream_name)
        print('                  ' + stream_status)
        print('')
        p = subprocess.Popen(
            [
                'mpv',
                stream_link,
                '--input-conf=%s' % input_file,
                '--title=\"%s\"' % stream_status
            ] + mpv_args
        , shell=False)
        p.communicate()

        if p.returncode == 4:
            sys.exit()

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


    ###  Resolve arguments  ###

    parser = ap.ArgumentParser(usage='%(prog)s [options] [-- [mpv]]', description='Stream twitch streams instead of browsing them.')

    # Optional arguemnts
    parser.add_argument('--game', metavar='GAME', type=str, default='irl', help='Change the "game"-type twitch streams should be fetched from.')
    parser.add_argument('--lang', metavar='LANGUAGE', type=str, default='en', help='Change the language the stream should be in.')
    parser.add_argument('--max', metavar='MAX', type=int, default=0, help='Set how many streams should be fetched (0 or lower means all).')
    parser.add_argument('--sort', metavar='SORT', type=str, default='random', help='Sort streams to be played after "random" or anything else (which uses twitch default popularity sorting).')

    parser.add_argument('--gen-input', action='store_true', help='Ryck will generate a new input.conf and backup the old.')

    parser.add_argument('--play-mem', action='store_true', help='Ryck will play the streams saved by user (`R` (`shift+r`)), available in `~/.ryck/remember`')

    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__), help="Prints version number and exits.")

    # Positional arguments
    parser.add_argument('mpv', nargs=ap.REMAINDER, help='Arguments to pass to `mpv`.')

    # Pass them to variables
    args = parser.parse_args()

    game = args.game
    lang = args.lang
    maximum = args.max
    sorting = args.sort

    gen_input = args.gen_input
    play_memory = args.play_mem

    mpv_args = args.mpv[1:]

    ### Build a working env for ryck  ###

    work_dir = os.environ['HOME'] + "/.ryck"
    if not os.path.isdir(work_dir):
        os.mkdir(work_dir)


    ###  Generate input file if non exist  ###

    input_file = work_dir + "/input.conf"
    if not os.path.isfile(input_file):
        create_input(work_dir)

    ###  Start actually doing something  ###

    if gen_input:
        create_input(work_dir)
    if play_memory:
        play_remember(work_dir, input_file, mpv_args)

    if not play_memory and not gen_input:
        play_default(input_file, lang, game, maximum, sorting, mpv_args)
