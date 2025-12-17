## Naming Summary Table

This table lists **every custom name** used in the exercises (containers, volumes, host folders, etc.) and **what each one is for**.  
Use it as a quick reference so you always know *what you are creating* and *why* when you run the commands.

| Kind         | Name                                 | What it is                          | Purpose / How it is used                                                                 |
|--------------|--------------------------------------|-------------------------------------|------------------------------------------------------------------------------------------|
| Container    | `bm1`                                | Container name                      | Main **bind mount** demo container; mounts your host folder into `/data` and is inspected. |
| Container    | `novol1`                             | Container name                      | First **no-volume** container; creates `/tmp/only-in-container.txt` to show data loss after removal. |
| Container    | `novol2`                             | Container name                      | Second **no-volume** container; proves `/tmp/only-in-container.txt` is gone after `novol1` is removed. |
| Container    | `vol1`                               | Container name                      | Container using Docker **volume** `myvol1` at `/data`; shows data persistence across container deletion. |
| Container    | `writer`                             | Container name                      | Writes to shared volume `sharedvol` at `/data` (creates `/data/shared.txt`).             |
| Container    | `reader`                             | Container name                      | Reads from the same shared volume `sharedvol` at `/data` to prove containers can share data. |
| Container    | `bm-wrong`                           | Container name                      | Container with a **wrong bind mount path**; shows what happens when you mount the wrong host directory. |
| Volume       | `myvol1`                             | Docker volume name                  | Single-container **persistent storage** example; holds `/data/persisted.txt` for `vol1`. |
| Volume       | `sharedvol`                          | Docker volume name                  | **Shared storage** example; used by both `writer` and `reader` to share `/data/shared.txt`. |
| Host folder  | `docker-volume-lab/bind-mount-demo`  | Directory on the host filesystem    | Host directory you bind mount into `/data` in `bm1`; shows that container writes appear directly on the host. |
| Image        | `alpine`                             | Docker image                        | Lightweight Linux image used as the base for all demo containers in the exercises.       |



```bash
pwd                             # Show current working directory
ls -la                          # List files (detailed)
cd /c/Users/YourName/projects   # Example: go to your project root
```

---

### 1. Bind Mount Basics (`bm1`)

```bash
mkdir -p docker-volume-lab/bind-mount-demo      # Create demo folder
cd docker-volume-lab/bind-mount-demo           # Enter demo folder
pwd                                             # Confirm where you are
ls -la                                          # Check contents
docker run -it --name bm1 -v "$(pwd)":/data alpine sh   # Start container with bind mount
# (inside container)
pwd                                             # Show current dir in container
ls -la /data                                    # List bind-mounted /data
echo "created-from-inside-container" > /data/hello-from-container.txt  # Create file
ls -la /data                                    # Confirm file in /data
cat /data/hello-from-container.txt             # Read file
exit                                            # Exit container
# (back on host, still in bind-mount-demo)
pwd                                             # Confirm still in demo folder
ls -la                                          # See the file on host
cat hello-from-container.txt                    # Read file from host
```

---

### 2. Inspect Bind Mount Container (`bm1`)

```bash
docker ps -a                                    # List all containers
docker inspect bm1                              # Full inspect of bm1
docker inspect bm1 --format '{{json .Mounts}}'  # Show only Mounts section (JSON)
```

---

### 3. Container Without Volume (Intentional Data Loss)

```bash
docker run -it --name novol1 alpine sh          # Start container with no mounts
# (inside container)
echo "this file lives only inside the container" > /tmp/only-in-container.txt  # Create temp file
ls -la /tmp                                     # List /tmp contents
cat /tmp/only-in-container.txt                  # Read file
exit                                            # Exit container
# (back on host)
docker rm novol1                                # Remove novol1 (and its filesystem)
docker run -it --name novol2 alpine sh          # Start fresh container
# (inside container)
ls -la /tmp                                     # Check /tmp
cat /tmp/only-in-container.txt                  # Try to read old file (should fail)
exit                                            # Exit container
```

---

### 4. Docker Volume Basics (`myvol1` / `vol1`)

```bash
docker volume create myvol1                     # Create Docker-managed volume
docker volume ls                                # List volumes
docker run -it --name vol1 -v myvol1:/data alpine sh   # Start container with volume at /data
# (inside container)
ls -la /data                                    # Check /data
echo "this should persist" > /data/persisted.txt   # Create persistent file
ls -la /data                                    # Confirm file exists
cat /data/persisted.txt                         # Read file
exit                                            # Exit container
# (back on host)
docker rm vol1                                  # Remove container, keep volume
docker run -it --name vol1 -v myvol1:/data alpine sh   # Start new container with same volume
# (inside container)
ls -la /data                                    # File should still be there
cat /data/persisted.txt                         # Confirm persistence
exit                                            # Exit container
```

