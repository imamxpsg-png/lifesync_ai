import streamlit as st
from groq import Groq
import json
import pandas as pd
import os
from datetime import datetime
# Mengimpor pustaka pembaca file .env untuk keamanan API Key
from dotenv import load_dotenv

# Memuat variabel rahasia dari file .env secara otomatis
load_dotenv()

# ==================== PENGATURAN ADMIN VIA .ENV ====================
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "openai/gpt-oss-20b"

# ==================== KONFIGURASI HALAMAN ====================
st.set_page_config(
    page_title="WhatsApp Web - LifeSync", 
    page_icon="💬", 
    layout="centered"
)

# 🔥 FIX TOTAL: MENGHAPUS PAKSA KOTAK ABU-ABU STREAMLIT & PERBAIKAN STRUKTUR CSS
st.markdown("""
    <style>
    /* Menyembunyikan elemen dekoratif bawaan Streamlit agar bersih total */
    #MainMenu, footer, header {visibility: hidden;}
    .block-container { max-width: 700px; padding-top: 0.5rem; padding-bottom: 0.5rem; }
    
    div[data-testid="stVerticalBlock"] > div {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
    }
    
    /* MENGHAPUS BACKGROUND ABU-ABU KAKU BAWAAN WIDGET STREAMLIT */
    div[data-testid="stTabs"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
    }
    div[data-testid="stTabs"] [data-baseweb="tab-panel"] {
        background: transparent !important;
        padding: 0px !important;
    }

    /* Wadah Utama Ruang Obrolan WhatsApp (Lebar Penuh & Bersih) */
    .chat-container {
        display: flex !important;
        flex-direction: column !important;
        gap: 12px !important;
        padding: 20px 15px !important;
        background-color: #efeae2 !important; 
        background-image: url('https://githubusercontent.com') !important; 
        background-repeat: repeat !important;
        border-radius: 12px 12px 0px 0px !important;
        height: 480px !important;
        overflow-y: auto !important;
        border: 1px solid #e9edef !important;
        border-bottom: none !important;
        margin-top: 10px !important;
        box-sizing: border-box !important;
    }
    
    /* Pengaturan Baris Obrolan Kanan (User) & Kiri (AI) */
    .chat-row {
        display: flex !important;
        width: 100% !important;
        margin: 4px 0px !important;
        background: transparent !important;
    }
    .user-row { justify-content: flex-end !important; }
    .ai-row { justify-content: flex-start !important; }
    
    /* Gelembung Pesan Khas WA Web */
    .wa-bubble {
        padding: 8px 12px 6px 12px !important;
        border-radius: 7.5px !important;
        max-width: 75% !important;
        font-size: 14.5px !important;
        line-height: 1.45;
        color: #111b21 !important;
        box-shadow: 0 1px 0.5px rgba(11,20,26,.13) !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    }
    .user-bubble {
        background-color: #d9fdd3 !important;
        border-top-right-radius: 0px !important;
        text-align: left !important;
    }
    .ai-bubble {
        background-color: #ffffff !important;
        border-top-left-radius: 0px !important;
        text-align: left !important;
    }
    
    /* Indikator Jam Waktu & Centang Biru WA */
    .wa-meta {
        font-size: 10px !important;
        color: #667781 !important;
        float: right !important;
        margin-top: 4px !important;
        margin-left: 8px !important;
        display: flex !important;
        align-items: center !important;
        gap: 2px !important;
    }
    .wa-ticks { color: #53bdeb !important; font-weight: bold !important; }

    /* Bar Pengetikan Kaki Bawah Sempurna */
    .wa-input-footer-bar {
        background-color: #f0f2f5 !important;
        padding: 12px 16px !important;
        border-radius: 0px 0px 12px 12px !important;
        border: 1px solid #e9edef !important;
        border-top: none !important;
        margin-bottom: 20px !important;
    }

    /* Custom Card Bersih untuk Halaman Keuangan */
    .fin-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e9edef;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        margin-bottom: 15px;
    }
    
    /* Tombol Kirim Kustom */
    .stButton>button {
        width: 100% !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 7px 0px !important;
        transition: all 0.2s ease !important;
    }
    .stButton>button:hover {
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1) !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== FUNGSI LOGIKA DATABASE MULTI-USER CLOUD SECURE ====================
def get_user_filepaths(user_id, password):
    """Menghasilkan nama file unik gabungan ID dan Password agar tidak bisa ditembus user lain di Cloud"""
    combined_string = f"{user_id}_{password}"
    safe_id = "".join(c for c in combined_string if c.isalnum() or c in ("_", "-")).lower()
    return f"{safe_id}_keuangan.xlsx", f"{safe_id}_diary.xlsx"

def load_excel_data(file_name):
    if os.path.exists(file_name):
        try: return pd.read_excel(file_name).to_dict(orient="records")
        except Exception: return []
    return []

def save_to_excel(data, file_name):
    df = pd.DataFrame(data)
    df.to_excel(file_name, index=False)
# ==================== MENU AUTENTIKASI AKUN SECURE (SIDEBAR LOGIN MULTI-DEVICE CLOUD) ====================
st.sidebar.title("🔐 Akses Akun Secure")
st.sidebar.write("ID dan Password digabungkan sebagai kunci database unik Anda di server cloud.")

if "active_user_id" not in st.session_state:
    st.session_state.active_user_id = ""
if "active_user_pwd" not in st.session_state:
    st.session_state.active_user_pwd = ""

user_id_input = st.sidebar.text_input(
    "Masukkan ID Akun/Nama Anda:", 
    value=st.session_state.active_user_id,
    placeholder="Contoh: budi123, ani_smk",
    key="txt_login_id"
)

user_pwd_input = st.sidebar.text_input(
    "Masukkan Password Rahasia Anda:", 
    value=st.session_state.active_user_pwd,
    type="password",
    placeholder="Contoh: rahasia123",
    key="txt_login_pwd"
)

if st.sidebar.button("Masuk / Ganti Akun", key="btn_login_submit"):
    if user_id_input.strip() and user_pwd_input.strip():
        st.session_state.active_user_id = user_id_input.strip()
        st.session_state.active_user_pwd = user_pwd_input.strip()
        # Bersihkan sesi memori lama agar berganti ke database user baru
        st.session_state.pop("pengeluaran", None)
        st.session_state.pop("diary_history", None)
        st.toast(f"Berhasil masuk sebagai: {st.session_state.active_user_id}", icon="🚀")
        st.rerun()
    else:
        st.sidebar.error("ID Akun dan Password tidak boleh kosong!")

if st.session_state.active_user_id:
    if st.sidebar.button("🚪 Keluar (Logout)", key="btn_logout"):
        st.session_state.active_user_id = ""
        st.session_state.active_user_pwd = ""
        st.session_state.pop("pengeluaran", None)
        st.session_state.pop("diary_history", None)
        st.rerun()

st.sidebar.write("---")

# ==================== MANAGEMEN DATA BERDASARKAN USER AKTIF ====================
if st.session_state.active_user_id and st.session_state.active_user_pwd:
    # Mengunci nama file gabungan ID + Password unik
    EXCEL_FINANCE, EXCEL_DIARY = get_user_filepaths(st.session_state.active_user_id, st.session_state.active_user_pwd)
    
    if "pengeluaran" not in st.session_state:
        st.session_state.pengeluaran = load_excel_data(EXCEL_FINANCE)
    if "diary_history" not in st.session_state:
        st.session_state.diary_history = load_excel_data(EXCEL_DIARY)
        
    saldo_awal_total = sum(item['jumlah'] for item in st.session_state.pengeluaran if item['tipe'] == 'Pemasukan/Modal')
    total_terpakai = sum(item['jumlah'] for item in st.session_state.pengeluaran if item['tipe'] == 'Pengeluaran')
    sisa_saldo = saldo_awal_total - total_terpakai
else:
    st.session_state.pengeluaran = []
    st.session_state.diary_history = []
    saldo_awal_total = 0.0
    total_terpakai = 0.0
    sisa_saldo = 0.0

st.sidebar.title("💬 Web Menu")
halaman_aktif = st.sidebar.radio(
    "Pindah Ruang Chat:",
    ["💰 1. Asisten Finansial", "🌱 2. Cult Jurnal (Chat WA)", "📊 3. Pusat Unduhan Berkas"]
)

# -------------------- HALAMAN 1: ASISTEN FINANSIAL --------------------
if halaman_aktif == "💰 1. Asisten Finansial":
    st.title("💰 Pelacakan Finansial & AI Planner")
    st.write("---")
    
    if not st.session_state.active_user_id:
        st.warning("🔒 Silakan masukkan ID Akun & Password Anda terlebih dahulu di sidebar sebelah kiri untuk membuka data keuangan.")
    else:
        st.caption(f"Akun Aktif: **{st.session_state.active_user_id}**")
        
        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        st.write("**💵 Input Saldo Utama (Uang Saku)**")
        c_dana1, c_dana2 = st.columns(2)
        with c_dana1:
            input_modal = st.number_input("Tambah Uang Saku Baru (Rp):", min_value=0.0, step=50000.0, key="num_m")
        with c_dana2:
            st.write("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
            btn_modal = st.button("Tambah", key="btn_m")
        
        if btn_modal and input_modal > 0:
            st.session_state.pengeluaran.append({
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "keterangan": "Uang Saku Bulanan (Modal)", 
                "jumlah": input_modal, 
                "tipe": "Pemasukan/Modal"
            })
            save_to_excel(st.session_state.pengeluaran, EXCEL_FINANCE)
            st.toast("Dana saku berhasil dicatat!", icon="💵")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.metric(label="📊 Sisa Saldo Aktif Anda Saat Ini:", value=f"Rp {sisa_saldo:,.0f}")
        
        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        st.write("**📝 Catat Transaksi Pengeluaran**")
        c1, c2, c3 = st.columns([2, 1.5, 1])
        with c1:
            input_ket = st.text_input("Keterangan Belanja", placeholder="Contoh: Makan siang, buku kuliah", key="txt_k")
        with c2:
            input_nominal = st.number_input("Nominal Belanja (Rp)", min_value=0.0, step=5000.0, key="num_n")
        with c3:
            st.write("<div style='padding-top:28px;'></div>", unsafe_allow_html=True)
            btn_tambah = st.button("Catat", key="btn_a")
            
        if btn_tambah and input_ket and input_nominal > 0:
            st.session_state.pengeluaran.append({
                "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "keterangan": input_ket, 
                "jumlah": input_nominal, 
                "tipe": "Pengeluaran"
            })
            save_to_excel(st.session_state.pengeluaran, EXCEL_FINANCE)
            st.toast("Pengeluaran belanja disimpan!", icon="✅")
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="fin-card">', unsafe_allow_html=True)
        st.write("**🤖 Rencana Finansial AI**")
        user_fin_query = st.text_area("Tanyakan strategi anggaran pada AI:", placeholder="Bagaimana menghemat sisa saldo saya?", key="query_fin")
        if st.button("Rencanakan Keuangan", key="btn_ai_fin"):
            if user_fin_query:
                with st.spinner("AI sedang menghitung strategi..."):
                    try:
                        client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
                        if client:
                            data_konteks = f"Modal: Rp {saldo_awal_total:,.0f} | Sisa: Rp {sisa_saldo:,.0f} | Log: {json.dumps(st.session_state.pengeluaran)}"
                            chat_completion = client.chat.completions.create(
                                messages=[
                                    {"role": "system", "content": "You are a professional financial planner. Answer in Indonesian language."},
                                    {"role": "user", "content": f"{data_konteks}\n\nPertanyaan: {user_fin_query}"}
                                ],
                                model=MODEL_NAME,
                            )
                            st.markdown(chat_completion.choices[0].message.content)
                        else:
                            st.error("API Key tidak ditemukan di file .env Anda!")
                    except Exception as e: st.error(f"Error AI: {e}")
        st.markdown('</div>', unsafe_allow_html=True)
# -------------------- HALAMAN 2: KONSULTAN PSIKOLOGI (CHAT WA BERSIH & TERKUNCI) --------------------
# 🔥 PERBAIKAN MUTLAK: Menyinkronkan label string elif dengan teks radio sidebar secara presisi
elif halaman_aktif == "🌱 2. Cult Jurnal (Chat WA)":
    st.title("🌱 WhatsApp Web - Mind Care Counselor")
    st.write("---")
    
    if not st.session_state.active_user_id or not st.session_state.active_user_pwd:
        st.warning("🔒 Silakan masukkan ID Akun & Password Anda terlebih dahulu di sidebar sebelah kiri untuk membuka ruang obrolan curhat.")
    else:
        st.caption(f"Akun Aktif: **{st.session_state.active_user_id}**")
        
        # 🗂️ JENDELA UTAMA RUANG OBROLAN WHATSAPP (KOTAK WALLPAPER UTUH)
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        
        if st.session_state.diary_history:
            # Mengurutkan riwayat agar chat terlama di atas dan chat terbaru di bawah
            for chat in reversed(st.session_state.diary_history):
                waktu_format = chat['Waktu'][-8:-3] if 'Waktu' in chat else "11:47"
                
                # 🟢 Tampilkan Gelembung Kanan (User / Kamu)
                if chat.get('Cerita User'):
                    st.markdown(f"""
                        <div class="chat-row user-row">
                            <div class="wa-bubble user-bubble">
                                {chat['Cerita User']}
                                <div class="wa-meta">
                                    {waktu_format} <span class="wa-ticks">✓✓</span>
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
                
                # ⚪ Tampilkan Gelembung Kiri (AI / Counselor) - DIKUNCI DI DALAM KONTEN WALLPAPER
                if chat.get('Respon AI'):
                    st.markdown(f"""
                        <div class="chat-row ai-row">
                            <div class="wa-bubble ai-bubble">
                                {chat['Respon AI']}
                                <div class="wa-meta">
                                    {waktu_format}
                                </div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div style="display:flex; justify-content:center; align-items:center; height:100%; color:#667781; font-size:14px; font-family:sans-serif;">
                    Belum ada percakapan. Mulai ketik pesan pertama Anda di bawah!
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True) # Kunci Penutup chat-container (Tag div aman berada di luar perulangan)
        # 📥 BAR INPUT PENGISI TEKS DI BAWAH CHAT ROOM (MURNI MENYAMPING SECARA SEIMBANG)
        st.markdown('<div class="wa-input-footer-bar">', unsafe_allow_html=True)
        col_mic, col_input, col_btn = st.columns([0.5, 5, 0.7])
        
        with col_mic:
            audio_file = None
            try:
                if hasattr(st, "audio_input"): audio_file = st.audio_input("🎙️", label_visibility="collapsed")
                elif hasattr(st, "experimental_audio_input"): audio_file = st.experimental_audio_input("🎙️", label_visibility="collapsed")
            except Exception: st.write("🎙️")
            
        with col_input:
            user_msg = st.text_input("Bar Pesan WA", placeholder="📎 📝 Type a message...", label_visibility="collapsed", key="wa_text_input_bar_clean_final")
            
        with col_btn:
            submit_msg = st.button("🚀", key="wa_send_btn_clean_final")
        st.markdown('</div>', unsafe_allow_html=True) # Penutup wa-input-footer-bar
                
        if submit_msg:
            teks_final = user_msg
            client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None
            
            # Proses translasi rekaman audio jika ada berkas dari Microphone
            if audio_file is not None and not user_msg and client:
                with st.spinner("Mengonversi suara..."):
                    try:
                        transcript = client.audio.transcriptions.create(model="whisper-large-v3", file=audio_file)
                        teks_final = transcript.text
                    except Exception as e: st.error(f"Gagal memproses audio: {e}")
                    
            if teks_final and client:
                with st.spinner("AI sedang mengetik..."):
                    try:
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": "You are a friendly Indonesian AI student counselor. If user asks general factual questions: answer accurately. If venting/sad: motivate warmly. If highly stressed: validate, motivate, and give 3 actionable steps to reduce stress. If giving medical advice, you must follow clinical safety guidelines by listing 3 distinct treatment possibilities and adding a clear medical disclaimer."},
                                {"role": "user", "content": teks_final}
                            ],
                            model=MODEL_NAME,
                        )
                        # 🔥 FIX ERROR LIST: Mengakses indeks [0] dari properti choices sebelum memanggil message
                        ai_response = chat_completion.choices[0].message.content
                        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        
                        st.session_state.diary_history.insert(0, {
                            "Waktu": waktu_sekarang,
                            "Cerita User": teks_final, 
                            "Respon AI": ai_response
                        })
                        save_to_excel(st.session_state.diary_history, EXCEL_DIARY)
                        st.rerun()
                    except Exception as e: st.error(f"Error AI: {e}")
            elif not client:
                st.error("Fitur AI tidak aktif karena API Key belum diisi di file .env.")

# -------------------- HALAMAN 3: PUSAT UNDUHAN BERKAS --------------------
elif halaman_aktif == "📊 3. Pusat Unduhan Berkas":
    st.title("📊 Pusat Ekspor Dokumen Resmi")
    st.write("Unduh ringkasan transaksi finansial dan berkas percakapan psikolog Anda.")
    st.write("---")
    
    if not st.session_state.active_user_id or not st.session_state.active_user_pwd:
        st.warning("🔒 Silakan masukkan ID Akun & Password Anda terlebih dahulu di sidebar sebelah kiri untuk membuka pusat unduhan berkas.")
    else:
        st.caption(f"Akun Aktif: **{st.session_state.active_user_id}**")
        
        st.subheader("💰 1. Unduh Laporan Keuangan (Excel)")
        if st.session_state.pengeluaran:
            df_fin = pd.DataFrame(st.session_state.pengeluaran)
            st.dataframe(df_fin, use_container_width=True)
            try:
                with open(EXCEL_FINANCE, "rb") as f:
                    st.download_button(label=f"📥 Download Keuangan ({st.session_state.active_user_id}).xlsx", data=f, file_name=f"Laporan_Keuangan_{st.session_state.active_user_id}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception: pass
        else: st.info("Belum ada riwayat keuangan.")

        st.write("---")
        st.subheader("📝 2. Unduh Hasil Konsultasi (Word & Excel)")
        if st.session_state.diary_history:
            df_diary = pd.DataFrame(st.session_state.diary_history)
            st.dataframe(df_diary, use_container_width=True)
            
            # Ekspor Berkas Microsoft Word (.docx)
            try:
                from docx import Document
                doc = Document()
                doc.add_heading(f'RIWAYAT KONSULTASI MAHASISWA - USER: {st.session_state.active_user_id.upper()}', 0)
                for log in reversed(st.session_state.diary_history):
                    p = doc.add_paragraph()
                    p.add_run(f"📅 Waktu: {log['Waktu']}\n").bold = True
                    p.add_run(f"👤 Kamu: {log['Cerita User']}\n")
                    p.add_run(f"🤖 AI: {log['Respon AI']}\n")
                    doc.add_paragraph("-" * 40)
                
                word_file_name = f"Riwayat_Konsultasi_{st.session_state.active_user_id}.docx"
                doc.save(word_file_name)
                
                with open(word_file_name, "rb") as f_word:
                    st.download_button(label="📥 Download Consult (.docx / Word)", data=f_word, file_name=word_file_name, mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            except Exception as e: st.warning(f"Jalankan 'pip install python-docx' untuk ekspor Word. Log: {e}")
                
            try:
                with open(EXCEL_DIARY, "rb") as f_excel:
                    st.download_button(label=f"📥 Download Consult ({st.session_state.active_user_id}).xlsx", data=f_excel, file_name=f"Riwayat_Konsultasi_{st.session_state.active_user_id}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            except Exception: pass
        else: st.info("Belum ada riwayat chat.")
