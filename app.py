import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import requests

# ─── KONSTANTA ───────────────────────────────────────────────────────────────
# Paste URL Apps Script Web App Anda di sini setelah deploy
APPS_SCRIPT_URL = st.secrets.get("APPS_SCRIPT_URL", "")
SHEET_NAME      = "Mahasiswa"

KUESIONER = [
    {
        "judul": "Kuesioner Flipbook Interaktif Berbasis Integrated Language Skills",
        "seksi": [
            {"nama": "Interaktivitas", "items": [
                "Flipbook mudah dinavigasi saat digunakan.",
                "Menu dan tombol dalam flipbook mudah dipahami.",
                "Flipbook memberikan respon (feedback) terhadap aktivitas pengguna.",
                "Saya dapat berpindah antar halaman dengan mudah.",
            ]},
            {"nama": "Integrasi Keterampilan Bahasa", "items": [
                "Flipbook menyediakan latihan mendengarkan (listening) yang jelas.",
                "Flipbook menyediakan latihan berbicara (speaking) yang membantu.",
                "Flipbook menyediakan teks bacaan (reading) yang menarik.",
                "Flipbook menyediakan latihan menulis (writing) yang relevan.",
                "Keterampilan listening, speaking, reading, dan writing terintegrasi dengan baik.",
            ]},
            {"nama": "Desain Pembelajaran", "items": [
                "Tampilan flipbook menarik secara visual.",
                "Materi dalam flipbook disusun secara sistematis.",
                "Flipbook membuat saya lebih tertarik untuk belajar.",
                "Flipbook membantu saya memahami materi dengan lebih mudah.",
                "Tampilan flipbook sesuai karakteristik mahasiswa PGSD.",
                "Flipbook dapat memberi motivasi dalam minat belajar.",
                "Tampilan flipbook sesuai karakteristik mahasiswa PGSD.",
            ]},
            {"nama": "Kegunaan (Usability)", "items": [
                "Flipbook mudah digunakan tanpa bantuan orang lain.",
                "Flipbook membantu meningkatkan efektivitas belajar saya.",
                "Flipbook menghemat waktu dalam memahami materi.",
                "Flipbook dapat digunakan kapan saja dan di mana saja.",
            ]},
        ]
    },
    {
        "judul": "Kuesioner Adaptive Thinking English Communication",
        "seksi": [
            {"nama": "Language Adaptability", "items": [
                "Saya mampu menyesuaikan bahasa Inggris dalam situasi formal dan informal.",
                "Saya dapat menyesuaikan cara berbicara sesuai lawan bicara.",
                "Saya mampu memahami berbagai aksen bahasa Inggris.",
                "Saya menggunakan kosakata sesuai konteks pembicaraan.",
                "Saya dapat menyesuaikan kosakata bahasa Inggris sesuai konteks pembelajaran di SD.",
                "Saya mampu menggunakan bahasa Inggris sederhana ketika menjelaskan materi kepada siswa SD.",
                "Saya dapat mengubah struktur kalimat agar lebih mudah dipahami oleh lawan bicara.",
                "Saya tetap dapat berkomunikasi dalam bahasa Inggris meskipun memiliki keterbatasan kosakata.",
                "Saya mampu menyesuaikan bahasa ketika menghadapi situasi komunikasi yang tidak terduga.",
                "Saya dapat mengubah gaya bahasa Inggris saya ketika berbicara dengan dosen, teman, atau siswa.",
            ]},
            {"nama": "Cognitive Flexibility", "items": [
                "Saya mampu memahami informasi bahasa Inggris dari audio, teks, dan video.",
                "Saya mengubah strategi ketika mengalami kesulitan berkomunikasi.",
                "Saya dapat menghubungkan ide-ide dalam bahasa Inggris.",
                "Saya mampu memahami makna tersirat dalam percakapan.",
                "Saya mampu berpikir cepat dalam merespon percakapan bahasa Inggris.",
                "Saya dapat memahami makna kalimat bahasa Inggris dari konteks, meskipun tidak mengetahui semua kata.",
                "Saya dapat mengubah strategi komunikasi ketika mengalami kesulitan memahami lawan bicara.",
                "Saya mampu melihat berbagai kemungkinan makna dari satu ungkapan bahasa Inggris.",
                "Saya mampu berpindah dari satu topik ke topik lain dalam percakapan bahasa Inggris dengan lancar.",
                "Saya dapat menghubungkan pengetahuan sebelumnya dengan informasi baru dalam bahasa Inggris.",
                "Saya mampu menemukan cara alternatif untuk menyampaikan ide dalam bahasa Inggris.",
                "Saya tidak mudah bingung ketika menghadapi situasi komunikasi yang kompleks dalam bahasa Inggris.",
                "Saya mampu memahami informasi bahasa Inggris dari berbagai sumber.",
                "Saya mampu menghubungkan ide dalam bahasa Inggris secara logis.",
                "Saya dapat memahami makna tersirat dalam percakapan bahasa Inggris.",
            ]},
            {"nama": "Integrated Communication Skills", "items": [
                "Saya dapat merespon percakapan setelah mendengarkan.",
                "Saya mampu menjelaskan isi bacaan secara lisan.",
                "Saya dapat menulis berdasarkan informasi yang didengar.",
                "Saya mampu merespon secara cepat dalam percakapan.",
                "Saya dapat memahami instruksi dalam bahasa Inggris dan melaksanakannya dengan benar.",
                "Saya dapat mengintegrasikan berbagai keterampilan bahasa Inggris dalam kegiatan pembelajaran.",
                "Saya mampu menggunakan bahasa tubuh dan ekspresi untuk mendukung komunikasi bahasa Inggris.",
                "Saya dapat merespon percakapan dengan tepat berdasarkan apa yang saya dengar.",
                "Saya mampu menulis ide dalam bahasa Inggris dan menjelaskannya secara lisan.",
                "Saya mampu menggabungkan keterampilan mendengar dan berbicara dalam komunikasi bahasa Inggris.",
            ]},
            {"nama": "Communicative Problem Solving", "items": [
                "Saya bertanya ulang ketika tidak memahami percakapan.",
                "Saya menggunakan kata lain (parafrase) saat kesulitan.",
                "Saya tetap berkomunikasi walaupun kosakata terbatas.",
                "Saya mampu memperbaiki kesalahan komunikasi.",
                "Saya mampu mencari cara untuk tetap berkomunikasi ketika mengalami kesulitan dalam bahasa Inggris.",
                "Saya mampu meminta klarifikasi ketika tidak memahami lawan bicara.",
                "Saya dapat memperbaiki kesalahan komunikasi dalam bahasa Inggris secara mandiri.",
                "Saya mampu menemukan solusi ketika terjadi miskomunikasi dalam percakapan bahasa Inggris.",
                "Saya tetap percaya diri dalam berkomunikasi meskipun mengalami kesalahan.",
                "Saya dapat menggunakan strategi seperti gesture atau contoh untuk memperjelas maksud dan tujuan komunikasi.",
            ]},
        ]
    },
    {
        "judul": "Kuesioner Kompetensi Profesional Mahasiswa PGSD",
        "seksi": [
            {"nama": "Content Mastery", "items": [
                "Saya memahami materi Bahasa Inggris untuk siswa SD.",
                "Saya mampu menjelaskan materi pembelajaran bahasa inggris dengan sederhana kepada siswa SD.",
                "Saya dapat mengaitkan materi dengan kehidupan sehari-hari.",
                "Saya memahami konsep dasar materi Bahasa Inggris untuk siswa SD yang akan diajarkan.",
                "Saya memahami keterkaitan antar topik dalam satu mata pelajaran.",
                "Saya mampu menjawab pertanyaan siswa terkait materi pembelajaran dengan tepat.",
                "Saya menguasai berbagai sumber belajar untuk memperdalam materi ajar.",
                "Saya mampu mengembangkan materi ajar sesuai dengan kebutuhan siswa.",
            ]},
            {"nama": "Pedagogical Skills", "items": [
                "Saya mampu merancang pembelajaran berbasis digital.",
                "Saya mampu menggunakan flipbook dalam pembelajaran.",
                "Saya dapat mengelola kelas dengan baik.",
                "Saya mampu merancang rencana pembelajaran yang sistematis dan terstruktur.",
                "Saya menggunakan metode pembelajaran yang bervariasi sesuai dengan karakteristik siswa.",
                "Saya mampu mengelola kelas secara efektif selama proses pembelajaran.",
                "Saya dapat menyesuaikan strategi pembelajaran berdasarkan kebutuhan siswa.",
                "Saya mampu menciptakan suasana belajar yang aktif dan menyenangkan.",
                "Saya menggunakan teknik penilaian yang sesuai untuk mengukur hasil belajar siswa.",
                "Saya mampu memberikan umpan balik yang konstruktif kepada siswa.",
                "Saya dapat mengidentifikasi kesulitan belajar siswa dan memberikan solusi yang tepat.",
                "Saya dapat mendesain pembelajaran dengan mengintegrasikan empat keterampilan Bahasa Inggris (menyimak, berbicara, membaca, dan menulis).",
            ]},
            {"nama": "Digital Competence", "items": [
                "Saya mampu menggunakan teknologi dalam pembelajaran.",
                "Saya dapat membuat bahan ajar digital sederhana.",
                "Saya mampu mengintegrasikan teknologi dalam proses belajar.",
                "Saya mampu menggunakan teknologi dalam pembelajaran.",
                "Saya dapat membuat bahan ajar digital sederhana (misalnya PPT, e-modul, flipbook).",
                "Saya dapat memanfaatkan media pembelajaran berbasis digital (video, aplikasi, dll.).",
                "Saya dapat menggunakan platform pembelajaran online untuk mendukung kegiatan belajar.",
                "Saya memahami etika penggunaan teknologi dalam pembelajaran.",
                "Saya dapat membantu siswa dalam menggunakan teknologi untuk belajar.",
                "Saya mampu memilih media digital yang sesuai dengan tujuan pembelajaran.",
            ]},
            {"nama": "Professional Communication", "items": [
                "Saya mampu menjelaskan materi dalam bahasa Inggris.",
                "Saya percaya diri berbicara dalam bahasa Inggris.",
                "Saya mampu berinteraksi dengan siswa menggunakan bahasa Inggris.",
                "Saya mampu menjelaskan materi dalam bahasa Inggris.",
                "Saya dapat berkomunikasi dengan rekan sejawat secara profesional.",
                "Saya mampu menerima dan memberikan kritik secara konstruktif.",
                "Saya mampu menyesuaikan gaya komunikasi dengan situasi pembelajaran.",
                "Saya mampu berkomunikasi dengan siswa secara jelas dan efektif.",
                "Saya mampu menjelaskan instruksi pembelajaran dengan mudah dipahami siswa.",
                "Saya menunjukkan sikap percaya diri saat menyampaikan materi pembelajaran bahasa inggris kepada siswa.",
            ]},
        ]
    },
]