---

### 5. Inspect Volume Mount (`vol1` / `myvol1`)

```bash
docker ps -a                                    # List containers
docker inspect vol1                             # Inspect container using volume
docker inspect vol1 --format '{{json .Mounts}}' # Show Mounts section only
```

---

### 6. One Volume, Two Containers (`sharedvol`, `writer`, `reader`)

```bash
docker volume create sharedvol                  # Create shared volume
docker volume ls                                # Confirm volume exists
docker run -it --name writer -v sharedvol:/data alpine sh   # Writer container
# (inside writer)
echo "hello from writer" > /data/shared.txt     # Create shared file
ls -la /data                                    # Confirm file exists
cat /data/shared.txt                            # Read file
exit                                            # Exit writer
# (back on host)
docker run -it --name reader -v sharedvol:/data alpine sh   # Reader container
# (inside reader)
ls -la /data                                    # See shared.txt
cat /data/shared.txt                            # Read content written by writer
exit                                            # Exit reader
```

---

### 7. Wrong Host Path Bind Mount (`bm-wrong`)

```bash
pwd                                             # Confirm you are in bind-mount-demo
ls -la                                          # See contents
cd ..                                           # Intentionally go one level up (wrong dir)
pwd                                             # Confirm wrong directory
ls -la                                          # List contents here
docker run -it --name bm-wrong -v "$(pwd)/data":/data alpine sh  # Bind mount wrong path
# (inside container)
ls -la /data                                    # /data is empty or unexpected
exit                                            # Exit container
```

---

### 8. Cleanup

```bash
docker ps -a                                    # See all containers
docker volume ls                                # See all volumes
docker rm -f bm1 novol2 writer reader bm-wrong vol1  # Force-remove demo containers
docker volume rm myvol1 sharedvol               # Remove demo volumes (if no longer needed)
```

---

## Refactored Lesson in Clean Markdown (Git Bash version)

# Docker Volumes — Deep Hands-On (Git Bash Edition)

This version assumes you are on **Windows** and running commands in **Git Bash**. Wherever you see `docker run` etc., run those commands from a Git Bash terminal.

---

## Learning Objectives

By the end of this notebook/file, you will be able to:

- Explain the difference between **container filesystem** and **external storage**.
- Describe what a **bind mount** is and where the data lives physically.
- Describe what a **Docker volume** is and where the data lives physically.
- Predict which data survives container deletion (and which does not).
- Use `docker inspect` and the `Mounts` section to prove your assumptions.

---

## Ground Rules

- You run **all Docker commands from your HOST Git Bash terminal**.
- When a command is meant to run **inside the container**, it will be clearly labeled.
- This is a **teaching-focused** document:
  - Docker commands are shown in Markdown code blocks.
  - Do **not** try to run Docker commands from Python; always use Git Bash.

---

## Naming Convention

We will use consistent names:

- Bind mount container: `bm1`
- “No volume” containers: `novol1`, `novol2`
- Volume name: `myvol1`
- Volume container: `vol1`
- Shared volume name: `sharedvol`
- Shared volume containers: `writer`, `reader`

---

## Exercise 1 — Bind Mount Basics: Where Does the File Live?

### 1) Objective

Understand that with a **bind mount**, Docker is pointing directly to a real folder on your **host filesystem**.

### 2) Host Preparation (Where am I?)

You are on the **HOST**, using **Git Bash**.

Create a dedicated folder and stand inside it.

```bash
mkdir -p docker-volume-lab/bind-mount-demo
cd docker-volume-lab/bind-mount-demo
pwd
ls -la
```

Key idea:

> `$(pwd)` means: **“the folder you are standing in RIGHT NOW”** in Git Bash.

### 3) Command to Run (HOST — Git Bash)

Start a container with a bind mount from your current host directory into `/data` inside the container:

```bash
docker run -it --name bm1 -v "$(pwd)":/data alpine sh
```

### 4) Command to Run (CONTAINER — inside `bm1`)

Now you are **inside** the `bm1` container shell:

```bash
pwd
ls -la /data
echo "created-from-inside-container" > /data/hello-from-container.txt
ls -la /data
cat /data/hello-from-container.txt
exit
```

### 5) Expected Output

Back on the **HOST** (in `docker-volume-lab/bind-mount-demo`), you should see:

```bash
pwd
ls -la
cat hello-from-container.txt
```

You should see the same `hello-from-container.txt` file both:

- Inside the container at `/data/hello-from-container.txt`.
- On the host in `docker-volume-lab/bind-mount-demo/hello-from-container.txt`.

