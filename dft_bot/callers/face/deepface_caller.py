import os
from deepface import DeepFace

from dft_bot.callers.caller import BotType, Caller
from dft_bot.utils import ToolResponse

class DeepfaceCaller(Caller):
    name = "Deepface"
    url = "https://github.com/serengil/deepface"
    
    async def call(self) -> ToolResponse:
        print("START Deepface CALL")

        self.result = ToolResponse(f"Deepface:verify", input="2 images")
        img1_path = self.input.get("img1_path")
        img2_path = self.input.get("img2_path")

        try:
            result = DeepFace.verify(
                img1_path = img1_path, img2_path = img2_path,
                model_name = 'VGG-Face',
                detector_backend="retinaface",
                distance_metric="euclidean_l2",
            )
        except Exception as e:
            print(e)
            self.result.text = f"An error occurred."
            return

        if result["verified"]:
            self.result.text = f"The two faces belong to the same person!"
        else:
            self.result.text = f"The two faces DO NOT belong to the same person."
        result["distance"] = round(result['distance'], 2)
        self.result.text += "\n\n" + "\n ".join([f" - {k}: {v}" for k,v in result.items() if k in ["distance", "threshold", "model", "detector_backend"]])

        await self.send_result()

        print("DONE Deepface CALL")
