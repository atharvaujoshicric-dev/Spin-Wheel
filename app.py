import streamlit as st
import math
import random
import time

st.set_page_config(page_title=“Lucky Spin Wheel”, layout=“centered”, page_icon=“🎡”)

# ── CSS ──────────────────────────────────────────────────────────────────────

st.markdown(”””

<style>
@import url('https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@700;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 60% 20%, #2d0057 0%, #1a0033 60%, #0d0020 100%);
    min-height: 100vh;
}

[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 60% 20%, #2d0057 0%, #1a0033 60%, #0d0020 100%) !important;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }

/* Main title */
.spin-title {
    font-family: 'Bangers', cursive;
    font-size: 3.2rem;
    text-align: center;
    letter-spacing: 4px;
    color: #FFD700;
    text-shadow: 0 0 20px #ff8c00aa, 3px 3px 0 #a0522d;
    margin-bottom: 0.2rem;
    line-height: 1.1;
}
.spin-subtitle {
    font-family: 'Nunito', sans-serif;
    font-size: 1rem;
    text-align: center;
    color: #f5c97a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
    opacity: 0.85;
}

/* Wheel container */
.wheel-outer {
    display: flex;
    justify-content: center;
    align-items: center;
    margin: 0 auto 1.5rem auto;
    position: relative;
    width: 520px;
}

/* Canvas wrapper with marigold border effect */
.wheel-wrapper {
    position: relative;
    display: inline-block;
}
.wheel-wrapper::before {
    content: '';
    position: absolute;
    top: -14px; left: -14px;
    width: calc(100% + 28px);
    height: calc(100% + 28px);
    border-radius: 50%;
    background: repeating-conic-gradient(#FF8C00 0deg 7deg, #FFD700 7deg 14deg);
    z-index: 0;
    opacity: 0.9;
    filter: drop-shadow(0 0 10px #ff8c0066);
}
.wheel-wrapper::after {
    content: '';
    position: absolute;
    top: -6px; left: -6px;
    width: calc(100% + 12px);
    height: calc(100% + 12px);
    border-radius: 50%;
    background: #1a0033;
    z-index: 1;
}
#wheelCanvas {
    position: relative;
    z-index: 2;
    border-radius: 50%;
    display: block;
}

/* Pointer */
.pointer {
    position: absolute;
    top: -28px;
    left: 50%;
    transform: translateX(-50%);
    z-index: 10;
    width: 0;
    height: 0;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.6));
}

/* Result card */
.result-card {
    background: linear-gradient(135deg, #3d0070 0%, #6a00b8 50%, #3d0070 100%);
    border: 3px solid #FFD700;
    border-radius: 16px;
    padding: 1.2rem 2rem;
    text-align: center;
    margin: 1rem auto;
    max-width: 380px;
    box-shadow: 0 0 30px #FFD70055, inset 0 0 20px #00000044;
    animation: resultPop 0.5s cubic-bezier(0.34,1.56,0.64,1);
}
@keyframes resultPop {
    0%  { transform: scale(0.5); opacity: 0; }
    100%{ transform: scale(1);   opacity: 1; }
}
.result-label {
    font-family: 'Bangers', cursive;
    font-size: 1rem;
    color: #f5c97a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}
.result-prize {
    font-family: 'Bangers', cursive;
    font-size: 2.4rem;
    color: #FFD700;
    text-shadow: 2px 2px 0 #a0522d, 0 0 20px #FFD70088;
    letter-spacing: 2px;
    margin: 0;
}
.result-emoji {
    font-size: 2.5rem;
    margin-bottom: 0.3rem;
}

/* Spin button */
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #FFD700, #FF8C00) !important;
    color: #1a0033 !important;
    font-family: 'Bangers', cursive !important;
    font-size: 1.6rem !important;
    letter-spacing: 3px !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.6rem 3rem !important;
    box-shadow: 0 6px 20px #FF8C0066, 0 2px 0 #a0522d !important;
    transition: all 0.2s !important;
    text-transform: uppercase !important;
    width: 100% !important;
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.04) !important;
    box-shadow: 0 10px 30px #FFD70099 !important;
}
.stButton > button:active {
    transform: translateY(1px) scale(0.98) !important;
}

/* Stats / history */
.stats-row {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin-top: 1rem;
    flex-wrap: wrap;
}
.stat-chip {
    background: rgba(255,215,0,0.12);
    border: 1.5px solid rgba(255,215,0,0.35);
    border-radius: 20px;
    padding: 4px 14px;
    font-family: 'Nunito', sans-serif;
    font-size: 0.78rem;
    color: #f5c97a;
    letter-spacing: 1px;
}

/* Confetti canvas */
#confettiCanvas {
    position: fixed;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 9999;
}
</style>

