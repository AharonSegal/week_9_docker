#################################################
#                                               #
#             DOCKER COMMANDS                   #
#                                               #
#################################################

<!-- 
░██                                                 
                                                    
░██░█████████████   ░██████    ░████████  ░███████  
░██░██   ░██   ░██       ░██  ░██    ░██ ░██    ░██ 
░██░██   ░██   ░██  ░███████  ░██    ░██ ░█████████ 
░██░██   ░██   ░██ ░██   ░██  ░██   ░███ ░██        
░██░██   ░██   ░██  ░█████░██  ░█████░██  ░███████  
                                     ░██            
                               ░███████             
                                                     -->
                    __                               
           |  \                              
 __     __  \$$  ______   __   __   __       
|  \   /  \|  \ /      \ |  \ |  \ |  \      
 \$$\ /  $$| $$|  $$$$$$\| $$ | $$ | $$      
  \$$\  $$ | $$| $$    $$| $$ | $$ | $$      
   \$$ $$  | $$| $$$$$$$$| $$_/ $$_/ $$      
    \$$$   | $$ \$$     \ \$$   $$   $$      
     \$     \$$  \$$$$$$$  \$$$$$\$$$$       
                                             
(outside of the container)     


## Check Running Containers

```bash
docker ps
docker ps -a
# - Displays container ID, name, image, ports, and status
```
docker ps -a
is used to list all Docker containers on your system, including both running and stopped ones. Here's a breakdown:
docker ps → shows only running containers.
-a (or --all) → includes all containers, whether they are running, stopped, or exited.

<!-- 
                                    ░██               ░██                               
                                    ░██                                                 
 ░███████   ░███████  ░████████  ░████████  ░██████   ░██░████████   ░███████  ░██░████ 
░██    ░██ ░██    ░██ ░██    ░██    ░██          ░██  ░██░██    ░██ ░██    ░██ ░███     
░██        ░██    ░██ ░██    ░██    ░██     ░███████  ░██░██    ░██ ░█████████ ░██      
░██    ░██ ░██    ░██ ░██    ░██    ░██    ░██   ░██  ░██░██    ░██ ░██        ░██      
 ░███████   ░███████  ░██    ░██     ░████  ░█████░██ ░██░██    ░██  ░███████  ░██      
                                                                                         -->
               
                                          /  |              
  _______   ______    ______    ______   _$$ |_     ______  
 /       | /      \  /      \  /      \ / $$   |   /      \ 
/$$$$$$$/ /$$$$$$  |/$$$$$$  | $$$$$$  |$$$$$$/   /$$$$$$  |
$$ |      $$ |  $$/ $$    $$ | /    $$ |  $$ | __ $$    $$ |
$$ \_____ $$ |      $$$$$$$$/ /$$$$$$$ |  $$ |/  |$$$$$$$$/ 
$$       |$$ |      $$       |$$    $$ |  $$  $$/ $$       |
 $$$$$$$/ $$/        $$$$$$$/  $$$$$$$/    $$$$/   $$$$$$$/ 
                                                            
