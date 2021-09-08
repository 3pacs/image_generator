"""Simple flask app that generates images and displays on the browser"""
from imager import makeImage
from flask import Flask, render_template
import os

# Flask App configurations
app = Flask(__name__)
image_folder = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = image_folder


@app.route('/')
@app.route('/home')
def home():
    """Home Page view that has the image and a button that generates a new image"""
    output = makeImage(20)
    image = os.path.join(app.config['UPLOAD_FOLDER'], output)
    return render_template("index.html", img_produce=image)


if __name__ == '__main__':  # defining main
    app.run()
