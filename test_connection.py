# test_connection.py
import ollama

MODEL = "gemma4:latest"

def ask_agent(system_prompt: str, user_prompt: str) -> str:
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response["message"]["content"]

if __name__ == "__main__":
    system = (
        "You are a Scientist contestant in a debate tournament. "
        "You value evidence and logic. You are precise but not very persuasive."
    )
    topic = "Should AI replace teachers?"
    reply = ask_agent(system, f"Give a 3-sentence opening statement on: {topic}")
    print(reply)