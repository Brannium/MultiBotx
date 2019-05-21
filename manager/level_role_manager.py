import asyncio
import datetime

import discord
from dateutil.relativedelta import *

from manager import role_manager
from utility import sqlHandler

db = sqlHandler.MyDatabase()


class Timer:
    def __init__(self, timeout, callback, args):
        self._timeout = timeout
        self._callback = callback
        self._args = args
        self._task = asyncio.ensure_future(self._job())

    async def _job(self):
        await asyncio.sleep(self._timeout)
        await self._callback(*self._args)

    def cancel(self):
        self._task.cancel()


async def job(client):
    print('[Onlinetime Level Role] running monthly level update')
    for s in client.servers:

        config = db.get_config(s.id)
        # check if levelrole is enabled
        if config['levelrole']['enabled']:
            stats = db.get_stats(s.id)

            for m in s.members:

                # check if user is not blacklisted for levelrole
                if not role_manager.on_roleblacklist(m, config['levelrole']['roleblacklist']):

                    online_time = stats['onlinetime'][m.id]
                    roles = config['levelrole']['roles']
                    online_times = config['levelrole']['onlinetimes']
                    online_times.append(float('inf'))
                    if not online_time:
                        online_time = 0
                    #print('[Onlinetime Level Role] member \'%s\' on server \'%s\': %ss' % (m, s, online_time))
                    index = index_of_highest_level_role(m, config['levelrole']['roles'])
                    if index == -1:
                        if online_time >= online_times[index + 1]:
                            role = discord.utils.get(s.roles, name=roles[index + 1])
                            print('[Onlinetime Level Role] Member %s got role %s' % (m, role))
                            await client.add_roles(m, role)
                    elif index >= 0:
                        if online_time >= online_times[index + 1]:
                            role = discord.utils.get(s.roles, name=roles[index + 1])
                            role_lost = discord.utils.get(s.roles, name=roles[index])
                            print('[Onlinetime Level Role] Member %s got role %s and lost role %s' % (m, role, role_lost))
                            await client.add_roles(m, role)
                            await client.remove_roles(m, role_lost)
                        elif online_time <= online_times[index]:
                            role = discord.utils.get(s.roles, name=roles[index])
                            print('[Onlinetime Level Role] Member %s lost role %s' % (m, role))
                            await client.remove_roles(m, role)
                        else:
                            role = discord.utils.get(s.roles, name=roles[index])
                            print('[Onlinetime Level Role] Member %s keeps role %s' % (m, role))
                stats['onlinetime'][m.id] = 0
            db.save_stats(s.id, stats)
    print('[Onlinetime Level Role] finished monthly update')
    start_timer(client)


def index_of_highest_level_role(member, role_names):
    for i, role_name in enumerate(reversed(role_names)):
        role = discord.utils.get(member.server.roles, name=role_name)
        if member.roles.__contains__(role):
            return len(role_names) - i - 1
    return -1


def seconds_to_next_month():
    dt = datetime.datetime.now()
    start = dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    start += relativedelta(months=+1)
    x = (start - dt).total_seconds()
    print('[Onlinetime Level Role] performing next update in %s seconds' % round(x))
    return x


def start_timer(client):
    Timer(seconds_to_next_month(), job, [client])
