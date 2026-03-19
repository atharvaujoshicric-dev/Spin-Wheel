import streamlit as st
import random
import time
from datetime import datetime, timedelta
from streamlit_confetti import confetti

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyluxe Exclusive", page_icon="🏢", layout="centered")

# --- CUSTOM LUXURY CSS ---
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), 
                    url('https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1920&q=80');
        background-size: cover;
        background-attachment: fixed;
    }
    
    .timer-box {
        background: rgba(212, 175, 55, 0.1);
        border: 1px solid #D4AF37;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        color: #D4AF37;
        font-weight: bold;
        font-size: 18px;
        margin-bottom: 20px;
    }

    .wheel-container { display: flex; justify-content: center; margin: 20px 0; }
    
    .wheel {
        width: 200px; height: 200px; border: 5px solid #D4AF37; border-radius: 50%;
        background: conic-gradient(
            #1a1d23 0deg 45deg, #D4AF37 45deg 90deg, 
            #1a1d23 90deg 135deg, #D4AF37 135deg 180deg, 
            #1a1d23 180deg 225deg, #D4AF37 225deg 270deg, 
            #1a1d23 270deg 315deg, #D4AF37 315deg 360deg
        );
        box-shadow: 0 0 15px rgba(212, 175, 55, 0.4);
    }

    .spinning { animation: spin 1s cubic-bezier(0.15, 0, 0.15, 1) infinite; }
    @keyframes spin { 100% { transform: rotate(3600deg); } }

    .stButton>button {
        background-color: #D4AF37 !important; 
        color: black !important; 
        font-weight: bold !important;
        border-radius: 4px !important;
    }
    
    .prize-card {
        background: rgba(255, 255, 255, 0.05);
        border-left: 5px solid #D4AF37;
        padding: 15px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'spins_left' not in st.session_state:
    st.session_state.spins_left = 2
if 'winner_name' not in st.session_state:
    st.session_state.winner_name = ""
if 'is_spinning' not in st.session_state:
    st.session_state.is_spinning = False
if 'final_prize' not in st.session_state:
    st.session_state.final_prize = None
if 'expiry_time' not in st.session_state:
    st.session_state.expiry_time = None

# --- HEADER ---
st.markdown("<h1 style='text-align:center; color:#D4AF37; margin-bottom:0;'>SKYLUXE</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#aaa;'>RESIDENCES & REWARDS</p>", unsafe_allow_html=True)

# 1. Lead Generation Phase
if not st.session_state.winner_name:
    with st.container():
        st.markdown("### UNLOCK YOUR EXCLUSIVE OFFERS")
        name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        agree = st.checkbox("I agree to the Terms and Conditions of Skyluxe Projects.")
        
        if st.button("REGISTER TO SPIN"):
            if name and phone and agree:
                st.session_state.winner_name = name
                st.session_state.expiry_time = datetime.now() + timedelta(minutes=10)
                st.rerun()
            elif not agree:
                st.warning("Please accept the Terms and Conditions.")
            else:
                st.error("Details required.")

else:
    # 2. Timer & Game Phase
    remaining = st.session_state.expiry_time - datetime.now()
    
    if remaining.total_seconds() <= 0:
        st.error("⌛ This exclusive session has expired.")
    else:
        # Timer Display
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        st.markdown(f'<div class="timer-box">TIME REMAINING: {mins:02d}:{secs:02d}</div>', unsafe_allow_html=True)

        st.write(f"Welcome, *{st.session_state.winner_name}* | Remaining Spins: *{st.session_state.spins_left}*")
        
        # Wheel UI
        wheel_class = "spinning" if st.session_state.is_spinning else ""
        st.markdown(f'<div class="wheel-container"><div class="wheel {wheel_class}"></div></div>', unsafe_allow_html=True)

        if st.session_state.spins_left > 0 and not st.session_state.is_spinning:
            if st.button("🎰 SPIN NOW"):
                st.session_state.is_spinning = True
                st.rerun()

        # Logic for selection
        if st.session_state.is_spinning:
            time.sleep(1.8)
            prizes = [
                "Airpods", "Apple iPad", "Split Air Conditioner", 
                "Double Door Refrigerator", "Spin Again", 
                "Better Luck Next Time", "Better Luck Next Time", "Better Luck Next Time"
            ]
            result = random.choice(prizes)
            
            if result == "Spin Again":
                st.session_state.final_prize = "🔄 SPIN AGAIN! (Chance Preserved)"
            else:
                st.session_state.spins_left -= 1
                st.session_state.final_prize = result
            
            st.session_state.is_spinning = False
            st.rerun()

        # Results Display
        if st.session_state.final_prize:
            st.markdown(f'<div class="prize-card"><h3>RESULT: {st.session_state.final_prize}</h3></div>', unsafe_allow_html=True)
            
            if "Better Luck" not in st.session_state.final_prize and "Spin Again" not in st.session_state.final_prize:
                # Fixed: Removed the 'delay' argument
                confetti(emojis=['🏢', '✨', '🏆'])
                st.balloons()

    if st.session_state.spins_left == 0 and not st.session_state.is_spinning:
        st.info("Please visit the Skyluxe Experience Center to claim your reward.")
        if st.button("New Registration"):
            for key in st.session_state.keys(): del st.session_state[key]
            st.rerun()
