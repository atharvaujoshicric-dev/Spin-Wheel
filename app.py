import streamlit as st
import random

st.set_page_config(page_title='Lucky Spin Wheel', layout='centered')

st.markdown('''
<style>
@import url("https://fonts.googleapis.com/css2?family=Bangers&display=swap");
body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background: #1a0033 !important;
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
    margin-top: 0.5rem !important;
}
</style>
''', unsafe_allow_html=True)

# Segments in clockwise order starting from TOP (12 o clock)
# Pointer is at TOP. The segment at top when wheel stops = prize.
# From image clockwise: APPLE IPAD, BETTER LUCK NEXT TIME, SPIN AGAIN,
# DOUBLE DOOR REFRIGERATOR, SPLIT AIR CONDITIONER, BETTER LUCK NEXT TIME,
# APPLE AIRPODS, SPIN AGAIN
SEGMENTS = [
    {'label': 'APPLE\nIPAD',                  'bg': '#4B0082', 'fg': '#FFD700', 'prize': True},
    {'label': 'BETTER\nLUCK\nNEXT TIME',       'bg': '#F0DEB4', 'fg': '#4B0082', 'prize': False},
    {'label': 'SPIN\nAGAIN',                   'bg': '#4B0082', 'fg': '#FFD700', 'prize': False},
    {'label': 'DOUBLE\nDOOR\nREFRIGERATOR',    'bg': '#F0DEB4', 'fg': '#1a0033', 'prize': True},
    {'label': 'SPLIT AIR\nCONDITIONER',        'bg': '#4B0082', 'fg': '#FFD700', 'prize': True},
    {'label': 'BETTER\nLUCK\nNEXT TIME',       'bg': '#F0DEB4', 'fg': '#4B0082', 'prize': False},
    {'label': 'APPLE\nAIRPODS',                'bg': '#4B0082', 'fg': '#FFFFFF', 'prize': True},
    {'label': 'SPIN\nAGAIN',                   'bg': '#F0DEB4', 'fg': '#FF6600', 'prize': False},
]

N = 8
SLICE = 360.0 / N

if 'angle' not in st.session_state:
    st.session_state['angle'] = 0.0
if 'prev_angle' not in st.session_state:
    st.session_state['prev_angle'] = 0.0
if 'spun' not in st.session_state:
    st.session_state['spun'] = False
if 'result_idx' not in st.session_state:
    st.session_state['result_idx'] = -1

segs_json = '['
for i, s in enumerate(SEGMENTS):
    comma = ',' if i < N - 1 else ''
    label_js = s['label'].replace('\n', '\\n')
    segs_json += '{"label":"' + label_js + '","bg":"' + s['bg'] + '","fg":"' + s['fg'] + '"}' + comma
segs_json += ']'

final_angle = st.session_state['angle']
prev_angle  = st.session_state['prev_angle']
spun        = st.session_state['spun']
result_idx  = st.session_state['result_idx']

