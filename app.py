import streamlit as st
import streamlit.components.v1 as components
import json

# Prize data with vibrant jewel-tone colors — each slice is distinct
prizes = [
    {"label": "AIRPODS APPLE",   "img": "🎧", "color": "#E63946", "text": "#ffffff"},  # Crimson Red
    {"label": "BETTER LUCK",     "img": "🍀", "color": "#2EC4B6", "text": "#ffffff"},  # Teal
    {"label": "SPIN AGAIN",      "img": "🔄", "color": "#FF9F1C", "text": "#000000"},  # Amber
    {"label": "IPAD APPLE",      "img": "📱", "color": "#6A4C93", "text": "#ffffff"},  # Violet
    {"label": "REFRIGERATOR",    "img": "🧊", "color": "#1982C4", "text": "#ffffff"},  # Sapphire Blue
    {"label": "AIR CONDITIONER", "img": "❄️", "color": "#8AC926", "text": "#000000"},  # Lime Green
    {"label": "BETTER LUCK",     "img": "✨", "color": "#FF595E", "text": "#ffffff"},  # Coral
]

st.set_page_config(page_title="Premium Rewards", layout="centered")

st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background-color: #0d0d0d;}
    </style>
""", unsafe_allow_html=True)

wheel_html = f"""
<div id="app-container" style="
    background: radial-gradient(circle at 50% 30%, #1a1a2e 0%, #0d0d0d 100%);
    padding: 40px 20px; border-radius: 24px; display: flex; flex-direction: column;
    align-items: center; box-shadow: 0 30px 80px rgba(0,0,0,0.7);
    font-family: 'Segoe UI', sans-serif;
">

    <!-- Pointer -->
    <div style="
        position: relative; z-index: 10;
        width: 0; height: 0;
        border-left: 16px solid transparent;
        border-right: 16px solid transparent;
        border-top: 36px solid #ff2d55;
        filter: drop-shadow(0 4px 8px rgba(255,45,85,0.7));
        margin-bottom: -14px;
    "></div>

    <!-- Wheel ring -->
    <div style="
        padding: 12px;
        background: conic-gradient(#d4af37, #f7e681, #d4af37, #8a6d3b, #d4af37);
        border-radius: 50%;
        box-shadow: 0 0 40px rgba(212,175,55,0.4), inset 0 0 15px rgba(0,0,0,0.6);
    ">
        <canvas id="wheel" width="460" height="460" style="border-radius: 50%; display: block;"></canvas>
    </div>

    <!-- Spin button -->
    <button id="spin-btn" onclick="spinWheel()" style="
        margin-top: 36px; padding: 14px 56px; font-size: 22px; font-weight: 800;
        text-transform: uppercase; letter-spacing: 3px;
        background: linear-gradient(135deg, #d4af37 0%, #f7e681 50%, #d4af37 100%);
        border: none; border-radius: 50px; cursor: pointer; color: #0d0d0d;
        box-shadow: 0 8px 25px rgba(212,175,55,0.5);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    "
    onmouseover="this.style.transform='scale(1.05)'; this.style.boxShadow='0 12px 35px rgba(212,175,55,0.7)'"
    onmouseout="this.style.transform='scale(1)'; this.style.boxShadow='0 8px 25px rgba(212,175,55,0.5)'"
    >
        🎰 Spin to Win
    </button>

    <div id="status" style="
        color: #f7e681; font-size: 26px; font-weight: 700;
        margin-top: 28px; letter-spacing: 1px; min-height: 44px;
        text-shadow: 0 0 20px rgba(247,230,129,0.6);
        transition: opacity 0.3s;
    "></div>
</div>

<script>
const prizes = {json.dumps(prizes)};
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');

const CX = 230, CY = 230, R = 228;
const sliceAngle = (2 * Math.PI) / prizes.length;

let currentRotation = 0;
let spinning = false;

// Pre-compute border colors (slightly lighter/darker variant per slice)
function lighten(hex, pct) {{
    let n = parseInt(hex.slice(1), 16);
    let r = Math.min(255, (n >> 16) + pct);
    let g = Math.min(255, ((n >> 8) & 0xff) + pct);
    let b = Math.min(255, (n & 0xff) + pct);
    return `rgb(${{r}},${{g}},${{b}})`;
}}

function drawWheel() {{
    ctx.clearRect(0, 0, 460, 460);

    // Draw slices — flat color, no per-frame gradients
    prizes.forEach((p, i) => {{
        const startA = i * sliceAngle + currentRotation;
        const endA   = startA + sliceAngle;

        ctx.beginPath();
        ctx.moveTo(CX, CY);
        ctx.arc(CX, CY, R, startA, endA);
        ctx.closePath();
        ctx.fillStyle = p.color;
        ctx.fill();

        // Thin separator line
        ctx.strokeStyle = "rgba(0,0,0,0.35)";
        ctx.lineWidth = 2;
        ctx.stroke();
    }});

    // Single radial vignette overlay (drawn once on top — cheap)
    const vignette = ctx.createRadialGradient(CX, CY, R * 0.55, CX, CY, R);
    vignette.addColorStop(0, "rgba(0,0,0,0)");
    vignette.addColorStop(1, "rgba(0,0,0,0.28)");
    ctx.beginPath();
    ctx.arc(CX, CY, R, 0, 2 * Math.PI);
    ctx.fillStyle = vignette;
    ctx.fill();

    // Labels
    prizes.forEach((p, i) => {{
        const midA = i * sliceAngle + currentRotation + sliceAngle / 2;
        ctx.save();
        ctx.translate(CX, CY);
        ctx.rotate(midA);

        // Icon
        ctx.font = "28px Arial";
        ctx.textAlign = "center";
        ctx.fillText(p.img, R - 32, 6);

        // Label
        ctx.font = "bold 15px Arial";
        ctx.fillStyle = p.text;
        ctx.shadowColor = "rgba(0,0,0,0.6)";
        ctx.shadowBlur = 4;
        ctx.textAlign = "right";
        ctx.fillText(p.label, R - 62, 6);
        ctx.shadowBlur = 0;
        ctx.restore();
    }});

    // Center hub
    const hubGrad = ctx.createRadialGradient(CX - 6, CY - 6, 2, CX, CY, 28);
    hubGrad.addColorStop(0, "#f7e681");
    hubGrad.addColorStop(1, "#8a6d3b");
    ctx.beginPath();
    ctx.arc(CX, CY, 28, 0, 2 * Math.PI);
    ctx.fillStyle = hubGrad;
    ctx.fill();
    ctx.strokeStyle = "#000";
    ctx.lineWidth = 2;
    ctx.stroke();
}}

function spinWheel() {{
    if (spinning) return;
    spinning = true;

    const btn = document.getElementById('spin-btn');
    const status = document.getElementById('status');
    btn.disabled = true;
    btn.style.opacity = "0.6";
    status.style.opacity = "0";
    status.innerText = "";

    // Random extra rotation (10–15 full spins) + random landing offset
    const extraSpins   = (10 + Math.random() * 5) * 2 * Math.PI;
    const landingOffset = Math.random() * 2 * Math.PI;
    const totalRotation = extraSpins + landingOffset;
    const duration      = 5500; // ms — shorter = snappier, less lag risk
    const startTime     = performance.now();
    const startRotation = currentRotation;

    function easeOut(t) {{
        // Quintic ease-out: smooth deceleration, no lag
        return 1 - Math.pow(1 - t, 5);
    }}

    function frame(now) {{
        const elapsed = now - startTime;
        const t       = Math.min(elapsed / duration, 1);
        currentRotation = startRotation + totalRotation * easeOut(t);
        drawWheel();

        if (t < 1) {{
            requestAnimationFrame(frame);
        }} else {{
            // Pointer is at top = 270° = 1.5π from canvas 0°
            const norm = ((currentRotation % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
            const pointerAngle = (1.5 * Math.PI - norm + 4 * Math.PI) % (2 * Math.PI);
            const idx = Math.floor(pointerAngle / sliceAngle) % prizes.length;
            status.innerText = "🏆 " + prizes[idx].label;
            status.style.opacity = "1";
            btn.disabled = false;
            btn.style.opacity = "1";
            spinning = false;
        }}
    }}

    requestAnimationFrame(frame);
}}

drawWheel();
</script>
"""

components.html(wheel_html, height=820)
