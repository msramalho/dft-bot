import whisper

from dft_bot.callers.caller import BotType, Caller
from dft_bot.constants import TMP_DIR
from dft_bot.utils import ToolResponse

class WhisperCaller(Caller):
    name = "OpenAiWhisper"
    url = "https://github.com/openai/whisper"

    def __init__(self, input: dict, bot_data: dict, bot_type: BotType):
        super().__init__(input, bot_data, bot_type)
        self.model = whisper.load_model("tiny")


    async def call(self) -> ToolResponse:
        print("START Whisper CALL")

        video = self.input.get("video")
        self.result = ToolResponse(f"Whisper", input='video')

        result = self.model.transcribe(video)
        self.result.text = result["text"]

        await self.send_result()

        print("DONE YtDlp CALL")
