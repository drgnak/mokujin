#!/usr/bin/env python3
import os, datetime, logging
import sys

sys.path.insert(1, (os.path.dirname(__file__)))

from discord.ext import commands
from mokucore.resources import const, embed
from mokucore import tkfinder, configurator

base_path = os.path.dirname(__file__)
config = configurator.Configurator(os.path.abspath(os.path.join(base_path, "resources", "config.json")))
description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927, continued by Tib#1303'

# Set logger to log errors
logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)

logfile_directory = os.path.abspath(os.path.join(base_path, "..", "log"))
logfile_path = logfile_directory + "\\logfile.log"

# Create logfile if not exists
if not os.path.exists(logfile_directory):
    os.makedirs(logfile_directory)

if not os.path.isfile(logfile_path):
    open(logfile_path, "w")

file_handler = logging.FileHandler(logfile_path)

formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

feedback_channel_id = config.read_config()['FEEDBACK_CHANNEL_ID']


class Mokujin:
    prefix = '!'
    description = 'The premier Tekken 7 Frame bot, made by Baikonur#4927, continued by Tib#1303'

    def __init__(self, bot):
        self.bot = bot
    @commands.group(name="tk", pass_context=True)
    async def _tk(self, ctx):
        """This has the main functionality of the bot. It has a lot of
        things that would be better suited elsewhere but I don't know
        if I'm going to change it."""

        try:
            message = ctx.message
            channel = message.channel
            user_message = message.content.split(' ', 1)[1]

            if message.content.startswith(self.prefix + "tk auto-delete"):

                if message.author.permissions_in(channel).manage_messages:
                    duration = user_message.split(' ', 1)[1]
                    if duration.isdigit() or duration == "-1":
                        config.save_auto_delete_duration(channel.id, duration)
                        await self.bot.say(embed=embed.success_embed("Saved"))
                    else:
                        await self.bot.say(embed=embed.error_embed("Duration needs to be a number in seconds"))
                else:
                    await self.bot.say(embed=embed.error_embed("You need the permission <manage_messages> to do that"))
                return

            elif message.content == self.prefix + 'tk help':
                await self.bot.say(embed=embed.help_embed())
                return

            elif message.content.startswith(self.prefix + 'tk feedback'):
                user_message = user_message.split(' ', 1)[1]
                server_name = str(message.channel.guild)

                try:

                    feedback_channel = bot.get_channel(feedback_channel_id)
                    user_message = user_message.replace("\n", "")
                    result = "{}  ;  {} ;   {};\n".format(str(message.author), server_name, user_message)
                    await self.bot.say(result)

                    await self.bot.say(embed=embed.success_embed("Feedback sent"))
                except Exception as e:
                    await self.bot.say(embed=embed.error_embed("Feedback couldn't be sent caused by: " + e))
                return

            else:

                delete_after = config.get_auto_delete_duration(channel.id)


                # user_message = content
                command = user_message
                user_message_list = command.split(' ', 1)

                if len(user_message_list) <= 1:
                    # malformed command
                    return

                original_name = user_message_list[0].lower()
                original_move = user_message_list[1]

                character_name = tkfinder.correct_character_name(original_name)

                if character_name is not None:
                    character = tkfinder.get_character_data(character_name)
                    character_move = original_move.lower()

                    if original_move.lower() in const.MOVE_TYPES.keys():

                        move_list = tkfinder.get_by_move_type(character, const.MOVE_TYPES[character_move])
                        if len(move_list) < 1:
                            result = embed.error_embed(
                                'No ' + const.MOVE_TYPES[character_move].lower() + ' for ' + character['proper_name'])
                            await self.bot.say(embed=result, delete_after=delete_after)
                        elif len(move_list) == 1:
                            character_move = tkfinder.get_move(character, move_list[0])
                            result = embed.move_embed(character, character_move)
                            await self.bot.say(embed=result, delete_after=delete_after)
                        elif len(move_list) > 1:
                            result = embed.move_list_embed(character, move_list, const.MOVE_TYPES[character_move])
                            await self.bot.say(embed=result, delete_after=delete_after)

                    else:
                        character_move = tkfinder.get_move(character, original_move)

                        if character_move is not None:
                            result = embed.move_embed(character, character_move)
                            await self.bot.say(embed=result, delete_after=delete_after)
                        else:
                            similar_moves = tkfinder.get_similar_moves(original_move, character_name)
                            result = embed.similar_moves_embed(similar_moves)
                            await self.bot.say(embed=result, delete_after=delete_after)
                else:
                    bot_msg = 'Character {} does not exist.'.format(original_name)
                    result = embed.error_embed(bot_msg)
                    await message.self.bot.say(embed=result, delete_after=5)
                    return

            return
        except Exception as e:
            print(e)
            logger.error(e)


def is_me(m):
    return m.author == bot.user

def setup(bot):
    bot.add_cog(Mokujin(bot))