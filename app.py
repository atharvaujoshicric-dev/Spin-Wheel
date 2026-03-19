import streamlit as st
import streamlit.components.v1 as components
import base64
import json

st.set_page_config(page_title="Alpha Spin Wheel", layout="centered")

# Custom CSS for Streamlit UI
st.markdown("""
<style>
    .stApp {
        background-color: #fdfbf7;
    }
    .main {
        padding-top: 1rem;
    }
    div.block-container {
        padding-top: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to encode image to base64
def get_image_base64(path):
    with open(path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()

try:
    wheel_base64 = get_image_base64("wheel.png")
except:
    try:
        wheel_base64 = get_image_base64("IMG_1769.jpg")
    except:
        st.error("Wheel image not found! Please ensure wheel.png is in the directory.")
        st.stop()

# Fixed prizes based on the image provided
# Note: These must match the visual order in the image (starting from top, clockwise)
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

if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.header("🏆 Recent Winners")
    if st.session_state.history:
        for entry in reversed(st.session_state.history):
            st.write(f"🎉 **{entry}**")
    else:
        st.write("No winners yet!")
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.rerun()

st.markdown("<h1 style='text-align: center; color: #4A148C; font-family: serif; margin-bottom: 0;'>🎡 Premium Spin Wheel 🎡</h1>", unsafe_allow_html=True)

prizes_json = json.dumps(prizes)

wheel_html = f"""
<div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Arial Black', sans-serif;">
    
    <!-- Pointer -->
    <div id="pointer" style="
        width: 0; 
        height: 0; 
        border-left: 20px solid transparent; 
        border-right: 20px solid transparent; 
        border-top: 40px solid #FF8F00; 
        z-index: 100; 
        margin-bottom: -15px;
        filter: drop-shadow(0 4px 6px rgba(0,0,0,0.3));
    "></div>

    <div id="wheel-container" style="position: relative; width: 600px; height: 600px; border-radius: 50%; box-shadow: 0 15px 50px rgba(0,0,0,0.2);">
        <img id="wheel-img" src="data:image/png;base64,{wheel_base64}" style="width: 100%; height: 100%; transition: transform 6s cubic-bezier(0.1, 0, 0, 1); transform: rotate(0deg); border-radius: 50%;">
    </div>

    <button id="spin-button" style="
        margin-top: 30px; 
        padding: 18px 70px; 
        font-size: 24px; 
        font-weight: 900; 
        background: #4A148C; 
        color: #FFD700; 
        border: 4px solid #FF8F00; 
        border-radius: 50px; 
        cursor: pointer; 
        transition: 0.3s;
        box-shadow: 0 8px 20px rgba(0,0,0,0.25);
        letter-spacing: 2px;
        text-transform: uppercase;
    ">SPIN FOR PRIZE</button>
    
    <h2 id="winner-display" style="
        margin-top: 25px; 
        font-family: serif; 
        color: #4A148C; 
        height: 60px; 
        text-align: center;
        font-size: 32px;
        font-weight: bold;
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
    display.innerText = "Processing Your Luck...";
    btn.style.opacity = "0.7";
    
    // Add multiple full rotations (5-10) plus a random position
    const spins = (1800 + Math.floor(Math.random() * 360));
    currentRotation += spins;
    img.style.transform = `rotate(${{currentRotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        btn.style.opacity = "1";
        
        // Calculate winner
        // The wheel has 8 slices. Each is 45 degrees.
        // 0 degrees rotation = Apple iPad at the top (if it's the first slice)
        const actualDeg = (currentRotation % 360);
        
        // Winning calculation: (Pointer position - current rotation) / slice angle
        // Pointer is at the top (270 degrees in image space)
        const numSlices = 8;
        const sliceDeg = 360 / numSlices;
        const winningIndex = Math.floor(((270 - (actualDeg % 360) + 360) % 360) / sliceDeg);
        
        const winner = prizes[winningIndex];
        display.innerText = "🎉 " + winner.label + " 🎉";
        
        if (!winner.label.includes("BETTER LUCK")) {{
            confetti({{
                particleCount: 250,
                spread: 120,
                origin: {{ y: 0.6 }},
                colors: ['#4A148C', '#FF8F00', '#FFD700', '#FFFFFF']
            }});
        }}
    }}, 6100);
}});
</script>
"""

components.html(wheel_html, height=850)
