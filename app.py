from flask import Flask, render_template,request, redirect , url_for, flash, session
import os

from products.routes import product_bp
from users.routes import user_bp
app = Flask(__name__)

# Register blueprints 
app.register_blueprint(product_bp)
app.register_blueprint(user_bp)

@app.route("/")
def home():
	return "Home Page"


if __name__ == "__main__":
	app.run(debug = True)