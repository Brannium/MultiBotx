import discord

from utility import sqlHandler

db = sqlHandler.MyDatabase()

async def ex(member, client):

    config = db.get_config(member.server.id)
    if config['autorole']['enabled']:
        if not on_roleblacklist(member, config['autorole']['roleblacklist']):
            for key, value in config['autorole']['links'].items():
                if key == member.game.name:
                    role = discord.utils.get(member.server.roles, name=value)
                    if role is not None:
                        if not member.roles.__contains__(role):
                            print('Member %s got role %s' % (member, role))
                            await client.add_roles(member, role)


def on_roleblacklist(member, list):

    for element in list:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False
