import os
import pathlib
from telethon import TelegramClient

from dataclasses import dataclass, field
import time, uuid
from slugify import slugify
from telethon.tl.types import DocumentAttributeFilename

from dft_bot.constants import TMP_DIR

@dataclass
class ToolResponse:
    """Class containing tool responses."""

    tool: str
    text: str = ""
    input: str = ""  # user input field, eg: email, phone, ...
    filename: str = None
    # error: str = None
    start_time: float = field(default_factory=time.time)

    async def send_telegram(self, client: TelegramClient, sender_id: str):
        self.text = f"<b>{self.tool}</b>: <code>{self.input}</code>\n\n{self.text}\n\n[ {self.tool.lower()} took {self.get_total_time_seconds()} seconds]"
        await self.send_telegram_split_if_needed(client, sender_id, 1)

        if self.filename:
            _, file_extension = os.path.splitext(self.filename)
            await client.send_file(
                sender_id,
                self.filename,
                attributes=[
                    DocumentAttributeFilename(
                        file_name=f"{slugify(self.tool + '-' + self.input)}{file_extension or '.txt'}"
                    )
                ],
            )
            # delete file
            pathlib.Path(self.filename).unlink(missing_ok=True)

    def get_filename(self, extension:str="html"):
        return os.path.join(TMP_DIR, f"{slugify(self.tool + '-' + self.input)}-{generate_uuid()[0:8]}.{extension}")

    def write_text_to_file(self, extension:str="html", text:str=None):
        # writes either self.text or provided text to a file
        text_to_write = text or self.text
        self.filename = self.get_filename(extension)
        with open(self.filename, "w") as f:
            f.write(text_to_write)
    
    def get_total_time_seconds(self):
        return round(time.time() - self.start_time, 2)

    async def send_telegram_split_if_needed(
        self, client: TelegramClient, sender_id: str, part: int = 1
    ):
        # recursive function that splits long telegram messages
        MAX_LENGTH = 4096
        if len(self.text) <= MAX_LENGTH:
            message_to_send = self.text
            if part > 1:
                message_to_send = f"(part {part}/x)\n" + self.text[0:cut_at] + "..."
            await client.send_message(sender_id, message_to_send, parse_mode="HTML")
        else:
            cut_at = MAX_LENGTH - 50
            message_to_send = f"(part {part}/x)\n" + self.text[0:cut_at] + "..."
            await client.send_message(sender_id, message_to_send, parse_mode="HTML")
            await self.send_telegram_split_if_needed(
                client, sender_id, self.text[cut_at:], part + 1
            )


def generate_uuid():
    return str(uuid.uuid4())
