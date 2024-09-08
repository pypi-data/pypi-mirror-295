# Push InnerTune Likes

A basic Python script to extract liked songs from [InnerTune](https://github.com/z-huang/InnerTune)
(via an exported backup), and push those likes to YouTube Music (via [ytmusicapi](https://github.com/sigma67/ytmusicapi)).

## Example usage

My personal workflow is:

1. Use InnerTune on my phone as normal
1. Export a backup
1. Run this script on my phone using Termux

### Setup

```bash
pip install push-innertune-likes
ytmusicapi oauth
```

### Sync Steps

1. Export an InnerTune backup (`InnerTune.backup`)
1. Run the script

```bash
push_innertune_likes --backup InnerTune.backup --credentials oauth.json
```

## Compatibility

### Desktop

This has been tested with:

- OSX 14.6
- Python 3.12

### Android

This script can be run on Android via [Termux](https://github.com/termux/termux-app)
with pip installed.

This has been tested with:

- Android 14
- Termux 0.118.1 - Python 3.11

## Caveats

- All likes from InnerTune will be pushed to YouTube Music
- Even if you previously un-liked a song on YTM
- This script does not sync un-likes from InnerTune
  - It is trivial to remove to YTM likes, but it raises more syncing issues

## Alternatives

[OuterTune](https://github.com/DD3Boh/OuterTune) is an InnerTune fork which
syncs likes (and playlists and etc). If bugs in that fork do not affect you,
it is a better option.
