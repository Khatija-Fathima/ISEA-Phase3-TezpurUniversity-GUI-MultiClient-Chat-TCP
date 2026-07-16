# ISEA-Phase3-TezpurUniversity

# SentinelChat  – Secure GUI-Based Multi-Client TCP Chat Application

**Submitted by:** Khatija Fathima  
**Roll No.:** 323506402225  
**Institution:** Andhra University (B.Tech CSE - Cybersecurity)  
**Internship:** ISEA Summer Internship 2026, Tezpur University

---

# Project Overview

SentinelChat is a Secure Multi-Client TCP Chat Application developed using Python Socket Programming and Tkinter GUI.

This project was initially developed as a GUI-based chat application and later enhanced in **Assignment 7** by implementing multiple security mechanisms including secure authentication, password hashing, duplicate login prevention, session timeout, account lockout, secure logging, and network packet analysis using Wireshark.

---

# Assignment 7 Security Features

- Secure User Authentication
- SHA-256 Password Hashing
- Duplicate Login Prevention
- Account Lock after 5 Failed Login Attempts
- Countdown Timer During Account Lock
- Show / Hide Password
- Session Timeout after 3 Minutes of Inactivity
- Secure Event Logging
- Input Validation
- Wireshark TCP Packet Verification

---

# Existing Chat Features

- Multi-Client TCP Communication
- Broadcast Messaging
- Private Chat
- Group Chat
- Chat History Viewer
- Server Status Dashboard
- Online User List
- Modern Tkinter GUI

---

# Technologies Used

- Python 3
- TCP Socket Programming
- Tkinter
- Threading
- JSON
- CSV
- hashlib (SHA-256)
- Wireshark

---

# Project Structure

```
server.py                TCP Server
client_gui.py            Secure Login Window
dashboard.py             Main Dashboard
broadcast.py             Broadcast Messaging
private_chat.py          Private Chat Module
group_chat.py            Group Chat Module
history.py               Chat History
status.py                Server Status Dashboard
cyber_bg.py              Animated Background
ui_fx.py                 GUI Effects
users.json               User Credentials
chat_history.csv         Chat History
security_log.txt         Security Events
Assignment7_Report.pdf   Project Report
Assignment7_Wireshark.pcapng  Wireshark Capture
GUI_SCREENSHOTS/         GUI Images
SCREENSHOTS/             Network Images
Graphs/                  Performance Graphs
```

---

# Security Implementation

### Authentication

- Username and Password Verification
- SHA-256 Password Storage
- Duplicate Login Detection

### Account Protection

- Maximum 5 Login Attempts
- Automatic Account Lock
- Live Countdown Timer

### Session Management

- Automatic Logout after 3 Minutes of Inactivity

### Logging

Security events recorded include:

- Successful Login
- Failed Login
- Duplicate Login Attempts
- Account Lock
- Session Timeout
- User Logout

---

# Network Verification

The application traffic was verified using **Wireshark**.

Verified TCP Operations:

- TCP Three-Way Handshake
- Authentication Packets
- Broadcast Communication
- Private Chat
- Group Chat
- Session Termination

---

# Performance Testing

Tested with multiple simultaneous clients.

Performance graphs include:

- Clients vs Delay
- Clients vs Throughput
- Message Type Distribution

---

# Assignment Deliverables

- Complete Python Source Code
- Secure GUI Application
- Assignment Report
- Wireshark Packet Capture
- GUI Screenshots
- Network Screenshots
- Performance Graphs

---

# Developed During

ISEA Summer Internship 2026

Tezpur University

---

## Author

**Khatija Fathima**

B.Tech Computer Science & Engineering (Cybersecurity)

Andhra University
