from flask import Flask, request, jsonify
import mysql.connector
from functools import wraps
import time
import hashlib
import random
import string

# ---------------- TEST ONLY -----------------
from flask_cors import CORS
# ---------------- TEST ONLY -----------------


# Declare the Flask app variable
app = Flask(__name__)

# ---------------- TEST ONLY -----------------
CORS(app)
# ---------------- TEST ONLY -----------------

# Basic logger function, to log Api requests
def logRequestActivity(client_ip, requested_path):
    with open('logs/apilogs.log', 'a', encoding='UTF-8') as logfile:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logfile.write(f"[{current_time}] [INFO] API Access attempt from {client_ip} to {requested_path}\n")

# Logger for general information logging
def generalLog(client_ip, message):
    with open('logs/generallog.log', 'a', encoding='UTF-8') as logfile:
        current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
        logfile.write(f"[{current_time}] [INFO] User with {client_ip} IP, {message}\n")
 
# Hash the api key using SHA256 before passing it to the sql query part
def hashApiKey(apiKey):
    hasher = hashlib.sha256()
    hasher.update(apiKey.encode('utf-8'))
    return hasher.hexdigest()

# Generate an Api key with the default length of 20
def generateApiKey(length=20):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

# Decorator factory to fetch Api keys from the database,
# and to require a certain access level for different endpoints
def requireAuthentication(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr
            requested_path = request.path
            logRequestActivity(client_ip, requested_path)
            
            try:
                if 'X-API-KEY' in request.headers:
                    mydb = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="",
                        database="users"
                    )

                    mycursor = mydb.cursor()
                    sql_query = "SELECT access_level FROM users WHERE api_key = %s"
                    mycursor.execute(sql_query, (hashApiKey(request.headers.get('X-API-KEY')),))
                    apiQuery = mycursor.fetchone()
                    mycursor.close()
                    mydb.close()

                    if apiQuery is not None and apiQuery[0] >= level:
                        return func(*args, **kwargs)
                    elif not apiQuery:
                        generalLog(request.remote_addr, message=f"tried to access the {requested_path} endpoint, but the provided API key cannot be found!")
                        return jsonify({"error": "Unauthorized"}), 401
                    elif apiQuery[0] < level:
                        generalLog(request.remote_addr, message=f"tried to access the {requested_path} endpoint, but their access level didn't meet the required level.")
                        return jsonify({"error": "Insufficient permission"}), 403
                else:
                    generalLog(request.remote_addr, message=f"tried to access the {requested_path} endpoint, but they didn't provide an API key.")
                    return jsonify({"error": "Unauthorized!"}), 401
            except mysql.connector.errors.InterfaceError:
                generalLog(request.remote_addr, message=f"tried to access the {requested_path} endpoint, but the SQL server is down.")
                return jsonify({"error": "Internal SQL server error!"}), 500
        return wrapper
    return decorator

# Test route, not used
@app.route("/authorize")
@requireAuthentication(1)
def basicAuth():
    return "Authorized!"

# Test route, not used
@app.route("/router")
@requireAuthentication(3)
def router():
    return "Authorized!"

# Route used to register a new Api user into the database, 
# and send the generated Api key as the response
# NOTE: It requires access level 3 to use this endpoint
@app.route("/register")
@requireAuthentication(3)
def registerUser():
    if "User-Name" in request.headers and "Access-Level" in request.headers:
        access_level = request.headers.get('Access-Level', '')
        
        if access_level.isdigit():
            newApiKey = generateApiKey(length=20)
            newHashedApiKey = hashApiKey(newApiKey)
            try:
                mydb = mysql.connector.connect(
                    host="localhost",
                    user="root",
                    password="",
                    database="users"
                )

                mycursor = mydb.cursor()
                sql_query = "INSERT INTO users (user_name, api_key, access_level) VALUES (%s, %s, %s)"
                mycursor.execute(sql_query, (request.headers.get('User-Name'), newHashedApiKey, request.headers.get('Access-Level')))
                mydb.commit()
                mycursor.close()
                mydb.close()
                
                response = f"The following API key: {newApiKey} had been generated for user {request.headers.get('UsrName')}\nDONT lose this key, as it isn't recoverable!"
                generalLog(request.remote_addr, message=f"registered a new user, with the name: {request.headers.get("User-Name")}, API key (hashed): {newHashedApiKey}, and access level: {request.headers.get("Access-Level")}")
                return response
            except mysql.connector.errors.ProgrammingError:
                return jsonify({"error": "Internal SQL server error!"}), 500
        else:
            generalLog(request.remote_addr, message=f"tried to access the {request.path} endpoint, but they provided an invalid Access-Level!")
            return jsonify({"error": "Bad request!"}), 400
    else:
        generalLog(request.remote_addr, message=f"tried to access the {request.path} endpoint, but they didn't provide User-Name and/or Access-Level.")
        return jsonify({"error": "Bad request!"}), 400

# Run the entire Flask app in debug mode
# NOTE: Turn off debug mode if in production!
if __name__ == "__main__":
    app.run(debug=True)