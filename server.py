import socket
import threading
import os
from datetime import datetime

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}

client_info = {}

groups = {}

private_message_count = 0
broadcast_message_count = 0

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
    for client in clients:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                client.close()
                if client in clients:
                    clients.remove(client)
                    
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

    for client in clients:

        try:
            client.send(f"[BROADCAST] {sender}: {message}".encode())
        except:
            pass

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

        for member in groups[group]:

            try:
                member.send(f"[GROUP {group}] {sender}: {message}".encode())
            except:
                pass                    
                    
def handle_client(client):

    username = usernames[client]

    while True:

        try:

            message = client.recv(1024).decode()

            if not message:
                break

 

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
        except:
            break

    t = datetime.now().strftime("%H:%M:%S")
    print(f"{t},DISCONNECTED,{username}")

    client.close()

    if client in client_info:
       client_info[client]["status"] = "Offline"

    if client in clients:
       clients.remove(client)

    if client in usernames:
       del usernames[client]
        
def receive():

    print(f"Server running on port {PORT}")

    while True:

        client, address = server.accept()

        username = client.recv(1024).decode()

        usernames[client] = username
        
        show_last_messages(client, username)
        
        client_info[client] = {
               "username": username,
               "ip": address[0],
               "port": address[1],
               "login_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "status": "Online"
        }

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

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()    
        
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
           
