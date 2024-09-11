from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent.resolve()))
import admin_bot.core.tg
import asyncio


async def async_main():
    await admin_bot.core.tg.init()
    await admin_bot.core.tg.set_handlers()


def main():
    asyncio.run(async_main())


if __name__ == '__main__':
    main()

