from random import randint

class GameUtils:

    def __init__(self):
        self.player_score = 0
        self.computer_score = 0

    def rockPaperScissors(self):
        """
        Returns a random gesture from the game rock, paper, scissors.

        Args:
            None
        
        Returns:
            gesture: Random gesture from the game rock, paper, scissors
        """

        gestures = {
            0: "rock",
            1: "paper",
            2: "scissors"
        }
        result = randint(0, 1000) % 3
        return gestures[result]


    def processGameResult(self, player_gesture, computer_gesture):
        """
        Process the result of the game.

        Args:
            player_gesture: Gesture played by the player (str: rock, paper, scissors)
            computer_gesture: Gesture played by the computer (str: rock, paper, scissors)

        Returns:
            result: Result of the game (str: 1 (win), -1 (lose), 0 (draw))
        """

        # Invalid gesture or no gesture
        if not player_gesture:
            return None
        
        if player_gesture == computer_gesture:
            result = 0
        elif player_gesture == "rock":
            if computer_gesture == "paper":
                result = -1
            else:
                result = 1
        elif player_gesture == "paper":
            if computer_gesture == "scissors":
                result = -1
            else:
                result = 1
        else:
            if computer_gesture == "rock":
                result = -1
            else:
                result = 1

        print(f"Player: {player_gesture} | Computer: {computer_gesture} | Result: {result}")

        if result == 1:
            self.addPlayerScore()
        elif result == -1:
            self.addComputerScore()
        
        return result

    def addPlayerScore(self):
        """
        Add a point to the player's score.

        Args:
            None

        Returns:
            None
        """

        self.player_score += 1

    def addComputerScore(self):
        """
        Add a point to the computer's score.

        Args:
            None

        Returns:
            None
        """

        self.computer_score += 1

    def getPlayerScore(self):
        """
        Get the player's score.

        Args:
            None

        Returns:
            player_score: Player's score
        """

        return self.player_score

    
    def getComputerScore(self):
        """
        Get the computer's score.

        Args:
            None

        Returns:
            computer_score: Computer's score
        """

        return self.computer_score

