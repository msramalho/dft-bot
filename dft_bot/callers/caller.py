import asyncio
from dft_bot.utils import ToolResponse
from enum import Enum

class BotType(Enum):
    telethon = "telethon"
    discord = "discord"
    slack = "slack"

class Caller:
    def __init__(self, input: dict, bot_data:dict, bot_type: BotType):
        self.input = input
        self.bot_data = bot_data
        self.bot_type = bot_type
        self.result: ToolResponse = None

    async def call(self) -> ToolResponse:
        # Call the number
        pass

    async def send_result(self):
        if self.bot_type == BotType.telethon:
            return await self.telegram_result()
        elif self.bot_type == BotType.discord:
            return await self.discord_result()
        elif self.bot_type == BotType.slack:
            return await self.slack_result()
        assert False, "Not implemented"

    async def telegram_result(self):
        if not self.result: return
        await self.result.send_telegram(self.bot_data.get("client"), self.bot_data.get("sender_id"))

    async def discord_result(self):
        pass

    async def slack_result(self):
        pass
