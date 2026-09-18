import random
import streamlit as st

from agents.contestant import default_contestants
from debate.topics import TOPICS
from run_round import run_round

st.set_page_config(page_title="AI Survivor", layout="wide")

if "contestants" not in st.session_state:
    st.session_state.contestants = default_contestants()
if "champion" not in st.session_state:
    st.session_state.champion = None

st.title("🏆 AI Survivor: The Last Agent Standing")

active = [c for c in st.session_state.contestants if not c.eliminated]

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Contestants")
    for c in st.session_state.contestants:
        status = "❌ eliminated" if c.eliminated else "✅ active"
        st.markdown(f"**{c.name}** ({c.profession}) — {status}  \nSurvived: {c.rounds_survived}")

    run_disabled = len(active) <= 1
    if st.button("▶ Run Next Round", disabled=run_disabled, use_container_width=True):
        st.session_state.run_round_now = True

    if len(active) == 1 and st.session_state.champion is None:
        st.session_state.champion = active[0].name

    if st.session_state.champion:
        st.success(f"🏆 Champion: {st.session_state.champion}")

with col2:
    if st.session_state.get("run_round_now"):
        st.session_state.run_round_now = False
        topic = random.choice(TOPICS)
        st.subheader(f"Topic: {topic}")

        log_area = st.container()
        events = []

        def on_event(kind, payload):
            events.append((kind, payload))
            with log_area:
                if kind == "stance":
                    st.caption(payload["text"])
                elif kind == "opening":
                    st.markdown(f"**{payload['name']}** ({payload['profession']}, *{payload['stance']}*)")
                    st.write(payload["text"])
                elif kind == "rebuttal":
                    st.markdown(f"**{payload['name']}** rebuts **{payload['target']}**")
                    st.write(payload["text"])
                elif kind == "score":
                    st.caption(
                        f"{payload['name']} scored {payload['total']} "
                        f"(opening {payload['opening_total']} + rebuttal {payload['rebuttal_total']})"
                    )
                elif kind == "leaderboard":
                    st.subheader("Leaderboard")
                    for name, total in payload["ranked"]:
                        tag = " ❌ ELIMINATED" if name == payload["eliminated"] else ""
                        st.write(f"{name}: {total}{tag}")
                    st.error(f"**Why {payload['eliminated']} was eliminated:** {payload['reason']}")

        eliminated_name = run_round(active, topic, on_event=on_event)
        st.rerun()
    else:
        st.info("Click **Run Next Round** to start a debate.")