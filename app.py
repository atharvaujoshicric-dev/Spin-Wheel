import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data from your design
prizes = [
    {"label": "Apple Airpods", "icon": "🎧", "color": "#FF5F6D"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#FFC371"},
    {"label": "SPIN AGAIN", "icon": "🔄", "color": "#48c6ef"},
    {"label": "APPLE IPAD", "icon": "📱", "color": "#6f86d6"},
    {"label": "REFRIGERATOR", "icon": "❄️", "color": "#2af598"},
    {"label": "Split AC", "icon": "💨", "color": "#f093fb"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#f5576c"}
]

st.set_page_config(page_title="Premium Spin Wheel", layout="centered")

wheel_html = f"""
<div id="wrapper" style="display: flex; flex-direction: column; align-items: center; background: #f0f2f6; padding: 40px; border-radius: 20px;">
    
    <div id="pointer" style="
        width: 0; height: 0; 
        border-left: 20px solid transparent; 
        border-right: 20px solid transparent; 
        border-top: 35px solid #d00000; 
        z-index: 100; margin-bottom: -15px;
        filter: drop-shadow(0 4px 4px rgba(0,0,0,0.2));
    "></div>

    <div id="wheel-container" style="position: relative; width: 500px; height: 500px; border: 12px solid #333; border-radius: 50%; box-shadow: 0 15px 35px rgba(0,0,0,0.2);">
        <svg id="wheel-svg" viewBox="0 0 500 500" style="width: 100%; height: 100%; transition: transform 7s cubic-bezier(0.1, 0, 0, 1);">
            <g id="wheel-group"></g>
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 70px; height: 70px; background: white; border-radius: 50%; border: 5px solid #333; display: flex; align-items: center; justify-content: center; font-size: 28px; box-shadow: 0 4px 10px rgba(0,0,0,0.3);">🎁</div>
    </div>

    <button id="spin-btn" style="
        margin-top: 40px; padding: 18px 70px; 
        font-size: 24px; font-weight: 800; 
        background: linear-gradient(135deg, #1e1e1e, #444); 
        color: white; border: none; border-radius: 50px; 
        cursor: pointer; box-shadow: 0 8px 15px rgba(0,0,0,0.2);
        transition: 0.3s;
    ">SPIN NOW</button>
    
    <h2 id="winner-text" style="margin-top: 25px; font-family: sans-serif; color: #333; height: 40px; letter-spacing: 1px;"></h2>
</div>

<script>
const prizes = {json.dumps(prizes)};
const wheelGroup = document.getElementById('wheel-group');
const svg = document.getElementById('wheel-svg');
const btn = document.getElementById('spin-btn');
const winnerDisplay = document.getElementById('winner-text');

const numSlices = prizes.length;
const sliceDeg = 360 / numSlices;

prizes.forEach((p, i) => {{
    const startAngle = i * sliceDeg;
    const endAngle = (i + 1) * sliceDeg;
    const rad = 250;
    
    // 1. Draw Slice
    const x1 = 250 + rad * Math.cos(Math.PI * startAngle / 180);
    const y1 = 250 + rad * Math.sin(Math.PI * startAngle / 180);
    const x2 = 250 + rad * Math.cos(Math.PI * endAngle / 180);
    const y2 = 250 + rad * Math.sin(Math.PI * endAngle / 180);
    const pathData = `M 250 250 L ${{x1}} ${{y1}} A 250 250 0 0 1 ${{x2}} ${{y2}} Z`;
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("fill", p.color);
    path.setAttribute("stroke", "#fff");
    path.setAttribute("stroke-width", "2");
    wheelGroup.appendChild(path);

    // 2. Create Curved Text Path (Proper Wrapping)
    const textPathId = 'tpath' + i;
    const tPath = document.createElementNS("http://www.w3.org/2000/svg", "path");
    // Define an invisible arc for text to sit on (radius 190)
    const tx1 = 250 + 190 * Math.cos(Math.PI * startAngle / 180);
    const ty1 = 250 + 190 * Math.sin(Math.PI * startAngle / 180);
    const tx2 = 250 + 190 * Math.cos(Math.PI * endAngle / 180);
    const ty2 = 250 + 190 * Math.sin(Math.PI * endAngle / 180);
    tPath.setAttribute("id", textPathId);
    tPath.setAttribute("d", `M ${{tx1}} ${{ty1}} A 190 190 0 0 1 ${{tx2}} ${{ty2}}`);
    tPath.setAttribute("fill", "none");
    wheelGroup.appendChild(tPath);

    // 3. Add Text and Icon
    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const tPathElement = document.createElementNS("http://www.w3.org/2000/svg", "textPath");
    tPathElement.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", "#" + textPathId);
    tPathElement.setAttribute("startOffset", "50%");
    tPathElement.setAttribute("text-anchor", "middle");
    tPathElement.setAttribute("fill", "white");
    tPathElement.style.fontSize = "14px";
    tPathElement.style.fontWeight = "bold";
    tPathElement.textContent = p.icon + " " + p.label;
    
    text.appendChild(tPathElement);
    wheelGroup.appendChild(text);
}});

let rotation = 0;

btn.addEventListener('click', () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    winnerDisplay.innerText = "Processing Your Fortune...";
    
    // Calculate a massive spin (10-15 rotations) + random landing
    const extraSpins = 3600 + Math.floor(Math.random() * 360);
    rotation += extraSpins;
    
    // GPU Accelerated Animation
    svg.style.transform = `rotate(${{rotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        const actualDeg = rotation % 360;
        // Logic to find winner at the 12 o'clock position (270 degrees)
        const winningIndex = Math.floor(((270 - actualDeg + 360) % 360) / sliceDeg);
        winnerDisplay.innerText = "🏆 WINNER: " + prizes[winningIndex].label + " 🏆";
    }}, 7100);
}});
</script>
"""

components.html(wheel_html, height=800)
