import os
import requests
from decouple import config, Config, RepositoryIni
from functools import lru_cache  # Pour implémenter un cache en mémoire
import logging
logger = logging.getLogger(__name__)

# Initialize config with settings.ini
config = Config(RepositoryIni('settings.ini'))

class TMDBServices:
    BASE_URL = "https://api.themoviedb.org/3"
    IMAGE_BASE_URL = "https://image.tmdb.org/t/p"
    API_KEY = config('TMDB_API_KEY')

    if not API_KEY:
        raise ValueError("La clé API (TMDB_API_KEY) est manquante dans settings.ini.")

    @classmethod
    def get_image_url(cls, path, size='w500'):
        """Get the full URL for a TMDB image."""
        if not path:
            return None
        return f"{cls.IMAGE_BASE_URL}/{size}{path}"

    @classmethod
    @lru_cache(maxsize=100)
    def search_movie(cls, query, page=1, language='fr-FR', include_adult=False):
        """Search movies via TMDB API."""
        if not query:
            return {"error": "La requête de recherche est vide."}

        try:
            response = requests.get(
                f"{cls.BASE_URL}/search/movie",
                params={
                    'api_key': cls.API_KEY,
                    'query': query,
                    'language': language,
                    'page': page,
                    'include_adult': include_adult
                }
            )
            response.raise_for_status()  
            data = response.json()
            
            # Process image URLs in results
            if 'results' in data:
                for movie in data['results']:
                    if movie.get('poster_path'):
                        movie['poster_url'] = cls.get_image_url(movie['poster_path'])
                    if movie.get('backdrop_path'):
                        movie['backdrop_url'] = cls.get_image_url(movie['backdrop_path'], 'original')
            
            logger.debug(f"TMDB Search Response: {data}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB Search Error: {e}")
            return {"error": str(e)}
        
    @classmethod
    @lru_cache(maxsize=100)
    def get_movie_details(cls, tmdb_id, language='fr-FR', append_to_response=None):
        """Get movie details via TMDB API."""
        if not tmdb_id:
            return {"error": "L'identifiant du film est manquant."}

        try:
            params = {
                'api_key': cls.API_KEY,
                'language': language
            }
            if append_to_response:
                params['append_to_response'] = append_to_response

            response = requests.get(
                f"{cls.BASE_URL}/movie/{tmdb_id}",
                params=params
            )
            response.raise_for_status()
            data = response.json()
            
            # Process image URLs
            if data.get('poster_path'):
                data['poster_url'] = cls.get_image_url(data['poster_path'])
            if data.get('backdrop_path'):
                data['backdrop_url'] = cls.get_image_url(data['backdrop_path'], 'original')
            
            # Process images from append_to_response
            if 'images' in data:
                if 'posters' in data['images']:
                    data['images']['posters'] = [
                        {**poster, 'url': cls.get_image_url(poster['file_path'], 'original')}
                        for poster in data['images']['posters']
                    ]
                if 'backdrops' in data['images']:
                    data['images']['backdrops'] = [
                        {**backdrop, 'url': cls.get_image_url(backdrop['file_path'], 'original')}
                        for backdrop in data['images']['backdrops']
                    ]
            
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"TMDB Movie Details Error: {e}")
            return {"error": f"Une erreur est survenue lors de la récupération des détails : {str(e)}"}