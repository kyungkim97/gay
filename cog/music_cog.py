import youtube_dl as youtube_dl
from discord import FFmpegPCMAudio
from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands


class MusicCog(Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx: Context):
        if ctx.author.voice is not None:
            await ctx.author.voice.channel.connect()
            await ctx.send('접속함')

    @commands.command()
    async def play(self, ctx: Context, url: str):
        voice = None
        for vc in self.bot.voice_clients:
            if vc.guild == ctx.guild:
                voice = vc
                break

        option = {
            'outtmpl_': 'file/' + url.split('=')[1] + '.mp3'
        }

        with youtube_dl.YoutubeDL(option) as ydl:
            ydl.download(url)
            info = ydl.extract_info(url, download=False)
            title = info["title"]

        if voice is not None:
            voice.play(FFmpegPCMAudio("file/" + url.split('=')[1] + ".mp3"))
            await ctx.send(title + "is playing now")
        else:
            await ctx.send('오류가발생했음')


    @commands.command()
    async def leave(self, ctx: Context):
        await self.bot.voice.channel.disconnect()
        await ctx.send('나감')


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
