

def ex(message, invoke, args, client):
    yield from client.send_message(message.channel, "Pong!")