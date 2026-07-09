listOfPlaces = ["a", "b", "c", "d", "e", "f", "g", "h"]
listOfNumbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
listOfPieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]

def calculate(x_in, y_in, placement_in):
   
    x_mapping = {
        "x0": "A",  # First column
        "x1": "B",  # Second column
        "x2": "C",  # Third column
        "x3": "D",  # Fourth column
        "x4": "E",  # Fifth column
        "x5": "F",  # Si th column
        "x6": "G",  # Seventh column
        "x7": "H",  # Eighth column (maps to f)
    }
    y_mapping = {
        "y0": "1",  # First rank
        "y1": "2",  # Second rank
        "y2": "3",  # Third rank
        "y3": "4",  # Fourth rank
        "y4": "5",  # Fifth rank
        "y5": "6",  # Sixth rank
        "y6": "7",  # Seventh rank
        "y7": "8",  # Eighth rank
    }

    if placement_in == "pawn":
        first = 'pawn'
    else:
        first = placement_in
    second = x_mapping.get(x_in, "") if x_in in x_mapping else "invalid"
    third = y_mapping.get(y_in, "") if y_in in y_mapping else "invalid"

    result = first + second + third
    print(f"Your move is: {result}")
    return result

# ai revised it but I wrote the original and understand the concept
def update_game_state(analyzed_move, response_string, History, takenHistory, whitePoints, wasCaptured=False):
    if response_string is None and analyzed_move is None:
        History.append('Null move from White ,' + " " 'Null move from Black')
        return whitePoints
    if response_string is None or analyzed_move is None:
        return whitePoints
    
    # Check if white player captured a piece
    if wasCaptured:
        piece_taken = f"White captured at {analyzed_move}!"
        takenHistory.append(piece_taken)
        whitePoints += 1
        print(f"Piece captured! White points now: {whitePoints}")
    
    # Always add the move to history
    History.append(f'{analyzed_move} from White , {response_string} from Black')
    print("Piece Moved!")
    
    return whitePoints
