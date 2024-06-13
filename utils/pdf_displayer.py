import streamlit as st
import base64


# Function to display PDF in Streamlit
def displayPDF(pdf_bytes):
    # Directly encode the bytes object to base64
    base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)
