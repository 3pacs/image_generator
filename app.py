"""Simple flask app that generates images and displays on the browser"""
from PIL.Image import ImageTransformHandler
from flask.helpers import url_for
from imager import X, makeImage
from flask import Flask, render_template,redirect
import os
import sqlite3
from flask import g

# Flask App configurations
app = Flask(__name__ )
image_folder = os.path.join('static', 'output')
app.config['UPLOAD_FOLDER'] = image_folder
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

DATABASE = 'db.sqlite'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/')
def home():
    """Home Page view that has the image and a button that generates a new image"""
    img = "img0.png"
    db = get_db()
    image = os.path.join(app.config['UPLOAD_FOLDER'], img)
    bg = os.path.join(app.config['UPLOAD_FOLDER'], "new/bg/"+img)
    return render_template("index.html", img_produce=image,img_produce2=bg)

@app.route('/generate')
def generate():
    img = makeImage(1)
    return redirect(url_for('home'))

@app.route('/gallary')
def gallary():
    images = []
    for save in query_db('select * from saved'):
        #print(save[1], 'has the path ', save[0])
        images.append({
            'id':save[1],
            'image':save[0]
        })
    return render_template("gallary.html",images=images)



from shutil import copyfile
import time
@app.route('/add_to_gallary/<id>')
def add_to_gallary(id):
    
    print(id)
    if str(id) == "1":

        name = int(time.time())
        x = "static/saved/"+str(name)+".png"
        copyfile("static/output/new/bg/img0.png", x)
        cur = get_db().cursor()
        cur.execute("""INSERT INTO saved(image) 
               VALUES (?);""", (x,))
        
    elif str(id) == "2":
 
        name = int(time.time())
        x = "static/saved/"+str(name)+".png"
        copyfile("static/output/img0.png", x)
        cur = get_db().cursor()
        cur.execute("""INSERT INTO saved(image) 
               VALUES (?);""", (x,))
    
    get_db().commit()
    return redirect(url_for("home"))

if __name__ == '__main__':  # defining main
    app.run()
