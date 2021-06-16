from discord.ext import commands
from discord.ext import tasks
from discord.ext.commands import Cog, Context, Bot

from bitcoin import get_doge, get_bitcoin, get_ethereum
from corona import get_corona
from hangang import get_temperature


class TestCog(Cog):
    def __init__(self, bot):
        self.bot = bot

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

    @Cog.listener()
    async def on_ready(self):
        self.corona_loop.start()

    @tasks.loop(seconds=21600)
    async def corona_loop(self):
        main_channel = self.bot.get_channel(764417709098139660)
        anchor_date, confirmation, isolation, dead = get_corona()
        await main_channel.send(f'{anchor_date} 확진자는 '
                                f'`{confirmation}`명 격리자는 `{isolation}`명, 사망자는 `{dead}`명입니다.')


def setup(bot: Bot):
    bot.add_cog(TestCog(bot))
