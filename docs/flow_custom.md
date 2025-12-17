```markdown
# FastAPI + Docker Execution Checklist (Git Bash, Step-by-step with Tests)

This guide shows how to build and run the FastAPI Items API in Docker on Windows using **Git Bash**, with a JSON file database stored either in a **Docker volume** or in a **host bind mount**.

Names we use:

- Project root: `C:/Users/a0527/שולחן העבודה/docker_proj/test`
- Docker image: `items-api-image`
- Docker tag: `v1`
- Docker container: `items-api-container`
- Docker volume: `items-db-volume`
- Data path inside container: `/app/data`
- Local data folder: `C:/Users/a0527/שולחן העבודה/docker_proj/test/data`

All commands below are for **Git Bash** and include a quick **test command after each step** so you can verify it worked.

---

## 1️⃣ Build Docker image

**Command:**

```bash
cd "/c/Users/a0527/שולחן העבודה/docker_proj/test"

docker build -t items-api-image:v1 .
```

**Test it: list images and grep ours**

```bash
docker images | grep items-api-image
```

You should see a line with `items-api-image   v1`.

---

## 2️⃣ Option A – Use a Docker volume for the database

### 2.1 Create the volume

**Command:**

```bash
docker volume create items-db-volume
```

**Test it:**

```bash
docker volume ls | grep items-db-volume
```

You should see `items-db-volume` in the list.

---

### 2.2 Initialize `db.json` inside the volume (one time)

**Command:**

```bash
docker run -it -v items-db-volume:/data alpine sh
```

Inside the Alpine shell:

```sh
mkdir -p /data
echo "{}" > /data/db.json
ls -l /data
cat /data/db.json
exit
```

**Test it (from Git Bash again):**

```bash
docker run --rm -v items-db-volume:/data alpine ls -l /data
docker run --rm -v items-db-volume:/data alpine cat /data/db.json
```

You should see `db.json` listed and its contents `{}` printed.

---

### 2.3 Run the FastAPI container with the volume

**Command:**

```bash
docker stop items-api-container 2>/dev/null || true
docker rm items-api-container 2>/dev/null || true

docker run -d -p 8000:8000 \
  --name items-api-container \
  -v items-db-volume:/app/data \
  items-api-image:v1
```

**Test it:**

```bash
docker ps | grep items-api-container
docker logs items-api-container
```

- `docker ps` should show `items-api-container` in `Up` state.
- `docker logs` should not show errors about missing `data/db.json`.

Then open in browser:

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/health`

---

## 3️⃣ Option B – Use a host bind mount for the database

This uses your real local folder:

`C:/Users/a0527/שולחן העבודה/docker_proj/test/data`

### 3.1 Ensure local `db.json` exists

**Command:**

```bash
cd "/c/Users/a0527/שולחן העבודה/docker_proj/test"

mkdir -p data
echo "{}" > data/db.json
```

**Test it:**

```bash
ls data
cat data/db.json
```

You should see `db.json` and `{}`.

---

### 3.2 Run the FastAPI container with a bind mount

**Command:**

```bash
docker stop items-api-container 2>/dev/null || true
docker rm items-api-container 2>/dev/null || true

docker run -d -p 8000:8000 \
  --name items-api-container \
  -v "C:\Users\a0527\שולחן העבודה\docker_proj\test\arc:/app/data" \
  items-api-image:v1
```

**Test it:**

```bash
docker ps | grep items-api-container
docker logs items-api-container
```

- `docker ps` should show `items-api-container` running.
- `docker logs` should not show a `FileNotFoundError` for `data/db.json`.

Then in your browser check:

- `http://localhost:8000/`
- `http://localhost:8000/docs`
- `http://localhost:8000/health`

---

## 4️⃣ Common issues and quick checks

- **Image not found**  
  Run `docker images | grep items-api-image`.  
  If empty, rebuild:  
  ```bash
  cd "/c/Users/a0527/שולחן העבודה/docker_proj/test"
  docker build -t items-api-image:v1 .
  ```

- **Container already exists / name in use**  
  ```bash
  docker stop items-api-container 2>/dev/null || true
  docker rm items-api-container 2>/dev/null || true
  ```

- **Missing `db.json` inside container**  
  - Volume option: redo step **2.2** (Alpine init).
  - Bind mount option: redo step **3.1** to ensure `data/db.json` exists on host.

```

To continue together:

1. Run the **build step** (section 1) and its **test command**, paste any errors if there are any.
2. Choose: do you want to proceed with **Option A (volume)** or **Option B (bind mount)** first?