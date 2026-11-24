from flask import Flask, render_template,request, redirect , url_for, flash, session, render_template,jsonify
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///app.db"
db = SQLAlchemy(app)

class User(db.Model):
	__tablename__= "users"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(50),nullable=False)
	email = db.Column(db.String(50), nullable=False)
	age= db.Column(db.Integer)

@app.route("/")
def home():
	return "Home Page"

# Flask error handler code
@app.errorhandler(404)
def page_not_found(error):
	return render_template("404.html")

@app.errorhandler(500)
def internal_server_error(error):
	return render_template("500.html")

@app.route("/test")
def test_500():
	result = 10/0
	return result
# Database CRUD operations

@app.route("/create_user", methods=["POST"])
def create_user():
	data =  request.get_json()
	name = data.get("name")
	email = data.get("email")
	age = data.get("age")
	user = User(name =name, email=email, age=age)
	db.session.add(user)
	db.session.commit()
	return "User created successfully"

@app.route("/get_users", methods=["GET"])
def get_users():
	users =  User.query.all()
	users_data = []
	for user in users:
		users_data.append({"id":user.id, "name":user.name, "email":user.email,"age":user.age})
	return jsonify(users_data)

# Render data on HTML page
@app.route("/all_users", methods=["GET"])
def all_users():
	users = User.query.all()
	return render_template("users.html", users = users)

@app.route("/user/<int:id>", methods=["GET"])
def user(id):
	user= db.get_or_404(User,id)
	return jsonify({
		"id":user.id,
		"name":user.name,
		"email":user.email,
		"age":user.age
	})

@app.route("/user/<int:id>", methods=["PATCH"])
def update_user(id):
	data =  request.get_json()
	user = db.get_or_404(User, id)
	if "name" in data:
		user.name = data.get("name")
	if "email" in data:
		user.email = data.get("email")
	if "age" in data:
		user.age = data.get("age")
	db.session.commit()
	return jsonify({"Message":"User updated successfully",
					"User":{"id":user.id, "name":user.name , "email":user.email, "age": user.age}})

@app.route("/user/<int:id>", methods = ["DELETE"])
def delete_user(id):
	user = db.get_or_404(User, id)
	db.session.delete(user)
	db.session.commit()
	return jsonify({"Message":"User Deleted Successfully",
					"User Details": {"id":user.id, "name":user.name , "email":user.email, "age": user.age}})


if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	#app.run(debug = False) make false to test internal server error
	app.run(debug=True)