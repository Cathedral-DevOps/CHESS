// Define an async function that sends chess move data to the backend server
async function sendVariablesToBackend() {
  // Find the HTML element with ID "moveButton" and attach a click event listener
  document
    .getElementById("moveButton")
    .addEventListener("click", async (event) => {
      // Prevent the default button click behavior (page refresh)
      event.preventDefault();
      // Set the X coordinate of the chess move (file position)
      const xCoordinate = "x1";
      // Set the Y coordinate of the chess move (rank position)
      const yCoordinate = "y4";
      // Set the username of the player making the move
      const username = "mathew";
      // Set the chess piece being moved
      const placement = "pawn";
      const player_color = "white";
      // Create a data object containing all the move information
      const payload = {
        xCoordinate: xCoordinate,  // File position
        yCoordinate: yCoordinate,  // Rank position
        username: username,  // Player name
        placement: placement,  // Piece type
        player_color: player_color,
      };
      // Try to send the data to the backend server
      try {
        // Send a POST request to the Flask backend API with the chess move data
        const response = await fetch("http://localhost:5000/api/receive-data", {
          method: "POST",  // Use POST method to send data
          headers: {
            // Tell the server the data is in JSON format
            "Content-Type": "application/json",
          },
          // Convert the payload object to JSON string and send it as the request body
          body: JSON.stringify(payload),
        });
        // Check if the response status indicates success (200-299)
        if (response.ok) {
          // Parse the response body as JSON
          const jsonResponse = await response.json();
          // Log the success response to browser console for debugging
          console.log("Success response from Flask:", jsonResponse);
          // Update the HTML element with ID "aiResponse" to display the AI's suggested move
          document.getElementById("aiResponse").innerText =
            `Best Move: ${jsonResponse.ai_response}`;
        } else {
          // If the response indicates an error (4xx or 5xx status code)
          console.error("HTTP error status:", response.status);
          // Display error message to the user
          document.getElementById("aiResponse").innerText =
            `Error: HTTP ${response.status}`;
        }
      } catch (error) {
        // Catch network errors or other exceptions
        console.error("Network or connection error:", error);
        // Display the error message to the user
        document.getElementById("aiResponse").innerText =
          `Error: ${error.message}`;
      }
    });
}
// Call the function to attach the event listener when the page loads
sendVariablesToBackend();
