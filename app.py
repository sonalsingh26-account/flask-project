from flask import Flask, render_template,request

app = Flask(__name__)

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/about")
def about():
	return render_template("about.html")

@app.route("/contact", methods=["GET","POST"])
def contact():
	if request.method =="POST":
		name = request.form.get("username")
		email = request.form.get("email")
		message = request.form.get("message")
		return f"Data received from post api {name}: {email}: {message}"

	return render_template("contact.html")

@app.route("/search")   # This is GET method
def search():
	query = request.args.get('query')
	return f"Get api received query {query}"
if __name__ == "__main__":
	app.run(debug = True)