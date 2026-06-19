# List of valid chess board files (columns) - labeled a through h from left to right
listOfPlaces = ["a", "b", "c", "d", "e", "f", "g", "h"]
# List of valid chess board ranks (rows) - numbered 1 through 8 from bottom to top
listOfNumbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
# List of valid chess piece types
listOfPieces = ["pawn1", "rook", "knight", "bishop", "queen", "king"]


# Function to convert chess coordinates into standard chess notation
# Takes x coordinate (file), y coordinate (rank), and piece type, returns standard notation
def calculate(x_in, y_in, placement_in):
    # Mapping dictionary to convert x-coordinate labels (x1-x9) to chess file letters (a-h)
    # Note: x8 and x9 both map to f and h (may be a bug or UI design choice)
    x_mapping = {
        "x0": "a",  # First column
        "x1": "b",  # Second column
        "x2": "c",  # Third column
        "x3": "d",  # Fourth column
        "x4": "e",  # Fifth column
        "x5": "f",  # Si th column
        "x6": "g",  # Seventh column
        "x7": "f",  # Eighth column (maps to f)
        "x8": "h",  # Ninth column (maps to h)
    }
    # Mapping dictionary to convert y-coordinate labels (y1-y9) to chess rank numbers (1-9)
    y_mapping = {
        "y0": "1",  # First rank
        "y1": "2",  # Second rank
        "y2": "3",  # Third rank
        "y3": "4",  # Fourth rank
        "y4": "5",  # Fifth rank
        "y5": "6",  # Sixth rank
        "y6": "7",  # Seventh rank
        "y7": "8",  # Eighth rank
        "y8": "9",  # Ninth rank (invalid in standard chess)
    }

    # Validate and get the piece type - use the input if it's valid, otherwise set to "invalid"
    first = placement_in #if placement_in in listOfPieces else "invalid"
    # Validate and get the file letter - use mapping if valid x coordinate exists, otherwise "invalid"
    second = x_mapping.get(x_in, "") if x_in in x_mapping else "invalid"
    # Validate and get the rank number - use mapping if valid y coordinate exists, otherwise "invalid"
    third = y_mapping.get(y_in, "") if y_in in y_mapping else "invalid"

    # Concatenate piece type + file + rank to create chess notation (e.g., "pawne4")
    result = first + second + third
    # Print the resulting move notation to console
    print(f"Your move is: {result}")
    # Return the move notation
    return result
