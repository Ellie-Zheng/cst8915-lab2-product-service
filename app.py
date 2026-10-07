"""Product catalog API for the Algonquin Pet Store."""

import os

from flask import Flask, jsonify


app = Flask(__name__)

PRODUCTS = [
    {"id": 1, "name": "Dog Food", "price": 19.99},
    {"id": 2, "name": "Cat Food", "price": 34.99},
    {"id": 3, "name": "Bird Seeds", "price": 10.99},
]


@app.get("/products")
def get_products():
    response = jsonify(PRODUCTS)
    # The Store Front is hosted on a separate origin.
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


if __name__ == "__main__":
    # Azure App Service imports app:app and chooses its own listening port.
    # This server and PORT setting are for running the service locally.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3030")))
