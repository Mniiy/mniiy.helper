import yt_dlp
from libs.song import Song 
import discord
from collections import deque


class MusicPlayer:
    def __init__(self, Context):
        self.Context= Context
        self.queue= deque()
        self.current:Song= None

    async def playNext(self):
        if len(self.queue) > 0:
            try:
                self.current= self.queue.popleft()
                voice = discord.utils.get(self.Context.bot.voice_clients, guild=self.Context.guild)
                voice.play(discord.FFmpegPCMAudio(self.current.url), after=lambda e: self.Context.bot.loop.create_task(self.playNext()))
            except Exception as error:
                await self.Context.send(f"what? {error}")
        else:
            self.Context.send("Track ended.")
            self.current= None

    async def loadPlaylist(self, url: str):
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            playlist_info = ydl.extract_info(url, download=False)
            for entry in playlist_info['entries']:
                song = Song(entry['url'])
                self.addQueue(song)
        await self.Context.send(f"Loaded {len(playlist_info['entries'])} songs from the playlist.")

    def Queue(self):
        tmp= ""

        for song in self.queue:
            tmp += f"{song.title}\n"

        embed=discord.Embed(
            title="Queue 🎧",
            description=tmp
        )
        embed.set_thumbnail(url=self.current.thumbnail)
        embed.set_footer(text=f"Current: {self.current.title}")
        return embed

    def addQueue(self, song:Song):
        self.queue.append(song)
