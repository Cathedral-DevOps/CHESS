
// AI Content
// JavaScript was by far the hardest part of this project, especially because we do not have full or any real knowledge of the lang.
// I decided that it was okay to use AI for certain parts of this to make up for time, and then learn what everything does so
// I actually understand everything and not just ai it all like a bum. Plus, I can reuse this code for future projects!
function normalizePieceName(pieceId) {
  const rawPiece = pieceId.split("-")[1] || "piece";
  const match = rawPiece.match(/[a-z]+/i);
  return (match ? match[0] : "piece").toLowerCase();
}

document.addEventListener("DOMContentLoaded", () => {
  let highlightedSquare;
  const piecesList = document.querySelectorAll(".piece");
  const squares = document.querySelectorAll(".board-location");
  const moveHistory = [];
  let currentSetting = localStorage.getItem("settings")

  // 1. Drag Start: Track piece ID & Ensure unique IDs
  piecesList.forEach((piece, index) => {
    // Ensure every piece has a unique ID so we move the correct element
    piece.id = piece.id + "-" + index;

    piece.addEventListener("dragstart", (e) => {
      const playerColor = "w";
      const pieceColor = e.target.id.startsWith("w") ? "w" : "b";
      if (pieceColor !== playerColor) {
        e.preventDefault();
        return;
      }
      e.dataTransfer.setData("text/plain", e.target.id);
    });
  });

  // 2. Allow Drag Over
  squares.forEach((square) => {
    square.addEventListener("dragover", (e) => {
      e.preventDefault();
    });

    // 3. Drop handler
    square.addEventListener("drop", (e) => {
      e.preventDefault();
      const pieceId = e.dataTransfer.getData("text/plain");
      const draggedPiece = document.getElementById(pieceId);
      if (!draggedPiece) return;

      // Find the actual square container, even if dropping directly onto text
      const targetSquare = e.target.closest(".board-location");
      if (targetSquare) {
        // Check if the square already contains a different piece
        const existingPiece = targetSquare.querySelector(".piece");
        let wasCaptured = false;
        if (existingPiece && existingPiece !== draggedPiece) {
          // Capture logic: remove the old piece, then add the new one
          existingPiece.remove();
          targetSquare.appendChild(draggedPiece);
          wasCaptured = true;
        } else {
          // Empty square logic: clear out old coordinate text and append
          if (targetSquare.children.length === 0) {
            targetSquare.textContent = "";
          }
          targetSquare.appendChild(draggedPiece);
        }

        // --- TRACK THE MOVE ---
        const squareId = targetSquare.id;
        const xVal = "x" + squareId.charAt(1);
        const yVal = "y" + squareId.charAt(3);

        // Figure out piece name (e.g. w-pawn5-3 -> pawn)
        const movedPiece = normalizePieceName(draggedPiece.id);
        let newestMove = movedPiece + " " + xVal + " " + yVal;
        moveHistory.push(newestMove);
        // Track the color safely
        let movedColor = "Black";
        if (
          draggedPiece.classList.contains("white-piece") ||
          draggedPiece.id.startsWith("w-")
        ) {
          movedColor = "White";
        } else if (
          draggedPiece.classList.contains("black-piece") ||
          draggedPiece.id.startsWith("b-")
        ) {
          movedColor = "Black";
        }

        const moveDescription = `${movedColor} ${movedPiece} to square (${xVal}, ${yVal})`;
        console.log(`Tracked Move: ${moveDescription}`);
        if (currentSetting === "NoChessMax"){
          console.log("Dovetail is disabled. Move data will not be sent to the server.");
          return;
        }
        else 
          {
        // Send the updated move data directly using the key names Flask expects!
        sendToFlask({
          xCoordinate: xVal,
          yCoordinate: yVal,
          placement: movedPiece,
          player_color: movedColor,
          username: "Player",
          highlightedSquare: "None",
          moveHistory: moveHistory,
          wasCaptured: wasCaptured,
        })};
      }
    });
  });
});
//vibe coded all down

function parseAIMove(aiResponse) {
  // Matches the format: "Black Knight to f6"
  const match = aiResponse.match(/(\w+)\s+(\w+)\s+to\s+(\w)(\d)/i);
  if (!match) return null;

  const [, color, piece, targetFile, targetRank] = match;
  const fileMap = { a: 0, b: 1, c: 2, d: 3, e: 4, f: 5, g: 6, h: 7 };
  const rankMap = { 1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6, 8: 7 };

  return {
    color: color.toLowerCase(),
    piece: piece.toLowerCase(),
    targetX: fileMap[targetFile.toLowerCase()],
    targetY: rankMap[targetRank],
  };
}

