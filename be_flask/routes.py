from flask import Flask, request, Response, make_response, jsonify, redirect, url_for, session
from flask_cors import CORS, logging
from werkzeug.utils import secure_filename
from esrgan.esrgan import esrgan_load_generate
import json
import os
import base64
import io
from PIL import Image

logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
CORS(app)

app.config.from_envvar('APP_SETTINGS')
app.secret_key = app.config['DEFAULT_APP_KEY']


@app.route('/', methods=['GET'])
def basic_get():
    return "success", 200


@app.route('/api/upload', methods=['POST', 'OPTIONS'])
def fileUpload():
    try:
        UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
        target=os.path.join(UPLOAD_FOLDER,'static')
        if not os.path.isdir(target):
            os.mkdir(target)
        file = request.files['file']
        filename = secure_filename(file.filename)
        destination="/".join([target, filename])
        file.save(destination)
        session['uploadFilePath']=destination
        base,_ = os.path.splitext(destination)
        upscaled_path= base + '_upscaled'+ '.png'
        upscaled_path = destination.replace(".jpg","") + '_upscaled'+ '.png'
        print('calling scale generation')
        orig,output = esrgan_load_generate(destination, filename, upscaled_path, int(request.form['upscale_level']))
        os.remove("%s"%destination)
        with open(upscaled_path,"rb") as upscaled_img:
            strr = base64.b64encode(upscaled_img.read()).decode("utf-8")
            os.remove("%s"%upscaled_path)
            return "data:image/png;base64,"+strr
    except Exception as e:
        print("error: ",e)
        return "Unable to upload", 404

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
#    debug = app.config['DEBUG'], threaded = app.config['THREADED'], port = app.conifg['PORT'], use_reloader = True
   app.run(debug=True)