import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data with high-end Jewel Tone colors
prizes = [
    {"label": "AIRPODS APPLE", "img": "🎧", "color": "#2E3192", "text": "#ffffff"}, # Royal Blue
    {"label": "BETTER LUCK", "img": "🍀", "color": "#1B1464", "text": "#ffffff"},   # Deep Navy
    {"label": "SPIN AGAIN", "img": "🔄", "color": "#00A99D", "text": "#ffffff"},   # Teal
    {"label": "IPAD APPLE", "img": "📱", "color": "#2E3192", "text": "#ffffff"}, 
    {"label": "REFRIGERATOR", "img": "🧊", "color": "#1B1464", "text": "#ffffff"},
    {"label": "AIR CONDITIONER", "img": "❄️", "color": "#00A99D", "text": "#ffffff"},
    {"label": "BETTER LUCK", "img": "✨", "color": "#2E3192", "text": "#ffffff"}
]

st.set_page_config(page_title="Premium Rewards", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #050505;}
    </style>
""", unsafe_allow_html=True)

wheel_html = f"""
<div id="app-container" style="background: radial-gradient(circle, #1a1a1a 0%, #000000 100%); padding: 40px; border-radius: 30px; display: flex; flex-direction: column; align-items: center; box-shadow: 0 20px 50px rgba(0,0,0,0.8); font-family: 'Segoe UI', sans-serif;">
    
    <div id="pointer" style="
        position: relative; z-index: 100;
        width: 0; height: 0; 
        border-left: 20px solid transparent; 
        border-right: 20px solid transparent; 
        border-top: 40px solid #FF3131; 
        filter: drop-shadow(0 5px 10px rgba(0,0,0,0.5));
        margin-bottom: -20px;
    "></div>

    <div style="padding: 15px; background: linear-gradient(145deg, #CFB53B, #8A7500); border-radius: 50%; box-shadow: 0 10px 40px rgba(0,0,0,0.7);">
        <div id="wheel-wrapper" style="width: 500px; height: 500px; position: relative; border-radius: 50%; overflow: hidden;">
            <svg id="wheel-svg" viewBox="0 0 500 500" style="width: 100%; height: 100%; transition: transform 7s cubic-bezier(0.15, 0, 0.15, 1); will-change: transform;">
                <g id="wheel-group"></g>
            </svg>
        </div>
    </div>

    <button id="spin-btn" style="
        margin-top: 40px; padding: 18px 70px; font-size: 22px; font-weight: 900;
        text-transform: uppercase; letter-spacing: 2px;
        background: linear-gradient(to right, #CFB53B, #F9E274);
        border: none; border-radius: 50px; cursor: pointer;
        color: #000; box-shadow: 0 10px 25px rgba(207,181,59,0.3);
        transition: all 0.3s ease;
    ">Spin to Win</button>

    <h1 id="status" style="color: #CFB53B; margin-top: 30px; letter-spacing: 1px; min-height: 60px; text-align: center;"></h1>
</div>

<script>
const prizes = {json.dumps(prizes)};
const wheelGroup = document.getElementById('wheel-group');
const svg = document.getElementById('wheel-svg');
const btn = document.getElementById('spin-btn');
const status = document.getElementById('status');

const numSlices = prizes.length;
const sliceDeg = 360 / numSlices;

// Use SVG for better text wrapping and resolution
prizes.forEach((p, i) => {{
    const startAngle = i * sliceDeg;
    const endAngle = (i + 1) * sliceDeg;
    
    // Draw Slice Path
    const x1 = 250 + 250 * Math.cos(Math.PI * startAngle / 180);
    const y1 = 250 + 250 * Math.sin(Math.PI * startAngle / 180);
    const x2 = 250 + 250 * Math.cos(Math.PI * endAngle / 180);
    const y2 = 250 + 250 * Math.sin(Math.PI * endAngle / 180);
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", `M 250 250 L ${{x1}} ${{y1}} A 250 250 0 0 1 ${{x2}} ${{y2}} Z`);
    path.setAttribute("fill", p.color);
    path.setAttribute("stroke", "rgba(255,255,255,0.1)");
    wheelGroup.appendChild(path);

    // Add Wrapped Text and Icon
    const textGroup = document.createElementNS("http://www.w3.org/2000/svg", "g");
    textGroup.setAttribute("transform", `rotate(${{startAngle + sliceDeg/2}}, 250, 250)`);
    
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "400");
    text.setAttribute("y", "255");
    text.setAttribute("fill", p.text);
    text.setAttribute("font-size", "14px");
    text.setAttribute("font-weight", "bold");
    text.setAttribute("text-anchor", "end");
    text.style.fontFamily = "Arial";
    
    // Split text into two lines if long
    const words = p.label.split(' ');
    if(words.length > 1) {{
        text.innerHTML = `<tspan x="380" dy="-8">${{words[0]}}</tspan><tspan x="380" dy="18">${{words.slice(1).join(' ')}}</tspan>`;
    }} else {{
        text.textContent = p.label;
    }}
    
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
    icon.setAttribute("x", "460");
    icon.setAttribute("y", "260");
    icon.setAttribute("font-size", "28px");
    icon.setAttribute("text-anchor", "middle");
    icon.textContent = p.img;

    textGroup.appendChild(text);
    textGroup.appendChild(icon);
    wheelGroup.appendChild(textGroup);
}});

let rotation = 0;

btn.onclick = () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    status.innerText = "⭐ REVEALING FORTUNE... ⭐";
    
    const spins = 10 + Math.floor(Math.random() * 5);
    const extraDegrees = Math.floor(Math.random() * 360);
    rotation += (spins * 360) + extraDegrees;
    
    // Trigger CSS hardware accelerated animation
    svg.style.transform = `rotate(${{rotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        const actualDeg = rotation % 360;
        // Logic for 12 o'clock position (270 degrees)
        const winningIndex = Math.floor(((270 - actualDeg + 360) % 360) / sliceDeg);
        status.innerHTML = "🏆 WINNER: " + prizes[winningIndex].label + " 🏆";
    }}, 7100);
}};
</script>
"""

components.html(wheel_html, height=850)
