from flask import Blueprint
product_bp = Blueprint("products",__name__)

@product_bp.route("/products")
def products():
	return "Product Page"