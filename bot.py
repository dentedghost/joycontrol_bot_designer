import argparse
import asyncio
import command
import logging
import os

from joycontrol import logging_default as log

logger = logging.getLogger(__name__)


async def _main(args):

    cli = command.CCLI()

    try:
        await cli.run()
    finally:
        logger.info('Stopping communication...')

if __name__ == '__main__':
    # check if root
    if not os.geteuid() == 0:
        raise PermissionError('Script must be run as root!')

    # setup logging
    log.configure()

    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--log')
    args = parser.parse_args()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(
        _main(args)
    )
   