“””, unsafe_allow_html=True)

# ── Wheel Data ─────────────────────────────────────────────────────────────

SEGMENTS = [
{“label”: “Apple iPad”,             “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “📱”, “prize”: True},
{“label”: “Better Luck\nNext Time”, “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “😢”, “prize”: False},
{“label”: “Spin Again”,             “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “🔄”, “prize”: False},
{“label”: “Double Door\nRefrigerator”,“color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “🧊”, “prize”: True},
{“label”: “Split Air\nConditioner”, “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “❄️”, “prize”: True},
{“label”: “Better Luck\nNext Time”, “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “😢”, “prize”: False},
{“label”: “Apple\nAirPods”,         “color”: “#3B0764”, “text_color”: “#FFFFFF”, “emoji”: “🎧”, “prize”: True},
{“label”: “Spin Again”,             “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “🔄”, “prize”: False},
]

N = len(SEGMENTS)
SLICE_DEG = 360 / N

# ── Session State ───────────────────────────────────────────────────────────

if “rotation” not in st.session_state:
st.session_state.rotation = 0.0
if “spinning” not in st.session_state:
st.session_state.spinning = False
if “result_idx” not in st.session_state:
st.session_state.result_idx = None
if “spin_count” not in st.session_state:
st.session_state.spin_count = 0
if “prize_count” not in st.session_state:
st.session_state.prize_count = 0

# ── Title ───────────────────────────────────────────────────────────────────

st.markdown(’<div class="spin-title">🎡 LUCKY SPIN WHEEL 🎡</div>’, unsafe_allow_html=True)
st.markdown(’<div class="spin-subtitle">Spin & Win Exciting Prizes</div>’, unsafe_allow_html=True)

# ── Canvas Wheel (drawn via JS) ─────────────────────────────────────────────

rotation_val = st.session_state.rotation

segments_js = str([
{
“label”: s[“label”].replace(”\n”, “\n”),
“color”: s[“color”],
“textColor”: s[“text_color”],
“emoji”: s[“emoji”],
}
for s in SEGMENTS
]).replace(”’”, ‘”’).replace(‘True’, ‘true’).replace(‘False’, ‘false’)

wheel_html = f”””

<div class="wheel-outer">
  <div class="wheel-wrapper" id="wheelWrapper">
    <!-- Pointer arrow -->
    <div class="pointer" id="pointer">
      <svg width="46" height="52" viewBox="0 0 46 52" fill="none">
        <polygon points="23,52 0,4 46,4" fill="#FFD700" stroke="#a0522d" stroke-width="2.5"/>
        <polygon points="23,42 8,10 38,10"  fill="#FF8C00"/>
      </svg>
    </div>
    <canvas id="wheelCanvas" width="460" height="460"></canvas>
  </div>
</div>
<canvas id="confettiCanvas"></canvas>

<script>
(function() {{
  const segments = {segments_js};
  const N = segments.length;
  const sliceDeg = 360 / N;
  const canvas = document.getElementById('wheelCanvas');
  const ctx = canvas.getContext('2d');
  const cx = canvas.width / 2, cy = canvas.height / 2, r = canvas.width / 2 - 8;
  let currentRotation = {rotation_val};

  function toRad(d) {{ return d * Math.PI / 180; }}

  function drawWheel(rot) {{
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < N; i++) {{
      const startAngle = toRad(rot + i * sliceDeg - 90);
      const endAngle   = toRad(rot + (i + 1) * sliceDeg - 90);
      const seg = segments[i];

      // Slice
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, r, startAngle, endAngle);
      ctx.closePath();
      ctx.fillStyle = seg.color;
      ctx.fill();
      ctx.strokeStyle = '#7c3aed';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Text
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(toRad(rot + i * sliceDeg + sliceDeg / 2 - 90));
      ctx.textAlign = 'right';
      ctx.fillStyle = seg.textColor;

      const lines = seg.label.split('\\n');
      const fontSize = lines.length > 1 ? 15 : 17;
      ctx.font = `900 ${{fontSize}}px 'Bangers', cursive`;

      const textR = r * 0.78;
      if (lines.length === 1) {{
        ctx.fillText(lines[0], textR, 5);
      }} else {{
        ctx.fillText(lines[0], textR, -fontSize * 0.6);
        ctx.fillText(lines[1], textR,  fontSize * 0.8);
      }}
      ctx.restore();
    }}

    // Outer ring decoration
    ctx.beginPath();
    ctx.arc(cx, cy, r + 2, 0, Math.PI * 2);
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 4;
    ctx.stroke();

    // Center circle
    ctx.beginPath();
    ctx.arc(cx, cy, 42, 0, Math.PI * 2);
    const grad = ctx.createRadialGradient(cx, cy, 5, cx, cy, 42);
    grad.addColorStop(0, '#fff');
    grad.addColorStop(0.4, '#f5e6c8');
    grad.addColorStop(1, '#d4a96a');
    ctx.fillStyle = grad;
    ctx.fill();
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 3;
    ctx.stroke();

    // S logo in center
    ctx.font = 'bold 36px serif';
    ctx.fillStyle = '#8B4513';
    ctx.textAlign = 'center';
    ctx.fillText('ꕥ', cx, cy + 12);
  }}

  // ── Spin animation ────────────────────────────────────────────────────────
  let animating = false;
  function spin(targetRot) {{
    if (animating) return;
    animating = true;
    const startRot  = currentRotation;
    const delta     = targetRot - startRot;
    const duration  = 4500;
    const startTime = performance.now();

    function easeOut(t) {{
      return 1 - Math.pow(1 - t, 4);
    }}

    function frame(now) {{
      const elapsed = now - startTime;
      const t = Math.min(elapsed / duration, 1);
      currentRotation = startRot + delta * easeOut(t);
      drawWheel(currentRotation);
      if (t < 1) {{
        requestAnimationFrame(frame);
      }} else {{
        currentRotation = targetRot % 360;
        drawWheel(currentRotation);
        animating = false;
        // Trigger confetti if prize
        const finalIdx = {st.session_state.result_idx if st.session_state.result_idx is not None else 'null'};
        if (finalIdx !== null && {str(SEGMENTS[st.session_state.result_idx]["prize"]).lower() if st.session_state.result_idx is not None else 'false'}) {{
          launchConfetti();
        }}
      }}
    }}
    requestAnimationFrame(frame);
  }}

  // Initial draw
  drawWheel(currentRotation);

  // If a target rotation is stored, animate
  const TARGET = {st.session_state.rotation};
  if (TARGET !== currentRotation) {{
    spin(TARGET);
  }}

  // ── Confetti ──────────────────────────────────────────────────────────────
  function launchConfetti() {{
    const cCanvas = document.getElementById('confettiCanvas');
    cCanvas.width = window.innerWidth;
    cCanvas.height = window.innerHeight;
    const cCtx = cCanvas.getContext('2d');
    const particles = [];
    const colors = ['#FFD700','#FF8C00','#7c3aed','#ffffff','#ff4f94','#00e5ff'];
    for (let i = 0; i < 180; i++) {{
      particles.push({{
        x: Math.random() * cCanvas.width,
        y: -20,
        vx: (Math.random() - 0.5) * 6,
        vy: Math.random() * 4 + 3,
        r: Math.random() * 8 + 4,
        color: colors[Math.floor(Math.random() * colors.length)],
        rot: Math.random() * 360,
        spin: (Math.random() - 0.5) * 8,
        shape: Math.random() > 0.5 ? 'rect' : 'circle'
      }});
    }}
    let frame2 = 0;
    function confettiLoop() {{
      cCtx.clearRect(0, 0, cCanvas.width, cCanvas.height);
      let alive = false;
      particles.forEach(p => {{
        p.x += p.vx; p.y += p.vy; p.rot += p.spin; p.vy += 0.08;
        if (p.y < cCanvas.height + 30) alive = true;
        cCtx.save();
        cCtx.translate(p.x, p.y);
        cCtx.rotate(p.rot * Math.PI / 180);
        cCtx.fillStyle = p.color;
        if (p.shape === 'rect') cCtx.fillRect(-p.r/2, -p.r/2, p.r, p.r*0.5);
        else {{ cCtx.beginPath(); cCtx.arc(0,0,p.r/2,0,Math.PI*2); cCtx.fill(); }}
        cCtx.restore();
      }});
      frame2++;
      if (alive && frame2 < 300) requestAnimationFrame(confettiLoop);
      else cCtx.clearRect(0, 0, cCanvas.width, cCanvas.height);
    }}
    confettiLoop();
  }}
}})();
</script>

