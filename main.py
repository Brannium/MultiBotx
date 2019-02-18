import os
import asyncio as asyncio
import re

import discord
from discord import Game, Embed

import autoclear_manager
import onlinetime_manager
import STATICS
import role_manager
from commands import cmd_ping, cmd_autorole, cmd_sortConfig, cmd_channelid, cmd_userid, cmd_onlinetime, cmd_config

client = discord.Client()

onlinetime_mngr = onlinetime_manager

commands = {

    "autorole": cmd_autorole,
    "channelid": cmd_channelid,
    "config": cmd_config,
    "onlinetime": cmd_onlinetime,
    "ping": cmd_ping,
    "sortConfig": cmd_sortConfig,
    "userid": cmd_userid

}


@client.event
async def on_ready():
    print('Bot is logged in successfully. Running on servers:\n')
    for s in client.servers:
        print(" - %s (%s)" % (s.name, s.id))

    await client.change_presence(game=Game(name="v0.5.1.2"))

    await onlinetime_mngr.check_online_members(client)

@client.event
@asyncio.coroutine
def on_message(message):

    # Checking message for defined prefix and call command class
    if message.content.startswith(STATICS.PREFIX):
        # Split command into invoke and args
        split = message.content.split(' ', 1)
        invoke = split[0][len(STATICS.PREFIX):]
        if len(split) > 1:
            args = re.findall('"[\w\s]+"|\w+', split[1])
            # remove " from individual strings in args
            for i in range(len(args)):
                args[i] = args[i].strip('"')
        else:
            args = []

        print("[Command] from %s: %s" % (message.author, message.content))

        if commands.__contains__(invoke):
            yield from commands.get(invoke).ex(message, invoke, args, client)
        else:
            yield from client.send_message(message.channel, embed=Embed(color=discord.Color.red(), description=("There is no such command: %s" % invoke)))


@client.event
async def on_member_update(before, after):

    # check members game and call role_manager
    if after.game is not None:
        await role_manager.ex(after, client)


@client.event
async def on_voice_state_update(before, after):

    await autoclear_manager.ex(client, before, after)
    await onlinetime_mngr.ex(client, before, after)


# start bot with access-token defined as system variable
access_token = os.environ.get('ACCESS_TOKEN')
if access_token is not None:
    client.run(access_token)
else:
    print("No Token found! Bot is not running!")
