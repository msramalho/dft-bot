
import os
from pathlib import Path
import shutil
import yt_dlp
from dft_bot.callers.caller import Caller
from dft_bot.constants import TMP_DIR
from dft_bot.utils import ToolResponse

class YtDlpCaller(Caller):
    name = "YtDlp"
    url = "https://github.com/yt-dlp/yt-dlp"
    
    async def call(self) -> ToolResponse:
        print("START YtDlp CALL")

        url = self.input.get("url")
        self.result = ToolResponse(f"YtDlp", input=url)

        try:
            ydl = yt_dlp.YoutubeDL({'outtmpl': os.path.join(TMP_DIR, f'%(id)s.%(ext)s'), 'quiet': False, 'noplaylist': True})
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            _, ext = os.path.splitext(filename)
            self.result.filename = self.result.get_filename(ext)
            filename = os.path.abspath(filename)
            shutil.copy(filename, self.result.filename)
            self.result.text = f"downloaded video successfully!"
            os.remove(filename)
        except Exception as e:
            print(e)
            self.result.text = f"An error occurred."


        await self.send_result()

        print("DONE YtDlp CALL")