## Pull an Image
```bash
docker pull nginx:latest
# - Downloads the Nginx image from Docker Hub (online Docker registry)
# - Stores it locally so you can run containers without internet
````

## Run a Container

```bash
docker run -d --name nginx-web -p 80:80 nginx:latest
# - Creates and starts a container from the nginx:latest image
# - -d → detached mode (runs in background)
# - --name nginx-web → assigns the container name
# - -p 80:80 → maps host port 80 to container port 80
```
 _______             __  __        __ 
|       \           |  \|  \      |  \
| $$$$$$$\ __    __  \$$| $$  ____| $$
| $$__/ $$|  \  |  \|  \| $$ /      $$
| $$    $$| $$  | $$| $$| $$|  $$$$$$$
| $$$$$$$\| $$  | $$| $$| $$| $$  | $$
| $$__/ $$| $$__/ $$| $$| $$| $$__| $$
| $$    $$ \$$    $$| $$| $$ \$$    $$
 \$$$$$$$   \$$$$$$  \$$ \$$  \$$$$$$$
                                      
---
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
* -t tag (image name)
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


## ✅ 5. Run Command (FastAPI-Correct)

```bash
docker run -p 8000:8000 fastapi-app
# -p → port mapping
# 8000:8000 → host:container
```


            __                               
           |  \                              
 __     __  \$$  ______   __   __   __       
|  \   /  \|  \ /      \ |  \ |  \ |  \      
 \$$\ /  $$| $$|  $$$$$$\| $$ | $$ | $$      
  \$$\  $$ | $$| $$    $$| $$ | $$ | $$      
   \$$ $$  | $$| $$$$$$$$| $$_/ $$_/ $$      
    \$$$   | $$ \$$     \ \$$   $$   $$      
     \$     \$$  \$$$$$$$  \$$$$$\$$$$       
                                             

```bash
docker start volume-test    # Start a stopped container named volume-test
docker exec -it fastapi-container sh
# - -it → interactive terminal
# - nginx-web → container name
# - bash → open Bash shell inside container
ls            # list files in current directory
ls -l         # detailed list (permissions, owner, size)
ls -la        # detailed list including hidden files

```

* `-i` → keeps STDIN open (allows typing commands)
* `-t` → allocates a pseudo-terminal (normal bash prompt)
* Combined (`-it`) → fully interactive bash
        🟡The terminal you used at creation does not persist
    Containers do not keep an interactive bash alive
    docker exec -it ... bash creates a new bash session
    That’s why you must specify it again 

docker inspect fastapi-container --format "{{ json .Mounts }}"

---
                               __  __   ______            
                              |  \|  \ /      \           
 ______ ____    ______    ____| $$ \$$|  $$$$$$\ __    __ 
|      \    \  /      \  /      $$|  \| $$_  \$$|  \  |  \
| $$$$$$\$$$$\|  $$$$$$\|  $$$$$$$| $$| $$ \    | $$  | $$
| $$ | $$ | $$| $$  | $$| $$  | $$| $$| $$$$    | $$  | $$
| $$ | $$ | $$| $$__/ $$| $$__| $$| $$| $$      | $$__/ $$
| $$ | $$ | $$ \$$    $$ \$$    $$| $$| $$       \$$    $$
 \$$  \$$  \$$  \$$$$$$   \$$$$$$$ \$$ \$$       _\$$$$$$$
                                                |  \__| $$
                                                 \$$    $$
                                                  \$$$$$$ 

# File Operations inside Container

## Copy Files

```bash
cp <source> <destination>
cp index.html index.html.backup
# - Copies a file or directory
# - Original file remains unchanged
```

## View, Create, and Concatenate Files (`cat`) & Quick Output (`echo`)

```bash
cat > newfile.txt       # Create a new file or overwrite
cat <filename>          # View contents of a file
cat file1 file2         # Concatenate and display multiple files
cat file1 >> file2      # Append contents of file1 to file2

echo
echo "Hello World"              # Print text to terminal
echo "Hello World" > file.txt   # Create or overwrite a file with single-line text
echo "Hello Again" >> file.txt  # Append text to an existing file
```
    Key Difference:
        cat → viewing, creating, or combining files (multi-line capable).
        echo → quick output or writing simple single-line content.

### Create a Multi-line File with Here-Document

```bash
cat > index.html << 'EOF'
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Custom Page</title>
</head>
<body>
    <h1>Welcome!</h1>
    <p>This is a custom HTML page created with cat.</p>
