import base64
import io
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

# Read image features
root = '/content/CS336.M11.KHCL/'
path_data = '/content/CS336.M11.KHCL/data/'
path_corpus = '/content/CS336.M11.KHCL/data/test/oxford5k/jpg/'

corpus = load_corpus(path_corpus)
method0, method1, method2 = load_features(path_data, corpus)
model, net, transform, ms, delf = load_methods(root)


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
@cross_origin(origin='*')
def index():
    if request.method == 'POST':
        # Upload image
        # file = request.files['query_img']
        query_file = request.form
        base64Img = query_file['image']
        bbx = (query_file['x'], query_file['y'], query_file['x_max'], query_file['y_max'])
        
        # Save query image
        img = decode_img(base64Img)
        query_path = "data/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + "query_img.png"
        img.save(query_path)

        # Run search
        results = method_0(query_path, bbx, method0, model)
    
        response = {'results': results}
        
        return json.dumps(response)
        
    else:
        return render_template('index.html')


if __name__=="__main__":
    CORS(app)
    run_with_ngrok(app)
    print('ngrok')
    app.run()
