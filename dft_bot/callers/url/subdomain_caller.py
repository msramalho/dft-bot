# # NOTE: this is highly rate-limited 5 requests per minute, see https://www.subdomain.center/
# from typing import *
# from urllib.parse import urlparse

# import aiohttp

# from dft_bot.callers.caller import Caller
# from dft_bot.utils import ToolResponse

# class SubdomainCaller(Caller):
#     async def call(self) -> ToolResponse:
#         print("START Subdomain CALL")

#         url = self.input.get("url")
#         # get domain from url
#         domain = urlparse(url).netloc
#         self.result: ToolResponse = ToolResponse("Subdomain", input=domain)

#         async with aiohttp.ClientSession() as session:
#             async with session.get(f"http://api.subdomain.center/?domain={domain}") as resp:
#                 if resp.status != 200:
#                     print(f"Error: api.subdomain.center returned {resp.status}")
#                     return
#                 self.result.text = "\n".join(await resp.json())
#                 print(self.result.text)

#         await self.send_result()
#         print("DONE Subdomain CALL")