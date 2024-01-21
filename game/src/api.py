from flask import Flask, render_template, Response, request
import numpy as np
import cv2
import base64

app = Flask(__name__)

# Set up the route for the game
@app.route('/video_feed', methods=['POST'])
def video_feed():

    # Get the image from the request
    file = request.files['image']

    image_np = np.frombuffer(file.read(), np.uint8)
    image = cv2.imdecode(image_np, cv2.IMREAD_COLOR)

    # Encode the processed image to base64 for embedding in HTML
    _, buffer = cv2.imencode('.png', image)
    encoded_image = base64.b64encode(buffer).decode('utf-8')
    
    # Embed the image in the HTML page
    return render_template('show.html', image=encoded_image)

    # # Embed the image in the HTML page
    # return Response(encoded_image, mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/show', methods=['GET'])
def get_video():
    return render_template('show.html')

if __name__ == '__main__':
    app.run(debug=True)