import streamlit as st
import random
import time
import base64
import json
from datetime import datetime, timedelta
import streamlit.components.v1 as components

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyluxe Exclusive", page_icon="🏢", layout="centered")

# --- PREMIUM LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --gold-dim: rgba(201,168,76,0.15);
        --gold-border: rgba(201,168,76,0.35);
        --dark: #0B0C0F;
        --dark-2: #13141A;
        --dark-3: #1C1E27;
        --text-muted: rgba(255,255,255,0.45);
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'Raleway', sans-serif;
    }

    .stApp {
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,0.08) 0%, transparent 70%),
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 60px,
                rgba(201,168,76,0.025) 60px,
                rgba(201,168,76,0.025) 61px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 60px,
                rgba(201,168,76,0.025) 60px,
                rgba(201,168,76,0.025) 61px
            ) !important;
    }

    h1, h2, h3 { font-family: 'Cinzel', serif !important; }

    /* ---- HEADER ---- */
    .luxury-header {
        text-align: center;
        padding: 40px 0 10px;
        position: relative;
    }
    .luxury-header h1 {
        font-family: 'Cinzel', serif;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: 0.35em;
        color: var(--gold-light);
        text-shadow: 0 0 40px rgba(201,168,76,0.3);
        margin: 0;
    }
    .luxury-header p {
        font-family: 'Raleway', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.45em;
        color: var(--text-muted);
        margin: 8px 0 0;
        text-transform: uppercase;
    }

    /* ---- BUTTONS ---- */
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
        color: var(--dark) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.25em !important;
        font-size: 0.78rem !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 14px 36px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---- UTILS ----
