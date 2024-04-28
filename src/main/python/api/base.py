import time
import tkinter.messagebox
from concurrent.futures import ThreadPoolExecutor
from typing import List, Union, Callable, Tuple, Dict

from tmdbv3api import TMDb, Movie, Person
from tmdbv3api.objs import genre

from src.main.python.models.models import Film, Worker

MAP_GENRE_NAME: Dict[str, int] = {}
MAP_GENRE_ID: Dict[int, str] = {}


def initialize_tmdb(token: str) -> TMDb:
    """
    Initialize the TMDb instance with the API token.

    Args:
        token (str): The TMDb API token.

    Returns:
        TMDb: Initialized TMDb instance.
    """
    tmdb = TMDb()
    tmdb.api_key = token
    return tmdb


def fetch_genre_ids() -> None:
    """
    Fetches movie genre IDs and names from the TMDb API
    and stores them in the global dictionaries MAP_GENRE_NAME and MAP_GENRE_ID.
    """
    global MAP_GENRE_NAME, MAP_GENRE_ID
    try:
        genres = genre.Genre().movie_list()
        for genre_data in genres:
            genre_name = genre_data['name'].lower()
            genre_id = genre_data['id']
            MAP_GENRE_NAME[genre_name] = genre_id
            MAP_GENRE_ID[genre_id] = genre_name
    except Exception as e:
        tkinter.messagebox.showinfo("Error", f"Error fetching genres from TMDb: {e}")


def get_genre_names() -> List[str]:
    """
    Get movie genre names.

    Returns:
        List[str]: List of genre names.
    """
    return list(MAP_GENRE_NAME.keys())


def get_genre_id(genre_name: str) -> Union[int, None]:
    """
    Get the ID of a genre given its name.

    Args:
        genre_name (str): The genre name.

    Returns:
        Union[int, None]: The genre ID if found, None otherwise.
    """
    return MAP_GENRE_NAME.get(genre_name.lower())


def get_genre_name(genre_id: int) -> Union[str, None]:
    """
    Get the name of a genre given its ID.

    Args:
        genre_id (int): The genre ID.

    Returns:
        Union[str, None]: The genre name if found, None otherwise.
    """
    return MAP_GENRE_ID.get(genre_id)


def parse_worker_details(cast: dict) -> Union[Worker, None]:
    """
    Parse details of a worker (actor/director) from the TMDb API.

    Args:
        cast (dict): Worker data obtained from the TMDb API.

    Returns:
        Union[Worker, None]: Worker object if details parsed successfully, None otherwise.
    """
    try:
        if Worker.exists(cast['original_name']):
            return Worker.find(cast['original_name'])
        details = Person().details(cast['id'])
        return Worker(name=cast['original_name'], birthday=details['birthday'], biography=details['biography'],
                      department=cast['known_for_department'], file=cast['profile_path'])
    except Exception as e:
        tkinter.messagebox.showinfo("Error", f"Error parsing worker details: {e}")
        print(f"Error parsing worker details: {e}")
        return None


def parse_movie_data(movie_data: dict, is_popular: bool = False) -> Tuple[Film, List[dict]]:
    """
    Parse movie data obtained from the TMDb API.

    Args:
        movie_data (dict): Movie data obtained from the TMDb API.
        is_popular (bool, optional): Indicates if the movie is popular. Defaults to False.

    Returns:
        Tuple[Film, List[dict]]: Parsed movie object and list of actor/director data.
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
    parse_movie.add_genre([genre_name for genre_name in genre_names if genre_name is not None])

    persons = Movie().credits(movie_data['id'])
    casts = persons.cast
    return parse_movie, casts


def process_casts(executor: ThreadPoolExecutor, casts: List[dict], parse_movie: Film) -> None:
    """
    Process actors and directors of a movie in parallel using ThreadPoolExecutor.

    Args:
        executor (ThreadPoolExecutor): ThreadPoolExecutor object to handle parallel executions.
        casts (List[dict]): List of actor/director data obtained from the TMDb API.
        parse_movie (Film): Film object to which actors and directors will be added.
    """
    future_workers = [executor.submit(parse_worker_details, cast) for cast in casts]
    for future in future_workers:
        worker_details = future.result()
        print(f"Processing worker {worker_details.name}")
        if worker_details is not None:
            if worker_details.department == 'Acting':
                parse_movie.add_actor(worker_details)
            elif worker_details.department == 'Directing':
                parse_movie.add_director(worker_details)


def process_movies(fetch_function: Callable, start: int, end: int, max_workers: int, are_popular: bool = False) -> List[Film]:
    """
    Process movies in parallel using ThreadPoolExecutor.

    Args:
        fetch_function (Callable): Function to fetch movie data.
        start (int): Starting page number.
        end (int): Ending page number.
        max_workers (int): Maximum number of worker threads.
        are_popular (bool, optional): Indicates if the movies are popular. Defaults to False.

    Returns:
        List[Film]: List of Film objects created from the processed movie data.
    """
    movies = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for page in range(start, end):
            results = fetch_function(page)
            for movie_data in results:

                print("Processing movie ", movie_data['title'])
                start_time = time.time()
                if not Film.exists(movie_data['title']):
                    parse_movie, casts = parse_movie_data(movie_data, are_popular)
                    process_casts(executor, casts, parse_movie)
                    movies.append(parse_movie)
                end_time = time.time()
                print("Time =", end_time - start_time)

    print("Saving movies!!!")

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for movie in movies:
            print("Saving " + movie.title)
            executor.submit(movie.save())

    return movies