html_code = '''
<div style="display:flex;flex-direction:column;align-items:center;padding:10px 0;font-family:Bangers,cursive;">

  <div style="position:relative;width:500px;height:500px;">

    <!-- Marigold ring canvas (static) -->
    <canvas id="ringCanvas" width="500" height="500"
      style="position:absolute;top:0;left:0;z-index:1;border-radius:50%;"></canvas>

    <!-- Wheel canvas -->
    <canvas id="wheelCanvas" width="440" height="440"
      style="position:absolute;top:30px;left:30px;z-index:2;border-radius:50%;"></canvas>

    <!-- Pointer at top center -->
    <div style="position:absolute;top:-4px;left:50%;transform:translateX(-50%);z-index:10;">
      <svg width="44" height="56" viewBox="0 0 44 56">
        <polygon points="22,56 1,6 43,6" fill="#FFD700" stroke="#8B4513" stroke-width="2"/>
        <polygon points="22,46 7,12 37,12" fill="#FF8C00"/>
        <circle cx="22" cy="9" r="5" fill="#FFD700" stroke="#8B4513" stroke-width="1.5"/>
      </svg>
    </div>

  </div>

  <!-- Result display -->
  <div id="resultBox" style="display:none;margin-top:12px;padding:14px 32px;border-radius:16px;
    font-size:1.6rem;letter-spacing:2px;text-align:center;max-width:420px;
    box-shadow:0 0 30px #FFD70055;transition:all 0.3s;"></div>

</div>

<canvas id="confettiCanvas" style="position:fixed;top:0;left:0;width:100%;height:100%;
  pointer-events:none;z-index:9999;"></canvas>

<script>
(function() {
  var SEGS = ''' + segs_json + ''';
  var N = 8, SLICE = 360 / N;

  // --- Marigold ring ---
  var rc  = document.getElementById('ringCanvas');
  var rctx = rc.getContext('2d');
  var rcx = rc.width / 2, rcy = rc.height / 2;
  var flowerR = 235, petalR = 11;
  var count = 56;
  for (var f = 0; f < count; f++) {
    var a = (f / count) * Math.PI * 2 - Math.PI / 2;
    var fx = rcx + Math.cos(a) * flowerR;
    var fy = rcy + Math.sin(a) * flowerR;
    // petals
    for (var p = 0; p < 6; p++) {
      var pa = (p / 6) * Math.PI * 2;
      rctx.beginPath();
      rctx.ellipse(fx + Math.cos(pa) * petalR * 0.6, fy + Math.sin(pa) * petalR * 0.6,
        petalR * 0.55, petalR * 0.35, pa, 0, Math.PI * 2);
      rctx.fillStyle = (f % 2 === 0) ? '#FF8C00' : '#FFA500';
      rctx.fill();
    }
    // center dot
    rctx.beginPath();
    rctx.arc(fx, fy, 4, 0, Math.PI * 2);
    rctx.fillStyle = '#8B2500';
    rctx.fill();
  }

  // --- Wheel ---
  var wc  = document.getElementById('wheelCanvas');
  var ctx = wc.getContext('2d');
  var cx  = wc.width / 2, cy = wc.height / 2, R = wc.width / 2 - 3;

  function toRad(d) { return d * Math.PI / 180; }

  function drawWheel(rot) {
    ctx.clearRect(0, 0, wc.width, wc.height);

    for (var i = 0; i < N; i++) {
      var startA = toRad(rot + i * SLICE - 90);
      var endA   = toRad(rot + (i + 1) * SLICE - 90);
      var seg    = SEGS[i];

      // Slice fill
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.arc(cx, cy, R, startA, endA);
      ctx.closePath();
      ctx.fillStyle = seg.bg;
      ctx.fill();
      ctx.strokeStyle = '#6B21A8';
      ctx.lineWidth = 2.5;
      ctx.stroke();

      // Text
      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(toRad(rot + i * SLICE + SLICE / 2 - 90));
      ctx.textAlign = 'right';
      ctx.fillStyle = seg.fg;

      var lines = seg.label.split('\\n');
      var fs = lines.length <= 2 ? 16 : 13;
      ctx.font = '900 ' + fs + 'px Bangers, cursive';
      var lh = fs + 5;
      var totalH = lines.length * lh;
      var tr = R * 0.75;

      for (var l = 0; l < lines.length; l++) {
        ctx.fillText(lines[l], tr, -totalH / 2 + l * lh + lh * 0.78);
      }
      ctx.restore();
    }

    // Gold outer ring
    ctx.beginPath();
    ctx.arc(cx, cy, R, 0, Math.PI * 2);
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 6;
    ctx.stroke();

    // Marigold dots on inner border of wheel
    var dotCount = 44, dotR = R - 8;
    for (var d = 0; d < dotCount; d++) {
      var da = (d / dotCount) * Math.PI * 2;
      ctx.beginPath();
      ctx.arc(cx + Math.cos(da) * dotR, cy + Math.sin(da) * dotR, 5, 0, Math.PI * 2);
      ctx.fillStyle = d % 2 === 0 ? '#FF8C00' : '#FFD700';
      ctx.fill();
    }

    // Center circle
    ctx.beginPath();
    ctx.arc(cx, cy, 50, 0, Math.PI * 2);
    var cg = ctx.createRadialGradient(cx, cy, 4, cx, cy, 50);
    cg.addColorStop(0, '#ffffff');
    cg.addColorStop(0.5, '#f5e6c8');
    cg.addColorStop(1, '#c8943a');
    ctx.fillStyle = cg;
    ctx.fill();
    ctx.strokeStyle = '#FFD700';
    ctx.lineWidth = 3;
    ctx.stroke();

    // Inner circle ring
    ctx.beginPath();
    ctx.arc(cx, cy, 42, 0, Math.PI * 2);
    ctx.strokeStyle = 'rgba(160,100,40,0.4)';
    ctx.lineWidth = 1.5;
    ctx.stroke();

    // S logo
    ctx.font = 'bold 36px Georgia, serif';
    ctx.fillStyle = '#8B4513';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('S', cx, cy);
  }

  // Initial draw at final resting angle
  var FINAL = ''' + str(final_angle) + ''';
  var PREV  = ''' + str(prev_angle) + ''';
  var SPUN  = ''' + ('true' if spun else 'false') + ''';
  var RES   = ''' + str(result_idx) + ''';

  drawWheel(FINAL);

  if (SPUN) {
    animateSpin(PREV, FINAL);
  }

  function animateSpin(from, to) {
    var dur = 5000;
    var t0  = performance.now();
    function ease(t) { return 1 - Math.pow(1 - t, 4); }
    function frame(now) {
      var t = Math.min((now - t0) / dur, 1);
      drawWheel(from + (to - from) * ease(t));
      if (t < 1) {
        requestAnimationFrame(frame);
      } else {
        drawWheel(to);
        showResult(RES);
      }
    }
    requestAnimationFrame(frame);
  }

  function showResult(idx) {
    if (idx < 0) return;
    var seg = SEGS[idx];
    var box = document.getElementById('resultBox');
    box.style.display = 'block';
    var label = seg.label.replace(/\\n/g, ' ');
    if (label.indexOf('LUCK') !== -1) {
      box.innerHTML = '<span style="color:#9ca3af;">😔 ' + label + '</span>';
      box.style.background = 'linear-gradient(135deg,#1f1f3a,#2d2d4e)';
      box.style.border = '3px solid #6b7280';
    } else if (label.indexOf('SPIN') !== -1) {
      box.innerHTML = '<span style="color:#a78bfa;">🔄 ' + label + '</span>';
      box.style.background = 'linear-gradient(135deg,#2d0057,#4B0082)';
      box.style.border = '3px solid #a78bfa';
    } else {
      box.innerHTML = '<span style="color:#FFD700;">🎉 YOU WON: ' + label + '!</span>';
      box.style.background = 'linear-gradient(135deg,#3d0070,#6a00b8)';
      box.style.border = '3px solid #FFD700';
      launchConfetti();
    }
  }

  // Show result immediately if page reloaded after spin
  if (!SPUN && RES >= 0) {
    showResult(RES);
  }

  function launchConfetti() {
    var cc = document.getElementById('confettiCanvas');
    cc.width = window.innerWidth; cc.height = window.innerHeight;
    var c = cc.getContext('2d');
    var cols = ['#FFD700','#FF8C00','#7c3aed','#fff','#ff4f94','#00e5ff'];
    var ps = [];
    for (var i = 0; i < 220; i++) ps.push({
      x: Math.random() * cc.width, y: -20,
      vx: (Math.random() - 0.5) * 9, vy: Math.random() * 5 + 2,
      r: Math.random() * 9 + 4,
      col: cols[Math.floor(Math.random() * cols.length)],
      rot: Math.random() * 360, sp: (Math.random() - 0.5) * 10,
      sh: Math.random() > 0.5 ? 'r' : 'c'
    });
    var fn = 0;
    function loop() {
      c.clearRect(0, 0, cc.width, cc.height);
      var alive = false;
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
      if (alive && fn < 450) requestAnimationFrame(loop);
      else c.clearRect(0, 0, cc.width, cc.height);
    }
    loop();
  }

})();
</script>
'''