function movePieceToSquare(piece, targetSquare) {
  if (!piece || !targetSquare) return;
  const existing = targetSquare.querySelector(".piece");
  if (existing && existing !== piece) existing.remove();
  targetSquare.textContent = "";
  targetSquare.appendChild(piece);
}

function findCorrectPiece(color, pieceType, targetX, targetY) {
  const colorPrefix = color === 'white' ? 'w-' : 'b-';
  // Gather every piece of this type (e.g., all black knights)
  const candidates = Array.from(document.querySelectorAll(`[id^="${colorPrefix}${pieceType}"]`));
  
  for (const piece of candidates) {
    const parent = piece.parentElement;
    if (!parent || !parent.id.startsWith('x')) continue;
    
    // Extract current coordinates from the square ID (e.g., "x1y7" -> x=1, y=7)
    const currX = parseInt(parent.id.charAt(1));
    const currY = parseInt(parent.id.charAt(3));
    
    const dx = Math.abs(targetX - currX);
    const dy = Math.abs(targetY - currY);

    // Basic distance validation to find the piece that can legally make this move
    let canMove = false;
    switch (pieceType) {
      case 'knight': canMove = (dx === 1 && dy === 2) || (dx === 2 && dy === 1); break;
      case 'bishop': canMove = (dx === dy); break;
      case 'rook': canMove = (dx === 0 || dy === 0); break;
      case 'queen': canMove = (dx === dy) || (dx === 0 || dy === 0); break;
      case 'king': canMove = (dx <= 1 && dy <= 1); break;
      case 'pawn': 
        const direction = color === 'white' ? 1 : -1;
        const yDiff = targetY - currY;
        if (dx === 0 && (yDiff === direction || (yDiff === 2 * direction && (currY === 1 || currY === 6)))) {
          canMove = true; // Moving straight forward
        } else if (dx === 1 && yDiff === direction) {
          canMove = true; // Diagonal capture
        }
        break;
    }

    if (canMove) return piece; // Found the right one!
  }
  
  return candidates[0] || null; // Fallback just in case
}

function executeBotMove(aiResponse) {
  const move = parseAIMove(aiResponse);
  if (!move) {
    console.error("AI response format invalid. Expected 'Color piece to Square'.");
    return;
  }

  // Use our smart checker to find the piece instead of blindly guessing
  const pieceToMove = findCorrectPiece(move.color, move.piece, move.targetX, move.targetY);

  if (pieceToMove) {
    const targetSquare = document.getElementById(`x${move.targetX}y${move.targetY}`);
    movePieceToSquare(pieceToMove, targetSquare);
  } else {
    console.error(`Could not find a valid ${move.color} ${move.piece} to move!`);
  }
}

// kind of vibe coded kind of not.
// Send data to Flask Python server
async function sendToFlask(moveData) {
  // Packaging the payload with the exact keys you specified
  const payload = {
    username: moveData.username || "Player",
    xCoordinate: moveData.xCoordinate || xCoordinate,
    yCoordinate: moveData.yCoordinate || yCoordinate,
    placement: moveData.placement || placement,
    player_color: moveData.player_color || "Black",
    highlightedSquare: moveData.highlightedSquare,
    moveHistory: moveData.moveHistory,
    wasCaptured: moveData.wasCaptured || false,
  };

  const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  };

  try {
    const response = await fetch("/api/receive-data", requestOptions);
    if (!response.ok) {
      const errorPayload = await response.json();
      throw new Error(
        errorPayload.error || errorPayload.message || "Server error",
      );
    }
    const result = await response.json();
    console.log("Analysis successful:", result.processed_move);
    console.log("Dovetail has stated:", result.ai_response);

    if (result.whitePoints !== undefined) {
      const whiteScoreEl = document.getElementById("White-Score");
      if (whiteScoreEl) {
        whiteScoreEl.textContent = "White: " + result.whitePoints;
      }
    }
   

    setTimeout(() => {
      executeBotMove(result.ai_response);
    }, 500);

    return result;
  } catch (error) {
    console.error("Dovetail pipeline error:", error.message);
  }
}
