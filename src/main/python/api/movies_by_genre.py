from tmdbv3api.objs import genre

from src.main.python.api.base import fetch_movies_by_genre_page, process_movies

MAP_GENRE_NAME = {}
MAP_GENRE_ID = {}

def fetch_genre_ids():
    """
    Obtiene los IDs y nombres de géneros de películas desde la API de TMDb
    y los almacena en los diccionarios globales MAP_GENRE_NAME y MAP_GENRE_ID.
    """
    global MAP_GENRE_NAME
    global MAP_GENRE_ID
    genres = genre.Genre().movie_list()
    for genre_data in genres:
        MAP_GENRE_NAME[genre_data['name'].lower()] = genre_data['id']
        MAP_GENRE_ID[genre_data['id']] = genre_data['name']


def get_genre_id(genre_name):
    """
    Obtiene el ID de un género dado su nombre.

    Args:
        genre_name (str): Nombre del género.

    Returns:
        int or None: ID del género si se encuentra, None si no se encuentra.
    """
    return MAP_GENRE_NAME.get(genre_name.lower())


def get_genre_name(genre_id):
    """
    Obtiene el nombre de un género dado su ID.

    Args:
        genre_id (int): ID del género.

    Returns:
        str or None: Nombre del género si se encuentra, None si no se encuentra.
    """
    return MAP_GENRE_ID.get(genre_id)
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

