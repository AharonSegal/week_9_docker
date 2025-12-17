week9_docker/
├── .gitignore
├── server1/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── main.py
│ ├── requirements.txt
│ └── db/
│ └── shopping_list.json # Development only - ignored in Docker
├── server2/
│ ├── Dockerfile
│ ├── .dockerignore
│ ├── main.py
│ ├── requirements.txt
│ ├── db/
│ │ └── shopping_list.json # Development only - ignored in Docker
│ └── data/ # Bonus only
│ └── backup_shopping_list.json # Bonus - bind mounted in Docker
├── docker_commands.md #
└── seed_data.tar # Provided - use to seed the volume