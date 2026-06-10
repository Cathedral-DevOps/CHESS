
listOfPlaces = ["a", "b", "c", "d", "e", "f", "g", "h"]
listOfNumbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
listOfPieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]

def calculate(x_in, y_in, placement_in):
    x_mapping = {
        "x1": "a",
        "x2": "b",
        "x3": "c",
        "x4": "d",
        "x5": "e",
        "x6": "f",
        "x7": "g",
        "x8": "f",
        "x9": "h",
    }
    y_mapping = {
        "y1": "1",
        "y2": "2",
        "y3": "3",
        "y4": "4",
        "y5": "5",
        "y6": "6",
        "y7": "7",
        "y8": "8",
        "y9": "9",
    }

    first = placement_in if placement_in in listOfPieces else "invalid"
    second = x_mapping.get(x_in, "") if x_in in x_mapping else "invalid"
    third = y_mapping.get(y_in, "") if y_in in y_mapping else "invalid"

    result = first + second + third
    print(f"Your move is: {result}")
    return result
