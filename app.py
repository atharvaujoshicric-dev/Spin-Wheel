import streamlit as st
import random

st.set_page_config(page_title='Lucky Spin Wheel', layout='centered')

st.markdown('''
<style>
@import url("https://fonts.googleapis.com/css2?family=Bangers&display=swap");
body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #f0e6d3 !important;
}
#MainMenu, footer, header, [data-testid="stToolbar"] { visibility: hidden; }
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #FFD700) !important;
    color: #1a0033 !important;
    font-family: "Bangers", cursive !important;
    font-size: 1.8rem !important;
    letter-spacing: 4px !important;
    border: none !important;
    border-radius: 50px !important;
    padding: 0.5rem 4rem !important;
    width: 100% !important;
    box-shadow: 0 6px 20px #FF8C0066 !important;
    margin-top: 1rem !important;
}
.result-box {
    text-align: center;
    padding: 1rem 2rem;
    border-radius: 16px;
    margin: 1rem auto;
    max-width: 400px;
    font-family: "Bangers", cursive;
}
</style>
''', unsafe_allow_html=True)

if 'angle' not in st.session_state:
    st.session_state['angle'] = 0
if 'result' not in st.session_state:
    st.session_state['result'] = ''
if 'spun' not in st.session_state:
    st.session_state['spun'] = False

SEGMENTS = [
    {'label': 'APPLE IPAD',               'bg': '#4B0082', 'fg': '#FFD700'},
    {'label': 'BETTER LUCK NEXT TIME',    'bg': '#F5E6C8', 'fg': '#4B0082'},
    {'label': 'SPIN AGAIN',               'bg': '#4B0082', 'fg': '#FFD700'},
    {'label': 'DOUBLE DOOR REFRIGERATOR', 'bg': '#F5E6C8', 'fg': '#4B0082'},
    {'label': 'SPLIT AIR CONDITIONER',    'bg': '#4B0082', 'fg': '#FFD700'},
    {'label': 'BETTER LUCK NEXT TIME',    'bg': '#F5E6C8', 'fg': '#4B0082'},
    {'label': 'APPLE AIRPODS',            'bg': '#4B0082', 'fg': '#FFFFFF'},
    {'label': 'SPIN AGAIN',               'bg': '#F5E6C8', 'fg': '#FF6600'},
]

N = 8
SLICE = 360.0 / N

segs_json = '['
for i, s in enumerate(SEGMENTS):
    comma = ',' if i < N - 1 else ''
    segs_json += '{"label":"' + s['label'] + '","bg":"' + s['bg'] + '","fg":"' + s['fg'] + '"}' + comma
segs_json += ']'

final_angle = st.session_state['angle']
spun = st.session_state['spun']

