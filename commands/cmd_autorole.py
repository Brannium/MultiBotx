import discord

from utility import sqlHandler

db = sqlHandler.MyDatabase()


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))


def ex(message, invoke, args, client):
    if not has_permission(message.author):
        yield from send_embeded_message('You do not have the permissions to execute this command!', message.channel,
                                        discord.Color.red(), client)
        return

    if len(args) == 0:
        # no arguments --> show current autorole status
        config = db.get_config(message.server.id)
        yield from send_embeded_message('Autorole is currently %s' % config['autorole']['enabled'],
                                        message.channel, discord.Color.blue(), client)

    elif len(args) == 1:
        # one argument, e.g. help/enable/disable/list/link/unlink

        if args[0] == 'help':
            # show help message

            yield from show_help(message, client)

        elif args[0] == 'enable':
            # enable autorole feature

            config = db.get_config(message.server.id)
            config['autorole']['enabled'] = True
            db.save_config(message.server.id, config)

            yield from send_embeded_message('Autorole is now enabled!', message.channel, discord.Color.green(), client)

        elif args[0] == 'disable':
            # disable autorole feature

            config = db.get_config(message.server.id)
            config['autorole']['enabled'] = False
            db.save_config(message.server.id, config)

            yield from send_embeded_message('Autorole is now disabled!', message.channel, discord.Color.green(), client)

        elif args[0] == 'list':
            # show list of current links

            config = db.get_config(message.server.id)
            current_links = 'Current links(Game - Role):\n'
            for key, value in config['autorole']['links'].items():
                current_links += ('\n%s - %s' % (key, value))
            yield from send_embeded_message(current_links, message.channel, discord.Color.blue(), client)

        elif args[0] == 'link':
            # show syntax for link

            yield from send_embeded_message('Not the correct syntax, use \'autorole link [game] [role]\'',
                                            message.channel, discord.Color.red(), client)

        elif args[0] == 'unlink':
            # show syntax for unlink

            yield from send_embeded_message('Not the correct syntax, use \'autorole unlink [game]\'', message.channel,
                                            discord.Color.red(), client)

        else:
            # argument can not be used

            yield from send_embeded_message('Not a valid argument, use \'autorole help\'', message.channel,
                                            discord.Color.red(), client)

    elif len(args) == 2:

        if args[0] == 'unlink':
            config = db.get_config(message.server.id)
            if config['autorole']['links'][args[1]]:
                yield from send_embeded_message(
                    'Removed link from game \'%s\' to role \'%s\'' % (args[1], config['autorole']['links'][args[1]]),
                    message.channel, discord.Color.green(), client)
                del config['autorole']['links'][args[1]]
                db.save_config(message.server.id, config)
            else:
                yield from send_embeded_message('Can\'t find %s in config, nothing was removed' % args[1],
                                                message.channel, discord.Color.blue(), client)

        else:
            yield from show_help(message, client)

    elif len(args) == 3:

        if args[0] == 'link':
            config = db.get_config(message.server.id)
            config['autorole']['links'][args[1]] = args[2]
            db.save_config(message.server.id, config)
            yield from send_embeded_message('Game \'%s\' successfully linked to role \'%s\'' % (args[1], args[2]),
                                            message.channel, discord.Color.green(), client)

        else:
            yield from show_help(message, client)

    else:
        # to many arguments, show help

        yield from send_embeded_message('To many arguments!', message.channel, discord.Color.blue(), client)
        yield from show_help(message, client)


def show_help(message, client):
    yield from send_embeded_message('Usage:'
                                    '\n--autorole [enable, disable, list, help]'
                                    '\n--autorole link *game* *role*'
                                    '\n--autorole unlink *game*', message.channel, discord.Color.blue(), client)


def has_permission(member):
    config = db.get_config(member.server.id)
    for element in config['autorole']['permissions']:
        role = discord.utils.get(member.server.roles, name=element)
        if role is not None:
            if member.roles.__contains__(role):
                return True
    return False
