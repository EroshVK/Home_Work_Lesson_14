import sqlite3


def one_item(query: str):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row
        result = connection.execute(query).fetchone()

        if result is None:
            return None
        else:
            return dict(result)


def several_items(query: str):
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = []

        for item in connection.execute(query).fetchall():
            result.append(dict(item))

        return result


def two_actors(name1: str = 'Jack Black', name2: str = 'Dustin Hoffman'):
    query = f"""
            SELECT * FROM netflix
            WHERE netflix."cast" LIKE '%{name1}%' AND netflix."cast" LIKE '%{name2}%'
            """

    cast = []
    set_cast = set()
    result = several_items(query)

    for item in result:
        for actor in item['cast'].split(','):
            cast.append(actor)

    for actor in cast:
        if cast.count(actor) > 2:
            set_cast.add(actor)

    return list(set_cast)


def movie_json(type_movie = 'TV Show', release_year = '2017', listed_in = 'TV Dramas'):
    query = f"""
            SELECT * FROM netflix
            WHERE "type" = '{type_movie}'
            AND release_year = {release_year}
            AND listed_in like '%{listed_in}%'
            """

    result = []

    for item in several_items(query):
        result.append(
            {
                "title": item['title'],
                "release_year": item['release_year']
            }
        )

    return result
