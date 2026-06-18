
let placement = "pawn";
let xCoordinate = "x1";
let yCoordinate = "y1";

class ChessPiece {
    constructor(type, color, position) {
        this.type = type;
        this.color = color;
        this.position = position;
    }

getSymbol(){
    const symbols = {
        'king': { 'white': '♔', 'black': '♚' },
        'queen': { 'white': '♕', 'black': '♛' },
        'rook': { 'white': '♖', 'black': '♜' },
        'bishop': { 'white': '♗', 'black': '♝' },
        'knight': { 'white': '♘', 'black': '♞' },
        'pawn': { 'white': '♙', 'black': '♟' }
        };
        return symbols[this.type][this.color];
    }
}

const pieces = [
    new ChessPiece('king', 'white', 'e1'),
    new ChessPiece('queen', 'white', 'd1'),
    new ChessPiece('rook', 'white', 'a1'),
    new ChessPiece('rook', 'white', 'h1'),
    new ChessPiece('bishop', 'white', 'c1'),
    new ChessPiece('bishop', 'white', 'f1'),
    new ChessPiece('knight', 'white', 'b1'),
    new ChessPiece('knight', 'white', 'g1'),
    new ChessPiece('pawn', 'white', 'a2'),
    new ChessPiece('pawn', 'white', 'b2'),
    new ChessPiece('pawn', 'white', 'c2'),
    new ChessPiece('pawn', 'white', 'd2'),
    new ChessPiece('pawn', 'white', 'e2'),
    new ChessPiece('pawn', 'white', 'f2'),
    new ChessPiece('pawn', 'white', 'g2'),
    new ChessPiece('pawn', 'white', 'h2'),

    new ChessPiece('king', 'black', 'e8'),
    new ChessPiece('queen', 'black', 'd8'),
    new ChessPiece('rook', 'black', 'a8'),
    new ChessPiece('rook', 'black', 'h8'),
    new ChessPiece('bishop', 'black', 'c8'),
    new ChessPiece('bishop', 'black', 'f8'),
    new ChessPiece('knight', 'black', 'b8'),
    new ChessPiece('knight', 'black', 'g8'),
    new ChessPiece('pawn', 'black', 'a7'),
    new ChessPiece('pawn', 'black', 'b7'),
    new ChessPiece('pawn', 'black', 'c7'),
    new ChessPiece('pawn', 'black', 'd7'),
    new ChessPiece('pawn', 'black', 'e7'),
    new ChessPiece('pawn', 'black', 'f7'),
    new ChessPiece('pawn', 'black', 'g7'),
    new ChessPiece('pawn', 'black', 'h7'),

];

function positionToId(position) {
    const file = position.charCodeAt(0) - 97 // a - h to 0 - 7
    const rank = parseInt(position[1]) - 1 // 1 - 8 to 0 - 7
    return `square-${file}-${rank}`;
}

pieces.forEach( piece => {
    const squareId = positionToId(piece.position);
    const square = document.getElementById(squareId);
    if (square) {
        const span = createElement(`span`);
        span.classname = 'piece';
        span.textContent = piece.getSymbol();
        square.appendChild(span);
    }
});
//send to flask python.

async function sendToFlask(moveData){
    const payload = {
        username: moveData.username || "Player",
        xCoordinate: moveData.x,
        yCoordinate: moveData.y,
        placement: moveData.placementString,
        player_color: moveData.color
    };
    const requestOptions = {
        method: 'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body: JSON.stringify(payload)
    }
   try {
    const response = await fetch('/api/receive-data', requestOptions);
    if (!response.ok){
        const errorPayload = await response.json();
        throw new Error(errorPayload.error || errorPayload.message || 'Server error');

    }
    const result = await response.json();
    console.log("Analysis successful:",result.processed_move);
    console.log("ChessMax has stated:", result.ai_response);
    return result;
   } catch (error){
    console.error("Failed to fetch.", error.message);
    alaert("ChessMax pipeline error: "+ error.message);
   }
}