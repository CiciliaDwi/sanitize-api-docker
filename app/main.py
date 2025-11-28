from flask import Flask, request, jsonify
from pathlib import Path

app = Flask(__name__)

# --- Load replaced chars ---
REPLACED = {}
FILE = Path(__file__).resolve().parent / "replaced_chars.txt"

if FILE.exists():
    for line in FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if "=" in line:
            key, val = line.split("=")
            key = key.strip()
            val = val.strip()
            if key and val:
                REPLACED[key] = val


def replace_chars(text: str):
    result = ""
    for ch in text:
        lower = ch.lower()

        if lower in REPLACED:
            rep = REPLACED[lower]
            result += rep
        else:
            result += ch

    return result


@app.post("/replace")
def replace_endpoint():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    output = replace_chars(text)
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)