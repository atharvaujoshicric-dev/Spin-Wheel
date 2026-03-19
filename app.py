import streamlit as st
import random
import time
import base64
import json
from datetime import datetime
import streamlit.components.v1 as components

# Prize data with ultra-premium color palette - 8 segments
prizes = [
    {"label": "AIRPODS APPLE", "img": "🎧", "color": "#0a0a0a", "accent": "#C9A84C", "text": "#C9A84C"},
    {"label": "BETTER LUCK",   "img": "🍀", "color": "#1C1C1E", "accent": "#8E8E93", "text": "#E5E5EA"},
    {"label": "SPIN AGAIN",    "img": "🔄", "color": "#101010", "accent": "#C9A84C", "text": "#C9A84C"},
    {"label": "IPAD APPLE",    "img": "📱", "color": "#1C1C1E", "accent": "#8E8E93", "text": "#E5E5EA"},
    {"label": "REFRIGERATOR",  "img": "🧊", "color": "#0a0a0a", "accent": "#C9A84C", "text": "#C9A84C"},
    {"label": "BETTER LUCK",   "img": "✨", "color": "#1C1C1E", "accent": "#8E8E93", "text": "#E5E5EA"},
    {"label": "SPIN AGAIN",    "img": "🔄", "color": "#101010", "accent": "#C9A84C", "text": "#C9A84C"},
    {"label": "SPLIT AC",      "img": "❄️", "color": "#1C1C1E", "accent": "#8E8E93", "text": "#E5E5EA"},
]

st.set_page_config(page_title="SKYLUXE — Wheel of Fortune", layout="centered")

# --- PREMIUM LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --gold-dim: rgba(201,168,76,0.1);
        --gold-border: rgba(201,168,76,0.3);
        --dark: #0B0C0F;
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'Raleway', sans-serif;
        overflow: hidden;
    }

    .stApp {
        background-image: radial-gradient(circle at 50% -20%, rgba(201,168,76,0.12) 0%, transparent 80%) !important;
    }

    .block-container {
        padding-top: 0.2rem !important;
        padding-bottom: 0.2rem !important;
        max-width: 450px !important;
    }

    #MainMenu, footer, header {visibility: hidden;}
    
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
        color: var(--dark) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 700 !important;
        letter-spacing: 0.1em !important;
        font-size: 0.7rem !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 8px 15px !important;
        text-transform: uppercase !important;
    }
    </style>

    <div class="skuluxe-header">
        <div class="skuluxe-title">SKYLUXE</div>
        <div class="skuluxe-sub">Wheel of Fortune</div>
        <div class="skuluxe-divider"></div>
    </div>
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

