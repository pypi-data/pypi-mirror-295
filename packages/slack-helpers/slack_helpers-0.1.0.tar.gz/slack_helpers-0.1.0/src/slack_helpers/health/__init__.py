"""Check health of the installation."""

import logging

from .font import verify_fonts_bool
from .slack import check_env as slack_check_env
from .slack import check_send_text as slack_check_send_text

logger = logging.getLogger(__name__)


def main():
    successes = [slack_check_env()]
    successes.append(slack_check_send_text())
    successes.append(verify_fonts_bool())

    if all(successes):
        logger.info("")
        logger.info("💪 You are ready to go!")


if __name__ == "__main__":
    main()