</body>
</html>
EOF
```

* Everything between `<< 'EOF'` and `EOF` will be written into `index.html`.

---

 __                               
|  \                              
| $$  ______    ______    _______ 
| $$ /      \  /      \  /       \
| $$|  $$$$$$\|  $$$$$$\|  $$$$$$$
| $$| $$  | $$| $$  | $$ \$$    \ 
| $$| $$__/ $$| $$__| $$ _\$$$$$$\
| $$ \$$    $$ \$$    $$|       $$
 \$$  \$$$$$$  _\$$$$$$$ \$$$$$$$ 
              |  \__| $$          
               \$$    $$          
                \$$$$$$           

```bash
docker logs nginx-web-8080
# - Displays all logs generated by the container
```

## Follow Logs in Real-Time

```bash
docker logs -f nginx-web-8080
# -f → follow logs as they are produced
```

## Show Only Last N Lines

```bash
docker logs --tail 20 nginx-web-8080
# - Displays last 20 lines
```

## Combine Follow and Tail

```bash
docker logs -f --tail 10 nginx-web-8080
# - Shows last 10 lines and continues streaming new logs
```
---

           __                               
          |  \                              
  _______ | $$  ______    _______   ______  
 /       \| $$ /      \  /       \ /      \ 
|  $$$$$$$| $$|  $$$$$$\|  $$$$$$$|  $$$$$$\
| $$      | $$| $$  | $$ \$$    \ | $$    $$
| $$_____ | $$| $$__/ $$ _\$$$$$$\| $$$$$$$$
 \$$     \| $$ \$$    $$|       $$ \$$     \
  \$$$$$$$ \$$  \$$$$$$  \$$$$$$$   \$$$$$$$
                                         

# Exit Docker Container Shell

```bash
exit
# - Ends the current shell session inside the container
# - Returns you to the host terminal
```

## Docker Cleanup Commands

### Stop Running Containers
```bash
docker stop nginx-web nginx-web-8080
````

* Stops the running containers `nginx-web` and `nginx-web-8080`.
* Containers must be stopped before they can be removed.

### Remove Containers

```bash
docker rm nginx-web nginx-web-8080
```

* Deletes the stopped containers completely from Docker.
* Any data inside the container is lost unless stored in a Docker volume.

### Remove Docker Image

```bash
docker rmi nginx:latest
```

* Deletes the `nginx:latest` image from local Docker storage.
* Useful to free up space or force a fresh pull later.

---

## Check if Port 80 is in Use

### Linux

```bash
netstat -tulpn | grep :80
```

* `netstat` → shows network connections, listening ports, and associated programs
* `-t` → show TCP connections
* `-u` → show UDP connections
* `-l` → show only listening sockets
* `-p` → show process ID (PID) and program name
* `-n` → show numeric addresses instead of resolving hostnames
* `| grep :80` → filters results to show only processes using **port 80**

### Windows

```powershell
netstat -ano | findstr :80
```

* `-a` → all connections and listening ports
* `-n` → numeric addresses
* `-o` → shows PID of the process
* `| findstr :80` → filters results to show only processes using **port 80**

**Tip:** Use the PID to identify the process blocking the port:

```powershell
tasklist /FI "PID eq <PID>"
```


---
<!-- 
░███    ░██                       ░██                         ░██    ░██                      
░████   ░██                                                   ░██                             
░██░██  ░██  ░██████   ░██    ░██ ░██ ░████████  ░██████   ░████████ ░██ ░███████  ░████████  
░██ ░██ ░██       ░██  ░██    ░██ ░██░██    ░██       ░██     ░██    ░██░██    ░██ ░██    ░██ 
░██  ░██░██  ░███████   ░██  ░██  ░██░██    ░██  ░███████     ░██    ░██░██    ░██ ░██    ░██ 
░██   ░████ ░██   ░██    ░██░██   ░██░██   ░███ ░██   ░██     ░██    ░██░██    ░██ ░██    ░██ 
░██    ░███  ░█████░██    ░███    ░██ ░█████░██  ░█████░██     ░████ ░██ ░███████  ░██    ░██ 
                                            ░██                                               
                                      ░███████                                                 -->

## List Contents

```bash
ls        # Shows files and directories
ls -l     # Detailed listing
ls -la    # All files including hidden files
```

## Move Between Directories

```bash
cd ~                  # Go to home directory
cd ..                 # Move up one directory
cd -                  # Go back to previous directory
cd <directory_name>   # Move into a directory by name
cd /usr/share/nginx/html   # Absolute path
cd usr/share/nginx/html     # Relative path
```

## Check Current Directory

```bash
pwd   # Print working directory
```

## Show Directory Tree (Recursive)

```bash
tree   # Displays file tree (may need to install first)
# If not installed:
apt update
apt install -y tree
```

