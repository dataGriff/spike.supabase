import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query

st_supabase_client = st.connection("supabase",type=SupabaseConnection)

# Perform query.
##rows = conn.execute_query("*", table="dog", ttl="10m").execute()

response = execute_query(
        st_supabase_client.table("dog").select("name"), 
        ttl="10min",
    )

st.dataframe(response.data, use_container_width=True)

# for row in rows:
#     st.write(f"This is :{row['name']}:")

dog_name_input = st.text_input("Enter Dog Name")
st.button("Insert data")
if st.button:
    execute_query(
            st_supabase_client.table("dog").insert(
                [{"name": f"{dog_name_input}"}], 
            ),
            ttl=0,
        )