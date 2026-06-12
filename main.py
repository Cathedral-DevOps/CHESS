import torch
from transformers import pipeline
from flask import Flask, render_template, request, jsonify
from processing import calculate

# This code is only usable via logging in via terminal with your hugging face authentication token, which can be found on
# huggingface's website (needs an account). The Gemma 2.5 model will be downloaded ON to your device LOCALLY. Do not use this code
# unless your are OK with running a local AI model. For a live demo on our device, please contact Aditya Mathew (PREP2).


app = Flask(__name__)

# We use the 2B Instruction-Tuned variant, which fits comfortably on a laptop
model_id = "google/gemma-2-2b-it"
print("Loading Gemma 2")

# Set up the text generation pipeline globally so it only loads into memory ONCE on startup
pipe = pipeline(
    "text-generation", 
    model=model_id,
    # bfloat16 cuts memory usage in half so it runs safely on your Mac
    model_kwargs={"torch_dtype": torch.bfloat16}, 
    device_map="auto" # Automatically utilizes Mac hardware optimization (MPS/Metal)
)
print("-------Gemma 2 pipeline loaded successfully!-------")

## FLASK ROUTES
@app.route("/")
def home():
    # Pass None initially so the template knows there is no output yet
    return render_template("index.html", content=None)

# Unified Route: Receives data, analyzes it, queries the AI, and returns the response
@app.route('/api/receive-data', methods=['POST', 'OPTIONS'])
def receive_data():
    # Security Response for CORS Preflight requests from browsers
    if request.method == 'OPTIONS':
        response = jsonify({"status":"preflight"})
        response.headers.add("Access-Control-Allow-Origin","*")
        response.headers.add("Access-Control-Allow-Headers","Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response, 200

    # Capture incoming JSON data from JavaScript
    data = request.get_json()
    if not data:
        return jsonify({"status":"error","message":"No data received"}), 400

    username = data.get("username")
    xCoordinate = data.get("xCoordinate")
    yCoordinate = data.get("yCoordinate")
    placement = data.get("placement")
    
    print(f"Received from JS: {username}, {xCoordinate}, {yCoordinate}, {placement}")

    # Run Analysis and AI generation within a single safe lifecycle loop
    try:
        # Step 1: Run your calculation engine
        analyzed_move = calculate(xCoordinate, yCoordinate, placement)
        print(f"Processed Chess Move notation: {analyzed_move}")
        
        if not analyzed_move:
            return jsonify({"error":"The processing script returned an empty string"}), 500

        # Step 2: Format the dynamic prompt for your local Gemma model
        messages = [
            {
                "role": "user", 
                "content": f"You are a chess grandmaster AI. Analyze these opening moves and tell me the best response for black. Only mention the name of the move and your confidence out of 100% in a well-formatted way: {analyzed_move}. DO NOT EXPLAIN ANYTHING. ONLY GIVE ME THE MOVE AND CONFIDENCE LEVEL ALONE. MAKE A MOVE THAT IS IMPOSSIBLE TO BEAT."
            },
        ]
        
        print(f"\n--- Asking Gemma 2 about move: {analyzed_move} ---")
        
        # Step 3: Run the AI execution sequence right here while variables exist in memory
        outputs = pipe(messages, max_new_tokens=100, clean_up_tokenization_spaces=True)
        gemma_string = outputs[0]["generated_text"][-1]["content"]
        print(f"Gemma Response: {gemma_string}")

        # Step 4: Send everything back to your raw JavaScript application
        response = jsonify({
            "status": "success",
            "processed_move": analyzed_move,
            "ai_response": gemma_string
        })
        response.headers.add("Access-Control-Allow-Origin","*")
        return response, 200

    except Exception as e:
        print(f"DEBUG ERROR: pipeline crashed due to {str(e)}")
        return jsonify({"error": f"Internal pipeline crash: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
