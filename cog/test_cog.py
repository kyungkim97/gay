from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands


class TestCog(Cog):
    @commands.command()
    async def ping(self, ctx: Context):
        await ctx.send('pong!')


def setup(bot: Bot):
    bot.add_cog(TestCog())
