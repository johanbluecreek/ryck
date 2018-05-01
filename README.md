# ryck

You go onto [twitch.tv](https://twitch.tv/), your usual streamers are not there, or you have not found one you like yet, you keep on aimlessly clicking to find the one streamer to waste your time on. Not any more! `ryck.py` aims to automate this process for you! Run it, and streams will start flowing! With the press of a single key you go to the next.

This project is still in the early stages, so not all features have yet been implemented.

## Usage

There is basically nothing to do but to run the script at this point

```
$ ./ryck.py
```

which will start playing all currently live twitch streams under 'IRL' with the English language. This is all hard-coded, so change the code if you wanna change those defaults. Press `q` to go to the next, and `Ctrl+c` to stop.

### Key-mapping

Ryck will generate a `input.conf`-file (to be stored in `~/.ryck/`) and override the mpv default, or user-set, key mapping (that is, ryck runs mpv with `--input-conf=` set). Nothing will permanently change for you, but you should be aware of the default key-mapping of ryck:

 * `q`: Saves and **q**uits remaining links
 * `>`: Plays next video
 * `R`: **R**emembers stream link in `~/.ryck/remember` (plain text)
 * `i`: Prints the **i**nfo (streamer's "status") in mpv
 * `Ctrl+o`: Video link is **o**pened in default browser (using `xdg-open`)

## Todo/feature wish-list

Generally this is suppose to be quite featureless, but some small goodies should be added

* argparse
  - to change language
    - figure out all the language names
  - to change 'game'
    - figure out all the 'game' names
  - Sorting option (now just random, but also popularity, others?)
* Perhaps integrate initiating irssi and jump into the chat
* Option to play only remembered streams
