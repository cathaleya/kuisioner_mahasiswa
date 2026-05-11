import streamlit as st
import pandas as pd
import requests
import datetime
import base64
import os

# ==========================================
# CONFIG & STYLES
# ==========================================
st.set_page_config(page_title="Instrumen Evaluasi S-ELT", page_icon="🎓", layout="centered")

def local_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #f8fafc 0%, #ffffff 100%);
    }
    
    .stApp {
        background-color: #ffffff;
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }
    
    .stRadio > div {
        background: #f8fafc;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin-bottom: 10px;
        transition: all 0.3s ease;
    }
    
    .stRadio > div:hover {
        border-color: #10b981;
        box-shadow: 0 4px 12px rgba(16, 185, 129, 0.05);
    }
    
    h1, h2, h3 { color: #064e3b; font-weight: 800; }
    
    .stButton > button {
        width: 100%;
        background-color: #10b981 !important;
        color: white !important;
        border-radius: 12px;
        padding: 15px;
        font-weight: 700;
        border: none;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    
    .stButton > button:hover {
        background-color: #059669 !important;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }

    .hero-section {
        background: linear-gradient(135deg, #064e3b 0%, #10b981 100%);
        padding: 40px 20px;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin-bottom: 30px;
    }

    .dimension-card {
        background: #ecfdf5;
        padding: 10px 20px;
        border-radius: 10px;
        border-left: 5px solid #10b981;
        margin: 25px 0 15px 0;
        font-weight: bold;
        color: #064e3b;
    }
    
    .success-card {
        background: #f0fdf4;
        padding: 40px;
        border-radius: 24px;
        text-align: center;
        border: 2px solid #bbf7d0;
    }

    /* Flipbook Mobile Optimization */
    .flipbook-container {
        width: 100%;
        max-width: 400px;
        margin: 0 auto;
        aspect-ratio: 3/4;
    }
    </style>
    """, unsafe_allow_html=True)

local_css()

# ==========================================
# DATA & IMAGE LOADING
# ==========================================
KUESIONER = {
    "1. SINTAKS (SYNTAX)": [
        "Alur pembelajaran S-ELT jelas dan mudah diikuti",
        "Tahapan pembelajaran tersusun sistematis",
        "Urutan kegiatan menunjukkan hubungan yang logis",
        "Setiap tahap memiliki tujuan yang jelas",
        "Tahap decomposition terlihat dalam sintaks",
        "Tahap pattern recognition terintegrasi",
        "Tahap abstraction membantu pemahaman",
        "Tahap algorithmic thinking muncul dalam aktivitas",
        "Gamifikasi terintegrasi dalam sintaks",
        "Sintaks memungkinkan pembelajaran adaptif",
        "Terdapat mekanisme pengulangan (loop learning)",
        "Sintaks dapat diterapkan dalam kelas nyata"
    ],
    "2. SISTEM SOSIAL (SOCIAL SYSTEM)": [
        "Model mendorong mahasiswa aktif belajar",
        "Mahasiswa terlibat dalam proses analisis",
        "Mahasiswa berpikir mandiri dalam menyelesaikan tugas",
        "Peran dosen sebagai fasilitator sudah tepat",
        "Dosen tidak mendominasi pembelajaran",
        "Interaksi mahasiswa dengan sistem berjalan baik",
        "Interaksi sosial antar mahasiswa terjadi",
        "Model mendukung pembelajaran mandiri",
        "Mahasiswa dapat mengontrol proses belajar sendiri",
        "Model menciptakan suasana belajar interaktif"
    ],
    "3. PRINSIP REAKSI (PRINCIPLES OF REACTION)": [
        "Sistem memberikan umpan balik secara langsung",
        "Feedback membantu memahami kesalahan",
        "Respons sistem sesuai kemampuan mahasiswa",
        "Sistem memberikan petunjuk (hint) saat salah",
        "Dosen memberikan arahan tanpa langsung memberi jawaban",
        "Dosen mendorong mahasiswa berpikir",
        "Feedback sistem bersifat jelas dan mudah dipahami",
        "Respons pembelajaran bersifat adaptif"
    ],
    "4. SISTEM PENDUKUNG (SUPPORT SYSTEM)": [
        "Aplikasi Android mudah digunakan",
        "Tampilan aplikasi menarik",
        "Navigasi sistem mudah dipahami",
        "Materi pembelajaran sesuai kebutuhan",
        "Materi terintegrasi dengan Computational Thinking",
        "Fitur aplikasi mendukung pembelajaran",
        "Sistem mendukung pembelajaran interaktif",
        "Dosen mampu menggunakan model dengan baik",
        "Infrastruktur mendukung implementasi"
    ],
    "5. GAMIFIKASI & ALGORITMA": [
        "Sistem gamifikasi meningkatkan motivasi belajar",
        "Level dan reward mendorong partisipasi",
        "Aktivitas game tidak mengganggu tujuan belajar",
        "Sistem adaptif bekerja dengan baik",
        "Algoritma menentukan jalur belajar secara tepat",
        "Gamifikasi meningkatkan keterlibatan mahasiswa",
        "Sistem memberi pengalaman belajar yang menyenangkan"
    ],
    "6. DAMPAK INSTRUKSIONAL": [
        "Model meningkatkan kemampuan grammar",
        "Model meningkatkan vocabulary",
        "Model meningkatkan speaking ability",
        "Model meningkatkan pemahaman teks",
        "Model meningkatkan kemampuan berpikir logis",
        "Model meningkatkan kemampuan problem solving",
        "Model meningkatkan Computational Thinking"
    ],
    "7. DAMPAK PENGIRING (NURTURANT EFFECTS)": [
        "Model meningkatkan kemandirian belajar",
        "Model meningkatkan motivasi belajar",
        "Model meningkatkan kepercayaan diri",
        "Model meningkatkan keterampilan berpikir kritis",
        "Model meningkatkan literasi digital",
        "Model meningkatkan kemampuan adaptasi belajar"
    ]
}

PERTANYAAN_TERBUKA = [
    "Apa keunggulan utama Smart- English Language Teaching (S- ELT)?",
    "Apa kelemahan model Smart- English Language Teaching (S- ELT) ini?",
    "Apa yang perlu diperbaiki dari model Smart- English Language Teaching (S- ELT)?",
    "Apakah model Smart- English Language Teaching (S- ELT) ini cocok untuk calon guru SD? Jelaskan!",
    "Bagaimana pengalaman Anda menggunakan model Smart- English Language Teaching (S- ELT) ini?"
]

LIKERT_OPTIONS = {
    5: "🤩 Sangat Setuju",
    4: "🙂 Setuju",
    3: "😐 Cukup",
    2: "☹️ Tidak Setuju",
    1: "😡 Sangat Tidak Setuju"
}

@st.cache_data
def get_guide_images():
    imgs = []
    folder = r"d:\Riset_Prof_Herlina\riset_BIMA\prototype_selt\buku_panduan\gambar_aplikasi"
    for i in range(1, 20):
        path = os.path.join(folder, f"{i}.png")
        if os.path.exists(path):
            with open(path, "rb") as f:
                data = base64.b64encode(f.read()).decode()
                imgs.append(f"data:image/png;base64,{data}")
    return imgs

# ==========================================
# STATE MANAGEMENT
# ==========================================
if 'step' not in st.session_state:
    st.session_state.step = 0 # Mulai dari Panduan
if 'data_diri' not in st.session_state:
    st.session_state.data_diri = {}
if 'responses' not in st.session_state:
    st.session_state.responses = {}
if 'essays' not in st.session_state:
    st.session_state.essays = {}

# ==========================================
# FUNCTIONS
# ==========================================
def save_to_gsheet(payload):
    url = st.secrets.get("APPS_SCRIPT_URL", "")
    if not url:
        st.error("Konfigurasi APPS_SCRIPT_URL tidak ditemukan!")
        return False
    try:
        res = requests.post(url, json=payload, timeout=15)
        return res.status_code == 200
    except:
        return False

# ==========================================
# STEP 0: BUKU PANDUAN (FLIPBOOK)
# ==========================================
if st.session_state.step == 0:
    st.markdown('<div class="hero-section"><h1>📖 Buku Panduan S-ELT</h1><p>Geser atau klik untuk membalik halaman panduan</p></div>', unsafe_allow_html=True)
    
    images = get_guide_images()
    
    if images:
        # Flipbook HTML Component
        img_tags = "".join([f'<div class="page"><img src="{img}" style="width:100%; height:100%; object-fit:contain;"></div>' for img in images])
        
        html_code = f"""
        <div id="book-container" style="width: 100%; height: 500px; display: flex; justify-content: center; align-items: center; background: #f1f5f9; border-radius: 15px; overflow: hidden; position: relative;">
            <div id="flipbook" style="width: 320px; height: 450px;">
                {img_tags}
            </div>
        </div>
        <script src="https://cdn.jsdelivr.net/npm/page-flip@2.0.7/dist/js/page-flip.browser.min.js"></script>
        <script>
            const pageFlip = new St.PageFlip(document.getElementById('flipbook'), {{
                width: 320,
                height: 450,
                size: "fixed",
                minWidth: 320,
                maxWidth: 320,
                minHeight: 450,
                maxHeight: 450,
                maxShadowOpacity: 0.5,
                showCover: true,
                mobileScrollSupport: false
            }});
            pageFlip.loadFromHTML(document.querySelectorAll('.page'));
        </script>
        <style>
            .page {{ background-color: white; box-shadow: 0 0 20px rgba(0,0,0,0.1); }}
        </style>
        """
        st.components.v1.html(html_code, height=520)
        
        st.info("💡 **Tips Android**: Gunakan satu jari untuk menggeser ujung halaman buku ke kiri atau kanan.")
    else:
        st.error("Gagal memuat gambar panduan. Pastikan folder gambar tersedia.")

    if st.button("Selesai Membaca & Mulai Mengisi ➔"):
        st.session_state.step = 1
        st.rerun()

# ==========================================
# STEP 1: IDENTITAS
# ==========================================
elif st.session_state.step == 1:
    st.markdown("""
        <div class="hero-section">
            <h1 style="margin-bottom:0;">🎓 ANGKET RESPON MAHASISWA</h1>
            <a href="https://www.s-elt.cloud" style="color: white; text-decoration: none; font-weight: 600; opacity: 0.9;">www.s-elt.cloud</a>
            <p style="margin-top:15px; font-size: 1.1rem;">Evaluasi Model Smart-English Language Teaching (S-ELT)</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.subheader("👤 Identitas Responden")
    
    with st.form("id_form"):
        nama = st.text_input("Nama / Inisial *")
        peran = st.selectbox("Peran", ["Mahasiswa", "Dosen", "Guru", "Lainnya"])
        digital = st.radio("Pernah menggunakan media digital?", ["Ya", "Tidak"], horizontal=True)
        
        col1, col2 = st.columns(2)
        if col1.form_submit_button("⬅ Buka Panduan"):
            st.session_state.step = 0
            st.rerun()
            
        if col2.form_submit_button("Lanjutkan ke Instrumen ➔"):
            if nama.strip():
                st.session_state.data_diri = {
                    "Timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "Nama": nama,
                    "Peran": peran,
                    "Pengalaman_Digital": digital
                }
                st.session_state.step = 2
                st.rerun()
            else:
                st.warning("Mohon isi Nama/Inisial Anda.")

# ==========================================
# STEP 2: INSTRUMEN
# ==========================================
elif st.session_state.step == 2:
    st.title("📝 Instrumen Penilain")
    st.info(f"Responden: **{st.session_state.data_diri['Nama']}**")
    
    with st.form("survey_form"):
        # 1. Likert
        q_count = 1
        all_scores = []
        dim_means = {}
        
        for dimension, items in KUESIONER.items():
            st.markdown(f'<div class="dimension-card">{dimension}</div>', unsafe_allow_html=True)
            dim_scores = []
            for item in items:
                key = f"q_{q_count}"
                val = st.radio(f"{q_count}. {item}", options=[5,4,3,2,1], 
                               format_func=lambda x: LIKERT_OPTIONS[x], key=key, horizontal=True)
                st.session_state.responses[key] = val
                dim_scores.append(val)
                all_scores.append(val)
                q_count += 1
            dim_means[f"Mean_{dimension.split('.')[0]}"] = sum(dim_scores)/len(dim_scores)

        # 2. Open Questions
        st.markdown('<div class="dimension-card">D. PERTANYAAN TERBUKA</div>', unsafe_allow_html=True)
        for i, q in enumerate(PERTANYAAN_TERBUKA):
            key = f"essay_{i}"
            st.session_state.essays[key] = st.text_area(q, key=key)

        col1, col2 = st.columns(2)
        if col1.form_submit_button("⬅ Kembali"):
            st.session_state.step = 1
            st.rerun()
        
        if col2.form_submit_button("🚀 Kirim Evaluasi"):
            # Prepare Payload
            payload = st.session_state.data_diri.copy()
            # Raw Scores
            for k, v in st.session_state.responses.items():
                payload[k] = v
            # Essays
            for i, q in enumerate(PERTANYAAN_TERBUKA):
                payload[f"Essay_{i+1}"] = st.session_state.essays.get(f"essay_{i}", "")
            # Means
            payload["Overall_Mean"] = sum(all_scores)/len(all_scores)
            payload.update(dim_means)
            
            with st.spinner("Mengirim data..."):
                if save_to_gsheet(payload):
                    st.session_state.step = 3
                    st.rerun()
                else:
                    st.error("Gagal mengirim data ke Spreadsheet.")

# ==========================================
# STEP 3: SELESAI
# ==========================================
elif st.session_state.step == 3:
    st.balloons()
    st.markdown(f"""
        <div class="success-card">
            <h1 style="font-size: 4rem;">🥳</h1>
            <h1>Terima Kasih, {st.session_state.data_diri['Nama']}!</h1>
            <p style="font-size: 1.2rem; color: #166534;">Evaluasi Anda terhadap model S-ELT telah kami terima.</p>
            <p>Data Anda telah tersimpan secara real-time untuk analisis lebih lanjut.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Mulai Baru"):
        for k in list(st.session_state.keys()): del st.session_state[k]
        st.rerun()
t.session_state[k]
        st.rerun()
