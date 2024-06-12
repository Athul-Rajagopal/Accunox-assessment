# Django Social Networking API

A social networking application built using Django and Django Rest Framework.

## Features

- User signup and login with email and password
- Search users by email or name
- Send, accept, and reject friend requests
- List friends and pending friend requests
- Rate limiting on friend requests

## Requirements

- Docker
- Docker Compose

## Installation

Follow these steps to set up and run the project on your local machine.

### Clone the Repository

```bash
git clone https://github.com/Athul-Rajagopal/social-networking-API.git
cd social-networking-API/social_network
````

### Configure Environment Variables

Create a .env file in the project root with the following content:

```env
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
```

### Build and Run Docker Containers

Build and start the Docker containers:

```bash
docker-compose up -d --build
```

### Apply Database Migrations

Run the database migrations:

```bash
docker-compose run web python manage.py migrate
```

### Collect Static Files

Collect the static files:

```bash
docker-compose run web python manage.py collectstatic --noinput
```

## Running the Project

### Access the Application

The application should now be running on http://localhost:8000.

### Creating a Superuser

To create a superuser for accessing the Django admin panel:
```bash
docker-compose run web python manage.py createsuperuser
```

## API Endpoints

Here are some of the main API endpoints available in this project:

### User Signup

- **Endpoint**: `/signup/`
- **Method**: `POST`
- **Payload**:
``` json
{
  "username": "your_username",
  "email": "your_email@example.com",
  "password": "your_password"
}
```

### User Login

- **Endpoint**: `/login/`
- **Method**: `POST`
- **Payload**:
``` json
{
  "email": "your_email@example.com",
  "password": "your_password"
}
```

### Search Users

- **Endpoint**: `/search/?q=search_term`
- **Method**: `GET`
- **Headers**:
  
  ```
  Authorization: Bearer `<access_token>`
  ```

### Send Friend Request

- **Endpoint**: `/friend-request/send/`
- **Method**: `POST`
- **Headers**:
  
  ```
  Authorization: Bearer `<access_token>`
  ```
- **Payload**:
``` json
{
 "to_user": <user_id>
 }
```

### Responding friend request

- **Endpoint**: `/friend-request/respond/<int:request_id>/`
- **Method**: `PUT`
- **Headers**:
  
  ```
  Authorization: Bearer `<access_token>`
  ```

#### Accept

- **Payload**:
``` json
{
  "id": <request_id>,
  "from_user": {
    "id": <user_id>,
    "username": "<username>",
    "email": "<user email>"
  },
  "to_user": {
    "id": <user_id>
  },
  "status": "accepted"
}
```

#### Reject

- **Payload**:
``` json
{
  "id": <request_id>,
  "from_user": {
    "id": <user_id>,
    "username": "<username>",
    "email": "<user email>"
  },
  "to_user": {
    "id": <user_id>
  },
"status": "rejected"
    }
```

### List Friends

- **Endpoint**: `/friends/`
- **Method**: `GET`
- **Headers**:
  
  ```
  Authorization: Bearer `<access_token>`
  ```

### List Pending Friend Requests

- **Endpoint**: `/friend-requests/pending/`
- **Method**: `GET`
- **Headers**:
  
  ```
  Authorization: Bearer `<access_token>`
  ```


## Postman Collection

You can import the provided Postman collection to test the API endpoints. The collection includes examples for all endpoints. You can download it from [here](https://www.postman.com/athulrajagopal/workspace/accunox/collection/27782030-26f06caa-9e12-4ff4-9d0a-696645e8d1e2?action=share&creator=27782030)

.



