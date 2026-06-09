import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "data_mahasiswa" not in st.session_state:
    st.session_state.data_mahasiswa = {
        'Nama': ['Fatur', 'Arkhan', 'Galih', 'Sergio', 'Rival'],
        'Kelas': ['XI TKJ', 'XI TKJ', 'XI TKJ', 'XI TKJ', 'XI TKJ'],
        'Nilai': [90, 85, 90, 92, 88]
    }

if not st.session_state.logged_in:
    st.title('Login')
    st.write('Username: Fatur, Password: 1234')
    username = st.text_input('Username:')
    password = st.text_input('Password:', type='password')
    if st.button('Login', use_container_width=True):
        if username == '' and password == '':
            st.warning('Masukkan Username dan Password')
        elif username == 'Fatur' and password == '1234':
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error('Login Gagal')

else:
    st.sidebar.markdown("## ALPROGG App")
    st.sidebar.markdown("**SMK Telkom 2 Medan**")
    st.sidebar.divider()
    menu = st.sidebar.selectbox('Pilih Menu', ['Home', 'Data', 'Grafik', 'Cari & Filter', 'Download', 'About'])

    if st.sidebar.button('Logout', use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

    df = pd.DataFrame(st.session_state.data_mahasiswa)

    if menu == 'Home':
        st.title('Selamat Datang!')
        st.success('Login Berhasil, Fatur Rahman')
        col1, col2, col3 = st.columns(3)
        col1.metric('Total Siswa', len(df))
        col2.metric('Nilai Tertinggi', df['Nilai'].max())
        col3.metric('Nilai Terendah', df['Nilai'].min())

    elif menu == 'Data':
        st.title('Data Siswa')

        st.header('Tambah Data')
        with st.form('form_input'):
            nama_input = st.text_input('Nama:')
            kelas_input = st.selectbox('Kelas:', ['XI TKJ1', 'XI TKJ2', 'XI TKJ3'])
            nilai_input = st.number_input('Nilai:', min_value=0, max_value=100)
            submit = st.form_submit_button('Simpan', use_container_width=True)

        if submit:
            if nama_input == '':
                st.warning('Nama Tidak Boleh Kosong')
            else:
                st.session_state.data_mahasiswa['Nama'].append(nama_input)
                st.session_state.data_mahasiswa['Kelas'].append(kelas_input)
                st.session_state.data_mahasiswa['Nilai'].append(int(nilai_input))
                st.success(f'Data {nama_input} berhasil ditambahkan!')
                st.rerun()

        st.header('Tabel Data')
        st.dataframe(df, use_container_width=True)

        st.header('Statistik Nilai')
        col1, col2, col3 = st.columns(3)
        col1.metric('Rata-rata', round(df['Nilai'].mean(), 1))
        col2.metric('Tertinggi', df['Nilai'].max())
        col3.metric('Terendah', df['Nilai'].min())

        st.header('Import CSV')
        file = st.file_uploader('Upload File CSV', type=['csv'])
        if file is not None:
            df_csv = pd.read_csv(file)
            st.success('File berhasil diupload!')
            st.dataframe(df_csv, use_container_width=True)
        else:
            st.info('Silakan upload file CSV')

    elif menu == 'Grafik':
        st.title('Visualisasi Grafik')
        df = pd.DataFrame(st.session_state.data_mahasiswa)
        fig1 = px.bar(df, x='Nama', y='Nilai')
        st.plotly_chart(fig1, use_container_width=True)
        fig2 = px.line(df, x='Nama', y='Nilai', markers=True)
        st.plotly_chart(fig2, use_container_width=True)
        fig3 = px.pie(df, names='Nama', values='Nilai')
        st.plotly_chart(fig3, use_container_width=True)
    
    elif menu == 'Cari & Filter':
        st.title('Cari & Filter Data')
        search = st.text_input('Cari nama:')
        if search:
            hasil = df[df['Nama'].str.contains(search, case=False)]
            st.dataframe(hasil, use_container_width=True)
        else:
            kelas_filter = st.selectbox('Filter Kelas:', ['Semua'] + list(df['Kelas'].unique()))
            if kelas_filter == 'Semua':
                st.dataframe(df, use_container_width=True)
            else:
                st.dataframe(df[df['Kelas'] == kelas_filter], use_container_width=True)

    elif menu == 'Download':
        st.title('Download Data')
        st.dataframe(df, use_container_width=True)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button('Download CSV', data=csv, file_name='data_mahasiswa.csv', mime='text/csv', use_container_width=True)

    elif menu == 'About':
        st.title('About')
        st.write('Nama  : Fatur Rahman')
        st.write('Kelas : XI TKJ')
        st.write('Tugas : Formatif Akhir ALPROG')
