## 📦 Building a Docker Image

```bash
docker build -t fastapi-app .
docker build -t <custom name> .
# docker build → builds a Docker image from a Dockerfile
# -t fastapi-app → tag (name) for the image
# . → build context (current directory)
```
* Docker looks for a file named `Dockerfile` in the build context
* The **build context (`.`)** is sent to Docker (files available for COPY)
* Each instruction in the Dockerfile creates a **layer**

🟡 **Important**
Only files inside the build context can be copied into the image.

---

## 🏷️ Image Naming (Tags)

```bash
docker build -t fastapi-app:latest .
```

* `fastapi-app` → image name
* `latest` → tag (version label)

If no tag is provided, Docker automatically uses `latest`.

---

## 📋 List Docker Images

```bash
docker images
# Shows all locally available images
```
---

## 🚀 Running a Container from the Image

```bash
docker run -p 8000:8000 fastapi-app
# docker run → creates and starts a new container
# -p 8000:8000 → port mapping (host:container)
# fastapi-app → image name
```

### 🔍 Port Mapping Explained

* Left side (`8000`) → port on your computer
* Right side (`8000`) → port inside the container
* Requests to `localhost:8000` go into the container

---

## 🧱 Run in Detached Mode (Background)

```bash
docker run -d -p 8000:8000 --name fastapi-container fastapi-app
# -d → detached (runs in background)
# --name fastapi-container → assign a container name
```

🟡 Detached containers keep running even after you close the terminal.

---

## 📜 List Running Containers

```bash
docker ps
# Shows running containers only
```

```bash
docker ps -a
# Shows all containers (running + stopped)
```

---

## ⏹️ Stop a Running Container

```bash
docker stop fastapi-container
# Gracefully stops the container
```

---

## ▶️ Start a Stopped Container

```bash
docker start fastapi-container
# Starts an existing stopped container
```

🟡 **Note**
`docker start` does NOT re-run the image build.
It only starts an already created container.

---

## 🖥️ Execute a Command Inside a Running Container

```bash
docker exec -it fastapi-container bash
# -i → keep STDIN open
# -t → allocate terminal
# bash → open shell inside container
```

### 🔍 Flags Explained

* `-i` → allows typing input
* `-t` → provides a normal terminal interface
* `-it` → fully interactive shell

🟡 **Important**

* Containers do **not** remember interactive shells
* Every `docker exec -it ... bash` opens a **new shell session**
* When you exit, the container keeps running

---

## 🧹 Remove Containers

```bash
docker rm fastapi-container
# Removes a stopped container
```

```bash
docker rm -f fastapi-container
# Force remove (even if running)
```

---

## 🧼 Remove Images

```bash
docker rmi fastapi-app
# Deletes the image
```

🟡 You must remove dependent containers first.

---

## 🧠 Common Build Flow (Mental Model)

1. `docker build` → creates an **image**
2. `docker run` → creates + starts a **container**
3. `docker start` → restarts an existing container
4. `docker exec` → enter a running container
5. `docker stop` → stop execution
6. `docker rm` → delete container
7. `docker rmi` → delete image

---
                             

