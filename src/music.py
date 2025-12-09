import discord
from discord.ext import commands
import yt_dlp, os
import datetime
from collections import deque # gonna kms, this code... I hate this code...
# Why? IDK

ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'progress': True,
            'writethumbnail': True,
            'no_warnings': True,
        }

class Song:
    def __init__(self, url:str):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            self.info= ydl.extract_info(url, download=False)
            self.url= self.info['url']
            self.originalUrl= url
            self.title= self.info['title']
            self.description= self.info.get('description', None)
            self.duration = self.info.get('duration', None)
            self.thumbnail = self.info.get('thumbnail', None)
    
    def embed(self) -> discord.Embed:
        embed= discord.Embed(
            title=self.title,
            url=self.originalUrl,
            description=f"{self.description}\n\nTime: {self.TotalDuration()}"
        )
        embed.set_image(url=self.thumbnail)
        return embed
    
    def TotalDuration(self) -> str:
        if self.duration:
            t= datetime.timedelta(seconds=self.duration)
            return f"{int(t.total_seconds() // 60)}:{int(t.total_seconds() % 60):02}"
        return "00:00"


class MusicPlayer:
    def __init__(self, ctx:commands.Context):
        self.ctx= ctx
        self.queue= deque()
        self.current:Song= None

    async def playNext(self):
        if len(self.queue) > 0:
            self.current= self.queue.popleft()
            try:
                voice = discord.utils.get(self.ctx.bot.voice_clients, guild=self.ctx.guild)
                if voice and voice.is_playing():
                    voice.stop()
                voice.play(discord.FFmpegPCMAudio(self.current.url), after=lambda e: self.ctx.bot.loop.create_task(self.playNext()))
            except Exception as error:
                await self.ctx.send(f"what? {error}")
    
    def Queue(self):
        tmp= ""

        for song in self.queue:
            tmp += f"{song.title} - [Url]({song.originalUrl})\n"

        embed=discord.Embed(
            title="Queue 🎧",
            description=tmp
        )
        embed.set_thumbnail(url=self.current.thumbnail)
        embed.set_footer(text=f"Current: {self.current.title}")
        return embed

    def addQueue(self, song:Song):
        self.queue.append(song)

class music(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.players = {}
        super().__init__()


    @commands.command(
        name="join",
        description="Entra na call atual :3")
    async def joinCommand(self, ctx:commands.Context):
        if not ctx.author.voice:
            await ctx.send("Not connected (What?)")
            return
        
        channel= ctx.author.voice.channel
        try:
            await channel.connect()
            await ctx.send("Connected :3")
        except Exception as error:
            await ctx.send(f"wtf... {error}")
    

    @commands.command(
            name="play",
            description="Toca música",
            aliases=["p", "yt"]
        )
    async def playCommand(self, ctx:commands.Context, url:str):
        if not ctx.voice_client:
            await ctx.send("I'm not in a vc (UwU)")
            return

        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]

        song= Song(url)
        player.addQueue(song)

        if not player.current:
            await player.playNext()
            await ctx.send(embed=song.embed())
        else:
            await ctx.send("added to queue")

    
    @commands.command(
        name="next",
        description="Passa pra prox musica")
    async def nextCommand(self, ctx:commands.Context):
        if not ctx.author.voice:
            await ctx.send("Not connected (What?)")
            return
        
        channel= ctx.author.voice.channel
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]
        player.playNext()
            
    @commands.command(
        name="queue",
        description="Vê a queue)")
    async def queueCommand(self, ctx:commands.Context):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]
        
        queue= player.Queue()
        await ctx.send(embed=queue)


    @commands.command(
        name="playing",
        aliases=["current", "c"],
        description="Que música tá tocando?")
    async def playingCommand(self, ctx:commands.Context):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]
        
        current= player.current
        await ctx.send(embed=current.embed())

async def setup(bot):
    await bot.add_cog(music(bot))