<!-- 
░██    ░██            ░██                                                  
░██    ░██            ░██                                                  
░██    ░██  ░███████  ░██ ░██    ░██ ░█████████████   ░███████   ░███████  
░██    ░██ ░██    ░██ ░██ ░██    ░██ ░██   ░██   ░██ ░██    ░██ ░██        
 ░██  ░██  ░██    ░██ ░██ ░██    ░██ ░██   ░██   ░██ ░█████████  ░███████  
  ░██░██   ░██    ░██ ░██ ░██   ░███ ░██   ░██   ░██ ░██               ░██ 
   ░███     ░███████  ░██  ░█████░██ ░██   ░██   ░██  ░███████   ░███████  
                                                                            -->

            __                               
           |  \                              
 __     __  \$$  ______   __   __   __       
|  \   /  \|  \ /      \ |  \ |  \ |  \      
 \$$\ /  $$| $$|  $$$$$$\| $$ | $$ | $$      
  \$$\  $$ | $$| $$    $$| $$ | $$ | $$      
   \$$ $$  | $$| $$$$$$$$| $$_/ $$_/ $$      
    \$$$   | $$ \$$     \ \$$   $$   $$      
     \$     \$$  \$$$$$$$  \$$$$$\$$$$       
                                             
(outside of the volume)                                           
                                             
### List Volumes

```bash
docker volume ls
```
* Lists all Docker volumes on your system.

### Inspect Volume on Host 

```bash
docker volume inspect myvolume
```
* Shows detailed information about the volume, including mountpoint on the host.

  ______                                  __                     
 /      \                                |  \                    
|  $$$$$$\  ______    ______    ______  _| $$_     ______        
| $$   \$$ /      \  /      \  |      \|   $$ \   /      \       
| $$      |  $$$$$$\|  $$$$$$\  \$$$$$$\\$$$$$$  |  $$$$$$\      
| $$   __ | $$   \$$| $$    $$ /      $$ | $$ __ | $$    $$      
| $$__/  \| $$      | $$$$$$$$|  $$$$$$$ | $$|  \| $$$$$$$$      
 \$$    $$| $$       \$$     \ \$$    $$  \$$  $$ \$$     \      
  \$$$$$$  \$$        \$$$$$$$  \$$$$$$$   \$$$$   \$$$$$$$      
                                                                 

### Create a Volume
```bash
docker volume create myvolume
docker volume create first_lab
```
* Creates a named Docker volume called `myvolume`.
* Volumes allow data to persist even if containers are removed.

 __       __                                 __      __                     
|  \     /  \                               |  \    |  \                    
| $$\   /  $$  ______   __    __  _______  _| $$_    \$$ _______    ______  
| $$$\ /  $$$ /      \ |  \  |  \|       \|   $$ \  |  \|       \  /      \ 
| $$$$\  $$$$|  $$$$$$\| $$  | $$| $$$$$$$\\$$$$$$  | $$| $$$$$$$\|  $$$$$$\
| $$\$$ $$ $$| $$  | $$| $$  | $$| $$  | $$ | $$ __ | $$| $$  | $$| $$  | $$
| $$ \$$$| $$| $$__/ $$| $$__/ $$| $$  | $$ | $$|  \| $$| $$  | $$| $$__| $$
| $$  \$ | $$ \$$    $$ \$$    $$| $$  | $$  \$$  $$| $$| $$  | $$ \$$    $$
 \$$      \$$  \$$$$$$   \$$$$$$  \$$   \$$   \$$$$  \$$ \$$   \$$ _\$$$$$$$
                                                                  |  \__| $$
                                                                   \$$    $$
                                                                    \$$$$$$ 

You are mounting the volume myvolume into the container at path /data.
Attaching a volume to a specific path inside a container so the container can read and write data there.

```bash
docker run -it --name volume-test -v myvolume:/data alpine sh
```
* docker run
    Creates and starts a new container from an image.
* -it
    Runs the container in interactive mode with a terminal:
    -i → keeps STDIN open so you can type commands
    -t → allocates a terminal (TTY)

