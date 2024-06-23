# Task List API - Clean Architecture

This is a RESTful API for managing a task list, implemented using FastAPI and containerized with Docker with "Clean Architecture" design pattern.

## Features

- CRUD operations for tasks
- API authorization with 1-minute expiration tokens
- Unit tests
- Dockerized deployment
- Clean Architecture

## Requirements

- Python 3.9+
- FastAPI 0.89+
- Docker


## Setup

- Install dependencies:

    ```
    pip install -r requirements.txt
    ```

## Run
1. ### prod mode:
    ```
    docker build -t fastapi_image .
    ```

    if successfully built,

    ```
    docker run -d --name fastapi_container -p 80:80 fastapi_image
    ```
2. ### dev mode
    ```
    docker-compose up --build
    ```

## Test
- run
 
    ```
    pytest
    ```
