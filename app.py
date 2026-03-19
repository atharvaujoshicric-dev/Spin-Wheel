import streamlit as st
import streamlit.components.v1 as components
import json

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

st.set_page_config(page_title="SKULUXE — Wheel of Fortune", layout="centered")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:ital,wght@0,300;0,600;1,300&display=swap');
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stApp {background: #000000;}

    .skuluxe-header {
        text-align: center;
        padding: 36px 0 8px 0;
        letter-spacing: 0.22em;
    }
    .skuluxe-title {
        font-family: 'Playfair Display', serif;
        font-size: 52px;
        font-weight: 900;
        color: #C9A84C;
        line-height: 1;
        text-shadow: 0 0 40px rgba(201,168,76,0.3);
        margin: 0;
    }
    .skuluxe-sub {
        font-family: 'Cormorant Garamond', serif;
        font-size: 18px;
        font-weight: 300;
        font-style: italic;
        color: #8E8E93;
        letter-spacing: 0.35em;
        margin-top: 6px;
        text-transform: uppercase;
    }
    .skuluxe-divider {
        width: 120px;
        height: 1px;
        background: linear-gradient(to right, transparent, #C9A84C, transparent);
        margin: 14px auto 0 auto;
    }
    </style>

    <div class="skuluxe-header">
        <div class="skuluxe-title">SKULUXE</div>
        <div class="skuluxe-sub">Wheel of Fortune</div>
        <div class="skuluxe-divider"></div>
    </div>
""", unsafe_allow_html=True)

wheel_html = f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Cormorant+Garamond:ital,wght@0,300;1,300&display=swap');

* {{ box-sizing: border-box; margin: 0; padding: 0; }}

#app-container {{
    background: radial-gradient(ellipse at 50% 0%, #1a1208 0%, #000000 65%);
    padding: 40px 20px 50px;
    border-radius: 24px;
    display: flex;
    flex-direction: column;
    align-items: center;
    border: 1px solid #2a2007;
}}

#pointer-wrap {{
    position: relative;
    z-index: 10;
    margin-bottom: -18px;
    filter: drop-shadow(0 6px 18px rgba(201,168,76,0.5));
}}
#pointer-wrap svg {{ display: block; }}

#wheel-ring {{
    padding: 12px;
    background: conic-gradient(#C9A84C 0deg, #8a6520 90deg, #C9A84C 180deg, #8a6520 270deg, #C9A84C 360deg);
    border-radius: 50%;
    box-shadow:
        0 0 0 2px #3a2800,
        0 10px 50px rgba(0,0,0,0.9),
        0 0 60px rgba(201,168,76,0.08);
    will-change: transform;
}}

canvas {{
    border-radius: 50%;
    display: block;
    will-change: transform;
}}

#spin-btn {{
    margin-top: 44px;
    padding: 16px 64px;
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    background: linear-gradient(135deg, #C9A84C 0%, #f0d880 50%, #C9A84C 100%);
    border: none;
    border-radius: 60px;
    cursor: pointer;
    color: #000;
    box-shadow: 0 8px 30px rgba(201,168,76,0.35), inset 0 1px 0 rgba(255,255,255,0.3);
    transition: transform 0.15s ease, box-shadow 0.15s ease, opacity 0.15s ease;
}}
#spin-btn:hover:not(:disabled) {{
    transform: translateY(-2px);
    box-shadow: 0 14px 40px rgba(201,168,76,0.5), inset 0 1px 0 rgba(255,255,255,0.3);
}}
#spin-btn:disabled {{
    opacity: 0.5;
    cursor: not-allowed;
    transform: none;
}}

#status {{
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: #C9A84C;
    letter-spacing: 0.08em;
    margin-top: 32px;
    min-height: 40px;
    text-align: center;
    text-shadow: 0 0 30px rgba(201,168,76,0.4);
    transition: opacity 0.3s ease;
}}
</style>

<div id="app-container">
    <div id="pointer-wrap">
        <svg width="44" height="44" viewBox="0 0 44 44" fill="none" xmlns="http://www.w3.org/2000/svg">
            <polygon points="22,44 4,4 40,4" fill="#C9A84C"/>
            <polygon points="22,44 4,4 40,4" fill="url(#pg)" opacity="0.6"/>
            <defs>
                <linearGradient id="pg" x1="4" y1="4" x2="40" y2="44" gradientUnits="userSpaceOnUse">
                    <stop offset="0" stop-color="#fff" stop-opacity="0.5"/>
                    <stop offset="1" stop-color="#000" stop-opacity="0"/>
                </linearGradient>
            </defs>
        </svg>
    </div>

    <div id="wheel-ring">
        <canvas id="wheel" width="480" height="480"></canvas>
    </div>

    <button id="spin-btn">Spin to Win</button>
    <div id="status"></div>
</div>

<script>
const prizes = {json.dumps(prizes)};
const canvas = document.getElementById('wheel');
const ctx = canvas.getContext('2d');
const btn = document.getElementById('spin-btn');
const status = document.getElementById('status');

const W = 480, CX = 240, CY = 240, R = 238;
const N = prizes.length;
const sliceAngle = (2 * Math.PI) / N;

// Premium segment colors — alternating deep palettes (8 segments)
const segColors = [
    {{ bg: '#0D0D0D', rim: '#C9A84C' }},
    {{ bg: '#161610', rim: '#6B6B6B' }},
    {{ bg: '#0D0D0D', rim: '#C9A84C' }},
    {{ bg: '#161610', rim: '#6B6B6B' }},
    {{ bg: '#0D0D0D', rim: '#C9A84C' }},
    {{ bg: '#161610', rim: '#6B6B6B' }},
    {{ bg: '#0D0D0D', rim: '#C9A84C' }},
    {{ bg: '#161610', rim: '#6B6B6B' }},
];

let rotation = 0;
let animId = null;

function drawWheel(rot) {{
    ctx.clearRect(0, 0, W, W);

    for (let i = 0; i < N; i++) {{
        const startA = i * sliceAngle + rot;
        const endA = startA + sliceAngle;
        const mid = startA + sliceAngle / 2;
        const sc = segColors[i % segColors.length];
        const p = prizes[i];

        // Segment fill
        const grad = ctx.createRadialGradient(CX, CY, 20, CX, CY, R);
        grad.addColorStop(0, lighten(sc.bg, 0.12));
        grad.addColorStop(1, sc.bg);

        ctx.beginPath();
        ctx.moveTo(CX, CY);
        ctx.arc(CX, CY, R, startA, endA);
        ctx.closePath();
        ctx.fillStyle = grad;
        ctx.fill();

        // Rim line
        ctx.beginPath();
        ctx.moveTo(CX, CY);
        ctx.arc(CX, CY, R, startA, endA);
        ctx.closePath();
        ctx.strokeStyle = sc.rim;
        ctx.lineWidth = 1.5;
        ctx.stroke();

        // Label
        ctx.save();
        ctx.translate(CX, CY);
        ctx.rotate(mid);
        ctx.textAlign = 'right';
        ctx.shadowBlur = 8;
        ctx.shadowColor = 'rgba(0,0,0,0.8)';

        ctx.font = 'bold 15px "Arial Narrow", Arial, sans-serif';
        ctx.letterSpacing = '1px';
        ctx.fillStyle = p.text;
        ctx.fillText(p.label, R - 52, 5);

        ctx.font = '22px Arial';
        ctx.shadowBlur = 0;
        ctx.fillText(p.img, R - 16, 8);
        ctx.restore();
    }}

    // Radial dividers (subtle luxury lines from center)
    for (let i = 0; i < N; i++) {{
        const a = i * sliceAngle + rot;
        ctx.beginPath();
        ctx.moveTo(CX + Math.cos(a) * 34, CY + Math.sin(a) * 34);
        ctx.lineTo(CX + Math.cos(a) * R, CY + Math.sin(a) * R);
        ctx.strokeStyle = 'rgba(201,168,76,0.25)';
        ctx.lineWidth = 0.8;
        ctx.stroke();
    }}

    // Center jewel
    const cg = ctx.createRadialGradient(CX - 5, CY - 5, 2, CX, CY, 28);
    cg.addColorStop(0, '#f0d880');
    cg.addColorStop(0.5, '#C9A84C');
    cg.addColorStop(1, '#5c3d00');

    ctx.beginPath();
    ctx.arc(CX, CY, 28, 0, 2 * Math.PI);
    ctx.fillStyle = cg;
    ctx.fill();
    ctx.strokeStyle = '#2a1800';
    ctx.lineWidth = 2;
    ctx.stroke();

    // Inner ring on jewel
    ctx.beginPath();
    ctx.arc(CX, CY, 20, 0, 2 * Math.PI);
    ctx.strokeStyle = 'rgba(255,255,255,0.15)';
    ctx.lineWidth = 1;
    ctx.stroke();
}}

function lighten(hex, amt) {{
    const n = parseInt(hex.slice(1), 16);
    const r = Math.min(255, (n >> 16) + Math.round(amt * 255));
    const g = Math.min(255, ((n >> 8) & 0xff) + Math.round(amt * 255));
    const b = Math.min(255, (n & 0xff) + Math.round(amt * 255));
    return `rgb(${{r}},${{g}},${{b}})`;
}}

// Smooth easing — no lag, uses requestAnimationFrame properly
function easeOutQuart(t) {{
    return 1 - Math.pow(1 - t, 4);
}}

btn.addEventListener('click', () => {{
    if (btn.disabled) return;
    btn.disabled = true;
    status.textContent = '';

    // 1. Pre-pick the winner
    const winnerIdx = Math.floor(Math.random() * N);

    // 2. The pointer sits at the TOP of the canvas = -π/2 in canvas coords.
    //    Segment i occupies [i*sliceAngle, (i+1)*sliceAngle] + rotation.
    //    We want the midpoint of segment winnerIdx to sit at -π/2.
    //    So we need:  winnerIdx*sliceAngle + sliceAngle/2 + targetRot = -π/2  (mod 2π)
    //    => targetRot = -π/2 - winnerIdx*sliceAngle - sliceAngle/2
    const targetRot = -Math.PI / 2 - (winnerIdx * sliceAngle + sliceAngle / 2);

    // 3. Bring targetRot to same mod-2π neighbourhood as current rotation,
    //    then add at least 6 full extra spins so it always looks dramatic.
    const currentMod = rotation % (2 * Math.PI);
    let targetMod = ((targetRot % (2 * Math.PI)) + 2 * Math.PI) % (2 * Math.PI);
    // How far to spin from current mod position to target mod (always forward)
    let delta = targetMod - currentMod;
    if (delta <= 0) delta += 2 * Math.PI;          // always spin forward
    const extraSpins = (6 + Math.floor(Math.random() * 3)) * 2 * Math.PI;
    const totalSpin = extraSpins + delta;

    const duration = 6500;
    const startRot = rotation;
    let startTime = null;

    function frame(ts) {{
        if (!startTime) startTime = ts;
        const elapsed = ts - startTime;
        const t = Math.min(elapsed / duration, 1);
        rotation = startRot + totalSpin * easeOutQuart(t);
        drawWheel(rotation);

        if (t < 1) {{
            animId = requestAnimationFrame(frame);
        }} else {{
            btn.disabled = false;
            // Winner was pre-determined — display directly, no recalculation
            status.textContent = '🏆 ' + prizes[winnerIdx].label;
        }}
    }}

    if (animId) cancelAnimationFrame(animId);
    animId = requestAnimationFrame(frame);
}});

drawWheel(rotation);
</script>
"""

components.html(wheel_html, height=900)
