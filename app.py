import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data from your design
prizes = [
    {"label": "AIRPODS APPLE", "icon": "🎧", "color": "#2c3e50"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#e74c3c"},
    {"label": "SPIN AGAIN", "icon": "🔄", "color": "#3498db"},
    {"label": "IPAD APPLE", "icon": "📱", "color": "#8e44ad"},
    {"label": "REFRIGERATOR", "icon": "❄️", "color": "#27ae60"},
    {"label": "AIR CONDITIONER", "icon": "💨", "color": "#16a085"},
    {"label": "BETTER LUCK", "icon": "❌", "color": "#f39c12"}
]

st.set_page_config(page_title="Premium Spin Wheel", layout="centered")

wheel_html = f"""
<div id="container" style="display: flex; flex-direction: column; align-items: center; font-family: 'Segoe UI', sans-serif; background: #111; padding: 50px; border-radius: 30px;">
    
    <div id="pointer" style="
        width: 0; height: 0; 
        border-left: 20px solid transparent; 
        border-right: 20px solid transparent; 
        border-top: 40px solid #ffffff; 
        z-index: 100; margin-bottom: -10px;
        filter: drop-shadow(0 0 10px rgba(255,255,255,0.5));
    "></div>

    <div id="wheel-wrapper" style="position: relative; width: 500px; height: 500px; border: 15px solid #222; border-radius: 50%; box-shadow: 0 0 50px rgba(0,0,0,0.8);">
        <svg id="wheel-svg" viewBox="0 0 500 500" style="width: 100%; height: 100%; transition: transform 8s cubic-bezier(0.2, 0, 0.1, 1);">
            <g id="slices"></g>
        </svg>
        <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 80px; height: 80px; background: #222; border: 4px solid #fff; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 30px; box-shadow: 0 0 20px rgba(0,0,0,0.5);">🎁</div>
    </div>

    <button id="spin-btn" style="
        margin-top: 40px; padding: 15px 60px; font-size: 22px; font-weight: bold;
        background: white; color: black; border: none; border-radius: 50px;
        cursor: pointer; box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        transition: 0.3s; text-transform: uppercase; letter-spacing: 2px;
    ">Launch Spin</button>

    <div id="winner-msg" style="margin-top: 30px; color: #fff; font-size: 28px; font-weight: bold; height: 40px; text-shadow: 0 0 10px rgba(255,255,255,0.3);"></div>
</div>

<script>
const prizes = {json.dumps(prizes)};
const slicesGroup = document.getElementById('slices');
const svg = document.getElementById('wheel-svg');
const btn = document.getElementById('spin-btn');
const msg = document.getElementById('winner-msg');

const totalSlices = prizes.length;
const arc = 360 / totalSlices;

prizes.forEach((p, i) => {{
    const startDeg = i * arc;
    const endDeg = (i + 1) * arc;
    const rad = 250;
    
    // Create Slice Path
    const x1 = 250 + rad * Math.cos(Math.PI * startDeg / 180);
    const y1 = 250 + rad * Math.sin(Math.PI * startDeg / 180);
    const x2 = 250 + rad * Math.cos(Math.PI * endDeg / 180);
    const y2 = 250 + rad * Math.sin(Math.PI * endDeg / 180);
    
    const pathData = `M 250 250 L ${{x1}} ${{y1}} A 250 250 0 0 1 ${{x2}} ${{y2}} Z`;
    
    const path = document.createElementNS("http://www.w3.org/2000/svg", "path");
    path.setAttribute("d", pathData);
    path.setAttribute("fill", p.color);
    path.setAttribute("stroke", "#111");
    path.setAttribute("stroke-width", "2");
    slicesGroup.appendChild(path);

    // Create Curved Text Path
    const textPathId = "path" + i;
    const textArc = document.createElementNS("http://www.w3.org/2000/svg", "path");
    // This arc is slightly inside the wheel for the text to sit on
    const tx1 = 250 + 180 * Math.cos(Math.PI * startDeg / 180);
    const ty1 = 250 + 180 * Math.sin(Math.PI * startDeg / 180);
    const tx2 = 250 + 180 * Math.cos(Math.PI * endDeg / 180);
    const ty2 = 250 + 180 * Math.sin(Math.PI * endDeg / 180);
    
    textArc.setAttribute("id", textPathId);
    textArc.setAttribute("d", `M ${{tx1}} ${{ty1}} A 180 180 0 0 1 ${{tx2}} ${{ty2}}`);
    textArc.setAttribute("fill", "none");
    slicesGroup.appendChild(textArc);

    const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
    const tp = document.createElementNS("http://www.w3.org/2000/svg", "textPath");
    tp.setAttributeNS("http://www.w3.org/1999/xlink", "xlink:href", "#" + textPathId);
    tp.setAttribute("startOffset", "50%");
    tp.setAttribute("text-anchor", "middle");
    tp.setAttribute("fill", "white");
    tp.style.fontSize = "16px";
    tp.style.fontWeight = "bold";
    tp.textContent = p.icon + " " + p.label;
    
    text.appendChild(tp);
    slicesGroup.appendChild(text);
}});

let rotation = 0;
btn.onclick = () => {{
    if(btn.disabled) return;
    btn.disabled = true;
    msg.innerText = "Processing Fortune...";
    
    // Add 5-10 full spins + random offset
    const extraSpins = 1800 + Math.floor(Math.random() * 360);
    rotation += extraSpins;
    
    svg.style.transform = `rotate(${{rotation}}deg)`;

    setTimeout(() => {{
        btn.disabled = false;
        const actualDeg = (rotation % 360);
        // Calculation: 270 is the top (12 o'clock)
        const winningIndex = Math.floor(((270 - actualDeg + 360) % 360) / arc);
        msg.innerText = "🏆 WINNER: " + prizes[winningIndex].label;
    }}, 8000);
}};
</script>
"""

components.html(wheel_html, height=850)
