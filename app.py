from flask import Flask, render_template, request, redirect
from flask_basicauth import BasicAuth
import os
import firebase_admin
from firebase_admin import credentials, storage

app = Flask(__name__)

# Basic Authentication
app.config['BASIC_AUTH_USERNAME'] = 'kirvptc'
app.config['BASIC_AUTH_PASSWORD'] = 'kirvptc'
basic_auth = BasicAuth(app)

# Detect credentials.json in the same directory
cred_path = os.path.join(os.path.dirname(__file__), "ptc-iot-digital-signage-test-firebase-adminsdk-2zuhv-079eb5493d.json")
cred = credentials.Certificate(cred_path)
firebase_admin.initialize_app(cred, {"storageBucket": "ptc-iot-digital-signage-test.appspot.com"})

@app.route("/")
@basic_auth.required
def index():
    # Fetch file list from Firebase Storage
    bucket = storage.bucket()
    blobs = list(bucket.list_blobs())
    files = [blob.name for blob in blobs]

    return render_template("index.html", files=files)

@app.route("/upload", methods=["POST"])
@basic_auth.required
def upload():
    file = request.files["file"]
    if file:
        # Upload file to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(file.filename)
        blob.upload_from_string(file.read(), content_type=file.content_type)

    return redirect("/")

@app.route("/delete", methods=["POST"])
@basic_auth.required
def delete():
    files_to_delete = request.form.getlist("filesToDelete")
    if files_to_delete:
        # Delete selected files from Firebase Storage
        bucket = storage.bucket()
        for file_name in files_to_delete:
            blob = bucket.blob(file_name)
            blob.delete()

    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

