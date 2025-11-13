import asyncio
import logging

from broker import start_consuming

logger = logging.getLogger(__name__)


async def main() -> None:
    await start_consuming()


if __name__ == "__main__":
    logger.warning("Service 2 starting...")
    asyncio.run(main())
