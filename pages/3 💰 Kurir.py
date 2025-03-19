import streamlit as st
from PIL import Image
from utils.firebase_config import fs
from utils.cookies import load_cookie_to_session
import os

# Load data from cookies
try:
    load_cookie_to_session(st.session_state)
except RuntimeError:
    st.stop()

# Set page configuration
logo_path = os.path.join("image", "icon.png")
logo = Image.open(logo_path)

# Resize the logo to a smaller size
logo_resized = logo.resize((32, 32))  # Resize to 32x32 pixels

try:
    st.set_page_config(page_title="Kurir Page", page_icon=logo_resized)
except st.errors.StreamlitSetPageConfigMustBeFirstCommandError:
    pass


if (
    "role" in st.session_state and
    st.session_state.role == "Employe" and
    "signout" in st.session_state and
    not st.session_state.signout
):
    st.title('Courier Page')
    st.text(f'Hello, {st.session_state.username}!')

    # Display orders assigned to the courier
    st.subheader("Assigned Orders")
    assigned_orders_ref = fs.collection('orders').where(
        'courier', '==', st.session_state.username).where('confirmed', '==', True)
    assigned_orders = assigned_orders_ref.stream()

    assigned_orders_list = []
    for order in assigned_orders:
        order_data = order.to_dict()
        order_data['id'] = order.id
        assigned_orders_list.append(order_data)

    if assigned_orders_list:
        orders_df = pd.DataFrame(assigned_orders_list)
        st.dataframe(orders_df)

        selected_order = st.selectbox(
            "Select Order to Mark as Delivered", orders_df['id'].unique())

        if st.button("Mark as Delivered"):
            fs.collection('orders').document(selected_order).update({
                'delivered': True
            })
            st.success("Order marked as delivered!")
    else:
        st.write("No assigned orders found.")
else:
    st.error("Please log in as Employe to access this page.")
