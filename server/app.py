from flask import Flask, send_file, render_template, jsonify, request
from flask_cors import CORS
from generate import generate_images
from PIL import Image
import os
import base64
import time
import io

'''
Generate => getByteStream => remove => 

flask framework
'''

app = Flask(__name__)
CORS(app)

@app.route("/gen")
def gen():
    seed = request.args.get('seed')
    trun = request.args.get('trun')

    generate_images('model/metfaces.pkl',[int(seed)],float(trun),'const','out',None,None)

    return { "msg": 'generated' }


@app.route("/get/<img>")
def get(img):
    file = f'out/seed{img}.png'

    im = Image.open(file)
    data = io.BytesIO()
    im.save(data, "JPEG")
    encoded_img_data = base64.b64encode(data.getvalue())

    return {
        "msg": encoded_img_data.decode('utf-8'),
    }

@app.route("/remove/<img>", methods=['GET'])
def remove(img):
    if os.path.exists(f'out/seed{img}.png'):
        os.remove(f'out/seed{img}.png')
        return {"msg": 'deleted'}
    else:
        return {"msg": 'does not exist'}


if __name__ == '__main__':
    app.run(debug=True)

'''
server/model/network-snapshot-003000.pkl

@app.route("/get/<img>")
def get(img):
    file = f'out/{img}.png'
    return send_file(file, mimetype='image/png')
'''