import csv
import chardet
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

MOVIE_DB_API_KEY = "your moviedb api key"
MOVIE_DB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
MOVIE_DB_INFO_URL = "https://api.themoviedb.org/3/movie"
MOVIE_DB_IMAGE_URL = "https://image.tmdb.org/t/p/w500"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'any password'
Bootstrap5(app)

CSV_FILE = 'movies.csv'


class FindMovieForm(FlaskForm):
    title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


class RateMovieForm(FlaskForm):
    rating = StringField("Your Rating Out of 10 e.g. 7.5")
    review = StringField("Your Review")
    submit = SubmitField("Done")


def read_movies_from_csv():
    movies = []
    with open(CSV_FILE, 'rb') as f:
        rawdata = f.read()
        result = chardet.detect(rawdata)
        encoding = result['encoding']

    with open(CSV_FILE, 'r', encoding=encoding) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Handle specific characters causing issues
            for key, value in row.items():
                if isinstance(value, str):
                    row[key] = value.replace('\x97', '')  # Replace problematic character
            movies.append(row)
    return movies


def write_movies_to_csv(movies):
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['id', 'title', 'year', 'description', 'rating', 'ranking', 'review', 'img_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for movie in movies:
            writer.writerow(movie)


@app.route("/")
def home():
    movies = read_movies_from_csv()
    movies.sort(key=lambda x: x['rating'] if x['rating'] is not None else 0, reverse=True)
    for i, movie in enumerate(movies):
        movie['ranking'] = len(movies) - i
    write_movies_to_csv(movies)
    return render_template("index.html", movies=movies)


@app.route("/add", methods=["GET", "POST"])
def add_movie():
    form = FindMovieForm()
    if form.validate_on_submit():
        movie_title = form.title.data
        response = requests.get(MOVIE_DB_SEARCH_URL, params={"api_key": MOVIE_DB_API_KEY, "query": movie_title})
        data = response.json()["results"]
        return render_template("select.html", options=data)
    return render_template("add.html", form=form)


@app.route("/find")
def find_movie():
    movie_api_id = request.args.get("id")
    if movie_api_id:
        movie_api_url = f"{MOVIE_DB_INFO_URL}/{movie_api_id}"
        response = requests.get(movie_api_url, params={"api_key": MOVIE_DB_API_KEY, "language": "en-US"})
        data = response.json()
        new_movie = {
            'id': data['id'],
            'title': data['title'],
            'year': data['release_date'].split("-")[0],
            'description': data['overview'],
            'rating': None,
            'ranking': None,
            'review': None,
            'img_url': f"{MOVIE_DB_IMAGE_URL}{data['poster_path']}"
        }
        movies = read_movies_from_csv()
        movies.append(new_movie)
        write_movies_to_csv(movies)
        return redirect(url_for("rate_movie", id=new_movie['id']))


@app.route("/edit", methods=["GET", "POST"])
def rate_movie():
    form = RateMovieForm()
    movie_id = int(request.args.get("id"))
    movies = read_movies_from_csv()
    movie = next((m for m in movies if int(m['id']) == movie_id), None)
    if movie and form.validate_on_submit():
        movie['rating'] = float(form.rating.data) if form.rating.data else None
        movie['review'] = form.review.data
        write_movies_to_csv(movies)
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete")
def delete_movie():
    movie_id = int(request.args.get("id"))
    movies = read_movies_from_csv()
    movies = [m for m in movies if int(m['id']) != movie_id]
    write_movies_to_csv(movies)
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
