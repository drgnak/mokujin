#!/usr/bin/env python3
import os, sys
import datetime
import asyncio

import discord
from discord.ext import commands

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)
import tkfinder
import config

# Dict for searching special move types
move_types = {  'ra': 'Rage art',
                'rage_art': 'Rage art',
                'rd': 'Rage drive',
                'rage_drive': 'Rage drive',
                'wb': 'Wall bounce',
                'wall_bounce': 'Wall bounce',
                'ts': 'Tail spin',
                'tail_spin': 'Tail spin',
                'screw': 'Tail spin',
                'homing': 'Homing',
                'homari': 'Homing',
                'armor': 'Power crush',
                'armori': 'Power crush',
                'pc': 'Power crush',
                'power': 'Power crush',
                'power_crush': 'Power crush'}

def move_embed(character, move):
    '''Returns the embed message for character and move'''
    embed = discord.Embed(title=character['proper_name'],
            colour=0x00EAFF,
            url=character['online_webpage'],
            description='Move: ' + move['Command'])

    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])
    embed.add_field(name='Startup', value='i' + move['Start up frame'])
    embed.add_field(name='Block', value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name='Counter Hit', value=move['Counter hit frame'])
    embed.add_field(name='Notes', value=move['Notes'])

    return embed

def move_list_embed(character, move_list, move_type):
    '''Returns the embed message for a list of moves matching to a special move type'''
    desc_string = ''
    for move in move_list:
        desc_string += move + '\n'

    embed = discord.Embed(title=character['proper_name'] + ' ' + move_type.lower() + ':',
            colour=0x00EAFF,
            description=desc_string)

    return embed

def error_embed(err):
    embed = discord.Embed(title='Error',
            colour=0xFF4500,
            description=err)

    return embed

class Mokujin:
    prefix = '!'
    description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927'

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name="tk", pass_context=True)
    async def _tk(self, ctx):
        '''This has the main functionality of the bot. It has a lot of
        things that would be better suited elsewhere but I don't know
        if I'm going to change it.
        '''
        message = ctx.message
        channel = message.channel
        content = message.content.split(' ', 1)
        try:
            await self.bot.delete_message(message)
        except:
            pass

        # if message.content.startswith(self.prefix) and ((isinstance(channel, discord.channel.DMChannel)) or (channel.name in config.CHANNELS)):
        if len(content) > 1:
            user_message = content[1]
            # user_message = user_message.replace(self.prefix, '')
            user_message_list = user_message.split(' ', 1)

            if len(user_message_list) <= 1:
                # malformed command
                return

            chara_name = user_message_list[0].lower()
            chara_move = user_message_list[1]

            # iterate through character aliases in config for matching value
            chara_alias = list(filter(lambda x: (chara_name in x['alias']), config.CHARACTER_NAMES))
            if chara_alias:
                chara_name = chara_alias[0]['name']

            character = tkfinder.get_character(chara_name)
            if character is not None:
                if chara_move.lower() in move_types:
                    chara_move = chara_move.lower()
                    move_list = tkfinder.get_by_move_type(character, move_types[chara_move])
                    if  len(move_list) < 1:
                        embed = error_embed('No ' + move_types[chara_move].lower() + ' for ' + character['proper_name'])
                        msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                        return
                    elif len(move_list) == 1:
                        move = tkfinder.get_move(character, move_list[0], False)
                        embed = move_embed(character, move)
                        msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                        return
                    elif len(move_list) > 1:
                        embed = move_list_embed(character, move_list, move_types[chara_move])
                        msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                        return

                else:
                    move = tkfinder.get_move(character, chara_move, True)

                    #First checks the move as case sensitive, if it doesn't find it
                    #it checks it case unsensitive

                    if move is not None:
                        embed = move_embed(character, move)
                        msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                        return
                    else:
                        move = tkfinder.get_move(character, chara_move, False)
                        if move is not None:
                            embed = move_embed(character, move)
                            msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                            return
                        else:
                            embed = error_embed('Move not found: ' + chara_move)
                            msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)
                            return
            else:
                bot_msg = 'Character ' + chara_name + ' does not exist.'
                embed = error_embed(bot_msg)
                msg = await self.bot.say(embed=embed, delete_after=config.DELETE_AFTER)

                return

def setup(bot):
    bot.add_cog(Mokujin(bot))