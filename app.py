import streamlit as st
import random

cfg = dict(page_title='Lucky Spin Wheel', layout='centered')
st.set_page_config(**cfg)

st.markdown('''
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
.stButton > button {
    background: linear-gradient(135deg, #FF8C00, #FFD700, #FF8C00) !important;
    color: #1a0033 !important; font-family:"Bangers",cursive !important;
    font-size:1.6rem !important; letter-spacing:3px !important;
    border:none !important; border-radius:50px !important;
    padding:0.6rem 3rem !important; width:100% !important;
    box-shadow:0 6px 20px #FF8C0066 !important;
}
.stats-row { display:flex; gap:12px; justify-content:center; margin-top:1rem; flex-wrap:wrap; }
.stat-chip {
    background:rgba(255,215,0,0.12); border:1.5px solid rgba(255,215,0,0.35);
    border-radius:20px; padding:4px 14px; font-family:"Nunito",sans-serif;
    font-size:0.78rem; color:#f5c97a;
}
#confettiCanvas { position:fixed; top:0; left:0; width:100%; height:100%; pointer-events:none; z-index:9999; }
</style>
''', unsafe_allow_html=True)

SEGMENTS = [
    {'label': 'Apple iPad',               'color': '#3B0764', 'tc': '#FFD700', 'prize': True},
    {'label': 'Better Luck Next Time',    'color': '#F5E6C8', 'tc': '#3B0764', 'prize': False},
    {'label': 'Spin Again',               'color': '#3B0764', 'tc': '#FFD700', 'prize': False},
    {'label': 'Double Door Refrigerator', 'color': '#F5E6C8', 'tc': '#3B0764', 'prize': True},
    {'label': 'Split Air Conditioner',    'color': '#3B0764', 'tc': '#FFD700', 'prize': True},
    {'label': 'Better Luck Next Time',    'color': '#F5E6C8', 'tc': '#3B0764', 'prize': False},
    {'label': 'Apple AirPods',            'color': '#3B0764', 'tc': '#FFFFFF', 'prize': True},
    {'label': 'Spin Again',               'color': '#F5E6C8', 'tc': '#3B0764', 'prize': False},
]

N = len(SEGMENTS)
SLICE_DEG = 360.0 / N

for key, val in [('rotation', 0.0), ('result_idx', None), ('spin_count', 0), ('prize_count', 0)]:
    if key not in st.session_state:
        st.session_state[key] = val

st.markdown('<div class="spin-title">LUCKY SPIN WHEEL</div>', unsafe_allow_html=True)
st.markdown('<div class="spin-subtitle">Spin and Win Exciting Prizes</div>', unsafe_allow_html=True)

rot = st.session_state['rotation']
ridx = st.session_state['result_idx']
is_prize_js = 'true' if (ridx is not None and SEGMENTS[ridx]['prize']) else 'false'

segs_js = '['
for i, s in enumerate(SEGMENTS):
    comma = ',' if i < N - 1 else ''
    segs_js += '{"label":"' + s['label'] + '","color":"' + s['color'] + '","tc":"' + s['tc'] + '"}' + comma
segs_js += ']'

