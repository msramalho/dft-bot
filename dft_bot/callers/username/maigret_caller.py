import os
import shutil
from typing import *

import tempfile, subprocess, json, traceback
from dft_bot.callers.caller import BotType, Caller
from dft_bot.constants import TMP_DIR
from dft_bot.utils import ToolResponse

class MaigretCaller(Caller):
    name = "Maigret"
    url = "https://github.com/soxoj/maigret"

    async def call(self) -> ToolResponse:
        print("START Maigret CALL")
        username = self.input.get("username")
        await self.call_maigret(username)
        await self.send_result()
        print("DONE input CALL")

    async def call_maigret(self, username:str) -> ToolResponse:

        self.result: ToolResponse = ToolResponse("input", input=username)
        try:
            with tempfile.TemporaryDirectory(dir=TMP_DIR, suffix="maigret") as report_dir:
                # TODO: add --all-sites and remove --no-recursion and --top-sites
                command = f"maigret {username} --pdf --folderoutput {report_dir} --no-recursion --top-sites 100" 
                cli_output = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT, text=True
                )
                print(cli_output)
                self.result.text = cli_output.split("[*] Short text report:")[1]
                self.result.filename = self.result.get_filename("pdf")
                shutil.copy(os.path.join(report_dir, os.listdir(report_dir)[0]), self.result.filename)

        except Exception as e:
            print(f"An error occurred: {str(e)}: {traceback.format_exc()}")
            self.result.text = "An error occurred"
