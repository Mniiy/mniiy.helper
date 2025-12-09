import yt_dlp, discord, datetime

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
        self.looped: bool= False
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
