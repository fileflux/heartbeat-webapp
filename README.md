
# Heartbeat Web Application

## Overview
This is a Python Flask-based web application designed to receive heartbeat signals from EKS nodes. It stores and updates information about the worker node name, worker node availability, total ZFS pool size, and available space in the ZFS pool in a CockroachDB cluster. The app provides an endpoint to handle heartbeat signals from the EKS nodes, ensuring that the system can monitor worker node health and performance in real-time.

## Features
- Receive and process heartbeat signals from nodes via a `/heartbeat` API endpoint.
- Store and update node status and information in a CockroachDB Cluster.
- Dockerized for easy deployment.
- Includes custom readiness and liveness probes for Kubernetes to ensure high availability.
- GitHub Actions CI/CD workflow to build a multi-platform container image and push it to DockerHub.
- Integrated security scanning of the container image using Trivy.

## Prerequisites
To run this application locally or in a container, you need:
- Python 3.11+
- Flask
- CockroachDB Cluster (for database interactions)
- Docker (for containerization)

Install the dependencies locally by running:
```bash
pip install -r requirements.txt
```

## Repository Structure

```plaintext
heartbeat-webapp-main/             
├── Dockerfile              
├── README.md               
├── app.py                  
├── db.py                  
├── liveness.sh             
├── readiness.sh            
├── requirements.txt        
```

### What Each File Does
- **docker.yaml**: Contains the GitHub Actions workflow for building and pushing the multi-platform container image to DockerHub and scanning it for vulnerabilities using Trivy.

- **app.py**: The core of the web application. It exposes a `/heartbeat` endpoint that accepts POST requests and stores/updates node data and information in a CockroachDB Cluster.
  
- **db.py**: Handles database connections, using CockroachDB as the backend database for storing node information.

- **liveness.sh**: A script used for Kubernetes' liveness probe, checking whether the app is running and responsive.

- **readiness.sh**: A script for Kubernetes' readiness probe, ensuring the app is ready to serve requests.

- **requirements.txt**: Specifies the Python dependencies required to run the web application (Flask, PostgreSQL connector, etc.), to be installed while building the container image.

- **Dockerfile**: Configuration for building the web app Docker image. It sets up the necessary Python environment, installs dependencies, and configures health checks.

## Building a Docker Image

To build the Docker image for this web app:

1. Clone the repository:
   ```bash
   git clone https://github.com/fileflux/heartbeat-webapp.git
   cd heartbeat-webapp
   ```

2. Build the Docker image:
   ```bash
   docker build -t heartbeat-webapp .
   ```

## Probes

This web app includes Kubernetes health probes:

- **Liveness Probe**: Ensures that the container is still running. If this probe fails, Kubernetes will restart the container.
  ```bash
  ./liveness.sh
  ```

- **Readiness Probe**: Ensures that the app is ready to serve traffic. If this probe fails, Kubernetes will stop sending requests to the container.
  ```bash
  ./readiness.sh
  ```

Both scripts are designed to return appropriate status codes to Kubernetes based on the application’s health.

## GitHub Workflow (including Trivy)

A GitHub Actions workflow is included to automate the build process. The workflow builds a multi-platform container image using Docker for AMD64 and ARM based systems and pushes the image to DockerHub. This workflow also integrates `Trivy`, a vulnerability scanning tool to scan the aforementioned container image, to ensure that it is secure.

This workflow:
1. Checks the code and accesses DockerHub.
2. Builds and pushes multi-platform Docker images for AMD64 and ARM to DockerHub using the Dockerfile in the repository.
3. Runs a security scan on the Docker image using `Trivy`.
4. Logs out from DockerHub.

## Usage

Once the app is running, the EKS nodes can send a POST request to the `/heartbeat` endpoint to register or update node information. Example payload:

```json
{
  "node_name": "Node1",
  "zpool_name": "zpool1",
  "total_space": "500GB",
  "available_space": "250GB"
}
```

## Additional Notes
- Ensure that the CockroachDB cluster is set up and running before starting the web application. You can modify the database connection in `db.py` to match your configuration.
- The liveness and readiness probes are useful when deploying the app in a Kubernetes environment to ensure high availability.
