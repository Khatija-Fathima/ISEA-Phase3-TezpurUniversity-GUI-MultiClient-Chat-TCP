# SentinelChat
### Secure GUI-Based Multi-Client TCP Chat Application

![Python](...)
![TCP](...)
![Tkinter](...)
![Socket Programming](...)
![ISEA Internship](...)

**Submitted by:** Khatija Fathima  
**Roll No.:** 323506402225  
**Institution:** Andhra University (B.Tech Computer Science & Engineering - Cybersecurity)  
**Internship:** ISEA Summer Internship 2026, Tezpur University

---

# Project Overview

SentinelChat is a Secure GUI-Based Multi-Client TCP Chat Application developed using Python Socket Programming and Tkinter.


The project was initially developed as a multi-client TCP chat application and enhanced during **Assignment 7** by implementing practical security mechanisms including secure authentication, SHA-256 password hashing, duplicate login prevention, account lockout, session timeout, secure logging, and TCP packet verification using Wireshark.

In **Assignment 8**, the same application was further optimized by improving connection management, reliability, scalability, configuration management, resource handling, and performance evaluation while preserving all previously implemented security features. The application was optimized rather than redesigned, following the Assignment 8 guidelines.


# Application Preview


Login Window Screenshot


<img width="722" height="885" alt="login" src="https://github.com/user-attachments/assets/2d2b1195-1a20-480c-a4b3-f42900f99f55" />

<img width="702" height="877" alt="LOGINS~1" src="https://github.com/user-attachments/assets/bade77ef-1eca-4b33-b09e-c50e29849276" />

Dashboard Screenshot


<img width="1912" height="1020" alt="DASHBO~1" src="https://github.com/user-attachments/assets/4cd05392-2284-4841-ac77-b6b8684f7584" />

Private Chat Screenshot


<img width="1917" height="1022" alt="PRIVAT~1" src="https://github.com/user-attachments/assets/931f88e7-b2ac-48de-94cf-3c90bd9f51ae" />

<img width="1917" height="1035" alt="PRIVAT~2" src="https://github.com/user-attachments/assets/9aef7045-b147-4fd4-aec1-a7f0ce220d6f" />

Group Chat Screenshot


<img width="1195" height="902" alt="GROUP_1" src="https://github.com/user-attachments/assets/ce21c866-8749-4a0c-8f5e-2424431cc140" />

<img width="1192" height="902" alt="GROUP_2" src="https://github.com/user-attachments/assets/69cd1c6e-65a9-4002-9140-165495cff320" />

<img width="1912" height="1031" alt="GROUP_4" src="https://github.com/user-attachments/assets/85bd6056-7d41-4bc4-af9f-d9598d5b166f" />

<img width="1917" height="1076" alt="GROUP_~1" src="https://github.com/user-attachments/assets/7faaed8e-b9b1-4ab6-863f-ad81963ef0b2" />


---

# Assignment 7 Security Features (Retained)

- Secure User Authentication
- SHA-256 Password Hashing
- Duplicate Login Prevention
- Account Lock after Multiple Failed Login Attempts
- Countdown Timer During Account Lock
- Show / Hide Password
- Session Timeout after Inactivity
- Secure Event Logging
- Input Validation
- Wireshark TCP Packet Verification

---

# Assignment 8 Optimizations

### Connection Management

- Automatic Client Cleanup
- Proper Socket Resource Management
- Graceful Client Disconnection Handling
- SO_REUSEADDR Socket Reuse

### Reliability Improvements

- Graceful Shutdown
- Improved Exception Handling
- Better Session Timeout Handling
- Stable Client Connection Management

### Scalability Improvements

- Multi-threaded Client Handling
- Improved Thread Management
- Support for Multiple Concurrent Clients
- Enhanced Resource Utilization

### Configuration Management

- Runtime Configuration using `config.json`
- Removal of Hardcoded Configuration Values
- Configurable Host, Port, Buffer Size and Timeout

### Performance Evaluation

- Delay Analysis
- Throughput Analysis
- CPU Utilization Analysis
- Memory Utilization Analysis
- Performance Graph Generation
- Performance Results stored in `performance_results.csv`

---

# Existing Chat Features

| Feature              | Status |
| -------------------- | ------ |
| Login Authentication | ✅     |
| Broadcast            | ✅     |
| Private Chat         | ✅     |
| Group Chat           | ✅     |
| Online Users         | ✅     |
| Chat History         | ✅     |
| Session Timeout      | ✅     |


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
- Configurable JSON Configuration (`config.json`)

# System Architecture

Client

↓

Server

↓

Authentication

↓

Broadcast

↓

Private

↓

History

↓

CSV

↓

Logs


# Project Structure

