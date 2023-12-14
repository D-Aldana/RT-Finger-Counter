import cv2
import numpy as np

def initializeVideoCapture():
    """
    Initialize the video capture object.

    Args:
        None

    Returns:
        cap: VideoCapture object
    """

    cap = cv2.VideoCapture(0)
    return cap

def getFrame(cap):
    """
    Get a frame from the video capture object.

    Args:
        cap: VideoCapture object

    Returns:
        frame: Frame from the video capture object
    """

    _, frame = cap.read()
    return frame

def countdown(frame, seconds):
    """
    Display a countdown on the frame.

    Args:
        frame: Frame to display the countdown on
        seconds: Number of seconds to countdown from

    Returns:
        frame: Frame with the countdown displayed on it
    """

    x, y, _ = frame.shape
    for i in range(seconds, 0, -1):
        cv2.rectangle(frame, (0, 0), (y, x), (0, 0, 0), -1)
        centerText(str(i), frame)
        cv2.imshow("Rock Paper Scissors", frame)
        cv2.waitKey(1000)

def centerText(msg, frame, colour=(255, 255, 255)):
    """
    Display text in the center of the frame.

    Args:
        msg: Message to display
        frame: Frame to display the message on
        colour: Colour of the text

    Returns:
        frame: Frame with the text displayed on it
    """
    
    text = msg
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 1
    font_thickness = 2
    text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2
    text_y = (frame.shape[0] + text_size[1]) // 2
    cv2.putText(frame, text, (text_x, text_y), font, font_scale, colour, font_thickness)
    return frame