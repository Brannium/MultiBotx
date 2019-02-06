import discord

from utility import sqlHandler

db = sqlHandler.MyDatabase()


def ex(message, invoke, args, client):

    stats = db.get_stats(message.server.id)
    onlinetime = stats['onlinetime'][args[0]]

    if onlinetime:
        yield from send_embeded_message(
            'User %s was online for %s seconds in total' % (args[0], onlinetime), message.channel, discord.Color.blue(),client)
    else:
        yield from send_embeded_message('User %s was not online yet' % args[0], message.channel, discord.Color.blue(), client)


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
