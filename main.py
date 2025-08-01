import asyncio
import logging

from create_bot import init_bot

async def main():
    await init_bot()


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        # stream=sys.stdout,
    )

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Stop NSA Worker Bot (Ctrl+C)')
