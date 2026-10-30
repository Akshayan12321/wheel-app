import streamlit as st
import random

st.set_page_config(page_title="Spin Wheel", page_width=1000)

if "colors" not in st.session_state:
    st.session_state.colors = [
        ("Red", "#E53935", "Most Billed Hours", ""),
        ("Orange", "#FB8C00", "Least Missed SLA", ""),
        ("Yellow", "#FDD835", "Kill Rate", ""),
        ("Green", "#43A047", "CSAT Leader", ""),
        ("Blue", "#1E88E5", "Resolved Tickets", ""),
        ("Purple", "#8E24AA", "Avg. Ticket Resolve", ""),
        ("Pink", "#EC407A", "Avg. Response Time", "")
    ]

if "history" not in st.session_state:
    st.session_state.history = []

if "last_winner" not in st.session_state:
    st.session_state.last_winner = "Click SPIN to start!"

st.markdown("""
    <style>
    .stApp { background-color: #0b0b0b; color: #d4af37; }
    h1, h2, h3 { color: #d4af37 !important; text-align: center; }
    .winner-box {
        background-color: #141414;
        border: 2px solid #d4af37;
        padding: 20px;
        text-align: center;
        border-radius: 10px;
        font-size: 24px;
        font-weight: bold;
        color: #d4af37;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Metric Spin Wheel")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Current Metrics on Wheel")
    for idx, (color_name, hex_code, metric, person) in enumerate(st.session_state.colors):
        display_val = f"**{metric}** ➔ {person if person else '*Unassigned*'}"
        st.markdown(f"<span style='color:{hex_code}; font-size:18px;'>■</span> {display_val}", unsafe_allow_html=True)

with col2:
    st.subheader("Controls & History")
    
    if st.button("🎡 SPIN THE WHEEL", use_container_width=True, type="primary"):
        winner_idx = random.randint(0, len(st.session_state.colors) - 1)
        chosen = st.session_state.colors[winner_idx]
        metric_name, person_name = chosen[2], chosen[3]
        
        result_text = f"{metric_name} ({person_name})" if person_name else metric_name
        st.session_state.last_winner = f"WINNER: {result_text}"
        st.session_state.history.append(result_text)

    st.markdown(f'<div class="winner-box">{st.session_state.last_winner}</div>', unsafe_allow_html=True)
    
    st.markdown("### ⚙️ Assign Names")
    with st.form("config_form"):
        updated_colors = []
        for idx, (color_name, hex_code, metric, person) in enumerate(st.session_state.colors):
            new_person = st.text_input(metric, value=person, key=f"input_{idx}")
            updated_colors.append((color_name, hex_code, metric, new_person))
        
        if st.form_submit_button("Save Names"):
            st.session_state.colors = updated_colors
            st.success("Names updated successfully!")
            st.rerun()

    st.markdown("### 📜 Winner History")
    if st.session_state.history:
        for i, h in enumerate(reversed(st.session_state.history[-10:]), 1):
            st.text(f"{i}. {h}")
    else:
        st.text("No spins yet.")
