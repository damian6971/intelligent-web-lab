from flask import Flask, jsonify, request

app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "nazwa": "Klawiatura mechaniczna", "kategoria": "akcesoria", "cena": 349.99, "opis": "Przełączniki hot-swap, podświetlenie RGB"},
    {"id": 2, "nazwa": "Mysz bezprzewodowa", "kategoria": "akcesoria", "cena": 129.00, "opis": "Ciche przyciski, 4000 DPI"},
    {"id": 3, "nazwa": "Monitor 27 cali", "kategoria": "monitory", "cena": 1099.00, "opis": "Matryca IPS, 144 Hz"},
    {"id": 4, "nazwa": "Słuchawki nauszne", "kategoria": "audio", "cena": 449.00, "opis": "ANC, 40 h pracy na baterii"},
    {"id": 5, "nazwa": "Hub USB-C", "kategoria": "akcesoria", "cena": 199.00, "opis": "HDMI, 3x USB-A, czytnik SD"},
]

@app.route("/api/health")
def health():
    return jsonify({"status": "ok"})

@app.route("/api/products")
def products():
    if "max_price" in request.args:
        if not request.args["max_price"].isdigit():
            return jsonify({"error": "Invalid price parameter"}), 400
        filtered = [p for p in PRODUCTS if p["cena"] <= int(request.args["max_price"])]
        return jsonify(filtered)
    return jsonify(PRODUCTS)

@app.route("/api/products/<int:product_id>")
def product(product_id):
    for product in PRODUCTS:
        if product["id"] == product_id:
            return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.post("/api/products")
def add_product():
    data = request.get_json(silent=True)

    if not isinstance(data, dict) or not {"nazwa", "kategoria", "cena", "opis"} <= data.keys():
        return jsonify({"error": "Oczekiwano obiektu JSON z polami nazwa, kategoria, cena, opis."}), 400

    if "id" in data:
        return jsonify({"error": "Pole 'id' jest generowane automatycznie przez serwer."}), 400

    if any(not isinstance(data[key], str) or not data[key].strip() for key in ("nazwa", "kategoria", "opis")):
        return jsonify({"error": "Pola tekstowe muszą być niepustymi napisami."}), 400

    price = data["cena"]
    if type(price) not in (int, float) or price < 0 or price != price or price == float("inf"):
        return jsonify({"error": "Pole 'cena' musi być skończoną liczbą nieujemną."}), 400

    new_id = max((p["id"] for p in PRODUCTS), default=0) + 1
    new_product = {key: data[key].strip() if isinstance(data[key], str) else data[key] for key in
                   ("nazwa", "kategoria", "cena", "opis")}
    new_product["id"] = new_id

    PRODUCTS.append(new_product)
    return jsonify(new_product), 201

if __name__ == "__main__":
    app.run(debug=True)