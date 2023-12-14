from random import randint

def rockPaperScissors():
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


def processGameResult(player_gesture):
    """
    Process the result of the game.

    Args:
        player_gesture: Gesture played by the player (str: rock, paper, scissors)

    Returns:
        result: Result of the game (str: 1 (win), -1 (lose), 0 (draw))
    """
    
    computer_gesture = rockPaperScissors()
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
    return result