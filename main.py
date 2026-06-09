import torch
from transformers import pipeline
from flask import Flask, render_template, request, jsonify
from processing import calculate

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
    device_map="auto"  # Automatically utilizes Mac hardware optimization (MPS/Metal)
)
print("-------Gemma 2 pipeline loaded successfully!-------")


## FLASK ROUTES

@app.route("/")
def home():
    # Pass None initially so the template knows there is no output yet
    return render_template("index.html", content=None)

#call variables from JavaScript
@app.route('/api/receive-data', methods=['POST', 'OPTIONS'])
def receive_data():
    #Sec Req
    if request.method == 'OPTIONS':
        response = jsonify({"status":"preflight"})
        response.headers.add("Access-Control-Allow-Origin","*")
        response.headers.add("Access-Control-Allow-Headers","Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response, 200
        #capture
    data = request.get_json()
    if not data:
        return jsonify({"status":"error","message":"No data received"}), 4
    username = data.get("username")
    xCoordinate = data.get("xCoordinate")
    yCoordinate = data.get("yCoordinate")
    placement = data.get("placement")
    print(f"Received: {username}, {xCoordinate}, {yCoordinate}, {placement}")
    #run analysis
    analyzed_move = calculate(xCoordinate, yCoordinate, placement)
    print(f"ready for ai. {analyzed_move}")
    return analyzed_move
    #respond
    response = jsonify({
        "status":"success",
        "message": analyzed_move
    })
    response.headers.add("Acess-Control-Allow-Origin","*")
    return response, 200


@app.route('/submit', methods=['POST'])
def submit(analyzed_move):
    captured_entry = request.form.get('lastmove')
    if not captured_entry:
        return render_template("index.html", content="No move entered. Please try again.")


    # Format your prompt as a structured chat history with the NEW dynamic chess move
    messages = [
        {
            "role": "user", 
            "content": f"You are a chess grandmaster AI. Analyze these opening moves and tell me the best response for black. Only mention the name of the move and your confidence out of 100% in a well-formatted way: {analyzed_move}. DO NOT EXPLAIN ANYTHING. ONLY GIVE ME THE MOVE AND CONFIDENCE LEVEL ALONE. MAKE A MOVE THAT IS IMPOSSIBLE TO BEAT."
        },
    ]

    print(f"\n--- Asking Gemma 2 about move: {analyzed_move} ---")
    
    # Generate the text on-demand inside the view function
    outputs = pipe(messages, max_new_tokens=100, clean_up_tokenization_spaces=True)
    gemma_string = outputs[0]["generated_text"][-1]["content"]

    # This return statement fixes the TypeError by rendering the page with the response!
    return render_template("index.html", content=gemma_string, last_move=analyzed_move)


if __name__ == "__main__":
    app.run(host='0.0.0.0',port="5000",debug=True)