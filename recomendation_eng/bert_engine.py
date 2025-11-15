# bert_engine.py
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

# --------------------------
# Recommendation Engine
# --------------------------
class BookRecommender:
    def __init__(self, books_path="resource/books.csv", model_name="all-MiniLM-L6-v2"):
        logger.warning("Loading SentenceTransformer model...")
        self.model = SentenceTransformer(model_name)

        logger.warning("Loading books CSV...")
        self.books = pd.read_csv(books_path)
        self.books['text'] = (
            self.books['title'].fillna("") + " " +
            self.books['authors'].fillna("") + " " +
            self.books['original_title'].fillna("")
        )

        logger.warning("Generating embeddings for all books...")
        self.embeddings = self.model.encode(self.books['text'].tolist(), convert_to_tensor=False)
        self.embeddings = np.array(self.embeddings)
        logger.warning("Embeddings ready!")

    def recommend(self, book_id, top_k=10):
        idx = self.books.index[self.books['book_id'] == int(book_id)][0]
        query_emb = self.embeddings[idx].reshape(1, -1)
        scores = cosine_similarity(query_emb, self.embeddings)[0]
        top_indices = np.argsort(scores)[::-1]

        recs = []
        for i in top_indices:
            if int(self.books.iloc[i]['book_id']) == int(book_id):
                continue
            recs.append({
                "book_id": int(self.books.iloc[i]['book_id']),
                "score": float(scores[i])
            })
            if len(recs) >= top_k:
                break
        return recs


# --------------------------
# Preload recommender for your logic.py / broker.py
# --------------------------
BOOKS_PATH = "resource/books.csv"
MODEL_NAME = "all-MiniLM-L6-v2"
recommender = BookRecommender(BOOKS_PATH, MODEL_NAME)
