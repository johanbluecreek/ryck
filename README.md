# ryck

Wanna try out watching some twitch streamers without any effort? You are in the right place.

## Usage

I'm unsure of the accurate way to bundle twitch API client-IDs, so for now you have to get one yourself. So start off heading over to [dev.twitch.tv](https://dev.twitch.tv/), register an account, press after that find a 'Register an App'-button, and fill in name for you app with whatever and the redirect-URI with `https://twitchapps.com/tokengen/` (which [this repo]() suggests ¯\\_(ツ)_/¯), then find your `Client-ID` and paste it into a file `client_id.txt` in the same folder as `ryck.py` is in.

At this stage, which is past the stage of seeing-that-this-was-way-too-much-effort-and-abandoning-this-project-forever, you are(/would be) done, and

```
$ ./ryck.py
```

will start playing twitch streams from 'IRL' with the english language. This is all hard-coded, so change the code if you wanna change those defaults.

## Todo/feature wish-list

Generally this is suppose to be quite featureless, but some small goodies should be added

* argparse
  - to change language
    - figure out all the language names
  - to change 'game'
    - figure out all the 'game' names
* proper keys (borrow from [reddytt](https://github.com/johanbluecreek/reddytt)) for exiting
* saving option to remember a good stream
* bundle the client-ID somehow
* Perhaps integrate initiating irssi and jump into the chat
* An input key in mpv to open the stream-page (to join chat or so)
