import streamlit as st
from PIL import Image, ImageOps
from utils.database import connect_db
from utils.cookies import load_cookie_to_session
import os
import pandas as pd
import asyncio
from streamlit_option_menu import option_menu
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode
from sub_pages import dashboard, search, update_data, chatbot, update

# Load data from cookies
try:
    load_cookie_to_session(st.session_state)
except RuntimeError:
    st.stop()

logo_path = os.path.join("image", "icon.png")
logo = Image.open(logo_path)

logo_resized = logo.resize((40, 50))
padding = 8
new_size = (logo_resized.width + 2 * padding,
            logo_resized.height + 2 * padding)
logo_with_padding = ImageOps.expand(logo_resized, border=padding, fill=(
    255, 255, 255, 0))

try:
    st.set_page_config(page_title="Dashboard Page",
                       page_icon=logo_with_padding)
except st.errors.StreamlitSetPageConfigMustBeFirstCommandError:
    pass

with st.sidebar:
    app = option_menu(
        menu_title="Select Menu",
        options=["Dashboard", "Search", "Update Data", "Chatbot", "Test"],
        icons=["grid", "search", "table", "chat", "code"],
        menu_icon="menu-button-wide",
        default_index=0,
        orientation="vertical",
        styles={
            "container": {"padding": "1px", "background-color": "#42C2FF"},
            "menu-title": {"font-size": "24px", "font-weight": "bold", "color": "white"},
            "icon": {"color": "white", "font-size": "18px"},
            "nav-link": {"color": "white", "font-size": "18px", "text-align": "left", "margin": "5px"},
            "nav-link-selected": {"background-color": "#0077B6"}
        }
    )

if app == 'Dashboard':
    dashboard.app()
if app == 'Search':
    search.app()
if app == 'Update Data':
    update_data.app()
if app == 'Test':
    update.app()
if app == 'Chatbot':
    chatbot.app()
