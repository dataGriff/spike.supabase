import streamlit as st
from st_supabase_connection import SupabaseConnection

st_supabase_client = st.connection("supabase", type=SupabaseConnection)

st.title("Dog Walking Management Tool")

# Authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    # Hide sidebar until logged in
    # st.sidebar.empty()

    auth_mode = st.radio("Choose authentication mode", options=["Login", "Sign Up"])

    if auth_mode == "Login":
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")

            if login_button:
                try:
                    user = st_supabase_client.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state["user"] = user.user
                    st.success("Logged in successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Login failed: {e}")
    elif auth_mode == "Sign Up":
        with st.form("signup_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            signup_button = st.form_submit_button("Sign Up")

            if signup_button:
                try:
                    user = st_supabase_client.auth.sign_up({"email": email, "password": password})
                    st.session_state["user"] = user.user
                    st.success("Account created successfully! You are now logged in.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Sign-up failed: {e}")

if st.session_state["user"] is not None:
    # Show sidebar content after login
    st.write(f"Welcome, {st.session_state['user'].email}!")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st_supabase_client.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()
        st.switch_page("pages/dogs.py")