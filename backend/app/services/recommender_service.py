# app/services/recommender_service.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderService:

    @staticmethod
    def recomendar(consulta: str, documentos: list[str]):
        vect = TfidfVectorizer()
        tfidf = vect.fit_transform([consulta] + documentos)
        sims = cosine_similarity(tfidf[0:1], tfidf[1:]).flatten()
        return sims.tolist()
