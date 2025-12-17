# FastAPI Items API (Docker Example)

This project is a tiny FastAPI web API that manages "items" stored in a simple JSON file (`data/db.json`).  
It exposes basic CRUD endpoints to list, create, update, and delete items over HTTP.  
On startup, the app checks that `data/db.json` exists before serving requests.  
You can run it locally with `uvicorn main:app --reload` after creating `data/db.json`.  
You can also build a Docker image from the `Dockerfile` and run the API in a container with a mounted volume for `data/db.json`.  
Swagger UI is available at `http://localhost:8000/docs` when the app is running.