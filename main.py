from flask import Flask, jsonify
from utils import *

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False


@app.route('/movie/<title>')
def get_by_title(title: str):
    query = f"""
    SELECT * FROM netflix
    WHERE title = '{title}'
    ORDER BY date_added DESC
    """
    query_result = one_item(query)

    if query_result is None:
        return 'Такого названия не существует'

    movie = {
        "title": query_result['title'],
        "country": query_result['country'],
        "release_year": query_result['release_year'],
        "genre": query_result['listed_in'],
        "description": query_result['description'],
    }

    return jsonify(movie)


@app.route('/movie/<year1>/to/<year2>')
def get_by_years(year1: str, year2: str):
    query = f"""
        SELECT title, release_year FROM netflix
        WHERE release_year BETWEEN {year1} AND {year2}
        LIMIT 100 
        """

    query_result = []

    for item in several_items(query):
        query_result.append(
            {
                "title": item['title'],
                "release_year": item['release_year'],
            }
        )

    return jsonify(query_result)


@app.route('/rating/<category>')
def get_by_rating(category: str):

    if category == 'children':
        query_rating = "('G')"

    elif category == 'family':
        query_rating = "('G', 'PG', 'PG-13')"

    elif category == 'adult':
        query_rating = "('R', 'NC-17')"

    else:
        return 'Такой категории не существует'

    query = f"""
        SELECT title, rating, description FROM netflix
        WHERE rating in {query_rating}
        """

    query_result = []

    for item in several_items(query):
        query_result.append(
            {
                "title": item['title'],
                "rating": item['rating'],
                "description": item['description'],
            }
        )

    return jsonify(query_result)


@app.route('/genre/<genre>')
def get_by_genre(genre: str):
    query = f"""
            SELECT * FROM netflix
            WHERE listed_in LIKE '%{genre}%'
            ORDER BY release_year DESC
            LIMIT 10
            """

    query_result = []

    for item in several_items(query):
        query_result.append(
            {
                "title": item['title'],
                "description": item['description'],
            }
        )

    return jsonify(query_result)


if __name__ == '__main__':
    app.run(debug=True)
