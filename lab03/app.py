from flask import Flask, jsonify, request
from recommender import matrix, recommend

app = Flask(__name__)
app.json.compact = False
app.json.sort_keys = False   

@app.route("/api/recommend")
def api_recommend():
    user = request.args.get("user", "").strip()
    if not user:
        return jsonify({"error": "podaj parametr ?user=..."}), 400
    k = 3
    if "k" in request.args:
        try:
            k = int(request.args["k"])
        except ValueError:
            k = 0
        if not 1 <= k <= len(matrix.index) - 1:
            return jsonify({"error": "k musi byc liczba calkowita z zakresu 1-%d" % (len(matrix.index) - 1)}), 400
    recs = recommend(user, k=k)
    if recs is None:
        return jsonify({"error": "nie znam takiego uzytkownika",
                        "known_users": sorted(matrix.index.tolist())}), 404
    return jsonify({"user": user, "k": k, "count": len(recs), "recommendations": recs})

@app.route("/api/users")
def api_users():
    return jsonify({"users": sorted(matrix.index.tolist())})

if __name__ == "__main__":
    app.run(debug=True)