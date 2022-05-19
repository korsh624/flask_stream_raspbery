import cv2
import serial
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
from flask import Flask, render_template, Response, request, redirect, url_for
data='open'
read="___"

data='open'
arduino = serial.Serial('/dev/ttyACM0',9600)
def sendmessage():
    count=0
    while (count<1):
        arduino.write(data.encode())
        read=arduino.readline()
        print(read)
        time.sleep(1)
        count=count+1
    count=0

camera  = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)
# while True:
#     for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
#         image = frame.array
#         cv2.imshow("Frame", image)
#         key = cv2.waitKey(1) & 0xFF
#     rawCapture.truncate(0)
#     if key == ord("q"):
#         break

# cap = cv2.VideoCapture(0)
print("connected camera")

app = Flask(__name__)
def gen_frames():
    while True:
        # data = arduino.readline()
        #prinnt("# read the port data")
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF

        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(image, read, (10, 50), font, 1, color=(0, 255, 255), thickness=2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        rawCapture.truncate(0)
        if key == ord("q"):
            break
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=False)
