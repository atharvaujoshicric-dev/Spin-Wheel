import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data with refined labels and premium colors
prizes = [
    {"label": "AIRPODS APPLE", "img": "🎧", "color": "#1a1a1b", "text": "#ffffff"}, # Sleek Black
    {"label": "BETTER LUCK", "img": "🍀", "color": "#d4af37", "text": "#000000"},   # Metallic Gold
    {"label": "SPIN AGAIN", "img": "🔄", "color": "#e5e5e5", "text": "#000000"},   # Silver
    {"label": "IPAD APPLE", "img": "📱", "color": "#1a1a1b", "text": "#ffffff"}, 
    {"label": "REFRIGERATOR", "img": "🧊", "color": "#d4af37", "text": "#000000"},
    {"label": "AIR CONDITIONER", "img": "❄️", "color": "#e5e5e5", "text": "#000000"},
    {"label": "BETTER LUCK", "img": "✨", "color": "#1a1a1b", "text": "#ffffff"}
]

st.set_page_config(page_title="Premium Rewards", layout="centered")

# Hide Streamlit header/footer for a standalone "App" feel
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #000000;}
    </style>
""", unsafe_allow_html=True)

wheel_html = f"""
<div id="app-container" style="background: radial-gradient(circle, #2c3e50 0%, #000000 100%); padding: 40px; border-radius: 20px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 20px 50px rgba(0,0,0,0.5);">
    
    <div id="pointer" style="
        position: relative; z-index: 10;
        width: 40px; height: 40px; 
        background: #ff0000; clip-path: polygon(50% 100%, 0 0, 100% 0);
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.5));
        margin-bottom: -15px;
    "></div>

    <div id="wheel-case" style="
        padding: 15px; background: linear-gradient(145deg, #d4af37, #8a6d3b); 
        border-radius: 50%; box-shadow: inset 0 0 20px rgba(0,0,0,0.8), 0 10px 30px rgba(0,0,0,0.6);
    ">
        <canvas id="wheel" width="500" height="500" style="border-radius: 50%;"></canvas>
    </div>

    <button id="spin-btn" style="
        margin-top: 40px; padding: 15px 60px; font-size: 24px; font-weight: 900;
        text-transform: uppercase; letter-spacing: 2px;
        background: linear-gradient(to right, #d4af37, #f7e681);
        border: none; border-radius: 50px; cursor: pointer;
        color: #000; box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        transition: all 0.2s ease;
    ">Spin to Win</button>

    <h1 id="status" style="color: #d4af37; font-family: 'Georgia', serif; margin-top: 30px; letter-spacing: 1px; min-height: 50px;"></h1>
</div>

<script>
const prizes = {json.dumps(prizes)};
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const btn = document.getElementById('spin-btn');
const status = document.getElementById('status');

const centerX = 250;
const centerY = 250;
const radius = 250;
const sliceAngle = (2 * Math.PI) / prizes.length;

let currentRotation = 0;

function drawWheel() {{
    ctx.clearRect(0,0,500,500);
    
    prizes.forEach((p, i) => {{
        const angle = i * sliceAngle + currentRotation;
        
        // Draw Slice with Gradient for 3D look
        const grad = ctx.createRadialGradient(centerX, centerY, 50, centerX, centerY, radius);
        grad.addColorStop(0, p.color);
        grad.addColorStop(1, "#000000"); // Dark edge for depth
        
        ctx.beginPath();
        ctx.fillStyle = grad;
        ctx.moveTo(centerX, centerY);
        ctx.arc(centerX, centerY, radius, angle, angle + sliceAngle);
        ctx.fill();
        ctx.strokeStyle = "#444";
        ctx.stroke();

        // Draw Text (Curved effect)
        ctx.save();
        ctx.translate(centerX, centerY);
        ctx.rotate(angle + sliceAngle / 2);
        ctx.textAlign = "right";
        ctx.fillStyle = p.text;
        ctx.font = "bold 18px Arial";
        ctx.shadowBlur = 5;
        ctx.shadowColor = "rgba(0,0,0,0.5)";
        ctx.fillText(p.label, radius - 60, 10);
        
        // Draw Icon
        ctx.font = "30px Arial";
        ctx.fillText(p.img, radius - 20, 12);
        ctx.restore();
    }});

    // Center Hub
    ctx.beginPath();
    ctx.arc(centerX, centerY, 30, 0, 2*Math.PI);
    ctx.fillStyle = "#d4af37";
    ctx.fill();
    ctx.stroke();
}}

btn.onclick = () => {{
    if(btn.style.opacity == "0.5") return;
    btn.style.opacity = "0.5";
    status.innerText = "GOOD LUCK...";
    
    const spins = 10 + Math.random() * 5;
    const totalRotation = spins * 2 * Math.PI;
    const duration = 7000; // 7 seconds for a "heavy" feel
    const start = performance.now();
    const initialRotation = currentRotation;

    function animate(now) {{
        const elapsed = now - start;
        const t = Math.min(elapsed / duration, 1);
        
        // Custom Easing: Cubic-Bezier Slow Start, Very Slow Stop
        const easeOut = 1 - Math.pow(1 - t, 4);
        
        currentRotation = initialRotation + (totalRotation * easeOut);
        drawWheel();

        if (t < 1) {{
            requestAnimationFrame(animate);
        }} else {{
            btn.style.opacity = "1";
            const normalized = (currentRotation % (2 * Math.PI));
            // Pointer at top (1.5 * PI)
            const winningIndex = Math.floor(((1.5 * Math.PI - normalized + (8 * Math.PI)) % (2 * Math.PI)) / sliceAngle);
            status.innerHTML = "🏆 " + prizes[winningIndex].label;
        }}
    }}
    requestAnimationFrame(animate);
}};

drawWheel();
</script>
"""

components.html(wheel_html, height=850)
