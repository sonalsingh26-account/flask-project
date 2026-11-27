from flask import Flask ,  request,  jsonify
from pymongo import MongoClient
from bson import ObjectId
import re

app = Flask(__name__)

client = MongoClient("mongodb://localhost:27017")
client.admin.command("ping")  # coommand to check mongo db connected successfully
print("Mongo Db connected successfully")
db = client["flask_db"]
users_collection = db["users"]

@app.route("/")
def home():
    return "welcome flask Mongo tutorial!!"
# CRUD Operation
@app.route("/add", methods=["POST"])
def create_user():
    data = request.get_json()
    result = users_collection.insert_one(data)
    return jsonify({"message":"User created successfully",
                    "id" : str(result.inserted_id)}), 201

@app.route("/add/bulk", methods = ["POST"])
def create_user_bulk():
    data = request.get_json()
    result= users_collection.insert_many(data)
    ids = [str(user_id) for user_id in result.inserted_ids]
    return jsonify({"Message":"Bulk users created successfully!!",
                    "ids":ids
                    }) , 201

@app.route("/users", methods= ["GET"])
def get_users():
    users = users_collection.find()
    user_data =[]
    for user in users:
        user_data.append({
            "id" : str(user["_id"]),
            "name":user["name"],
            "age": user["age"],
            "email":user["email"],
            "city": user["city"]
            })
    return jsonify(user_data), 200

@app.route("/user/one", methods=["GET"])
def get_one_user():
    user = users_collection.find_one()
    if user is None:
        return jsonify({"message":"user is not found"}) , 404
    return jsonify({
        "id" : str(user["_id"]),
        "name" : user["name"],
        "email" : user["email"],
        "age" : user["age"]
    }), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_user(user_id):
    user= users_collection.find_one({
        "_id":ObjectId(user_id)
    })
    if user is None:
        return jsonify({"message":"User not found for given user id"}),404
    return jsonify({"id":str(user["_id"]),
                    "name":user["name"],
                    "age":user["age"],
                    "email":user["email"]
                    }),200
@app.route("/user/<user_id>", methods=["PUT"])
def update_one_user(user_id):
    user_id =  ObjectId(user_id)
    data = request.get_json()
    result = users_collection.update_one(
        {"_id" : user_id},
        {
            "$set":{
                "name": data.get("name"),
                "age": data.get("age"),
                "email":data.get("email")
                    }
        }
        )
    if result.matched_count==0:
        return jsonify({"message":"user not found"}),404
    return jsonify({
        "message":"user updated successfully!!"
    })
@app.route("/user/partial/all",methods=["PATCH"])
def update_all_users_partial():
    result = users_collection.update_many(
        {},
        {"$set": {"city": "Delhi"}}
    )
    if result.matched_count == 0:
        return jsonify({"message":"user is not found"}),404
    return jsonify({"message":"user updated successfully"})

#Partial update using Patch
@app.route("/user/partial/<user_id>", methods=["PATCH"])
def partial_update_one_user(user_id):
    user_id = ObjectId(user_id)
    data = request.get_json()
    update_data = {}
    if "name" in data:
        update_data["name"] = data["name"]
    if "email" in data:
        update_data["email"] = data["email"]
    if "age" in data:
        update_data["age"] = data["age"]   
    if "city" in data:
        update_data["city"] = data["city"]   
    result = users_collection.update_one(
        {"_id":user_id},
        {
            "$set":update_data
            
        })
    if result.matched_count ==0:
        return jsonify({"message":"user is not found"}),404
    return jsonify({"message":"user updated successfully!!"}), 200

@app.route("/user/<user_id>",methods=["DELETE"])
def delete_user(user_id):
    result = users_collection.delete_one(
        {"_id":ObjectId(user_id)})
    if result.deleted_count ==0:
        return jsonify({"message":"user not found"}),404
    return jsonify({"message":"user deleted successfully"}),200

@app.route("/user/search", methods=["GET"])
def search_user():
    city = request.args.get("city", "").strip()
    if not city:
        return jsonify({"message": "City query parameter is required"}), 400

    users = users_collection.find({
        #"city": city
        #"age": {"$gte": 41},
        #"age" : {"$gte": 41},
        #"city" :{"$in":["Delhi"]}
        #"city" :{"$nin":["Delhi"]}
        #"$and":[{"age": {"$gte": 38}}, {"name": "sonal"}]
        #"phone":{"$exists":True}
        "name":{"$regex":"so","$options":"i"}

    })
    user_data = []
    for user in users:
        user_data.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "age": user["age"],
            "email": user["email"],
            "city": user["city"]
        })
    if not user_data:
        return jsonify({"message": "No users found for the given city"}), 404
    return jsonify(user_data), 200
if __name__=="__main__":
    app.run(debug=True)