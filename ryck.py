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
__version__ = "0.1.2"
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
        f.write('X quit 8')

def known_games():

    games = {'',
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

    print("Ryck: These are a bunch of 'game's that have been used.")
    print("      There are more than these, and you have to escape characters yourself for now.")
    print("      Example: 'Pillars of Eternity' yeilds correct game if entered as 'pillars+of+eternity'.\n")
    print(games)

def known_langs():

    #XXX: there is no way of doing this properly. Russians appear to select broadcaster_language in the opposite way as swedish streamers do. Whatever you do, you will miss streams.
    langs = {'English': 'en', 'Swedish': 'sv'}

    print("Ryck: You can try which every you want, but these are the ones that has been known to work:\n")
    print(langs)


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

def play_default(work_dir, input_file, lang, game, maximum, minimum, sorting, mpv_args):
    # Hard coded limit of what the twitch-api accepts
    limit = 100

    # Headers to auth with twitch-api
    headers = get_headers()

    # Create a list of the excluded streams
    exclusion_file = work_dir + "/exclude"
    excluded_streams = []
    if os.path.isfile(exclusion_file):
        with open(exclusion_file, 'r') as f:
            lines = f.readlines()
            for line in lines:
                excluded_streams.append(line.strip('\n'))

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

        while len(streams) <= maximum and len(data['streams']) == limit and data['streams'][-1]['viewers'] > minimum:
            r = requests.get(data['_links']['next'], headers=headers)
            data = r.json()

            streams += copy.copy(data['streams'][:maximum-len(streams)])

    else:

        # Else, just fetch them all

        call_link = construct_link(lang, game, str(limit))

        r = requests.get(call_link, headers=headers)
        data = r.json()

        streams += copy.copy(data['streams'])

        while len(data['streams']) == limit and data['streams'][-1]['viewers'] > minimum:
            r = requests.get(data['_links']['next'], headers=headers)
            data = r.json()

            streams += copy.copy(data['streams'])

    if minimum > 0:
        new_streams = []
        for stream in streams:
            if stream['viewers'] >= minimum:
                new_streams.append(stream)
        streams = new_streams

    # Then we proceed to sort the streams (popularity/viewers is default sorting)
    if sorting == 'random':
        random.shuffle(streams)

    # Then we play
    left = len(streams)
    for stream in streams:

        print("Ryck: Streams left: ", left)
        left -= 1

        if stream['channel']['url'] in excluded_streams:
            print("Ryck: Stream has been excluded. Moving on.")
        else:
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

            if p.returncode == 8:
                print("Ryck: Excluding steam.")
                with open(exclusion_file, 'a') as f:
                    f.write(stream_link + '\n')

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
    parser.add_argument('--min', metavar='MIN', type=int, default=0, help='Set the minimal amount of views the streamer should have.')
    parser.add_argument('--sort', metavar='SORT', type=str, default='random', help='Sort streams to be played after "random" or anything else (which uses twitch default popularity sorting).')

    parser.add_argument('--gen-input', action='store_true', help='Ryck will generate a new input.conf and backup the old.')

    parser.add_argument('--print-game', action='store_true', help='Prints known game options.')
    parser.add_argument('--print-lang', action='store_true', help='Prints known language options.')

    parser.add_argument('--play-mem', action='store_true', help='Ryck will play the streams saved by user (`R` (`shift+r`)), available in `~/.ryck/remember`')

    parser.add_argument('--version', action='version', version='%(prog)s {}'.format(__version__), help="Prints version number and exits.")

    # Positional arguments
    parser.add_argument('mpv', nargs=ap.REMAINDER, help='Arguments to pass to `mpv`.')

    # Pass them to variables
    args = parser.parse_args()

    game = args.game
    lang = args.lang
    maximum = args.max
    minimum = args.min
    sorting = args.sort

    if any(map(lambda x: "?" in x or "&" in x, [game, lang])):
        print("Ryck: Are you trying to manipulate the twitch-api call? Stop that!")
        sys.exit()

    gen_input = args.gen_input
    print_game = args.print_game
    print_lang = args.print_lang
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
    if print_game:
        known_games()
    if print_lang:
        known_langs()
    if play_memory:
        play_remember(work_dir, input_file, mpv_args)

    if not play_memory and not gen_input and not print_game and not print_lang:
        play_default(work_dir, input_file, lang, game, maximum, minimum, sorting, mpv_args)
