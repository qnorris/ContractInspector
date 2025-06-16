import PyPDF2
import streamlit as st
import re
from typing import Dict, Tuple

# ----------------------------
# Page configuration
# ----------------------------
st.set_page_config(
    page_title="LegalGuard AI", 
    page_icon="⚖️",
    layout="wide"
)

# ----------------------------
# Authentication state
# ----------------------------
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# ----------------------------
# Password Protection
# ----------------------------
if not st.session_state.authenticated:
    st.title("🔒 Authentication Required")
    password_input = st.text_input("Enter password:", type="password")

    if st.button("Submit"):
        if password_input == "102938":  # 🔐 Set your password here
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
            st.stop()
    else:
        st.stop()

# ----------------------------
# PDF Text Extraction
# ----------------------------
def extract_pdf_text(uploaded_file) -> Tuple[str, bool]:
    try:
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        text = "\n".join(page.extract_text() or "" for page in pdf_reader.pages)
        return text, bool(text.strip())
    except Exception as e:
        st.error(f"PDF Error: {str(e)}")
        return "", False

# ----------------------------
# Clause Analysis
# ----------------------------
def analyze_nda_clauses(text: str) -> Dict[str, bool]:
    text_lower = text.lower()
    clauses = {
        "Confidentiality": [r"confidential", r"non.?disclosure", r"trade secret"],
        "Non-Compete": [r"non.?compete", r"restraint.*trade"],
        "Governing Law": [r"governing law", r"jurisdiction"],
        "Injunctive Relief": [r"injunctive relief", r"irreparable harm"],
        "Attorney Fees": [r"attorney.*fees", r"legal.*costs"]
    }
    return {
        name: any(re.search(p, text_lower) for p in patterns)
        for name, patterns in clauses.items()
    }

# ----------------------------
# Main App
# ----------------------------
def main():
    st.title("⚖️ NDA Compliance Checker")
    uploaded_file = st.file_uploader("Upload NDA (PDF)", type="pdf")

    if uploaded_file:
        text, success = extract_pdf_text(uploaded_file)
        if success:
            st.subheader("📋 Analysis Results")
            results = analyze_nda_clauses(text)
            for clause, present in results.items():
                st.write(f"{'✅' if present else '❌'} {clause}")
        else:
            st.warning("Could not extract text from the uploaded PDF.")

# ----------------------------
# Run Main App If Authenticated
# ----------------------------
if st.session_state.authenticated:
    main()



