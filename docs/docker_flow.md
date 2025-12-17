# **Full FastAPI + Docker Execution Checklist**

---

## **1️⃣ Create FastAPI project**

1. Make a project folder:

```bash
mkdir docker_volume_db_server
cd docker_volume_db_server
```

2. Create a virtual environment (optional for local dev):

```bash
python -m venv venv
source venv/Scripts/activate
python.exe -m pip install --upgrade pip
```

3. Install FastAPI and Uvicorn:

```bash
pip install fastapi uvicorn
```

4. Create `main.py` with your FastAPI app:

```python
from fastapi import FastAPI

app = FastAPI()

DB_PATH = "data/db.json"

def check_database_exists():
    import os
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError(f"Database file not found: {DB_PATH}")

@app.on_event("startup")
async def startup_event():
    check_database_exists()

@app.get("/")
def read_root():
    return {"message": "Hello World"}
```

---

## **2️⃣ Prepare the database file**

```bash
mkdir -p data
echo "{}" > data/db.json
```

* This creates the `data` folder and an empty JSON file for the database.


## **3️⃣ Create Dockerfile**

```dockerfile
# Dockerfile
# Use an official Python image
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# Copy requirement file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port FastAPI will listen on
EXPOSE 8000

# Start FastAPI with uvicorn
CMD ["python", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

```

* Make `requirements.txt`:

pip freeze > requirements.txt

---



  ░██████   ░██████████   ░███    ░█████████  ░██████████
 ░██   ░██      ░██      ░██░██   ░██     ░██     ░██    
░██             ░██     ░██  ░██  ░██     ░██     ░██    
 ░████████      ░██    ░█████████ ░█████████      ░██    
        ░██     ░██    ░██    ░██ ░██   ░██       ░██    
 ░██   ░██      ░██    ░██    ░██ ░██    ░██      ░██    
  ░██████       ░██    ░██    ░██ ░██     ░██     ░██    
                                                         



## **4️⃣ Build Docker image**

```bash
docker build -t fastapi-app:v1 .
```


## **5️⃣ Handle Docker volumes**

2. Create a volume if needed:

```bash
docker volume create first_lab
```
```bash
docker volume ls
```
3. Populate volume with `db.json` (if empty):
USING IMPORT
```bash
# TO MAKE MANUALLY
docker run -it -v first_lab:/data alpine sh
# mkdir -p /data
# echo "{}" > /data/db.json
ls -l /data  #Inside the container, list files in /data:
cat /data/db.json
exit
```

---

## **6️⃣ Run Docker container**

* First, remove any existing container with the same name:

```bash
docker stop fastapi-container
docker rm fastapi-container
```

* Then run the container with the volume:

```bash
docker run -d -p 8000:8000 --name fastapi-container -v first_lab:/app/data fastapi-app:v1

```
Run container with bind mount
docker run -d -p 8000:8000 \
  --name fastapi-container \
  -v "C:/Users/a0527/שולחן העבודה/docker_proj/day_2/docker_volume_db_server/archive:/app/data" \
  fastapi-app:v1
  
TEST
http://localhost:8000/docs
* Check logs (optional):

```bash
docker logs fastapi-container
```

---

## **7️⃣ Access the FastAPI app**

Open in browser or API client:

```
http://localhost:8000
```

You should see:

```json
{"message": "Hello World"}
```

---

## **8️⃣ Issues we faced & how we solved them**

| Issue                   | Cause                                           | Solution                                                        |
| ----------------------- | ----------------------------------------------- | --------------------------------------------------------------- |
| Container name conflict | Tried to run container with name already in use | `docker stop fastapi-container` + `docker rm fastapi-container` |
| Missing database file   | App couldn’t find `data/db.json`                | Created the file manually or populated Docker volume with it    |
| Volume not populated    | The volume existed but was empty                | Used temporary Alpine container to add `db.json`                |

---

✅ Following this checklist, you can **start from scratch**, build the FastAPI app, Dockerize it, attach a persistent database volume, and run the app successfully.

---

If you want, I can also create a **diagram showing the workflow from project → Docker → volume → running app**, which makes it super easy to visualize for future projects. Do you want me to do that?
