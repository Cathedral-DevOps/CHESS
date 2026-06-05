import torch
from transformers import pipeline
import chess
import random

def generate_moves():
    board = chess.Board()
    move_history = []
    for _ in range(20):
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            break
    chosen_move = random.choice(legal_moves)
    move_string = chosen_move.uci()
    move_history.append(move_string)
    board.push(chosen_move)
    return move_history
def process_chess_game(moves_list):
    print("--- Second Function Activated ---")
    #print(f"Received a sequence of {len(moves_list)} moves.")
    for index, move in enumerate(moves_list):
        print(f"executing step {index +1}: {move}")

my_generated_set = generate_moves()
process_chess_game(my_generated_set)

# We use the 2B Instruction-Tuned variant, which fits comfortably on a laptop
model_id = "google/gemma-2-2b-it"

print("Loading Gemma 2... (Note: The first run will download roughly 5GB of files)")

# Set up the text generation pipeline
pipe = pipeline(
    "text-generation",
    model=model_id,
    # bfloat16 cuts memory usage in half so it runs safely on your Mac
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto"  # Automatically utilizes Mac hardware optimization
)

# Format your prompt as a structured chat history
messages = [
    {
        "role": "user", 
        "content": f"You are a chess grandmaster AI. Analyze these opening moves and tell me the best response for black. Only mention the name of the move and your confidence out of 100% in a well-formatted way: {my_generated_set}."
    },
]

print("\n--- Asking Gemma 2 ---")
outputs = pipe(messages, max_new_tokens=150, clean_up_tokenization_spaces=True)

# Print out just the newly generated text from the model
print(outputs[0]["generated_text"][-1]["content"])