“””

st.components.v1.html(wheel_html, height=520)

# ── Spin Button ─────────────────────────────────────────────────────────────

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
spin_clicked = st.button(“🎰  SPIN  🎰”, use_container_width=True)

if spin_clicked:
# Choose random segment (weighted: prizes less likely)
weights = [0.08, 0.22, 0.15, 0.08, 0.08, 0.22, 0.08, 0.09]
idx = random.choices(range(N), weights=weights, k=1)[0]

```
# Calculate final rotation: multiple full spins + land on chosen segment
extra_spins = random.randint(6, 10) * 360
# Pointer is at top (12 o'clock). We want slice `idx` to end up under pointer.
# Segment idx starts at idx*sliceDeg from top (after -90 offset in drawing).
# To center segment under pointer: rotation = -(idx * SLICE_DEG + SLICE_DEG/2)
target_offset = -(idx * SLICE_DEG + SLICE_DEG / 2) + random.uniform(-SLICE_DEG * 0.35, SLICE_DEG * 0.35)
# Normalise so we always spin forward
current = st.session_state.rotation % 360
needed  = (target_offset % 360 - current) % 360
if needed < 45:
    needed += 360
new_rotation = st.session_state.rotation + extra_spins + needed

st.session_state.rotation   = new_rotation
st.session_state.result_idx = idx
st.session_state.spin_count += 1
if SEGMENTS[idx]["prize"]:
    st.session_state.prize_count += 1
st.rerun()
```

