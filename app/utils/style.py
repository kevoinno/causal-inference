import streamlit as st

def setup_page(title: str, icon: str):
    """
    Sets up the page configuration and injects custom CSS for fonts and styling.
    
    Args:
        title (str): The page title to display in the browser tab.
        icon (str): The favicon (emoji) to display in the browser tab.
    """
    st.set_page_config(
        page_title=title,
        page_icon=icon,
        layout="wide"
    )

    # Inject Inter font from Google Fonts and apply to all elements
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@500;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            font-weight: 500; /* Thicker default weight */
        }
        
        /* Ensure headers also use the font */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Inter', sans-serif;
            font-weight: 700; /* Thicker headers */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
