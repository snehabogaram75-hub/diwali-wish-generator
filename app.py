import streamlit as st
import streamlit.components.v1 as components
from wish import generate_wish
from card_html import card_html

st.set_page_config(page_title="Diwali Wish Generator", page_icon="🪔")
st.title("🪔 Diwali Wish Generator")
st.caption("Personalized Diwali wishes, mee style lo!")

name = st.text_input("Name", placeholder="Ravi")
relation = st.selectbox("Relation", ["friend", "amma", "nanna", "brother", "sister", "boss", "colleague", "teacher", "student", "relative"])
language = st.radio("Language", ["Tanglish", "Telugu", "English", "Hindi"], horizontal=True)

if st.button("Generate Wish ✨", disabled=not name.strip()):
    with st.spinner("Wish rasthunna..."):
        st.session_state["wish"] = generate_wish(name.strip(), relation, language)
        st.session_state["name"] = name.strip()

if "wish" in st.session_state:
    components.html(card_html(st.session_state["name"], st.session_state["wish"]), height=800)
