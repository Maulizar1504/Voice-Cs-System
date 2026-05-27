import uuid
import json
from datetime import datetime

def generate_filename(ext):
    return f"{uuid.uuid4().hex}.{ext}"

def timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_log(data, filepath):

    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(data, ensure_ascii=False) + "\n")