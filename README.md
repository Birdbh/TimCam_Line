# TimCam Project

## Overview
This project consists of three main components:
1. **camera.py**: Uses OpenCV to process video streams and detect pedestrians.
2. **streamlit.py**: A Streamlit app to display line statistics.
3. **db.py**: Manages database operations using TimescaleDB.

## camera.py
This script processes a video stream to detect pedestrians using OpenCV. It performs the following steps:
1. Opens a video stream from a specified URL.
2. Reads frames from the stream.
3. Processes frames using various image processing techniques.
4. Detects pedestrians in the processed frames.
5. Draws rectangles around detected pedestrians and displays the frames.
6. Inserts the number of detected pedestrians into the database.

### How to Run
To run the pedestrian detection script:
```bash
python camera.py
```

## streamlit.py
This script creates a Streamlit app to display line statistics. It performs the following steps:
1. Calculates various statistics from the database.
2. Displays the statistics in a user-friendly dashboard.

### How to Run
To run the Streamlit app:
```bash
streamlit run streamlit.py
```

## db.py
This script manages database operations using TimescaleDB. It includes functions to:
1. Connect to the database.
2. Create necessary tables.
3. Insert and retrieve data.
4. Calculate various statistics.

## Setting Up TimescaleDB with Docker
To set up TimescaleDB using Docker, follow these steps:

1. **Install Docker**: If you don't have Docker installed, download and install it from [here](https://www.docker.com/products/docker-desktop).

2. **Pull TimescaleDB Image**:
    ```bash
    docker pull timescale/timescaledb:latest-pg12
    ```

3. **Run TimescaleDB Container**:
    ```bash
    docker run -d --name timescaledb -p 5432:5432 -e POSTGRES_PASSWORD=password timescale/timescaledb:latest-pg12
    ```

4. **Connect to TimescaleDB**:
    Use the connection string in `db.py` to connect to the database:
    ```python
    CONNECTION = "dbname=postgres user=postgres password=password host=localhost port=5432"
    ```

5. **Create Tables**:
    Run the `create_table` function in `db.py` to create the necessary tables:
    ```python
    import db
    db.create_table()
    ```

Now you are ready to run the Streamlit app and the pedestrian detection script with the TimescaleDB backend.
```