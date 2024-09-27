import subprocess
import sys
import os
    
if sys.platform != "win32":
    venvdir = os.path.abspath(os.path.join(os.getcwd(), 'venv\\Scripts'))
    #print(venvdir)
    subprocess.run(['pwd'])
    #subprocess.run([".workspace/venv/Scripts/activate"])

import discord
from io import BytesIO
import asyncio

channel_id_fetch = 510901019077771264 #1171620108301520956  # Channel to get images from
channel_id_send = 1288328300804177920  # Channel to send images to

async def save_attachment(file):
    byte_stream = BytesIO()
    await file.save(byte_stream, seek_begin=True, use_cached=False)
    byte_stream.seek(0)
    return byte_stream


class Client(discord.Client):
    def __init__(self, client):
        super().__init__()
        self.message_fetch_channel = None
        self.message_send_channel = None
        self.client = None

    async def on_ready(self):
        self.message_fetch_channel = await self.client.fetch_channel(channel_id_fetch)
        self.message_send_channel = await self.client.fetch_channel(channel_id_send)

        print('Logged on')
    try:
        async def on_message(self, message):
            if message.channel.id == channel_id_fetch:
                if not hasattr(message, 'embeds'):
                    return

                if len(message.attachments) > 0:
                    for i in message.attachments:
                        print("image")
                        # Code to convert attachment into byte data (allows you to send the image without saving it to filesystem)
                        bytedata = await save_attachment(i)
                        file = discord.File(bytedata, filename="image.png")

                        await self.message_send_channel.send(content=message.content, file=file)

                else:
                    print("text")
                    await self.message_send_channel.send(message.content)
                    
        async def on_message_edit(self, before, after):
            print("edit")
            await self.message_send_channel.send(content = after.content)
    except:
        print("crash happened")

client = Client(client=None)
client.client = client  # Assigning the client instance to itself
client.run("MTI4ODI5MzQ4OTg2MzQzMDIyOA.G-K5Fi.YsVtd0PFwDToSPXQrkZAkDgQCcNd4zxwrCPLyU")
