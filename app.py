from flask import Flask, render_template,request, redirect , url_for

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
		age = request.form.get("age")
		if not name:
			return "Name is required for registration"
		if not email:
			return "Email is reuired for registration"
		if not age:
			return "Age is required for registration"
		if not age.isdigit():
			return "Age must be integer"

		#return redirect("/success")  #But this is not recommanded way to call direct end point while use function so in future endpoint change so not need to change in the redirect 
		return redirect("success")
	return render_template("contact.html")

@app.route("/success")
def success():
	return "Registration done successfully!!"

@app.route("/search")   # This is GET method
def search():
	query = request.args.get('query')
	return f"Get api received query {query}"
if __name__ == "__main__":
	app.run(debug = True)