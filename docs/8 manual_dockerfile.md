This lab exercises a clear **separation of concerns** with the following goals:
* ✅ Python dependency resolution happens **locally first**
* ✅ `requirements.txt` is **derived**, not magic
* ✅ Docker does **not** replace Python fundamentals
* ✅ Order matters: **deps → install → app**

Below is a **single, complete Markdown file**, mentor-tone, CLI-first, with:

* Local `.venv`
* `pip install` locally
* `pip freeze → requirements.txt`
* Copy **requirements first**
* Install deps **inside container** with `--break-system-packages`
* Copy `main.py` **only after**
* Explicit `/app` creation
* Clear emphasis blocks you can color later

You can copy-paste this whole file.

---

````md
# 🐳 Building a FastAPI Image Manually — The Right Way (CLI Only)

> 👋 Hi.  
> In this lab, I want you to slow down and **think like an engineer**, not like a tutorial follower.

We will:
- work with Python **locally first**
- then move **only what is necessary** into Docker
- and only at the end understand why Dockerfile exists

🚫 No Dockerfile  
🚫 No Docker Compose  
✅ Full understanding

---

## 🎯 Learning Goals

By the end of this lab, you should be able to explain:

- Why dependencies are resolved **locally first**
- What `requirements.txt` really represents
- Why Docker does not read your Python environment
- Why dependency layers should be built **before** app code
- Why Dockerfile instruction order matters

---

## ⚠️ Ground Rules

- Commands are always marked as:
  - **HOST**
  - **CONTAINER**
- Do not skip steps
- If something exists somewhere — **you created it**

---

## 🧠 Core Mental Model (Read This Carefully)

> Docker does not care about your Python, your venv, or your project  
> unless you explicitly give it files.

---

## 0️⃣ Create Project Folder (HOST)

````batch
mkdir fastapi-manual-lab
cd fastapi-manual-lab
cd
dir -la
ls -la
````

Expected:

```text
.
..
```

> 🔵 Empty folder. Nothing exists yet.

---

## 1️⃣ Create and Activate Local Virtual Environment (HOST)

> 🎯 This step is **intentional**.
> Docker will NOT use this venv — *you* are using it.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Verify:

```bash
which python
```

> 🟢 This Python runs on **your machine**, not in Docker.

---

## 2️⃣ Create the FastAPI App Locally (HOST)

Create `main.py`:

```bash
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello from inside the container"}
```

Verify:

```bash
ls -la
```

---

## 3️⃣ Install Dependencies Locally (HOST)

> You must understand what your app needs **before Docker exists**.

```bash
pip install fastapi uvicorn
```

Verify:

```bash
python -c "import fastapi; print(fastapi.__version__)"
```

> 🧠 Important:
> Docker does NOT see this installation.

---

## 4️⃣ Generate `requirements.txt` from Reality (HOST)

> This file describes **what your app actually needs**, not what you guess.

```bash
pip freeze > requirements.txt
```

Inspect it:

```bash
cat requirements.txt
```

> 🟡 This file is now the **contract** between your app and Docker.

---

## 5️⃣ Run a Bare Container (HOST)

> Now we enter Docker’s isolated world.

```bash
docker run -it --name fastapi-manual -p 8000:8000 alpine sh
```

You are now **INSIDE the container**.

---

## 6️⃣ Prove Nothing Exists Inside the Container (CONTAINER)

```bash
python3 --version
ls /app
```

Expected:

* Python not found
* `/app` does not exist

> 🔴 Docker sees **nothing** from your host by default.

---

## 7️⃣ Install Python Inside the Container (CONTAINER)

```bash
apk update
apk add python3 py3-pip
```

Verify:

```bash
python3 --version
pip3 --version
```

> 🧠 This affects **only this container**.

---

## 8️⃣ Create `/app` Explicitly (CONTAINER)

```bash
mkdir /app
ls /
```

> 🔵 `/app` exists only because **you created it**.

---

## 9️⃣ Copy `requirements.txt` FIRST (HOST)

> ⚠️ This order is **intentional**.

From a **new terminal tab**:

```bash
docker cp requirements.txt fastapi-manual:/app/requirements.txt
```

Verify inside container:

```bash
ls /app
```

Expected:

```text
requirements.txt
```

> 🧠 We install dependencies **before** copying app code.

---

## 🔟 Install Dependencies Inside the Container (CONTAINER)

⚠️ **IMPORTANT — REQUIRED FLAG**

```bash
pip3 install -r /app/requirements.txt --break-system-packages
```

Why?

> Alpine Linux protects system Python.
> Inside containers, this flag is expected and safe.

Verify:

```bash
python3 -c "import fastapi; print(fastapi.__version__)"
```

---

## 1️⃣1️⃣ Copy `main.py` LAST (HOST)

```bash
docker cp main.py fastapi-manual:/app/main.py
```

Verify:

```bash
ls /app
```

Expected:

```text
requirements.txt
main.py
```

> 🟢 This mirrors best-practice Dockerfile layering.

---

## 1️⃣2️⃣ Run FastAPI (CONTAINER)

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Open browser (HOST):

```
http://localhost:8000
```

Expected:

```json
{"message":"Hello from inside the container"}
```

Stop server:

```text
Ctrl + C
```

---

## 1️⃣3️⃣ Inspect Container Changes (HOST — CRITICAL)

```bash
docker diff fastapi-manual
```

Look for:

* Installed packages
* `/app`
* Python binaries

> 🧠 These are **filesystem changes**, not an image yet.

---

## 1️⃣4️⃣ Freeze the Container into an Image (HOST)

```bash
docker commit fastapi-manual fastapi-img:manual
```

Remove container:

```bash
docker rm fastapi-manual
```

---

## 1️⃣5️⃣ Prove the Image Works Alone (HOST)

```bash
docker run -it --rm -p 8000:8000 fastapi-img:manual sh
```

Inside:

```bash
ls /app
uvicorn main:app --host 0.0.0.0 --port 8000
```

> 🔥 This container never saw your venv
> Everything came from the image

---

## 🧠 Mentor Summary (This Is the Lesson)

* You resolved dependencies **locally**
* You froze them into `requirements.txt`
* You copied dependencies **before** code
* You installed inside Docker **explicitly**
* You created an image **on purpose**

### This sentence matters:

> **Dockerfile exists to automate this exact flow.**

---

## 🧪 Reflection (Answer Out Loud)

1. Why didn’t Docker use your `.venv`?
2. Why copy `requirements.txt` before `main.py`?
3. What would change if `main.py` changes?
4. What would change if dependencies change?
5. Why does Dockerfile layer order matter?

---

👣 **Next step**
We will now write a Dockerfile that does **exactly this**, line by line.

No magic.
Only understanding.

```