# =====================
# 1. LEAD GENERATION
# =====================
if not st.session_state.winner_name:
    st.markdown("""
    <div style="text-align: center; padding: 30px 0 10px;">
        <h1 style="font-family: 'Cinzel'; color: #E8C97A; letter-spacing: 0.3em; margin: 0; font-size: 2.2rem;">SKYLUXE</h1>
        <p style="font-size: 0.6rem; color: rgba(255,255,255,0.4); letter-spacing: 0.4em; margin: 5px 0 0; text-transform: uppercase;">Residences · Rewards · Legacy</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div style="text-align:center; color:#C9A84C; font-family:Cinzel; font-size:0.85rem; letter-spacing:0.1em; margin:20px 0;">UNLOCK EXCLUSIVE OFFER</div>', unsafe_allow_html=True)
    
    name = st.text_input("Full Name", placeholder="Your Name")
    phone = st.text_input("Phone Number", placeholder="Your Phone")
    agree = st.checkbox("I agree to terms")

    if st.button("REGISTER & SPIN"):
        if name and phone and agree:
            st.session_state.winner_name = name
            st.rerun()
        else:
            st.error("Please fill all fields.")

# =====================
# 2. GAME PHASE
# =====================
else:
    # Top Bar with Logout
    col_welcome, col_logout = st.columns([3, 1])
    with col_welcome:
        st.markdown(f"""
        <div style="color: rgba(255,255,255,0.5); font-size: 0.65rem; letter-spacing: 0.1em; text-transform: uppercase; padding-top: 10px;">
            WELCOME: <span style="color: #E8C97A; font-weight: bold;">{st.session_state.winner_name.upper()}</span>
        </div>
        """, unsafe_allow_html=True)
    with col_logout:
        if st.button("LOGOUT", key="logout_top"):
            st.session_state.winner_name = ""
            st.rerun()

    st.markdown("""
    <div style="text-align: center; margin: 5px 0 15px;">
        <h1 style="font-family: 'Cinzel'; color: #E8C97A; letter-spacing: 0.2em; margin: 0; font-size: 1.6rem;">SKYLUXE</h1>
    </div>
    """, unsafe_allow_html=True)

    # ACCURATE ORDER FROM TOP (0 DEGREES) CLOCKWISE
    prizes = [
        {"label": "APPLE IPAD", "icon": "📱"},              # 0 deg (Top)
        {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},  # 45 deg
        {"label": "SPIN AGAIN", "icon": "🔄"},             # 90 deg
        {"label": "DOUBLE DOOR REFRIGERATOR", "icon": "❄️"}, # 135 deg
        {"label": "SPLIT AIR CONDITIONER", "icon": "💨"},   # 180 deg (Bottom)
        {"label": "BETTER LUCK NEXT TIME", "icon": "❌"},  # 225 deg
        {"label": "APPLE AIRPODS", "icon": "🎧"},          # 270 deg (Left)
        {"label": "SPIN AGAIN", "icon": "🔄"}              # 315 deg
    ]
    
    wheel_html = f"""
    <div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
        <div id="pointer" style="width: 0; height: 0; border-left: 10px solid transparent; border-right: 10px solid transparent; border-top: 22px solid #C9A84C; z-index: 100; margin-bottom: -12px; filter: drop-shadow(0 0 5px rgba(201,168,76,0.5));"></div>

        <div id="wheel-container" style="position: relative; width: 280px; height: 280px; border-radius: 50%; border: 4px solid #C9A84C; box-shadow: 0 0 30px rgba(201,168,76,0.15); background: #000; overflow: hidden;">
            <img id="wheel-img" src="data:image/png;base64,{wheel_base64}" style="width: 100%; height: 100%; transition: transform 6s cubic-bezier(0.1, 0, 0, 1); transform: rotate(0deg); border-radius: 50%;">
        </div>

        <button id="spin-button" style="margin-top: 20px; padding: 10px 40px; font-size: 0.9rem; font-weight: bold; background: linear-gradient(135deg, #C9A84C, #8B6914); color: #0B0C0F; border: none; border-radius: 2px; cursor: pointer; text-transform: uppercase; letter-spacing: 2px; font-family: 'Cinzel', serif; box-shadow: 0 5px 15px rgba(0,0,0,0.4);">SPIN TO WIN</button>

        <h2 id="winner-display" style="margin-top: 15px; color: #E8C97A; font-family: 'Cinzel', serif; text-align: center; font-size: 1.1rem; min-height: 30px; letter-spacing: 1px; text-shadow: 0 0 8px rgba(232, 201, 122, 0.3);"></h2>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/canvas-confetti@1.6.0/dist/confetti.browser.min.js"></script>
    <script>
    const prizes = {json.dumps(prizes)};
    const img = document.getElementById('wheel-img');
    const btn = document.getElementById('spin-button');
    const display = document.getElementById('winner-display');
    let currentRotation = 0;

    btn.addEventListener('click', () => {{
        if(btn.disabled) return;
        btn.disabled = true;
        btn.style.opacity = "0.6";
        display.innerText = "WAITING FOR LUCK...";
        
        const extraDegrees = Math.floor(Math.random() * 360);
        currentRotation += 1800 + extraDegrees;
        img.style.transform = `rotate(${{currentRotation}}deg)`;

        setTimeout(() => {{
            btn.disabled = false;
            btn.style.opacity = "1";
            
            const netRotation = (currentRotation % 360);
            const numSlices = 8;
            const sliceDeg = 360 / numSlices;
            const winningIndex = Math.floor(((360 - netRotation + (sliceDeg / 2)) % 360) / sliceDeg);
            const winner = prizes[winningIndex];
            
            display.innerText = "🎉 " + winner.label + " 🎉";
            
            // Logic: Hide button if not "SPIN AGAIN"
            if (winner.label !== "SPIN AGAIN") {{
                btn.style.display = 'none';
                display.innerHTML += '<div style="font-size: 0.7rem; color: #8E8E93; margin-top: 5px; font-family: Raleway;">SCREENSHOT TO CLAIM YOUR PRIZE</div>';
            }} else {{
                display.innerText = "🔄 SPIN AGAIN! 🔄";
            }}
            
            if (!winner.label.includes("BETTER LUCK") && winner.label !== "SPIN AGAIN") {{
                confetti({{ particleCount: 150, spread: 70, origin: {{ y: 0.6 }}, colors: ['#C9A84C', '#E8C97A', '#FFFFFF'] }});
            }}
        }}, 6100);
    }});
    </script>
    """
    components.html(wheel_html, height=450)

st.markdown('<div style="text-align:center; font-size:0.5rem; color:rgba(255,255,255,0.3); margin-top:5px; letter-spacing: 1px;">SKYLUXE RESIDENCES</div>', unsafe_allow_html=True)
