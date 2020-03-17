import random


def displayRules():
    # Returns the rules of how to play the game.
    return """
    RULES FOR TIC-TAC-TOE:

    1. The game is played on a grid that's 3 squares by 3 squares.

    2. You will play against the computer. One of you will be X, and the other will be O. 
       Players take turns putting their marks in empty squares. Who goes first will be decided using a coin toss.

    3. The first player to get 3 of their marks in a row (up, down, across, or diagonally) is the winner.

    4. When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.
    
    """


def drawBoard():
    # Draw the board for the game to be played on.
    return f"""
         |     |     
      {MOVES_LIST[6]}  |  {MOVES_LIST[7]}  |  {MOVES_LIST[8]}  
    _____|_____|_____
         |     |     
      {MOVES_LIST[3]}  |  {MOVES_LIST[4]}  |  {MOVES_LIST[5]}  
    _____|_____|_____
         |     |     
      {MOVES_LIST[0]}  |  {MOVES_LIST[1]}  |  {MOVES_LIST[2]}  
         |     |     
    
    """


def playerSelectedMarkers():
    # Return markers for both players.
    playerLetter = ""
    computerLetter = ""
    while not (playerLetter == "X" or playerLetter == "O"):
        print("Do you want to be 'X' or 'O'?")
        playerLetter = input().upper()
    if playerLetter == "X":
        playerLetter = PLAYER_LETTERS[0]
        computerLetter = PLAYER_LETTERS[1]
    elif playerLetter == "O":
        playerLetter = PLAYER_LETTERS[1]
        computerLetter = PLAYER_LETTERS[0]
    return playerLetter, computerLetter


def selectWhoPlaysFirst():
    # Player gets to choose who plays first if he / she wins the coin toss.
    global turn
    playFirst = ""
    while not (playFirst == "y" or playFirst == "n"):
        print(f"{playerName}, do you want to go first? Type 'y' for yes and 'n' for no.")
        playFirst = input().lower()
    if playFirst == "y":
        print(f"{playerName} will play first.")
        turn = PLAYERS[0]
    else:
        print(f"Computer will go first.")
        turn = PLAYERS[1]
    return turn


def playerGameLoop():
    # Loop for the player's turn
    nextMove = ""
    while nextMove == "":
        print("""Enter your move from 1 - 9 to place your marker in the designated block. See below guide:

                 |     |
              7  |  8  |  9
            _____|_____|_____
                 |     |
              4  |  5  |  6
            _____|_____|_____
                 |     |
              1  |  2  |  3
                 |     |

                    """)
        # Get player's move
        nextMove = input()
        # Check if player's move is valid or not.
        if nextMove not in VALID_MOVES:
            # Invalid move.
            print("That is not a valid move. Please enter numbers from 1 - 9 only.")
            nextMove = ""
        else:
            if MOVES_LIST[int(nextMove) - 1] == " ":
                # Valid move.
                MOVES_LIST[int(nextMove) - 1] = playerLetter
                print(f"Player has placed an {playerLetter} in block {nextMove}.")
            else:
                # Move has already been made
                print("Move has already been made")
                print(drawBoard())
                nextMove = ""


def isWinner(listOfMoves, character):
    # Check if there is a winner.
    isWinner = False
    if listOfMoves[0] == listOfMoves[1] == listOfMoves[2] == character:
        isWinner = True
    elif listOfMoves[3] == listOfMoves[4] == listOfMoves[5] == character:
        isWinner = True
    elif listOfMoves[6] == listOfMoves[7] == listOfMoves[8] == character:
        isWinner = True
    elif listOfMoves[0] == listOfMoves[3] == listOfMoves[6] == character:
        isWinner = True
    elif listOfMoves[1] == listOfMoves[4] == listOfMoves[7] == character:
        isWinner = True
    elif listOfMoves[2] == listOfMoves[5] == listOfMoves[8] == character:
        isWinner = True
    elif listOfMoves[0] == listOfMoves[4] == listOfMoves[8] == character:
        isWinner = True
    elif listOfMoves[2] == listOfMoves[4] == listOfMoves[6] == character:
        isWinner = True
    return isWinner


def isGameTied():
    # Check for tied game.
    isGameTied = False
    if " " not in MOVES_LIST:
        isGameTied = True
    return isGameTied


def defensiveMove(boardCopy, possibleMoves):
    # Look for a defensive move - stop the player from winning
    for move in possibleMoves:
        boardCopy[VALID_MOVES.index(move)] = playerLetter
        isWinningMove = isWinner(boardCopy, playerLetter)
        if isWinningMove:
            boardCopy[VALID_MOVES.index(move)] = " "
            computerMove = move
            return computerMove


