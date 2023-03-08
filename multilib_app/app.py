from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
@app.route('/main')
def main():
    return render_template("main.html")

@app.route('/movies')
def movies():
    return render_template("movies.html")
@app.route('/serials')
def serials():
    return render_template("serials.html")
@app.route('/books')
def books():
    return render_template("books.html")
@app.route('/anime')
def anime():
    return render_template("anime.html")
@app.route('/manga')
def manga():
    return render_template("manga.html")

@app.route('/search')
def search():
    return render_template("search.html")

@app.route('/auth')
def auth():
    return render_template("auth.html")

@app.route('/profile')
def profile():
    return render_template("profile.html")

@app.route('/product')
def product():
    return render_template("product.html")


if __name__ == "__main__":
    app.run(debug=True)