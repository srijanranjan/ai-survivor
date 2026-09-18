import json
import ollama

MODEL = "gemma4:latest"

JUDGE_SYSTEM = (
    "You are a strict debate judge. You score contestant statements on: "
    "logic, evidence, persuasion, creativity, clarity, relevance. "
    "Each category is scored 0-10. "
    "Respond ONLY with valid JSON, no markdown, no commentary, in this exact format: "
    '{"logic": 0, "evidence": 0, "persuasion": 0, "creativity": 0, "clarity": 0, "relevance": 0}'
)


def score_statement(contestant_name: str, topic: str, statement: str) -> dict:
    prompt = (
        f"Topic: {topic}\n"
        f"Contestant: {contestant_name}\n"
        f"Statement: \"{statement}\"\n"
        f"Score this statement."
    )
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": prompt},
        ],
    )
    raw = response["message"]["content"].strip()

    if raw.startswith("```"):
        raw = raw.strip("`")
        if raw.lower().startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    try:
        scores = json.loads(raw)
    except json.JSONDecodeError:
        scores = {"logic": 5, "evidence": 5, "persuasion": 5, "creativity": 5, "clarity": 5, "relevance": 5}

    scores["total"] = sum(v for k, v in scores.items() if k != "total")
    return scores

def explain_elimination(eliminated_name: str, eliminated_total: int, ranked: list, topic: str) -> str:
    others = ", ".join(f"{n} ({s})" for n, s in ranked if n != eliminated_name)
    prompt = (
        f"Topic: {topic}\n"
        f"Eliminated: {eliminated_name} with a score of {eliminated_total}.\n"
        f"Other scores: {others}\n"
        f"As the tournament host, explain in 1-2 sentences why {eliminated_name} was eliminated this round."
    )
    response = ollama.chat(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are the tournament host. Be concise and slightly dramatic."},
            {"role": "user", "content": prompt},
        ],
    )
    return response["message"]["content"]