### 6) Common Mistakes

- Running `docker run -v "$(pwd)":/data ...` from the **wrong directory**.
- Always run `pwd` right before using `$(pwd)` to confirm where you are.

### 7) Thinking Questions

- The container created a file. Why did it appear on the HOST?
- Did Docker “copy” the file to the host, or did it write directly into your filesystem?

---

## Exercise 2 — Inspect a Container with a Bind Mount (MANDATORY)

### 1) Objective

Visually understand how Docker represents a **bind mount** using `docker inspect`.

### 2) Command to Run (HOST — Git Bash)

Confirm that the container exists:

```bash
docker ps -a
```

Inspect the container and focus on `Mounts`:

```bash
docker inspect bm1
```

Optional shorter output:

```bash
docker inspect bm1 --format '{{json .Mounts}}'
```

### 3) Expected Output

In the `Mounts` section you should see something like:

```text
"Mounts": [
  {
    "Type": "bind",
    "Source": "/c/Users/YourName/.../docker-volume-lab/bind-mount-demo",
    "Destination": "/data",
    "Mode": "",
    "RW": true,
    "Propagation": "rprivate"
  }
]
```

Key points:

- `"Type": "bind"` — not a Docker-managed volume.
- `"Source"` — a **host path** (on Windows with Git Bash, usually `/c/...`).
- `"Destination"` — where that host folder appears in the container (`/data`).
- `"RW": true` — container can write into the mount.

Docker is *not* storing your data; it is **pointing at your host filesystem**.

---

## Exercise 3 — Container Without Volume (Intentional Data Loss)

### 1) Objective

Prove that files written only to the **container filesystem** disappear when the container is removed.

### 2) Command to Run (HOST — Git Bash)

Start a container **without** bind mounts or volumes:

```bash
docker run -it --name novol1 alpine sh
```

### 3) Command to Run (CONTAINER — inside `novol1`)

Create a file that exists only in the container filesystem:

```bash
echo "this file lives only inside the container" > /tmp/only-in-container.txt
ls -la /tmp
cat /tmp/only-in-container.txt
exit
```

Back on the host, remove the container:

```bash
docker rm novol1
```

Start a new container:

```bash
docker run -it --name novol2 alpine sh
```

Inside `novol2`, check for the file:

```bash
ls -la /tmp
cat /tmp/only-in-container.txt
exit
```

### 4) Expected Output

- In `novol2`, `/tmp/only-in-container.txt` is **gone**.
- `cat` should fail with *“No such file or directory”*.

### 5) Common Mistakes

- Confusing **stopped** container with **removed** container:
  - `exit` → container stopped, filesystem still exists.
  - `docker rm` → container removed, filesystem deleted.

### 6) Thinking Questions

- What exactly did we delete when running `docker rm novol1`?
- Why is this behavior okay for short-lived tasks but risky for databases?

---

## Exercise 4 — Docker Volume (Managed Persistence)

### 1) Objective

Create a Docker volume and show that data survives container deletion.

### 2) Command to Run (HOST — Git Bash)

Create a volume:

```bash
docker volume create myvol1
docker volume ls
```

Attach the volume at `/data`:

```bash
docker run -it --name vol1 -v myvol1:/data alpine sh
```

### 3) Command to Run (CONTAINER — inside `vol1`)

Write data into the mounted path:

```bash
ls -la /data
echo "this should persist" > /data/persisted.txt
ls -la /data
cat /data/persisted.txt
exit
```

Back on the host, remove the container:

```bash
docker rm vol1
```

Reattach the **same volume** to a new container named `vol1` (or another name):

```bash
docker run -it --name vol1 -v myvol1:/data alpine sh
```

Inside the container:

```bash
ls -la /data
cat /data/persisted.txt
exit
```

### 4) Expected Output

- `/data/persisted.txt` is still there after container deletion and recreation.
- The data is held by the **volume**, not by the container.

### 5) Common Mistakes

- Thinking the volume is deleted when the container is deleted.
- Docker volumes are separate objects; they persist until removed explicitly.

### 6) Thinking Questions

- What is the “thing” that holds the data now: the container or the volume?
- Why is this approach safer for production databases?

---

## Exercise 5 — Inspect a Container with a Docker Volume (MANDATORY)

### 1) Objective

Compare Docker volumes to bind mounts using `docker inspect`.

### 2) Command to Run (HOST — Git Bash)

Confirm container exists:

```bash
docker ps -a
```

Inspect `vol1`:

```bash
docker inspect vol1
docker inspect vol1 --format '{{json .Mounts}}'
```

### 3) Expected Output

