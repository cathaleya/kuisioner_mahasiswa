import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io
import requests

# ─── KONSTANTA ───────────────────────────────────────────────────────────────
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
                "Saya dapat menyesuaikan kosakata bahasa Inggris sesuai dengan konteks pembelajaran di SD.",
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
                "Saya dapat menggunakan strategi seperti gesture atau contoh untuk memperjelas maksud, dan tujuan komunikasi.",
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

LIKERT = {
    "🤩 Sangat Suka": 5, 
    "🙂 Suka": 4,
    "😐 Biasa Saja": 3, 
    "🙁 Kurang Suka": 2, 
    "😠 Tidak Suka": 1
}

# ─── INITIAL STATE ───────────────────────────────────────────────────────────
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'user_data' not in st.session_state:
    st.session_state.user_data = {}

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
    page_title="Instrumen Penelitian S-ELT",
    page_icon="🎓",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }
.hero {
    background: linear-gradient(135deg,#064e3b 0%,#059669 100%);
    padding: 2.5rem 2rem; border-radius: 24px; color: white;
    margin-bottom: 2rem; text-align: center;
    box-shadow: 0 10px 30px rgba(6,78,59,0.2);
}
.hero h1 { font-size:2.2rem; margin:0 0 .5rem; font-weight:800; }
.hero p  { margin:0; opacity:.9; font-size:1.1rem; }
.k-header {
    background:#ecfdf5; border-left:6px solid #10b981;
    padding:1rem 1.5rem; border-radius:0 15px 15px 0;
    font-weight:800; color:#064e3b; font-size:1.2rem;
    margin:2.5rem 0 1rem;
}
.s-header {
    background: #f0fdf4;
    color:#166534; padding:.6rem 1.2rem; border-radius:10px;
    font-weight:700; font-size:1rem; margin:1.2rem 0 .8rem;
    border: 1px solid #dcfce7;
}
.item-row {
    background:white; border-radius:15px; padding:1.2rem;
    margin:.8rem 0; box-shadow:0 2px 10px rgba(0,0,0,0.03);
    border: 1px solid #f1f5f9; font-size:1rem; color:#1e293b;
    line-height: 1.5;
}
.stRadio > div { gap: 15px; }
.step-indicator {
    text-align: center; margin-bottom: 20px; color: #064e3b; font-weight: 800;
}
</style>
""", unsafe_allow_html=True)

# ─── HEADER ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <h1>📝 Angket Respon Mahasiswa</h1>
  <p>Platform Smart-English Language Teaching (S-ELT)</p>
</div>
""", unsafe_allow_html=True)

# ─── STEP 1: IDENTITAS ───────────────────────────────────────────────────────
if st.session_state.step == 1:
    st.markdown('<div class="step-indicator">LANGKAH 1 DARI 2: DATA DIRI</div>', unsafe_allow_html=True)
    with st.container(border=True):
        st.markdown("### 👤 Identitas Mahasiswa")
        nama      = st.text_input("Nama Lengkap *", placeholder="Siapa namamu?")
        institusi = st.text_input("Asal Kampus *", placeholder="Nama Universitas/Sekolah")
        c1, c2    = st.columns(2)
        kontak    = c1.text_input("No. WhatsApp", placeholder="08xxxxxxxxxx")
        email     = c2.text_input("Email", placeholder="email@contoh.com")
        
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Lanjutkan ke Pertanyaan ➔", use_container_width=True):
            if not nama.strip() or not institusi.strip():
                st.warning("⚠️ Mohon lengkapi Nama dan Kampus terlebih dahulu ya!")
            else:
                st.session_state.user_data = {
                    "nama": nama,
                    "institusi": institusi,
                    "kontak": kontak,
                    "email": email
                }
                st.session_state.step = 2
                st.rerun()

# ─── STEP 2: PERTANYAAN ──────────────────────────────────────────────────────
elif st.session_state.step == 2:
    st.markdown(f'<div class="step-indicator">LANGKAH 2 DARI 2: INSTRUMEN EVALUASI</div>', unsafe_allow_html=True)
    st.info(f"Halo **{st.session_state.user_data['nama']}**! Silakan isi semua pertanyaan di bawah ini dengan jujur ya. 😊")
    
    with st.form("form_pertanyaan", border=False):
        all_answers = []
        global_num  = 0

        for k in KUESIONER:
            st.markdown(f'<div class="k-header">📋 {k["judul"]}</div>', unsafe_allow_html=True)
            for s in k["seksi"]:
                st.markdown(f'<div class="s-header">🔹 {s["nama"]}</div>', unsafe_allow_html=True)
                for item in s["items"]:
                    global_num += 1
                    st.markdown(f'<div class="item-row"><b>{global_num}.</b> {item}</div>', unsafe_allow_html=True)
                    jawaban = st.radio("", list(LIKERT.keys()), key=f"q_{global_num}", index=None, horizontal=True, label_visibility="collapsed")
                    all_answers.append({
                        "Kuesioner": k["judul"],
                        "Dimensi":   s["nama"],
                        "No":        global_num,
                        "Pernyataan": item,
                        "Jawaban":   jawaban,
                        "Skor":      LIKERT[jawaban] if jawaban else None,
                    })

        st.markdown('<div class="k-header">✍️ Berikan Pendapatmu</div>', unsafe_allow_html=True)
        deskripsi_list = []
        for i, q in enumerate(DESKRIPSI):
            st.markdown(f"**{i+1}. {q}**")
            ans = st.text_area("", key=f"desc_{i}", height=120, placeholder="Tuliskan pendapatmu di sini ya...", label_visibility="collapsed")
            deskripsi_list.append({"No": i+1, "Pertanyaan": q, "Jawaban": ans})

        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([1, 2])
        if c1.form_submit_button("⬅ Kembali"):
            st.session_state.step = 1
            st.rerun()
            
        submitted = c2.form_submit_button("🚀 Kirim Jawaban Sekarang", use_container_width=True)

    if submitted:
        belum_dijawab = [a["No"] for a in all_answers if a["Jawaban"] is None]
        if belum_dijawab:
            st.error(f"⚠️ Masih ada **{len(belum_dijawab)} soal** yang terlewat! Yuk, lengkapi dulu semua jawabanmu.")
        else:
            with st.spinner("⏳ Mengirim jawabanmu ke server..."):
                ud = st.session_state.user_data
                ok, err = save_to_gsheet(ud['nama'], ud['institusi'], ud['kontak'], ud['email'], all_answers, deskripsi_list)
                
                if ok:
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error(f"⚠️ Aduh, gagal menyimpan: {err}")

# ─── STEP 3: TERIMA KASIH ────────────────────────────────────────────────────
elif st.session_state.step == 3:
    st.balloons()
    st.markdown(f"""
    <div style="background:#f0fdf4; padding:40px; border-radius:24px; border:1px solid #bbf7d0; text-align:center; margin-top:20px; box-shadow: 0 10px 30px rgba(0,0,0,0.05);">
        <h1 style="color:#064e3b; margin-top:0;">✨ Hore! ✨</h1>
        <h2 style="color:#166534;">Terima kasih, {st.session_state.user_data['nama']}!</h2>
        <p style="color:#166534; font-size:1.2rem; opacity:0.8;">Jawabanmu sudah kami terima dengan aman.</p>
        <div style="font-size: 5rem; margin: 20px 0;">🎉</div>
        <p style="color:#064e3b; font-weight: 600;">Partisipasimu sangat berarti bagi pengembangan platform S-ELT.</p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("Isi Kembali untuk Mahasiswa Lain"):
        st.session_state.step = 1
        st.session_state.user_data = {}
        st.rerun()
