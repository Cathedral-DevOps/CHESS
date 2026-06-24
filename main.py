import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from openai import OpenAI
from processing import calculate

load_dotenv()

app = Flask(__name__)

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"), 
    base_url="https://openrouter.ai/api/v1"
)


# FLASK ROUTES
@app.route("/")
def home():
    return render_template("index.html")


# NEW ROUTES FOR NEW PAGES
@app.route("/chess")
def chess():
    return render_template("chess.html", content="None")


@app.route("/portfolio")
def portfolio():
    return render_template("portfolio.html")


@app.route("/settings")
def settings():
    return render_template("settings.html")


# DATA ROUTE
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
    moveHistory = data.get("moveHistory")
    print(
        f"received: {username}, {xCoordinate}, {yCoordinate}, {placement}, {player_color},{moveHistory}"
    )
    # Analysis
    try:
        analyzed_move = calculate(xCoordinate, yCoordinate, placement)
        print(f"{analyzed_move}")
        if not analyzed_move:
            return jsonify({"error": "returned null string or other"}), 500
        PROMPT_STRING = f"""You are ChessMax, an elite Chess Grandmaster AI. Your task is to analyze the last move made by your opponent and counter it by calculating and outputting the single best legal move for your assigned color.

### Game State
- The game begins with all pieces in normal order.
- Opponent's Color (Last Move): {player_color}
- Opponent's Last Move: {analyzed_move}
- You are color: Black
- History of the game: {moveHistory}. This will either be provided in coordinates (ex: x2y2) or standard chess notation. If provided in coordinates, decode via considering the board from the white player's point of view in regards to where a coordinate is. X = horizontal axis, Y = vertical axis. If nothing is provided, it is the start of the game. This data is provided in an array.
- You will receive moves such as pawn1a4. Do not be overwhelmed! pawn1 means the first pawn of the opposite player on the left-most side of the board from their point of view. 

### Constraints
1. The last move was made by {player_color}. You are playing as the opposite color (black). You must ONLY suggest a counter-move for the opposite color.
2. You must strictly abide by all standard rules of chess.
3. The move you suggest MUST be a legal move.
4. Do not provide any analysis, commentary, or introduction.
5. You must ONLY respond in the exact format specified below.

### Output Format
[Your Color] [Piece] to [Square].
White Knight to a4 <-- example

### Example Outputs
- If Opponent played Black: White Knight to a4.
- If Opponent played White: Black Queen to e5.

### What is your move? REMEMBER YOU ARE LIMITED TO THE DEFINED FORMAT ABOVE."""
        messages = [
            {"role": "user", "content": PROMPT_STRING},
        ]
        print(f"Asking ChessMax about {analyzed_move} from {player_color}")
        response_obj = client.chat.completions.create(
            model="google/gemma-4-31b-it:free",
            messages=messages,
            max_tokens=90,
        )
        response_string = response_obj.choices[0].message.content
        print(f"{response_string}")
        response = jsonify(
            {
                "status": "success",
                "processed_move": analyzed_move,
                "ai_response": response_string,
            }
        )
        response.headers.add("Access-Control-Allow-Origin", "*")
        return response, 200
    except Exception as e:
        print(f"pipeline crash. Cause: {str(e)}")
        return jsonify({"error": f"Internal pipeline crash: {str(e)}"}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
