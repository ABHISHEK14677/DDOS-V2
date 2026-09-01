# ⚡ DDOS-V2

> **Multi-Vector Network Stress Testing Tool — Authorized Lab Use Only**

DDOS-V2 is a Python-based network stress-testing project designed for **authorized security labs and systems you own or have explicit permission to test**.

The project provides multiple traffic-generation modes, configurable concurrency, duration controls, rate ceilings, live statistics, and an interactive terminal interface.

---

## ⚠️ Important

**USE ONLY ON SYSTEMS YOU OWN OR HAVE WRITTEN AUTHORIZATION TO TEST.**

Unauthorized traffic flooding can cause:

* Service disruption
* Network degradation
* Resource exhaustion
* Security incidents
* Legal consequences

The author is not responsible for misuse of this project.

---

## ✨ Features

* UDP stress-testing mode
* TCP connection stress-testing mode
* HTTP application-layer testing mode
* Configurable worker threads
* Configurable test duration
* Optional traffic-rate ceiling
* Live terminal statistics
* Interactive mode
* Command-line mode
* Hostname/IP resolution
* Optional TLS support for HTTP testing
* Optional destination-port rotation for UDP mode
* Ctrl+C graceful shutdown

---

## 🧰 Requirements

* Python **3.x**
* Linux, macOS, or Windows
* Network access to an **authorized test environment**

No third-party Python packages are required by the current script.

---

# 🚀 Installation

## Clone the repository

```bash
git clone https://github.com/ABHISHEK14677/DDOS-V2.git
```

## Enter the project directory

```bash
cd DDOS-V2
```

## Check Python

```bash
python3 --version
```

## Run

```bash
python3 DDOS-V2.py
```

---

# 🖥️ Interactive Mode

Start the program without command-line arguments:

```bash
python3 DDOS-V2.py
```

The interactive interface asks for parameters such as:

```text
vector
target
port
threads
duration
rate ceiling
payload size
```

HTTP mode additionally supports:

```text
Host header / SNI
TLS
```

---

# 🔧 Available Modes

## UDP

UDP-based network stress testing.

```text
udp
```

Supports configurable:

* Payload size
* Worker threads
* Duration
* Rate ceiling
* Destination-port rotation

---

## TCP

TCP connection stress testing.

```text
tcp
```

Supports configurable:

* Worker threads
* Duration
* Rate ceiling

---

## HTTP

HTTP application-layer stress testing.

```text
http
```

Supports:

* HTTP GET requests
* Randomized request paths
* User-Agent variation
* Host header
* SNI
* Optional TLS
* Worker threads
* Duration
* Rate ceiling

---

# ⚙️ Command-Line Options

The script exposes the following options:

| Option           | Purpose                               |
| ---------------- | ------------------------------------- |
| `vector`         | Testing mode: `udp`, `tcp`, or `http` |
| `target`         | Authorized test host/IP               |
| `-p, --port`     | Destination port                      |
| `-t, --threads`  | Number of worker threads              |
| `-d, --duration` | Test duration                         |
| `-r, --rate`     | Traffic-rate ceiling                  |
| `-s, --size`     | UDP payload size                      |
| `--rotate`       | Rotate UDP destination ports          |
| `--host`         | HTTP Host header / SNI                |
| `--tls`          | Enable TLS for HTTP mode              |

---

# 📊 Live Statistics

During a test, the program displays live statistics similar to:

```text
[   1.0s]       ... sent |    ... err | total ...
[   2.0s]       ... sent |    ... err | total ...
[   3.0s]       ... sent |    ... err | total ...
```

At completion, the program reports:

```text
done — ... sent, ... errors in ...s
```

The average packets/operations per second is also displayed.

---

# 🛑 Stopping a Test

Press:

```text
Ctrl+C
```

The program catches `SIGINT`, sets its stop event, and asks worker threads to terminate cleanly.

---

# 🧠 Architecture

The project can be viewed as five main components:

```text
                ┌──────────────────┐
                │   CLI / Menu     │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Target Resolver  │
                └────────┬─────────┘
                         │
              ┌──────────┼──────────┐
              │          │          │
              ▼          ▼          ▼
            UDP         TCP        HTTP
              │          │          │
              └──────────┼──────────┘
                         ▼
                ┌──────────────────┐
                │ Worker Threads   │
                └────────┬─────────┘
                         │
                         ▼
                ┌──────────────────┐
                │ Live Monitoring   │
                └──────────────────┘
```

---

# 🔬 Learning Objectives

This project can be useful for learning about:

* Python socket programming
* UDP and TCP behavior
* HTTP request handling
* TLS connections
* Threading
* Rate limiting
* DNS resolution
* Signal handling
* Graceful process termination
* Network monitoring
* Defensive DDoS analysis

---

# 🧪 Recommended Lab Environment

For safe experimentation, use an isolated environment such as:

```text
┌───────────────┐
│ Test Machine  │
│   Generator   │
└───────┬───────┘
        │
   Isolated LAN
        │
        ▼
┌───────────────┐
│ Test Server   │
│    / VM       │
└───────────────┘
```

Monitor the test server using tools such as:

```bash
top
```

```bash
ss -s
```

```bash
ip -s link
```

```bash
iftop
```

Only monitor and test infrastructure you are authorized to use.

---

# 🛡️ Defensive Research

The project can also be used to understand how defenders detect abnormal traffic patterns.

Useful defensive indicators include:

* Sudden traffic spikes
* Large numbers of connections
* High packets-per-second rates
* Unusual source distributions
* Increased server CPU usage
* Increased network utilization
* HTTP request-rate anomalies
* Connection failures
* Service latency increases

---

# 📁 Project Structure

```text
DDOS-V2/
│
├── DDOS-V2.py
└── README.md
```

---

# 🐍 Python Concepts Used

The project demonstrates several Python standard-library concepts:

```text
argparse
socket
threading
signal
time
random
os
ssl
sys
string
```

---

# ⚠️ Responsible Use

This software is intended strictly for:

* Authorized penetration-testing laboratories
* Local security research
* Network-performance experiments
* Educational environments
* Systems owned by the tester
* Systems where explicit written authorization exists

**Do not use it against public websites, servers, networks, or services without permission.**

---

# 👨‍💻 Author

**ABHISHEK M**

GitHub:

```text
https://github.com/ABHISHEK14677
```

Repository:

```text
https://github.com/ABHISHEK14677/DDOS-V2
```

---

# ⭐ Support

If this project helps with your cybersecurity learning:

* ⭐ Star the repository
* 🍴 Fork the project
* 🐛 Report bugs
* 💡 Suggest improvements
* 🔧 Contribute responsibly

---

## 📜 License

Add an appropriate open-source license to the repository before distributing the project publicly.

---

<div align="center">

# ⚡ DDOS-V2

### Network Stress Testing • Python • Cybersecurity Lab

**Learn • Test • Monitor • Secure**

</div>
