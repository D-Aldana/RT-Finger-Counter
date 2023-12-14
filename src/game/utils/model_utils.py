import mediapipe as mp
import tensorflow as tf
from tensorflow.keras.models import load_model

def initializeMediaPipe():
    """
    Initialize the MediaPipe hands object.

    Returns:
        hands: MediaPipe hands object
        mpDraw: MediaPipe drawing utils object
    """

    mpHands = mp.solutions.hands
    hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
    mpDraw = mp.solutions.drawing_utils
    return hands, mpDraw


def loadModel():
    """
    Load the gesture recognizer model.

    Returns:
        model: Gesture recognizer model
    """

    model = load_model('mp_hand_gesture')
    return model

def getClassNames():
    """
    Load the class names.

    Returns:
        classNames: List of class names
    """

    f = open('gesture.names', 'r')
    classNames = f.read().split('\n')
    f.close()
    return classNames