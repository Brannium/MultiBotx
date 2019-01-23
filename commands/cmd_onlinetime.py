from utility import statsManager

sm = statsManager


async def ex(message, invoke, args, client):

    json_decoded = sm.getStats(message.server)
    print('User %s was online for %s seconds in total' % (args[0], json_decoded['onlinetime'][message.author.id]))


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
