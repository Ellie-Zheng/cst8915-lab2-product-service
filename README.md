# Product Service (Lab 3: Python)

Lab 3 rewrites the Lab 2 Rust/Warp Product Service in Python/Flask so it can run on Azure App Service. The Store Front still calls `GET /products` and receives the same three products. Only the implementation and hosting change. The original Rust version remains available through this repository's `lab2-final` tag.

## How Lab 2 behavior carries into Lab 3

| Lab 2 (Rust) | Lab 3 (Python) | What stays the same |
| --- | --- | --- |
| `warp::path("products")` | Flask `@app.get("/products")` | The Store Front requests `GET /products`. |
| Three product objects in `src/main.rs` | The `PRODUCTS` list in `app.py` | IDs, names, prices, and in-code storage. There is still no product database. |
| `serde_json::json!` and Warp's JSON reply | Flask `jsonify(PRODUCTS)` | The response is a JSON array with the same product data. |
| Warp CORS filter with `allow_any_origin()` | `flask-cors` with `CORS(app)` | A Store Front hosted at another origin can read the response. |
| Rust `dotenv().ok()` and `env::var("PORT")` | `python-dotenv` `load_dotenv()` and `os.environ.get("PORT")` | An optional local `.env` can supply `PORT`; an existing environment variable takes precedence; the local default is `3030`. |
| `Cargo.toml` / `Cargo.lock` and Cargo build output | `requirements.txt` and a local `.venv` | Dependencies are declared for this service and installed separately from other projects. |

The Product Service still does **not** connect to RabbitMQ. That backing service is used by the separate Order Service. The `0.0.0.0` bind address remains for local runs; on Azure, App Service imports the Flask `app` object and starts its own server.

## API

`GET /products` returns a JSON array:

```json
[
  {"id": 1, "name": "Dog Food", "price": 19.99},
  {"id": 2, "name": "Cat Food", "price": 34.99},
  {"id": 3, "name": "Bird Seeds", "price": 10.99}
]
```

`flask-cors` permits cross-origin requests so the separately hosted Store Front can read the response. With the example `Origin` header in the test below, it returns that origin in `Access-Control-Allow-Origin`.

## Run and test locally on Windows (PowerShell)

Install Python 3 and make sure the `py` launcher works. In the repository root, run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe app.py
```

Keep that terminal open. In another terminal, test:

```powershell
curl.exe -i http://127.0.0.1:3030/products
curl.exe -i -H "Origin: http://localhost:8080" http://127.0.0.1:3030/products
```

Both requests should return HTTP `200` and the three products. The second should also include `Access-Control-Allow-Origin: http://localhost:8080`. You can also open `http://127.0.0.1:3030/products` in your browser or run `test-product-service.http` with the VS Code REST Client extension. Press `Ctrl+C` in the first terminal to stop the service.

These commands use the project's virtual environment directly, so PowerShell script activation is not required.

## Run locally on Linux or macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Test with `curl -i http://127.0.0.1:3030/products`.

## Configuration and Azure App Service

`PORT` is optional for local execution and defaults to `3030`. As in Lab 2, you can set it in the shell (for example, `$env:PORT = "3031"` in PowerShell) or create a local `.env` in this repository's root containing `PORT=3031`. `python-dotenv` loads `.env` when present; an existing shell or Azure environment variable takes precedence. Restart the local server after changing `PORT`. `.env` is ignored by Git and must not be committed.

For Lab 3, create a **Linux** Azure App Service with a Python runtime and deploy this repository. Keep `app.py` and `requirements.txt` at the repository root. App Service detects the Flask object named `app` and starts it with Gunicorn; the `if __name__ == "__main__"` block and local `PORT=3030` are for `python app.py` on your computer. Do not upload the local `.env`: Azure configuration belongs in App Service environment variables. Copy the app's actual default URL from Azure Portal and add `/products` to test the deployed endpoint.

## Instructor reference

This rewrite follows the Python/Flask approach in Professor Ramy Mohamed's [Lab 3 Product Service reference repository](https://github.com/ramymohamed10/product-service-L3P), especially its [app.py](https://github.com/ramymohamed10/product-service-L3P/blob/main/app.py) and [requirements.txt](https://github.com/ramymohamed10/product-service-L3P/blob/main/requirements.txt). The code here keeps this student's Lab 2 catalog and API behavior while documenting the Rust-to-Python mapping above.
