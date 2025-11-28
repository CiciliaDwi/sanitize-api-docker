from pathlib import Path
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load banned words from: app/replaced_chars.txt
BANNED_WORDS = []
BANNED_PATH = Path(__file__).resolve().parent / "replaced_chars.txt"

if BANNED_PATH.exists():
    content = BANNED_PATH.read_text(encoding="utf-8")
    lines = content.splitlines()
    for line in lines:
        BANNED_WORDS.append(line)

def replaced_chars(text, replaced_chars):
    lower_text = text.lower()

    for w in banned_words:
        if w == "":
            continue  # avoid infinite loop if there is an empty line

        target = w.lower()
        idx = lower_text.find(target)

        while idx != -1:
            original = text[idx: idx + len(w)]

            if len(original) <= 2:
                masked = "*" * len(original)
            else:
                masked = original[0] + ("*" * (len(original) - 2)) + original[-1]

            text = text[:idx] + masked + text[idx + len(w):]
            lower_text = text.lower()
            idx = lower_text.find(target, idx + len(masked))

    return text

@app.post("/replace")
def replace_endpoint():
    data = request.get_json(silent=True) or {}
    text = data.get("text", "")
    cleaned = sanitize(text, BANNED_WORDS)
    return jsonify({"cleaned": cleaned})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
