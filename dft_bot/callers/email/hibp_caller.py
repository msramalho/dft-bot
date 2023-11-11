import json
from typing import *

import aiohttp, os

from dft_bot.callers.caller import BotType, Caller
from dft_bot.constants import TMP_DIR
from dft_bot.utils import ToolResponse

class HIBPCaller(Caller):
    name = "HaveIBeenPwned"
    url = "https://haveibeenpwned.com/"

    def __init__(self, input: dict, bot_data: dict, bot_type: BotType):
        super().__init__(input, bot_data, bot_type)
        self.api_key = os.environ.get("HIBP_API_KEY")
        assert self.api_key and len(self.api_key), "invalid env variable for HaveIBeenPwned set HIBP_API_KEY=YOUR_KEY"

    async def call(self) -> ToolResponse:
        print("START HIBP CALL")
        email = self.input.get("email")
        await self.call_api(email)
        await self.send_result()
        print("DONE HIBP CALL")

    async def call_api(self, email:str) -> ToolResponse:
        self.result: ToolResponse = ToolResponse(f"HaveIBeenPwned", input=email)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://haveibeenpwned.com/api/v3/breachedaccount/{email}?truncateResponse=false", headers={
                "hibp-api-key": f"{self.api_key}",     
            }) as r:
                if r.status != 200:
                    self.result.text = f"Error: HIBP returned {r.status}"
                    print(self.result.text)
                    return
                res_d = await r.json()
                if len(res_d):
                    self.result.text = f"{len(res_d)} breaches found for:\n\n" + "\n".join([f" - {b.get('Name')} ({b.get('Domain')}) breached at {b.get('BreachDate', 'NA')}" for b in res_d])
                    self.result.write_text_to_file("json", json.dumps(res_d, indent=2))
                else:
                    self.result.text = f"No breaches found."
    

