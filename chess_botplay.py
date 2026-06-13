import torch
from transformers import pipeline
from main import analyzed_move, player_color

last_move = analyzed_move

model_id = "google/gemma-2-2b-it"
pipe = pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto",
)
print("success")

messages = [
            {
                "role": "user",
                "content": f"You are a chess grandmaster AI called PlayBot. You must take this last move from a chess game, {analyzed_move}, and predict the next best move. Only respond with the move the player should make in english. Example response: Knight to a4. Only respond like this. Predict in accordance with strategies that the top chess players use. The player plays as {player_color}. What move should you make next? This is what you are trying to answer. You are playing the opposite color."
            },
        ]
print(f"Asking ChessMax about {analyzed_move} from {player_color}")
outputs = pipe(messages, max_new_tokens=190, clean_up_tokenization_spaces=True)
bot_string = outputs[0]["generated_text"][-1]["content"]
print(f"Bot move is {bot_string}")