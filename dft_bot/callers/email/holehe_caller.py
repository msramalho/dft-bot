from typing import List
import trio, httpx
from holehe.core import (
    import_submodules,
    get_functions,
    TrioProgress,
    launch_module,
)
from dft_bot.callers.caller import BotType, Caller
from dft_bot.utils import ToolResponse

class HoleheCaller(Caller):
    name = "Holehe"
    url = "https://github.com/megadose/holehe"

    async def call(self) -> ToolResponse:
        print("START HOLEHE CALL")
        email = self.input.get("email")
        self.result = await self.search_holehe(email)
        await self.send_result()
        print("DONE HOLEHE CALL")


    async def search_holehe(self, email):
        res: ToolResponse = ToolResponse("HOLEHE", input=email)

        # fetch all available methods and respective callables
        modules = import_submodules("holehe.modules")
        websites = get_functions(modules)
        # call methods
        data = trio.run(call_all_modules, *[email, websites])
        # build string response
        res.text = result_to_string(data, websites)
        return res


async def call_all_modules(email: str, websites) -> List:
    # parallel invocation and retrieval of results
    out = []
    async_client = httpx.AsyncClient(timeout=10)
    instrument = TrioProgress(len(websites))
    trio.lowlevel.add_instrument(instrument)
    async with trio.open_nursery() as nursery:
        for website in websites:
            nursery.start_soon(launch_module, website, email, async_client, out)
    trio.lowlevel.remove_instrument(instrument)
    # sort by modules names
    out = sorted(out, key=lambda i: i["name"])
    # Close the client
    await async_client.aclose()
    return out


def result_to_string(data: List[dict], websites: List) -> str:
    description = ""

    counter = {"exists": 0, "rateLimit": 0, "not found": 0}
    description_entries = []
    for results in data:
        entry = ""
        if results["rateLimit"]:
            counter["rateLimit"] += 1
            # entry += "[x] " + results["domain"]
        elif results["exists"] == False:
            counter["not found"] += 1
            # entry += "[-] " + results["domain"]
        elif results["exists"] == True:
            counter["exists"] += 1
            websiteprint = ""
            if results["emailrecovery"] is not None:
                websiteprint += " " + results["emailrecovery"]
            if results["phoneNumber"] is not None:
                websiteprint += " / " + results["phoneNumber"]
            if results["others"] is not None and "FullName" in str(
                results["others"].keys()
            ):
                websiteprint += " / FullName " + results["others"]["FullName"]
            if results["others"] is not None and "Date, time of the creation" in str(
                results["others"].keys()
            ):
                websiteprint += (
                    " / Date, time of the creation "
                    + results["others"]["Date, time of the creation"]
                )
            entry = "[+] " + results["domain"] + websiteprint
        if len(entry):
            description_entries.append(entry)
    description += "\n".join(description_entries)
    description += f"\n\n{str(len(websites))} websites checked"
    description += "\n".join([f" -> {k}: {v}" for k, v in counter.items()])
    return description