The `Mounts` section should conceptually look like:

```text
"Mounts": [
  {
    "Type": "volume",
    "Name": "myvol1",
    "Source": "/var/lib/docker/volumes/myvol1/_data",
    "Destination": "/data",
    "Driver": "local",
    "Mode": "z",
    "RW": true,
    "Propagation": ""
  }
]
```

On Docker Desktop (Windows), the actual internal path may differ, but importantly:

- `"Type": "volume"`
- `"Name": "myvol1"`
- `"Source"` is a Docker-managed internal path.
- `"Destination": "/data"`

**Comparison:**

| Feature          | Bind Mount                   | Docker Volume                   |
|-----------------|------------------------------|---------------------------------|
| Type            | `bind`                       | `volume`                        |
| Source          | Host filesystem path         | Docker-managed internal path    |
| Who manages it? | You (paths, permissions)     | Docker                          |
| Portability     | Low (absolute host paths)    | High (Docker object by name)    |
| Typical usage   | Local dev, special cases     | Production data, DBs, services  |

---

## Exercise 6 — One Volume, Two Containers

### 1) Objective

Show that multiple containers can share the same volume.

### 2) Command to Run (HOST — Git Bash)

Create a shared volume:

```bash
docker volume create sharedvol
docker volume ls
```

Start a writer container:

```bash
docker run -it --name writer -v sharedvol:/data alpine sh
```

### 3) Command to Run (CONTAINER — inside `writer`)

```bash
echo "hello from writer" > /data/shared.txt
ls -la /data
cat /data/shared.txt
exit
```

Back on the host, start a reader container:

```bash
docker run -it --name reader -v sharedvol:/data alpine sh
```

Inside `reader`:

```bash
ls -la /data
cat /data/shared.txt
exit
```

### 4) Expected Output

- `reader` sees `/data/shared.txt` created by `writer`.
- The **volume** is the bridge that allows data sharing.

### 5) Common Mistakes

- Expecting containers to share data automatically.
- Without a bind mount or volume, container filesystems are isolated.

### 6) Thinking Questions

- What exactly is the “bridge” that allowed sharing here?
- If we delete both containers, what happens to the volume data?

---

## Exercise 7 — Common Mistake: Wrong Host Path

### 1) Objective

Simulate a bind mount failure caused by using the wrong host directory.

### 2) Command to Run (HOST — Git Bash)

First, locate the correct folder:

```bash
pwd
ls -la
```

Assume you are in `docker-volume-lab/bind-mount-demo`. Now **intentionally move** to the parent directory:

```bash
cd ..
pwd
ls -la
```

Start a container with a bind mount to a path that may not contain your expected files:

```bash
docker run -it --name bm-wrong -v "$(pwd)/data":/data alpine sh
```

### 3) Command to Run (CONTAINER — inside `bm-wrong`)

```bash
ls -la /data
exit
```

### 4) Expected Output

- `/data` is empty or not what you expected, because you mounted the wrong host directory.

Correct mindset:

- Bind mounts are only as correct as the host path you provide.
- Relative paths depend on the directory where you run the command.

### 5) Thinking Questions

- Why can Docker mount an empty directory without warning?
- If your project moves to another location on disk, what breaks first: bind mounts or volumes?

---

## Exercise 8 — Cleanup and Safety

### 1) Objective

Clean up containers and volumes, and understand why Docker does not delete volumes automatically.

### 2) Command to Run (HOST — Git Bash)

List containers and volumes:

```bash
docker ps -a
docker volume ls
```

Remove containers (adjust names if different):

```bash
docker rm -f bm1 novol2 writer reader bm-wrong vol1
```

Remove volumes (only if you are sure you no longer need them):

```bash
docker volume rm myvol1 sharedvol
```

### 3) Expected Output

- `docker ps -a` shows no demo containers.
- `docker volume ls` no longer shows `myvol1` or `sharedvol`.

### 4) Thinking Questions

- Why is it safer that Docker does **not** auto-delete volumes with containers?
- What would go wrong in production if volumes were automatically removed?

---

## Final Summary (Explain in Your Own Words)

1. **Bind mount vs Docker volume**  
   - Where does the data live in each case?  
   - Who manages that location?

2. **What `docker inspect` reveals**  
   - In the `Mounts` section, which fields clearly show “bind mount” vs “volume”?

3. **Why Docker volumes are safer in production**  
   - Consider portability, stability, and safety for long-lived state like databases.

4. **What happens to data when containers are deleted**  
   - Data in:
     - Pure container filesystem
     - Bind mounts
     - Docker volumes

If you want, I can also add a **Makefile-style script for Git Bash** to automate some of these exercises.