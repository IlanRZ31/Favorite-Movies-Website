from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, FloatField
from wtforms.validators import DataRequired, URL
import requests

API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTIzNTY0YWFhYmI5MjM5MzdhMzg1YzllMjA4YTgzMCIsInN1YiI6IjY0YjcxNmJhYjUxM2E4MDEyYzI1NmZmMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z6GHTcsfUiBFuFti9BU8Kma4Ru3Ezr_k-to5SdCYaNg"
movie_url = "https://api.themoviedb.org/3/search/movie"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxYTIzNTY0YWFhYmI5MjM5MzdhMzg1YzllMjA4YTgzMCIsInN1YiI6IjY0YjcxNmJhYjUxM2E4MDEyYzI1NmZmMyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.Z6GHTcsfUiBFuFti9BU8Kma4Ru3Ezr_k-to5SdCYaNg"
}

db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///top-movies.db"
# initialize the app with the extension
db.init_app(app)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float)
    ranking = db.Column(db.String(250), nullable=False)
    review = db.Column(db.String(350))
    img_url = db.Column(db.String(100), nullable=False)


with app.app_context():
    db.create_all()

app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
bootstrap = Bootstrap5(app)


class AddMovieForm(FlaskForm):
    title = StringField('Movie Name', validators=[DataRequired()])
    # year = IntegerField('Release Year', validators=[DataRequired()])
    # description = StringField('Description', validators=[DataRequired()])
    # rating = FloatField("Rating", validators=[DataRequired()])
    # ranking = IntegerField("Ranking", validators=[DataRequired()])
    # review = StringField("Review", validators=[DataRequired()])
    # img_url = StringField("Image URL", validators=[DataRequired(), URL()])
    submit = SubmitField('Submit')


class EditMovieForm(FlaskForm):
    review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField('Submit')


@app.route("/")
def home():
    result = db.session.execute(db.select(Movie).order_by(Movie.rating))
    all_movies = result.scalars().all() # convert ScalarResult to Python List

    for i in range(len(all_movies)):
        all_movies[i].ranking = len(all_movies) - i
    db.session.commit()

    return render_template("index.html", movies=all_movies)


@app.route("/add", methods=['GET', 'POST'])
def add():
    form = AddMovieForm()
    if form.validate_on_submit():
        parameters = {"query": form.title.data}
        response = requests.get(movie_url, headers=headers, params=parameters)
        data = response.json()["results"]
        return render_template("select.html", data=data)
    else:
        return render_template("add.html", form=form)


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    form = EditMovieForm()
    movie = db.get_or_404(Movie, id)
    if form.validate_on_submit():
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", form=form, movie=movie)


@app.route("/delete")
def delete():
    movie_id = request.args.get('id')
    movie_to_delete = db.get_or_404(Movie, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


@app.route("/find/<int:id>")
def find_movie(id):
    movie_details_url = "https://api.themoviedb.org/3/movie/{}".format(id)
    response = requests.get(movie_details_url, headers=headers)
    data = response.json()

    # Check if the movie with the same title already exists in the database
    existing_movie = Movie.query.filter_by(title=data["original_title"]).first()

    if existing_movie:
        # If the movie exists, redirect to the edit page for that movie
        return redirect(url_for("home"))
    else:
        # If the movie does not exist, add it to the database
        movie = Movie(
            title=data["original_title"],
            year=int(data["release_date"].split("-")[0]),
            description=data["overview"],
            rating=data["vote_average"],
            ranking=0,
            review=None,
            img_url="https://image.tmdb.org/t/p/w500/{}".format(data["poster_path"]),
        )
        db.session.add(movie)
        db.session.commit()

        # Redirect to the edit page for the newly added movie with the generated movie ID
        return redirect(url_for("edit", id=movie.id))




if __name__ == '__main__':
    app.run(debug=True)
