import streamlit as st
from streamlit_lottie import st_lottie
import json
import datetime

# ---- Funktion zum Laden der Lottie-Animation ----
def load_lottiefile(path: str):
    with open(path, "r") as f:
        return json.load(f)

# ---- Initialisierung ----
st.set_page_config(page_title="🎓 Studien-Dashboard", layout="centered")
st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

# ---- Animation ----
lottie_animation = load_lottiefile("assets/animation.json")

# ---- Header ----
st_lottie(lottie_animation, height=200)
st.title("📚 Studien-Dashboard")

# ---- Aufgabenliste (ToDos) ----
st.subheader("✅ Aufgabenliste")
if "tasks" not in st.session_state:
    st.session_state.tasks = []

new_task = st.text_input("Neue Aufgabe eingeben")
if st.button("➕ Aufgabe hinzufügen") and new_task:
    st.session_state.tasks.append({"text": new_task, "done": False})

for i, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        st.session_state.tasks[i]["done"] = st.checkbox(task["text"], value=task["done"], key=f"task_{i}")
    with col2:
        if st.button("🗑️", key=f"delete_{i}"):
            st.session_state.tasks.pop(i)
            st.experimental_rerun()

# ---- Stundenplan (Platzhalter) ----
st.subheader("📅 Stundenplan")
st.write("Dies ist ein Platzhalter. Später kannst du Drag&Drop oder Bearbeitung einbauen.")
schedule = {
    "Montag": ["Mathematik", "Technische Mechanik"],
    "Dienstag": ["Elektrotechnik", "Informatik"],
    "Mittwoch": ["Maschinenelemente", "Projektarbeit"],
    "Donnerstag": ["Frei"],
    "Freitag": ["Werkstoffkunde"]
}
for tag, fächer in schedule.items():
    st.write(f"**{tag}**: {', '.join(fächer)}")

# ---- Projektübersicht ----
st.subheader("🧠 Projekte")
projektname = st.text_input("Neues Projekt eingeben")
fortschritt = st.slider("Fortschritt (%)", 0, 100, 0)

if st.button("💾 Projekt speichern"):
    if "projekte" not in st.session_state:
        st.session_state.projekte = []
    st.session_state.projekte.append({"name": projektname, "fortschritt": fortschritt})

if "projekte" in st.session_state:
    for projekt in st.session_state.projekte:
        st.markdown(f"**{projekt['name']}**")
        st.progress(projekt['fortschritt'])

# ---- Terminliste ----
st.subheader("📆 Termine")
datum = st.date_input("Wähle ein Datum", datetime.date.today())
beschreibung = st.text_input("Was steht an?")
if st.button("📌 Termin hinzufügen"):
    if "termine" not in st.session_state:
        st.session_state.termine = []
    st.session_state.termine.append((datum, beschreibung))

if "termine" in st.session_state:
    for d, beschr in st.session_state.termine:
        st.markdown(f"📍 **{d.strftime('%d.%m.%Y')}** – {beschr}")
