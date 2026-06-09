async function sendVariablesToBackend(){

    const xCoordinate = x1;
    const yCoordinate = y4;
    const username = 'mathew';
    const placement = 'pawn';

    const payload = {
        xCoordinate: xCoordinate,
        yCoordinate: yCoordinate,
        username: username,
        placement: placement
    };
    try {
        const response = await fetch('http://localhost:5000/api/receive_data',{
            method: 'POST',
            headers: {
                'Content-Type':'application/json'
            },
            body: JSON.stringify(payload)
        });
        if (response.ok){
            const jsonResponse = await response.json();
            console.log("Success respone from Flask:", jsonResponse);
            alert(`Flask says: ${jsonResponse.message}`);
        } else {
            console.error("HTTP error status:", response.status);
        }
    
    } catch (error) {
        console.error("Network or connection error:", error);
    }
}
sendVariablesToBackend();