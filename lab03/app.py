from flask import Flask, jsonify, request
from recommender import matrix, recommend

app = Flask(__name__)

@app.route("/api/recommend")
def api_recommend():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400
    recs = recommend(user)
    if recs is None:
        return jsonify({"error": "nie znam takiego uzytkownika",
                        "known_users": sorted(matrix.index.tolist())}), 404
    return jsonify({"user": user, "count": len(recs), "recommendations": recs})

@app.route("/api/users")
def api_users():
    return jsonify({"users": sorted(matrix.index.tolist())})

if __name__ == "__main__":
    app.run(debug=True)