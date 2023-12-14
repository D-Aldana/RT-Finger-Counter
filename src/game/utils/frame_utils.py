import cv2

class VideoUtils:

    def __init__(self):
        pass


    def initializeVideoCapture(self):
        """
        Initialize the video capture object.

        Args:
            None

        Returns:
            cap: VideoCapture object
        """

        cap = cv2.VideoCapture(0)
        return cap


    def readFrame(self, cap):
        """
        Get a frame from the video capture object.

        Args:
            cap: VideoCapture object

        Returns:
            frame: Frame from the video capture object
        """

        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        # frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return frame

    def checkQuit(self):
        """
        Check if the user wants to quit the game.

        Args:
            None

        Returns:
            True if the user wants to quit, False otherwise
        """

        return cv2.waitKey(1) & 0xFF == ord('q')


    def destroyVideoCapture(self, cap):
        """
        Release the video capture object.

        Args:
            cap: VideoCapture object

        Returns:
            None
        """
        
        cap.release()
        cv2.destroyAllWindows()


class DisplayUtils:

    def __init__(self):
        pass

    
    def showFrame(self, frame):
        """
        Display a frame.

        Args:
            frame: Frame to display

        Returns:
            None
        """

        cv2.imshow("Rock Paper Scissors", frame)


    def wait(self, ms):
        """
        Wait for a specified number of milliseconds.

        Args:
            ms: Number of milliseconds to wait

        Returns:
            None
        """

        cv2.waitKey(ms)


    def checkGameStart(self):
        """
        Check if the user wants to start the game.

        Args:
            None

        Returns:
            True if the user wants to start the game, False otherwise
        """

        return cv2.waitKey(1) == ord(' ')

    def countdown(self, frame, seconds):
        """
        Display a countdown on the frame.

        Args:
            frame: Frame to display the countdown on
            seconds: Number of seconds to countdown from

        Returns:
            frame: Frame with the countdown displayed on it
        """
        x, y = frame.shape[:2]
        startMsg = "Get Ready..."
        cv2.rectangle(frame, (0, 0), (y, x), (0, 0, 0), -1)
        frame = self.centerText(startMsg, frame)
        self.showFrame(frame)
        self.wait(2000)

        x, y, _ = frame.shape
        for i in range(seconds, 0, -1):
            cv2.rectangle(frame, (0, 0), (y, x), (0, 0, 0), -1)
            self.centerText(str(i), frame)
            self.showFrame(frame)
            self.wait(1000)
        return frame
        
    
    def centerText(self, msg, frame, colour=(255, 255, 255)):
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


    def displayResult(self, frame, result, player_gesture, computer_gesture):
        """
        Display the result of the game.

        Args:
            frame: Frame to display the result on
            result: Result of the game

        Returns:
            frame: Frame with the result displayed on it
        """

        if result == 1:
            msg = "You win!"
        elif result == -1:
            msg = "You lose!"
        elif result == 0:
            msg = "It's a draw!"
        else:
            msg = "Invalid gesture!"

        result = f"You played {player_gesture} | Computer played {computer_gesture}"
        cv2.putText(frame, result, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)
        frame = self.centerText(msg, frame, colour=(0, 255, 0))
        return frame

    def displayScore(self, frame, player_score, computer_score):
        """
        Display the score of the game.

        Args:
            frame: Frame to display the score on
            player_score: Player's score
            computer_score: Computer's score

        Returns:
            frame: Frame with the score displayed on it
        """

        msg = f"Player: {player_score} | Computer: {computer_score}"
        frame = cv2.putText(frame, msg, (10, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        return frame


