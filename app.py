from flask import Flask , request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from sqlalchemy import text
from urllib.parse import quote_plus

load_dotenv()
app = Flask(__name__)
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = quote_plus(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = "mysql+pymysql://"+f"{DB_USERNAME}:{DB_PASSWORD}"+f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
db = SQLAlchemy(app)

@app.route("/")
def home():
	return "Welcome Flask Course"


@app.route("/db-test")
def db_test():
	result = db.session.execute(text("SELECT 1"))
	value = result.scalar()
	return f"Database setup completed !! Result : {value}"
			   	
class User(db.Model):
	__tablename__ = "user"
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(50), nullable = False)
	email = db.Column(db.String(50), nullable=False)
	age = db.Column(db.Integer)
	orders = db.relationship("Order", backref="user", lazy= True)

class Order(db.Model):
	__tablename__ = "order"
	id = db.Column(db.Integer, primary_key= True)
	product = db.Column(db.String(50), nullable = False)
	price = db.Column(db.Float, nullable= False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)

@app.route("/create-user", methods = ["POST"])
def create_user():
	data = request.get_json()
	user = User(name = data.get("name"), email = data.get("email") , age= data.get("age"))
	db.session.add(user)
	db.session.commit()
	return "User created successfully"

@app.route("/users", methods = ["GET"])
def users():
	users = User.query.all()
	user_data = []
	for user in users:
		user_data.append({"name": user.name , "email":user.email , "age" : user.age})
	return jsonify({"User Details": user_data})

@app.route("/order", methods = ["POST"])
def order():
	data = request.get_json()
	order = Order(product = data.get("product") , price = data.get("price") , user_id = data.get("user_id"))
	db.session.add(order)
	db.session.commit()
	return "Order created successfully !!"

@app.route("/orders", methods=["GET"])
def get_orders():
	orders = Order.query.all()
	order_data = []
	for order in orders:
		order_data.append({"product": order.product , "price": order.price, "user_id":order.user_id})
	return jsonify({"Order Details":order_data})

# Below method important
# Get order by user id
@app.route("/user/<int:user_id>/orders" ,  methods=["GET"])
def get_orders_by_users(user_id):
	user = db.get_or_404(User, user_id)
	orders = user.orders
	order_data = []
	for order in orders:
		order_data.append({"id":order.id, "product":order.product , "price":order.price, "user_id":order.user_id})
	return jsonify({"user":user.name , "Order details":order_data})

# filter method
@app.route("/users/filter", methods=["GET"])
def filter_users():
	age = request.args.get("age")         
	# Filter conditions  filter by age

	#users = User.query.filter(User.age > age).all()
	#users = User.query.filter(User.age > age, User.name=="sonal").all()  # for multiple and condition
	
	# like conditions

	#users = User.query.filter(User.name.like("%h")).all() # for like condition endswith h
	#users = User.query.filter(User.name.like("s%")).all()  # like condition startswith s
	#users = User.query.filter(User.email.like("%gmail.com%")).all() # filter on gmail.com in between email string
	
	# Orderby conditions
	#users = User.query.order_by(User.age.desc()).all()  # descending age
	#users = User.query.order_by(User.age.asc()).all()    # ascending age

	# filter and order by condition
	users =  User.query.filter(User.age >25).order_by(User.age.desc()).all()

	users_data = []
	for user in users:
		users_data.append({'id':user.id,'name':user.name,'email':user.email,'age':user.age})
	return jsonify(users_data)

# join of two table
# Get users with orders details
@app.route("/users/orders", methods = ["GET"])
def get_users_orders():
	result = db.session.query(
		User.name,
		Order.product,
		Order.price
	).join(
		Order,
		User.id == Order.user_id
	) 
	details = []
	for name ,  product, amount in result:
		details.append({"name":name , "product":product , "price":amount})
	return jsonify(details)

# below code for pagination
@app.route("/users_page", methods=["GET"])
def get_users_per_page():
	page = request.args.get('page',1,type=int)
	per_page = request.args.get('per_page',2, type=int)
	pagination = User.query.paginate(page=page, per_page=per_page)
	users = pagination.items
	data = []
	for user in users:
		data.append({"id":user.id, "name":user.name,"email":user.email, "age":user.age})
	return jsonify({
		"Total Page":pagination.total,
		"Pages":pagination.pages,
		"Page": pagination.page,
		"Per Page":pagination.per_page,
		"users":data})

if __name__ =="__main__":
	with app.app_context():
		db.create_all()
	app.run(debug = True)