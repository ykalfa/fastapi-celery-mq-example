# Async Job Queue with RabbitMQ & Python

This project demonstrates a Distributed Task Queue using Python, Celery, and RabbitMQ, with a FastAPI-based API server. It showcases how to submit and process asynchronous tasks, focusing on system resilience through robust Retry Logic with Exponential Backoff.

## Project Description

The project consists of three main services running in separate containers using Docker Compose:

* **FastAPI Application**: An API server that allows submitting tasks to the queue.

* **Celery Worker**: A worker process that receives and executes tasks from RabbitMQ.

* **RabbitMQ**: A message broker that acts as a bridge between the FastAPI server and the Celery Worker.

## Key Enhancements & Features

The primary enhancement in this project is the implementation of **robust Retry Logic with Exponential Backoff** for temporarily failing tasks.

* **Purpose**: To ensure system resilience against transient failures (such as network issues, temporarily unavailable external services, etc.).

* **Implementation**: The `send` task in `worker.py` has been modified to simulate temporary failures. In case of a failure, Celery attempts to re-execute the task a limited number of times.

* **Exponential Backoff**: The waiting time between each retry increases exponentially (e.g., 1, 2, 4 seconds, etc.). This prevents overwhelming the system or external services during persistent failures.

## Technologies Used

* **Python 3.x**

* **FastAPI**: A web framework for building fast APIs.

* **Celery**: A Distributed Task Queue for handling asynchronous tasks.

* **RabbitMQ**: A message broker.

* **Docker & Docker Compose**: For managing and running services in containers.

## How to Run the Project

Ensure Docker Desktop is installed and running on your machine.

1. **Fork & Clone the Project:**

   * Fork this project to your GitHub account.

   * Clone the project to your local machine:

     ```bash
     git clone [https://github.com/YOUR_GITHUB_USERNAME/fastapi-celery-mq-example.git](https://github.com/YOUR_GITHUB_USERNAME/fastapi-celery-mq-example.git)
     ```

   * Navigate into the project directory:

     ```bash
     cd fastapi-celery-mq-example
     ```

2. **Build and Start the Containers:**

   * Start the services using Docker Compose:

     ```bash
     docker-compose up -d --build
     ```

   * (The `--build` flag is especially important the first time to build the images from source code).

3. **Check Service Status:**

   * Verify that all services are running:

     ```bash
     docker-compose ps
     ```

   * You should see `rabbit`, `fastapi`, and `worker` in an `Up` state.

## Project Usage

1. **Access the API:**

   * Open your browser and navigate to: [http://localhost:8080/docs](http://localhost:8080/docs)

   * This will display the Swagger UI interface for the API.

2. **Submit a Task:**

   * In the Swagger UI, find the `POST /api/v1/tasks/send_message` endpoint.

   * Click "Try it out".

   * In the `msg` text box, type any message (e.g., `"hello world"`).

   * Click the "Execute" button.

3. **View Worker Logs:**

   * To observe the `retries` in action, open a new terminal (separate from the one where you ran `docker-compose up`).

   * Run the following command to view the worker container's logs:

     ```bash
     docker-compose logs -f worker
     ```

   * Due to the simulated failure (70% chance of failure), you'll likely see log messages indicating task failures and retries with increasing wait times, until the task succeeds or reaches its maximum retry limit.

## Additional Notes

* The project is configured with `max_retries=3`, meaning Celery will attempt to re-execute the task up to 3 additional times (a total of 4 attempts including the original) before it permanently fails.

* `retry_backoff=True` ensures that the waiting time between retries increases exponentially.
