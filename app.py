"""Lab 3 Python version of the Lab 2 Rust Product Service.

The public API and its three products stay the same; only the implementation
and the Azure hosting platform change.
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv


# Lab 2 used Rust's dotenv() for a local .env file. This is the Python equivalent.
# load_dotenv() does not replace variables already set in the shell or Azure.
load_dotenv()

app = Flask(__name__)

# Replaces Lab 2's Warp CORS filter. The Store Front is hosted separately,
# so its browser requests need permission to read this service's response.
CORS(app)

# Keep the exact Lab 2 catalog: the data is still in code, not a database.
PRODUCTS = [
    {"id": 1, "name": "Dog Food", "price": 19.99},
    {"id": 2, "name": "Cat Food", "price": 34.99},
    {"id": 3, "name": "Bird Seeds", "price": 10.99},
]


# Replaces the Warp GET /products route. The URL and HTTP method stay the same.
@app.get("/products")
def get_products():
    # Flask's jsonify replaces Rust's serde_json response for the same data.
    return jsonify(PRODUCTS)


if __name__ == "__main__":
    # Like Lab 2, local runs use PORT from the environment or default to 3030.
    # Azure App Service imports app:app and starts it with its own Gunicorn
    # server, so this block is used only by `python app.py` on your computer.
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "3030")))
