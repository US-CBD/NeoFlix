class Person:
    def __init__(self, name: str, age: int, bibliography: str):
        self.name = name
        self.age = age
        self.bibliography = bibliography
        self.films = []

    def add_film(self, film):
        self.films.append(film)