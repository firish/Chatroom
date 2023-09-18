# Nimble Messaging Application

This is a robust messaging platform that allows users to communicate, share their thoughts, and express themselves by upvoting or downvoting each message.

## Features

### Frontend

- **User Account Management**
    - Register a new account with a username and password.
    - Log into the platform using existing credentials.

- **Messaging**
    - View historical messages from other users after a successful login.
    - Send messages to other users.
    - Upvote or downvote messages to express opinions.

- **Interface**
    - Provides a polished and professional user interface & experience.

### Backend

- **User Account Management**
    - Process sign-up requests and store user details in the database.
    - Handle login requests and validate user credentials.
    - Reject login attempts with incorrect username or password.

- **Messaging**
    - Store received messages in the database.
    - Ensure a race-condition-free environment for the upvote and downvote functionalities, even in a horizontally scalable system.

- **Authentication**
    - Uses basic password authentication.
    - No reliance on external services for authentication.

## Server Directory Structure

The application's server directory is structured as follows:

- **app.py**  
  This is the primary server file where all the routes, configurations, and server-related functionalities reside.

- **create_tables.py**  
  Utility script to connect to the PostgreSQL database and set up the necessary tables for the application.

- **create_mock_data.py**  
  Utility script that's used to populate the database tables with mock data to aid in testing and development.

- **Dockerfile**  
  The Docker configuration file used to containerize the server application for deployment.

- **minikube-deployment.yaml**  
  Kubernetes configuration for deploying the containerized server application on Minikube.

- **minikube-service.yaml**  
  Kubernetes service configuration to expose the server application running on Minikube.

- **requirements.txt**  
  Contains the list of Python modules and their respective versions required for the server application.

## Client Directory Structure

The application's client directory is structured as follows:

- **App.js / App.css**  
  These are the main React files responsible for rendering the primary layout and components of the application.

- **loginSignup.js / loginSignup.css**  
  These files manage the login and sign-up functionalities of the application. The JavaScript file (`loginSignup.js`) contains React components and logic for user login and registration, while the CSS file (`loginSignup.css`) styles these components.

- **chatroom.js / chatroom.css**  
  Responsible for the chatroom functionality. The JavaScript file (`chatroom.js`) houses the React components and logic required for the chatroom feature, enabling users to send and receive messages. The accompanying CSS file (`chatroom.css`) provides the styling for the chatroom components.

- **Dockerfile**  
  The Docker configuration file used to containerize the client application for deployment. It packages the React application with all its dependencies into a Docker container, making it easier to deploy and run in various environments.

- **client-minikube-deployment.yaml**  
  Kubernetes configuration file tailored for deploying the containerized client application on Minikube.

- **client-minikube-service.yaml**  
  Kubernetes service configuration that exposes the client application running on Minikube to be accessible from a browser or other clients.

Each file has a distinct role, ensuring smooth development, testing, deployment, and scaling of the application.



### Deployment Guide

## Prerequisites

- **Docker**: Ensure Docker is installed.
- **Kubernetes Tools**: Ensure `kubectl` and Minikube are installed.
- **Docker Hub**: Ensure you have a Docker Hub account.

## Backend Deployment

1. **Navigate to your server directory**:
    ```bash
    cd path/to/server
    ```

2. **Build the Docker image for the server**:
    ```bash
    docker build -t <YOUR-DOCKERHUB-USERNAME>/backend-service:latest .
    ```

3. **Login to Docker Hub**:
    ```bash
    docker login
    ```

4. **Push the image to Docker Hub**:
    ```bash
    docker push <YOUR-DOCKERHUB-USERNAME>/backend-service:latest
    ```

5. **Start Minikube**:
    ```bash
    minikube start
    ```

6. **Apply the server deployment and service configurations**:
    ```bash
    kubectl apply -f minikube-deployment.yaml
    kubectl apply -f minikube-service.yaml
    ```

## Frontend Deployment

1. **Navigate to your client directory**:
    ```bash
    cd path/to/client
    ```

2. **Build the Docker image for the frontend**:
    ```bash
    docker build -t <YOUR-DOCKERHUB-USERNAME>/react-client:latest .
    ```

3. **Push the frontend image to Docker Hub**:
    ```bash
    docker push <YOUR-DOCKERHUB-USERNAME>/react-client:latest
    ```

4. **Apply the client deployment and service configurations**:
    ```bash
    kubectl apply -f react-client-deployment.yaml
    kubectl apply -f react-client-service.yaml
    ```

## Database Setup (PostgreSQL)

1. **Deploy a PostgreSQL instance** in your preferred way, whether it's a Docker container, Minikube deployment, or an external database service.

2. **Run `create_tables.py` to set up the database tables**:
    ```bash
    python create_tables.py
    ```

3. **Optionally, populate the database with mock data using `create_mock_data.py`**:
    ```bash
    python create_mock_data.py
    ```

## Accessing the Applications

1. **To access the server application**, use the Minikube service URL:
    ```bash
    minikube service server-service
    ```

2. **To access the client application**, use the Minikube service URL for the react client:
    ```bash
    minikube service react-client-service
    ```

> **Note**: Remember to replace `<YOUR-DOCKERHUB-USERNAME>` with your actual Docker Hub username in the commands. Adjust any paths and filenames based on your actual directory structure and naming conventions.