def get_image_base64(path):
    try:
        with open(path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode()
    except:
        return ""

wheel_base64 = get_image_base64("wheel.png")

# ---- SESSION STATE ----
if 'winner_name' not in st.session_state:
    st.session_state.winner_name = ""
if 'expiry_time' not in st.session_state:
    st.session_state.expiry_time = None

# ---- HEADER ----
st.markdown("""
<div class="luxury-header">
    <h1>SKYLUXE</h1>
    <p>Residences &nbsp;·&nbsp; Rewards &nbsp;·&nbsp; Legacy</p>
</div>
""", unsafe_allow_html=True)

# =====================
# 1. LEAD GENERATION
# =====================
if not st.session_state.winner_name:
    st.markdown('<div style="text-align:center; color:var(--gold-light); font-family:Cinzel; font-size:1.2rem; letter-spacing:0.2em; margin:20px 0;">UNLOCK YOUR EXCLUSIVE OFFER</div>', unsafe_allow_html=True)
    
    with st.container():
        name = st.text_input("Full Name", placeholder="Enter your name")
        phone = st.text_input("Phone Number", placeholder="Enter your contact number")
        agree = st.checkbox("I agree to the Terms & Conditions and Privacy Policy")

        if st.button("REGISTER & SPIN"):
            if name and phone and agree:
                st.session_state.winner_name = name
                st.session_state.expiry_time = datetime.now() + timedelta(minutes=10)
                st.rerun()
            else:
                st.error("Please complete all fields and agree to the terms.")

# =====================
# 2. GAME PHASE
# =====================
else:
    remaining = st.session_state.expiry_time - datetime.now()
    if remaining.total_seconds() <= 0:
        st.error("⌛ This exclusive session has expired.")
        if st.button("START NEW SESSION"):
            st.session_state.winner_name = ""
            st.rerun()
    else:
        mins, secs = divmod(int(remaining.total_seconds()), 60)
        
        st.markdown(f"""
        <div style="text-align:center; color:var(--text-muted); font-size:0.9rem; margin-bottom:20px;">
            Welcome, <span style="color:var(--gold-light); font-weight:bold;">{st.session_state.winner_name}</span> | 
            Session expires in: <span style="color:var(--gold-light);">{mins:02d}:{secs:02d}</span>
        </div>
        """, unsafe_allow_html=True)

        prizes = [
            {"label": "APPLE IPAD", "icon": "📱"},
            {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},
            {"label": "SPIN AGAIN", "icon": "🔄"},
            {"label": "DOUBLE DOOR REFRIGERATOR", "icon": "❄️"},
            {"label": "SPLIT AIR CONDITIONER", "icon": "💨"},
            {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},
            {"label": "APPLE AIRPODS", "icon": "🎧"},
            {"label": "SPIN AGAIN", "icon": "🔄"}
        ]
        
        prizes_json = json.dumps(prizes)
        
        wheel_html = f"""
        <div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Raleway', sans-serif;">
            <!-- Pointer -->
            <div id="pointer" style="
                width: 0; 
                height: 0; 
                border-left: 15px solid transparent; 
                border-right: 15px solid transparent; 
                border-top: 30px solid #C9A84C; 
                z-index: 100; 
                margin-bottom: -10px; 
                filter: drop-shadow(0 0 10px rgba(201,168,76,0.5));
            "></div>

            <!-- Wheel -->
            <div id="wheel-container" style="
                position: relative; 
                width: 400px; 
                height: 400px; 
                border-radius: 50%; 
                border: 6px solid #C9A84C; 
                box-shadow: 0 0 50px rgba(201,168,76,0.2), inset 0 0 20px rgba(0,0,0,0.5);
                background: #000;
                overflow: hidden;
            ">
                <img id="wheel-img" src="data:image/png;base64,{wheel_base64}" style="
                    width: 100%; 
                    height: 100%; 
                    transition: transform 6s cubic-bezier(0.1, 0, 0, 1); 
                    transform: rotate(0deg); 
                    border-radius: 50%;
                ">
            </div>

            <!-- Spin Button -->
            <button id="spin-button" style="
                margin-top: 30px; 
                padding: 16px 60px; 
                font-size: 1.1rem; 
                font-weight: bold; 
                background: linear-gradient(135deg, #C9A84C, #8B6914); 
                color: #0B0C0F; 
                border: none; 
                border-radius: 4px; 
                cursor: pointer; 
                text-transform: uppercase; 
                letter-spacing: 3px;
                font-family: 'Cinzel', serif;
                box-shadow: 0 10px 20px rgba(0,0,0,0.3);
                transition: transform 0.2s;
            ">SPIN FOR PRIZE</button>

            <!-- Winner Display -->
            <h2 id="winner-display" style="
                margin-top: 25px; 
                color: #E8C97A; 
                font-family: 'Cinzel', serif; 
                text-align: center; 
                min-height: 50px;
                letter-spacing: 1px;
                text-shadow: 0 0 10px rgba(232, 201, 122, 0.5);
            "></h2>
        </div>

        <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
        <script>
        const prizes = {prizes_json};
        const img = document.getElementById('wheel-img');
        const btn = document.getElementById('spin-button');
        const display = document.getElementById('winner-display');
        let currentRotation = 0;

        btn.addEventListener('click', () => {{
            if(btn.disabled) return;
            btn.disabled = true;
            btn.style.opacity = "0.5";
            btn.style.transform = "scale(0.95)";
            display.innerText = "Revealing Your Fortune...";
            
            // Random spins (at least 5 full rotations)
            const extraDegrees = Math.floor(Math.random() * 360);
            const totalDegrees = 1800 + extraDegrees;
            currentRotation += totalDegrees;
            
            img.style.transform = `rotate(${{currentRotation}}deg)`;

            setTimeout(() => {{
                btn.disabled = false;
                btn.style.opacity = "1";
                btn.style.transform = "scale(1)";
                
                // Calculate winner
                const actualDeg = (currentRotation % 360);
                // Pointer is at the top (0 deg). 
                // Each slice is 360 / 8 = 45 degrees.
                // The winning slice index:
                const numSlices = 8;
                const sliceDeg = 360 / numSlices;
                
                // Adjustment: Pointer is at 12 o'clock. 
                // We need to find which slice landed under it.
                // If the wheel rotated X degrees clockwise, the pointer effectively moved X degrees counter-clockwise on the wheel.
                const winningIndex = Math.floor(((360 - (actualDeg % 360)) % 360) / sliceDeg);
                const winner = prizes[winningIndex];
                
                display.innerText = "🎉 " + winner.label + " 🎉";
                
                if (!winner.label.includes("BETTER LUCK")) {{
                    const duration = 3 * 1000;
                    const end = Date.now() + duration;

                    (function frame() {{
                        confetti({{
                            particleCount: 5,
                            angle: 60,
                            spread: 55,
                            origin: {{ x: 0 }},
                            colors: ['#C9A84C', '#E8C97A', '#FFFFFF']
                        }});
                        confetti({{
                            particleCount: 5,
                            angle: 120,
                            spread: 55,
                            origin: {{ x: 1 }},
                            colors: ['#C9A84C', '#E8C97A', '#FFFFFF']
                        }});

                        if (Date.now() < end) {{
                            requestAnimationFrame(frame);
                        }}
                    }}());
                }}
            }}, 6100);
        }});
        </script>
        """
        components.html(wheel_html, height=650)

        if st.button("↩ LOGOUT / NEW REGISTRATION"):
            st.session_state.winner_name = ""
            st.rerun()

    st.markdown('<div style="text-align:center; font-size:0.7rem; color:var(--text-muted); margin-top:50px; letter-spacing: 2px;">SKYLUXE RESIDENCES &nbsp;·&nbsp; ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)
