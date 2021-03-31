from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands


class Exitcode(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: Context):
        if ctx.author.voice is not None:
            await ctx.author.voice.channel.connect()
            await ctx.send('접속함')

    @commands.command()
    async def leave(self, ctx: Context):
        await self.bot.voice.channel.disconnect()
        await ctx.send('나감')


def setup(bot: Bot):
    bot.add_cog(Exitcode(bot))
