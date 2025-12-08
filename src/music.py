import discord
from discord.ext import commands
import yt_dlp, os
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
            'no_warnings': True,
        }

class MusicPlayer:
    def __init__(self, ctx:commands.Context):
        self.ctx= ctx
        self.queue= deque()
        self.current= None

    async def playNext(self):
        if len(self.queue) > 0:
            self.current= self.queue.popleft()
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download(self.current['url'])
                
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")

                voice = discord.utils.get(self.ctx.bot.voice_clients, guild=self.ctx.guild)
                if voice.playing:
                    voice.stop()
                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: self.ctx.bot.loop.create_task(self.play_next()))


                await self.ctx.send("playing...\nIdk LOL")
            except Exception as error:
                await self.ctx.send(f"what? {error}")
    
    def addQueue(self, url:str, title:str):
        self.queue.append({"url": url, "title":title})

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
            description="Toca música"
        )
    async def playCommand(self, ctx:commands.Context, url):
        if not ctx.voice_client:
            await ctx.send("I'm not in a vc (UwU)")
            return

        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                title = info['title']
                player.addQueue(url, title)
        except Exception as error:
            await ctx.send(f"wtf... {error}")

        if not player.current:
            await player.playNext()

    
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
        player.play_next()
            
    

async def setup(bot):
    await bot.add_cog(music(bot))