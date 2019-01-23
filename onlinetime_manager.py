import time

from utility import statsManager

sm = statsManager

went_online_time = dict()


async def ex(client, before, after):

    if (before.voice.is_afk and not after.voice.is_afk):
        # Member went from afk to active
        print('[Onlinetime Manager] %s is no longer afk')
        if (after.voice.voice_channel is not None):
            # User is active in a voice channel
            await went_online(after.id)
    if (not before.voice.is_afk and after.voice.is_afk):
        # Member went afk
        print('[Onlinetime Manager] %s is now afk')
        if (before.voice.voice_channel is not None):
            # Member is no longer active in that voice channel
            await went_offline(before.id)
    # Check if member joined or left a channel
    if (before.voice.voice_channel is None and after.voice.voice_channel is not None):
        # Member joined a channel
        print('[Onlinetime Manager] %s joined a channel' % after.name)
        await went_online(after.id)

    if (before.voice.voice_channel is not None and after.voice.voice_channel is None):
        # Member left the channel
        print('[Onlinetime Manager] %s left a channel' % after.name)
        await went_offline(after)


async def check_online_members(client):

    for s in client.servers:
        for m in s.members:
            if (m.voice.voice_channel is not None and not m.voice.is_afk):
                await went_online(m.id)
                print('[Onlinetime Manager] Member \'%s#%s (%s)\' is online' % (m.name, m.discriminator, m.display_name))

async def went_online(member_id):
    went_online_time[str(member_id)] = int(time.time())


async def went_offline(member):
    json_decoded = sm.getStats(member.server)
    if str(member.id) in went_online_time:      # check if 'user went online time' is saved
        elapsed_time = (int(time.time())) - went_online_time[str(member.id)]
        try:
            json_decoded['onlinetime'][member.id] += elapsed_time
        except KeyError:
            json_decoded['onlinetime'][member.id] = elapsed_time
        sm.saveStats(member.server, json_decoded)
        print('[Onlinetime Manager] Member \'%s#%s (%s)\' went offline after being online for %s seconds' % (member.name, member.discriminator, member.display_name, elapsed_time))   # TODO give seconds in Minutes and hours
        del went_online_time[str(member.id)]
    else:
        print('[Onlinetime Manager] Error 101 on member \'%s#%s (%s)\'' % (member.name, member.discriminator, member.display_name))
