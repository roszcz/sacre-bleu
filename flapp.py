from flask import send_file
from flask import Flask, jsonify, render_template, request
from utils.realcam import PhotoTaker

taker = PhotoTaker()
app = Flask(__name__)

@app.route('/get_image', methods = ['GET'])
def get_image():
    taker.take_picture()
    filename = 'tmp.png'
    return send_file(filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
