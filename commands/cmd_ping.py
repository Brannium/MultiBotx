def ex(message, invoke, args, client):
    response = yield from client.send_message(message.channel, ":hourglass_flowing_sand:")
    time = (response.timestamp - message.timestamp).total_seconds() * 1000
    yield from client.edit_message(response, new_content=':hourglass_flowing_sand:%sms' % round(time))