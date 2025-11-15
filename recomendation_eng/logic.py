import json
import logging
from pika.adapters.blocking_connection import BlockingChannel
from pika.spec import Basic, BasicProperties

from bert_engine import recommender  # import the preloaded recommender

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING)


def user_cart(ch: BlockingChannel, method: Basic.Deliver, properties: BasicProperties, body: bytes):
    data = json.loads(body.decode())
    book_id = data.get("book_id")
    author = data.get("authors")
    title = data.get("original_title")
    logger.warning(f"User notified for book {book_id} by {author} - {title}")

    try:
        recs = recommender.recommend(book_id=book_id, top_k=5)
    
        detailed_recs = []
        for r in recs:
          book_info = recommender.books[recommender.books['book_id'] == r['book_id']].iloc[0]
          detailed_recs.append({
            "book_id": r['book_id'],
            "title": book_info['title'],
            "authors": book_info['authors'],
            "score": r['score']
           })
        logger.warning(f"Recommendations for book {book_id}: {detailed_recs}")

    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
