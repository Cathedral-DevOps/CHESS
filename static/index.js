async function sendVariablesToBackend(){
    
    document.getElementById("moveButton").addEventListener("click", async (event) => {
    event.preventDefault();
    const xCoordinate = 'x1';
    const yCoordinate = 'y4';
    const username = 'mathew';
    const placement = 'pawn';
    const payload = {
        xCoordinate: xCoordinate,
        yCoordinate: yCoordinate,
        username: username,
        placement: placement
    };
    try {
        const response = await fetch('http://localhost:5000/api/receive-data',{
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(payload)
        });
        if (response.ok){
            const jsonResponse = await response.json();
            console.log("Success response from Flask:", jsonResponse);
            document.getElementById("aiResponse").innerText = `Best Move: ${jsonResponse.ai_response}`;
        } else {
            console.error("HTTP error status:", response.status);
            document.getElementById("aiResponse").innerText = `Error: HTTP ${response.status}`;
        }
    
    } catch (error) {
        console.error("Network or connection error:", error);
        document.getElementById("aiResponse").innerText = `Error: ${error.message}`;
    }
    });
}
sendVariablesToBackend();