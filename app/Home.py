import streamlit as st

# Set page config for the main page
st.set_page_config(
    page_title="Causal Buddy",
    page_icon="🔬",
    layout="wide"
)

# Main homepage content
st.markdown("<h1 style='text-align:center;'>Causal Buddy</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center;'color = #666666;'>Tools that make learning causal inference easy</div>", unsafe_allow_html=True)

st.write("")
st.write("")

# Create columns: left (narrow), right (wide)
left, _ = st.columns([1, 3])

with left:
    with st.container(border=True):
        st.markdown("### 🔬 Difference-in-Difference (DiD) Tool")
        st.markdown("Learn and Simulate a 2x2 DiD design")
        st.write("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Simulation Tool", type="primary", use_container_width=True):
                st.switch_page("pages/📈_DiD_Simulation_Tool.py")
        with col2:
            if st.button("Learn DiD", type="primary", use_container_width=True):
                st.switch_page("pages/📚_DiD_Guide.py")