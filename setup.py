import subprocess
import sys
import os

import discord
from io import BytesIO
import asyncio

channel_fetch = [1171620108301520956, 1171621051034247258, 1329920795073318994, 1352665901127696488]

NE_channel_send = [1288328300804177920, 1358273610451779634, 1358273639555793076, 1358273678940573918]

PP_channel_send = [1289680351517478987, 1358273610451779634, 1358273639555793076, 1358273678940573918]

async def save_attachment(file):
    byte_stream = BytesIO()
    await file.save(byte_stream, seek_begin=True, use_cached=False)
    byte_stream.seek(0)
    return byte_stream

class Client(discord.Client):
    def __init__(self, client):
        super().__init__()
        self.picks_fetch_channel = [None, None, None, None]

        self.NE_picks_channel = [None, None, None, None]

        self.PP_picks_channel = [None, None, None, None]

        self.client = None

    async def on_ready(self):
        
        self.picks_fetch_channel =  [
                                    await self.client.fetch_channel(channel_fetch[0]),
                                    await self.client.fetch_channel(channel_fetch[1]),
                                    await self.client.fetch_channel(channel_fetch[2]), 
                                    await self.client.fetch_channel(channel_fetch[3])
                                    ]

        self.NE_picks_channel = [
                                await self.client.fetch_channel(NE_channel_send[0]),
                                await self.client.fetch_channel(NE_channel_send[1]),
                                await self.client.fetch_channel(NE_channel_send[2]),
                                await self.client.fetch_channel(NE_channel_send[3])
                                ]

        self.PP_picks_channel = [
                                await self.client.fetch_channel(PP_channel_send[0]),
                                await self.client.fetch_channel(PP_channel_send[1]),
                                await self.client.fetch_channel(PP_channel_send[2]),
                                await self.client.fetch_channel(PP_channel_send[3])
                                ]

        print('Logged on')

    async def on_message(self, message):
        for i in range(0, channel_fetch):
            if message.channel.id == channel_fetch[i]:
                if not hasattr(message, 'embeds'):
                    return

                if len(message.attachments) > 0:
                    for i in message.attachments:
                        print("image")
                        # Code to convert attachment into byte data (allows you to send the image without saving it to filesystem)
                        bytedata = await save_attachment(i)
                        file = discord.File(bytedata, filename="image.png")

                        await self.NE_picks_channel[i].send(content=message.content, file=file)
                        await self.PP_picks_channel[i].send(content=message.content, file=file)

                else:
                    print("text")
                    await self.NE_picks_channel[i].send(message.content)
                    await self.PP_picks_channel[i].send(message.content)

    async def on_message_edit(self, before, after):
        for i in range(0, channel_fetch):
            if before.channel.id == channel_fetch[i]:
                print("edit")
                await self.NE_picks_channel[i].send(content = after.content)
                await self.PP_picks_channel[i].send(content = after.content)

client = Client(client=None)
client.client = client  # Assigning the client instance to itself
client.run("")