DESKRIPSI = [
    "Bagaimana pengalaman Anda menggunakan flipbook interaktif? Uraikan dengan rinci.",
    "Apakah flipbook membantu meningkatkan kemampuan profesional dalam pembelajaran bahasa Inggris Anda? Jelaskan alasannya.",
    "Bagaimana pengaruhnya terhadap cara berpikir adaptif dan komunikasi pada pembelajaran Bahasa Inggris Anda? Uraikan dengan rinci.",
]

LIKERT = {"Sangat Tidak Setuju (STS)": 1, "Tidak Setuju (TS)": 2,
          "Netral (N)": 3, "Setuju (S)": 4, "Sangat Setuju (SS)": 5}

# ─── GOOGLE SHEETS via APPS SCRIPT ──────────────────────────────────────────
def build_headers():
    hdrs = ["Timestamp", "Nama", "Institusi", "Kontak", "Email"]
    q = 0
    for k in KUESIONER:
        for s in k["seksi"]:
            for _ in s["items"]:
                q += 1
                hdrs.append(f"Q{q}")
    for i in range(1, 4):
        hdrs.append(f"Deskripsi_{i}")
    hdrs.append("Rata_rata_Keseluruhan")
    for k in KUESIONER:
        for s in k["seksi"]:
            hdrs.append(f"Mean_{s['nama'].replace(' ','_')}")
    return hdrs

