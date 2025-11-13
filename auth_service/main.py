import logging

from broker import start_consuming

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.warning('Service 1 starting...')
    start_consuming()
