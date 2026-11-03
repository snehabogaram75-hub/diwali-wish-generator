import joblib
import streamlit as st
import streamlit.components.v1 as components
from concurrent.futures import ThreadPoolExecutor
from wish import generate_wish
from card_html import card_html

@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

def best_wish(name, relation, language, n=3):
    model = load_model()
    with ThreadPoolExecutor(n) as ex:
        wishes = list(ex.map(lambda _: generate_wish(name, relation, language), range(n)))
    scores = model.predict_proba(wishes)[:, 1]
    return sorted(zip(scores, wishes), reverse=True)

st.set_page_config(page_title="Diwali Wish Generator", page_icon="🪔")
st.title("🪔 Diwali Wish Generator")
st.caption("Personalized Diwali wishes, in your own style!")

name = st.text_input("Name", placeholder="Ravi")
relation = st.selectbox("Relation", ["friend", "amma", "nanna", "brother", "sister", "boss", "colleague", "teacher", "student", "relative"])
language = st.radio("Language", ["Tanglish", "English", "Hindi"], horizontal=True)

if st.button("Generate Wish ✨", disabled=not name.strip()):
    with st.spinner("Writing 3 wishes and picking the best one..."):
        st.session_state["ranked"] = best_wish(name.strip(), relation, language)
        st.session_state["name"] = name.strip()

if "ranked" in st.session_state:
    ranked = st.session_state["ranked"]
    components.html(card_html(st.session_state["name"], ranked[0][1]), height=800)
    with st.expander("Classifier ranking (natural-score)"):
        for s, w in ranked:
            st.write(f"**{s:.2f}** — {w}")
