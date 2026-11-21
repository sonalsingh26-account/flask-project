from flask import Flask , render_template

app = Flask(__name__)

@app.route("/")
def login():
	is_logged_in = True
	marks = 75
	return render_template("home.html",login = is_logged_in , marks = marks)

if __name__ == "__main__":
	app.run(debug = True)