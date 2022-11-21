import base64

import cv2
import torch
import numpy as np
from helper import base64EncodeImage,  detect_demo
from flask import Flask, request, render_template


app = Flask(__name__, template_folder='templates')

# for demo purposes
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# for pipe detection
# model = torch.hub.load('ultralytics/yolov5', 'custom', path='models/best.pt')
# model.conf = .5
# model.iou = .2


@app.route("/home")
def home():
    print("hello")
    return render_template('index.html')


@app.route("/home", methods=['POST'])
def get_base64img():

    image64 = request.get_json()['image64']
    image = base64.b64decode(image64)

    # converting the binary data to numpy array
    images_arr = np.frombuffer(image, dtype=np.uint8)
    # reading the image from numpy array
    img = cv2.imdecode(images_arr, flags=cv2.IMREAD_COLOR)

    # for demo
    img = detect_demo(img, model)

    # for pipe detection
    # img, n = detect(img, model)
    # print(f"n pipes: {n}")

    # encode the image into base64 to be sent back to the client
    b64image = base64EncodeImage(img)

    payload = {'image': b64image}

    # preprocessing to match json data format
    encoded_payload = str(payload).replace("'", r'"')

    # cv2.imshow("test", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return encoded_payload


if __name__ == "__main__":
    app.run(debug=True)