```
server.py                      Main TCP Server
client_gui.py                  Login Window
dashboard.py                   Main Dashboard
broadcast.py                   Broadcast Messaging
private_chat.py                Private Chat
group_chat.py                  Group Chat
history.py                     Chat History
status.py                      Server Status Dashboard

config.json                    Runtime Configuration
users.json                     User Credentials
chat_history.csv               Chat History
security_log.txt               Security Log
performance_results.csv        Performance Results

Assignment8_Report.pdf         Project Report
Assignment8_Wireshark.pcapng   Wireshark Packet Capture

GUI_SCREENSHOTS/               GUI Images
SCREENSHOTS/                   Network Screenshots
Graphs/                        Performance Graphs
```

---

# Security Implementation

### Authentication

- Username and Password Verification
- SHA-256 Password Storage
- Duplicate Login Detection

### Account Protection

- Limited Login Attempts
- Temporary Account Lock
- Lock Countdown Timer

### Session Management

- Automatic Session Timeout
- Secure Logout
- Session Monitoring

### Logging

Security events recorded include:

- Successful Login
- Failed Login
- Duplicate Login
- Account Lock
- Session Timeout
- User Logout

---

# Network Verification

The application traffic was verified using **Wireshark**.

Verified TCP Operations:

- TCP Three-Way Handshake
- Authentication Packets
- Broadcast Messaging
- Private Chat
- Group Chat
- Connection Termination
  
<img width="1917" height="1022" alt="WHIRES~1" src="https://github.com/user-attachments/assets/72967435-fb32-4018-bb98-243df6944ad0" />


<img width="1917" height="1026" alt="WHIRES~2" src="https://github.com/user-attachments/assets/5f95fae7-cf16-4f2f-ad79-2336aa77fcd6" />


<img width="1917" height="1020" alt="WHIRES~3" src="https://github.com/user-attachments/assets/6819c14d-97e9-4c56-b70a-3b9f096ddc3f" />


<img width="1917" height="1035" alt="WHIRES~4" src="https://github.com/user-attachments/assets/1cd51d96-a1d3-490a-93ef-c0f8548bc6ab" />


<img width="1917" height="1027" alt="WHC3D5~1" src="https://github.com/user-attachments/assets/76f598ba-f691-4946-ade1-3047d38b51de" />


<img width="1917" height="1032" alt="WIRESH~2" src="https://github.com/user-attachments/assets/7143d995-b507-4a44-918b-dd394354d2b9" />


<img width="1452" height="1020" alt="WIRESH~1" src="https://github.com/user-attachments/assets/79e84e52-c45e-4d9e-a1fd-e7521247c8f2" />


---

# Performance Evaluation

The optimized application was evaluated using multiple concurrent client instances.

Performance metrics measured include:

- Communication Delay
- Throughput
- CPU Utilization
- Memory Utilization

Performance results were recorded in:

- `performance_results.csv`

Generated Graphs:

- Clients vs Delay


  <img width="600" height="400" alt="CLIENT~1" src="https://github.com/user-attachments/assets/09ba4f3b-d0e2-40ed-aa00-391f6df61ffe" />

- Clients vs Throughput

  
  <img width="600" height="400" alt="CLIENT~2" src="https://github.com/user-attachments/assets/b4d97add-3acf-42d8-93ce-12cd0da38fd8" />

  
- Message Type Distribution

  
  <img width="600" height="400" alt="MESSAG~1" src="https://github.com/user-attachments/assets/02d396e6-3b2a-4533-9ea3-a032d1d1598f" />


---

# Assignment Deliverables

- Complete Python Source Code
- Optimized GUI-Based Multi-Client TCP Application
- Configuration File (`config.json`)
- Performance Results (`performance_results.csv`)
- Assignment 8 Report
- Wireshark Packet Capture
- GUI Screenshots
- Performance Graphs
- Handwritten Reflection

---

# Learning Outcomes

This project provided practical experience in:

- TCP Socket Programming
- Client-Server Architecture
- Secure Authentication
- Network Security
- Multi-threaded Programming
- Connection Management
- Reliability Enhancement
- Scalability Optimization
- Configuration Management
- Performance Analysis
- Wireshark Packet Inspection

---

Installation

git clone ...

cd ...

pip install ...

python server.py

python client_gui.py

------

# Developed During

**ISEA Summer Internship 2026**

Department of Computer Science & Engineering

**Tezpur University**

---

## Author

**Khatija Fathima**

B.Tech Computer Science & Engineering (Cybersecurity)

Andhra University

---

## Assignment Status

✅ Assignment 7 Completed

✅ Assignment 8 Completed

This repository contains the final optimized version of **SentinelChat**, developed during the **ISEA Summer Internship 2026** at **Tezpur University**, incorporating both the security enhancements from Assignment 7 and the optimization, scalability, and reliability improvements from Assignment 8.
