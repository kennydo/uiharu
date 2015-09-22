from __future__ import print_function

import argparse
import logging.config
import sys

from uiharu.config import ConfigAction
from uiharu import create_app


_logging_config = dict(
    version=1,
    disable_existing_loggers=False,
    formatters={
        'verbose': {
            'format': '%(asctime)s [%(levelname)s] %(message)s'
        },
    },
    handlers={
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'null': {
            'class': 'logging.NullHandler',
        }
    },
    loggers={
        '': {
            'handlers': ['console'],
            'level': logging.INFO,
        },
        'temperusb': {
            'level': logging.WARN,
        },
    },
)
logging.config.dictConfig(_logging_config)
log = logging.getLogger(__name__)


def parse_cli_args():
    """Parse the CLI arguments and return the populated namespace."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--config',
        action=ConfigAction,
        help="The location of the JSON config file",
    )
    return parser.parse_args()


def main():
    args = parse_cli_args()

    if not args.config:
        print("Error: A config path must be specified", file=sys.stderr)
        sys.exit(1)

    app = create_app(args.config)
    app.run(host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
