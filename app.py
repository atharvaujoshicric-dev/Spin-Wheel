import streamlit as st
import random
import time
from datetime import datetime, timedelta
from streamlit_confetti import confetti

# --- PAGE CONFIG ---
st.set_page_config(page_title="Skyluxe Exclusive", page_icon="🏢", layout="centered")

# --- PREMIUM LUXURY CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@300;400;600&family=Cinzel:wght@400;600;700&family=Raleway:wght@300;400;500&display=swap');

    :root {
        --gold: #C9A84C;
        --gold-light: #E8C97A;
        --gold-dim: rgba(201,168,76,0.15);
        --gold-border: rgba(201,168,76,0.35);
        --dark: #0B0C0F;
        --dark-2: #13141A;
        --dark-3: #1C1E27;
        --text-muted: rgba(255,255,255,0.45);
    }

    html, body, .stApp {
        background-color: var(--dark) !important;
        font-family: 'Raleway', sans-serif;
    }

    .stApp {
        background-image: 
            radial-gradient(ellipse 80% 50% at 50% -10%, rgba(201,168,76,0.08) 0%, transparent 70%),
            repeating-linear-gradient(
                0deg,
                transparent,
                transparent 60px,
                rgba(201,168,76,0.025) 60px,
                rgba(201,168,76,0.025) 61px
            ),
            repeating-linear-gradient(
                90deg,
                transparent,
                transparent 60px,
                rgba(201,168,76,0.025) 60px,
                rgba(201,168,76,0.025) 61px
            ) !important;
    }

    h1, h2, h3 { font-family: 'Cinzel', serif !important; }

    /* ---- HEADER ---- */
    .luxury-header {
        text-align: center;
        padding: 40px 0 10px;
        position: relative;
    }
    .luxury-header::before {
        content: '';
        display: block;
        width: 60px;
        height: 1px;
        background: var(--gold);
        margin: 0 auto 18px;
    }
    .luxury-header h1 {
        font-family: 'Cinzel', serif;
        font-size: 2.8rem;
        font-weight: 700;
        letter-spacing: 0.35em;
        color: var(--gold-light);
        text-shadow: 0 0 40px rgba(201,168,76,0.3);
        margin: 0;
    }
    .luxury-header p {
        font-family: 'Raleway', sans-serif;
        font-size: 0.7rem;
        letter-spacing: 0.45em;
        color: var(--text-muted);
        margin: 8px 0 0;
        text-transform: uppercase;
    }
    .luxury-header::after {
        content: '◆';
        display: block;
        color: var(--gold);
        font-size: 0.6rem;
        margin-top: 14px;
        opacity: 0.7;
    }

    /* ---- TIMER ---- */
    .timer-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        margin: 20px auto 10px;
        max-width: 320px;
    }
    .timer-box {
        background: var(--gold-dim);
        border: 1px solid var(--gold-border);
        padding: 10px 28px;
        border-radius: 2px;
        text-align: center;
        color: var(--gold-light);
        font-family: 'Cinzel', serif;
        font-size: 1.3rem;
        letter-spacing: 0.2em;
        width: 100%;
        position: relative;
        overflow: hidden;
    }
    .timer-box::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.06), transparent);
        animation: shimmer 2.5s infinite;
    }
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    .timer-label {
        font-size: 0.55rem;
        letter-spacing: 0.35em;
        color: var(--text-muted);
        display: block;
        margin-bottom: 2px;
        font-family: 'Raleway', sans-serif;
    }

    /* ---- WHEEL SECTION ---- */
    .wheel-outer {
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 10px 0 24px;
        position: relative;
    }

    /* Pointer triangle */
    .wheel-pointer {
        width: 0;
        height: 0;
        border-left: 14px solid transparent;
        border-right: 14px solid transparent;
        border-top: 28px solid var(--gold);
        filter: drop-shadow(0 4px 10px rgba(201,168,76,0.6));
        margin-bottom: -6px;
        z-index: 10;
        position: relative;
    }

    /* Outer decorative ring */
    .wheel-ring {
        width: 300px;
        height: 300px;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            #1C1D26 0deg 45deg,
            #232430 45deg 90deg,
            #1C1D26 90deg 135deg,
            #232430 135deg 180deg,
            #1C1D26 180deg 225deg,
            #232430 225deg 270deg,
            #1C1D26 270deg 315deg,
            #232430 315deg 360deg
        );
        border: 3px solid transparent;
        background-clip: padding-box;
        box-shadow:
            0 0 0 3px var(--gold),
            0 0 0 6px var(--dark-2),
            0 0 0 8px rgba(201,168,76,0.4),
            0 0 60px rgba(201,168,76,0.18),
            inset 0 0 40px rgba(0,0,0,0.5);
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: transform 0.05s;
    }

    /* Gold segment dividers via pseudo-element overlay */
    .wheel-ring::before {
        content: '';
        position: absolute;
        inset: 0;
        border-radius: 50%;
        background: conic-gradient(
            from 0deg,
            transparent 0deg 44deg,
            rgba(201,168,76,0.55) 44deg 46deg,
            transparent 46deg 89deg,
            rgba(201,168,76,0.55) 89deg 91deg,
            transparent 91deg 134deg,
            rgba(201,168,76,0.55) 134deg 136deg,
            transparent 136deg 179deg,
            rgba(201,168,76,0.55) 179deg 181deg,
            transparent 181deg 224deg,
            rgba(201,168,76,0.55) 224deg 226deg,
            transparent 226deg 269deg,
            rgba(201,168,76,0.55) 269deg 271deg,
            transparent 271deg 314deg,
            rgba(201,168,76,0.55) 314deg 316deg,
            transparent 316deg 360deg
        );
    }

    /* Center hub */
    .wheel-hub {
        width: 60px;
        height: 60px;
        background: radial-gradient(circle at 40% 35%, #E8C97A, #8B6914);
        border-radius: 50%;
        border: 3px solid rgba(255,255,255,0.15);
        box-shadow:
            0 0 0 4px var(--dark-2),
            0 0 0 7px var(--gold),
            0 0 20px rgba(201,168,76,0.4);
        position: absolute;
        z-index: 5;
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: 'Cinzel', serif;
        font-size: 1.1rem;
        color: var(--dark);
    }

    /* Segment labels - positioned absolutely around wheel */
    .segment-label {
        position: absolute;
        width: 80px;
        text-align: center;
        font-family: 'Cinzel', serif;
        font-size: 0.52rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        color: rgba(255,255,255,0.9);
        text-transform: uppercase;
        transform-origin: center 150px;
        line-height: 1.3;
    }

    /* Spin animation */
    @keyframes spin-ease {
        0%   { transform: rotate(0deg); }
        100% { transform: rotate(3960deg); }
    }
    .spinning {
        animation: spin-ease 3s cubic-bezier(0.23, 1, 0.32, 1) forwards;
    }

    /* Outer decorative dots */
    .wheel-dots {
        position: absolute;
        width: 320px;
        height: 320px;
        border-radius: 50%;
        pointer-events: none;
    }

    /* ---- PRIZE REVEAL ---- */
    .prize-reveal {
        background: linear-gradient(135deg, rgba(201,168,76,0.08) 0%, rgba(201,168,76,0.03) 100%);
        border: 1px solid var(--gold-border);
        border-left: 4px solid var(--gold);
        padding: 24px 32px;
        margin: 20px 0;
        border-radius: 0 4px 4px 0;
        position: relative;
        overflow: hidden;
        animation: reveal-in 0.6s cubic-bezier(0.23,1,0.32,1) forwards;
    }
    @keyframes reveal-in {
        from { opacity: 0; transform: translateY(10px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .prize-reveal::before {
        content: '';
        position: absolute;
        inset: 0;
        background: linear-gradient(90deg, transparent, rgba(201,168,76,0.04), transparent);
        animation: shimmer 3s infinite;
    }
    .prize-reveal .label {
        font-size: 0.6rem;
        letter-spacing: 0.35em;
        color: var(--text-muted);
        font-family: 'Raleway', sans-serif;
        margin-bottom: 8px;
    }
    .prize-reveal .value {
        font-family: 'Cinzel', serif;
        font-size: 1.35rem;
        color: var(--gold-light);
        letter-spacing: 0.1em;
    }
    .prize-reveal .sub {
        font-size: 0.72rem;
        color: var(--text-muted);
        margin-top: 6px;
        font-family: 'Raleway', sans-serif;
    }

    /* ---- FORM ---- */
    .stTextInput label, .stCheckbox label {
        color: var(--text-muted) !important;
        font-family: 'Raleway', sans-serif !important;
        font-size: 0.75rem !important;
        letter-spacing: 0.18em !important;
        text-transform: uppercase !important;
    }
    .stTextInput input {
        background: var(--dark-3) !important;
        border: 1px solid var(--gold-border) !important;
        border-radius: 2px !important;
        color: #fff !important;
        font-family: 'Raleway', sans-serif !important;
        padding: 12px 16px !important;
    }
    .stTextInput input:focus {
        border-color: var(--gold) !important;
        box-shadow: 0 0 0 1px var(--gold) !important;
    }

    /* ---- BUTTONS ---- */
    .stButton > button {
        background: linear-gradient(135deg, #C9A84C, #8B6914) !important;
        color: var(--dark) !important;
        font-family: 'Cinzel', serif !important;
        font-weight: 600 !important;
        letter-spacing: 0.25em !important;
        font-size: 0.78rem !important;
        border: none !important;
        border-radius: 2px !important;
        padding: 14px 36px !important;
        width: 100% !important;
        transition: all 0.3s ease !important;
        text-transform: uppercase !important;
        position: relative;
        overflow: hidden;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #E8C97A, #C9A84C) !important;
        box-shadow: 0 6px 30px rgba(201,168,76,0.35) !important;
        transform: translateY(-1px) !important;
    }

    /* ---- WELCOME TEXT ---- */
    .welcome-line {
        text-align: center;
        font-family: 'Raleway', sans-serif;
        font-size: 0.8rem;
        letter-spacing: 0.15em;
        color: var(--text-muted);
        margin-bottom: 16px;
    }
    .welcome-line span { color: var(--gold-light); font-weight: 500; }

    /* ---- SPINS REMAINING ---- */
    .spins-row {
        display: flex;
        justify-content: center;
        gap: 8px;
        margin-bottom: 20px;
    }
    .spin-dot {
        width: 10px; height: 10px;
        border-radius: 50%;
        background: var(--gold);
        box-shadow: 0 0 8px rgba(201,168,76,0.5);
    }
    .spin-dot.used {
        background: var(--dark-3);
        border: 1px solid var(--gold-border);
        box-shadow: none;
    }

    /* ---- DIVIDER ---- */
    .gold-divider {
        display: flex;
        align-items: center;
        gap: 12px;
        margin: 24px 0;
        color: var(--gold-border);
        font-size: 0.55rem;
        letter-spacing: 0.3em;
    }
    .gold-divider::before, .gold-divider::after {
        content: '';
        flex: 1;
        height: 1px;
        background: linear-gradient(90deg, transparent, var(--gold-border));
    }
    .gold-divider::after {
        background: linear-gradient(90deg, var(--gold-border), transparent);
    }

    /* Info / warning boxes */
    .stAlert {
        background: var(--dark-3) !important;
        border-color: var(--gold-border) !important;
        color: var(--text-muted) !important;
        border-radius: 2px !important;
    }

    /* Unlock heading */
    .unlock-heading {
        font-family: 'Cinzel', serif;
        font-size: 1.05rem;
        letter-spacing: 0.3em;
        color: var(--gold-light);
        text-align: center;
        margin: 30px 0 24px;
    }
    .unlock-sub {
        font-family: 'Raleway', sans-serif;
        font-size: 0.72rem;
        color: var(--text-muted);
        text-align: center;
        letter-spacing: 0.12em;
        margin-bottom: 28px;
    }

    .footer-note {
        text-align: center;
        font-family: 'Raleway', sans-serif;
        font-size: 0.62rem;
        letter-spacing: 0.18em;
        color: rgba(255,255,255,0.2);
        margin-top: 40px;
        padding-bottom: 30px;
    }
    </style>
""", unsafe_allow_html=True)

# ---- SESSION STATE ----
if 'spins_left' not in st.session_state:
    st.session_state.spins_left = 2
if 'winner_name' not in st.session_state:
    st.session_state.winner_name = ""
if 'is_spinning' not in st.session_state:
    st.session_state.is_spinning = False
if 'final_prize' not in st.session_state:
    st.session_state.final_prize = None
if 'expiry_time' not in st.session_state:
    st.session_state.expiry_time = None

# ---- HEADER ----
st.markdown("""
<div class="luxury-header">
    <h1>SKYLUXE</h1>
    <p>Residences &nbsp;·&nbsp; Rewards &nbsp;·&nbsp; Legacy</p>
</div>
""", unsafe_allow_html=True)

# =====================
# 1. LEAD GENERATION
# =====================
if not st.session_state.winner_name:
    st.markdown('<div class="unlock-heading">UNLOCK YOUR EXCLUSIVE OFFER</div>', unsafe_allow_html=True)
    st.markdown('<div class="unlock-sub">Two complimentary spins await — register to reveal your reward</div>', unsafe_allow_html=True)

    name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    agree = st.checkbox("I agree to the Terms & Conditions of Skyluxe Projects")

    if st.button("REGISTER & SPIN"):
        if name and phone and agree:
            st.session_state.winner_name = name
            st.session_state.expiry_time = datetime.now() + timedelta(minutes=10)
            st.rerun()
        elif not agree:
            st.warning("Please accept the Terms & Conditions to continue.")
        else:
            st.error("All fields are required.")

    st.markdown('<div class="footer-note">EXCLUSIVE PREVIEW EVENT &nbsp;·&nbsp; LIMITED ACCESS</div>', unsafe_allow_html=True)

# =====================
# 2. GAME PHASE
# =====================
else:
    remaining = st.session_state.expiry_time - datetime.now()

    if remaining.total_seconds() <= 0:
        st.error("⌛ This exclusive session has expired.")
    else:
        mins, secs = divmod(int(remaining.total_seconds()), 60)

        # Timer
        st.markdown(f"""
        <div class="timer-wrap">
            <div class="timer-box">
                <span class="timer-label">Session Expires In</span>
                {mins:02d}:{secs:02d}
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Welcome + Spins
        spins = st.session_state.spins_left
        dots_html = ''.join(
            f'<div class="spin-dot{"" if i < spins else " used"}"></div>'
            for i in range(2)
        )
        st.markdown(f"""
        <div class="welcome-line">Welcome, <span>{st.session_state.winner_name}</span></div>
        <div class="spins-row">{dots_html}</div>
        <div style="text-align:center; font-family:'Raleway',sans-serif; font-size:0.65rem; letter-spacing:0.3em; color:var(--text-muted); margin-bottom:24px;">
            {spins} SPIN{"S" if spins != 1 else ""} REMAINING
        </div>
        """, unsafe_allow_html=True)

        # ---- WHEEL ----
        wheel_class = "spinning" if st.session_state.is_spinning else ""

        # 8 segments with labels
        segments = [
            ("AIRPODS", "🎧"),
            ("APPLE", "IPAD"),
            ("TRY", "AGAIN"),
            ("AC", "UNIT"),
            ("BETTER", "LUCK"),
            ("FRIDGE", "◆"),
            ("BETTER", "LUCK"),
            ("BETTER", "LUCK"),
        ]

        # Build segment labels (positioned around the wheel)
        labels_html = ""
        for i, (line1, line2) in enumerate(segments):
            angle = i * 45 + 22.5  # center of each 45° segment
            labels_html += f"""
            <div class="segment-label" style="
                position:absolute;
                top:50%; left:50%;
                width:68px;
                margin-left:-34px;
                margin-top:-150px;
                transform-origin: 34px 150px;
                transform: rotate({angle}deg);
                font-family:'Cinzel',serif;
                font-size:0.46rem;
                font-weight:600;
                letter-spacing:0.06em;
                color:rgba(255,255,255,0.82);
                text-align:center;
                text-transform:uppercase;
            ">{line1}<br>{line2}</div>"""

        st.markdown(f"""
        <div class="wheel-outer">
            <div class="wheel-pointer"></div>
            <div class="wheel-ring {wheel_class}" style="position:relative;">
                {labels_html}
                <div class="wheel-hub">✦</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Spin button
        if spins > 0 and not st.session_state.is_spinning:
            if st.button("✦ SPIN THE WHEEL"):
                st.session_state.is_spinning = True
                st.rerun()

        # Spin logic
        if st.session_state.is_spinning:
            time.sleep(3.2)
            prizes = [
                "Airpods", "Apple iPad", "Split Air Conditioner",
                "Double Door Refrigerator", "Spin Again",
                "Better Luck Next Time", "Better Luck Next Time", "Better Luck Next Time"
            ]
            result = random.choice(prizes)

            if result == "Spin Again":
                st.session_state.final_prize = "SPIN AGAIN"
            else:
                st.session_state.spins_left -= 1
                st.session_state.final_prize = result

            st.session_state.is_spinning = False
            st.rerun()

        # Prize reveal
        if st.session_state.final_prize:
            prize = st.session_state.final_prize
            is_win = "Better Luck" not in prize and "SPIN AGAIN" not in prize

            if is_win:
                sub_text = "Visit the Skyluxe Experience Center to claim your reward."
                icon = "✦"
            elif "SPIN AGAIN" in prize:
                sub_text = "Your chance is preserved — spin again!"
                icon = "◈"
            else:
                sub_text = "Keep exploring — fortune favors the persistent."
                icon = "◇"

            st.markdown(f"""
            <div class="prize-reveal">
                <div class="label">YOUR RESULT</div>
                <div class="value">{icon}&nbsp;&nbsp;{prize}</div>
                <div class="sub">{sub_text}</div>
            </div>
            """, unsafe_allow_html=True)

            if is_win:
                confetti(emojis=['🏢', '✨', '🏆', '◆'])
                st.balloons()

        st.markdown('<div class="gold-divider">◆</div>', unsafe_allow_html=True)

    # Out of spins
    if st.session_state.spins_left == 0 and not st.session_state.is_spinning:
        st.info("Please visit the Skyluxe Experience Center to claim your reward.")
        if st.button("↩ New Registration"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()

    st.markdown('<div class="footer-note">SKYLUXE RESIDENCES &nbsp;·&nbsp; ALL RIGHTS RESERVED</div>', unsafe_allow_html=True)
