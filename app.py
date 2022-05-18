import cv2
import serial
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



cap = cv2.VideoCapture(0)
print("connected camera")
app = Flask(__name__)
def gen_frames():  
    while True:
        # data = arduino.readline()
        #prinnt("# read the port data")
        success,frame = cap.read()  # read the camera frame
        frame=cv2.resize(frame, (800, 600))
        font = cv2.FONT_HERSHEY_COMPLEX
        cv2.putText(frame, read, (10, 50), font, 1, color=(0, 255, 255), thickness=2)
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == "__main__":
    app.run(debug=True)
