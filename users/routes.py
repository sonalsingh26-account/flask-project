from flask import Blueprint
user_bp = Blueprint("users",
					__name__,
					url_prefix="/users")

@user_bp.route("/")
def users():
	return "User Page"

@user_bp.route("/profile")
def profile():
	return "Profile Page"