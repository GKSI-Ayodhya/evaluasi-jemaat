import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Sistem Follow-up Jemaat", layout="centered")

# 1. Koneksi ke Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Ambil Daftar Nama dari Google Sheets (Tab: Daftar_Nama)
# Kita pakai Try-Except agar aplikasi tidak error jika Sheets belum siap
try:
    df_nama = conn.read(worksheet="Daftar_Nama")
    list_mentor = df_nama['Mentor'].unique().tolist()
except:
    st.error("Gagal membaca tab 'Daftar_Nama'. Pastikan Anda sudah membuat tab tersebut di Google Sheets dan mengatur Secrets!")
    st.stop()

st.title("🙏 Form Evaluasi Kelompok Kecil")

# 3. Form Input
with st.form("main_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        mentor_terpilih = st.selectbox("Pilih Nama Mentor", options=list_mentor)
        tanggal = st.date_input("Tanggal", date.today())
    
    with col2:
        filter_anggota = df_nama[df_nama['Mentor'] == mentor_terpilih]['Anggota'].tolist()
        anggota_terpilih = st.selectbox("Pilih Nama Anggota", options=filter_anggota)
        status = st.selectbox("Status", ["Rutin", "Urgent", "Sakit"])

    st.divider()
    kondisi = st.select_slider("Kondisi Spiritual", 
                              options=["Kritis", "Lemah", "Stabil", "Bertumbuh", "Baik"])
    catatan = st.text_area("Catatan / Pokok Doa")

    submit = st.form_submit_button("Simpan Laporan")

    if submit:
        old_data = conn.read(worksheet="Data_Update")
        new_entry = pd.DataFrame([{
            "Tanggal": str(tanggal),
            "Mentor": mentor_terpilih,
            "Anggota": anggota_terpilih,
            "Kondisi": kondisi,
            "Catatan": catatan
        }])
        updated_df = pd.concat([old_data, new_entry], ignore_index=True)
        conn.update(worksheet="Data_Update", data=updated_df)
        st.success(f"Laporan untuk {anggota_terpilih} telah tersimpan!")
