# Blackbit Web Encryptor

A web-based file encryption and decryption system with a cyberpunk UI. Backed by Flask and Cryptography (Fernet), fully local and stateless — no database needed.


## ✨ Features
- Encrypt any uploaded file using Fernet (AES-128 in CBC mode with HMAC; URL-safe token).
- Auto-generate a `.key` file for decryption later.
- Decrypt by uploading the `.encrypted` file and its `.key`.
- Temporary storage in `./temp/` with automatic cleanup.
- Cyberpunk / hacker UI with:
  - Neon glowing theme
  - Matrix rain overlay
  - Three.js 3D background (neon grid + wireframe cube)
  - Typewriter status messages & live console logs
- No external database, works entirely on your machine.


## 🏗 Tech Stack
- Backend: Python 3.10+, Flask, cryptography (Fernet), Flask-CORS, pathlib
- Frontend: HTML, CSS, Vanilla JS, Three.js, Typed.js


## 📦 Project Structure
```
.
├─ app.py
├─ requirements.txt
├─ templates/
│  └─ index.html
└─ static/
   ├─ css/
   │  └─ styles.css
   ├─ js/
   │  └─ main.js
   └─ img/
      └─ favicon.svg
```

A `temp/` folder is created automatically at runtime to store transient files.


## 🚀 Getting Started

1) Install dependencies
- It’s recommended to use a virtual environment.

Windows (PowerShell):
```
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2) Run the server
```
python app.py
```

3) Open in browser
```
http://127.0.0.1:5000
```


## 🔐 How It Works
- Encryption uses `cryptography.fernet.Fernet`. A new random key is generated per encryption request.
- The uploaded file is encrypted in-memory, then saved as a temporary `.encrypted` file and a separate `.key` file.
- Decryption takes the `.encrypted` file and `.key`, decrypts to the original contents, and returns the restored file.
- Files in `./temp/` are named with a random ID and periodically cleaned (older than 15 minutes) on each operation.


— ⚡ Blackbit v2.0
