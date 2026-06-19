document.addEventListener("DOMContentLoaded", () => {
  const piecesList = document.querySelectorAll(".piece");
  const squares = document.querySelectorAll(".board-location");

  // 1. Drag Start: Track piece ID & Ensure unique IDs
  piecesList.forEach((piece, index) => {
    // Ensure every piece has a unique ID so we move the correct element
    piece.id = piece.id + "-" + index;

    piece.addEventListener("dragstart", (e) => {
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
        if (existingPiece && existingPiece !== draggedPiece) {
          // Capture logic: remove the old piece, then add the new one
          existingPiece.remove();
          targetSquare.appendChild(draggedPiece);
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

        // Figure out piece name (e.g. w-pawn-3 -> pawn)
        const idParts = draggedPiece.id.split("-");
        const movedPiece = idParts[1] || "piece";

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

        // Send the updated move data directly using the key names Flask expects!
        sendToFlask({
          xCoordinate: xVal,
          yCoordinate: yVal,
          placement: movedPiece,
          player_color: movedColor,
          username: "Player",
        });
      }
    });
  });
});

// Send data to Flask Python server
async function sendToFlask(moveData) {
  // Packaging the payload with the exact keys you specified
  const payload = {
    username: moveData.username || "Player",
    xCoordinate: moveData.xCoordinate || xCoordinate,
    yCoordinate: moveData.yCoordinate || yCoordinate,
    placement: moveData.placement || placement,
    player_color: moveData.player_color || "Black",
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
    console.log("ChessMax has stated:", result.ai_response);
    document.querySelector(".score").innerHTML =
      `Score: Black: ---- White: ---- Best Move: ${result.ai_response}`;
    return result;
  } catch (error) {
    console.error("ChessMax pipeline error:", error.message);
  }
}
