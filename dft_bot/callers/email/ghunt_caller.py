from typing import *

import tempfile, subprocess, json, traceback
from dft_bot.callers.caller import Caller
from dft_bot.constants import TMP_DIR
from dft_bot.utils import ToolResponse

class GHuntCaller(Caller):
    async def call(self) -> ToolResponse:
        print("START GHUNT CALL")
        email = self.input.get("email")
        self.result = await self.search_ghunt(email)
        await self.send_result()
        print("DONE GHUNT CALL")

    async def search_ghunt(self, email:str) -> ToolResponse:
        res: ToolResponse = ToolResponse("GHUNT", input=email)
        try:
            with tempfile.NamedTemporaryFile(
                "r+", dir=TMP_DIR, prefix="ghunt_", suffix=".json"
            ) as json_file:
                command = f"ghunt email --json {json_file.name} {email}"
                cli_output = subprocess.check_output(
                    command, shell=True, stderr=subprocess.STDOUT, text=True
                )
                cli_output = cli_output.split("\n[+] JSON output wrote")[0]
                res.write_text_to_file("html", cli_output)

                # fetch most relevant data points
                json_res = json.load(json_file)
                profile = json_res.get("PROFILE_CONTAINER") or {}
                gaia_id = (profile.get("profile") or {}).get("personId")
                profile_pic = (
                    ((profile.get("profile") or {}).get("profilePhotos") or {}).get(
                        "PROFILE"
                    )
                    or {}
                ).get("url")
                timezone = ((profile.get("calendar") or {}).get("details") or {}).get(
                    "time_zone"
                ) or {}
                data_points = []
                if gaia_id:
                    data_points.append(f"GAIA ID: <span>{gaia_id}</span>")
                if profile_pic:
                    data_points.append(f"Profile picture: {profile_pic}")
                if timezone:
                    data_points.append(f"timezone: {timezone}")
                res.text = "\n".join(data_points)
        except Exception as e:
            print(f"An error occurred: {str(e)}: {traceback.format_exc()}")
            res.error = "An error occurred"
        return res
