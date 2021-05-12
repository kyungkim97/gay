from os.path import isfile
from urllib.parse import parse_qs, urlparse

import discord
import youtube_dl as youtube_dl
from discord import FFmpegPCMAudio, TextChannel
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

        self.playing = False
        self.queue = list()

    @commands.command()
    async def j(self, ctx: Context):
        if ctx.author.voice is not None:
            await ctx.author.voice.channel.connect()
            await ctx.send('접속함')

    def download_audio(self, url):
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

        return title

    def play_next(self, error, voice):
        if self.queue:
            url = self.queue.pop(0)

            self.download_audio(url)

            voice.play(FFmpegPCMAudio("file/" + extract_video_id(url) + ".mp3"),
                       after=lambda error_: self.play_next(error_, voice))
        else:
            self.playing = False

    @commands.command()
    async def p(self, ctx: Context, url: str):
        if self.playing:
            self.queue.append(url)
            await ctx.send('노래가 추가')
        else:
            voice = None
            for vc in self.bot.voice_clients:
                if vc.guild == ctx.guild:
                    voice = vc
                    break
            if not isfile(filename := "file/" + extract_video_id(url) + ".mp3"):
                title = self.download_audio(url)
            else:
                title = '노래'

            if voice is not None:
                voice.play(FFmpegPCMAudio(filename),
                           after=lambda error: self.play_next(error, voice))
                await ctx.send(title + " is playing now")
                self.playing = True
            else:
                await ctx.send('오류가발생했음')

    @commands.command()
    async def pause(self, ctx: Context):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)  # 봇의 음성 관련 정보
        if voice.is_playing():  # 노래가 재생중이면
            voice.pause()  # 일시정지
            await ctx.send('노래 멈춤')
        else:
            await ctx.send("재생중인 곡 없음")  # 오류(?)

    # 다시 재생
    @commands.command()
    async def resume(self, ctx: Context):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)  # 봇의 음성 관련 정보
        if voice.is_paused():  # 일시정지 상태이면
            voice.resume()
            await ctx.send('노래 다시 재생')
        else:
            await ctx.send("일시정지 아님")  # 오류(?)

    # 정지
    @commands.command()
    async def stop(self, ctx: Context):
        await self.bot.voice_clients[0].disconnect()
        await ctx.send('나감')


def setup(bot: Bot):
    bot.add_cog(MusicCog(bot))
