""""Send a random pyjoke back on:

- Direct messages that contains "joke" at begging
- Any mention in any channel.

"""

import logging
import os
import re

from dotenv import load_dotenv
import pyjokes
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN, name="Joke Bot")
logger = logging.getLogger(__name__)


@app.message(re.compile("^joke$"))
def show_random_joke(message, say):
    """Send a random pyjoke back"""
    channel_type = message["channel_type"]

    if channel_type != "im":
        logger.info(f"This don't works in different channels {channel_type}")
        # print(message)

    dm_channel = message["channel"]
    user_id = message["user"]

    joke = pyjokes.get_joke()
    logger.info(f"Sent joke < {joke} > to user {user_id}")

    say(text=joke, channel=dm_channel)


@app.event("app_mention")
def handle_app_mention_joke(body, logger, say):
    logger.info(body)
    # print(body)
    joke = pyjokes.get_joke()
    channel_id = body["event"]["channel"]
    say(text=joke, channel=channel_id)


def main():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()


if __name__ == "__main__":
    main()
