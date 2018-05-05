# ryck

You go onto [twitch.tv](https://twitch.tv/), your usual streamers are not there, or you have not found one you like yet, you keep on aimlessly clicking to find the one streamer to waste your time on. Not any more! `ryck.py` aims to automate this process for you! Run it, and streams will start flowing! With the press of a single key you go to the next.

## Usage

The short story is that you can just run it (make sure it is in your `$PATH`)

```
$ ryck.py
```

and it will start playing streams from 'IRL' in English. Check out the 'Key-mapping' section below to see how to control the streams.

The long story is told by the help:

```
$ ./github/ryck/ryck.py --help
usage: ryck.py [options] [-- [mpv]]

Stream twitch streams instead of browsing them.

positional arguments:
  mpv              Arguments to pass to `mpv`.

optional arguments:
  -h, --help       show this help message and exit
  --game GAME      Change the "game"-type twitch streams should be fetched
                   from.
  --lang LANGUAGE  Change the language the stream should be in.
  --max MAX        Set how many streams should be fetched (0 or lower means
                   all).
  --min MIN        Set the minimal amount of views the streamer should have.
  --exclude EXC    Comma separated list of words to exclude from streamers
                   "status".
  --only ONLY      Comma separated list of words that a streamer must have in
                   "status".
  --sort SORT      Sort streams to be played after "random" or anything else
                   (which uses twitch default popularity sorting).
  --gen-input      Ryck will generate a new input.conf and backup the old.
  --print-game     Prints known game options.
  --print-lang     Prints known language options.
  --play-mem       Ryck will play the streams saved by user (`R` (`shift+r`)),
                   available in `~/.ryck/remember`
  --version        Prints version number and exits.
```

### Key-mapping

Ryck will generate a `input.conf`-file (to be stored in `~/.ryck/`) and override the mpv default, or user-set, key mapping (that is, ryck runs mpv with `--input-conf=` set). Nothing will permanently change for you, but you should be aware of the default key-mapping of ryck:

 * `q`: Saves and **q**uits remaining links
 * `>`: Plays next video
 * `R`: **R**emembers stream link in `~/.ryck/remember` (plain text)
 * `X`: Link is e**x**cluded, and will no longer appear. (`~/.ryck/exclude`, plain text)
 * `i`: Prints the **i**nfo (streamer's "status") in mpv
 * `Ctrl+o`: Video link is **o**pened in default browser (using `xdg-open`)

## Todo/feature wish-list

Generally this is suppose to be quite featureless, but some small goodies should be added

* Some chat-integration (perhaps integrate initiating irssi and jump into the chat)
* add more languages
* Can the status be updated? (say you watch a stream for 2 hours, change, and the status may have changed. Updates in general I guess.)
