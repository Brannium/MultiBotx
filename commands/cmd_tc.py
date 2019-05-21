from manager import level_role_manager


async def ex(message, invoke, args, client):

    lrm = level_role_manager

    # Check permissions
    if message.author.id == '316610049927675917':
        await lrm.job(client)