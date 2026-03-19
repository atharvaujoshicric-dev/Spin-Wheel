import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data from your design document
prizes = [
    "AIRPODS APPLE",            # [cite: 1]
    "BETTER LUCK NEXT TIME",    # [cite: 2, 3]
    "SPIN AGAIN",               # [cite: 4, 5]
    "IPAD APPLE",               # [cite: 6]
    "DOUBLE DOOR REFRIGERATOR", # [cite: 7, 8, 10]
    "SPLIT AIR CONDITIONER",    # [cite: 9, 10]
    "BETTER LUCK NEXT TIME"     # [cite: 11, 12]
]

st.set_page_config(page_title="Premium Spin Wheel", layout="centered")

# Visual layout and CSS
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stTitle { color: white; text-align: center; font-family: 'Inter', sans-serif; }
    </style>
""", unsafe_allow_html=True)

st.title("🎡 Executive Prize Draw")

# Premium Wheel HTML/JS
wheel_html = f"""
<div id="wrapper" style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh;">
    <div id="pointer" style="
        width: 0; height: 0; 
        border-left: 20px solid transparent; 
        border-right: 20px solid transparent; 
        border-top: 30px solid #FF3E3E; 
        z-index: 100; margin-bottom: -15px;
        filter: drop-shadow(0 2px 4px rgba(0,0,0,0.5));
    "></div>

    <div id="wheel-container" style="position: relative; width: 500px; height: 500px;">
        <svg id="wheel-svg" viewBox="0 0 500 500" style="width: 100%; height: 100%; transform: rotate(0deg); transition: transform 5s cubic-bezier(0.1, 0, 0, 1); shadow: 0 10px 40px rgba(0,0,0,0.5);">
            <defs>
                <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">
                    <feGaussianBlur in="SourceAlpha" stdDeviation="3" />
                    <feOffset dx="2" dy="2" />
                    <feComponentTransfer><feFuncA type="linear" slope="0.5"/></feComponentTransfer>
                    <feMerge><feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge>
                </filter>
            </defs>
            <g id="wheel-group"></g>
        </svg>
        <circle cx="250" cy="250" r="25" fill="#222" stroke="#444" stroke-width="2" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%);" />
    </div>

    <button id="spin-button" style="
        margin-top: 40px; padding: 15px 50px; 
        font-size: 22px; font-weight: 800; letter-spacing: 1px;
        background: linear-gradient(135deg, #6e8efb, #a777e3); 
        color: white; border: none; border-radius: 50px; 
        cursor: pointer; box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        transition: 0.2s;
    ">SPIN NOW</button>
    
    <h2 id="winner-display" style="color: #00ffcc; font-family: sans-serif; margin-top: 20px; height: 30px; text-transform: uppercase;"></h2>
</div>

<script>
const prizes = {json.dumps(prizes)};
const colors = ["#FF5F6D", "#FFC371", "#48c6ef", "#6f86d6", "#2af598", "#f093fb", "#f5576c"];
const wheelGroup = document.getElementById('wheel-group');
const svg = document.getElementById('wheel-svg');
const btn = document.getElementById('spin-button');
const display = document.getElementById('winner-display');

const numSlices = prizes.length;
const sliceDeg = 360 / numSlices;

// Build segments with SVG
prizes.forEach((prize, i) => {{
    const startAngle = i * sliceDeg;
    const endAngle = (i + 1) * sliceDeg;
    const x1 = 250 + 250 * Math.cos(Math.PI * startAngle / 180);
    const y1 = 250 + 250 * Math.sin(Math.PI * startAngle / 180);
    const x2 = 250 + 250 * Math.cos(Math.PI * endAngle / 180);
    const y2 = 250 + 250 * Math.sin(Math.PI * endAngle / 180);
    
    const pathData = `M 250 250 L ${{x1}} ${{y1}} A 250 250 0 0 1 ${{x2}} ${{y2}} Z`;
    
    // Create segment
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("fill", colors[i % colors.length]);
    path.setAttribute("stroke", "#fff");
    path.setAttribute("stroke-width", "1");
    wheelGroup.appendChild(path);

    // Create Text path
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    text.setAttribute("x", "380");
    text.setAttribute("y", "255");
    text.setAttribute("fill", "white");
    text.setAttribute("font-weight", "bold");
    text.setAttribute("font-family", "Arial");
    text.setAttribute("font-size", "14px");
    text.setAttribute("transform", `rotate(${{startAngle + sliceDeg/2}}, 250, 250)`);
    text.textContent = prize;
    wheelGroup.appendChild(text);
}});

let currentRotation = 0;

btn.addEventListener('click', () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    display.innerText = "SPINNING...";
    
    const spins = 1440 + Math.floor(Math.random() * 360);
    currentRotation += spins;
    svg.style.transform = `rotate(${{currentRotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        
        // Calculation for 12 o'clock pointer:
        // Adjust for initial orientation and calculate index
        const actualDeg = (currentRotation % 360);
        // We subtract the degree from 270 because 0 degrees in CSS/SVG is 3 o'clock.
        // The pointer is at 12 o'clock (270 deg).
        const winningIndex = Math.floor(((270 - actualDeg + 360) % 360) / sliceDeg);
        
        display.innerText = "⭐ WINNER: " + prizes[winningIndex] + " ⭐";
    }}, 5000);
}});
</script>
"""

components.html(wheel_html, height=750)
