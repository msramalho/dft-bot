# NOTE THIS ONLY WORKS pending this: https://github.com/obsidianforensics/unfurl/issues/187

# from typing import *

# from dft_bot.callers.caller import Caller
# from dft_bot.utils import ToolResponse
# from unfurl.core import Unfurl

# class UnfurlCaller(Caller):
#     async def call(self) -> ToolResponse:
#         print("START Unfurl CALL")

#         url = self.input.get("url")
#         self.result: ToolResponse = ToolResponse("Unfurl", input=url)
#         unfurl = Unfurl(remote_lookups=False)
#         unfurl.add_to_queue(data_type='url', key=None, value=url)
#         unfurl.parse_queue()
#         self.result.text = unfurl.generate_text_tree(detailed=False) + f"\n\nshare: https://dfir.blog/unfurl/?url={url}"
#         print(self.result.text)
#         self.result.write_text_to_file("txt")
#         await self.send_result()
#         print("DONE Unfurl CALL")