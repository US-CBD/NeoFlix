import time
import tkinter.messagebox
from concurrent.futures import ThreadPoolExecutor

from tmdbv3api import TMDb, Movie, Person, Discover
from tmdbv3api.objs import genre

from src.main.python.models.models import Film, Worker

MAP_GENRE_NAME = {}
MAP_GENRE_ID = {}


def initialize_tmdb(token):
    """
    Inicializa la instancia de TMDb con el token de la API.

    Args:
        token (str): Token de la API de TMDb.

    Returns:
        TMDb: Instancia de la clase TMDb inicializada.
    """
    tmdb = TMDb()
    tmdb.api_key = token
    return tmdb


def fetch_genre_ids():
    """
    Obtiene los IDs y nombres de géneros de películas desde la API de TMDb
    y los almacena en los diccionarios globales MAP_GENRE_NAME y MAP_GENRE_ID.
    """
    global MAP_GENRE_NAME
    global MAP_GENRE_ID
    try:
        genres = genre.Genre().movie_list()
    except:
        tkinter.messagebox.showinfo("Error", "Error fetching genres from TMDb.")
    for genre_data in genres:
        MAP_GENRE_NAME[genre_data['name'].lower()] = genre_data['id']
        MAP_GENRE_ID[genre_data['id']] = genre_data['name']

def get_genre_names():
    """
    Obtiene los nombres de los géneros de películas.

    Returns:
        list: Lista de nombres de géneros.
    """
    return list(MAP_GENRE_NAME.keys())


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


def parse_worker_details(cast):
    """
    Parsea los detalles de un trabajador (actor/director) desde la API de TMDb.

    Args:
        cast (dict): Datos del trabajador obtenidos de la API de TMDb.

    Returns:
        Worker or None: Objeto Worker si los detalles se pudieron parsear correctamente, None en caso contrario.
    """
    try:
        details = Person().details(cast['id'])
        return Worker(name=cast['original_name'], birthday=details['birthday'], bibliography=details['biography'],
                      department=cast['known_for_department'], file=cast['profile_path'])
    except Exception as e:
        tkinter.messagebox.showinfo("Error", f"Error parsing worker details: {e}")
        print(f"Error parsing worker details: {e}")
        return None


def parse_movie_data(movie_data, is_popular=False):
    """
    Parsea los datos de una película obtenidos de la API de TMDb.

    Args:
        movie_data (dict): Datos de la película obtenidos de la API de TMDb.

    Returns:
        Film: Objeto Film creado a partir de los datos de la película.
        list: Lista de actores y directores de la película.
    """
    parse_movie = Film(
        title=movie_data['title'],
        release_date=movie_data['release_date'],
        description=movie_data['overview'],
        file=movie_data['poster_path'],
        vote_average=movie_data['vote_average'],
        is_popular=is_popular
    )

    genre_names = [get_genre_name(genre_id) for genre_id in movie_data['genre_ids']]
    for genre_name in genre_names:
        if genre_name is not None:
            parse_movie.add_genre(genre_name)

    casts = Movie().credits(movie_data['id']).cast
    return parse_movie, casts


def process_casts(executor, casts, parse_movie):
    """
    Procesa los actores y directores de una película en paralelo utilizando ThreadPoolExecutor.

    Args:
        executor (ThreadPoolExecutor): Objeto ThreadPoolExecutor para manejar las ejecuciones en paralelo.
        casts (list): Lista de datos de actores y directores obtenidos de la API de TMDb.
        parse_movie (Film): Objeto Film al que se agregarán los actores y directores.
    """
    future_workers = [executor.submit(parse_worker_details, cast) for cast in casts]
    for future in future_workers:
        worker_details = future.result()
        if worker_details is not None:
            if worker_details.department == 'Acting':
                parse_movie.add_actor(worker_details)
            elif worker_details.department == 'Directing':
                parse_movie.add_director(worker_details)





def process_movies(fetch_function, start, end, max_workers, are_popular=False):
    """
    Procesa películas en paralelo utilizando ThreadPoolExecutor.

    Args:
        fetch_function (function): Función para obtener los datos de las películas.
        start (int): Número de página inicial.
        end (int): Número de página final.
        max_workers (int): Número máximo de hilos de ejecución.

    Returns:
        list: Lista de objetos Film creados a partir de los datos de las películas procesadas.
    """
    movies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(start, end):
            results = fetch_function(page)
            for movie_data in results:
                print(movie_data['title'])
                start_time = time.time()
                parse_movie, casts = parse_movie_data(movie_data, are_popular)
                process_casts(executor, casts, parse_movie)
                end_time = time.time()
                print("Time =", end_time - start_time)
                movies.append(parse_movie)
    for movie in movies:
        movie.save()
    return movies




