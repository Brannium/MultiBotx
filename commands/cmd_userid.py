import discord


def ex(message, invoke, args, client):
    if len(args) == 0:
        yield from send_embeded_message("%s\'s ID: %s" % (message.author, message.author.id), message.channel,
                                        discord.Color.blue(), client)
    else:
        arg = ' '.join(args)

        if not arg.__contains__('#'):
            yield from send_embeded_message('Wrong user format! Use --userid [username#1234]', message.channel,
                                            discord.Color.red(), client)
            return

        member = discord.utils.get(message.server.members, name=arg.split('#')[0], discriminator=arg.split('#')[1])
        if member:
            yield from send_embeded_message("%s\'s ID: %s" % (member, member.id), message.channel, discord.Color.blue(),
                                            client)
        else:
            yield from send_embeded_message('Member %s not found' % arg, message.channel, discord.Color.blue(), client)


def send_embeded_message(content, channel, color, client):
    yield from client.send_message(channel, embed=discord.Embed(color=color, description=content))
