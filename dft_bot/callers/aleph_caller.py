from typing import *
import requests, os
# from urllib.parse import urlparse

import aiohttp

from dft_bot.callers.caller import BotType, Caller
from dft_bot.utils import ToolResponse

class AlephCaller(Caller):
    def __init__(self, input: dict, bot_data: dict, bot_type: BotType):
        super().__init__(input, bot_data, bot_type)
        self.api_key = os.environ.get("ALEPH_SECRET_API_KEY")
        assert self.api_key and len(self.api_key), f"invalid env variable for Aleph API key: ALEPH_SECRET_API_KEY={self.api_key}"
    
    async def call(self) -> ToolResponse:
        print("START ALEPH CALL")

        if email := self.input.get("email"): await self.call_email(email)
        # TODO: other entities, eg phone number, domain

        if self.result:
            await self.send_result()
        print("DONE ALEPH CALL")

    async def call_email(self, email:str) -> ToolResponse:
        self.result: ToolResponse = ToolResponse("Aleph:email", input=email)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://aleph.occrp.org/api/2/entities", params={
                "filter:emails": email,
                "filter:schemata": "Thing",
                "limit": 1,
                "q": "",
            }, headers={
                "Accept": "application/json, text/plain, */*",
                "Authorization": f"ApiKey {self.api_key}",     
            }) as r:
                if r.status != 200:
                    print(f"Error: ALEPH returned {r.status}")
                    return
                res_d = await r.json()

                if res_d.get("total") > 0:
                    self.result.text = f"There are {res_d.get('total')} entities on ALEPH!\n\nSee them at: https://aleph.occrp.org/search?filter:schemata=Thing&filter:emails={email}&q=\n\nFor a general search use:https://aleph.occrp.org/search?q={email}"

        return ToolResponse("Aleph:email", input=email)
    
