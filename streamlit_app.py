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
    # --- 5. UPDATE JEMAAT LUAR GRUP (OPSIONAL) ---
st.divider()
with st.expander("➕ Berikan Update untuk Jemaat di Luar Grup Anda"):
    with st.form("form_tambahan", clear_on_submit=True):
        # Mengambil semua nama jemaat dari semua mentor untuk pilihan dropdown
        semua_jemaat = []
        for anggota_list in data_kelompok.values():
            semua_jemaat.extend(anggota_list)
        semua_jemaat = sorted(list(set(semua_jemaat))) # Urutkan dan hapus duplikat

        st.info("Gunakan bagian ini jika Anda ingin meng-update jemaat dari kelompok lain.")
        
        # Pilihan nama jemaat (bisa pilih dari daftar atau ketik sendiri)
        nama_pilihan = st.selectbox("Pilih Nama Jemaat (Lintas Grup):", ["-- Ketik Nama Baru --"] + semua_jemaat)
        
        if nama_pilihan == "-- Ketik Nama Baru --":
            nama_jemaat_final = st.text_input("Ketik Nama Jemaat Baru:")
        else:
            nama_jemaat_final = nama_pilihan

        c1, c2, c3 = st.columns([2, 2, 4])
        with c1:
            h_tambahan = st.selectbox("Jenis Followup", ["Meetup", "By Call", "By Chat/Whatsapp", "None"], key="h_extra")
        with c2:
            k_tambahan = st.select_slider("Kondisi Spiritual", options=["Kritis", "Lemah", "Stabil", "Bertumbuh", "Baik"], value="Stabil", key="k_extra")
        with c3:
            c_tambahan = st.text_input("Catatan/Pokok Doa", key="c_extra")

        submit_extra = st.form_submit_button("Simpan Update Tambahan", type="secondary")

        if submit_extra:
            if not nama_jemaat_final or nama_jemaat_final == "-- Ketik Nama Baru --":
                st.error("Mohon isi nama jemaat.")
            else:
                try:
                    # Proses simpan (sama dengan yang di atas)
                    existing_data = conn.read(worksheet="Data_Update", ttl=0)
                    new_entry = pd.DataFrame([{
                        "Tanggal": str(tanggal),
                        "Mentor": f"{mentor} (Cross-Update)", # Menandai bahwa ini update lintas grup
                        "Anggota": nama_jemaat_final,
                        "Jenis Followup": h_tambahan,
                        "Kondisi Spiritual": k_tambahan,
                        "Catatan": c_tambahan
                    }])
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    conn.update(worksheet="Data_Update", data=updated_df)
                    st.success(f"Berhasil menyimpan update untuk {nama_jemaat_final}")
                except Exception as e:
                    st.error(f"Gagal simpan: {e}")