st.components.v1.html(html_code, height=580)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    spin_btn = st.button('SPIN THE WHEEL', use_container_width=True)

if spin_btn:
    # Pick random segment
    idx = random.randint(0, N - 1)

    # Pointer is at top (12 o clock = -90 deg in canvas coords).
    # Segment i occupies angles: [i*SLICE, (i+1)*SLICE] relative to rotation.
    # For segment i to be under the pointer after rotation R:
    #   pointer angle in wheel frame = (-R - (-90)) mod 360 = (90 - R) mod 360
    # Center of segment i in wheel frame = i*SLICE + SLICE/2
    # So we need: (90 - R) mod 360 = i*SLICE + SLICE/2
    # => R = 90 - (i*SLICE + SLICE/2) + 360*k
    # We pick enough full rotations so it spins at least 7 full turns.

    target_seg_center = idx * SLICE + SLICE / 2
    jitter = random.uniform(-SLICE * 0.28, SLICE * 0.28)
    target_seg_center += jitter

    # Desired final rotation (mod 360)
    desired_mod = (90 - target_seg_center) % 360

    prev = st.session_state['angle']
    cur_mod = prev % 360

    # How much more to rotate to reach desired_mod
    delta = (desired_mod - cur_mod) % 360
    if delta < 45:
        delta += 360

    extra_spins = random.randint(7, 10) * 360
    new_angle = prev + extra_spins + delta

    st.session_state['prev_angle'] = prev
    st.session_state['angle'] = new_angle
    st.session_state['result_idx'] = idx
    st.session_state['spun'] = True
    st.rerun()
