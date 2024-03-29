from src.main.python.models.models import Film
from src.main.python.models.models import Opinion
from src.main.python.models.models import Person
from src.main.python.models.models import User
from src.main.python.repositories.FilmRepository import FilmRepository
from src.main.python.repositories.OpinionRepository import OpinionRepository
from src.main.python.repositories.PersonRepository import PersonRepository
from src.main.python.repositories.UserRepository import UserRepository


def main():
    # Crear instancias de películas, personas y usuarios
    director1 = Person("Director 1", 50, "Bibliography 1")
    director2 = Person("Director 2", 60, "Bibliography 2")
    film1 = Film("Film 1", "2022-01-01", director1, "Description 1")
    film2 = Film("Film 2", "2023-01-01", director2, "Description 2")
    person1 = Person("Person 1", 30, "Bibliography 1")
    person2 = Person("Person 2", 40, "Bibliography 2")
    user1 = User("User1")
    user2 = User("User2")

    # Añadir actores, géneros y películas favoritas
    film1.add_actor(person1)
    film1.add_actor(person2)
    film1.add_genre("Genre 1")
    film1.add_genre("Genre 2")

    film2.add_actor(person1)
    film2.add_actor(person2)
    film2.add_genre("Genre 3")
    film2.add_genre("Genre 4")

    person1.add_film(film1)
    person2.add_film(film1)
    user1.add_favorite_film(film1)
    user2.add_favorite_film(film2)

    # Inicializar repositorios
    film_repo = FilmRepository()
    person_repo = PersonRepository()
    user_repo = UserRepository()
    opinion_repo = OpinionRepository()

    # Crear o actualizar nodos en la base de datos
    film_repo.create_or_update(film1)
    film_repo.create_or_update(film2)
    user_repo.create_or_update(user1)
    user_repo.create_or_update(user2)

    # Buscar y eliminar nodos en la base de datos
    found_film = film_repo.find("Film 1")
    if found_film:
        print("Film found:", found_film)
        film_repo.delete("Film 1")
        print("Film deleted")

    found_person = person_repo.find("Person 1")
    if found_person:
        print("Person found:", found_person)
        person_repo.delete("Person 1")
        print("Person deleted")

    found_user = user_repo.find("User1")
    if found_user:
        print("User found:", found_user)
        user_repo.delete("User1")
        print("User deleted")

    # Realizar algunas consultas adicionales
    print("\n--- Additional Queries ---")
    film2 = film_repo.find("Film 2")
    print("Film 2:", film2)

    director2_node = film_repo.find_director_for_film("Film 2")
    print("Director for Film 2:", director2_node)

    actors_for_film2 = film_repo.find_actors_for_film("Film 2")
    print("Actors for Film 2:", actors_for_film2)

    genres_for_film2 = film_repo.find_genres_for_film("Film 2")
    print("Genres for Film 2:", genres_for_film2)

    opinions_for_film2 = film_repo.find_opinions_for_film("Film 2")
    print("Opinions for Film 2:", opinions_for_film2)

    # Crear y añadir opiniones a una película
    opinion1 = Opinion("Great movie!", 5, user1, film2)
    opinion2 = Opinion("Not my cup of tea.", 2, user2, film2)
    opinion_repo.create_or_update(opinion1)
    opinion_repo.create_or_update(opinion2)

    updated_opinions_for_film2 = film_repo.find_opinions_for_film("Film 2")
    print("Updated Opinions for Film 2:", updated_opinions_for_film2)

if __name__ == "__main__":
    main()

