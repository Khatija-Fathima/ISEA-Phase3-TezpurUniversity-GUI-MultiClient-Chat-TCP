import socket
import threading

HOST = input("Server IP: ")
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter Username: ")
client.send(username.encode())

print("\n========== COMMANDS ==========")
print("/msg username message")
print("/all message")
print("/group create groupname")
print("/group join groupname")
print("/group groupname message")
print("/list")
print("==============================\n")


def receive():
    while True:
        try:
            message = client.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server.")
            break


def write():
    while True:
        try:
            message = input()
            client.send(message.encode())
        except:
            break


threading.Thread(target=receive, daemon=True).start()
write()
