import PyPDF2
import streamlit as st
import re
from typing import Dict, Tuple
from datetime import datetime

# Configure the page
st.set_page_config(
    page_title="LegalGuard AI", 
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Password protection - WORKING VERSION
if not st.session_state.authenticated:
    st.title("🔒 Authentication Required")
    password_input = st.text_input("Enter password:", type="password", key="pw")
    
    if st.button("Submit"):
        if password_input == "102938":  # CHANGE THIS
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Incorrect password")
            st.stop()
    else:
        st.stop()

# Only show the app if authenticated
if st.session_state.authenticated:
    def extract_pdf_text(uploaded_file) -> Tuple[str, bool]:
        """Extract text from PDF."""
        try:
            pdf_reader = PyPDF2.PdfReader(uploaded_file)
            return "\n".join(page.extract_text() for page in pdf_reader.pages), True
        except Exception as e:
            st.error(f"PDF Error: {str(e)}")
            return "", False

    def analyze_nda_clauses(text: str) -> Dict[str, bool]:
        """Analyze NDA clauses."""
        text_lower = text.lower()
        clauses = {
            "Confidentiality": [r"confidential", r"non.?disclosure", r"trade secret"],
            "Non-Compete": [r"non.?compete", r"restraint.*trade"],
            "Governing Law": [r"governing law", r"jurisdiction"],
            "Injunctive Relief": [r"injunctive relief", r"irreparable harm"],
            "Attorney Fees": [r"attorney.*fees", r"legal.*costs"]
        }
        return {name: any(re.search(p, text_lower) for p in patterns) 
                for name, patterns in clauses.items()}

    def main():
        """Main app interface."""
        st.title("⚖️ NDA Compliance Checker")
        uploaded_file = st.file_uploader("Upload NDA (PDF)", type="pdf")
        
        if uploaded_file:
            text, success = extract_pdf_text(uploaded_file)
            if success and text.strip():
                results = analyze_nda_clauses(text)
                st.write("## Analysis Results")
                for clause, present in results.items():
                    st.write(f"{'✅' if present else '❌'} {clause}")
            else:
                st.warning("Could not extract text from PDF")

    if __name__ == "__main__":
        main()
