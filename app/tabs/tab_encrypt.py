"""
Tab: PDF Şifrele / Şifre Çöz
PDF'e parola koyma veya var olan parolayı kaldırma.
"""

import streamlit as st
from app.file_helpers import save_uploaded_file, download_button
from pdf_engine import encrypt_pdf, decrypt_pdf


def render():
    st.header("🔒 PDF Şifrele / Şifre Çöz")

    mode = st.radio(
        "İşlem seçin",
        ["Şifrele (Parola koy)", "Şifre Çöz (Parola kaldır)"],
        key="encrypt_mode",
    )

    uploaded = st.file_uploader("PDF dosyası seçin", type=["pdf"], key="encrypt_upload")

    if not uploaded:
        st.info("Bir PDF dosyası yükleyin.")
        return

    if mode == "Şifrele (Parola koy)":
        password = st.text_input("Parola belirleyin", type="password", key="enc_pass")
        password2 = st.text_input("Parolayı tekrarlayın", type="password", key="enc_pass2")

        if password and password2:
            if password != password2:
                st.warning("Parolalar eşleşmiyor.")
                return

            if st.button("🔒 Şifrele", key="encrypt_btn", type="primary"):
                with st.spinner("Şifreleniyor..."):
                    path = save_uploaded_file(uploaded)
                    try:
                        result = encrypt_pdf(path, password)
                        st.success("PDF şifrelendi!")
                        download_button(result, "📥 Şifrelenmiş PDF'i İndir")
                    except Exception as e:
                        st.error(f"Hata: {e}")
    else:
        password = st.text_input("Mevcut parolayı girin", type="password", key="dec_pass")

        if password and st.button("🔓 Şifre Çöz", key="decrypt_btn", type="primary"):
            with st.spinner("Şifre çözülüyor..."):
                path = save_uploaded_file(uploaded)
                try:
                    result = decrypt_pdf(path, password)
                    st.success("PDF şifresi çözüldü!")
                    download_button(result, "📥 Şifresi Çözülmüş PDF'i İndir")
                except Exception as e:
                    st.error(f"Hata: {e}")
