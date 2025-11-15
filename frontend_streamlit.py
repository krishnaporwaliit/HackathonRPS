import streamlit as st
import subprocess
import sys
import os

st.set_page_config(page_title="Rock-Paper-Scissors", page_icon="🎮")

st.title("Rock-Paper-Scissors Launcher 🎮")
st.write("Select the number of rounds and click Start to play your game!")

# Slider for number of rounds
rounds = st.slider("Number of rounds:", 1, 20, 3)

# Start button
if st.button("Start Game"):
    st.write(f"Launching game for {rounds} rounds...")
    
    # Path to your game file
    game_path = os.path.abspath("trial1.py")
    
    try:
        # Launch the game
        subprocess.Popen([sys.executable, game_path, str(rounds)], cwd=os.getcwd())
        st.success("Game launched! Check your OpenCV window.")
    except Exception as e:
        st.error(f"Failed to launch the game: {e}")