def aiStrategy():
    # Determines a strategy for the computer to follow during game play.
    possibleMoves = [move for move in VALID_MOVES if MOVES_LIST[int(move) - 1] == " "]
    desiredMoves = []
    computerMove = ""
    boardCopy = MOVES_LIST

    # Check for a block move - stop the player from winning.
    computerMove = defensiveMove(boardCopy, possibleMoves)

    if computerMove == "":
        # No block move, check for a corner move, or the center block.
        for move in possibleMoves:
            if move in CORNER_MOVES:
                desiredMoves.append(move)
            elif move == VALID_MOVES[4]:
                desiredMoves.append(move)
            boardCopy[VALID_MOVES.index(move)] = " "

    if len(desiredMoves) >= 1:
        for possibleMove in possibleMoves:
            boardCopy[VALID_MOVES.index(possibleMove)] = computerLetter
            # Check if move would result in a win and choose a move that would.
            isWinningMove = isWinner(boardCopy, computerLetter)
            if isWinningMove:
                computerMove = possibleMove
                break
            else:
                boardCopy[VALID_MOVES.index(possibleMove)] = " "
                continue
        # If not a winning move, make a random corner move.
        if computerMove == "":
                computerMove = random.choice(desiredMoves)

    # If no corner move, make a side move
    else:
        for move in possibleMoves:
            if move in SIDE_MOVES:
                desiredMoves.append(move)

        if len(desiredMoves) >= 1:
            for possibleMove in possibleMoves:
                boardCopy[VALID_MOVES.index(possibleMove)] = computerLetter
                # Check if move would result in a win and choose a move that would.
                isWinningMove = isWinner(boardCopy, computerLetter)
                if isWinningMove:
                    computerMove = possibleMove
                    break
                else:
                    boardCopy[VALID_MOVES.index(possibleMove)] = " "
                    continue
            # If not a winning move, make a random side move.
            if computerMove == "":
                computerMove = random.choice(desiredMoves)

    print(f"Computer has placed an {computerLetter} in block {computerMove}.")
    if computerMove == "":
        raise ValueError("No value has been set for computer move.")
    else:
        MOVES_LIST[int(computerMove) - 1] = computerLetter


if __name__ == "__main__":

    # Constants
    MOVES_LIST = [" " for i in range(9)]
    VALID_MOVES = ("1", "2", "3", "4", "5", "6", "7", "8", "9")
    CORNER_MOVES = (VALID_MOVES[0], VALID_MOVES[2], VALID_MOVES[6], VALID_MOVES[8])
    SIDE_MOVES = (VALID_MOVES[1], VALID_MOVES[3], VALID_MOVES[5], VALID_MOVES[7])
    PLAYER_LETTERS = ("X", "O")
    PLAYERS = ("Player", "Computer")

    letsPlay = False

    # Intro
    print("Welcome to Tic Tac Toe!")
    playerName = ""
    while len(playerName) == 0:
        print("Please enter your name: ")
        playerName = input().title()
    print(f"Welcome {playerName}! ", end="")

    userInput = " "
    while not (userInput == "" or userInput == "h"):
        print("Press 'ENTER' to play a new game, or press 'h' for a guide on how to play.")
        userInput = input().lower()

    if userInput.lower().startswith("h"):
        letsPlay = False
        print(displayRules())
        print("Press 'ENTER' to play a new game, or any other key to exit")
        userInput = input()
        # Check if user has pressed ENTER to proceed or not.
        if not userInput == "":
            print(f"You have chosen not to proceed. Goodbye {playerName}!")
            letsPlay = False
        else:
            letsPlay = True
    else:
        letsPlay = True

    if letsPlay:
        # Coin toss to decide who plays first and who gets to choose between 'X' and 'O'.
        print(f"The computer will flip a coin, {playerName} gets to choose heads or tails.")
        playerCoinToss = ""
        while not (playerCoinToss == "h" or playerCoinToss == "t"):
            print("Please enter 'h' for heads, or 't' for tails.")
            playerCoinToss = input().lower()

        coinToss = random.randint(1, 2)
        print()

        if (coinToss == 1 and playerCoinToss == "h") or (coinToss == 2 and playerCoinToss == "t"):
            # Player wins the coin toss:
            print(f"{playerName} wins the coin toss.")
            print()
            playerLetter, computerLetter = playerSelectedMarkers()
            print(f"Player will be letter '{playerLetter}', computer will be letter '{computerLetter}'")
            turn = selectWhoPlaysFirst()

        else:
            # Computer wins the coin toss:
            print("Computer wins the coin toss.")
            # Randomly select who will play first - 1 means computer will go first, 2 means player will go first.
            computerPlaysFirst = random.randint(1, 2)
            if computerPlaysFirst == 1:
                print("Computer will play first")
                turn = PLAYERS[1]
            else:
                print(f"{playerName} will play first.")
                turn = PLAYERS[0]

            # Randomly select which letter will represent the players.
            computerLetterIndex = random.randint(0, 1)
            if computerLetterIndex == 0:
                computerLetter = PLAYER_LETTERS[0]
                playerLetter = PLAYER_LETTERS[1]
            else:
                computerLetter = PLAYER_LETTERS[1]
                playerLetter = PLAYER_LETTERS[0]
            print(f"Computer will be letter {computerLetter}. Player will be letter {playerLetter}.")

        print()

        while letsPlay:

            while turn == PLAYERS[0]:
                playerGameLoop()
                # Check if player has won
                isWinningMove = isWinner(MOVES_LIST, playerLetter)
                if isWinningMove:
                    print(f"Congratulations {playerName}! You win!")
                    print(drawBoard())
                    letsPlay = False
                    break
                else:
                    # Check if game is tied
                    gameEndsInTie = isGameTied()
                    if gameEndsInTie:
                        print(f"The game ends in a tie. Well played {playerName}!")
                        print(drawBoard())
                        letsPlay = False
                        break
                    else:
                        # Computer's turn
                        turn = PLAYERS[1]
                        print(f"{turn}'s turn.")
                        print()
                        print(drawBoard())

            while turn == PLAYERS[1]:
                aiStrategy()
                # Check if computer wins
                isWinningMove = isWinner(MOVES_LIST, computerLetter)
                if isWinningMove:
                    print(f"Sorry {playerName}, the computer wins!")
                    print(drawBoard())
                    letsPlay = False
                    break
                else:
                    # Check if game ends in a tie
                    gameEndsInTie = isGameTied()
                    if gameEndsInTie:
                        print(f"The game ends in a tie. Well played {playerName}!")
                        print(drawBoard())
                        letsPlay = False
                        break
                    else:
                        # Player's turn
                        turn = PLAYERS[0]
                        print(f"{turn}'s turn.")
                        print()
                        print(drawBoard())
