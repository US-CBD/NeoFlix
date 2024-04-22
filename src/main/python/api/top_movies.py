from tmdbv3api import Movie

from src.main.python.api.base import process_movies


def get_top_movies(start: int = 1, end: int = 2, max_workers: int = 5) -> list:
    """
    Retrieve popular movies from the TMDb API.

    Args:
        start (int): The starting page number (default: 1).
        end (int): The ending page number (default: 2).
        max_workers (int): The maximum number of worker threads (default: 5).

    Returns:
        list: List of Film objects created from the popular movies.
    """
    fetch_function = lambda page: Movie().popular(page=page)
    return process_movies(fetch_function, start, end, max_workers, are_popular=True)
