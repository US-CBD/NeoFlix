from tmdbv3api import Discover

from src.main.python.api.base import process_movies, get_genre_id


def fetch_movies_by_genre_page(genre_id: int, page: int) -> list:
    """
    Retrieve a page of movies for a specific genre from the TMDb API.

    Args:
        genre_id (int): The genre ID.
        page (int): The page number.

    Returns:
        list: List of movies from the specified page.
    """
    try:
        results = Discover().discover_movies({"with_genres": genre_id, "page": page, "sort_by": "popularity.desc"})
        return results
    except Exception as e:
        print(f"Error fetching movies by genre page: {e}")
        return []


def get_movies_by_genre(genre_name: str, start: int = 1, end: int = 2, max_workers: int = 5) -> list:
    """
    Retrieve movies of a specific genre from the TMDb API.

    Args:
        genre_name (str): The genre name.
        start (int): The starting page number (default: 1).
        end (int): The ending page number (default: 2).
        max_workers (int): The maximum number of worker threads (default: 5).

    Returns:
        list: List of Film objects created from the movies of the specified genre.
    """
    genre_id = get_genre_id(genre_name)
    if genre_id is None:
        return []

    fetch_function = lambda page: fetch_movies_by_genre_page(genre_id, page)
    return process_movies(fetch_function, start, end, max_workers)


