# ryck

You go onto [twitch.tv](https://twitch.tv/), your usual streamers are not there, or you have not found one you like yet, you keep on aimlessly clicking to find the one streamer to waste your time on. Not any more! `ryck.py` aims to automate this process for you! Run it, and streams will start flowing! With the press of a single key you go to the next.

This project is still in the early stages, so not all features have yet been implemented.

## Usage

There is basically nothing to do but to run the script at this point

```
$ ./ryck.py
```

which will start playing all currently live twitch streams under 'IRL' with the English language. This is all hard-coded, so change the code if you wanna change those defaults. Press `q` to go to the next, and `Ctrl+c` to stop.

## Todo/feature wish-list

Generally this is suppose to be quite featureless, but some small goodies should be added

* argparse
  - to change language
    - figure out all the language names
  - to change 'game'
    - figure out all the 'game' names
  - Sorting option (now just random, but also popularity, others?)
* proper keys (borrow from [reddytt](https://github.com/johanbluecreek/reddytt)) for exiting
* saving option to remember a good stream
* bundle the client-ID somehow
* Perhaps integrate initiating irssi and jump into the chat
* An input key in mpv to open the stream-page (to join chat or so)