html = (
    '<div style="display:flex;justify-content:center;margin-bottom:1rem;">'
    '<div class="wheel-wrapper">'
    '<div class="pointer">'
    '<svg width="46" height="52" viewBox="0 0 46 52" fill="none">'
    '<polygon points="23,52 0,4 46,4" fill="#FFD700" stroke="#a0522d" stroke-width="2.5"/>'
    '<polygon points="23,42 8,10 38,10" fill="#FF8C00"/>'
    '</svg></div>'
    '<canvas id="wheelCanvas" width="460" height="460"></canvas>'
    '</div></div>'
    '<canvas id="confettiCanvas"></canvas>'
    '<script>'
    '(function(){'
    'var segs=' + segs_js + ';'
    'var N=segs.length,sd=360/N;'
    'var cv=document.getElementById("wheelCanvas"),ctx=cv.getContext("2d");'
    'var cx=cv.width/2,cy=cv.height/2,r=cv.width/2-8;'
    'var curRot=' + str(rot) + ';'
    'var isPrize=' + is_prize_js + ';'
    'function rad(d){return d*Math.PI/180;}'
    'function draw(rot){'
    'ctx.clearRect(0,0,cv.width,cv.height);'
    'for(var i=0;i<N;i++){'
    'var s=rad(rot+i*sd-90),e=rad(rot+(i+1)*sd-90);'
    'ctx.beginPath();ctx.moveTo(cx,cy);ctx.arc(cx,cy,r,s,e);ctx.closePath();'
    'ctx.fillStyle=segs[i].color;ctx.fill();'
    'ctx.strokeStyle="#7c3aed";ctx.lineWidth=2.5;ctx.stroke();'
    'ctx.save();ctx.translate(cx,cy);'
    'ctx.rotate(rad(rot+i*sd+sd/2-90));'
    'ctx.textAlign="right";ctx.fillStyle=segs[i].tc;'
    'ctx.font="900 14px Bangers,cursive";'
    'var words=segs[i].label.split(" ");'
    'var h=Math.ceil(words.length/2);'
    'var l1=words.slice(0,h).join(" "),l2=words.slice(h).join(" ");'
    'var tr=r*0.78;'
    'if(words.length<=2){ctx.fillText(segs[i].label,tr,5);}'
    'else{ctx.fillText(l1,tr,-8);ctx.fillText(l2,tr,10);}'
    'ctx.restore();'
    '}'
    'ctx.beginPath();ctx.arc(cx,cy,r+2,0,Math.PI*2);'
    'ctx.strokeStyle="#FFD700";ctx.lineWidth=4;ctx.stroke();'
    'ctx.beginPath();ctx.arc(cx,cy,42,0,Math.PI*2);'
    'var g=ctx.createRadialGradient(cx,cy,5,cx,cy,42);'
    'g.addColorStop(0,"#fff");g.addColorStop(0.5,"#f5e6c8");g.addColorStop(1,"#d4a96a");'
    'ctx.fillStyle=g;ctx.fill();'
    'ctx.strokeStyle="#FFD700";ctx.lineWidth=3;ctx.stroke();'
    'ctx.font="bold 26px serif";ctx.fillStyle="#8B4513";ctx.textAlign="center";'
    'ctx.fillText("S",cx,cy+9);'
    '}'
    'var anim=false;'
    'function spin(target){'
    'if(anim)return;anim=true;'
    'var s0=curRot,d=target-s0,dur=4500,t0=performance.now();'
    'function ease(t){return 1-Math.pow(1-t,4);}'
    'function frame(now){'
    'var t=Math.min((now-t0)/dur,1);'
    'curRot=s0+d*ease(t);draw(curRot);'
    'if(t<1){requestAnimationFrame(frame);}'
    'else{anim=false;if(isPrize)confetti();}'
    '}'
    'requestAnimationFrame(frame);'
    '}'
    'draw(curRot);'
    'var TARGET=' + str(rot) + ';'
    'if(Math.abs(TARGET-curRot)>1)spin(TARGET);'
    'function confetti(){'
    'var cc=document.getElementById("confettiCanvas");'
    'cc.width=window.innerWidth;cc.height=window.innerHeight;'
    'var c=cc.getContext("2d");'
    'var cols=["#FFD700","#FF8C00","#7c3aed","#fff","#ff4f94","#00e5ff"],ps=[];'
    'for(var i=0;i<180;i++)ps.push({'
    'x:Math.random()*cc.width,y:-20,'
    'vx:(Math.random()-0.5)*6,vy:Math.random()*4+3,'
    'r:Math.random()*8+4,col:cols[Math.floor(Math.random()*cols.length)],'
    'rot:Math.random()*360,sp:(Math.random()-0.5)*8,'
    'sh:Math.random()>0.5?"r":"c"'
    '});'
    'var fn=0;'
    'function loop(){'
    'c.clearRect(0,0,cc.width,cc.height);var alive=false;'
    'ps.forEach(function(p){'
    'p.x+=p.vx;p.y+=p.vy;p.rot+=p.sp;p.vy+=0.08;'
    'if(p.y<cc.height+30)alive=true;'
    'c.save();c.translate(p.x,p.y);c.rotate(p.rot*Math.PI/180);'
    'c.fillStyle=p.col;'
    'if(p.sh==="r")c.fillRect(-p.r/2,-p.r/2,p.r,p.r*0.5);'
    'else{c.beginPath();c.arc(0,0,p.r/2,0,Math.PI*2);c.fill();}'
    'c.restore();'
    '});'
    'fn++;if(alive&&fn<300)requestAnimationFrame(loop);'
    'else c.clearRect(0,0,cc.width,cc.height);'
    '}'
    'loop();'
    '}'
    '})();'
    '</script>'
)

st.components.v1.html(html, height=520)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    spin_clicked = st.button('SPIN', use_container_width=True)

if spin_clicked:
    weights = [0.08, 0.22, 0.15, 0.08, 0.08, 0.22, 0.08, 0.09]
    idx = random.choices(range(N), weights=weights, k=1)[0]
    extra = random.randint(6, 10) * 360
    offset = -(idx * SLICE_DEG + SLICE_DEG / 2) + random.uniform(-SLICE_DEG * 0.35, SLICE_DEG * 0.35)
    cur = st.session_state['rotation'] % 360
    needed = (offset % 360 - cur) % 360
    if needed < 45:
        needed += 360
    st.session_state['rotation'] = st.session_state['rotation'] + extra + needed
    st.session_state['result_idx'] = idx
    st.session_state['spin_count'] += 1
    if SEGMENTS[idx]['prize']:
        st.session_state['prize_count'] += 1
    st.rerun()

ridx = st.session_state['result_idx']
if ridx is not None:
    seg = SEGMENTS[ridx]
    name = seg['label']
    if seg['prize']:
        st.markdown(
            '<div class="result-card">'
            '<div class="result-label">Congratulations! You Won</div>'
            '<div class="result-prize">' + name + '</div>'
            '</div>',
            unsafe_allow_html=True
        )
    elif 'Spin' in name:
        st.markdown(
            '<div class="result-card" style="border-color:#a78bfa;">'
            '<div class="result-label" style="color:#c4b5fd;">Your turn again!</div>'
            '<div class="result-prize" style="color:#a78bfa;">SPIN AGAIN</div>'
            '</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="result-card" style="border-color:#6b7280;background:linear-gradient(135deg,#1f1f3a,#2d2d4e);">'
            '<div class="result-label" style="color:#9ca3af;">Do not give up!</div>'
            '<div class="result-prize" style="color:#9ca3af;">BETTER LUCK NEXT TIME</div>'
            '</div>',
            unsafe_allow_html=True
        )

sc = st.session_state['spin_count']
pc = st.session_state['prize_count']
if sc > 0:
    wr = int(pc / sc * 100)
    st.markdown(
        '<div class="stats-row">'
        '<div class="stat-chip">Spins: ' + str(sc) + '</div>'
        '<div class="stat-chip">Prizes Won: ' + str(pc) + '</div>'
        '<div class="stat-chip">Win Rate: ' + str(wr) + '%</div>'
        '</div>',
        unsafe_allow_html=True
    )
