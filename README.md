# AI Survivor: The Last Agent Standing

A multi-agent AI debate tournament. Contestant agents (each with their own
personality, profession, and memory) debate assigned topics, get scored by
a Judge agent, and the lowest scorer is eliminated each round — until one
champion remains.

Runs fully locally via [Ollama](https://ollama.com) — no API key required.

## Setup

```cmd
python -m venv venv
venv\Scripts\activate
pip install ollama streamlit
```

Make sure Ollama is installed and running, then pull the model:

```cmd
ollama pull llama3.1:8b
```

## Running

**Terminal (single round):**
```cmd
python run_round.py
```

**Streamlit dashboard:**
```cmd
streamlit run app.py
```

Click **Run Next Round** to run a debate: contestants are assigned
for/against stances on a random topic, give opening statements, rebut an
opponent, get scored by the Judge, and the lowest scorer is eliminated
(with a host explanation of why). Repeat until one contestant remains.

## Project structure
ai-survivor/

├── app.py                 # Streamlit dashboard  
├── run_round.py           # Core round logic (CLI + reusable by app.py)  
├── agents/
│   ├── contestant.py      # Contestant class: personality, stance, memory  
│   └── judge.py           # Scoring + elimination explanation  
└── debate/
      └── topics.py          # Topic list + stance assignment 

## Current scope (v1)

- 4 contestants, single-elimination
- Opening statement + one rebuttal per round
- Judge scores on logic, evidence, persuasion, creativity, clarity, relevance
- Memory: tracks rounds survived, informal friends/enemies

## Not yet built (from original spec)

- 8 contestants, Fact Checker agent, Audience agent, dynamic events
  (lightning round, hidden immunity, etc.), full statistics engine
- Persistent round history in the dashboard (currently overwritten each run)
- SQLite persistence (currently in-memory only, resets on restart)