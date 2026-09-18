import ollama

MODEL = "gemma4:latest"


class Contestant:
    def __init__(self, name: str, profession: str, personality: str, strengths: str, weaknesses: str):
        self.name = name
        self.profession = profession
        self.personality = personality
        self.strengths = strengths
        self.weaknesses = weaknesses

        # Memory
        self.friends = []
        self.enemies = []
        self.votes_received = []
        self.arguments_made = []
        self.fact_check_history = []
        self.scores_history = []
        self.credibility = 10  # starts neutral-positive
        self.stance = None  # "for" or "against", set per topic
        self.rounds_survived = 0
        self.eliminated = False

    def system_prompt(self) -> str:
        stance_line = ""
        if self.stance:
            stance_line = f"In this debate you must argue strictly {self.stance.upper()} the topic. Do not concede the other side. "
        return (
            f"You are {self.name}, a {self.profession} competing in a debate tournament. "
            f"Personality: {self.personality}. "
            f"Strengths: {self.strengths}. Weaknesses: {self.weaknesses}. "
            f"{stance_line}"
            f"Stay in character. Be concise."
        )

    def _ask(self, user_prompt: str) -> str:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {"role": "system", "content": self.system_prompt()},
                {"role": "user", "content": user_prompt},
            ],
        )
        text = response["message"]["content"]
        self.arguments_made.append(text)
        return text

    def opening_statement(self, topic: str) -> str:
        return self._ask(f"Give a 3-sentence opening statement on: {topic}")

    def rebuttal(self, topic: str, opponent_name: str, opponent_statement: str) -> str:
        prompt = (
            f"Topic: {topic}\n"
            f"{opponent_name} argued: \"{opponent_statement}\"\n"
            f"Give a 2-3 sentence rebuttal."
        )
        return self._ask(prompt)

    def closing_statement(self, topic: str) -> str:
        return self._ask(f"Give a 2-sentence closing statement on: {topic}")

    def update_memory(self, round_total_score: int, opponents_this_round: list, survived: bool):
        self.scores_history.append(round_total_score)
        if survived:
            self.rounds_survived += 1
        else:
            self.eliminated = True

        for opp_name, opp_score in opponents_this_round:
            if opp_score > round_total_score and opp_name not in self.enemies:
                self.enemies.append(opp_name)
            elif opp_score <= round_total_score and opp_name not in self.friends:
                self.friends.append(opp_name)

def default_contestants():
    return [
        Contestant(
            "Dr. Ada", "Scientist",
            "precise, evidence-driven, calm",
            "strong evidence, rigorous logic",
            "weak persuasion, dry delivery",
        ),
        Contestant(
            "Mr. Voss", "Lawyer",
            "sharp, combative, articulate",
            "excellent rebuttals, strong logic",
            "can seem cold or overly aggressive",
        ),
        Contestant(
            "Priya", "Entrepreneur",
            "bold, optimistic, persuasive",
            "creative framing, risk-taking, charismatic",
            "sometimes light on evidence",
        ),
        Contestant(
            "Professor Okafor", "Historian",
            "reflective, measured, draws on precedent",
            "context, credibility, nuance",
            "can be slow to make a decisive point",
        ),
    ]