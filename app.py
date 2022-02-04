import base64
import io
import os
import json
import numpy as np
from PIL import Image
from datetime import datetime
from flask import Flask, request
from pathlib import Path
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok
from retrieval_model import load_features, load_corpus, method_0, method_1, method_2, load_methods
from argparse import ArgumentParser 

app = Flask(__name__)
cors = CORS(app, resources={r"/": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

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
    query_file = request.form
    base64Img = query_file['image']
    x1, y1 = int(float(query_file['x'])), int(float(query_file['y']))
    x2, y2 = int(float(query_file['x_max'])), int(float(query_file['y_max']))
    methodRequest = query_file['method']
    
    # Save query image
    img = decode_img(base64Img)
    if not os.path.exists("data/uploaded/"): os.makedirs("data/uploaded/")
    query_path = "data/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + "query_img.png"
    img.save(query_path)

    # Run search
    if x1 == 0 and y1 == 0 and x2 == 0 and y2 == 0: x2, y2 = img.size

    if methodRequest == '0':
        results = method_0(query_path, [x1, y1, x2, y2], fe_method0, model)
    elif methodRequest == '1':
        results = method_1(query_path, [x1, y1, x2, y2], fe_method1)
    elif methodRequest == '2':
        results = method_2(query_path, [x1, y1, x2, y2], fe_method2, delf, 20)
    results = [encode_img(str(args.path_corpus + i)) for i in results]
    response = {'results': results}
    
    return json.dumps(response)
  elif request.method == 'GET': return "200"

if __name__=="__main__":
    parser = ArgumentParser(description='Server')
    parser.add_argument('-ng','--ngrok',default=0,  
                        metavar='NGROK', help='Expose local web server to the internet with ngrok')
    parser.add_argument('-r','--root',default='/content/CS336.M11.KHCL/',  
                        metavar='ROOT', help='Path to your root folder of project')
    parser.add_argument('-pd','--path_data',default='/content/CS336.M11.KHCL/data/', 
                        metavar='PATHDATA', help='Path to your dataset')
    parser.add_argument('-pc','--path_corpus',default='/content/CS336.M11.KHCL/data/test/oxford5k/jpg/', 
                        metavar='PATHCORPUS', help='Path to your images database, use for return image')

    args = parser.parse_args()  

    corpus = load_corpus(args.path_corpus)
    fe_method0, fe_method1, fe_method2 = load_features(args.path_data, corpus)
    model, delf = load_methods(args.root)

    if str(args.ngrok) == '1':
        run_with_ngrok(app)
        print('ngrok')
    app.run()
