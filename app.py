import streamlit as st
import random

st.set_page_config(page_title=“Lucky Spin Wheel”, layout=“centered”, page_icon=“🎡”)

# CSS

st.markdown(”””

<style>
@import url("https://fonts.googleapis.com/css2?family=Bangers&family=Nunito:wght@700;900&display=swap");
html, body, [data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 60% 20%, #2d0057 0%, #1a0033 60%, #0d0020 100%);
    min-height: 100vh;
}
[data-testid="stAppViewContainer"] {
    background: radial-gradient(ellipse at 60% 20%, #2d0057 0%, #1a0033 60%, #0d0020 100%) !important;
}
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stToolbar"] { display: none; }
.spin-title {
    font-family: "Bangers", cursive;
    font-size: 3.2rem;
    text-align: center;
    letter-spacing: 4px;
    color: #FFD700;
    text-shadow: 0 0 20px #ff8c00aa, 3px 3px 0 #a0522d;
    margin-bottom: 0.2rem;
}
.spin-subtitle {
    font-family: "Nunito", sans-serif;
    font-size: 1rem;
    text-align: center;
    color: #f5c97a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.wheel-outer { display:flex; justify-content:center; align-items:center; margin:0 auto 1.5rem auto; position:relative; width:520px; }
.wheel-wrapper { position:relative; display:inline-block; }
.wheel-wrapper::before {
    content:"";
    position:absolute; top:-14px; left:-14px;
    width:calc(100% + 28px); height:calc(100% + 28px);
    border-radius:50%;
    background:repeating-conic-gradient(#FF8C00 0deg 7deg, #FFD700 7deg 14deg);
    z-index:0;
}
.wheel-wrapper::after {
    content:"";
    position:absolute; top:-6px; left:-6px;
    width:calc(100% + 12px); height:calc(100% + 12px);
    border-radius:50%; background:#1a0033; z-index:1;
}
#wheelCanvas { position:relative; z-index:2; border-radius:50%; display:block; }
.pointer { position:absolute; top:-28px; left:50%; transform:translateX(-50%); z-index:10; }
.result-card {
    background: linear-gradient(135deg, #3d0070 0%, #6a00b8 50%, #3d0070 100%);
    border: 3px solid #FFD700; border-radius:16px; padding:1.2rem 2rem;
    text-align:center; margin:1rem auto; max-width:380px;
    box-shadow:0 0 30px #FFD70055; animation:resultPop 0.5s ease;
}
@keyframes resultPop { 0%{transform:scale(0.5);opacity:0;} 100%{transform:scale(1);opacity:1;} }
.result-label { font-family:"Bangers",cursive; font-size:1rem; color:#f5c97a; letter-spacing:3px; }
.result-prize { font-family:"Bangers",cursive; font-size:2.4rem; color:#FFD700; text-shadow:2px 2px 0 #a0522d; }
.result-emoji { font-size:2.5rem; margin-bottom:0.3rem; }
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #FFD700, #FF8C00) !important;
    color: #1a0033 !important; font-family:"Bangers",cursive !important;
    font-size:1.6rem !important; letter-spacing:3px !important;
    border:none !important; border-radius:50px !important;
    padding:0.6rem 3rem !important; width:100% !important;
    box-shadow:0 6px 20px #FF8C0066 !important;
}
.stButton > button:hover { transform:translateY(-3px) scale(1.04) !important; }
.stats-row { display:flex; gap:12px; justify-content:center; margin-top:1rem; flex-wrap:wrap; }
.stat-chip {
    background:rgba(255,215,0,0.12); border:1.5px solid rgba(255,215,0,0.35);
    border-radius:20px; padding:4px 14px; font-family:"Nunito",sans-serif;
    font-size:0.78rem; color:#f5c97a; letter-spacing:1px;
}
#confettiCanvas { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
</style>

“””, unsafe_allow_html=True)

SEGMENTS = [
{“label”: “Apple iPad”,              “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “📱”, “prize”: True},
{“label”: “Better Luck Next Time”,   “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “😢”, “prize”: False},
{“label”: “Spin Again”,              “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “🔄”, “prize”: False},
{“label”: “Double Door Refrigerator”,“color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “🧊”, “prize”: True},
{“label”: “Split Air Conditioner”,   “color”: “#3B0764”, “text_color”: “#FFD700”, “emoji”: “❄️”, “prize”: True},
{“label”: “Better Luck Next Time”,   “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “😢”, “prize”: False},
{“label”: “Apple AirPods”,           “color”: “#3B0764”, “text_color”: “#FFFFFF”, “emoji”: “🎧”, “prize”: True},
{“label”: “Spin Again”,              “color”: “#F5E6C8”, “text_color”: “#3B0764”, “emoji”: “🔄”, “prize”: False},
]

N = len(SEGMENTS)
SLICE_DEG = 360 / N

if “rotation” not in st.session_state:
st.session_state.rotation = 0.0
if “result_idx” not in st.session_state:
st.session_state.result_idx = None
if “spin_count” not in st.session_state:
st.session_state.spin_count = 0
if “prize_count” not in st.session_state:
st.session_state.prize_count = 0

st.markdown(’<div class="spin-title">🎡 LUCKY SPIN WHEEL 🎡</div>’, unsafe_allow_html=True)
st.markdown(’<div class="spin-subtitle">Spin & Win Exciting Prizes</div>’, unsafe_allow_html=True)

rotation_val = st.session_state.rotation
result_idx = st.session_state.result_idx
is_prize_js = “false”
if result_idx is not None and SEGMENTS[result_idx][“prize”]:
is_prize_js = “true”

segs_json = “[”
for i, s in enumerate(SEGMENTS):
comma = “,” if i < len(SEGMENTS) - 1 else “”
label = s[“label”].replace(”\n”, “ “)
segs_json += ‘{“label”:”’ + label + ‘”,“color”:”’ + s[“color”] + ‘”,“textColor”:”’ + s[“text_color”] + ‘”}’ + comma
segs_json += “]”

wheel_html = “””

<div class="wheel-outer">
  <div class="wheel-wrapper" id="wheelWrapper">
    <div class="pointer">
      <svg width="46" height="52" viewBox="0 0 46 52" fill="none">
        <polygon points="23,52 0,4 46,4" fill="#FFD700" stroke="#a0522d" stroke-width="2.5"/>
        <polygon points="23,42 8,10 38,10" fill="#FF8C00"/>
      </svg>
    </div>
    <canvas id="wheelCanvas" width="460" height="460"></canvas>
  </div>
</div>
<canvas id="confettiCanvas"></canvas>
<script>
(function(){
  var segments = """ + segs_json + """;
  var N = segments.length;
  var sliceDeg = 360 / N;
  var canvas = document.getElementById("wheelCanvas");
  var ctx = canvas.getContext("2d");
  var cx = canvas.width/2, cy = canvas.height/2, r = canvas.width/2 - 8;
  var currentRotation = """ + str(rotation_val) + """;
  var isPrize = """ + is_prize_js + """;
  function toRad(d){ return d * Math.PI / 180; }
  function drawWheel(rot){
    ctx.clearRect(0,0,canvas.width,canvas.height);
    for(var i=0;i<N;i++){
      var start = toRad(rot + i*sliceDeg - 90);
      var end   = toRad(rot + (i+1)*sliceDeg - 90);
      var seg   = segments[i];
      ctx.beginPath(); ctx.moveTo(cx,cy); ctx.arc(cx,cy,r,start,end); ctx.closePath();
      ctx.fillStyle = seg.color; ctx.fill();
      ctx.strokeStyle = "#7c3aed"; ctx.lineWidth = 2.5; ctx.stroke();
      ctx.save();
      ctx.translate(cx,cy);
      ctx.rotate(toRad(rot + i*sliceDeg + sliceDeg/2 - 90));
      ctx.textAlign = "right";
      ctx.fillStyle = seg.textColor;
      ctx.font = "900 15px Bangers, cursive";
      var words = seg.label.split(" ");
      var half = Math.ceil(words.length/2);
      var line1 = words.slice(0,half).join(" ");
      var line2 = words.slice(half).join(" ");
      var textR = r * 0.78;
      if(words.length <= 2){ ctx.fillText(seg.label, textR, 5); }
      else { ctx.fillText(line1, textR, -8); ctx.fillText(line2, textR, 12); }
      ctx.restore();
    }
    ctx.beginPath(); ctx.arc(cx,cy,r+2,0,Math.PI*2);
    ctx.strokeStyle="#FFD700"; ctx.lineWidth=4; ctx.stroke();
    ctx.beginPath(); ctx.arc(cx,cy,42,0,Math.PI*2);
    var g = ctx.createRadialGradient(cx,cy,5,cx,cy,42);
    g.addColorStop(0,"#fff"); g.addColorStop(0.4,"#f5e6c8"); g.addColorStop(1,"#d4a96a");
    ctx.fillStyle=g; ctx.fill();
    ctx.strokeStyle="#FFD700"; ctx.lineWidth=3; ctx.stroke();
    ctx.font="bold 28px serif"; ctx.fillStyle="#8B4513"; ctx.textAlign="center";
    ctx.fillText("S", cx, cy+10);
  }
  var animating = false;
  function spin(targetRot){
    if(animating) return; animating=true;
    var startRot=currentRotation, delta=targetRot-startRot;
    var duration=4500, startTime=performance.now();
    function easeOut(t){ return 1-Math.pow(1-t,4); }
    function frame(now){
      var t=Math.min((now-startTime)/duration,1);
      currentRotation=startRot+delta*easeOut(t);
      drawWheel(currentRotation);
      if(t<1){ requestAnimationFrame(frame); }
      else { animating=false; if(isPrize) launchConfetti(); }
    }
    requestAnimationFrame(frame);
  }
  drawWheel(currentRotation);
  var TARGET = """ + str(rotation_val) + """;
  if(Math.abs(TARGET - currentRotation) > 1) spin(TARGET);
  function launchConfetti(){
    var cc=document.getElementById("confettiCanvas");
    cc.width=window.innerWidth; cc.height=window.innerHeight;
    var cx2=cc.getContext("2d");
    var colors=["#FFD700","#FF8C00","#7c3aed","#ffffff","#ff4f94","#00e5ff"];
    var particles=[];
    for(var i=0;i<180;i++) particles.push({
      x:Math.random()*cc.width, y:-20,
      vx:(Math.random()-0.5)*6, vy:Math.random()*4+3,
      r:Math.random()*8+4, color:colors[Math.floor(Math.random()*colors.length)],
      rot:Math.random()*360, spin:(Math.random()-0.5)*8,
      shape:Math.random()>0.5?"rect":"circle"
    });
    var frame2=0;
    function loop(){
      cx2.clearRect(0,0,cc.width,cc.height);
      var alive=false;
      particles.forEach(function(p){
        p.x+=p.vx; p.y+=p.vy; p.rot+=p.spin; p.vy+=0.08;
        if(p.y<cc.height+30) alive=true;
        cx2.save(); cx2.translate(p.x,p.y); cx2.rotate(p.rot*Math.PI/180);
        cx2.fillStyle=p.color;
        if(p.shape==="rect") cx2.fillRect(-p.r/2,-p.r/2,p.r,p.r*0.5);
        else { cx2.beginPath(); cx2.arc(0,0,p.r/2,0,Math.PI*2); cx2.fill(); }
        cx2.restore();
      });
      frame2++;
      if(alive && frame2<300) requestAnimationFrame(loop);
      else cx2.clearRect(0,0,cc.width,cc.height);
    }
    loop();
  }
})();
</script>
"""

st.components.v1.html(wheel_html, height=520)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
spin_clicked = st.button(“🎰  SPIN  🎰”, use_container_width=True)

if spin_clicked:
weights = [0.08, 0.22, 0.15, 0.08, 0.08, 0.22, 0.08, 0.09]
idx = random.choices(range(N), weights=weights, k=1)[0]
extra_spins = random.randint(6, 10) * 360
target_offset = -(idx * SLICE_DEG + SLICE_DEG / 2) + random.uniform(-SLICE_DEG * 0.35, SLICE_DEG * 0.35)
current = st.session_state.rotation % 360
needed  = (target_offset % 360 - current) % 360
if needed < 45:
needed += 360
st.session_state.rotation   = st.session_state.rotation + extra_spins + needed
st.session_state.result_idx = idx
st.session_state.spin_count += 1
if SEGMENTS[idx][“prize”]:
st.session_state.prize_count += 1
st.rerun()

if st.session_state.result_idx is not None:
idx  = st.session_state.result_idx
seg  = SEGMENTS[idx]
name = seg[“label”]
emoji = seg[“emoji”]
is_prize = seg[“prize”]
if is_prize:
st.markdown(f’’’<div class="result-card">
<div class="result-emoji">{emoji}</div>
<div class="result-label">🎉 Congratulations! You Won 🎉</div>
<div class="result-prize">{name}</div>
</div>’’’, unsafe_allow_html=True)
elif “Spin Again” in name:
st.markdown(’’’<div class="result-card" style="border-color:#a78bfa;">
<div class="result-emoji">🔄</div>
<div class="result-label" style="color:#c4b5fd;">Your turn again!</div>
<div class="result-prize" style="color:#a78bfa;">SPIN AGAIN</div>
</div>’’’, unsafe_allow_html=True)
else:
st.markdown(’’’<div class="result-card" style="border-color:#6b7280;background:linear-gradient(135deg,#1f1f3a,#2d2d4e);">
<div class="result-emoji">😔</div>
<div class="result-label" style="color:#9ca3af;">Don’t give up!</div>
<div class="result-prize" style="color:#9ca3af;">BETTER LUCK NEXT TIME</div>
</div>’’’, unsafe_allow_html=True)

if st.session_state.spin_count > 0:
st.markdown(f’’’<div class="stats-row">
<div class="stat-chip">🎡 Spins: {st.session_state.spin_count}</div>
<div class="stat-chip">🏆 Prizes Won: {st.session_state.prize_count}</div>
<div class="stat-chip">🍀 Win Rate: {st.session_state.prize_count / st.session_state.spin_count * 100:.0f}%</div>
</div>’’’, unsafe_allow_html=True)
