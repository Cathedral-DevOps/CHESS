import torch
from transformers import pipeline
from flask import Flask, render_template, request, jsonify
from processing import calculate

app = Flask(__name__)
model_id = "google/gemma-2-2b-it"
pipe = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)
print("success")


# FLASK ROUTES
@app.route("/")
def home():
    return render_template("index.html")

#NEW ROUTES FOR NEW PAGES
@app.route("/chess")
def chess():
    return render_template("chess.html",content="None")
@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")
@app.route("/settings")
def settings():
    return render_template("settings.html")


#DATA ROUTE
@app.route("/api/receive-data", methods=["POST", "OPTIONS"])
def receive_data():
    if request.method == "OPTIONS":
        response = jsonify({"status": "preflight"})
        response.headers.add("Access-Control-Allow-Origin", "*")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST")
        return response, 200
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data received."}), 400
    username = data.get("username")
    xCoordinate = data.get("xCoordinate")
    yCoordinate = data.get("yCoordinate")
    placement = data.get("placement")
    player_color = data.get("player_color")
    print(f"received: {username}, {xCoordinate}, {yCoordinate}, {placement}")
    # Analysis
    try:
        analyzed_move = calculate(xCoordinate, yCoordinate, placement)
        print(f"{analyzed_move}")
        if not analyzed_move:
            return jsonify({"error": "returned null string or other"}), 500
        messages = [
            {
                "role": "user",
                "content": f"You are a chess grandmaster AI called ChessMax. You must take this last move from a chess game, {analyzed_move}, and predict the next best move. Only respond with the move the player should make in english. Example response: White Knight to a4. Only respond like this. Predict in accordance with strategies that the top chess players use. The player previously played as {player_color}. What move should {player_color} make next? This is what you are trying to answer. Please respond correctly."
            },
        ]
        print(f"Asking ChessMax about {analyzed_move} from {player_color}")
        outputs = pipe(messages, max_new_tokens=420, clean_up_tokenization_spaces=True)
        gemma_string = outputs[0]["generated_text"][-1]["content"]
        print(f"{gemma_string}")
        response = jsonify(
            {
                "status": "success",
                "processed_move": analyzed_move,
                "ai_response": gemma_string,
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200
    except Exception as e:
        print(f"pipeline crash. Cause: {str(e)}")
        return jsonify({"error": f"Internal pipeline crash: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
