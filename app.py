from flask import Flask, render_template,request, redirect , url_for, flash, session

app = Flask(__name__)
app.secret_key = "change_on_production"

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
			flash("Name is required for registration","danger")
			return redirect(url_for("contact"))
		if not email:
			flash("Email is reuired for registration","danger")
			return redirect(url_for("contact"))
		if not age:
			flash("Age is required for registration","danger")
			return redirect(url_for("contact"))
		if not age.isdigit():
			flash("Age must be integer","danger")
			return redirect(url_for("contact"))

		#return redirect("/success")  #But this is not recommanded way to call direct end point while use function so in future endpoint change so not need to change in the redirect 
		#return redirect("success")
		# Now below code for flash messagee
		flash("Registration done Successfully !!","success")
	return render_template("contact.html")

@app.route("/success")
def success():
	return "Registration done successfully!!"

@app.route("/search")   # This is GET method
def search():
	query = request.args.get('query')
	return f"Get api received query {query}"

# Below code for session mechanism
@app.route("/login")
def login():
	session["username"] = "sonal"
	return f"Logged in successfully !!"
@app.route("/dashboard")
def dashboard():
	username  =  session.get("username",None)
	if username:
		return f"Welcome to {username}"
	return "Please Login first"
@app.route("/logout")
def logout():
	session.pop("username",None)
	return f"Logout successfully !!" 


if __name__ == "__main__":
	app.run(debug = True)