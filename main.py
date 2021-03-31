import os

from discord.ext.commands import Bot

bot = Bot('.')


@bot.event
async def on_ready():
    print('is on')


bot.load_extension('mooseun_cog')

bot.run(os.environ['BOT_TOKEN'])
