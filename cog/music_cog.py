from urllib.parse import parse_qs, urlparse

import youtube_dl as youtube_dl
from discord import FFmpegPCMAudio
from discord.ext.commands import Cog, Context, Bot
from discord.ext import commands


def extract_video_id(url):
    # Examples:
    # - http://youtu.be/SA2iWivDJiE
    # - http://www.youtube.com/watch?v=_oPAwA_Udwc&feature=feedu
    # - http://www.youtube.com/embed/SA2iWivDJiE
    # - http://www.youtube.com/v/SA2iWivDJiE?version=3&amp;hl=en_US
    query = urlparse(url)
    if query.hostname == 'youtu.be': return query.path[1:]
    if query.hostname in {'www.youtube.com', 'youtube.com'}:
        if query.path == '/watch': return parse_qs(query.query)['v'][0]
        if query.path[:7] == '/embed/': return query.path.split('/')[2]
        if query.path[:3] == '/v/': return query.path.split('/')[2]
    # fail?
    return None


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
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': 'file/' + extract_video_id(url)
        }

        with youtube_dl.YoutubeDL(option) as ydl:
            ydl.download([url])
            info = ydl.extract_info(url, download=False)
            title = info["title"]

        if voice is not None:
            voice.play(FFmpegPCMAudio("file/" + extract_video_id(url) + ".mp3"))
            await ctx.send(title + "is playing now")
        else:
            await ctx.send('오류가발생했음')

    @commands.command()
    async def leave(self, ctx: Context):
        await self.bot.voice.channel.disconnect()
        await ctx.send('나감')


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
