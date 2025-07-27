import streamlit as st
import datetime

# CSS laden
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("assets/style.css")

st.set_page_config(page_title="🎓 Studien-Dashboard", layout="centered")

def glass_container(func):
    st.markdown('<div class="block-container">', unsafe_allow_html=True)
    func()
    st.markdown('</div>', unsafe_allow_html=True)

# Aufgabenverwaltung
if "tasks" not in st.session_state:
    st.session_state.tasks = []

def add_task():
    if st.session_state.new_task_text.strip():
        st.session_state.tasks.append({"text": st.session_state.new_task_text, "done": False})
        st.session_state.new_task_text = ""

# Haupttitel
st.title("📚 Studien-Dashboard")

def render_tasks():
    st.subheader("✅ Aufgabenliste")

    st.text_input("Neue Aufgabe eingeben", key="new_task_text", on_change=add_task)

    for i, task in enumerate(st.session_state.tasks):
        cols = st.columns([0.85, 0.15])
        with cols[0]:
            done = st.checkbox(task["text"], value=task["done"], key=f"task_{i}")
            st.session_state.tasks[i]["done"] = done
        with cols[1]:
            if st.button("🗑️", key=f"delete_{i}"):
                st.session_state.tasks.pop(i)
                st.experimental_rerun()

glass_container(render_tasks)

def render_schedule():
    st.subheader("📅 Stundenplan")
    schedule = {
        "Montag": ["Mathematik", "Technische Mechanik"],
        "Dienstag": ["Elektrotechnik", "Informatik"],
        "Mittwoch": ["Maschinenelemente", "Projektarbeit"],
        "Donnerstag": ["Frei"],
        "Freitag": ["Werkstoffkunde"]
    }
    for tag, faecher in schedule.items():
        st.write(f"**{tag}**: {', '.join(faecher)}")

glass_container(render_schedule)

# Projektverwaltung
if "projekte" not in st.session_state:
    st.session_state.projekte = []

def add_project():
    if st.session_state.new_proj_name.strip():
        st.session_state.projekte.append({"name": st.session_state.new_proj_name, "progress": st.session_state.new_proj_progress})
        st.session_state.new_proj_name = ""
        st.session_state.new_proj_progress = 0

def render_projects():
    st.subheader("🧠 Projekte")
    st.text_input("Neues Projekt eingeben", key="new_proj_name")
    st.slider("Fortschritt (%)", 0, 100, key="new_proj_progress")
    if st.button("💾 Projekt speichern"):
        add_project()

    for projekt in st.session_state.projekte:
        st.markdown(f"**{projekt['name']}**")
        st.progress(projekt["progress"])

glass_container(render_projects)

# Termine
if "termine" not in st.session_state:
    st.session_state.termine = []

def add_appointment():
    if st.session_state.new_appointment_desc.strip():
        st.session_state.termine.append((st.session_state.new_appointment_date, st.session_state.new_appointment_desc))
        st.session_state.new_appointment_desc = ""
        st.session_state.new_appointment_date = datetime.date.today()

def render_appointments():
    st.subheader("📆 Termine")
    st.date_input("Datum auswählen", key="new_appointment_date", value=datetime.date.today())
    st.text_input("Beschreibung", key="new_appointment_desc")
    if st.button("📌 Termin hinzufügen"):
        add_appointment()

    for d, beschr in st.session_state.termine:
        st.write(f"📍 **{d.strftime('%d.%m.%Y')}** – {beschr}")

glass_container(render_appointments)
