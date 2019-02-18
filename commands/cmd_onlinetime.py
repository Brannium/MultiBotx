import discord

import onlinetime_manager
from utility import sqlHandler

db = sqlHandler.MyDatabase()
otm = onlinetime_manager


async def ex(message, invoke, args, client):

    if len(args) > 0:
        member_id = args[0]
    else:
        member_id = message.author.id

    try:
        member = message.server.get_member(member_id)
        await otm.save_time(member)
    except Exception as e:
        print('Error while getting member: %s' % e)

    stats = db.get_stats(message.server.id)
    onlinetime = stats['onlinetime'][member_id]

    if onlinetime:
        await send_embeded_message(
            'User %s was online for %s seconds in total' % (member_id, onlinetime), message.channel, discord.Color.blue(),client)
    else:
        await send_embeded_message('User %s was not online yet' % member_id, message.channel, discord.Color.blue(), client)


async def send_embeded_message(content, channel, color, client):
    await client.send_message(channel, embed=discord.Embed(color=color, description=content))
