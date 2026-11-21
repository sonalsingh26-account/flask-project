from flask import Flask, render_template , request
import uuid
app = Flask(__name__)

# Initialize routes
# rendering static data on jinja2 templates
@app.route("/")
def home():
	name = "dear user"
	course = "software course"
	price = 15000
	return render_template("home.html",name = name,course = course,price=price)


@app.route("/user/<name>")
def user(name):
	return f"User Page {name}!!"

@app.route("/usercourse/<string:name>/<int:course>/<float:price>")
def usercourse(name,course,price):
	return f"User {name} is learning course {course} price is {price}!!"

# Path parameter
@app.route("/filepath/<path:path>")
def filepath(path):
	return f"file path is {path}"

@app.route("/unique/<uuid:unique>")
def unique(unique):
	return f"unique number is {unique}"

# query parameter
@app.route("/search")
def search():
	name = request.args.get("name")
	course = request.args.get("course","fronend")
	return f"{name} is learning {course}"

@app.route("/course")
def student():
	data = {"name":"Python",
			"Duration":"12hrs",
			"Place":"[Delhi,Mumbai]"
			}
	return render_template("home.html",data=data)

if __name__ == "__main__":
	app.run(debug=True)
