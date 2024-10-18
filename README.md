
# Flask RESTful API with MySQL Integration

## Overview

This repository provides a RESTful API built using Flask, integrated with MySQL for user management and API key authentication. It supports different levels of access for API keys, ensuring secure access to various endpoints. The API allows user registration, API key generation, and request logging.

## Features

- **API Key Authentication**: Every request is authenticated using API keys, with different access levels (1 to 3).
- **User Management**: Users can be registered via the API, and their API keys are stored in a MySQL database.
- **Access Control**: Specific endpoints require higher access levels.
- **Logging**: Logs API requests and general information to files for monitoring purposes.
- **CORS Support**: CORS is enabled for testing purposes, allowing cross-origin requests.
- **API Key Generation**: Automatically generates new API keys for users during registration.
- **SQL-Based User Storage**: Users, their API keys, and access levels are stored in a MySQL database.

## File Structure

- **apikeys.txt**: Example of generated API keys and their respective access levels.
- **restful_api.py**: The main Flask application containing the API logic and authentication mechanism.
- **users.sql**: SQL file for setting up the `users` table in a MySQL database.
- **logs/**: Directory to store API and general logs (created dynamically during execution).
- **test_site/index.html**: A simple HTML (and provided JavaScript file) for testing API functionality.

## Prerequisites

- Python 3.x
- Flask (`pip install Flask`)
- Flask-CORS (`pip install Flask-CORS`)
- MySQL (with a database named `users`)
- MySQL Connector (`pip install mysql-connector-python`)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Levy-Y/api-template
cd api-template
``` 

### 2. Install Dependencies

```bash
pip install Flask Flask-CORS mysql-connector-python
``` 

### 3. MySQL Setup

1.  Create a MySQL database named `users`.
2.  Use the provided `users.sql` script to create the necessary table and insert initial users:

```bash
mysql -u root -p users < users.sql
``` 

This will create a `users` table with the following fields:

-   `user_name`: Stores the username of the API key owner.
-   `api_key`: Stores the hashed version of the API key.
-   `access_level`: Defines the access level (1, 2, or 3).

### 4. Running the Flask App

Start the Flask application in development mode:

```bash
python restful_api.py
```

The app will run by default in `debug` mode. For production, remember to disable debug mode.

### 5. API Key Example (Optional)

The `apikeys.txt` file contains sample API keys with their corresponding access levels:

-   Level 3: Highest access level, can register new users and access protected routes.
-   Lower levels have limited access to certain endpoints.

## API Endpoints

### 1. `/authorize` [GET]

-   **Description**: Verifies if the user is authorized with at least level 1 access.
-   **Headers**: Requires `X-API-KEY`.
-   **Access Level**: 1
-   **Response**: `"Authorized!"` if access is granted.

### 2. `/router` [GET]

-   **Description**: Verifies if the user is authorized with at least level 3 access.
-   **Headers**: Requires `X-API-KEY`.
-   **Access Level**: 3
-   **Response**: `"Authorized!"` if access is granted.

### 3. `/register` [GET]

-   **Description**: Registers a new API user and generates an API key.
-   **Headers**:
    -   `X-API-KEY`: An API key with level 3 access.
    -   `User-Name`: The name of the new user.
    -   `Access-Level`: The access level for the new user (1, 2, or 3).
-   **Access Level**: 3
-   **Response**: The newly generated API key. It is only displayed once and not recoverable later.
-   **Example**:
    
    ```json
    {
      "User-Name": "NewUser",
      "Access-Level": "2"
    }
    ``` 
    

## Logging

Logs are written to the `logs` directory with two separate log files:

1.  **apilogs.log**: Logs API request activities, including client IPs and accessed paths.
2.  **generallog.log**: Logs general events, such as unauthorized access attempts and registration events.

## Security

-   **API Key Hashing**: API keys are hashed using SHA-256 before being stored in the database, ensuring security.
-   **Access Control**: The API restricts access based on the user's access level. Unauthorized or insufficient permission attempts are logged.

## Development Notes

-   **CORS**: CORS is enabled for testing purposes using `Flask-CORS`. Ensure to disable or configure it appropriately in production environments.
-   **Debug Mode**: The app runs in debug mode for development. Disable it for production by setting `debug=False` in `app.run()`.

## License

This project is licensed under the GNU General Public License v3.0 License. See the LICENSE file for details.
