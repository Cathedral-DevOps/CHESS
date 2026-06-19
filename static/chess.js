let placement = "pawn"; 
let xCoordinate = "x1"; 
let yCoordinate = "y1"; 

document.addEventListener("DOMContentLoaded", () => { 
  const piecesList = document.querySelectorAll('.piece'); // Renamed slightly to avoid clash with array below
  const squares = document.querySelectorAll('.board-location'); 

  // 1. Drag Start: Track piece ID 
  piecesList.forEach(piece => { 
    piece.addEventListener('dragstart', (e) => { 
      e.dataTransfer.setData('text/plain', e.target.id); 
    }); 
  }); 

  // 2. Allow Drag Over 
  squares.forEach(square => { 
    square.addEventListener('dragover', (e) => { 
      e.preventDefault(); 
    }); 

    // 3. Drop handler 
    square.addEventListener('drop', (e) => { 
      e.preventDefault(); 
      const pieceId = e.dataTransfer.getData('text/plain'); 
      const draggedPiece = document.getElementById(pieceId); 
      if (!draggedPiece) return; 

      // CRITICAL FIX: Always find the actual square container, even if dropping directly onto text 
      const targetSquare = e.target.closest('.board-location'); 
      if (targetSquare) { 
        // Check if the square already contains a different piece 
        const existingPiece = targetSquare.querySelector('.piece'); 
        if (existingPiece && existingPiece !== draggedPiece) { 
          // Capture logic: remove the old piece, then add the new one 
          existingPiece.remove(); 
          targetSquare.appendChild(draggedPiece); 
        } else { 
          // Empty square logic: clear out old coordinate text (like "B8") and append 
          // This checks if the square only contains plain text strings 
          if (targetSquare.children.length === 0) { 
            targetSquare.textContent = ''; 
          } 
          targetSquare.appendChild(draggedPiece); 
        } 
      } 
    }); 
  }); // <-- FIXED: This closes the squares.forEach loop correctly


  function positionToId(position) { 
    const file = position.charCodeAt(0) - 97; // a - h to 0 - 7 
    const rank = parseInt(position[1]) - 1; // 1 - 8 to 0 - 7 
    return `square-${file}-${rank}`; 
  } 

  chessPieces.forEach(piece => { 
    const squareId = positionToId(piece.position); 
    const square = document.getElementById(squareId); 
    if (square) { 
      const span = document.createElement(`span`); // FIXED: Added 'document.' prefix 
      span.className = 'piece'; // FIXED: Changed classname to className (camelCase)
      span.textContent = piece.getSymbol(); 
      square.appendChild(span); 
    } 
  }); 
}); // <-- FIXED: This closes the DOMContentLoaded listener correctly

// send to flask python. 
async function sendToFlask(moveData) { 
  const payload = { 
    username: moveData.username || "Player", 
    xCoordinate: moveData.x || xCoordinate, 
    yCoordinate: moveData.y || yCoordinate, 
    placement: moveData.placementString || placement, 
    player_color: moveData.color || "Black", 
  }; 
  
  const requestOptions = { 
    method: 'POST', 
    headers: { 'Content-Type': 'application/json' }, 
    body: JSON.stringify(payload) 
  }; 
  
  try { 
    const response = await fetch('/api/receive-data', requestOptions); 
    if (!response.ok) { 
      const errorPayload = await response.json(); 
      throw new Error(errorPayload.error || errorPayload.message || 'Server error'); 
    } 
    const result = await response.json(); 
    console.log("Analysis successful:", result.processed_move); 
    console.log("ChessMax has stated:", result.ai_response); 
    return result; 
  } catch (error) { 
    console.error("Failed to fetch.", error.message); 
    alert("ChessMax pipeline error: " + error.message); 
  } 
}
