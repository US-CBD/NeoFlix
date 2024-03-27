from tmdbv3api import Movie

from src.main.python.api.base import process_movies


def get_top_movies(start=1, end=2, max_workers=5):
    """
    Obtiene películas populares desde la API de TMDb.

    Args:
        start (int): Número de página inicial (por defecto: 1).
        end (int): Número de página final (por defecto: 2).
        max_workers (int): Número máximo de hilos de ejecución (por defecto: 5).

    Returns:
        list: Lista de objetos Film creados a partir de las películas populares.
    """
    fetch_function = lambda page: Movie().popular(page=page)
    return process_movies(fetch_function, start, end, max_workers)