from tmdbv3api import Discover

from src.main.python.api.base import process_movies, get_genre_id

def fetch_movies_by_genre_page(genre_id, page):
    """
    Obtiene una página de películas de un género específico desde la API de TMDb.

    Args:
        genre_id (int): ID del género.
        page (int): Número de página.

    Returns:
        list: Lista de películas de la página especificada.
    """
    results = Discover().discover_movies({"with_genres": genre_id, "page": page, "sort_by": "popularity.desc"})
    return results
def get_movies_by_genre(genre_name, start=1, end=2, max_workers=5):
    """
    Obtiene películas de un género específico desde la API de TMDb.

    Args:
        genre_name (str): Nombre del género.
        start (int): Número de página inicial (por defecto: 1).
        end (int): Número de página final (por defecto: 2).
        max_workers (int): Número máximo de hilos de ejecución (por defecto: 5).

    Returns:
        list: Lista de objetos Film creados a partir de las películas del género especificado.
    """
    genre_id = get_genre_id(genre_name)
    if genre_id is None:
        return []

    fetch_function = lambda page: fetch_movies_by_genre_page(genre_id, page)
    return process_movies(fetch_function, start, end, max_workers)

