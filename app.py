import base64
import io
import json
import numpy as np
from PIL import Image
from feature_extractor import FeatureExtractor
from datetime import datetime
from flask import Flask, request, render_template
from pathlib import Path
from flask_cors import CORS, cross_origin
from flask_ngrok import run_with_ngrok

app = Flask(__name__)

# Read image features
fe = FeatureExtractor()
features = []
img_paths = []
for feature_path in Path("./static/feature").glob("*.npy"):
    features.append(np.load(feature_path))
    img_paths.append(Path("./static/img") / (feature_path.stem + ".jpg"))
features = np.array(features)


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
        file = request.form.get('image')
        
        # Save query image
        img = decode_img(file)
        uploaded_img_path = "static/uploaded/" + datetime.now().isoformat().replace(":", ".") + "_" + "query_img.png"
        img.save(uploaded_img_path)

        # Run search
        query = fe.extract(img)
        dists = np.linalg.norm(features-query, axis=1)  # L2 distances to features
        ids = np.argsort(dists)[:30]  # Top 30 results
        scores = [ encode_img(str(img_paths[id])) for id in ids]
    
        response = {'query-path': str(uploaded_img_path), 'scores': scores}
        
        return json.dumps(response)
        
    else:
        return render_template('index.html')


if __name__=="__main__":
    app.run("0.0.0.0")
