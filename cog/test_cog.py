from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands

from bitcoin import get_doge, get_bitcoin, get_ethereum
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

    @commands.command()
    async def doge(self, ctx: Context):
        await ctx.send(f'DOGE now : {format(get_doge(), ",")} KRW')

    @commands.command()
    async def btc(self, ctx: Context):
        await ctx.send(f'BTC now : {format(get_bitcoin(), ",")} KRW')

    @commands.command()
    async def eth(self, ctx: Context):
        await ctx.send(f'ETH now : {format(get_ethereum(), ",")} KRW')


def setup(bot: Bot):
    bot.add_cog(TestCog())
