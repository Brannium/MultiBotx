import discord
from utility import ConfigManager

cm = ConfigManager

def ex(message, invoke, args, client):
    if has_permission(message.author):
        config = cm.getConfig(message.server)
        cm.saveConfig(message.server, config)
        yield from send_embeded_message('Config sorted!', message.channel, discord.Color.green(), client)
    else:
        yield from send_embeded_message('You don\'t have the permission to execute this command!', message.channel, discord.Color.red(), client)


def has_permission(member):
    config = cm.getConfig(member.server)
    for element in config['autorole']['permissions']:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
