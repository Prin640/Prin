import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

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
html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }
.main-header {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    padding: 2rem 2.5rem; border-radius: 16px; margin-bottom: 2rem;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}
.main-header h1 { color: #e2c97e; font-size: 1.8rem; font-weight: 700; margin: 0 0 0.3rem 0; }
.main-header p  { color: rgba(255,255,255,0.55); font-size: 0.95rem; margin: 0; }
.section-card {
    background: #ffffff; border: 1.5px solid #e8ecf4; border-radius: 12px;
    padding: 1.5rem 1.8rem; margin-bottom: 1.2rem;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
}
.section-title {
    font-size: 1rem; font-weight: 700; color: #0f3460;
    margin-bottom: 1rem; padding-bottom: 0.5rem;
    border-bottom: 2.5px solid #e2c97e;
}
.formula-box {
    background: linear-gradient(135deg, #f0fdf4, #dcfce7);
    border: 2px solid #16a34a; border-radius: 12px;
    padding: 1.2rem 1.5rem; text-align: center; margin: 1rem 0;
}
.formula-text {
    font-family: 'IBM Plex Mono', monospace; font-size: 1.15rem;
    color: #15803d; font-weight: 600;
}
.result-card {
    background: linear-gradient(135deg, #0f3460, #16213e);
    border-radius: 12px; padding: 1.2rem 1.5rem; color: white; margin-bottom: 0.8rem;
}
.result-label { font-size: 0.85rem; color: rgba(255,255,255,0.6); margin-bottom: 0.3rem; }
.result-value { font-family: 'IBM Plex Mono', monospace; font-size: 1.5rem; font-weight: 700; color: #e2c97e; }
.result-unit  { font-size: 0.9rem; color: rgba(255,255,255,0.5); margin-left: 0.3rem; }
.pile-max { background: linear-gradient(135deg, #7f1d1d, #991b1b) !important; }
.pile-min { background: linear-gradient(135deg, #14532d, #15803d) !important; }
.warning-box {
    background: #fef3c7; border: 1.5px solid #f59e0b; border-radius: 8px;
    padding: 0.8rem 1rem; color: #92400e; font-size: 0.9rem; margin-top: 0.5rem;
}
.ok-box {
    background: #dcfce7; border: 1.5px solid #16a34a; border-radius: 8px;
    padding: 0.8rem 1rem; color: #14532d; font-size: 0.9rem; margin-top: 0.5rem;
}
.calc-box {
    font-family: 'IBM Plex Mono', monospace; font-size: 0.9rem;
    line-height: 2; color: #1e293b; background: #f8fafc;
    border-radius: 8px; padding: 1rem 1.2rem;
}
</style>
""", unsafe_allow_html=True)

# ─── Header ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <h1>🏗️ การคำนวณแรงปฏิกิริยาเสาเข็ม — เยื้องศูนย์แบบสมมาตร</h1>
    <p>Eccentric Pile Foundation Calculator · Symmetric Pile Group (2-axis eccentricity)</p>
</div>
""", unsafe_allow_html=True)

# ─── Formula ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="section-card">
    <div class="section-title">📐 สูตรที่ใช้คำนวณ</div>
    <div class="formula-box">
        <div class="formula-text">Pᵢ = (Q / n)  +  (Mᵧ · xᵢ / Σx²)  +  (Mₓ · yᵢ / Σy²)</div>
    </div>
    <p style="color:#555; font-size:0.9rem; margin:0.5rem 0 0;">
        <b>Q</b> = แรงกระทำแนวดิ่งรวม &nbsp;|&nbsp;
        <b>n</b> = จำนวนเสาเข็ม &nbsp;|&nbsp;
        <b>Mₓ, Mᵧ</b> = โมเมนต์รอบแกน X, Y ที่ Centroid ใหม่ &nbsp;|&nbsp;
        <b>xᵢ, yᵢ</b> = ระยะเสาเข็มจาก C.G. ใหม่
    </p>
</div>
""", unsafe_allow_html=True)

# ─── Sidebar inputs ──────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ ข้อมูลนำเข้า")
    st.markdown("---")
    st.markdown("**📦 แรงกระทำ (Loads)**")
    Q         = st.number_input("Q — แรงแนวดิ่งรวม (ตัน)",          min_value=0.0, value=500.0, step=10.0, format="%.2f")
    Mx        = st.number_input("Mₓ — โมเมนต์รอบแกน X (ตัน·ม.)",   value=80.0,  step=5.0,  format="%.2f")
    My        = st.number_input("Mᵧ — โมเมนต์รอบแกน Y (ตัน·ม.)",   value=60.0,  step=5.0,  format="%.2f")
    st.markdown("---")
    st.markdown("**🔩 กำลังรับแรงอนุญาต**")
    P_allow   = st.number_input("Pₐₗₗₒw — แรงกดอนุญาต (ตัน/ต้น)",    min_value=1.0, value=120.0, step=5.0, format="%.2f")
    P_tension = st.number_input("Pₜₑₙₛᵢₒₙ — แรงดึงอนุญาต (ตัน/ต้น)", min_value=0.0, value=30.0,  step=5.0, format="%.2f")
    st.markdown("---")
    st.markdown("**📍 ตำแหน่งเสาเข็ม (จาก Centroid)**")
    st.caption("กรอก x, y ของแต่ละต้น (หน่วย: เมตร)")

    default_x = [-1.5,  1.5, -1.5,  1.5, -1.5,  1.5,  0.0,  0.0,
                  2.0, -2.0,  2.0, -2.0,  2.0, -2.0,  0.0,  0.0,
                  3.0, -3.0,  0.0,  0.0]
    default_y = [-1.5, -1.5,  1.5,  1.5,  0.0,  0.0, -1.5,  1.5,
                 -2.0, -2.0,  2.0,  2.0,  0.0,  0.0, -2.0,  2.0,
                  0.0,  0.0,  3.0, -3.0]

    n_piles = st.number_input("จำนวนเสาเข็ม (n)", min_value=2, max_value=20, value=4, step=1)

    pile_data = []
    for i in range(n_piles):
        c1, c2 = st.columns(2)
        with c1:
            xi = st.number_input(f"x{i+1} (m)", value=float(default_x[i % 20]),
                                  step=0.25, key=f"x_{i}", format="%.2f")
        with c2:
            yi = st.number_input(f"y{i+1} (m)", value=float(default_y[i % 20]),
                                  step=0.25, key=f"y_{i}", format="%.2f")
        pile_data.append({"Pile": f"pile_{i+1}", "x (m)": xi, "y (m)": yi})

# ─── Calculation ─────────────────────────────────────────────────────────────
df = pd.DataFrame(pile_data)
df["x²"] = df["x (m)"] ** 2
df["y²"] = df["y (m)"] ** 2

n       = len(df)
sum_x2  = df["x²"].sum()
sum_y2  = df["y²"].sum()
Q_n     = Q / n
coef_x  = My / sum_x2 if sum_x2 != 0 else 0.0
coef_y  = Mx / sum_y2 if sum_y2 != 0 else 0.0

df["Pᵢ (ตัน)"] = Q_n + coef_x * df["x (m)"] + coef_y * df["y (m)"]

P_max    = df["Pᵢ (ตัน)"].max()
P_min    = df["Pᵢ (ตัน)"].min()
pile_max = df.loc[df["Pᵢ (ตัน)"].idxmax(), "Pile"]
pile_min = df.loc[df["Pᵢ (ตัน)"].idxmin(), "Pile"]

# ─── Main layout ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns([3, 2])

# ── LEFT ──────────────────────────────────────────────────────────────────────
with col_left:
    # Table
    st.markdown('<div class="section-card"><div class="section-title">📊 ตารางคำนวณ</div>', unsafe_allow_html=True)

    disp = df.copy()
    disp["x (m)"]    = disp["x (m)"].map("{:.2f}".format)
    disp["y (m)"]    = disp["y (m)"].map("{:.2f}".format)
    disp["x²"]       = disp["x²"].map("{:.4f}".format)
    disp["y²"]       = disp["y²"].map("{:.4f}".format)
    disp["Pᵢ (ตัน)"] = disp["Pᵢ (ตัน)"].map("{:.4f}".format)

    summary = pd.DataFrame([{
        "Pile": "Σ (ผลรวม)", "x (m)": "-", "y (m)": "-",
        "x²": f"{sum_x2:.4f}", "y²": f"{sum_y2:.4f}",
        "Pᵢ (ตัน)": f"{df['Pᵢ (ตัน)'].sum():.4f}",
    }])
    st.dataframe(pd.concat([disp, summary], ignore_index=True), use_container_width=True, hide_index=True)

    st.markdown(f"""
    <div style="background:#f0f4ff; border-radius:8px; padding:0.7rem 1rem;
                font-family:'IBM Plex Mono',monospace; font-size:0.85rem; color:#1e3a5f; margin-top:0.5rem;">
        Σx² = {sum_x2:.4f} m² &nbsp;|&nbsp; Σy² = {sum_y2:.4f} m² &nbsp;|&nbsp; n = {n} ต้น
    </div></div>
    """, unsafe_allow_html=True)

    # Steps
    st.markdown('<div class="section-card"><div class="section-title">🔢 ขั้นตอนการคำนวณ</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="calc-box">
        Q/n &nbsp;&nbsp;&nbsp;&nbsp;= {Q:.2f} / {n} = <b>{Q_n:.4f}</b> ตัน<br>
        Mᵧ/Σx² = {My:.2f} / {sum_x2:.4f} = <b>{coef_x:.4f}</b> ตัน/ม.<br>
        Mₓ/Σy² = {Mx:.2f} / {sum_y2:.4f} = <b>{coef_y:.4f}</b> ตัน/ม.<br><br>
        Pᵢ = <b>{Q_n:.4f}</b> + (<b>{coef_x:.4f}</b>)·xᵢ + (<b>{coef_y:.4f}</b>)·yᵢ
    </div></div>
    """, unsafe_allow_html=True)

# ── RIGHT ─────────────────────────────────────────────────────────────────────
with col_right:
    # Results
    st.markdown('<div class="section-card"><div class="section-title">📋 ผลการคำนวณ</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="result-card pile-max">
        <div class="result-label">⬆ แรงกดสูงสุด ({pile_max})</div>
        <div class="result-value">{P_max:.3f}<span class="result-unit">ตัน</span></div>
    </div>
    <div class="result-card pile-min">
        <div class="result-label">⬇ แรงกดต่ำสุด ({pile_min})</div>
        <div class="result-value">{P_min:.3f}<span class="result-unit">ตัน</span></div>
    </div>
    """, unsafe_allow_html=True)

    if P_max <= P_allow:
        st.markdown(f'<div class="ok-box">✅ P_max = {P_max:.2f} ≤ P_allow = {P_allow:.2f} ตัน → <b>ผ่าน</b></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warning-box">⚠️ P_max = {P_max:.2f} > P_allow = {P_allow:.2f} ตัน → <b>ไม่ผ่าน</b></div>', unsafe_allow_html=True)

    if P_min >= 0:
        st.markdown(f'<div class="ok-box">✅ ไม่มีแรงดึง (P_min = {P_min:.2f} ≥ 0)</div>', unsafe_allow_html=True)
    elif abs(P_min) <= P_tension:
        st.markdown(f'<div class="ok-box">✅ |P_min| = {abs(P_min):.2f} ≤ P_tension = {P_tension:.2f} ตัน → <b>ผ่าน</b></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warning-box">⚠️ |P_min| = {abs(P_min):.2f} > P_tension = {P_tension:.2f} ตัน → <b>ไม่ผ่าน</b></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # Pile plan diagram (Plotly)
    st.markdown('<div class="section-card"><div class="section-title">🗺️ แผนผังเสาเข็ม</div>', unsafe_allow_html=True)

    pi_vals  = df["Pᵢ (ตัน)"].values
    vmin, vmax = pi_vals.min(), pi_vals.max()

    def get_color(p):
        if vmax == vmin:
            return "rgb(15,52,96)"
        t = (p - vmin) / (vmax - vmin)
        r = int(220 * t + 22 * (1 - t))
        g = int(38  * t + 163 * (1 - t))
        b = int(38  * t + 74  * (1 - t))
        return f"rgb({r},{g},{b})"

    fig_map = go.Figure()
    for _, row in df.iterrows():
        xi, yi, pi = row["x (m)"], row["y (m)"], row["Pᵢ (ตัน)"]
        fig_map.add_trace(go.Scatter(
            x=[xi], y=[yi], mode="markers+text",
            marker=dict(size=42, color=get_color(pi), line=dict(color="white", width=2)),
            text=[f"{pi:.1f}"], textposition="middle center",
            textfont=dict(color="white", size=10, family="IBM Plex Mono"),
            name=row["Pile"],
            hovertemplate=f"<b>{row['Pile']}</b><br>x={xi:.2f} m<br>y={yi:.2f} m<br>Pᵢ = {pi:.3f} ตัน<extra></extra>",
        ))
        fig_map.add_annotation(x=xi, y=yi - 0.38, text=row["Pile"],
                               showarrow=False, font=dict(size=9, color="#555"))

    fig_map.add_trace(go.Scatter(
        x=[0], y=[0], mode="markers+text",
        marker=dict(size=12, symbol="cross", color="black"),
        text=["C.G."], textposition="top right",
        textfont=dict(size=9, color="#333"),
        showlegend=False, hoverinfo="skip",
    ))

    pad = 1.0
    xs, ys = df["x (m)"].tolist(), df["y (m)"].tolist()
    fig_map.update_layout(
        height=360, showlegend=False,
        xaxis=dict(title="x (m)", zeroline=True, zerolinecolor="#bbb",
                   range=[min(xs + [0]) - pad, max(xs + [0]) + pad], gridcolor="#e5e7eb"),
        yaxis=dict(title="y (m)", zeroline=True, zerolinecolor="#bbb",
                   range=[min(ys + [0]) - pad, max(ys + [0]) + pad],
                   scaleanchor="x", scaleratio=1, gridcolor="#e5e7eb"),
        paper_bgcolor="white", plot_bgcolor="#f8fafc",
        margin=dict(l=40, r=20, t=10, b=40),
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ─── Bar chart ───────────────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-title">📊 กราฟแรงปฏิกิริยาแต่ละต้น</div>', unsafe_allow_html=True)

bar_colors = ["#dc2626" if p == P_max else "#16a34a" if p == P_min else "#0f3460"
              for p in df["Pᵢ (ตัน)"]]

fig_bar = go.Figure()
fig_bar.add_trace(go.Bar(
    x=df["Pile"], y=df["Pᵢ (ตัน)"],
    marker_color=bar_colors, marker_line_color="white", marker_line_width=1.5,
    text=df["Pᵢ (ตัน)"].map("{:.2f}".format), textposition="outside",
    hovertemplate="<b>%{x}</b><br>Pᵢ = %{y:.3f} ตัน<extra></extra>",
))
fig_bar.add_hline(y=P_allow, line_dash="dash", line_color="#f59e0b", line_width=2,
                  annotation_text=f"P_allow = {P_allow:.1f} t", annotation_position="top right")
fig_bar.add_hline(y=0, line_color="#333", line_width=1)
if P_tension > 0:
    fig_bar.add_hline(y=-P_tension, line_dash="dash", line_color="#7c3aed", line_width=2,
                      annotation_text=f"-P_tension = -{P_tension:.1f} t", annotation_position="bottom right")
fig_bar.update_layout(
    height=360, showlegend=False,
    yaxis=dict(title="Pᵢ (ตัน)", gridcolor="#e5e7eb"),
    xaxis=dict(title="เสาเข็ม"),
    paper_bgcolor="white", plot_bgcolor="#f8fafc",
    margin=dict(l=50, r=50, t=20, b=40),
)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; color:#aaa; font-size:0.8rem; margin-top:1rem; padding-bottom:2rem;">
    Pile Foundation Calculator · Pᵢ = Q/n + Mᵧ·x/Σx² + Mₓ·y/Σy²
</div>
""", unsafe_allow_html=True)
