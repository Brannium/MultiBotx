import discord

from utility import ConfigManager

cm = ConfigManager


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))


def ex(message, invoke, args, client):

    if not has_permission(message.author):
        yield from send_embeded_message('You do not have the permissions to execute this command!', message.channel, discord.Color.red(), client)
        return

    if len(args) == 0:
        # no arguments --> show current autorole status
        json_decoded = cm.getConfig(message.server)
        yield from send_embeded_message('Autorole is currently %s' % json_decoded['autorole']['enabled'],
                                        message.channel, discord.Color.blue(), client)

    elif len(args) == 1:
        # one argument, e.g. help/enable/disable/list/link/unlink

        if args[0] == 'help':
            # show help message

            yield from show_help(message, client)

        elif args[0] == 'enable':
            # enable autorole feature

            json_decoded = cm.getConfig(message.server)
            json_decoded['autorole']['enabled'] = True
            cm.saveConfig(message.server, json_decoded)

            yield from send_embeded_message('Autorole is now enabled!', message.channel, discord.Color.green(), client)

        elif args[0] == 'disable':
            # disable autorole feature

            json_decoded = cm.getConfig(message.server)
            json_decoded['autorole']['enabled'] = False
            cm.saveConfig(message.server, json_decoded)

            yield from send_embeded_message('Autorole is now disabled!', message.channel, discord.Color.green(), client)

        elif args[0] == 'list':
            # show list of current links

            json_decoded = cm.getConfig(message.server)
            current_links = 'Current links(Game - Role):\n'
            for key, value in json_decoded['autorole']['links'].items():
                current_links += ('\n%s - %s' % (key, value))
            yield from send_embeded_message(current_links, message.channel, discord.Color.blue(), client)

        elif args[0] == 'link':
            # show syntax for link

            yield from send_embeded_message('Not the correct syntax, use \'autorole link [game] [role]\'', message.channel, discord.Color.red(), client)

        elif args[0] == 'unlink':
            # show syntax for unlink

            yield from send_embeded_message('Not the correct syntax, use \'autorole unlink [game]\'', message.channel, discord.Color.red(), client)

        else:
            # argument can not be used

            yield from send_embeded_message('Not a valid argument, use \'autorole help\'', message.channel, discord.Color.red(), client)


def show_help(message, client):
    yield from send_embeded_message('Usage:\n--autorole [enable, disable, list]', message.channel, discord.Color.blue(), client)


def has_permission(member):
    config = cm.getConfig(member.server)
    for element in config['autorole']['permissions']:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False
