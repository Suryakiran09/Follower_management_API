## Social Networking Application using DRF

## Table of Contents
- [Introduction](#introduction)
- [Technologies Used](#technologies-used)
- [Overview](#overview)
- [Cloning the Repository](#cloning-the-repository)
- [Installation](#installation)
- [Starting Docker](#starting-docker)
- [Building and Running the Application](#building-and-running-the-application)
- [API Documentation](#api-documentation)
- [Endpoints](#endpoints)
- [Postman Collection](#postman-collection)

## Introduction
This application is a web service providing various social networking features using RESTful APIs. This document serves as a guide to install, run, and interact with the application using Docker and Docker Compose.

## Technologies Used

- Django
- Django Rest Framework
- Html
- Css
- Javascript
- SQLite3

## Overview

This application is a social networking platform developed using modern technologies like Django Rest Framework (DRF) and SQLite3. The platform enables users to sign up, log in, search for other users, send friend requests, and manage their friend list.

On the technical side, the backend employs Django Rest Framework (DRF) to develop RESTful API services, enabling seamless communication between the frontend and the backend systems.

Some notable features of this application comprise user authentication, user search functionality, friend request management, and authenticated API access. Altogether, the application aims to offer an engaging and interactive social networking experience.

- ### Models

    The application uses the following Django models to represent the entities involved in the social networking application:

    - **User**: Inherits from AbstractBaseUser and includes fields like `email`, `name`, and `friends` which is a many-to-many relationship with itself.
    - **FriendRequest**: Represents a friend request with fields `from_user`, `to_user`, `status`, and `created_at`.

- ### API Endpoints and Implementation

    - **Endpoint Authorizations**: The endpoints are designed to allow only authenticated users to access most of the functionalities.

    - **CRUD Operations**: Most models support Create, Read, Update, and Delete (CRUD) operations via DRF views such as `GenericAPIView`.

- ### Authentication and Security

    The application uses token-based authentication for secure API access.

    Security mechanisms in place include:

    - **Permissions**: DRF's `IsAuthenticated` permission class is used to control access to endpoints.
    - **Authorization**: Ensures only the appropriate user can access or modify their data.

- ### Trade-Offs

    - **Simplicity vs. Flexibility**: The application design prioritizes simplicity and ease of use over extensive customization.
    - **Performance vs. Detail**: The application uses SQLite3 for efficient data storage and retrieval.

    The design decisions and features are based on providing a straightforward and efficient social networking platform.

## Cloning the Repository
To clone the Git repository containing the application code:

```shell
git clone https://github.com/Suryakiran09/Follower_management_API.git
```

```shell
cd SocialNetAPI
```

## Installation
To get started with the application, you need to have Docker and Docker Compose installed on your system.

- **Docker:** Install Docker Desktop for Windows from the [official Docker website](https://www.docker.com/get-started).
- **Docker Compose:** Docker Compose is installed automatically with Docker Desktop. Check the [installation guide](https://docs.docker.com/compose/install/) for more information.

## Starting Docker
After installing Docker, Docker Desktop should automatically start on startup. You can check if Docker is running by looking for the Docker icon in the system tray.

## Building and Running the Application
To build and run the application, follow these steps:

1. **Clone the Repository:**
    Clone the Git repository containing the application code:

    ```shell
    git clone https://github.com/Suryakiran09/Follower_management_API.git
    ```
    ```shell
    cd SocialNetAPI
    ```

2. **Build the Application:**
    Use Docker Compose to build the application:

    ```shell
    docker-compose build
    ```

3. **Start the Application:**
    Start the application using Docker Compose:

    ```shell
    docker-compose up
    ```

The application will now be running and accessible at `http://localhost:8000/`.

## API Documentation

The API documentation can be accessed at the following URLs:

- **Swagger UI:** [Swagger UI](http://localhost:8000/)
  ```bash 
    http://localhost:8000/
    ```
- **ReDoc:** [ReDoc](http://localhost:8000/redoc/) 
  ```bash
    http://localhost:8000/redoc/
    ```

## Endpoints

### User Endpoints

1. **Register:**
   - **POST** `/register/` - Register a new user

2. **Login:**
   - **POST** `/login/` - Obtain authentication token

3. **Search Users:**
   - **GET** `/search/?q=<keyword>` - Search users by email or name

4. **Friend Request:**
   - **POST** `/friend-request/` - Send a friend request

5. **Friend Request Actions:**
   - **POST** `/friend-request/accept/` - Accept a friend request
   - **POST** `/friend-request/reject/` - Reject a friend request

6. **List Friends:**
   - **GET** `/friends/` - List friends

7. **List Pending Friend Requests:**
   - **GET** `/friend-requests/pending/` - List pending friend requests


## Postman Collection

### You can check the main folder for the Postman collection file.