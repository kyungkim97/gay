from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands

from hangang import get_temperature


class TestCog(Cog):
    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('pong!')

    @commands.command()
    async def hg(self, ctx: Context, unit: str = 'C'):
        if unit.upper() == 'F':
            await ctx.send(f'한강온도: {get_temperature() * 1.8 + 32}°F')
        else:
            await ctx.send(f'한강온도: {get_temperature()}°C')


def setup(bot: Bot):
    bot.add_cog(TestCog())