# ── Result Display ──────────────────────────────────────────────────────────

if st.session_state.result_idx is not None:
idx  = st.session_state.result_idx
seg  = SEGMENTS[idx]
name = seg[“label”].replace(”\n”, “ “)
emoji = seg[“emoji”]
is_prize = seg[“prize”]

```
if is_prize:
    st.markdown(f"""
    <div class="result-card">
      <div class="result-emoji">{emoji}</div>
      <div class="result-label">🎉 Congratulations! You Won 🎉</div>
      <div class="result-prize">{name}</div>
    </div>
    """, unsafe_allow_html=True)
elif "Spin Again" in name:
    st.markdown(f"""
    <div class="result-card" style="border-color:#a78bfa;">
      <div class="result-emoji">🔄</div>
      <div class="result-label" style="color:#c4b5fd;">Your turn again!</div>
      <div class="result-prize" style="font-size:1.8rem; color:#a78bfa;">SPIN AGAIN</div>
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown(f"""
    <div class="result-card" style="border-color:#6b7280; background:linear-gradient(135deg,#1f1f3a,#2d2d4e);">
      <div class="result-emoji">😔</div>
      <div class="result-label" style="color:#9ca3af;">Don't give up!</div>
      <div class="result-prize" style="color:#9ca3af; font-size:1.6rem;">BETTER LUCK NEXT TIME</div>
    </div>
    """, unsafe_allow_html=True)
```

# ── Stats ───────────────────────────────────────────────────────────────────

if st.session_state.spin_count > 0:
st.markdown(f”””
<div class="stats-row">
<div class="stat-chip">🎡 Spins: {st.session_state.spin_count}</div>
<div class="stat-chip">🏆 Prizes Won: {st.session_state.prize_count}</div>
<div class="stat-chip">🍀 Win Rate: {st.session_state.prize_count / st.session_state.spin_count * 100:.0f}%</div>
</div>
“””, unsafe_allow_html=True)

# ── Prizes Legend ───────────────────────────────────────────────────────────

st.markdown(”<br>”, unsafe_allow_html=True)
with st.expander(“🎁 Prize List”, expanded=False):
cols = st.columns(2)
prizes = [(s[“emoji”], s[“label”].replace(”\n”, “ “), s[“prize”]) for s in SEGMENTS]
for i, (em, lbl, is_p) in enumerate(prizes):
tag = “🏆” if is_p else (“🔄” if “Spin” in lbl else “💨”)
cols[i % 2].markdown(
f”<span style='font-family:Nunito,sans-serif; color:#f5c97a; font-size:0.9rem;'>{tag} {em} {lbl}</span>”,
unsafe_allow_html=True
)
