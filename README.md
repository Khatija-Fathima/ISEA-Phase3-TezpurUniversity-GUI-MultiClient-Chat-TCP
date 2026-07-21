# ISEA-Phase3-TezpurUniversity

# SentinelChat – Secure GUI-Based Multi-Client TCP Chat Application

**Submitted by:** Khatija Fathima  
**Roll No.:** 323506402225  
**Institution:** Andhra University (B.Tech Computer Science & Engineering - Cybersecurity)  
**Internship:** ISEA Summer Internship 2026, Tezpur University

---

# Project Overview

SentinelChat is a Secure GUI-Based Multi-Client TCP Chat Application developed using Python Socket Programming and Tkinter.

The project was initially developed as a multi-client TCP chat application and enhanced during **Assignment 7** by implementing practical security mechanisms including secure authentication, SHA-256 password hashing, duplicate login prevention, account lockout, session timeout, secure logging, and TCP packet verification using Wireshark.

In **Assignment 8**, the same application was further optimized by improving connection management, reliability, scalability, configuration management, resource handling, and performance evaluation while preserving all previously implemented security features. The application was optimized rather than redesigned, following the Assignment 8 guidelines.

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

---

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
- Clients vs Throughput
- Message Type Distribution

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
