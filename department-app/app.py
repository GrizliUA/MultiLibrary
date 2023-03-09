"""Module providing Flask realising hosting web-application at local instance"""
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
@app.route('/main')
### Main page function
def main():
    ### Main page route
    return render_template("main.html")
    ### Main page route



@app.route('/movies')
### movies page function
def movies():
    ### movies page route
    return render_template("movies.html")


@app.route('/serials')
### serials page function
def serials():
    ### serials page route
    return render_template("serials.html")


@app.route('/books')
### books page function
def books():
    ### books page route
    return render_template("books.html")


@app.route('/anime')
### anime page function
def anime():
    ### anime page route
    return render_template("anime.html")


@app.route('/manga')
### manga page function
def manga():
    ### manga page route
    return render_template("manga.html")


@app.route('/search')
### search page function
def search():
    ### search page route
    return render_template("search.html")


@app.route('/auth')
### auth page function
def auth():
    ### auth page route
    return render_template("auth.html")


@app.route('/profile')
### profile page function
def profile():
    ### profile page route
    return render_template("profile.html")


@app.route('/product')
### product page function
def product():
    ### product page route
    return render_template("product.html")


if __name__ == "__main__":
    app.run(debug=True)
