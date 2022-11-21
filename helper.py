import base64
import cv2
import numpy as np


def detect(img, model):

    result = model(img)
    detections = result.pandas().xyxy

    # get the first index of the array
    detectionsArray = np.array(detections)[0]

    for i in range(0, len(detectionsArray)):
        # cv2.rectangle only accepts integers
        start = (round(detectionsArray[i][2]), round(detectionsArray[i][3]))
        end = (round(detectionsArray[i][0]), round(detectionsArray[i][1]))
        cv2.rectangle(img, start, end, (200, 25, 30), 2)

    # return the img with bounding boxes and the number of detections
    return img, len(detectionsArray)


def detect_demo(img, model):
    result = model(img)
    detections = result.pandas().xyxy
    detectionsArray = np.array(detections)[0]

    for i in range(0, len(detectionsArray)):
        start = (round(detectionsArray[i][2]), round(detectionsArray[i][3]))
        end = (round(detectionsArray[i][0]), round(detectionsArray[i][1]))
        labels = detectionsArray[i][-1]
        cv2.rectangle(img, end, start, (200, 25, 30), 2)
        cv2.putText(img, labels, (start[0], start[1]-2),
                    cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    return img


def base64EncodeImage(img):
    ''' Takes an input image and returns a base64 encoded string representation of that image (jpg format)'''
    _, im_arr = cv2.imencode('.jpg', img)
    im_b64 = base64.b64encode(im_arr.tobytes()).decode('utf-8')

    return im_b64
