import discord
from utility import sqlHandler

db = sqlHandler.MyDatabase()

def ex(message, invoke, args, client):
    if has_permission(message.author):
        config = db.get_config(message.server.id)
        db.save_config(message.server.id, config)
        yield from send_embeded_message('Config sorted!', message.channel, discord.Color.green(), client)
    else:
        yield from send_embeded_message('You don\'t have the permission to execute this command!', message.channel, discord.Color.red(), client)


def has_permission(member):
    config = db.get_config(member.server.id)
    for element in config['autorole']['permissions']:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
