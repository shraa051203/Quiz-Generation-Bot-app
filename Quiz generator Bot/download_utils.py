import streamlit as st

def show_pdf_download_button(pdf_path, label="📥 Download Quiz as PDF", filename="quiz_export.pdf"):
    try:
        with open(pdf_path, "rb") as f:
            st.download_button(
                label=label,
                data=f,
                file_name=filename,
                mime="application/pdf"
            )
    except Exception as e:
        st.error(f"❌ Error generating download: {e}")
