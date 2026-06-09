
listOfPlaces = ["a", "b", "c", "d", "e", "f", "g", "h"]
listOfNumbers = ["1", "2", "3", "4", "5", "6", "7", "8"]
listOfPieces = ["pawn", "rook", "knight", "bishop", "queen", "king"]

def calculate(x_in, y_in, placement_in):
    x_mapped = {
        "x1": "a",
        "x2": "b",
        "x3": "c",
        "x4": "d",
        "x5": "e",
        "x6": "f",
        "x7": "g",
        "x8": "f",
        "x9": "h",
    }.get(x_in, x_in)
    y_mapped = {
        "y1": "1",
        "y2": "2",
        "y3": "3",
        "y4": "4",
        "y5": "5",
        "y6": "6",
        "y7": "7",
        "y8": "8",
        "y9": "9",
    }.get(y_in, y_in)

    if placement_in in listOfPieces:
        first = placement_in
    if x_in in listOfPlaces:
        second = x_mapped
    if y_in in listOfNumbers:
        third = y_mapped

    result = first + second + third
    print(f"Your move is: {result}")
    return result
