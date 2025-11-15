import logging

from broker import start_consuming

logger = logging.getLogger(__name__)


if __name__ == "__main__":
    logger.warning('Recomendation eng starting...')
    start_consuming()
