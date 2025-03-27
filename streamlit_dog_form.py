import streamlit as st
from enum import Enum
from st_supabase_connection import SupabaseConnection, execute_query
from supabase import create_client, Client
from datetime import datetime

st_supabase_client = st.connection("supabase", type=SupabaseConnection)

st.title("Dog Entry Form")

# Authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
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
    st.write(f"Welcome, {st.session_state['user'].email}!")
    logout_button = st.button("Logout")
    if logout_button:
        st_supabase_client.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()

    # Dog Entry Form Logic
    class Breed(Enum):
        StaffordshireBullTerrier = 1
        GermanShepherd = 2
        Spaniel = 3

    class Sex(Enum):
        Male = 1
        Female = 2

    form_values = {
        "name": str,
        "breed": int,
        "sex": int,
        "year_of_birth": int,
        "notes": str,
    }

    min_year = datetime.now().year - 25
    max_year = datetime.now().year
    default_year = datetime.now().year - 3

    # Fetch existing dogs from the database
    try:
        existing_dogs = execute_query(
            st_supabase_client.table("dog").select("*"),
            ttl="10min",
        )
        existing_dogs = existing_dogs.data if existing_dogs else []
    except Exception as e:
        st.error(f"An error occurred while fetching existing dogs: {e}")
        existing_dogs = []

    dog_ids = [dog["id"] for dog in existing_dogs]

    # Add a toggle for Insert or Update mode
    mode = st.radio("Choose mode", options=["Add", "Update"])

    if mode == "Update" and dog_ids:
        selected_dog = st.selectbox(
            "Select an existing dog to update",
            options=[f"{dog['name']} ({dog['sex']}, {dog['breed']})" for dog in existing_dogs],
            format_func=lambda x: x,
        )
        selected_dog_id = next(
            (dog["id"] for dog in existing_dogs if f"{dog['name']} ({dog['sex']}, {dog['breed']})" == selected_dog),
            None,
        )
        selected_dog = next((dog for dog in existing_dogs if dog["id"] == selected_dog_id), None)
    else:
        selected_dog = None

    with st.form(key="user_info_form"):
        form_values["name"] = st.text_input("Enter dog's name", value=selected_dog["name"] if selected_dog else "")
        form_values["breed"] = st.selectbox(
            "Select breed",
            options=[breed.name for breed in Breed],
            index=[breed.name for breed in Breed].index(selected_dog["breed"]) if selected_dog else 0,
        )
        form_values["sex"] = st.selectbox(
            "Select sex",
            options=[sex.name for sex in Sex],
            index=[sex.name for sex in Sex].index(selected_dog["sex"]) if selected_dog else 0,
        )
        form_values["year_of_birth"] = st.number_input(
            "Year of Birth",
            min_value=min_year,
            max_value=max_year,
            step=1,
            value=selected_dog["year_of_birth"] if selected_dog else default_year,
        )
        form_values["notes"] = st.text_area("Notes (optional)", value=selected_dog["notes"] if selected_dog else "")

        submit_button = st.form_submit_button(label="Submit")
        if submit_button:
            if not all(value for key, value in form_values.items() if key != "notes"):
                st.error("Please fill in all the fields")
            else:
                try:
                    if mode == "Add":
                        new_dog = [{key: value for key, value in form_values.items()}]
                        execute_query(
                            st_supabase_client.table("dog").insert(new_dog),
                            ttl=0,
                        )
                    elif mode == "Update" and selected_dog:
                        updated_dog = {key: value for key, value in form_values.items()}
                        execute_query(
                            st_supabase_client.table("dog").update(updated_dog).eq("name", selected_dog["name"]),
                            ttl=0,
                        )
                except Exception as e:
                    st.error(f"An error occurred while submitting the form: {e}")
                else:
                    st.balloons()
                    st.write("### Info")
                    for key, value in form_values.items():
                        st.write(f"**{key}** : {value}")