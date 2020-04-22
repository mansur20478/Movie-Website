from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("base.html")


@app.route("/film_page")
def film_page():
    return render_template("film_page.html")


if __name__ == '__main__':
    app.run()
