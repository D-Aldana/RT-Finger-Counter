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

