import os
import json
import asyncio

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import FloodWaitError

# =========================
# Railway Variables
# =========================

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION = os.getenv("SESSION")

# =========================
# Groups
# =========================

GROUPS = [
    "Trusted_Buy_Sell_BD",
    "rs_buy_sell_grp",
    "JS_buy_sell",
    "pagebuysel",
    "tradebanglazone4",
    "buysellbyAliBhai",
    "bdfbbuysell",
]

# =========================
# Captions
# =========================

CAPTIONS = [
    "পেজটি বিক্রয় করা হবে। আগ্রহীরা ইনবক্স করুন, দাম খুবই কম।",
    "কম দামে ভালো একটি পেজ বিক্রি করা হবে। বিস্তারিত ইনবক্সে।",
    "জরুরি ভিত্তিতে পেজ সেল। আগ্রহীরা দ্রুত ইনবক্স করুন।",
    "পেজ কিনতে চাইলে ইনবক্স করুন। বাজেট-ফ্রেন্ডলি প্রাইস।",
]

# =========================
# Photos
# =========================

PHOTOS = [
    "photos/photo1.jpg",
    "photos/photo2.jpg",
    "photos/photo3.jpg",
]

# =========================
# Delay
# =========================

POST_DELAY = 20 * 60

STATE_FILE = "state.json"

client = TelegramClient(
    StringSession(SESSION),
    API_ID,
    API_HASH
)

# =========================
# Load State
# =========================

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            pass

    return {
        "group_index": 0,
        "photo_index": 0
    }

# =========================
# Save State
# =========================

def save_state(group_index, photo_index):
    with open(STATE_FILE, "w") as f:
        json.dump(
            {
                "group_index": group_index,
                "photo_index": photo_index
            },
            f
        )

# =========================
# Scheduler
# =========================

async def scheduler():

    state = load_state()

    group_index = state["group_index"]
    photo_index = state["photo_index"]

    while True:

        group = GROUPS[group_index]

        caption = CAPTIONS[
            group_index % len(CAPTIONS)
        ]

        photo = PHOTOS[
            photo_index % len(PHOTOS)
        ]

        try:

            if not os.path.exists(photo):
                print(f"Photo not found: {photo}")

            else:

                await client.send_file(
                    group,
                    photo,
                    caption=caption
                )

                print(
                    f"SUCCESS | {group} | {photo}"
                )

        except FloodWaitError as e:

            print(
                f"FloodWait {e.seconds}s"
            )

            await asyncio.sleep(
                e.seconds
            )

        except Exception as e:

            print(
                f"FAILED | {group}"
            )

            print(e)

        group_index = (
            group_index + 1
        ) % len(GROUPS)

        photo_index = (
            photo_index + 1
        ) % len(PHOTOS)

        save_state(
            group_index,
            photo_index
        )

        await asyncio.sleep(
            POST_DELAY
        )

# =========================
# Main
# =========================

async def main():

    me = await client.get_me()

    print(
        f"Logged in as: {me.first_name}"
    )

    await scheduler()

with client:
    client.loop.run_until_complete(
        main()
    )
