import random
from agents.contestant import default_contestants
from agents.judge import score_statement
from debate.topics import TOPICS, assign_stances
from agents.judge import score_statement, explain_elimination


def run_round(contestants, topic, on_event=None):
    """
    on_event(kind, payload) is called as things happen, so a UI can render
    progressively. kind is one of:
    "stance", "opening", "rebuttal", "score", "leaderboard", "eliminated"
    """
    def emit(kind, payload):
        if on_event:
            on_event(kind, payload)
        else:
            print(payload.get("text", payload))

    assign_stances(contestants)
    for c in contestants:
        emit("stance", {"name": c.name, "stance": c.stance, "text": f"{c.name} is arguing: {c.stance.upper()}"})

    statements = {}
    for c in contestants:
        statement = c.opening_statement(topic)
        statements[c.name] = statement
        emit("opening", {"name": c.name, "profession": c.profession, "stance": c.stance, "text": statement})

    for_side = [c for c in contestants if c.stance == "for"]
    against_side = [c for c in contestants if c.stance == "against"]
    pairs = list(zip(for_side, against_side))

    rebuttals = {}
    for a, b in pairs:
        r1 = a.rebuttal(topic, b.name, statements[b.name])
        rebuttals[a.name] = r1
        emit("rebuttal", {"name": a.name, "target": b.name, "text": r1})

        r2 = b.rebuttal(topic, a.name, statements[a.name])
        rebuttals[b.name] = r2
        emit("rebuttal", {"name": b.name, "target": a.name, "text": r2})

    results = {}
    for c in contestants:
        open_scores = score_statement(c.name, topic, statements[c.name])
        rebuttal_scores = score_statement(c.name, topic, rebuttals.get(c.name, ""))
        total = open_scores["total"] + rebuttal_scores["total"]
        results[c.name] = total
        emit("score", {
            "name": c.name, "total": total,
            "opening_total": open_scores["total"], "rebuttal_total": rebuttal_scores["total"],
        })

    ranked = sorted(results.items(), key=lambda x: -x[1])
    eliminated_name = ranked[-1][0]

    elimination_reason = explain_elimination(eliminated_name, results[eliminated_name], ranked, topic)

    emit("leaderboard", {"ranked": ranked, "eliminated": eliminated_name, "reason": elimination_reason})

    for c in contestants:
        opponents_scores = [(n, s) for n, s in results.items() if n != c.name]
        survived = c.name != eliminated_name
        c.update_memory(results[c.name], opponents_scores, survived)

    emit("eliminated", {"name": eliminated_name})

    return eliminated_name


def main():
    contestants = default_contestants()
    topic = random.choice(TOPICS)
    print(f"\n=== TOPIC: {topic} ===\n")
    eliminated_name = run_round(contestants, topic)

    remaining = [c for c in contestants if c.name != eliminated_name]
    print(f"\n{eliminated_name} has been eliminated. {len(remaining)} contestants remain.")

    for c in remaining:
        print(f"{c.name} -> rounds_survived={c.rounds_survived}, enemies={c.enemies}, friends={c.friends}")


if __name__ == "__main__":
    main()