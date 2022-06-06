import argparse
import os
from PIL import Image
from werkzeug.utils import secure_filename
import torch
from flask import send_file,Flask,session, render_template,flash, request, redirect, url_for
import datetime
import json
import zipfile

HOST='0.0.0.0'
app = Flask(__name__)

uploads_dir = os.path.join(os.getcwd(), 'projects')

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def create_project(project_name,url):
    dir=os.path.join(os.getcwd(), 'projects')+'/'+project_name
    os.mkdir(dir)
    os.mkdir(dir+'/'+'data')
    info={
        "name":project_name,
        "create_at": str(datetime.datetime.now())
    }
    with open(dir+"/info.json", "w") as outfile:
        json.dump(info, outfile)
    open(dir+'/'+project_name+'.yaml','wb').write(open("./sample.yaml", "rb").read())
    open(dir+'/data/'+project_name+'.yaml','a').write("\ndownload: "+url+url_for('downloadFile',project=project_name,file=project_name+'.zip'))
def get_dirr():
    return os.path.join(os.getcwd(), 'projects')
def get_project():
    return os.listdir(os.path.join(os.getcwd(), 'projects'))
@app.route("/", methods=["GET", "POST"])
@app.route("/home", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        url=request.base_url.replace('/home','')
        new_pj=request.form.get("pj_name")
        create_project(new_pj,url)
            
    return render_template("homepage.html",projects=get_project())
@app.route("/project", methods=["GET", "POST"])
def project():
    session["project"]=request.args.get('project')
    data=open(get_dirr()+'/'+session["project"]+'/data/'+session["project"]+'.yaml','r',encoding='utf-8').read()
    return render_template("project.html",data=data)
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
        files = request.files.getlist("file")
        for f in files:
            x=os.path.join(uploads_dir,session["project"],'data', secure_filename(f.filename))
            print(x)
            f.save(os.path.join(uploads_dir,session["project"],'data', secure_filename(f.filename)))
        return (redirect(url_for('home',projects=get_project())))
@app.route('/download', methods=['GET'])
def downloadFile ():
    project=request.args.get("project")
    file=request.args.get("file")
    # return uploads_dir+'/'+project+'/'+file
    return send_file(uploads_dir+'/'+project+'/data/'+file,attachment_filename =file,as_attachment=True)

@app.route('/trainconfig', methods=["GET", "POST"])
def pj_config():
    if request.method == 'POST':
        pass 
    return render_template('project_config.html')
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Flask app exposing yolov5 models")
    parser.add_argument("--port", default=5000, type=int, help="port number")
    args = parser.parse_args()
    app.secret_key = 'secret key'
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(host=HOST,port=5055,debug=True)
