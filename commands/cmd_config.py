import json

import discord

from utility import sqlHandler

db = sqlHandler.MyDatabase()


def ex(message, invoke, args, client):
    config = db.get_config(message.server.id)
    yield from send_embeded_message(json.dumps(config, indent=2), message.channel, discord.Color.blue(), client)


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))

