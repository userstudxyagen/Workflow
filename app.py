import streamlit as st
import json
import datetime

# CSS laden
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

# Seite konfigurieren
st.set_page_config(page_title="🎓 Studien-Dashboard", layout="centered")

# Glasiger Container Style (über div)
def glass_container(content_func):
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    content_func()
    st.markdown('</div>', unsafe_allow_html=True)

# Initialisiere Tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Neue Aufgabe hinzufügen
def add_task():
    if st.session_state.new_task_text.strip():
        st.session_state.tasks.append({"text": st.session_state.new_task_text, "done": False})
        st.session_state.new_task_text = ""

# Header
st.title("📚 Studien-Dashboard")

# Aufgabenbereich mit Animationen
def render_tasks():
    st.subheader("✅ Aufgabenliste")

    st.text_input("Neue Aufgabe eingeben", key="new_task_text", on_change=add_task)
    
    # Liste der Tasks
    for i, task in enumerate(st.session_state.tasks):
        key_cb = f"task_done_{i}"
        key_del = f"task_del_{i}"

        # Container mit Slide-In für neue Tasks
        task_container = f'<div class="slide-in" id="task_{i}">'

        st.markdown(task_container, unsafe_allow_html=True)
        cols = st.columns([0.8, 0.2])
        with cols[0]:
            done = st.checkbox(task["text"], value=task["done"], key=key_cb)
            st.session_state.tasks[i]["done"] = done
        with cols[1]:
            if st.button("🗑️", key=key_del):
                # Task löschen mit Fade-Out (optisch nur per CSS hier, tatsächliches Entfernen direkt)
                st.session_state.tasks.pop(i)
                st.experimental_rerun()
        st.markdown("</div>", unsafe_allow_html=True)

glass_container(render_tasks)

# Stundenplan (als Platzhalter, ebenfalls glasig)
def render_schedule():
    st.subheader("📅 Stundenplan")
    schedule = {
        "Montag": ["Mathematik", "Technische Mechanik"],
        "Dienstag": ["Elektrotechnik", "Informatik"],
        "Mittwoch": ["Maschinenelemente", "Projektarbeit"],
        "Donnerstag": ["Frei"],
        "Freitag": ["Werkstoffkunde"]
    }
    for day, subjects in schedule.items():
        st.markdown(f"**{day}**: {', '.join(subjects)}")

glass_container(render_schedule)

# Projekte mit Fortschritt
if "projekte" not in st.session_state:
    st.session_state.projekte = []

def add_project():
    if st.session_state.new_proj_name.strip():
        st.session_state.projekte.append({"name": st.session_state.new_proj_name, "fortschritt": st.session_state.new_proj_prog})
        st.session_state.new_proj_name = ""
        st.session_state.new_proj_prog = 0

def render_projects():
    st.subheader("🧠 Projekte")
    st.text_input("Neues Projekt eingeben", key="new_proj_name")
    st.slider("Fortschritt (%)", 0, 100, key="new_proj_prog")
    if st.button("💾 Projekt speichern"):
        add_project()

    for projekt in st.session_state.projekte:
        st.markdown(f"**{projekt['name']}**")
        st.progress(projekt['fortschritt'])

glass_container(render_projects)

# Termine
if "termine" not in st.session_state:
    st.session_state.termine = []

def add_termin():
    if st.session_state.neuer_termin_beschr.strip():
        st.session_state.termine.append((st.session_state.neuer_termin_datum, st.session_state.neuer_termin_beschr))
        st.session_state.neuer_termin_beschr = ""
        st.session_state.neuer_termin_datum = datetime.date.today()

def render_termine():
    st.subheader("📆 Termine")
    st.date_input("Datum wählen", key="neuer_termin_datum", value=datetime.date.today())
    st.text_input("Beschreibung", key="neuer_termin_beschr")
    if st.button("📌 Termin hinzufügen"):
        add_termin()

    for d, beschr in st.session_state.termine:
        st.markdown(f"📍 **{d.strftime('%d.%m.%Y')}** – {beschr}")

glass_container(render_termine)
