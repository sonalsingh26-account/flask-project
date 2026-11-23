from flask import Flask, render_template,request, redirect , url_for, flash, session
import os
from dotenv import load_dotenv
app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
UPLOAD_FOLDER ="uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok = True)
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
#Upload file code
@app.route("/upload",methods=["GET","POST"])
def upload():
	if request.method == "POST":
		file =  request.files.get("file")
		if not file:
			return "Please upload file first"
		if file.filename =="":
			return "Please upload file as filename is not there"
		file.save(os.path.join(UPLOAD_FOLDER , file.filename))
		return "File uploaded successfully"
	return render_template("upload.html")

if __name__ == "__main__":
	app.run(debug = os.getenv("debug"))