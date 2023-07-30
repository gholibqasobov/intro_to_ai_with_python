import csv
import sys

names = {}
people = {}
movies = {}

"""
people = {
    102: {
        name: "some actor",
        birth: 1984,
        movies: set(some movies)
    }
}
"""


def load_data(directory):
    with open(f"{directory}/people.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row['id']] = {
                'name': row['name'],
                'birth': row['birth'],
                'movies': set()
            }

            if row['name'].lower() not in names:
                names[row['name'].lower()] = {row['id']}
            else:
                names[row['name'].lower()].add(row['id'])

    with open(f"{directory}/movies.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row['id']] = {
                'title': row['title'],
                'year': row['year'],
                'stars': set()
            }

    with open(f"{directory}/stars.csv") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row['person_id']]['movies'].add(row['movie_id'])
                movies[row['movie_id']]['stars'].add(row['person_id'])
            except KeyError:
                pass


"""

movies = {
    104257: {
        title: "movie title",
        year: 1990,
        stars: set(102, 129)
    }
}

"""


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)
    if path is None:
        print("Not connected")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]['name']
            person2 = person1[path[i+1][1]]['name']
            movie = movies[path[i+1][0]]['title']
            print(f"{i+1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):

    raise NotImplementedError


def person_id_for_name(name):
    person_ids = list(names.get(name.lower(), set())) # guess the same as names[name.lower()]
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person['name']
            birth = person['birth']
            person(f"ID: {person_id}, Name: {name}, Birth: {birth}")

        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    movie_ids = people[person_id]['movies']
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]['stars']:
            neighbors.add((movie_id, person_id))
    return neighbors
