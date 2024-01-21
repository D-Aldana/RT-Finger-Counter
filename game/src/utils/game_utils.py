from random import randint

class GameStart:
    def __init__(self):
        self.game_start = False

    def setGameStart(self, game_start):
        """
        Set the game start flag.

        Args:
            game_start: Game start flag

        Returns:
            None
        """

        self.game_start = game_start

    def getGameStart(self):
        """
        Get the game start flag.

        Args:
            None

        Returns:
            game_start: Game start flag
        """

        return self.game_start


class GameUtils:

    def __init__(self):
        self.username = None
        self.player_score = 0
        self.computer_score = 0
        self.consecutive_wins = 0

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
            self.consecutive_wins += 1
        elif result == -1:
            self.addComputerScore()
            self.consecutive_wins = 0
        
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

    def getConsecutiveWins(self):
        """
        Get the number of consecutive wins.

        Args:
            None

        Returns:
            consecutive_wins: Number of consecutive wins
        """

        return self.consecutive_wins
    
    def checkHighScore(self, redis, consecutive_wins, socketio):
        """
        Check if the consecutive wins is in the top 5 high scores. Add the score to the high scores if it is.

        Args:
            redis: Redis object
            consecutive_wins: Number of consecutive wins

        Returns:
            True if the score is top 1, False otherwise
        """
        
        if consecutive_wins == 0:
            return False
        
        # while self.username is None:
        #     socketio.emit('get_username')

        if self.username is None:
            return False

        high_scores = redis.zrange("high_scores", 0, 4, desc=True, withscores=True)

        if len(high_scores) < 5:
            redis.zadd("high_scores", {self.username: consecutive_wins})
            return True

        lowest_score = high_scores[-1][1]

        if consecutive_wins > lowest_score:
            redis.zremrangebyscore("high_scores", lowest_score, lowest_score)
            redis.zadd("high_scores", {self.username: consecutive_wins})
            return True

        return False
        

    def getHighScores(self, redis):
        """
        Get the high scores.

        Args:
            redis: Redis object

        Returns:
            high_scores: List of high scores
        """

        high_scores = redis.zrange("high_scores", 0, 4, desc=True, withscores=True)
        high_scores_data = [{"username": username, "score": int(score)} for username, score in high_scores]
        print(high_scores_data)
        return high_scores_data

    # def newHighScore(self, socketio):
    #     """
    #     Display a message that the player has a new high score.

    #     Args:
    #         None

    #     Returns:
    #         None
    #     """

    #     socketio.emit('new_high_score', {'username': self.username, 'consecutive_wins': self.consecutive_wins})

    def resetScore(self):
        """
        Reset the player's and computer's score.

        Args:
            None

        Returns:
            None
        """

        self.player_score = 0
        self.computer_score = 0

    def sendScore(self, socketio):
        """
        Send the score to the socketio server.

        Args:
            socketio: Socketio object
            player_score: Player's score
            computer_score: Computer's score

        Returns:
            None
        """

        socketio.emit('score', {'player_score': self.player_score, 'computer_score': self.computer_score, 'consecutive_wins': self.consecutive_wins})

    def sendTopScores(self, socketio, redis):
        """
        Send the top scores to the socketio server.

        Args:
            socketio: Socketio object
            redis: Redis object

        Returns:
            None
        """

        socketio.emit('top_scores', self.getHighScores(redis))

    def getUsername(self):
        """
        Get the username.

        Args:
            None

        Returns:
            username: Username
        """

        return self.username

    def setUsername(self, username):
        """
        Set the username.

        Args:
            username: Username

        Returns:
            None
        """

        self.username = username
