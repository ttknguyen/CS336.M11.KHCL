import base64
import io
import os
import json
import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok
from retrieval_model import load_features, load_corpus, method_0, method_1, method_2, load_methods

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Read image features
root = '/content/CS336.M11.KHCL/'
path_data = '/content/CS336.M11.KHCL/data/'
path_corpus = '/content/CS336.M11.KHCL/data/test/oxford5k/jpg/'

corpus = load_corpus(path_corpus)
method0, method1, method2 = load_features(path_data, corpus)
model, delf = load_methods(root)


def decode_img(msg):
    msg = msg[msg.find(',') + 1:]
    msg = base64.b64decode(msg)
    buf = io.BytesIO(msg)
    img = Image.open(buf)
    return img

def encode_img(pathImg):
    with open(pathImg, "rb") as image_file:
        base64str = str(base64.b64encode(image_file.read()))
    base64str = base64str[2:-1]
    return base64str

@app.route('/', methods=['GET', 'POST'])
@cross_origin(origin='*',headers=['Content-Type','Authorization'])
def index():
    if request.method == 'POST':
        # Upload image
        query_file = request.form
        # print(query_file)

        base64Img = query_file['image']
        x, y = int(float(query_file['x'])), int(float(query_file['y']))
        x_max, y_max = int(float(query_file['x_max'])), int(float(query_file['y_max']))
        
        # Save query image
        img = decode_img(base64Img)
        if not os.path.exists("data/uploaded/"): os.makedirs("data/uploaded/")
        query_path = "data/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + "query_img.png"
        img.save(query_path)

        # Run search
        if x == 0 and y == 0 and x_max == 0 and y_max == 0: x_max, y_max = img.size
        bbx = (x, y, x_max, y_max)

        results = method_0(query_path, bbx, method0, model)
        results = [encode_img(str(path_corpus + i)) for i in results]
        response = {'results': results}
        
        return json.dumps(response)
    else: return render_template('Ups somthing went wrong!!!')


if __name__=="__main__":
    # CORS(app)
    # run_with_ngrok(app)
    # print('ngrok')
    app.run()
