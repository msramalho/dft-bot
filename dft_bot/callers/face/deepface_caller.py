import os
from deepface import DeepFace

from dft_bot.callers.caller import BotType, Caller
from dft_bot.utils import ToolResponse

class DeepfaceCaller(Caller):
    name = "Deepface"
    url = "https://github.com/serengil/deepface"
    
    def __init__(self, input: dict, bot_data: dict, bot_type: BotType):
        super().__init__(input, bot_data, bot_type)
        self.api_key = os.environ.get("ALEPH_SECRET_API_KEY")
        assert self.api_key and len(self.api_key), f"invalid env variable for Aleph API key: ALEPH_SECRET_API_KEY={self.api_key}"
        
    
    async def call(self) -> ToolResponse:
        print("START ALEPH CALL")

        self.result = ToolResponse(f"Deepface:verify", input="2 images")
        img1_path = self.input.get("img1_path")
        img2_path = self.input.get("img2_path")

        try:
            result = DeepFace.verify(
                img1_path = img1_path, img2_path = img2_path,
                model_name = 'VGG-Face',
                detector_backend="retinaface"
            )
        except Exception as e:
            print(e)
            self.result.text = f"An error occurred."
            return

        if result["verified"]:
            self.result.text = f"The two faces belong to the same person!"
        else:
            self.result.text = f"The two faces do not belong to the same person."
        self.result.text += f"\n(cosine distance:{round(result['distance'], 2)}>{result['threshold']}, using model={result['model']} and detector={result['detector_backend']})"

        await self.send_result()

        print("DONE ALEPH CALL")
