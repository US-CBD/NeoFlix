from src.main.python.models.models import Film, Person, User, Opinion

# Crear instancias de personas (actores, directores, etc.)
director1 = Person("Frank Darabont", 62, "The Shawshank Redemption, The Green Mile")
actor1 = Person("Morgan Freeman", 84, "Million Dollar Baby, Se7en")
actor2 = Person("Tim Robbins", 63, "Mystic River, Arlington Road")
director2 = Person("Francis Ford Coppola", 82, "The Godfather, Apocalypse Now")
actor3 = Person("Marlon Brando", 80, "On the Waterfront, A Streetcar Named Desire")
actor4 = Person("Al Pacino", 82, "Scarface, Heat")
director3 = Person("Christopher Nolan", 51, "Inception, Interstellar")
actor5 = Person("Christian Bale", 49, "The Prestige, American Psycho")
actor6 = Person("Heath Ledger", "†", "Brokeback Mountain, A Knight's Tale")

# Crear instancias de películas
film1 = Film("The Shawshank Redemption", "1994", director1, "Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.")
film2 = Film("The Godfather", "1972", director2, "An organized crime dynasty's aging patriarch transfers control of his clandestine empire to his reluctant son.")
film3 = Film("The Dark Knight", "2008", director3, "When the menace known as The Joker emerges from his mysterious past, he wreaks havoc and chaos on the people of Gotham.")



# Asignar director y actores a las películas
film1.director = director1
film1.add_actor(actor1)
film1.add_actor(actor2)
film2.director = director2
film2.add_actor(actor3)
film2.add_actor(actor4)
film3.director = director3
film3.add_actor(actor5)
film3.add_actor(actor6)

# Crear instancias de usuarios y opiniones
user1 = User("user123")
user2 = User("moviebuff89")

opinion1 = Opinion("A masterpiece!", 5, user1, film1)
opinion2 = Opinion("Classic movie, a must-watch!", 5, user2, film1)
opinion3 = Opinion("Incredible performance by Heath Ledger!", 5, user1, film3)
opinion4 = Opinion("One of the best crime dramas ever made.", 5, user2, film2)

opinion1.save()
opinion2.save()
opinion3.save()
opinion4.save()

# Agregar opiniones a las películas y guardarlas
film1.add_opinion(opinion1)
film1.add_opinion(opinion2)
film3.add_opinion(opinion3)
film2.add_opinion(opinion4)

film1.save()
film2.save()
film3.save()

user1.add_favorite_film(film1)
user2.add_favorite_film(film2)

user1.save()
user2.save()

# Obtener las películas en las que una persona ha actuado o dirigido
acted_films_director1 = director1.get_acted_films()
directed_films_director1 = director1.get_directed_films()
acted_films_actor1 = actor1.get_acted_films()
acted_films_actor2 = actor2.get_acted_films()

# Obtener las películas favoritas de un usuario y sus opiniones
favorite_films_user1 = user1.get_favorite_films()
opinions_user1 = user1.get_opinions()

# Imprimir resultados
print("Películas dirigidas por", director1.name)
for film in directed_films_director1:
    print(film.title)

print("\nPelículas en las que", actor1.name, "ha actuado:")
for film in acted_films_actor1:
    print(film.title)

print("\nPelículas favoritas de", user1.username)
for film in favorite_films_user1:
    print(film.title)

print("\nOpiniones de", user1.username)
for opinion in opinions_user1:
    print(opinion.text)
