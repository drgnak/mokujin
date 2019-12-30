import discord
from random import randint


def move_embed(character, move):
    """Returns the embed message for character and move"""
    embed = discord.Embed(title=character['proper_name'],
                          colour=0x00EAFF,
                          url=character['online_webpage'],
                          description='**Move: ' + move['Command'] + '**')
    embed.set_thumbnail(url=character['portrait'])
    embed.add_field(name='Property', value=move['Hit level'])
    embed.add_field(name='Damage', value=move['Damage'])
    embed.add_field(name='Startup', value='i' + move['Start up frame'])
    embed.add_field(name='Block', value=move['Block frame'])
    embed.add_field(name='Hit', value=move['Hit frame'])
    embed.add_field(name='Counter Hit', value=move['Counter hit frame'])

    if 'Recovery' in move:
        embed.add_field(name='Recovery', value=move['Recovery'])
    if 'Notes' in move and not move['Notes'] == "-":
        embed.add_field(name='Notes', value=move['Notes'])
    if 'Gif' in move and move['Gif'] and not move['Gif'] == "-":
        embed.add_field(name='Gif', value=move['Gif'], inline=False)

    random_value = randint(0, 10)
    # every 10th time
    if random_value == 0:
        embed.add_field(name='Dev Note', value='Also dont forget to check !help to get the newest features :)',
                        inline=False)

    return embed


def move_list_embed(character, move_list, move_type):
    """Returns the embed message for a list of moves matching to a special move type"""
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


def success_embed(message):
    embed = discord.Embed(title='Success',
                          colour=0x3ddb2c,
                          description=message)
    return embed


def similar_moves_embed(similar_moves):
    embed = discord.Embed(title='Move not found', colour=0xfcba03,
                          description='Similar moves:\n**{}**'
                          .format('** **\n'.join(similar_moves)))
    return embed


def help_embed():
    text = "" \
           "!character move\t\t\t- get frame data of a move from a character \n" \
           "!auto-delete seconds\t\t\t-    change the duration of the bot waiting until he deletes the message in " \
           "this channel (-1 = deactivate)\n" \
           "?feedback message\t\t\t- send message including sender name to the devs \n\n " \
           "This bot deletes its messages after 20 seconds normally. You can configure this by using !auto-delete " \
           "function "
    embed = discord.Embed(title='Commands', description=text, colour=0x37ba25)
    embed.set_author(name='Author: Tib#1303')

    return embed


def thank_embed():
    text = "\n\n" \
           "Much thanks and love especially to T7Chicken Team, Ruxx, BKNR, Vesper, Maxwell and Evil. \n\n" \
           "This project won't be possible without you guys <3"
    embed = discord.Embed(title='Commands', description=text, colour=0x37ba25)
    embed.set_author(name='Author: Tib')
    return embed
