import os, secrets, pyotp
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.environ.get("API_KEY", False)
TOTP = os.environ.get("TOTP", False)

assert API_KEY and len(API_KEY) >= 10, "WARNING: Environment variable API_KEY not set (mandatory) or had less than 10 chars."
assert TOTP, "WARNING: Environment variable TOTP not set (use 'off' to disable)"


def valid_login(api_token_to_check: str, totp_to_check: str) -> bool:
    # TOTP is required unless disabled
    if (not totp_to_check or not len(totp_to_check)) and TOTP != "off":
        print("TOTP not provided, but is required")
        return False
    # check for correct API_KEY
    if not secrets.compare_digest(
        api_token_to_check.encode("utf8"), API_KEY.encode("utf8")
    ):
        print("WRONG API_KEY")
        return False
    # if enabled check for TOTP
    if TOTP != "off":
        totp = pyotp.TOTP(TOTP)
        print(f"checking {totp_to_check=} against {totp.now()}")
        return totp.verify(totp_to_check.strip())
    return True

# # TODO: implement TOTOP setup and then retrieve form sqlite and verify against TOTP
# def telegram_totp_auth(client, sender_id):
#     # decorator @telegram_totp_auth(client, sender_id) will only allow func to execute if TOTP is 'off' or is valid
#     def inner_decorator(func):
#         async def wrapped(*args, **kwargs):
#             print(f"CALLED {TOTP=}")
#             if TOTP == "off":
#                 return await func(*args, **kwargs)
#             elif pyotp.TOTP(TOTP).verify("123456"):
#                 return await func(*args, **kwargs)
#             else:
#                 await client.send_message(sender_id, "INVALID TOTP", parse_mode="HTML")

#         return wrapped

#     return inner_decorator