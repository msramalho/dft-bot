import boto3, os, traceback
# from PIL import Image

from dft_bot.callers.caller import BotType, Caller
from dft_bot.utils import ToolResponse

class AwsRekognitionCaller(Caller):
    name = "AwsRekognition"
    url = "https://docs.aws.amazon.com/rekognition/latest/APIReference/API_CompareFaces.html"
    
    def __init__(self, input: dict, bot_data: dict, bot_type: BotType):
        super().__init__(input, bot_data, bot_type)
        self.client = boto3.client(
            'rekognition',
            region_name=os.environ.get("AWS_REGION"),
            aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY")
        )
        
    
    async def call(self) -> ToolResponse:
        print("START AwsRekognition CALL")

        await self.similarity(self.input.get("img1_path"), self.input.get("img2_path"))
        
        await self.send_result()
        print("DONE AwsRekognition CALL")
    
    async def similarity(self, img1_path: str, img2_path: str, **kwargs) -> dict:
        # accepts similarity_threshold, from 0 to 100, defaults to 80
        # https://docs.aws.amazon.com/rekognition/latest/dg/faces-comparefaces.html
        i1 = open(img1_path, 'rb')
        i2 = open(img2_path, 'rb')
        similarity_threshold = kwargs.get('similarity_threshold', 80)
        self.result = ToolResponse(f"AwsRekognition", input="2 images")

        try:
            print(f'Calling AWS Detect faces for source={img1_path} and target={img2_path}')
            # SimilarityThreshold is 0 so that all the results are in FaceMatches, and then we use the threshold for comparing, otherwise we would not get the similarity values
            response = self.client.compare_faces(
                SimilarityThreshold=0,
                SourceImage={'Bytes': i1.read()},
                TargetImage={'Bytes': i2.read()}
            )
            assert len(response['FaceMatches']) == 1, "got multiple face pairs for single face passed"
        except Exception as e:
            print(f'Unable to call AWS Face comparison for {img1_path} and {img2_path} due to : {e}\n{traceback.format_exc()}')
            self.result.text = "AWS Rekognition error"
            return
        
        result = response['FaceMatches'][0]

        if result['Similarity'] >= similarity_threshold:
            self.result.text = f"The two faces belong to the same person!"
        else:
            self.result.text = f"The two faces do not belong to the same person."
        self.result.text += f"\n\n - similarity: {result['Similarity']:.3f}%\n - threshold: {similarity_threshold}%"