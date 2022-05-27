import argparse
import os
from PIL import Image
from werkzeug.utils import secure_filename
import torch
from flask import Flask,session, render_template,flash, request, redirect, url_for
import datetime
import json
import zipfile

app = Flask(__name__)

uploads_dir = os.path.join(os.getcwd(), 'projects')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def create_project(project_name):
    dir=os.path.join(os.getcwd(), 'projects')+'/'+project_name
    os.mkdir(dir)
    os.mkdir(dir+'/'+'data')
    info={
        "name":project_name,
        "create_at": str(datetime.datetime.now())
    }
    with open(dir+"/info.json", "w") as outfile:
        json.dump(info, outfile)
def get_dirr():
    return os.path.join(os.getcwd(), 'projects')
def get_project():
    return os.listdir(os.path.join(os.getcwd(), 'projects'))
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        
        new_pj=request.form.get("pj_name")
        create_project(new_pj)
            
    return render_template("homepage.html",projects=get_project())
@app.route("/project", methods=["GET", "POST"])
def project():
    session["project"]=request.args.get('project')
    return render_template("project.html",dirr=get_dirr())
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            x=os.path.join(uploads_dir,session["project"],'data', secure_filename(f.filename))
            print(x)
            f.save(os.path.join(uploads_dir,session["project"],'data', secure_filename(f.filename)))
            with zipfile.ZipFile(os.path.join(uploads_dir,session["project"],'data', secure_filename(f.filename)),"r") as zip_ref:
                zip_ref.extractall(os.path.join(uploads_dir,session["project"],'data'))
        return (redirect(url_for('home',projects=get_project())))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host="0.0.0.0",port=8080,debug=True)  # debug=True causes Restarting with stat