* --name volume-test
    Assigns a custom name (volume-test) to the container.

* -v myvolume:/data
    Mounts the Docker volume myvolume into the container at path /data.
    myvolume → volume managed by Docker
    /data → directory inside the container
        If /data does not exist, Docker creates it automatically.

* alpine
    The image used to create the container.
    Alpine Linux is a very small and lightweight Linux distribution.

* sh
    The command executed when the container starts.
    Launches the Alpine shell (sh) so you can interact with the container.

### Use the Same Volume in Another Container

```bash
docker run -it --name volume-test-2 -v myvolume:/data alpine sh
```

  ______                                                     __                     
 /      \                                                   |  \                    
|  $$$$$$\  _______   _______   ______    _______   _______  \$$ _______    ______  
| $$__| $$ /       \ /       \ /      \  /       \ /       \|  \|       \  /      \ 
| $$    $$|  $$$$$$$|  $$$$$$$|  $$$$$$\|  $$$$$$$|  $$$$$$$| $$| $$$$$$$\|  $$$$$$\
| $$$$$$$$| $$      | $$      | $$    $$ \$$    \  \$$    \ | $$| $$  | $$| $$  | $$
| $$  | $$| $$_____ | $$_____ | $$$$$$$$ _\$$$$$$\ _\$$$$$$\| $$| $$  | $$| $$__| $$
| $$  | $$ \$$     \ \$$     \ \$$     \|       $$|       $$| $$| $$  | $$ \$$    $$
 \$$   \$$  \$$$$$$$  \$$$$$$$  \$$$$$$$ \$$$$$$$  \$$$$$$$  \$$ \$$   \$$ _\$$$$$$$
                                                                          |  \__| $$
                                                                           \$$    $$
                                                                            \$$$$$$ 
```bash
docker start volume-test    #Start the container (if it’s stopped)
docker exec -it volume-test sh #Enter the container
```
    docker exec → run a command inside a running container
    -it → interactive terminal
    volume-test → container name
    sh → shell inside the container
      🟡The terminal you used at creation does not persist
        Containers do not keep an interactive shell alive
        docker exec -it ... sh creates a new shell session
        That’s why you must specify it again 

```bash
echo "Hello from the container!" > /data/containerfile.txt
ls /data
```
* File is now stored in the Docker volume, not just the container.


 _______   __                  __       
|       \ |  \                |  \      
| $$$$$$$\ \$$ _______    ____| $$      
| $$__/ $$|  \|       \  /      $$      
| $$    $$| $$| $$$$$$$\|  $$$$$$$      
| $$$$$$$\| $$| $$  | $$| $$  | $$      
| $$__/ $$| $$| $$  | $$| $$__| $$      
| $$    $$| $$| $$  | $$ \$$    $$      
 \$$$$$$$  \$$ \$$   \$$  \$$$$$$$      
                                        
                                        
                                        
bind is to use my local pc storage instead of a docker volume
```bash
docker run -it --name bind-test -v ~/docker-volume-lab:/data alpine sh
```
* -v ~/docker-volume-lab:/data
    Mount a host directory as a bind mount:
* ~/docker-volume-lab → Folder on the host machine.
* /data → Path inside the container where the folder is accessible.
    Changes inside /data reflect on the host folder and vice versa.

* Maps a host directory (`~/docker-volume-lab`) to `/data` in the container.
* Inside container:

           __                               
          |  \                              
  _______ | $$  ______    _______   ______  
 /       \| $$ /      \  /       \ /      \ 
|  $$$$$$$| $$|  $$$$$$\|  $$$$$$$|  $$$$$$\
| $$      | $$| $$  | $$ \$$    \ | $$    $$
| $$_____ | $$| $$__/ $$ _\$$$$$$\| $$$$$$$$
 \$$     \| $$ \$$    $$|       $$ \$$     \
  \$$$$$$$ \$$  \$$$$$$  \$$$$$$$   \$$$$$$$
                                         

```bash
docker rm -f volume-test volume-test-2 bind-test
docker volume rm myvolume
```

* Removes containers and the volume to free up resources.
