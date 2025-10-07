from __future__ import annotations

import io
import os
import re
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Tuple

from cryptography.fernet import Fernet, InvalidToken
from flask import (
    Flask,
    jsonify,
    render_template,
    request,
    send_from_directory,
    abort,
)
from flask_cors import CORS
from werkzeug.utils import secure_filename

# -------------------------------------------------------------
# Blackbit Web Encryptor - Flask Backend
# -------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent
TEMP_DIR = BASE_DIR / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

MAX_AGE_SECONDS = 15 * 60  # 15 minutes

app = Flask(__name__)
CORS(app)


# ------------------------ Utilities -------------------------

def _cleanup_temp(max_age_seconds: int = MAX_AGE_SECONDS) -> None:
    """Remove files in temp older than max_age_seconds."""
    now = datetime.utcnow()
    for p in TEMP_DIR.glob("*"):
        try:
            if not p.is_file():
                continue
            mtime = datetime.utcfromtimestamp(p.stat().st_mtime)
            if now - mtime > timedelta(seconds=max_age_seconds):
                p.unlink(missing_ok=True)
        except Exception:
            # best-effort cleanup
            pass


def _unique_name(suffix: str) -> str:
    return f"bb-{uuid.uuid4().hex}{suffix}"


def _sanitize_download_name(name: str) -> str:
    # allow alphanum, space, dot, dash, underscore; strip others
    return re.sub(r"[^\w\-. ]+", "_", name)[:200] or "download.bin"


# ------------------------ Routes ----------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/encrypt", methods=["POST"])
def encrypt_route():
    _cleanup_temp()

    if "file" not in request.files:
        return jsonify({"ok": False, "error": "No file part in request"}), 400

    up = request.files["file"]
    if up.filename == "":
        return jsonify({"ok": False, "error": "No file selected"}), 400

    original_name = secure_filename(up.filename) or "file.bin"

    try:
        t0 = time.perf_counter()
        raw = up.read()
        key = Fernet.generate_key()
        f = Fernet(key)
        enc = f.encrypt(raw)
        elapsed = time.perf_counter() - t0

        # Store files with unique names
        enc_store = _unique_name(".encrypted")
        key_store = _unique_name(".key")

        (TEMP_DIR / enc_store).write_bytes(enc)
        (TEMP_DIR / key_store).write_bytes(key)

        # Friendly download names
        friendly_enc = f"{Path(original_name).name}.encrypted"
        friendly_key = f"blackbit_{Path(original_name).stem}.key"

        return jsonify({
            "ok": True,
            "encrypted": {
                "store_name": enc_store,
                "url": f"/download/{enc_store}?name={_sanitize_download_name(friendly_enc)}",
                "display_name": friendly_enc,
                "size_bytes": len(enc),
            },
            "key": {
                "store_name": key_store,
                "url": f"/download/{key_store}?name={_sanitize_download_name(friendly_key)}",
                "display_name": friendly_key,
                "size_bytes": len(key),
            },
            "stats": {
                "original_name": original_name,
                "original_size": len(raw),
                "encrypted_size": len(enc),
                "elapsed_seconds": round(elapsed, 4),
            },
            "log": [
                "[OK] Key generated",
                "[OK] File encrypted successfully",
            ],
        })
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/decrypt", methods=["POST"])
def decrypt_route():
    _cleanup_temp()

    if "encrypted" not in request.files or "key" not in request.files:
        return jsonify({"ok": False, "error": "Missing file(s). Provide 'encrypted' and 'key'."}), 400

    up_enc = request.files["encrypted"]
    up_key = request.files["key"]

    if up_enc.filename == "":
        return jsonify({"ok": False, "error": "No encrypted file selected"}), 400
    if up_key.filename == "":
        return jsonify({"ok": False, "error": "No key file selected"}), 400

    enc_name_in = secure_filename(up_enc.filename)
    try:
        key_bytes = up_key.read()
        f = Fernet(key_bytes)
        t0 = time.perf_counter()
        dec = f.decrypt(up_enc.read())
        elapsed = time.perf_counter() - t0

        # Guess original friendly name
        base = Path(enc_name_in).name
        if base.lower().endswith(".encrypted"):
            friendly_dec = base[:-10]  # remove ".encrypted"
            if not friendly_dec:
                friendly_dec = "restored.bin"
        else:
            friendly_dec = f"{Path(base).stem}.restored{Path(base).suffix}"

        # Store with unique real name, but serve with friendly name
        ext = Path(friendly_dec).suffix
        store_name = _unique_name(ext if ext else ".bin")
        (TEMP_DIR / store_name).write_bytes(dec)

        return jsonify({
            "ok": True,
            "decrypted": {
                "store_name": store_name,
                "url": f"/download/{store_name}?name={_sanitize_download_name(friendly_dec)}",
                "display_name": friendly_dec,
                "size_bytes": len(dec),
            },
            "stats": {
                "elapsed_seconds": round(elapsed, 4),
            },
            "log": [
                "[OK] Key accepted",
                "[OK] File decrypted successfully",
            ],
        })

    except InvalidToken:
        return jsonify({"ok": False, "error": "Invalid key or corrupted encrypted file."}), 400
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 500


@app.route("/download/<path:filename>")
def download(filename: str):
    # Enforce filename pattern: bb-<uuid>.something
    if not re.fullmatch(r"bb-[0-9a-f]{32}\.[\w\-.]+", filename or ""):
        abort(404)

    fp = TEMP_DIR / filename
    if not fp.exists() or not fp.is_file():
        abort(404)

    download_name = request.args.get("name") or filename
    download_name = _sanitize_download_name(download_name)

    # Let Flask handle range requests and headers
    return send_from_directory(
        directory=str(TEMP_DIR),
        path=filename,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/octet-stream",
        max_age=0,
    )


# -------------------- Entrypoint -----------------------------

if __name__ == "__main__":
    # On Windows and most dev setups, binding to 127.0.0.1 is fine
    app.run(host="127.0.0.1", port=5000, debug=False)
