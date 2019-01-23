import discord

from utility import ConfigManager

cm = ConfigManager


async def ex(member, client):

    config = cm.getConfig(member.server)
    if config['autorole']['enabled']:
        if not on_roleblacklist(member, config):
            for key, value in config['autorole']['links'].items():
                if key == member.game.name:
                    role = discord.utils.get(member.server.roles, name=value)
                    if role is not None:
                        if not member.roles.__contains__(role):
                            print('Member %s got role %s' % (member, role))
                            await client.add_roles(member, role)


def on_roleblacklist(member, config):

    for element in config['autorole']['roleblacklist']:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False
