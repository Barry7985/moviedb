import os
import requests
from decouple import config
from functools import lru_cache  # Pour implémenter un cache en mémoire
import logging
logger = logging.getLogger(__name__)


class TMDBServices:
    BASE_URL = "https://api.themoviedb.org/3"
    API_KEY = config('TMDB_API_KEY')

    if API_KEY is None:
        raise ValueError("La clé API (TMDB_API_KEY) est manquante. Vérifiez votre fichier .env.")

    @classmethod
    @lru_cache(maxsize=100)
    def search_movie(cls,query):
        """Recherche des films via l'API TMDB."""
        if not query:
            return {"error": "La requête de recherche est vide."}

        try:
            response = requests.get(
                f"{cls.BASE_URL}/search/movie",
                params={
                    'api_key': cls.API_KEY,
                    'query': query,
                    'language': 'fr-FR'
                }
            )
            response.raise_for_status()  
            data = response.json()
            logger.debug(f"Réponse TMDB : {data}")  
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Erreur lors de la recherche TMDB : {e}")
            return {"error": str(e)}
        
    @classmethod
    @lru_cache(maxsize=100)  # Cache également pour limiter les requêtes
    def get_movie_details(cls, tmdb_id):
        """Récupère les détails d'un film via son ID TMDB."""
        if not tmdb_id:
            return {"error": "L'identifiant du film est manquant."}

        try:
            response = requests.get(
                f"{cls.BASE_URL}/movie/{tmdb_id}",
                params={
                    'api_key': cls.API_KEY,
                    'language': 'fr-FR'
                }
            )
            response.raise_for_status()  # Lève une exception si le statut HTTP est une erreur
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": f"Une erreur est survenue lors de la récupération des détails : {str(e)}"}