"""
Основная логика
"""
import discord
from settings_local import *

class DiscordClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        # следить только за одним каналом
        if message.channel.id != TRACK_CHANNEL_ID:
            return
        # игнорировать сообщения ботов
        if message.author.bot == True:
            return

        # если в сообщении есть вложения
        if message.attachments:
            # перебор всех вложений в сообщении на поиск картинок
            extensions = [".png", ".jpg", ".jpeg", ".gif"]
            reposts = list()
            for attachment in message.attachments:
                if not any(ext in attachment.url for ext in extensions):
                    continue
                content = "Оригинал: https://discord.com/channels/{}/{}/{}".format(
                    message.guild.id, message.channel.id, message.id)
                reposts.append({"content": content, "url": attachment.url})
            # отправляем картинки в канал скриншотов
            for pic in reposts:
                forward = self.get_channel(FORWARD_CHANNEL_ID)
                embed = discord.Embed()
                embed.set_image(url=pic['url'])
                await forward.send(content=pic['content'], embed=embed)

client = DiscordClient()
client.run(TOKEN)