html_code = '''
<div style="display:flex;flex-direction:column;align-items:center;padding:10px 0;">
  <div style="position:relative;width:480px;height:480px;">

    <!-- Marigold outer ring -->
    <canvas id="ringCanvas" width="480" height="480"
      style="position:absolute;top:0;left:0;z-index:1;"></canvas>

    <!-- Wheel -->
    <canvas id="wheelCanvas" width="440" height="440"
      style="position:absolute;top:20px;left:20px;z-index:2;border-radius:50%;"></canvas>

    <!-- Pointer -->
    <div style="position:absolute;top:-10px;left:50%;transform:translateX(-50%);z-index:10;">
      <svg width="40" height="55" viewBox="0 0 40 55">
        <polygon points="20,55 0,5 40,5" fill="#FFD700" stroke="#a0522d" stroke-width="2"/>
        <polygon points="20,45 6,10 34,10" fill="#FF8C00"/>
        <circle cx="20" cy="8" r="5" fill="#FFD700" stroke="#a0522d" stroke-width="1.5"/>
      </svg>
    </div>
  </div>
  <div id="resultBox" style="display:none;text-align:center;padding:1rem 2rem;border-radius:16px;
    margin-top:1rem;max-width:400px;font-family:Bangers,cursive;font-size:1.8rem;
    background:linear-gradient(135deg,#3d0070,#6a00b8);border:3px solid #FFD700;
    color:#FFD700;box-shadow:0 0 30px #FFD70055;letter-spacing:2px;"></div>
</div>

<canvas id="confettiCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;
  pointer-events:none;z-index:9999;"></canvas>

<script>
(function() {
  var SEGS = ''' + segs_json + ''';
  var N = 8, SLICE = 360 / N;
  var wc = document.getElementById('wheelCanvas');
  var ctx = wc.getContext('2d');
  var cx = wc.width / 2, cy = wc.height / 2, R = wc.width / 2 - 4;

  // Draw marigold ring
  var rc = document.getElementById('ringCanvas');
  var rctx = rc.getContext('2d');
  var rcx = rc.width/2, rcy = rc.height/2, outerR = 238, innerR = 218;
  var flowerCount = 52;
  for (var f = 0; f < flowerCount; f++) {
    var ang = (f / flowerCount) * Math.PI * 2;
    var fx = rcx + Math.cos(ang) * (outerR - 11);
    var fy = rcy + Math.sin(ang) * (outerR - 11);
    rctx.beginPath();
    rctx.arc(fx, fy, 10, 0, Math.PI * 2);
    rctx.fillStyle = (f % 2 === 0) ? '#FF8C00' : '#FFD700';
    rctx.fill();
    rctx.beginPath();
    rctx.arc(fx, fy, 5, 0, Math.PI * 2);
    rctx.fillStyle = '#8B2500';
    rctx.fill();
  }

  function toRad(d) { return d * Math.PI / 180; }

  function drawWheel(rot) {
    ctx.clearRect(0, 0, wc.width, wc.height);
    for (var i = 0; i < N; i++) {
      var start = toRad(rot + i * SLICE - 90);
      var end   = toRad(rot + (i + 1) * SLICE - 90);
      var seg   = SEGS[i];
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R, start, end);
      ctx.closePath();
      ctx.fillStyle = seg.bg;
      ctx.fill();
      ctx.strokeStyle = '#6B21A8';
      ctx.lineWidth = 3;
      ctx.stroke();

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(toRad(rot + i * SLICE + SLICE / 2 - 90));
      ctx.textAlign = 'right';
      ctx.fillStyle = seg.fg;

      var words = seg.label.split(' ');
      var lines = [];
      if (words.length <= 2) {
        lines = [seg.label];
      } else if (words.length === 3) {
        lines = [words[0], words[1] + ' ' + words[2]];
      } else {
        var half = Math.ceil(words.length / 2);
        lines = [words.slice(0, half).join(' '), words.slice(half).join(' ')];
      }

      var fs = lines.length === 1 ? 17 : 14;
      ctx.font = '900 ' + fs + 'px Bangers, cursive';
      var tr = R * 0.76;
      var lh = fs + 4;
      var totalH = lines.length * lh;
      for (var l = 0; l < lines.length; l++) {
        ctx.fillText(lines[l], tr, -totalH / 2 + l * lh + lh * 0.75);
      }
      ctx.restore();
    }

    // Outer gold ring
    ctx.beginPath();
    ctx.arc(cx, cy, R + 1, 0, Math.PI * 2);
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 5;
    ctx.stroke();

    // Center circle
    ctx.beginPath();
    ctx.arc(cx, cy, 46, 0, Math.PI * 2);
    var cg = ctx.createRadialGradient(cx, cy, 4, cx, cy, 46);
    cg.addColorStop(0, '#ffffff');
    cg.addColorStop(0.45, '#f5e6c8');
    cg.addColorStop(1, '#d4a96a');
    ctx.fillStyle = cg;
    ctx.fill();
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Inner ring dots on center
    ctx.beginPath();
    ctx.arc(cx, cy, 38, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(180,120,60,0.5)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // Letter S in center
    ctx.font = 'bold 32px Georgia, serif';
    ctx.fillStyle = '#8B4513';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('S', cx, cy);
  }

  var curRot = ''' + str(final_angle) + ''';
  drawWheel(curRot);

  var TARGET_ANGLE = ''' + str(final_angle) + ''';
  var SHOULD_SPIN = ''' + ('true' if spun else 'false') + ''';

  if (SHOULD_SPIN) {
    var startRot = curRot - (8 * 360 + (''' + str(final_angle) + ''' % 360));
    // recalculate: animate from previous to final
    var prevAngle = TARGET_ANGLE - (8 * 360);
    if (prevAngle < 0) prevAngle = 0;
    animateSpin(prevAngle, TARGET_ANGLE);
  }

  function animateSpin(from, to) {
    var dur = 5000;
    var t0 = performance.now();
    function ease(t) { return 1 - Math.pow(1 - t, 4); }
    function frame(now) {
      var t = Math.min((now - t0) / dur, 1);
      curRot = from + (to - from) * ease(t);
      drawWheel(curRot);
      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        drawWheel(to);
        showResult();
      }
    }
    requestAnimationFrame(frame);
  }

  function showResult() {
    var norm = ((TARGET_ANGLE % 360) + 360) % 360;
    var landed = Math.floor(((360 - norm + 90) % 360) / (360 / N)) % N;
    var seg = SEGS[landed];
    var box = document.getElementById('resultBox');
    box.style.display = 'block';
    box.innerText = seg.label;
    if (seg.label.indexOf('LUCK') !== -1) {
      box.style.background = 'linear-gradient(135deg,#1f1f3a,#2d2d4e)';
      box.style.borderColor = '#6b7280';
      box.style.color = '#9ca3af';
    } else if (seg.label.indexOf('SPIN') !== -1) {
      box.style.background = 'linear-gradient(135deg,#2d0057,#4B0082)';
      box.style.borderColor = '#a78bfa';
      box.style.color = '#a78bfa';
    } else {
      box.style.background = 'linear-gradient(135deg,#3d0070,#6a00b8)';
      box.style.borderColor = '#FFD700';
      box.style.color = '#FFD700';
      launchConfetti();
    }
  }

  function launchConfetti() {
    var cc = document.getElementById('confettiCanvas');
    cc.width = window.innerWidth; cc.height = window.innerHeight;
    var c = cc.getContext('2d');
    var cols = ['#FFD700','#FF8C00','#7c3aed','#fff','#ff4f94','#00e5ff'];
    var ps = [];
    for (var i = 0; i < 200; i++) ps.push({
      x: Math.random() * cc.width, y: -20,
      vx: (Math.random() - 0.5) * 8, vy: Math.random() * 5 + 3,
      r: Math.random() * 9 + 4,
      col: cols[Math.floor(Math.random() * cols.length)],
      rot: Math.random() * 360, sp: (Math.random() - 0.5) * 10,
      sh: Math.random() > 0.5 ? 'r' : 'c'
    });
    var fn = 0;
    function loop() {
      c.clearRect(0, 0, cc.width, cc.height); var alive = false;
      ps.forEach(function(p) {
        p.x += p.vx; p.y += p.vy; p.rot += p.sp; p.vy += 0.1;
        if (p.y < cc.height + 30) alive = true;
        c.save(); c.translate(p.x, p.y); c.rotate(p.rot * Math.PI / 180);
        c.fillStyle = p.col;
        if (p.sh === 'r') c.fillRect(-p.r/2, -p.r/2, p.r, p.r * 0.5);
        else { c.beginPath(); c.arc(0, 0, p.r/2, 0, Math.PI*2); c.fill(); }
        c.restore();
      });
      fn++;
      if (alive && fn < 400) requestAnimationFrame(loop);
      else c.clearRect(0, 0, cc.width, cc.height);
    }
    loop();
  }

  if (!SHOULD_SPIN) {
    var resultBox = document.getElementById('resultBox');
    if (resultBox) resultBox.style.display = 'none';
  }
})();
</script>
'''

st.components.v1.html(html_code, height=560)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    spin_btn = st.button('SPIN THE WHEEL', use_container_width=True)

if spin_btn:
    weights = [0.10, 0.20, 0.12, 0.10, 0.10, 0.20, 0.10, 0.08]
    idx = random.choices(range(N), weights=weights, k=1)[0]
    extra_spins = random.randint(7, 11) * 360
    seg_center = -(idx * SLICE + SLICE / 2)
    jitter = random.uniform(-SLICE * 0.3, SLICE * 0.3)
    prev = st.session_state['angle']
    cur_norm = prev % 360
    target_norm = (seg_center + jitter) % 360
    needed = (target_norm - cur_norm) % 360
    if needed < 90:
        needed += 360
    st.session_state['angle'] = prev + extra_spins + needed
    st.session_state['result'] = SEGMENTS[idx]['label']
    st.session_state['spun'] = True
    st.rerun()
