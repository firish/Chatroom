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

## Project Structure

The application's directory is structured as follows:

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

Each file has a distinct role, ensuring smooth development, testing, deployment, and scaling of the application.



## Installation & Setup

(You can include instructions here on how to set up and run the application.)



