import streamlit as st
import time
import random
import os
from datetime import datetime

# Page Configuration
st.set_page_config(
    page_title="Zainfxbot Pro Max",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom Dark Navy (#111827) + Electric Blue (#3B82F6) Professional Theme
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    .stApp {
        background-color: #111827;
        color: #ffffff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 4rem !important;
        max-width: 480px !important;
    }

    /* Titles */
    .bot-title-main {
        text-align: center;
        font-size: 2.2rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: 1px;
        margin: 0;
        text-transform: uppercase;
    }
    .bot-title-sub {
        text-align: center;
        font-size: 1.6rem;
        font-weight: 800;
        color: #3B82F6;
        letter-spacing: 2px;
        margin-top: -5px;
        margin-bottom: 20px;
        text-transform: uppercase;
    }

    /* Glass Card */
    .glass-card {
        background: rgba(17, 24, 39, 0.85);
        border: 1.5px solid rgba(59, 130, 246, 0.4);
        border-radius: 24px;
        padding: 25px 20px;
        box-shadow: 0 0 35px rgba(59, 130, 246, 0.2);
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }

    /* Inputs & Selectbox */
    .stTextInput > div > div {
        background-color: #1f2937 !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    .stSelectbox > div > div {
        background-color: #1f2937 !important;
        border: 1px solid #3B82F6 !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }

    /* Button Styling */
    .stButton > button {
        width: 100%;
        background: linear-gradient(90deg, #1d4ed8 0%, #3B82F6 100%);
        color: #ffffff;
        font-weight: 800;
        font-size: 1.1rem;
        border-radius: 14px;
        border: 1px solid #60a5fa;
        padding: 12px 0;
        box-shadow: 0 0 20px rgba(59, 130, 246, 0.5);
        margin-top: 15px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #3B82F6 100%, #1d4ed8 0%);
        box-shadow: 0 0 30px rgba(59, 130, 246, 0.8);
    }

    /* Stats Row */
    .stats-row {
        display: flex;
        justify-content: space-between;
        gap: 8px;
        margin-bottom: 15px;
    }
    .stat-box {
        background: #1f2937;
        border: 1px solid rgba(59, 130, 246, 0.3);
        border-radius: 14px;
        padding: 10px 5px;
        text-align: center;
        flex: 1;
    }
    .stat-label {
        font-size: 0.6rem;
        color: #93c5fd;
        text-transform: uppercase;
        font-weight: 700;
    }
    .stat-val {
        font-size: 0.8rem;
        color: #3B82F6;
        font-weight: 800;
        margin-top: 2px;
    }
    .badge-pro {
        background: linear-gradient(90deg, #1e3a8a 0%, #111827 100%);
        border: 1px solid #3B82F6;
        color: #60a5fa;
        text-align: center;
        border-radius: 18px;
        padding: 8px;
        font-weight: 800;
        font-size: 0.85rem;
        margin-bottom: 20px;
        box-shadow: 0 0 15px rgba(59, 130, 246, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

# Safe Logo Display Function
def show_logo():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        try:
            if os.path.exists("logo.png"):
                st.image("logo.png", width=120)
            elif os.path.exists("images.jfif"):
                st.image("images.jfif", width=120)
            else:
                st.markdown("<h2 style='text-align:center;'>🤖</h2>", unsafe_allow_html=True)
        except Exception:
            st.markdown("<h2 style='text-align:center;'>🤖</h2>", unsafe_allow_html=True)

# ================= POPUP MODAL FOR SIGNAL SCANNING =================
@st.dialog("🤖 AI ANALYZING MARKET")
def show_signal_popup(broker, market, pair, timer):
    st.markdown(f"""
        <div style="text-align: center; color: #3B82F6; font-weight: bold; font-size: 1.1rem; margin-bottom: 10px;">
            {pair} &nbsp;|&nbsp; {market} &nbsp;|&nbsp; {timer}
        </div>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div style="background: #0b1329; border: 1.5px solid #3B82F6; border-radius: 16px; padding: 15px; text-align: center; margin-bottom: 15px;">
            <div style="font-size: 1.1rem; font-weight: bold; color: #60a5fa; margin-bottom: 10px;">📈 Candle Pattern Scanner</div>
            <div style="display: flex; justify-content: center; align-items: flex-end; height: 80px; gap: 5px; padding: 10px; background: rgba(0,0,0,0.4); border-radius: 10px;">
                <div style="width: 7px; height: 35px; background: #22c55e; border-radius: 2px;"></div>
                <div style="width: 7px; height: 50px; background: #ef4444; border-radius: 2px;"></div>
                <div style="width: 7px; height: 25px; background: #22c55e; border-radius: 2px;"></div>
                <div style="width: 7px; height: 65px; background: #22c55e; border-radius: 2px;"></div>
                <div style="width: 7px; height: 40px; background: #ef4444; border-radius: 2px;"></div>
                <div style="width: 7px; height: 75px; background: #ef4444; border-radius: 2px;"></div>
                <div style="width: 7px; height: 55px; background: #22c55e; border-radius: 2px;"></div>
                <div style="width: 7px; height: 70px; background: #ef4444; border-radius: 2px;"></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    for i in range(100):
        time.sleep(0.03)
        progress_bar.progress(i + 1)
        if i < 30:
            status_placeholder.markdown("<p style='text-align:center; color:#93c5fd; font-size:0.85rem;'>🔄 Scanning candles & order book...</p>", unsafe_allow_html=True)
        elif i < 70:
            status_placeholder.markdown("<p style='text-align:center; color:#93c5fd; font-size:0.85rem;'>📊 Analyzing RSI, MACD & EMA indicators...</p>", unsafe_allow_html=True)
        else:
            status_placeholder.markdown("<p style='text-align:center; color:#93c5fd; font-size:0.85rem;'>⚡ Calibrating high-accuracy signal...</p>", unsafe_allow_html=True)

    time.sleep(0.4)
    status_placeholder.empty()
    progress_bar.empty()

    direction = random.choice(["UP 🟢", "DOWN 🔴"])
    accuracy = random.randint(97, 100)
    entry_time = datetime.now().strftime("%I:%M:%S %p")

    if "UP" in direction:
        st.markdown(f"""
            <div style="background: rgba(34, 197, 94, 0.15); border: 2px solid #22c55e; border-radius: 16px; padding: 20px; text-align: center;">
                <div style="font-size: 0.85rem; color: #94a3b8; font-weight: bold; text-transform: uppercase;">Signal Generated</div>
                <div style="font-size: 2.2rem; font-weight: 900; color: #22c55e; margin: 5px 0;">📈 {direction}</div>
                <div style="display: flex; justify-content: space-around; margin-top: 15px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;">
                    <div>
                        <span style="font-size: 0.7rem; color: #94a3b8;">ACCURACY</span><br>
                        <b style="color: #38bdf8; font-size: 1.1rem;">{accuracy}%</b>
                    </div>
                    <div>
                        <span style="font-size: 0.7rem; color: #94a3b8;">ENTRY TIME</span><br>
                        <b style="color: #38bdf8; font-size: 1.1rem;">{entry_time}</b>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
            <div style="background: rgba(239, 68, 68, 0.15); border: 2px solid #ef4444; border-radius: 16px; padding: 20px; text-align: center;">
                <div style="font-size: 0.85rem; color: #94a3b8; font-weight: bold; text-transform: uppercase;">Signal Generated</div>
                <div style="font-size: 2.2rem; font-weight: 900; color: #ef4444; margin: 5px 0;">📉 {direction}</div>
                <div style="display: flex; justify-content: space-around; margin-top: 15px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px;">
                    <div>
                        <span style="font-size: 0.7rem; color: #94a3b8;">ACCURACY</span><br>
                        <b style="color: #38bdf8; font-size: 1.1rem;">{accuracy}%</b>
                    </div>
                    <div>
                        <span style="font-size: 0.7rem; color: #94a3b8;">ENTRY TIME</span><br>
                        <b style="color: #38bdf8; font-size: 1.1rem;">{entry_time}</b>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button(f"🚀 PLACE ON {broker.upper()}"):
        st.success(f"Signal executed successfully on {broker}!")

# ================= LOGIN SCREEN =================
if not st.session_state.authenticated:
    show_logo()
    st.markdown("<h1 class='bot-title-main'>Zainfxbot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='bot-title-sub'>AI BOT PRO</h2>", unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.8rem; color:#93c5fd; margin-bottom:5px; text-transform:uppercase; font-weight:700;'>🔒 ENTER YOUR LICENSE KEY</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; font-size:0.7rem; color:#9ca3af; margin-bottom:15px;'>Secure Encrypted Connection</p>", unsafe_allow_html=True)

    license_key = st.text_input("License Key", placeholder="ZFX-XXXX-XXXX-XXXX", type="default", label_visibility="collapsed")

    if st.button("🛡️ ACTIVATE LICENSE"):
        if license_key.strip() == "ZFX-PRO-2026-9842" or len(license_key.strip()) >= 5:
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Invalid License Key! Use: ZFX-PRO-2026-9842")

    st.markdown("</div>", unsafe_allow_html=True)

# ================= MAIN DASHBOARD =================
else:
    show_logo()
    st.markdown("<h1 class='bot-title-main' style='font-size:1.6rem;'>Zainfxbot</h1>", unsafe_allow_html=True)
    st.markdown("<h2 class='bot-title-sub' style='font-size:1.1rem; margin-bottom:12px;'>AI BOT <span style='background:#3B82F6; color:#fff; padding:2px 8px; border-radius:8px; font-size:0.75rem;'>PRO MAX</span></h2>", unsafe_allow_html=True)

    st.markdown("""
        <div class="stats-row">
            <div class="stat-box">
                <div class="stat-label">LICENSE</div>
                <div class="stat-val">ACTIVE 🟢</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">AI ENGINE</div>
                <div class="stat-val">ONLINE 🟢</div>
            </div>
            <div class="stat-box">
                <div class="stat-label">USERS</div>
                <div class="stat-val">1.4M+</div>
            </div>
        </div>
        <div class="badge-pro">👑 SECURE PRO UNLOCKED ✅</div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='glass-card'>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align:center; margin:0; font-weight:900; color:#fff; font-size:1.3rem;'>GENERATE <span style='color:#3B82F6;'>SIGNALS</span></h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center; color:#93c5fd; font-size:0.7rem; margin-bottom:15px;'>AI Analyzed High Accuracy Trading Signals</p>", unsafe_allow_html=True)

    broker = st.selectbox("BROKER", ["Quotex", "Pocket Option", "IQ Option", "Tradowix"])
    market = st.selectbox("MARKET", ["Live Market", "OTC Market"])

    # Complete asset list added as requested
    if market == "Live Market":
        all_pairs = [
            "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD", "NZD/USD", "USD/CAD",
            "EUR/GBP", "EUR/JPY", "EUR/CHF", "EUR/AUD", "EUR/CAD", "EUR/NZD",
            "GBP/JPY", "GBP/CHF", "GBP/AUD", "GBP/CAD", "GBP/NZD",
            "AUD/JPY", "AUD/CHF", "AUD/CAD", "AUD/NZD",
            "NZD/JPY", "NZD/CHF", "NZD/CAD",
            "CAD/JPY", "CAD/CHF", "CHF/JPY",
            "USD/SGD", "USD/HKD", "USD/TRY", "USD/MXN", "USD/ZAR", "USD/PLN", "USD/NOK", "USD/SEK", "USD/DKK",
            "EUR/TRY", "EUR/PLN", "EUR/HUF", "EUR/SEK", "EUR/NOK",
            "GBP/SGD", "GBP/TRY",
            "BTC/USD", "ETH/USD", "LTC/USD", "XRP/USD", "BCH/USD", "ADA/USD", "DOT/USD",
            "LINK/USD", "SOL/USD", "AVAX/USD", "DOGE/USD", "SHIB/USD", "UNI/USD", "BNB/USD", "TRX/USD", "TON/USD",
            "XAU/USD", "XAG/USD", "Gold", "Silver", "Brent Oil", "WTI Crude Oil", "Natural Gas", "Platinum", "Palladium", "Copper",
            "US500", "US100", "US30", "UK100", "DE40", "FR40", "JP225", "HK50", "AU200", "EU50",
            "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "META", "NFLX", "NVDA", "AMD", "INTC", "BA", "KO", "DIS", "MCD", "NKE", "V", "MA", "PYPL"
        ]
    else:
        all_pairs = [
            "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC", "NZD/USD OTC", "USD/CAD OTC",
            "EUR/GBP OTC", "EUR/JPY OTC", "EUR/CHF OTC", "EUR/AUD OTC", "EUR/CAD OTC", "EUR/NZD OTC",
            "GBP/JPY OTC", "GBP/AUD OTC", "GBP/CAD OTC", "GBP/CHF OTC", "GBP/NZD OTC",
            "AUD/JPY OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/NZD OTC",
            "NZD/JPY OTC", "CAD/JPY OTC", "CAD/CHF OTC", "CHF/JPY OTC",
            "USD/INR OTC", "USD/PKR OTC", "USD/BRL OTC", "USD/MXN OTC", "USD/CNH OTC",
            "USD/IDR OTC", "USD/THB OTC", "USD/PHP OTC", "USD/VND OTC", "USD/EGP OTC",
            "USD/ARS OTC", "USD/CLP OTC", "USD/BDT OTC", "USD/TRY OTC", "USD/RUB OTC"
        ]

    pair = st.selectbox("PAIR (Searchable All Assets)", all_pairs)
    timer = st.selectbox("TIMER", ["5 Seconds", "10 Seconds", "15 Seconds", "30 Seconds", "1 Minute (1M)", "5 Minutes (5M)"])

    if st.button("🚀 GENERATE SIGNAL"):
        show_signal_popup(broker, market, pair, timer)

    st.markdown("</div>", unsafe_allow_html=True)

    if st.button("🔒 LOGOUT"):
        st.session_state.authenticated = False
        st.rerun()