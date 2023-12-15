from utils.model_utils import ModelUtils
from utils.frame_utils import VideoUtils, DisplayUtils
from utils.game_utils import GameUtils

def main():

    # Initialize the game
    game = GameUtils()

    # Initialize the video utils
    video = VideoUtils()

    # Initialize the display utils
    display = DisplayUtils()

    # Initialize the model utils
    model = ModelUtils()

    # Initialize MediaPipe
    hands, mpDraw = model.initializeMediaPipe()

    # Load the gesture recognizer model
    gesture_model = model.loadModel()

    # Load class names
    classNames = model.getClassNames()

    # Initialize the webcam
    cap = video.initializeVideoCapture()

    # Play the game
    while True:
        # Get a frame from the webcam
        frame = video.readFrame(cap)

        # Display the score
        frame = display.displayScore(frame, game.getPlayerScore(), game.getComputerScore())

        # Show the game start screen
        display.showFrame(frame)

        if display.checkGameStart():
            # Display the countdown
            frame = display.countdown(frame, 3)

            # Read gesture
            frame = video.readFrame(cap)

            # Get the computer gesture
            computer_gesture = game.rockPaperScissors()

            # Process the gesture
            frame, player_gesture = model.processGesture(frame, hands, gesture_model, classNames)
        
            # Process the game result
            result = game.processGameResult(player_gesture, computer_gesture)

            # Display the result
            frame = display.displayResult(frame, result, player_gesture, computer_gesture)

            # Display the frame
            display.showFrame(frame)

            display.wait(5000)

        # Check for quit
        if video.checkQuit():
            break
    
    # Release the webcam
    video.destroyVideoCapture(cap)
    

if __name__ == "__main__":
    main()