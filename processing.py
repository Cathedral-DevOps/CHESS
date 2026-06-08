from main import xCoordinate, yCoordinate
first = ''
second = ''
third=''


listOfPlaces = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
listOfNumbers = ['1', '2', '3', '4', '5', '6', '7', '8']
listOfPieces= ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']

selector = input("Select a piece: ")
position = input("Select a position letter: ")
position2 = input("Select a position number: ")

xCoordinate = listOfPlaces[0:8]
yCoordinate = listOfNumbers[0:8]


if selector in listOfPieces:
    first = selector
if position in listOfPlaces:
    second = position
if position2 in listOfNumbers:
    third = position2

result = first + second + third
print(f"Your move is: {result}")