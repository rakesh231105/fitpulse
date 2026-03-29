import streamlit as st
from input import input_page
from dashboard import dashboard_page

st.set_page_config(page_title="FitPulse", layout="wide")

# SESSION STATE
if "page" not in st.session_state:
    st.session_state.page = "login"

# ===============================
# 🎨 SIMPLE WHITE + GREEN STYLE
# ===============================
st.markdown("""
<style>
body {background-color:#f7fff9;}
h1,h2,h3 {color:#27ae60;}
.stButton>button {
    background:#2ecc71;
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

# ===============================
# 🔐 LOGIN PAGE
# ===============================
def login_page():
    st.markdown("<h1 style='text-align:center;'>💚 FitPulse Login</h1>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username == "admin" and password == "123":
                st.session_state.page = "input"
                st.success("Login successful")
                st.rerun()
            else:
                st.error("Invalid login")

# ===============================
# 🔄 NAVIGATION
# ===============================
if st.session_state.page == "login":
    login_page()

elif st.session_state.page == "input":
    input_page()

elif st.session_state.page == "dashboard":
    dashboard_page()