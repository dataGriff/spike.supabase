import streamlit as st
from enum import Enum

st.title("User Information Form")

# st.title("User Information Form")

# class Breed(Enum):
#     StaffordshireBullTerrier = 1
#     GermanShepherd = 2
#     Spaniel = 3

# form_values = {
#     "name": str,
#     "breed": int
# }

# with st.form(key="user_info_form"):

#     form_values["name"] = st.text_input("Enter dogs name")
#     form_values["breed"] = st.number_input("Enter dogs breed")

#     submit_button = st.form_submit_button(label="Submit")
#     if submit_button:
#         if not all(form_values.values()):
#             st.error("Please fill in all the fields")
#         else:
#             st.balloons()
#             st.write("### Info")
#             for (key,value) in form_values.items():
#                 st.write(f"**{key}** : {value}")
#     # print(name, age)
#     print(form_values)