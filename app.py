# app.py
import streamlit as st
import matplotlib.pyplot as plt
import random

# --- Team and Task Setup ---
team_proficiency = { "Seth": 1.5, "Peter": .7, "Margaret": 1.0, "Isabelle": 0.7,
    "Megan": 0.5, "Christian": 0.8, "Andre": 1.0, "Nicole": 1.2,
    "Angie": 1.5, "Daniel": 1.2, "Michael": 1.0 }

team_cost = { "Seth": 520, "Peter": 400, "Margaret": 240, "Isabelle": 240,
    "Megan": 240, "Christian": 400, "Andre": 240, "Nicole": 200,
    "Angie": 220, "Daniel": 240, "Michael": 210 }

tasks_info = {
    "Storyboarding": (3, 5, 8), "Design": (8, 10, 12), "Layout": (2, 4, 6),
    "Animation": (10, 12, 15), "Compositing": (2, 4, 6), "Sound": (2, 3, 5),
    "Director": (5, 7, 9)
}

# --- UI: Assignment ---
st.title("Animation Project Simulator")
st.header("Team Assignment per Phase")

task_assignments = {}
for task in tasks_info:
    selected = st.multiselect(f"{task} team:", team_proficiency.keys(), key=task)
    task_assignments[task] = selected

simulation_runs = st.slider("Number of Simulations", 1000, 20000, 10000)

# --- Simulation ---
def pert_sample(o, m, p):
    return (o + 4*m + p) / 6 + random.gauss(0, (p - o) / 6)

if st.button("Run Simulation"):
    durations = []
    costs = []
    phase_costs_accum = {t: [] for t in tasks_info}
    phase_durations_accum = {t: [] for t in tasks_info}

    for _ in range(simulation_runs):
        total_dur, total_cost = 0, 0
        for task, (o, m, p) in tasks_info.items():
            sampled = pert_sample(o, m, p)
            people = task_assignments[task]
            if people:
                speed = sum(1/team_proficiency[p] for p in people)
                adj_dur = sampled / (speed**0.5)
                cost = sum(team_cost[p] * adj_dur for p in people)
            else:
                adj_dur = sampled
                cost = 0
            total_dur += adj_dur
            total_cost += cost
            phase_costs_accum[task].append(cost)
            phase_durations_accum[task].append(adj_dur)

        durations.append(total_dur)
        costs.append(total_cost)

    # --- Output ---
    st.subheader("Results")
    st.write(f"Mean Duration: {sum(durations)/len(durations):.1f} days")
    st.write(f"Mean Cost: ${sum(costs)/len(costs):,.2f}")

    fig1, ax1 = plt.subplots()
    ax1.hist(durations, bins=50, color='skyblue', edgecolor='black')
    ax1.set_title("Project Duration Distribution")
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots()
    ax2.hist(costs, bins=50, color='lightgreen', edgecolor='black')
    ax2.set_title("Project Cost Distribution")
    st.pyplot(fig2)

    st.subheader("Mean Cost per Phase")
    for task in tasks_info:
        st.write(f"{task}: ${sum(phase_costs_accum[task])/len(phase_costs_accum[task]):,.2f} "
                 f"over {sum(phase_durations_accum[task])/len(phase_durations_accum[task]):.1f} days")