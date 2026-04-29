# ============================================================
#  การคำนวณแรงปฏิกิริยาเสาเข็ม — เยื้องศูนย์แบบสมมาตร
#  Library: streamlit, pandas, numpy  (ไม่ต้องติดตั้งเพิ่ม)
#  requirements.txt: streamlit / pandas / numpy
# ============================================================
import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="แรงปฏิกิริยาเสาเข็ม (เยื้องศูนย์)",
    page_icon="🏗️",
    layout="wide",
)

# ── CSS ──────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&family=IBM+Plex+Mono:wght@400;600&display=swap');
html, body, [class*="css"] { font-family: 'Sarabun', sans-serif; }

.hdr {
    background: linear-gradient(135deg,#1a1a2e,#0f3460);
    padding:1.8rem 2rem; border-radius:14px; margin-bottom:1.5rem;
}
.hdr h1 { color:#e2c97e; font-size:1.6rem; margin:0 0 .3rem; }
.hdr p  { color:rgba(255,255,255,.5); margin:0; font-size:.9rem; }

.card {
    background:#fff; border:1.5px solid #e8ecf4; border-radius:12px;
    padding:1.3rem 1.6rem; margin-bottom:1.1rem;
    box-shadow:0 2px 10px rgba(0,0,0,.05);
}
.card-title {
    font-weight:700; color:#0f3460; font-size:.95rem;
    border-bottom:2.5px solid #e2c97e; padding-bottom:.4rem; margin-bottom:1rem;
}
.formula {
    background:linear-gradient(135deg,#f0fdf4,#dcfce7);
    border:2px solid #16a34a; border-radius:10px;
    padding:1rem 1.4rem; text-align:center; margin:.8rem 0;
    font-family:'IBM Plex Mono',monospace; font-size:1.1rem;
    color:#15803d; font-weight:600;
}
.rcard {
    border-radius:10px; padding:1rem 1.3rem; margin-bottom:.7rem; color:#fff;
}
.rcard .lbl { font-size:.8rem; color:rgba(255,255,255,.6); margin-bottom:.2rem; }
.rcard .val { font-family:'IBM Plex Mono',monospace; font-size:1.4rem; font-weight:700; color:#e2c97e; }
.rcard .unit{ font-size:.85rem; color:rgba(255,255,255,.5); margin-left:.25rem; }
.bg-dark { background:linear-gradient(135deg,#0f3460,#16213e); }
.bg-red  { background:linear-gradient(135deg,#7f1d1d,#991b1b); }
.bg-green{ background:linear-gradient(135deg,#14532d,#15803d); }

.ok  { background:#dcfce7; border:1.5px solid #16a34a; border-radius:8px;
       padding:.7rem 1rem; color:#14532d; font-size:.88rem; margin-top:.5rem; }
.warn{ background:#fef3c7; border:1.5px solid #f59e0b; border-radius:8px;
       padding:.7rem 1rem; color:#92400e; font-size:.88rem; margin-top:.5rem; }
.mono{ font-family:'IBM Plex Mono',monospace; font-size:.88rem;
       background:#f8fafc; border-radius:8px; padding:.9rem 1.1rem;
       line-height:2; color:#1e293b; }
.tip { background:#eff6ff; border:1px solid #93c5fd; border-radius:8px;
       padding:.6rem 1rem; color:#1e40af; font-size:.83rem; margin-bottom:.8rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ───────────────────────────────────────────────────
st.markdown("""
<div class="hdr">
  <h1>🏗️ การคำนวณแรงปฏิกิริยาเสาเข็ม — เยื้องศูนย์แบบสมมาตร</h1>
  <p>Eccentric Pile Foundation · Pᵢ = Q/n + Mᵧ·x/Σx² + Mₓ·y/Σy²</p>
</div>
""", unsafe_allow_html=True)

# ── Formula card ─────────────────────────────────────────────
st.markdown("""
<div class="card">
  <div class="card-title">📐 สูตรที่ใช้คำนวณ</div>
  <div class="formula">Pᵢ = (Q / n)  +  (Mᵧ · xᵢ / Σx²)  +  (Mₓ · yᵢ / Σy²)</div>
  <p style="color:#555;font-size:.88rem;margin:.4rem 0 0">
    <b>Q</b> = แรงแนวดิ่งรวม &nbsp;|&nbsp; <b>n</b> = จำนวนเสาเข็ม &nbsp;|&nbsp;
    <b>Mₓ, Mᵧ</b> = โมเมนต์ที่ C.G. ใหม่ &nbsp;|&nbsp;
    <b>xᵢ, yᵢ</b> = ระยะเสาเข็มจาก C.G.
  </p>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SECTION 1 — ข้อมูลแรงกระทำ (แก้ไขได้ในหน้าหลัก)
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title">📦 ข้อมูลแรงกระทำและกำลังรับแรงอนุญาต</div>', unsafe_allow_html=True)

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    Q  = st.number_input("Q — แรงแนวดิ่งรวม (ตัน)",
                          min_value=0.0, value=500.0, step=10.0, format="%.2f")
with c2:
    Mx = st.number_input("Mₓ — โมเมนต์แกน X (ตัน·ม.)",
                          value=80.0, step=5.0, format="%.2f")
with c3:
    My = st.number_input("Mᵧ — โมเมนต์แกน Y (ตัน·ม.)",
                          value=60.0, step=5.0, format="%.2f")
with c4:
    P_allow   = st.number_input("P_allow (ตัน/ต้น)",
                                 min_value=1.0, value=120.0, step=5.0, format="%.2f")
with c5:
    P_tension = st.number_input("P_tension (ตัน/ต้น)",
                                 min_value=0.0, value=30.0, step=5.0, format="%.2f")

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SECTION 2 — ตารางตำแหน่งเสาเข็ม (แก้ไขได้ในตาราง)
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title">📍 ตารางตำแหน่งเสาเข็ม — คลิกช่องเพื่อแก้ไขได้เลย</div>', unsafe_allow_html=True)

st.markdown('<div class="tip">💡 <b>วิธีใช้:</b> คลิกที่ช่องในตารางด้านล่างเพื่อแก้ไขค่า x, y ของแต่ละต้น · กด Enter หรือคลิกที่อื่นเพื่อยืนยัน · เพิ่ม/ลดจำนวนต้นได้จากช่อง "จำนวนเสาเข็ม"</div>', unsafe_allow_html=True)

n_piles = st.number_input("จำนวนเสาเข็ม (n)", min_value=2, max_value=20, value=4, step=1, key="n_piles")
n_piles = int(n_piles)

def_x = [-1.5, 1.5,-1.5, 1.5,-1.5, 1.5, 0.0, 0.0,
           2.0,-2.0, 2.0,-2.0, 2.0,-2.0, 0.0, 0.0,
           3.0,-3.0, 0.0, 0.0]
def_y = [-1.5,-1.5, 1.5, 1.5, 0.0, 0.0,-1.5, 1.5,
         -2.0,-2.0, 2.0, 2.0, 0.0, 0.0,-2.0, 2.0,
          0.0, 0.0, 3.0,-3.0]

# สร้าง default dataframe ตาม n_piles
default_df = pd.DataFrame({
    "Pile"  : [f"pile_{i+1}" for i in range(n_piles)],
    "x (m)" : [float(def_x[i % 20]) for i in range(n_piles)],
    "y (m)" : [float(def_y[i % 20]) for i in range(n_piles)],
})

# ใช้ session_state เก็บ dataframe ที่แก้ไขแล้ว
if "pile_df" not in st.session_state or len(st.session_state.pile_df) != n_piles:
    st.session_state.pile_df = default_df.copy()

# st.data_editor — แก้ไขได้ทุกช่อง
edited_df = st.data_editor(
    st.session_state.pile_df,
    use_container_width=True,
    hide_index=True,
    num_rows="fixed",
    column_config={
        "Pile"  : st.column_config.TextColumn("ชื่อเสาเข็ม", width="small"),
        "x (m)" : st.column_config.NumberColumn("x (m) — ระยะจาก C.G. แกน Y",
                                                  format="%.2f", step=0.25,
                                                  min_value=-50.0, max_value=50.0),
        "y (m)" : st.column_config.NumberColumn("y (m) — ระยะจาก C.G. แกน X",
                                                  format="%.2f", step=0.25,
                                                  min_value=-50.0, max_value=50.0),
    },
    key="pile_editor",
)
st.session_state.pile_df = edited_df

if st.button("🔄 รีเซ็ตค่าเริ่มต้น"):
    st.session_state.pile_df = default_df.copy()
    st.rerun()

st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  CALCULATION
# ══════════════════════════════════════════════════════════════
df = edited_df.copy()
df["x²"]  = df["x (m)"] ** 2
df["y²"]  = df["y (m)"] ** 2

n    = len(df)
sx2  = df["x²"].sum()
sy2  = df["y²"].sum()
Qn   = Q / n
cx   = My / sx2 if sx2 != 0 else 0.0
cy   = Mx / sy2 if sy2 != 0 else 0.0
df["Pᵢ (ตัน)"] = Qn + cx * df["x (m)"] + cy * df["y (m)"]

P_max    = df["Pᵢ (ตัน)"].max()
P_min    = df["Pᵢ (ตัน)"].min()
pile_max = df.loc[df["Pᵢ (ตัน)"].idxmax(), "Pile"]
pile_min = df.loc[df["Pᵢ (ตัน)"].idxmin(), "Pile"]

# ══════════════════════════════════════════════════════════════
#  SECTION 3 — ผลการคำนวณ + ตารางสรุป
# ══════════════════════════════════════════════════════════════
L, R = st.columns([3, 2])

with L:
    # ── ตารางสรุปผล ──────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">📊 ตารางผลคำนวณ Pᵢ</div>', unsafe_allow_html=True)

    disp = pd.DataFrame({
        "Pile"      : df["Pile"],
        "x (m)"     : df["x (m)"].map("{:.2f}".format),
        "x²"        : df["x²"].map("{:.4f}".format),
        "y (m)"     : df["y (m)"].map("{:.2f}".format),
        "y²"        : df["y²"].map("{:.4f}".format),
        "Pᵢ (ตัน)"  : df["Pᵢ (ตัน)"].map("{:.4f}".format),
    })
    total_row = pd.DataFrame([{
        "Pile": "Σ ผลรวม",
        "x (m)": "-",
        "x²": f"{sx2:.4f}",
        "y (m)": "-",
        "y²": f"{sy2:.4f}",
        "Pᵢ (ตัน)": f"{df['Pᵢ (ตัน)'].sum():.4f}",
    }])
    st.dataframe(
        pd.concat([disp, total_row], ignore_index=True),
        use_container_width=True, hide_index=True,
    )

    st.markdown(f"""
    <div style="background:#f0f4ff;border-radius:8px;padding:.6rem 1rem;
         font-family:'IBM Plex Mono',monospace;font-size:.83rem;color:#1e3a5f;margin-top:.5rem;">
        Σx² = {sx2:.4f} m² &nbsp;|&nbsp; Σy² = {sy2:.4f} m² &nbsp;|&nbsp; n = {n} ต้น
    </div></div>
    """, unsafe_allow_html=True)

    # ── ขั้นตอนการคำนวณ ──────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">🔢 ขั้นตอนการคำนวณ</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="mono">
        Q / n &nbsp;&nbsp;&nbsp;&nbsp; = {Q:.2f} / {n} = <b>{Qn:.4f}</b> ตัน<br>
        Mᵧ / Σx² = {My:.2f} / {sx2:.4f} = <b>{cx:.4f}</b> ตัน/ม.<br>
        Mₓ / Σy² = {Mx:.2f} / {sy2:.4f} = <b>{cy:.4f}</b> ตัน/ม.<br><br>
        <b>Pᵢ = {Qn:.4f} + ({cx:.4f})·xᵢ + ({cy:.4f})·yᵢ</b>
    </div></div>
    """, unsafe_allow_html=True)

with R:
    # ── ผลลัพธ์ ──────────────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">📋 ผลการคำนวณ</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="rcard bg-red">
        <div class="lbl">⬆ แรงกดสูงสุด ({pile_max})</div>
        <div class="val">{P_max:.3f}<span class="unit">ตัน</span></div>
    </div>
    <div class="rcard bg-green">
        <div class="lbl">⬇ แรงกดต่ำสุด ({pile_min})</div>
        <div class="val">{P_min:.3f}<span class="unit">ตัน</span></div>
    </div>
    <div class="rcard bg-dark">
        <div class="lbl">⚖️ Q / n (เฉลี่ยต่อต้น)</div>
        <div class="val">{Qn:.3f}<span class="unit">ตัน</span></div>
    </div>
    """, unsafe_allow_html=True)

    # Safety check
    if P_max <= P_allow:
        st.markdown(f'<div class="ok">✅ P_max = {P_max:.2f} ≤ P_allow = {P_allow:.2f} ตัน → <b>ผ่าน</b></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warn">⚠️ P_max = {P_max:.2f} > P_allow = {P_allow:.2f} ตัน → <b>ไม่ผ่าน</b></div>', unsafe_allow_html=True)

    if P_min >= 0:
        st.markdown(f'<div class="ok">✅ ไม่มีแรงดึง (P_min = {P_min:.2f} ≥ 0)</div>', unsafe_allow_html=True)
    elif abs(P_min) <= P_tension:
        st.markdown(f'<div class="ok">✅ |P_min| = {abs(P_min):.2f} ≤ P_tension = {P_tension:.2f} ตัน → <b>ผ่าน</b></div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warn">⚠️ |P_min| = {abs(P_min):.2f} > P_tension = {P_tension:.2f} ตัน → <b>ไม่ผ่าน</b></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── SVG แผนผังเสาเข็ม ────────────────────────────────────
    st.markdown('<div class="card"><div class="card-title">🗺️ แผนผังเสาเข็ม</div>', unsafe_allow_html=True)

    W, H, pad = 320, 300, 45
    xs  = df["x (m)"].tolist()
    ys  = df["y (m)"].tolist()
    all_x = xs + [0]; all_y = ys + [0]
    xmin, xmax = min(all_x), max(all_x)
    ymin, ymax = min(all_y), max(all_y)
    span_x = max(xmax - xmin, 0.01)
    span_y = max(ymax - ymin, 0.01)

    def to_svg(rx, ry):
        sx = pad + (rx - xmin) / span_x * (W - 2*pad)
        sy = (H - pad) - (ry - ymin) / span_y * (H - 2*pad)
        return sx, sy

    vmin2 = df["Pᵢ (ตัน)"].min()
    vmax2 = df["Pᵢ (ตัน)"].max()

    def pile_rgb(p):
        t = (p - vmin2) / (vmax2 - vmin2) if vmax2 != vmin2 else 0.5
        r = int(220*t + 22*(1-t))
        g = int(38 *t + 163*(1-t))
        b = int(38 *t + 74 *(1-t))
        return f"rgb({r},{g},{b})"

    circles = ""
    for _, row in df.iterrows():
        sx, sy = to_svg(row["x (m)"], row["y (m)"])
        col = pile_rgb(row["Pᵢ (ตัน)"])
        circles += f"""
        <circle cx="{sx:.1f}" cy="{sy:.1f}" r="22" fill="{col}" stroke="white" stroke-width="2"/>
        <text x="{sx:.1f}" y="{sy:.1f}" dy="4" text-anchor="middle"
              font-size="9" fill="white" font-family="monospace" font-weight="bold">{row["Pᵢ (ตัน)"]:.1f}</text>
        <text x="{sx:.1f}" y="{sy+30:.1f}" text-anchor="middle"
              font-size="8" fill="#444" font-family="sans-serif">{row["Pile"]}</text>"""

    cgx, cgy = to_svg(0, 0)
    ax1x, _  = to_svg(xmin - 0.3, 0)
    ax2x, _  = to_svg(xmax + 0.3, 0)
    _,  ay1y = to_svg(0, ymin - 0.3)
    _,  ay2y = to_svg(0, ymax + 0.3)

    svg = f"""
    <svg width="{W}" height="{H}" xmlns="http://www.w3.org/2000/svg"
         style="background:#f8fafc;border-radius:8px;display:block;margin:auto;">
      <line x1="{ax1x:.0f}" y1="{cgy:.0f}" x2="{ax2x:.0f}" y2="{cgy:.0f}"
            stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
      <line x1="{cgx:.0f}" y1="{ay1y:.0f}" x2="{cgx:.0f}" y2="{ay2y:.0f}"
            stroke="#aaa" stroke-width="1" stroke-dasharray="4,3"/>
      {circles}
      <circle cx="{cgx:.1f}" cy="{cgy:.1f}" r="6" fill="none" stroke="#e2c97e" stroke-width="2.5"/>
      <line x1="{cgx-9:.1f}" y1="{cgy:.1f}" x2="{cgx+9:.1f}" y2="{cgy:.1f}" stroke="#e2c97e" stroke-width="2"/>
      <line x1="{cgx:.1f}" y1="{cgy-9:.1f}" x2="{cgx:.1f}" y2="{cgy+9:.1f}" stroke="#e2c97e" stroke-width="2"/>
      <text x="{cgx+12:.0f}" y="{cgy-10:.0f}" font-size="9" fill="#b45309" font-family="sans-serif" font-weight="bold">C.G.</text>
      <text x="4" y="{H-5}" font-size="8" fill="#999" font-family="sans-serif">🔴 แรงมาก → 🟢 แรงน้อย</text>
    </svg>"""

    st.markdown(svg, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
#  SECTION 4 — กราฟแท่ง
# ══════════════════════════════════════════════════════════════
st.markdown('<div class="card"><div class="card-title">📊 กราฟแรงปฏิกิริยาแต่ละต้น (ตัน)</div>', unsafe_allow_html=True)

chart_df = (
    df[["Pile", "Pᵢ (ตัน)"]]
    .set_index("Pile")
)
st.bar_chart(chart_df, color="#0f3460", use_container_width=True)

st.markdown(f"""
<div style="background:#f8fafc;border-radius:8px;padding:.7rem 1rem;
     font-family:'IBM Plex Mono',monospace;font-size:.85rem;color:#1e293b;margin-top:.3rem;">
    🟡 P_allow = {P_allow:.2f} ตัน &nbsp;|&nbsp;
    🟣 −P_tension = −{P_tension:.2f} ตัน &nbsp;|&nbsp;
    📈 P_max = {P_max:.2f} ตัน ({pile_max}) &nbsp;|&nbsp;
    📉 P_min = {P_min:.2f} ตัน ({pile_min})
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center;color:#bbb;font-size:.78rem;margin-top:.5rem;padding-bottom:1.5rem;">
    Pile Foundation Calculator · Pᵢ = Q/n + Mᵧ·x/Σx² + Mₓ·y/Σy²
</div>
""", unsafe_allow_html=True)
