import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle
import matplotlib.gridspec as gridspec

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="การคำนวณแรงปฏิกิริยาเสาเข็ม (เยื้องศูนย์)",
    page_icon="🏗️",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@300;400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');

html, body, [class*="css"] {
    font-family: 'Sarabun', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem 2.5rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.main-header h1 {
    color: #e2c97e;
    font-size: 1.8rem;
    font-weight: 700;
    margin: 0 0 0.3rem 0;
    letter-spacing: -0.5px;
}
.main-header p {
    color: rgba(255,255,255,0.55);
    font-size: 0.95rem;
    margin: 0;
}

.section-card {
    background: #ffffff;
    border: 1.5px solid #e8ecf4;
    border-radius: 12px;
    padding: 1.5rem 1.8rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.section-title {
    font-size: 1rem;
    font-weight: 700;
    color: #0f3460;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2.5px solid #e2c97e;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.formula-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 2px solid #16a34a;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    margin: 1rem 0;
}
.formula-box .formula-text {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.1rem;
    color: #15803d;
    font-weight: 600;
}

.result-card {
    background: linear-gradient(135deg, #0f3460, #16213e);
    border-radius: 12px;
    padding: 1.5rem;
    color: white;
    margin-bottom: 1rem;
}
.result-card .result-label {
    font-size: 0.85rem;
    color: rgba(255,255,255,0.6);
    margin-bottom: 0.3rem;
}
.result-card .result-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 700;
    color: #e2c97e;
}
.result-card .result-unit {
    font-size: 0.9rem;
    color: rgba(255,255,255,0.5);
    margin-left: 0.3rem;
}

.pile-max {
    background: linear-gradient(135deg, #7f1d1d, #991b1b) !important;
}
.pile-min {
    background: linear-gradient(135deg, #14532d, #15803d) !important;
}

.warning-box {
    background: #fef3c7;
    border: 1.5px solid #f59e0b;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #92400e;
    font-size: 0.9rem;
}
.ok-box {
    background: #dcfce7;
    border: 1.5px solid #16a34a;
    border-radius: 8px;
    padding: 0.8rem 1rem;
    color: #14532d;
    font-size: 0.9rem;
}

.step-badge {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 28px;
    height: 28px;
    background: #e2c97e;
    color: #1a1a2e;
    border-radius: 50%;
    font-weight: 700;
    font-size: 0.85rem;
    margin-right: 0.5rem;
    flex-shrink: 0;
}

.stDataFrame { border-radius: 8px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏗️ การคำนวณแรงปฏิกิริยาเสาเข็ม — เยื้องศูนย์แบบสมมาตร</h1>
    <p>Eccentric Pile Foundation Calculator · Symmetric Pile Group (2-axis eccentricity)</p>
</div>
""", unsafe_allow_html=True)

# ─── Formula display ─────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-title"><span class="step-badge">สูตร</span> สูตรที่ใช้คำนวณ</div>
    <div class="formula-box">
        <div class="formula-text">Pᵢ = (Q/n)  +  (Mᵧ·xᵢ / Σx²)  +  (Mₓ·yᵢ / Σy²)</div>
    </div>
    <p style="color:#555; font-size:0.9rem; margin:0.5rem 0 0;">
        โดย: <b>Q</b> = แรงกระทำแนวดิ่งรวม, <b>n</b> = จำนวนเสาเข็ม,
        <b>Mₓ, Mᵧ</b> = โมเมนต์รอบแกน X, Y ที่ Centroid ใหม่,
        <b>xᵢ, yᵢ</b> = ระยะเสาเข็มจาก Centroid (C.G. ใหม่)
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar inputs ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ ข้อมูลนำเข้า")
    st.markdown("---")

    st.markdown("**📦 แรงกระทำ (Loads)**")
    Q = st.number_input("Q — แรงแนวดิ่งรวม (ตัน)", min_value=0.0, value=500.0, step=10.0, format="%.2f")
    Mx = st.number_input("Mₓ — โมเมนต์รอบแกน X (ตัน·ม.)", value=80.0, step=5.0, format="%.2f")
    My = st.number_input("Mᵧ — โมเมนต์รอบแกน Y (ตัน·ม.)", value=60.0, step=5.0, format="%.2f")

    st.markdown("---")
    st.markdown("**🔩 ความสามารถรับแรงเสาเข็ม**")
    P_allow = st.number_input("Pₐₗₗₒw — แรงกดอนุญาต (ตัน/ต้น)", min_value=1.0, value=120.0, step=5.0, format="%.2f")
    P_tension = st.number_input("Pₜₑₙₛᵢₒₙ — แรงดึงอนุญาต (ตัน/ต้น)", min_value=0.0, value=30.0, step=5.0, format="%.2f")

    st.markdown("---")
    st.markdown("**📍 ตำแหน่งเสาเข็ม (จาก Centroid)**")
    st.caption("กรอก x, y ของแต่ละต้น (หน่วย: เมตร)")

    n_piles = st.number_input("จำนวนเสาเข็ม (n)", min_value=2, max_value=20, value=4, step=1)

    pile_data = []
    for i in range(n_piles):
        col1, col2 = st.columns(2)
        with col1:
            xi = st.number_input(f"x{i+1}", value=float([-1.5, 1.5, -1.5, 1.5, -1.5, 1.5, 0.0, 0.0][i % 8]),
                                  step=0.25, key=f"x_{i}", format="%.2f")
        with col2:
            yi = st.number_input(f"y{i+1}", value=float([-1.5, -1.5, 1.5, 1.5, 0.0, 0.0, -1.5, 1.5][i % 8]),
                                  step=0.25, key=f"y_{i}", format="%.2f")
        pile_data.append({"Pile": f"pile_{i+1}", "x (m)": xi, "y (m)": yi})

# ─── Calculation ─────────────────────────────────────────────────────────────
df = pd.DataFrame(pile_data)
df["x²"] = df["x (m)"] ** 2
df["y²"] = df["y (m)"] ** 2

sum_x2 = df["x²"].sum()
sum_y2 = df["y²"].sum()
n = len(df)

Q_per_pile = Q / n

df["Pᵢ (ตัน)"] = (
    Q_per_pile
    + (My * df["x (m)"] / sum_x2 if sum_x2 != 0 else 0)
    + (Mx * df["y (m)"] / sum_y2 if sum_y2 != 0 else 0)
)

P_max = df["Pᵢ (ตัน)"].max()
P_min = df["Pᵢ (ตัน)"].min()
pile_max = df.loc[df["Pᵢ (ตัน)"].idxmax(), "Pile"]
pile_min = df.loc[df["Pᵢ (ตัน)"].idxmin(), "Pile"]

# ─── Layout ─────────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

with col_left:
    st.markdown("""
    <div class="section-card">
        <div class="section-title"><span class="step-badge">1</span> ตารางคำนวณ</div>
    """, unsafe_allow_html=True)

    # Totals row
    totals = pd.DataFrame([{
        "Pile": "ผลรวม (Σ)",
        "x (m)": "",
        "y (m)": "",
        "x²": f"{sum_x2:.4f}",
        "y²": f"{sum_y2:.4f}",
        "Pᵢ (ตัน)": f"{df['Pᵢ (ตัน)'].sum():.4f}",
    }])

    display_df = df.copy()
    display_df["x²"] = display_df["x²"].map("{:.4f}".format)
    display_df["y²"] = display_df["y²"].map("{:.4f}".format)
    display_df["Pᵢ (ตัน)"] = display_df["Pᵢ (ตัน)"].map("{:.4f}".format)

    st.dataframe(display_df, use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="background:#f0f4ff; border-radius:8px; padding:0.8rem 1rem; font-family:'IBM Plex Mono',monospace; font-size:0.88rem; color:#1e3a5f; margin-top:0.5rem;">
        Σx² = {sum_x2:.4f} m² &nbsp;|&nbsp; Σy² = {sum_y2:.4f} m² &nbsp;|&nbsp; n = {n} ต้น
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # Calculation steps
    st.markdown("""
    <div class="section-card">
        <div class="section-title"><span class="step-badge">2</span> ขั้นตอนการคำนวณ</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="font-family:'IBM Plex Mono',monospace; font-size:0.9rem; line-height:2; color:#1e293b; background:#f8fafc; border-radius:8px; padding:1rem 1.2rem;">
        Q/n = {Q:.2f} / {n} = <b>{Q_per_pile:.4f}</b> ตัน<br>
        Mᵧ/Σx² = {My:.2f} / {sum_x2:.4f} = <b>{My/sum_x2:.4f}</b> (ถ้า Σx²≠0)<br>
        Mₓ/Σy² = {Mx:.2f} / {sum_y2:.4f} = <b>{Mx/sum_y2:.4f}</b> (ถ้า Σy²≠0)<br>
        <br>
        Pᵢ = {Q_per_pile:.4f} + ({My/sum_x2:.4f})·xᵢ + ({Mx/sum_y2:.4f})·yᵢ
    </div>
    """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col_right:
    # Result summary
    st.markdown("""
    <div class="section-card">
        <div class="section-title"><span class="step-badge">3</span> ผลการคำนวณ</div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="result-card pile-max">
        <div class="result-label">⬆ แรงกด max ({pile_max})</div>
        <div class="result-value">{P_max:.2f}<span class="result-unit">ตัน</span></div>
    </div>
    <div class="result-card pile-min">
        <div class="result-label">⬇ แรงกด min / แรงดึง ({pile_min})</div>
        <div class="result-value">{P_min:.2f}<span class="result-unit">ตัน</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Safety check
    if P_max <= P_allow:
        st.markdown(f"""
        <div class="ok-box">✅ <b>ผ่าน:</b> P_max = {P_max:.2f} ≤ P_allow = {P_allow:.2f} ตัน</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box">⚠️ <b>ไม่ผ่าน:</b> P_max = {P_max:.2f} > P_allow = {P_allow:.2f} ตัน — ต้องเพิ่มเสาเข็มหรือเพิ่มขนาด</div>
        """, unsafe_allow_html=True)

    if P_min >= 0:
        st.markdown(f"""
        <div class="ok-box" style="margin-top:0.5rem;">✅ <b>ไม่มีแรงดึง:</b> P_min = {P_min:.2f} ≥ 0</div>
        """, unsafe_allow_html=True)
    elif abs(P_min) <= P_tension:
        st.markdown(f"""
        <div class="ok-box" style="margin-top:0.5rem;">✅ <b>แรงดึงผ่าน:</b> |P_min| = {abs(P_min):.2f} ≤ P_tension = {P_tension:.2f} ตัน</div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="warning-box" style="margin-top:0.5rem;">⚠️ <b>แรงดึงเกิน:</b> |P_min| = {abs(P_min):.2f} > P_tension = {P_tension:.2f} ตัน</div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Pile layout diagram
    st.markdown("""
    <div class="section-card">
        <div class="section-title"><span class="step-badge">4</span> แผนผังเสาเข็ม</div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots(figsize=(5, 5))
    fig.patch.set_facecolor('#f8fafc')
    ax.set_facecolor('#f8fafc')

    pi_values = df["Pᵢ (ตัน)"].values
    norm = plt.Normalize(pi_values.min(), pi_values.max())
    cmap = plt.cm.RdYlGn_r

    for _, row in df.iterrows():
        xi, yi, pi = row["x (m)"], row["y (m)"], row["Pᵢ (ตัน)"]
        color = cmap(norm(pi))
        circle = Circle((xi, yi), 0.18, color=color, zorder=3, ec='#333', lw=1.2)
        ax.add_patch(circle)
        ax.text(xi, yi, f"{pi:.1f}", ha='center', va='center', fontsize=7.5,
                fontweight='bold', color='white', zorder=4)
        ax.text(xi, yi - 0.35, row["Pile"], ha='center', va='top',
                fontsize=7, color='#555')

    # Centroid marker
    ax.plot(0, 0, 'k+', markersize=14, markeredgewidth=2, zorder=5)
    ax.text(0.05, 0.05, 'C.G.', fontsize=8, color='#333')

    all_x = df["x (m)"].tolist() + [0]
    all_y = df["y (m)"].tolist() + [0]
    pad = 0.7
    ax.set_xlim(min(all_x) - pad, max(all_x) + pad)
    ax.set_ylim(min(all_y) - pad, max(all_y) + pad)
    ax.set_aspect('equal')
    ax.axhline(0, color='#999', lw=0.8, ls='--')
    ax.axvline(0, color='#999', lw=0.8, ls='--')
    ax.set_xlabel('x (m)', fontsize=9)
    ax.set_ylabel('y (m)', fontsize=9)
    ax.set_title('แผนผังตำแหน่งเสาเข็ม\n(สีแดง = แรงมาก, สีเขียว = แรงน้อย)', fontsize=9)
    ax.grid(True, alpha=0.3, color='#ccc')

    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    plt.colorbar(sm, ax=ax, label='Pᵢ (ตัน)', shrink=0.8)

    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()

    st.markdown("</div>", unsafe_allow_html=True)

# ─── Bar chart ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-title"><span class="step-badge">5</span> กราฟแรงปฏิกิริยาแต่ละต้น</div>
""", unsafe_allow_html=True)

fig2, ax2 = plt.subplots(figsize=(max(8, n * 1.2), 4))
fig2.patch.set_facecolor('#f8fafc')
ax2.set_facecolor('#f8fafc')

colors = ['#dc2626' if p == P_max else '#16a34a' if p == P_min else '#0f3460'
          for p in df["Pᵢ (ตัน)"]]
bars = ax2.bar(df["Pile"], df["Pᵢ (ตัน)"], color=colors, edgecolor='white',
               linewidth=1.5, width=0.6, zorder=3)

ax2.axhline(P_allow, color='#f59e0b', lw=1.5, ls='--', label=f'P_allow = {P_allow:.1f} ตัน')
ax2.axhline(0, color='#333', lw=1.0)
if P_tension > 0:
    ax2.axhline(-P_tension, color='#7c3aed', lw=1.5, ls='--', label=f'P_tension = -{P_tension:.1f} ตัน')

for bar, val in zip(bars, df["Pᵢ (ตัน)"]):
    ax2.text(bar.get_x() + bar.get_width() / 2,
             bar.get_height() + (0.5 if val >= 0 else -1.5),
             f'{val:.2f}', ha='center', va='bottom' if val >= 0 else 'top',
             fontsize=8.5, fontweight='bold', color='#1e293b')

ax2.set_ylabel('แรงปฏิกิริยา Pᵢ (ตัน)', fontsize=10)
ax2.set_title('แรงปฏิกิริยาเสาเข็มแต่ละต้น', fontsize=11, fontweight='bold')
ax2.legend(fontsize=9)
ax2.grid(axis='y', alpha=0.3, color='#ccc', zorder=0)
ax2.set_axisbelow(True)

plt.tight_layout()
st.pyplot(fig2, use_container_width=True)
plt.close()

st.markdown("</div>", unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:2rem;">
    Pile Foundation Calculator · สูตร Pᵢ = Q/n + Mᵧ·x/Σx² + Mₓ·y/Σy² · KMUTNB
</div>
""", unsafe_allow_html=True)
