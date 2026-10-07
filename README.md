# Product Service

This Python/Flask service returns the same three products as the original Rust service. The Store Front calls `GET /products` to load its catalog. Product data is defined in `app.py`; this service does not connect to RabbitMQ.

## API

`GET /products` returns a JSON array:

```json
[
  {"id": 1, "name": "Dog Food", "price": 19.99},
  {"id": 2, "name": "Cat Food", "price": 34.99},
  {"id": 3, "name": "Bird Seeds", "price": 10.99}
]
```

The response permits cross-origin requests so the separately hosted Store Front can read it.

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

Both requests should return HTTP `200` and the three products. The second should also include `Access-Control-Allow-Origin: *`. You can also open `http://127.0.0.1:3030/products` in your browser or run `test-product-service.http` with the VS Code REST Client extension. Press `Ctrl+C` in the first terminal to stop the service.

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

`PORT` is optional for local execution and defaults to `3030`. Set it in the shell if needed; do not commit a real `.env` file. For example, in PowerShell: `$env:PORT = "3031"` before starting `app.py`.

For Lab 3, create a **Linux** Azure App Service with a Python runtime and deploy this repository. Keep `app.py` and `requirements.txt` at the repository root. App Service detects the Flask object named `app` and starts it with Gunicorn, so the local `python app.py` command and `PORT=3030` are not Azure startup settings. Test the deployed service at `https://<your-product-app>.azurewebsites.net/products`.
