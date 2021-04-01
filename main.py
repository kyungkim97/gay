import os

from discord.ext.commands import Bot

bot = Bot('.')


@bot.event
async def on_ready():
    print(f'{bot.user.display_name} is on')


bot.load_extension('cog.music_cog')
bot.load_extension('cog.test_cog')

bot.run(os.environ['BOT_TOKEN'])
