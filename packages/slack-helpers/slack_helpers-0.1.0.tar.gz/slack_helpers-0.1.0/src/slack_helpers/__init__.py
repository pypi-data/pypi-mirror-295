import os

from slack_bolt import App

from . import _version

__version__ = _version.get_versions()["version"]


bot_token = os.environ.get("SLACK_BOT_TOKEN", None)

if bot_token is not None:
    app = App(token=bot_token)
    client = app.client
    channel_id = os.environ["SLACK_CHANNEL_ID"]
else:
    app = None
    client = None
    channel_id = None
