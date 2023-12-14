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


def preprocessFrame(frame):
    """
    Flip a frame vertically and convert to RGB

    Args:
        frame: Frame to process

    Returns:
        frame: Flipped and RGB frame
    """
    frame = cv2.flip(frame, 1)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
    return frame
    
def processGesture(frame, hands, model, classNames):
    """
    Process the gesture in the frame.

    Args:
        frame: Frame to process
        hands: Hands object
        model: Model to predict the gesture
        classNames: List of class names

    Returns:
        className: Predicted gesture
        msg: Message to display
    """

    frame = preprocessFrame(frame)
    x, y, _ = frame.shape
    
    
    result = hands.process(frame)
    msg = "No hand detected. Try again!"
    className = None

    if result.multi_hand_landmarks:
        landmarks = []
        for hand_landmarks in result.multi_hand_landmarks:
            for lm in hand_landmarks.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

        prediction = model.predict([landmarks])
        classID = np.argmax(prediction)
        className = classNames[classID]

        if className not in ["rock", "paper", "scissors"]:
            msg = "Invalid gesture. Try again!"
        else:
            msg = processGameResult(className)

    return className, msg


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


def destroyVideoCapture(cap):
    """
    Release the video capture object.

    Args:
        cap: VideoCapture object

    Returns:
        None
    """
    
    cap.release()
    cv2.destroyAllWindows()