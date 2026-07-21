import socket
import threading
import os
import json
import hashlib
from datetime import datetime, timedelta
import time



with open("config.json", "r") as file:
    config = json.load(file)

HOST = config["SERVER_HOST"]
PORT = config["SERVER_PORT"]
BUFFER_SIZE = config["BUFFER_SIZE"]
SESSION_TIMEOUT = config["SESSION_TIMEOUT"]
MAX_LOGIN_ATTEMPTS = config["MAX_LOGIN_ATTEMPTS"]
LOCK_TIME = config["LOCK_TIME"]
MAX_CLIENTS = config["MAX_CLIENTS"]


last_activity = time.time()


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(MAX_CLIENTS)

clients = []
usernames = {}
logged_in_users = set()

failed_attempts = {}
blocked_users = {}


client_info = {}

groups = {}

clients_lock = threading.Lock()

private_message_count = 0
broadcast_message_count = 0

def load_users():
    """
    Load user credentials from users.json.
    Returns a dictionary of users.
    """
    if not os.path.exists("users.json"):
        return {}

    with open("users.json", "r") as file:
        return json.load(file)


def authenticate_user(username, password):

    data = load_users()

    users = data.get("users", {})

    print("\n========== LOGIN DEBUG ==========")
    print("Username :", username)
    print("Password received.")

    if username not in users:
        print("❌ USER NOT FOUND")
        return False

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    print("Generated Hash :", hashed_password)
    print("Stored Hash    :", users[username]["password"])

    if hashed_password == users[username]["password"]:
        print("✅ PASSWORD MATCH")
        return True

    print("❌ PASSWORD DOES NOT MATCH")
    return False



def log_chat(sender, receiver, message_type, message):

    file_exists = os.path.exists("chat_history.csv")

    with open("chat_history.csv", "a") as f:

        if not file_exists:
            f.write("timestamp,sender,receiver,message_type,message\n")

        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        f.write(f"{t},{sender},{receiver},{message_type},{message}\n")
        
def show_last_messages(client, username):

    if not os.path.exists("chat_history.csv"):
        return

    messages = []

    with open("chat_history.csv", "r") as f:

        next(f, None)

        for line in f:

            parts = line.strip().split(",", 4)

            if len(parts) == 5:

                timestamp, sender, receiver, msg_type, message = parts

                if sender == username:

                    messages.append(
                        f"{timestamp} [{msg_type}] -> {receiver}: {message}"
                    )

    if messages:

        client.send("\n===== LAST 5 MESSAGES =====\n".encode())

        for msg in messages[-5:]:

            client.send((msg + "\n").encode())

        client.send("===========================\n".encode())        
        

def broadcast(message, sender):

    with clients_lock:
        for client in clients.copy():
            if client != sender:

                try:
                    client.send(message.encode())

                except (ConnectionResetError, BrokenPipeError, OSError):

                    print(f"Broadcast failed. Cleaning up client...")

                    cleanup_client(client)

                    
def private_message(sender, receiver_name, message):

    global private_message_count

    for client in usernames:

        if usernames[client] == receiver_name:

            client.send(f"[PRIVATE] {sender}: {message}".encode())

            private_message_count += 1

            return True

    return False


def broadcast_all(sender, message):

    global broadcast_message_count

    for client in clients.copy():

        try:
            client.send(f"[BROADCAST] {sender}: {message}".encode())

        except (ConnectionResetError, BrokenPipeError, OSError):

            print("Broadcast client disconnected.")

            cleanup_client(client)

    broadcast_message_count += 1


def create_group(group):

    if group not in groups:

        groups[group] = []
        return True

    return False


def join_group(client, group):

    if group in groups:

        if client not in groups[group]:

            groups[group].append(client)


def group_message(sender, group, message):

    if group in groups:

        for member in groups[group].copy():

            try:
                member.send(
                    f"[GROUP {group}] {sender}: {message}".encode()
                )

            except (ConnectionResetError, BrokenPipeError, OSError):

                print("Group member disconnected.")

                cleanup_client(member) 

def cleanup_client(client):

    username = usernames.get(client)

    try:
        client.close()
    except OSError:
        pass

    if client in clients:
        clients.remove(client)

    if client in usernames:
        del usernames[client]

    if username in logged_in_users:
        logged_in_users.remove(username)

    if client in client_info:
        client_info[client]["status"] = "Offline"
        del client_info[client]

    for group in groups.values():
        if client in group:
            group.remove(client)

    if username:
        security_log("LOGOUT", username)
        print(f"{username} disconnected and cleaned up.")            

                    
