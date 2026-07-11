# ISEA-GUI-MultiClient-Chat-TCP
GUI-Based Multi-Client Chat Application using TCP Socket Programming developed during the ISEA Summer Internship 2026 at Tezpur University.


# ISEA-Phase3-TezpurUniversity

## SentinelChat — GUI-Based Multi-Client Chat Application Using TCP

**Submitted by:** Khatija Fathima
**Roll No.:** 323506402225
**Institution:** Andhra University (B.Tech CSE - Cybersecurity)
**Internship:** ISEA Summer Internship 2026, Tezpur University

---

## Project Title
SentinelChat v2.0 — GUI-Based Multi-Client TCP Chat Application

## Objective
Convert the terminal-based TCP chat application from Assignment 5 into a polished graphical desktop application using Python Tkinter, while reusing the existing server and socket communication logic unchanged.

## Software Requirements
- Python 3.8+
- tkinter (built-in, no install needed)
- socket (built-in)
- threading (built-in)
- No external pip packages required

## Network Topology

```
h1 = Chat Server  →  runs server.py
h2 = Client A     →  runs client_gui.py
h3 = Client B     →  runs client_gui.py
h4 = Client C     →  runs client_gui.py
h5 = Client D     →  runs client_gui.py

All connected through switch s1
```

Mininet command:
```
sudo mn --topo single,5
```

## Execution Steps

```bash
# Step 1 — Start the server on h1
python3 server.py

# Step 2 — Start the GUI client on h2, h3, h4, h5
python3 client_gui.py

# Step 3 — In the login window:
#   Enter Server IP: 10.0.0.1
#   Enter Username: (your name)
#   Click CONNECT
```

## Features

| Feature | How to Use |
|---------|-----------|
| Login | Enter server IP + username, click CONNECT |
| Dashboard | Click any card to open that feature |
| Broadcast | Type message, click SEND BROADCAST — goes to all users |
| Private Chat | Select user from list, type message, click SEND |
| Group Chat | Click Create Group or Join Group, then send messages |
| Chat History | Search and filter all past messages |
| Server Status | Live message counts, CPU/MEM bars, activity log |
| Disconnect | Click Disconnect card on dashboard |

## File Structure

```
├── server.py           — TCP server (reused from Assignment 5, unchanged)
├── client_gui.py       — Login window
├── dashboard.py        — Main dashboard with animated cards
├── broadcast.py        — Broadcast messaging window
├── private_chat.py     — Private one-to-one chat with bubbles
├── group_chat.py       — Group chat with create/join
├── history.py          — Chat history viewer with search
├── status.py           — Server analytics dashboard
├── cyber_bg.py         — Animated particle background
├── ui_fx.py            — Shared animation helpers (GlowPulse, bubbles)
├── client.py           — Original terminal client (kept for testing)
├── chat_history.csv    — Persisted message log
├── performance_results.csv — Performance experiment data
├── screenshots/        — All GUI screenshots
└── report.pdf          — Full assignment report
```

## Implementation Notes

- **server.py is 100% unchanged** from Assignment 5
- All TCP commands are the same: `/msg`, `/all`, `/list`, `/group create`, `/group join`
- Background thread handles `client.recv()` — GUI never blocks
- `root.after(0, callback, msg)` used to safely update GUI from receive thread
- Animations use `Canvas` widgets + `root.after(30)` loops (~30fps)
- `GlowPulse` class in `ui_fx.py` provides breathing border effects
- Chat bubbles use `tk.Text` tag_config with `lmargin`/`rmargin` — no Canvas needed

## Screenshots

Screenshots are in the `screenshots/` folder covering:
- Login window
- Dashboard
- Broadcast messaging
- Private chat (two users)
- Group chat (four users)
- Chat history
- Server status
- Disconnect dialog
