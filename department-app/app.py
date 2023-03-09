"""Module providing Flask realising hosting web-application at local instance"""
from flask import Flask, render_template

app = Flask(__name__)
@app.route('/')
@app.route('/main')
def main():
    ### Main page route
    return render_template("main.html")

@app.route('/movies')
def movies():
    ### movies page route
    return render_template("movies.html")
@app.route('/serials')
def serials():
    ### serials page route
    return render_template("serials.html")
@app.route('/books')
def books():
    ### books page route
    return render_template("books.html")
@app.route('/anime')
def anime():
    ### anime page route
    return render_template("anime.html")
@app.route('/manga')
def manga():
    ### manga page route
    return render_template("manga.html")

@app.route('/search')
def search():
    ### search page route
    return render_template("search.html")

@app.route('/auth')
def auth():
    ### auth page route
    return render_template("auth.html")

@app.route('/profile')
def profile():
    ### profile page route
    return render_template("profile.html")

@app.route('/product')
def product():
    ### product page route
    return render_template("product.html")


if __name__ == "__main__":
    app.run(debug=True)
