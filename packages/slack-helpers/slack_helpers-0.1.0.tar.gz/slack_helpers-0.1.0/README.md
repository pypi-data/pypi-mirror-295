# slack-helpers

[![image](https://img.shields.io/pypi/v/slack-helpers.svg)](https://pypi.python.org/pypi/slack-helpers)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/slack-helpers)](https://pypistats.org/packages/slack-helpers)
[![image](https://img.shields.io/pypi/l/slack-helpers.svg)](https://pypi.python.org/pypi/slack-helpers)
[![image](https://img.shields.io/pypi/pyversions/slack-helpers.svg)](https://pypi.python.org/pypi/slack-helpers)

|  |  |
|--|--|
|[![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) |[![Actions status](https://github.com/deargen/slack-helpers/workflows/Style%20checking/badge.svg)](https://github.com/deargen/slack-helpers/actions)|
| [![Ruff](https://img.shields.io/badge/Ruff-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/ruff) | [![Actions status](https://github.com/deargen/slack-helpers/workflows/Linting/badge.svg)](https://github.com/deargen/slack-helpers/actions) |
| [![pytest](https://img.shields.io/badge/pytest-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/pytest-dev/pytest) [![doctest](https://img.shields.io/badge/doctest-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://docs.python.org/3/library/doctest.html) | [![Actions status](https://github.com/deargen/slack-helpers/workflows/Tests/badge.svg)](https://github.com/deargen/slack-helpers/actions) |
| [![uv](https://img.shields.io/badge/uv-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)](https://github.com/astral-sh/uv) | [![Actions status](https://github.com/deargen/slack-helpers/workflows/Check%20pip%20compile%20sync/badge.svg)](https://github.com/deargen/slack-helpers/actions) |
|[![Built with Material for MkDocs](https://img.shields.io/badge/Material_for_MkDocs-526CFE?style=for-the-badge&logo=MaterialForMkDocs&logoColor=white)](https://squidfunk.github.io/mkdocs-material/)|[![Actions status](https://github.com/deargen/slack-helpers/workflows/Deploy%20MkDocs%20on%20latest%20commit/badge.svg)](https://github.com/deargen/slack-helpers/actions)|


An easy wrapper to send objects to Slack.

📦 Main Features:

- Send text
- Send images (pillow)
- Send plots (matplotlib)
- Send tracebacks (rich tracebacks with syntax highlighting, in svg, png, or html)
- Set up with environment variables, so no need for more configuration. Just import and use.
- Ensure preview mode (append `""""dear-viewer""""` prefix to the text so it won't be considered as a binary)
- Instantly preview with `dear-chrome-viewer` (a Chrome extension to preview html, PDB, and other files)
  - Normally, the Slack preview just views the file in plain text so the extension just makes it easier to view the file in the browser.
- Does **NOT** error out if the Slack token is not set. It just logs a warning and does not send the message.
  - You don't need to add a conditional check for the token. Just import and use.

😢 Caveats:

- External dependencies have to be installed (The cairo library and fira code font)
  - The `scripts/install_binaries.sh` script installs the dependencies.


## 🛠️ Installation

We recommend using Conda because it's easier to install Cairo. If you don't want to use Conda, you can install Cairo using apt-get or brew.

```bash
conda create -n slack-helpers python=3.12
conda activate slack-helpers
pip install slack-helpers
bash scripts/install_binaries.sh  # install Fira Code font ~/.local/share/fonts, and Cairo using Conda
```

Set environment variables for the slack token and channel.

```bash
export SLACK_BOT_TOKEN=xoxb-xxxx
export SLACK_APP_TOKEN=xapp-xxxx
export SLACK_CHANNEL_ID=CXXXXXXXX
```

or use a `.env` file with `python-dotenv`.

```bash
# .env
SLACK_BOT_TOKEN=xoxb-xxxx
SLACK_APP_TOKEN=xapp-xxxx
SLACK_CHANNEL_ID=CXXXXXXXX
```

```python
import dotenv
dotenv.load_dotenv()
```

Check health of the installation. The below output shows that the Slack tokens are not set, and the Fira Code font is installed.

```console
$ slack-helpers health
09/07 21:37:12 ERROR    slack_helpers.health.slack - 😡 Please set the environment variable SLACK_BOT_TOKEN.                                                slack.py:14
               ERROR    slack_helpers.health.slack - 😡 Please set the environment variable SLACK_APP_TOKEN.                                                slack.py:14
               ERROR    slack_helpers.health.slack - 😡 Please set the environment variable SLACK_CHANNEL_ID.                                               slack.py:14
               INFO     slack_helpers.health.slack - 🚀 Sending a test message to the Slack channel...                                                      slack.py:45
               WARNING  slack_helpers.send_only - You tried to send messages on Slack, but the token is not set. All messages will be ignored.          send_only.py:21
               ERROR    slack_helpers.health.slack - 😡 The response is None.                                                                               slack.py:49
               INFO     slack_helpers.health.font - ✅ FiraCode font is installed.                                                                           font.py:35
```

## 🚀 Usage

See `tools/examples/` for complete set of examples.

### Send-only example

```python
from dotenv import load_dotenv

load_dotenv()

from slack_helpers.send_only import (
    send_divider,
    send_file,
    send_matplotlib_fig,
    send_pil_image,
    send_text,
)

if __name__ == "__main__":
    send_text("Hello, World!")
    send_divider()
    send_file(
        filename="1A0G.pdb",
        file="/path/to/1A0G.pdb",
        title="My Test PDB File",
        initial_comment="Here's a PDB file for you!",
    )
    send_matplotlib_fig(
        filename="matplotlib_fig.pdf",
        fig=fig,
        title="My Test Matplotlib Figure",
        initial_comment="Here's a matplotlib figure for you!",
    )
    send_pil_image(
        filename="pil_image.png",
        image=pil_image,
        title="My Test PIL Image",
        initial_comment="Here's a PIL image for you!",
    )
```

### Traceback example

```python
from dotenv import load_dotenv

load_dotenv()

from rich.traceback import Traceback

from slack_helpers.send_only import send_svg_as_pdf
from slack_helpers.utils.rich import (
    CONSOLE_WIDTH,
    rich_traceback_to_svg,
)


if __name__ == "__main__":
    try:
        raise Exception("This is an exception")
    except Exception:
        slack_text = "Exception occurred"

        tb = Traceback(show_locals=True, width=CONSOLE_WIDTH)
        tb_svg = rich_traceback_to_svg(
            tb, title=f"Exception occurred from host {socket.gethostname()}"
        )
        send_svg_as_pdf(
            filename="traceback.pdf",
            svg_file=tb_svg,
            title="traceback.pdf",
        )
```


### Interactive example

```python
from dotenv import load_dotenv

load_dotenv()

from slack_helpers import app
from slack_helpers.interactive import handler

assert app is not None, "Set environment variables SLACK_* first."


@app.message("hello")
def hello_message(body: dict[str, Any], say):
    print("Received a hello command")
    print(f"body: {pformat(body)}")
    say(text=f"Hi <@{body['event']['user']}>!")


handler.start()
```

