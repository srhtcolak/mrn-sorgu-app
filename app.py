
from flask import Flask, request, render_template, jsonify, redirect, url_for
import os
import json
import openpyxl

app = Flask(__name__)
DATA_FILE = "static/data/mrn_data.json"
USERS = {"21579": "14419907690", "admin2": "admin2pass", "admin3": "admin3pass"}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/query", methods=["POST"])
def query():
    mrn = request.form.get("mrn", "").strip().upper()
    if not os.path.exists(DATA_FILE):
        return jsonify({"error": "Veri dosyası bulunamadı."})
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    result = next((item for item in data if item["MRN"] == mrn), None)
    return jsonify(result) if result else jsonify({"error": "MRN bulunamadı."})

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    return jsonify({"success": USERS.get(username) == password})

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files['file']
    if file and file.filename.endswith(".xlsx"):
        wb = openpyxl.load_workbook(file)
        sheet = wb.active
        data = []
        for i, row in enumerate(sheet.iter_rows(values_only=True)):
            if i == 0:
                continue
            data.append({
                "MRN": str(row[0]).strip(),
                "Statü": row[1],
                "Varış Gümrük İdaresi": row[2],
                "Rejim Hak Sahibi": row[4]
            })
        os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return redirect(url_for("index"))
    return "Hatalı dosya", 400

if __name__ == "__main__":
    app.run(debug=True)