def save_to_gsheet(nama, institusi, kontak, email, answers, deskripsi_list):
    """Kirim data ke Google Sheet via Apps Script Web App (HTTP POST)."""
    if not APPS_SCRIPT_URL:
        return False, "APPS_SCRIPT_URL belum diisi di secrets."
    try:
        df  = pd.DataFrame(answers)
        ts  = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        row = [ts, nama, institusi, kontak, email]
        row += [int(s) for s in df["Skor"].tolist()]
        row += [d["Jawaban"] for d in deskripsi_list]
        row.append(round(float(df["Skor"].mean()), 3))
        for k in KUESIONER:
            for s in k["seksi"]:
                mask = (df["Kuesioner"] == k["judul"]) & (df["Dimensi"] == s["nama"])
                row.append(round(float(df.loc[mask, "Skor"].mean()), 3))
        payload = {"sheet": SHEET_NAME, "headers": build_headers(), "row": row}
        resp = requests.post(APPS_SCRIPT_URL, json=payload, timeout=15)
        result = resp.json()
        if result.get("status") == "ok":
            return True, None
        return False, result.get("message", "Unknown error")
    except Exception as e:
        return False, str(e)

# ─── PAGE CONFIG ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Instrumen Penelitian Mahasiswa PGSD",
    page_icon="👨‍🎓",
    layout="wide",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.hero {
    background: linear-gradient(135deg,#1e3a8a 0%,#3b82f6 60%,#60a5fa 100%);
    padding: 2.2rem 2rem; border-radius: 16px; color: white;
    margin-bottom: 1.5rem; box-shadow: 0 8px 30px rgba(59,130,246,.35);
}
.hero h1 { font-size:2rem; margin:0 0 .3rem; }
.hero p  { margin:0; opacity:.88; }
.k-header {
    background:#eff6ff; border-left:5px solid #3b82f6;
    padding:.75rem 1.2rem; border-radius:0 10px 10px 0;
    font-weight:700; color:#1e3a8a; font-size:1.05rem;
    margin:1.6rem 0 .6rem;
}
.s-header {
    background:linear-gradient(90deg,#1e3a8a,#3b82f6);
    color:white; padding:.55rem 1rem; border-radius:8px;
    font-weight:600; font-size:.9rem; margin:.9rem 0 .5rem;
}
.item-row {
    background:white; border-radius:10px; padding:.85rem 1rem;
    margin:.4rem 0; box-shadow:0 1px 6px rgba(0,0,0,.07);
    border-left:3px solid #bfdbfe; font-size:.92rem; color:#1e293b;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>👨‍🎓 Instrumen Penelitian — Mahasiswa PGSD</h1>
  <p>Pengembangan Flipbook Interaktif Berbasis Integrated Language Skills<br>
     Program Studi PGSD — Silakan isi dengan jujur dan objektif</p>
</div>
""", unsafe_allow_html=True)

with st.expander("📌 Petunjuk Pengisian", expanded=False):
    st.markdown("""
    1. Isi **data diri** Anda di bagian atas
    2. Baca setiap pernyataan dengan **seksama**
    3. Pilih jawaban yang **paling sesuai** dengan kondisi Anda
    4. Skala: **1** (Sangat Tidak Setuju) hingga **5** (Sangat Setuju)
    5. Isi semua bagian, termasuk **Deskripsi Pengalaman** di akhir
    6. Klik **✅ Kirim Jawaban** — data langsung tersimpan otomatis
    """)

# ─── DATA DIRI ───────────────────────────────────────────────────────────────
st.subheader("📝 Data Diri")
c1, c2 = st.columns(2)
nama      = c1.text_input("Nama Lengkap *", placeholder="Masukkan nama lengkap Anda")
institusi = c2.text_input("Asal Institusi *", placeholder="Nama perguruan tinggi")
c3, c4    = st.columns(2)
kontak    = c3.text_input("No. Kontak / WhatsApp", placeholder="08xxxxxxxxxx")
email     = c4.text_input("Email", placeholder="email@contoh.com")
st.markdown("---")

# ─── FORM ────────────────────────────────────────────────────────────────────
with st.form("form_mahasiswa", border=False):
    all_answers = []
    global_num  = 0

    for k in KUESIONER:
        st.markdown(f'<div class="k-header">📋 {k["judul"]}</div>', unsafe_allow_html=True)
        st.markdown(
            '<div style="background:#f8faff;border-radius:8px;padding:.5rem 1rem;'
            'margin-bottom:.8rem;font-size:.82rem;color:#475569;">'
            '📏 <b>1</b>=Sangat Tidak Setuju &nbsp;|&nbsp; <b>2</b>=Tidak Setuju &nbsp;|&nbsp;'
            '<b>3</b>=Netral &nbsp;|&nbsp; <b>4</b>=Setuju &nbsp;|&nbsp; <b>5</b>=Sangat Setuju'
            '</div>', unsafe_allow_html=True)

        for s in k["seksi"]:
            st.markdown(f'<div class="s-header">🔹 {s["nama"]}</div>', unsafe_allow_html=True)
            for item in s["items"]:
                global_num += 1
                st.markdown(f'<div class="item-row"><b>{global_num}.</b> {item}</div>',
                            unsafe_allow_html=True)
                jawaban = st.radio("", list(LIKERT.keys()),
                                   key=f"q_{global_num}", index=2,
                                   horizontal=True, label_visibility="collapsed")
                all_answers.append({
                    "Kuesioner": k["judul"],
                    "Dimensi":   s["nama"],
                    "No":        global_num,
                    "Pernyataan": item,
                    "Jawaban":   jawaban,
                    "Skor":      LIKERT[jawaban],
                })

    # Deskripsi Pengalaman
    st.markdown('<div class="k-header">✍️ Deskripsi Pengalaman</div>', unsafe_allow_html=True)
    deskripsi_list = []
    for i, q in enumerate(DESKRIPSI):
        st.markdown(f"**{i+1}. {q}**")
        ans = st.text_area("", key=f"desc_{i}", height=110,
                           placeholder="Tuliskan jawaban Anda di sini...",
                           label_visibility="collapsed")
        deskripsi_list.append({"No": i+1, "Pertanyaan": q, "Jawaban": ans})

    submitted = st.form_submit_button("✅ Kirim Jawaban", use_container_width=True)

# ─── SIMPAN & TAMPILKAN HASIL ────────────────────────────────────────────────
if submitted:
    if not nama.strip():
        st.warning("⚠️ Harap isi Nama Lengkap terlebih dahulu!")
        st.stop()

    # Simpan ke Google Sheets
    with st.spinner("⏳ Menyimpan data ke Google Sheets..."):
        ok, err = save_to_gsheet(nama, institusi, kontak, email,
                                  all_answers, deskripsi_list)

    if ok:
        st.success("✅ Data berhasil tersimpan ke Google Sheets!")
    else:
        st.warning(f"⚠️ Gagal menyimpan ke Google Sheets: {err}\n\n"
                   "Data tetap dapat diunduh melalui tombol Excel di bawah.")

    # Visualisasi
    df = pd.DataFrame(all_answers)
    overall = df["Skor"].mean()

    def kategori(m):
        if m < 1.8: return "Sangat Rendah"
        if m < 2.6: return "Rendah"
        if m < 3.4: return "Sedang"
        if m < 4.2: return "Tinggi"
        return "Sangat Tinggi"

    st.markdown("---")
    st.subheader("📊 Ringkasan Hasil Anda")
    m1, m2, m3 = st.columns(3)
    m1.metric("Rata-rata Keseluruhan", f"{overall:.2f} / 5.00")
    m2.metric("Total Pernyataan", len(df))
    m3.metric("Kategori", kategori(overall))

    by_dim = df.groupby("Dimensi")["Skor"].mean().reset_index()
    by_dim.columns = ["Dimensi", "Rata-rata"]
    fig1 = px.bar(by_dim, x="Rata-rata", y="Dimensi", orientation="h",
                  color="Rata-rata",
                  color_continuous_scale=["#ef4444","#eab308","#3b82f6"],
                  range_color=[1, 5], text="Rata-rata",
                  title="Rata-rata Skor per Dimensi")
    fig1.update_traces(texttemplate="%{text:.2f}", textposition="outside")
    fig1.update_layout(height=max(350, len(by_dim)*44),
                       plot_bgcolor="white", paper_bgcolor="white",
                       coloraxis_showscale=False,
                       margin=dict(l=0, r=50, t=50, b=20))
    fig1.update_xaxes(range=[0, 5.8])
    st.plotly_chart(fig1, use_container_width=True)

    dist  = df["Skor"].value_counts().sort_index()
    label_map = {1:"STS",2:"TS",3:"N",4:"S",5:"SS"}
    fig2  = go.Figure(go.Pie(
        labels=[label_map[i] for i in dist.index], values=dist.values,
        marker_colors=["#ef4444","#f97316","#eab308","#22c55e","#3b82f6"],
        hole=0.5, textinfo="label+percent"))
    fig2.update_layout(title="Distribusi Jawaban",
                       height=320, margin=dict(t=50,b=0,l=0,r=0))
    st.plotly_chart(fig2, use_container_width=True)

    # Backup Excel
    ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
    buf  = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        pd.DataFrame([{"Nama": nama, "Institusi": institusi,
                        "Kontak": kontak, "Email": email,
                        "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}]
                     ).to_excel(writer, sheet_name="Identitas", index=False)
        df.to_excel(writer, sheet_name="Data Jawaban", index=False)
        summary = df.groupby(["Kuesioner","Dimensi"])["Skor"].agg(
            Rata_rata="mean", Jumlah="count", Std_Dev="std").reset_index()
        summary.to_excel(writer, sheet_name="Ringkasan", index=False)
        pd.DataFrame(deskripsi_list).to_excel(writer, sheet_name="Deskripsi", index=False)

    st.download_button("⬇️ Unduh Salinan Hasil (Excel)",
                       data=buf.getvalue(),
                       file_name=f"Mahasiswa_{nama.replace(' ','_')}_{ts}.xlsx",
                       mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       use_container_width=True)
