import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import date

st.set_page_config(page_title="Update Kelompok Kecil", page_icon="👥", layout="wide")

# --- 1. DATABASE ANGGOTA (Daftar 4-8 orang per mentor) ---
data_kelompok = {
    "Pilih Mentor": [],

        "Edy Siregar": ["Aji Eka", "Aji Kezia", "Jhon T", "Michael T", "Noverio"],
            "Dea": ["Hanny", "Hedva", "Helvin", "Naomi", "Shindy BC"],
                "Doddy K": ["Andi", "Richard", "Samuel Rizkia", "Samuel Dwiky"],
                    "Martin": ["Ardo", "Archius", "Dustin", "Jefa", "Yunus"],
                        "Nike": ["Eva Sihombing", "Chintya", "Sinta Debataraja", "Sin Thia", "Ruth Angelina"],
                            "Rio": ["Frans Sihombing", "Josep STTS", "Luki", "Ravi"],
                                "Ruth H": ["Cindy", "Junita", "Maria", "Peggy", "Vina", "Yustina"],
                                    "Saida": ["Christine", "Jelita", "Mariany", "Messya", "Rachel", "Sandra", "Yosi"],
                                        "Sylva": ["Anggie", "Angelin BC", "Erlin Law", "Helmi", "Kezia", "Murni", "Sarah"],
                                            "Uhin": ["Mattew", "Oki", "Steven", "Zulfan"]
                                            }

# --- 2. KONEKSI ---
conn = st.connection("gsheets", type=GSheetsConnection)

st.title("👥 Form Update Mingguan Kelompok Kecil")
st.info("Pilih nama Anda, lalu isi update untuk setiap anggota di bawah ini.")

 # --- 3. PILIHAN MENTOR ---
col1, col2 = st.columns(2)
with col1:
    mentor = st.selectbox("Nama Mentor/Pemimpin Kelompok", options=list(data_kelompok.keys()))
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
                hadir = st.selectbox(f"Jenis Followup", ["Meetup", "By Call", "By Chat/Whatapps", "Belum difollowup"], key=f"h_{nama}")
            with c2:
                kondisi = st.select_slider(f"Kondisi Spritual", 
                options=["Kritis", "Lemah", "Stabil", "Bertumbuh", "Baik"], 
                value="Stabil", key=f"s_{nama}")
            with c3:
                catatan = st.text_input(f"Catatan/Pokok Doa", key=f"c_{nama}")
                                                                                                                                                                                                                                                                                                                                                            
            # Simpan data sementara ke dalam list
            list_update.append({
            "Tanggal": str(tanggal),
            "Mentor": mentor,
            "Anggota": nama,
            "Jenis Followup": hadir,
            "Kondisi": kondisi,
            "Catatan": catatan
            })
        # ... (akhir dari loop jemaat grup) ...
        # Pastikan kode di bawah ini sejajar dengan kata 'for' di atasnya

        st.write("---")
        with st.expander("➕ Tambahkan Update untuk Jemaat di Luar Grup Anda (Opsional)"):
            st.info("Gunakan bagian ini jika ada jemaat lain yang ingin Anda update kondisinya.")
            
            # Ambil semua jemaat untuk pilihan
            semua_jemaat = []
            for anggota_list in data_kelompok.values():
                semua_jemaat.extend(anggota_list)
            semua_jemaat = sorted(list(set(semua_jemaat)))

            c_extra_1, c_extra_2 = st.columns([1, 1])
            with c_extra_1:
                pilihan_nama = st.selectbox("Pilih Nama Jemaat:", ["-- Pilih / Ketik Baru --"] + semua_jemaat, key="pilih_extra")
            with c_extra_2:
                nama_manual = st.text_input("Atau Ketik Nama Baru:", key="nama_manual")

            ce1, ce2, ce3 = st.columns([2, 2, 4])
            with ce1:
                h_extra = st.selectbox("Jenis Followup", ["Meetup", "By Call", "By Chat/Whatsapp", "None"], key="h_ex")
            with ce2:
                k_extra = st.select_slider("Kondisi Spiritual", options=["Kritis", "Lemah", "Stabil", "Bertumbuh", "Baik"], value="Stabil", key="k_ex")
            with ce3:
                c_extra = st.text_input("Catatan/Pokok Doa", key="c_ex")

        st.divider()
        submit = st.form_submit_button("Simpan Semua Update Anggota", type="primary")

    if submit:
        # TENTUKAN NAMA EXTRA JEMAAT
        nama_extra = nama_manual if nama_manual else (pilihan_nama if pilihan_nama != "-- Pilih / Ketik Baru --" else None)
        
        # Jika ada nama extra, masukkan ke daftar update sebelum disimpan
        if nama_extra:
            list_update.append({
                "Tanggal": str(tanggal),
                "Mentor": f"{mentor} (Cross-Update)",
                "Anggota": nama_extra,
                "Jenis Followup": h_extra,
                "Kondisi Spiritual": k_extra,
                "Catatan": c_extra
            })
            
        
            # ... (proses simpan seperti biasa) ...
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