import streamlit as st
from enum import Enum
from st_supabase_connection import SupabaseConnection, execute_query
from datetime import datetime

st_supabase_client = st.connection("supabase",type=SupabaseConnection)

st.title("Dog Entry Form")

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

with st.form(key="user_info_form"):

    form_values["name"] = st.text_input("Enter dogs name")
    form_values["breed"] = st.selectbox("Select breed", options=[breed.name for breed in Breed])
    form_values["sex"] = st.selectbox("Select sex", options=[sex.name for sex in Sex])
    form_values["year_of_birth"] = st.number_input("Year of Birth", min_value=min_year, max_value=max_year, step=1, value=default_year)
    form_values["notes"] = st.text_area("Notes (optional)")
    
    submit_button = st.form_submit_button(label="Submit")
    if submit_button:
        if not all(value for key, value in form_values.items() if key != "notes"):
            st.error("Please fill in all the fields")
        else:
            try:
                new_dog = [{key: value for key, value in form_values.items()}]

                execute_query(
                st_supabase_client.table("dog").insert(
                    new_dog,
                ),
                ttl=0,
            )
            except Exception as e:
                st.error(f"An error occurred while submitting the form: {e}")
                ##logging.error(e)
            else:
                st.balloons()
                st.write("### Info")
                for (key,value) in form_values.items():
                    st.write(f"**{key}** : {value}")
    print(form_values)