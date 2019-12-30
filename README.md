# Mokujin

## Mokujin Red-DiscordBot Cog

This repo is for migrating the original discord.py-based code to [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot). Small changes have also been made to make it work with Python 3.5.

This cog is based on [Tib#1303's fork of mokujin](https://github.com/TLNBS2405/mokujin), which used [discord.py](https://github.com/Rapptz/discord.py) v1.2.5+ and Python 3.6+.


The bot now has all the functionalities currently planned and it seems to work well and is somewhat stable. Currently, the data the bot uses is being updated to season 3, and the rest of the season 3 data will be updated either on request or when we see a mistake.

Framedata acquired from RBNorway and community

## If you want to use this:

Clone this to a linux server that has Python 3.5.0+, into the cogs folder of [Red-DiscordBot](https://github.com/Cog-Creators/Red-DiscordBot).
You can add a feedback channel into `mokucore/resources/config.json` also.

Commands
```
!character move         -   get frame data of a move from a character
!auto-delete seconds   -    change the duration of the bot waiting until he deletes the message in this channel
?feedback message       -   send message to the author   
```
