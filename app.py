import streamlit as pd_stream
import plotly.graph_objects as pgo
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# 1. Page Configuration & Theme Initialization
pd_stream.set_page_config(
    page_title="US Treasury Yield Curve Engine",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling for Elite Visual Separation
pd_stream.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1, h2, h3 { color: #ffffff; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    div[data-testid="stMetricValue"] { font-size: 24px !important; }
    div[data-testid="stMetricLabel"] { font-size: 13px !important; white-space: nowrap !important; }
    .reportview-container .main .block-container { padding-top: 2rem; }
    .analysis-card {
        background-color: #161b22; 
        border: 1px solid #30363d; 
        padding: 20px; 
        border-radius: 8px;
        margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 2. Dynamic Macro-Data Generation Engine
@pd_stream.cache_data
def generate_yield_curve_data():
    np.random.seed(42)
    maturities_months = np.array([1, 3, 6, 12, 24, 36, 60, 84, 120, 240, 360]) # 1M to 30Y
    maturity_labels = ['1M', '3M', '6M', '1Y', '2Y', '3Y', '5Y', '7Y', '10Y', '20Y', '30Y']
    
    start_date = datetime(2024, 1, 1)
    dates = [start_date + timedelta(days=x*7) for x in range(150)] # Weekly data
    
    records = []
    
    for i, dt in enumerate(dates):
        if i < 40:
            base_short = 2.5 + np.sin(i/10) * 0.3
            base_long = 4.5 + np.cos(i/15) * 0.2
        elif i < 100:
            base_short = 5.2 + np.sin(i/12) * 0.2
            base_long = 3.8 - np.cos(i/20) * 0.3
        else:
            base_short = 3.5 + np.sin(i/15) * 0.1
            base_long = 3.8 + np.sin(i/25) * 0.15
            
        yields = []
        for m in maturities_months:
            weight = (m - 1) / (360 - 1)
            noise = np.random.normal(0, 0.04)
            current_yield = base_short + (base_long - base_short) * np.sqrt(weight) + noise
            yields.append(round(max(0.1, current_yield), 3))
            
        records.append({
            'Date': dt.strftime('%Y-%m-%d'),
            'Yields': yields,
            'Spread_10Y_2Y': round(yields[8] - yields[4], 3)
        })
        
    return dates, maturity_labels, records

dates, maturity_labels, records = generate_yield_curve_data()

# 3. Sidebar Control Interface
pd_stream.sidebar.title("Configuration Deck")
pd_stream.sidebar.markdown("Adjust structural parameters to isolate macro-finance insights.")

selected_date_str = pd_stream.sidebar.select_slider(
    "Select Historical Timeline Environment:",
    options=[r['Date'] for r in records],
    value=records[60]['Date']
)

current_record = next(r for r in records if r['Date'] == selected_date_str)
current_yields = current_record['Yields']
current_spread = current_record['Spread_10Y_2Y']

pd_stream.sidebar.markdown("---")
pd_stream.sidebar.markdown("### Architectural Specifications")
pd_stream.sidebar.info(
    "This node processes high-dimensional bond yield maturities using multi-axis vector spaces to predict capital allocation trends."
)

# 4. Core Header Block
pd_stream.title("📊 US Treasury Yield Curve Intelligence Workspace")
pd_stream.markdown(f"**Target Microeconomic Environment Context Active:** `Timeline Matrix Run: {selected_date_str}`")
pd_stream.markdown("---")

# 5. Optimized Financial Metric Indicators (Adjusted spacing to prevent clipping)
col1, col2, col3, col4 = pd_stream.columns([1.1, 1.1, 1.1, 1.3])

with col1:
    pd_stream.metric("US Treasury 3-Month", f"{current_yields[1]}%", help="Short-term target.")
with col2:
    pd_stream.metric("US Treasury 10-Year", f"{current_yields[8]}%", help="Long-term growth marker.")
with col3:
    delta_color = "inverse" if current_spread < 0 else "normal"
    pd_stream.metric("10Y - 2Y Spread", f"{current_spread}%", delta=f"{current_spread}% Inversion" if current_spread < 0 else "Normal Structure", delta_color=delta_color)
with col4:
    status_label = "🔴 CRITICAL INVERSION" if current_spread < -0.5 else ("     🟡 COMPRESSED" if current_spread < 0 else "     🟢 EQUILIBRIUM")
    pd_stream.metric("Curve Structural Health Indicator", status_label)

pd_stream.markdown("---")

# 6. Primary Visual Graphic Generation
col_left, col_right = pd_stream.columns([1.3, 1.2])

with col_left:
    pd_stream.subheader("Interactive Term Structure Analysis")
    
    fig = pgo.Figure()
    fig.add_trace(pgo.Scatter(
        x=maturity_labels,
        y=current_yields,
        mode='lines+markers',
        name='Active Curve Frame',
        line=dict(color='#00ffcc', width=4),
        marker=dict(size=10, color='#ffffff', line=dict(width=2, color='#00ffcc')),
        hovertemplate='Maturity: %{x}<br>Sovereign Yield: %{y}%<extra></extra>'
    ))
    
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=40, r=40, t=20, b=40),
        xaxis=dict(title="Maturity Spectrum", gridcolor='#21262d', showline=True, linecolor='#30363d'),
        yaxis=dict(title="Yield Rate Percentage (%)", gridcolor='#21262d', showline=True, linecolor='#30363d', range=[0, 6.5]),
        hovermode="x unified"
    )
    
    pd_stream.plotly_chart(fig, use_container_width=True)

with col_right:
    pd_stream.subheader("Macro-Finance Analytical Breakdown")
    
    if current_spread < 0:
        pd_stream.markdown(f"""
        <div class="analysis-card" style="border-left: 5px solid #ff4b4b;">
            <h3 style="color: #ff4b4b; margin-top:0;">Curve Status: Inverted Spectrum ({current_spread}%)</h3>
            <p><strong>Economic Interpretation:</strong><br>
            Short-term sovereign yields higher than long-term yields indicate aggressive restrictive monetary intervention by the Federal Reserve.</p>
            <p><strong>Banking Sector Risk Multipliers:</strong></p>
            <ul>
                <li><strong>Net Interest Margin Compression:</strong> Banks borrow on short-term rates and lend on long-term rates. An inverted matrix compresses profitability thresholds.</li>
                <li><strong>Credit Allocation Contraction:</strong> Structural banking stress drops aggregate loan volumes, triggering capital market cooling trends.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    else:
        pd_stream.markdown(f"""
        <div class="analysis-card" style="border-left: 5px solid #00cc66;">
            <h3 style="color: #00cc66; margin-top:0;">Curve Status: Upward Sloping Equilibrium (+{current_spread}%)</h3>
            <p><strong>Economic Interpretation:</strong><br>
            A standard upward-sloping model reflects healthy systemic risk appetites. Investors demand a higher premium for locking liquidity over long durations.</p>
            <p><strong>Banking Sector Risk Multipliers:</strong></p>
            <ul>
                <li><strong>Optimized Credit Spreads:</strong> Financial institutions capture strong arbitrage margins between short-end deposits and long-end commercial financing lending lines.</li>
                <li><strong>Capital Expansion:</strong> Normal yield curves accelerate standard corporate expansion and lower overall credit defaults.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

pd_stream.markdown("---")
pd_stream.caption("Designed for Academic Portfolio Validation Architecture — Developed via automated AI compilation routines.")


