## WatchThis! - Movie finder app
## About
This project implements a vector search system using pgvector and PostgreSQL. The goal is to efficiently store and retrieve high-dimensional embeddings, enabling tasks such as semantic search, similarity matching, and AI-powered recommendations.

### Overview
The project consists of four main Python files:

* Three files handle core functionality to run aplication (Database Setup, database interactions, and Vector Encoding).
* The fourth file, `main.py`, runs the entire pipeline.

Database type: **Vector Database**:
* We utilized the _PostgreSQL_ extension **PgVector** to setup the DB.

Site consists of 2 elements:
* Back-end, Flask app that is run on Python
* Front-end, Simple HTML site.

---
Currently remote access to database is not supported. For that reason even if you run docker file, make sure that Cmake, Visual Studio - C++ Devtools, PgVector is installed on your computer.  
`You need Cmake to install PgVector`

However if you already set up remote access to database, then you can install these programs on host device, and just run conainerized app on user-side. In that case **no need to install** additional tools. just docker
## Requirements(local run):
1. Install dependencies: `pip install -r requirements.txt`

2. Install [PgVector](https://github.com/pgvector/pgvector)
 from github and follow the [Instructions](https://github.com/pgvector/pgvector-python?tab=readme-ov-file#psycopg-2) in the documentation:
```bash:
git clone https://github.com/yourusername/vector-search-pgvector.git  
```

3. Check whether the extension is installed or not in PgAdmin:
```SQL:
CREATE EXTENSION IF NOT EXISTS vector;
```
## Requirements(local run):
**1. Build image**
 ```bash:
docker compose up --build
 ```
 * or if you want detached mode
 ```bash:
 docker compose up -d --build
 ```

 2. check if the process is running
 ```bash:
 docker ps
 ```

 3. To stop the whole process
 ```bash:
 docker compose down
 ```
***
### <img src="https://user-images.githubusercontent.com/74038190/213844263-a8897a51-32f4-4b3b-b5c2-e1528b89f6f3.png" width="50px" /> &nbsp; Made by Arlan, Bekzat, Miras, Amir &nbsp; <img src="https://user-images.githubusercontent.com/74038190/213844263-a8897a51-32f4-4b3b-b5c2-e1528b89f6f3.png" width="50px" />