from telethon.tl.functions.channels import JoinChannelRequest

async def yummy(client):
    await client(JoinChannelRequest(channel='yg_modules'))