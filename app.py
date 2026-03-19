import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data with Emoji/Icon placeholders based on your design
prizes = [
    {"label": "AIRPODS APPLE", "icon": "🎧", "color": "#FF5F6D"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#FFC371"},
    {"label": "SPIN AGAIN", "icon": "🔄", "color": "#48c6ef"},
    {"label": "IPAD APPLE", "icon": "📱", "color": "#6f86d6"},
    {"label": "REFRIGERATOR", "icon": "❄️", "color": "#2af598"},
    {"label": "AIR CONDITIONER", "icon": "💨", "color": "#f093fb"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#f5576c"}
]

st.set_page_config(page_title="Wheel Of Fortune", layout="centered")

# Injecting clean UI style
st.markdown("<h1 style='text-align: center; color: #1E1E1E;'>🎡 Wheel Of Fortune</h1>", unsafe_allow_html=True)

# The updated HTML/JS with SVG Icons and Text Alignment
wheel_html = f"""
<div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center;">
    <div id="pointer" style="width: 0; height: 0; border-left: 20px solid transparent; border-right: 20px solid transparent; border-top: 30px solid #D32F2F; z-index: 100; margin-bottom: -15px;"></div>

    <div id="wheel-container" style="position: relative; width: 500px; height: 500px;">
        <svg id="wheel-svg" viewBox="0 0 500 500" style="width: 100%; height: 100%; transform: rotate(0deg); transition: transform 6s cubic-bezier(0.1, 0, 0, 1);">
            <g id="wheel-group"></g>
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 60px; height: 60px; background: white; border-radius: 50%; border: 4px solid #333; display: flex; align-items: center; justify-content: center; font-size: 24px;">🎁</div>
    </div>

    <button id="spin-button" style="margin-top: 40px; padding: 18px 60px; font-size: 22px; font-weight: bold; background: #1E1E1E; color: white; border: none; border-radius: 12px; cursor: pointer; transition: 0.3s;">SPIN FOR PRIZE</button>
    
    <h2 id="winner-display" style="margin-top: 20px; font-family: sans-serif; color: #D32F2F; height: 40px;"></h2>
</div>

<script>
const prizes = {json.dumps(prizes)};
const wheelGroup = document.getElementById('wheel-group');
const svg = document.getElementById('wheel-svg');
const btn = document.getElementById('spin-button');
const display = document.getElementById('winner-display');

const numSlices = prizes.length;
const sliceDeg = 360 / numSlices;

prizes.forEach((prize, i) => {{
    const startAngle = i * sliceDeg;
    const endAngle = (i + 1) * sliceDeg;
    const x1 = 250 + 250 * Math.cos(Math.PI * startAngle / 180);
    const y1 = 250 + 250 * Math.sin(Math.PI * startAngle / 180);
    const x2 = 250 + 250 * Math.cos(Math.PI * endAngle / 180);
    const y2 = 250 + 250 * Math.sin(Math.PI * endAngle / 180);
    
    const pathData = `M 250 250 L ${{x1}} ${{y1}} A 250 250 0 0 1 ${{x2}} ${{y2}} Z`;
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("fill", prize.color);
    path.setAttribute("stroke", "white");
    path.setAttribute("stroke-width", "2");
    wheelGroup.appendChild(path);

    // Create container for text and icons to ensure center alignment
    const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
    g.setAttribute("transform", `rotate(${{startAngle + sliceDeg/2}}, 250, 250)`);
    
    // Prize Text
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "340"); 
    text.setAttribute("y", "255");
    text.setAttribute("fill", "white");
    text.setAttribute("font-weight", "bold");
    text.setAttribute("font-size", "14px");
    text.setAttribute("text-anchor", "middle");
    text.textContent = prize.label;
    g.appendChild(text);

    // Prize Icon (Placed further out)
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
    icon.setAttribute("x", "440");
    icon.setAttribute("y", "258");
    icon.setAttribute("font-size", "30px");
    icon.setAttribute("text-anchor", "middle");
    icon.textContent = prize.icon;
    g.appendChild(icon);

    wheelGroup.appendChild(g);
}});

let currentRotation = 0;

btn.addEventListener('click', () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    display.innerText = "Processing...";
    
    const spins = 1800 + Math.floor(Math.random() * 360);
    currentRotation += spins;
    svg.style.transform = `rotate(${{currentRotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        const actualDeg = (currentRotation % 360);
        const winningIndex = Math.floor(((270 - actualDeg + 360) % 360) / sliceDeg);
        display.innerText = "🎉 WINNER: " + prizes[winningIndex].label + " 🎉";
    }}, 6100);
}});
</script>
"""

components.html(wheel_html, height=750)
