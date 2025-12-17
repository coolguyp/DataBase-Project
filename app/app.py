from flask import Flask, request, jsonify
from db import get_db
from auth import generate_token, verify_token
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)
db = get_db()

@app.route("/user", methods=["POST"])
def create_user():
    data = request.json
    user = {"name": data["name"], "email": data["email"], "created_at": datetime.now()}
    res = db.users.insert_one(user)
    return jsonify({"user_id": str(res.inserted_id)})

@app.route("/login", methods=["POST"])
def login():
    user = db.users.find_one({"email": request.json["email"]})
    if not user:
        return jsonify({"error": "User not found"}), 404
    token = generate_token(user["_id"])
    return jsonify({"token": token})

@app.route("/transaction", methods=["POST"])
def transaction():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    verify_token(token)

    data = request.json
    db.transactions.insert_one({
        "user_id": ObjectId(data["user_id"]),
        "product": data["product"],
        "amount": data["amount"],
        "timestamp": datetime.now()
    })
    return jsonify({"message": "Transaction stored"})

@app.route("/analytics")
def analytics():
    token = request.headers.get("Authorization").replace("Bearer ", "")
    verify_token(token)

    pipeline = [{"$group": {"_id": "$product", "total": {"$sum": "$amount"}}}]
    return jsonify(list(db.transactions.aggregate(pipeline)))

@app.route("/")
def health():
    return "Enterprise Big Data System Running"

app.run(host="0.0.0.0", port=5000)
