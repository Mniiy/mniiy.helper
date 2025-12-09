import discord
from discord.ext import commands
from libs.song import Song 
from libs.player import MusicPlayer 
# gonna kms, this code... I hate this code...
# Why? IDK

class music(commands.Cog):
    def __init__(self, bot):
        self.bot= bot
        self.players = {}
        super().__init__()


    @commands.hybrid_command(
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
    
    @commands.hybrid_command(
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

        if 'playlist' in url:
            await player.loadPlaylist(url)
        else:
            song = Song(url)
            player.addQueue(song)

        if not player.current:
            await player.playNext()
            await ctx.send(embed=song.embed())
        else:
            await ctx.send("added to queue")
   
    @commands.hybrid_command(
        name="queue",
        description="Vê a queue)")
    async def queueCommand(self, ctx:commands.Context):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]
        
        queue= player.Queue()
        await ctx.send(embed=queue)

    @commands.hybrid_command(
        name="loop",
        aliases=["l"],
        description="Repete a música")
    async def playingCommand(self, ctx:commands.Context):
        if ctx.guild.id not in self.players:
            self.players[ctx.guild.id] = MusicPlayer(ctx)

        player = self.players[ctx.guild.id]
        
        player.loop()
        await ctx.send(embed=current.embed())



async def setup(bot):
    await bot.add_cog(music(bot))