def handle_client(client):

    username = usernames[client]

    last_activity = time.time()

    client.settimeout(1)
    while True:
        try:
            message = client.recv(BUFFER_SIZE).decode()
            print("=" * 60)
            print(repr(message)) 
            if not message:
                break
            last_activity = time.time()

            # Private Message
            if message.startswith("/msg"):

                parts = message.split(" ", 2)

                if len(parts) == 3:

                    receiver = parts[1]
                    text = parts[2]

                    log_chat(username, receiver, "PRIVATE", text)

                    if not private_message(username, receiver, text):
                        client.send("User not found.".encode())

            # List Online Users
            elif message == "/list":

                online_users = "\n".join(usernames.values())

                client.send(f"Online Users:\n{online_users}".encode())

            # Broadcast
            elif message.startswith("/all"):

                text = message[5:]

                log_chat(username, "ALL", "BROADCAST", text)

                broadcast_all(username, text)

            # Create Group
            elif message.startswith("/group create"):

                parts = message.split()

                if len(parts) == 3:

                    if create_group(parts[2]):

                        log_chat(username, parts[2], "GROUP_CREATE", "Group Created")

                        client.send("Group created.".encode())

                    else:

                        client.send("Group already exists.".encode())

            # Join Group
            elif message.startswith("/group join"):

                parts = message.split()

                if len(parts) == 3:

                    join_group(client, parts[2])

                    log_chat(username, parts[2], "GROUP_JOIN", "Joined Group")

                    client.send("Joined group.".encode())

            # Group Message
            elif message.startswith("/group"):

                parts = message.split(" ", 2)

                if len(parts) == 3:

                    group = parts[1]
                    text = parts[2]

                    log_chat(username, group, "GROUP", text)

                    group_message(username, group, text)

            # Normal Chat
            else:

                log_chat(username, "ALL", "NORMAL", message)

                broadcast(f"[{username}] {message}", client)

        except socket.timeout:
            print(f"Timeout check for {username}: {int(time.time() - last_activity)} seconds")

            if time.time() - last_activity >= SESSION_TIMEOUT:
                try:
                    security_log("SESSION TIMEOUT", username)
                    print(f"Session expired for {username}")
                    client.send("SESSION_TIMEOUT".encode())
                except:
                    pass
                break

            continue
        except:
            break

    t = datetime.now().strftime("%H:%M:%S")
    print(f"{t},DISCONNECTED,{username}")

    cleanup_client(client)

def receive():

    print(f"Server running on port {PORT}")

    while True:

        client, address = server.accept()

        login_data = client.recv(BUFFER_SIZE).decode()

        parts = login_data.split("|")

        if len(parts) != 3 or parts[0] != "LOGIN":
            client.send("LOGIN_FAILED".encode())
            client.close()
            continue

        username = parts[1]
        password = parts[2]

        # Check if user is temporarily blocked
        if username in blocked_users:
            if datetime.now() < blocked_users[username]:
                client.send("ACCOUNT_LOCKED".encode())
                client.close()
                continue
            else:
                del blocked_users[username]
                failed_attempts[username] = 0

        # Authenticate
        
        if not authenticate_user(username, password):
            security_log("LOGIN FAILED", username)
            failed_attempts[username] = failed_attempts.get(username, 0) + 1
            if failed_attempts[username] >= MAX_LOGIN_ATTEMPTS:
                security_log("ACCOUNT LOCKED", username)
                blocked_users[username] = datetime.now() + timedelta(seconds=LOCK_TIME)
                client.send("ACCOUNT_LOCKED".encode())
            else:
                client.send("LOGIN_FAILED".encode())
            client.close()
            continue

        # Successful login
        failed_attempts[username] = 0

        if username in logged_in_users:
            security_log("DUPLICATE LOGIN", username)
            client.send("DUPLICATE_LOGIN".encode())
            client.close()
            continue

        security_log("LOGIN_SUCCESS", username)

        logged_in_users.add(username)

        client.send("LOGIN_SUCCESS".encode())

        usernames[client] = username

        show_last_messages(client, username)

        client_info[client] = {
            "username": username,
            "ip": address[0],
            "port": address[1],
            "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "status": "Online"
        }

        with clients_lock:
            clients.append(client)


        t = datetime.now().strftime("%H:%M:%S")
        print(f"{t},CONNECTED,{username},{address[0]}")

        print("\n========== CLIENT INFO ==========")
        print(f"Username   : {client_info[client]['username']}")
        print(f"IP Address : {client_info[client]['ip']}")
        print(f"Port       : {client_info[client]['port']}")
        print(f"Login Time : {client_info[client]['login_time']}")
        print(f"Status     : {client_info[client]['status']}")
        print("=================================\n")

        thread = threading.Thread(
    target=handle_client,
    args=(client,),
    daemon=True
)
        thread.start()

def security_log(event, username):
    """
    Log security-related events.
    """
    with open("security_log.txt", "a", encoding="utf-8") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {event} : {username}\n")
        
try:
    receive()

except KeyboardInterrupt:

    print("\n")
    print("========= SERVER STATISTICS =========")
    print(f"Private Messages : {private_message_count}")
    print(f"Broadcast Messages : {broadcast_message_count}")
    print(f"Groups Created : {len(groups)}")
    print(f"Connected Clients : {len(clients)}")
    print("====================================")

    print("\nShutting down server...")

    for client in clients.copy():
        try:
            client.close()
        except OSError:
            pass

    server.close()

    print("Server shutdown completed.")    
