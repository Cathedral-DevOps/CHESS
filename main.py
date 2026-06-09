import torch
from transformers import pipeline
from flask import Flask, render_template, request, jsonify
from processing import first, second, third
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


def stringprocesser(captured_entry):
    print(f"Processing: {captured_entry}")
    return captured_entry

## FLASK ROUTES

@app.route("/")
def home():
    # Pass None initially so the template knows there is no output yet
    return render_template("index.html", content=None)

#call variables from JavaScript
@app.route('/receive-data', methods=['POST'])
def receive_data():
    data = request.get_json()
    xCoordinate = data.get('xCoordinate')
    yCoordinate = data.get('yCoordinate')
    print(f"Received from JS ---> xCoordinate: {xCoordinate} and yCoordinate: {yCoordinate}.")
    result = {
        "status":"success",
        "message":f"Date received: {xCoordinate}, {yCoordinate}"
    }
    return jsonify(result), 200


@app.route('/submit', methods=['POST'])
def submit():
    captured_entry = request.form.get('lastmove')
    if not captured_entry:
        return render_template("index.html", content="No move entered. Please try again.")

    processed_move = stringprocesser(captured_entry)

    # Format your prompt as a structured chat history with the NEW dynamic chess move
    messages = [
        {
            "role": "user", 
            "content": f"You are a chess grandmaster AI. Analyze these opening moves and tell me the best response for black. Only mention the name of the move and your confidence out of 100% in a well-formatted way: {processed_move}. DO NOT EXPLAIN ANYTHING. ONLY GIVE ME THE MOVE AND CONFIDENCE LEVEL ALONE. MAKE A MOVE THAT IS IMPOSSIBLE TO BEAT."
        },
    ]

    print(f"\n--- Asking Gemma 2 about move: {processed_move} ---")
    
    # Generate the text on-demand inside the view function
    outputs = pipe(messages, max_new_tokens=100, clean_up_tokenization_spaces=True)
    gemma_string = outputs[0]["generated_text"][-1]["content"]

    # This return statement fixes the TypeError by rendering the page with the response!
    return render_template("index.html", content=gemma_string, last_move=processed_move)


if __name__ == "__main__":
    app.run(debug=True)