import streamlit as st
from utils.style import setup_page

# Set page config for the main page
setup_page(
    title="Causal Buddy",
    icon="🔬"
)

# Main homepage content
st.markdown("<h1 style='text-align:center;'>Causal Buddy</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color: #666666;'>Tools that make learning causal inference easy</h4>", unsafe_allow_html=True)

st.write("")
st.write("")

# Create columns: left (narrow), right (wide)
col1, col2, col3 = st.columns([1, 1, 1])

with col1:
    with st.container(border=True):
        st.markdown("### 🔬 Difference-in-Difference (DiD) Tool")
        st.markdown("Learn and Simulate a 2x2 DiD design")
        st.write("")
        did_col1, did_col2 = st.columns(2)
        with did_col1:
            if st.button("Simulation Tool", type="primary", use_container_width=True):
                st.switch_page("pages/DiD_Simulation_Tool.py")
        with did_col2:
            if st.button("Learn DiD", type="primary", use_container_width=True):
                st.switch_page("pages/DiD_Guide.py")
with col2:
    with st.container(border=True):
        st.markdown('#### 🧪 A/B Testing Tool')
        st.markdown("Learn how to setup and analyze A/B tests and about sample ratio mismatch (SRM)")
        if st.button("A/B Testing Guide", type = "primary", use_container_width = True):
            st.switch_page("pages/AB_Testing_Simulation_Tool.py")