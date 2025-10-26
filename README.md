# Edge Device Security Demo

A minimal example showing **mutual TLS (mTLS)** authentication between an edge “device” and a cloud “server”.  
Built in Python using Flask and Requests to demonstrate certificate-based trust and encrypted telemetry transfer - a foundational concept in secure cloud and IoT systems (e.g., Azure Edge Security, AWS IoT Core).

---

## 🧠 Overview

This demo creates:
- A local **Certificate Authority (CA)** that issues certificates to a server and a device.
- A **Flask server** that requires client certificates for access.
- A **Python client (device)** that verifies the server’s identity before sending data.

Result: both sides authenticate each other, and communication is fully encrypted.

---

## 🧩 Folder Structure

```
edge-device-security-demo/
├── certs/             # Root CA, server, and device certificates (generated locally)
├── server/
│   └── server.py      # Flask HTTPS server requiring client certificates
├── device/
│   └── device.py      # Device client sending telemetry with its certificate
├── san.cnf            # SAN config used when creating the server certificate
└── README.md
```

---

## ⚙️ Running the Demo

### 1️. Setup (Linux / WSL)
```bash
sudo apt install python3 python3-venv openssl -y
python3 -m venv .venv
source .venv/bin/activate
pip install flask requests cryptography
```

### 2️. Create certificates
```bash
cd certs
# root CA
openssl genrsa -out rootCA.key 2048
openssl req -x509 -new -nodes -key rootCA.key -sha256 -days 1024 -out rootCA.pem -subj "/CN=MyRootCA"

# server certificate (SAN for localhost + 127.0.0.1)
openssl genrsa -out server.key 2048
openssl req -new -key server.key -out server.csr -subj "/CN=localhost"
echo "subjectAltName=DNS:localhost,IP:127.0.0.1" > san.cnf
openssl x509 -req -in server.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out server.crt -days 365 -sha256 -extfile san.cnf

# device certificate
openssl genrsa -out device.key 2048
openssl req -new -key device.key -out device.csr -subj "/CN=EdgeDevice01"
openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 365 -sha256
```

### 3️. Run the server
```bash
python server/server.py
```

### 4️. Run the device
```bash
python device/device.py
```

### ✅ Expected Output

**Server**
```
* Running on https://127.0.0.1:5001
Received: {'temperature': 27.8, 'status': 'OK'}
```

**Device**
```
Status: 200
Body: {"status": "ok"}
```

---

## 🧱 Concepts Demonstrated

- Public Key Infrastructure (PKI)
- Certificate creation and trust chains
- Mutual TLS (server ↔ client authentication)
- Secure device-to-cloud communication
- Foundations of **Edge / IoT security**

---

## 🛡️ Security Notice

This repository is for **educational purposes only**.  
Do **not** reuse the sample keys or certificates in production.  
All private keys should be generated locally and excluded from Git (`.gitignore`):

```
certs/*.key
certs/*.pem
certs/*.srl
```

---

## 🧾 License

MIT License — feel free to fork or adapt for learning.
