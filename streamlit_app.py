import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Update Kelompok Kecil", page_icon="👥", layout="wide")

# --- 1. DATABASE ANGGOTA (Daftar 4-8 orang per mentor) ---
data_kelompok = {
    "Pilih Mentor": [],
    "Mentor Andreas": ["Budi Santoso", "Candra Wijaya", "Dedi Kurniawan", "Eka Putri", "Feri Setiawan"],
    "Mentor Sarah": ["Gita Permata", "Hana Maria", "Iwan Setiawan", "Joko Susilo", "Kiki Amelia", "Lusi Ana"],
    "Mentor Yohanes": ["Maman Suherman", "Nana Suryana", "Oki Pratama", "Putri Utami"]
}

# --- 2. KONEKSI ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("👥 Form Update Mingguan Kelompok Kecil")
st.info("Pilih nama Anda, lalu isi update untuk setiap anggota di bawah ini.")

# --- 3. PILIHAN MENTOR ---
col1, col2 = st.columns(2)
with col1:
    mentor = st.selectbox("Nama Mentor/Pemimpin", options=list(data_kelompok.keys()))
with col2:
    tanggal = st.date_input("Tanggal Pertemuan", date.today())

st.divider()

# --- 4. FORM UPDATE MASSAL ---
if mentor != "Pilih Mentor":
    with st.form("form_massal", clear_on_submit=True):
        daftar_anggota = data_kelompok[mentor]
        list_update = []

        st.subheader(f"Update Anggota Kelompok {mentor}")
        
        # Membuat baris input untuk SETIAP anggota
        for nama in daftar_anggota:
            with st.expander(f"📍 Update untuk: {nama}", expanded=True):
                c1, c2, c3 = st.columns([2, 2, 4])
                with c1:
                    hadir = st.selectbox(f"Kehadiran", ["Hadir", "Izin", "Sakit", "Alpa"], key=f"h_{nama}")
                with c2:
                    kondisi = st.select_slider(f"Spritual", 
                                             options=["Kritis", "Lemah", "Stabil", "Bertumbuh", "Baik"], 
                                             value="Stabil", key=f"s_{nama}")
                with c3:
                    catatan = st.text_input(f"Catatan/Pokok Doa", key=f"c_{nama}")
                
                # Simpan data sementara ke dalam list
                list_update.append({
                    "Tanggal": str(tanggal),
                    "Mentor": mentor,
                    "Anggota": nama,
                    "Kehadiran": hadir,
                    "Kondisi": kondisi,
                    "Catatan": catatan
                })

        st.divider()
        submit = st.form_submit_button("Simpan Semua Update Anggota", type="primary")

        if submit:
            try:
                # Ambil data lama dari Google Sheets
                existing_data = conn.read(worksheet="Data_Update", ttl=0)
                
                # Ubah list update tadi menjadi DataFrame
                new_data_df = pd.DataFrame(list_update)
                
                # Gabungkan data lama dengan data baru (semua anggota sekaligus)
                updated_df = pd.concat([existing_data, new_data_df], ignore_index=True)
                
                # Update ke Google Sheets
                conn.update(worksheet="Data_Update", data=updated_df)
                
                st.success(f"✅ Berhasil! Update untuk {len(list_update)} anggota telah tersimpan.")
                st.balloons()
            except Exception as e:
                st.error(f"Gagal menyimpan: Pastikan Tab 'Data_Update' sudah ada di Google Sheets. Error: {e}")
else:
    st.warning("Silakan pilih Nama Mentor untuk memunculkan daftar anggota.")
