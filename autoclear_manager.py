import discord

from utility import sqlHandler

db = sqlHandler.MyDatabase()

async def ex(client, before, after):

    config = db.get_config(after.server.id)

    if config['autoclear']['enabled']:
        for user_id, channel_id in config['autoclear']['links'].items():
            if user_id == after.id:
                if after.voice.voice_channel is None and before.voice.voice_channel is not None:
                    channel = discord.utils.get(after.server.channels, id=channel_id)
                    user = discord.utils.get(after.server.members, id=user_id)
                    print('Clearing channel \'%s\'(%s) as \'%s\'(%s) left the voice channel' % (channel.name, channel_id, user, user_id))
                    await client.purge_from(channel, limit=100, check=is_not_pinned)


def is_not_pinned(m):
    return not m.pinned
