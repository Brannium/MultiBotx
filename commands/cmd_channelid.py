import discord


def ex(message, invoke, args, client):

    yield from send_embeded_message("Channel-ID: %s" % message.channel.id, message.channel, discord.Color.blue(), client)


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
