import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit_calendar import calendar
from datetime import datetime

st_supabase_client = st.connection("supabase", type=SupabaseConnection)

# Authentication
if "user" not in st.session_state:
    st.session_state["user"] = None

if st.session_state["user"] is None:
    st.switch_page("home.py")

if st.session_state["user"] is not None:
    st.write(f"Welcome, {st.session_state['user'].email}!")
    logout_button = st.sidebar.button("Logout")
    if logout_button:
        st_supabase_client.auth.sign_out()
        st.session_state["user"] = None
        st.rerun()

st.title("Walk Management")

# Fetch the list of dogs from the database
dog_list = execute_query(
    st_supabase_client.table("dog")
    .select("id, name")
    .order("name"),
    ttl="10min",
)

if dog_list:
    dog_list = [
        {"id": dog["id"], "name": dog["name"]}
        for dog in dog_list.data
    ]
    dog_list = dog_list if dog_list else []

tab1, tab2  = st.tabs([ "View Scheduled Walks", "Calendar View" ])

with tab1:
    try:
        walk_list = execute_query(
            st_supabase_client.table("walk")
            .select("scheduled_at, dog(name), status, dog_id")
            .eq("status", "Scheduled")
            .order("scheduled_at"),
            ##ttl="10min",
        )
        if walk_list:
            walk_list = [
            {"scheduled_at": walk["scheduled_at"],"dog_name": walk["dog"]["name"],"status": walk["status"],"dog_id": walk["dog_id"], }
            for walk in walk_list.data
            ]
        walk_list = walk_list if walk_list else []
        st.write("You have {} scheduled walks.".format(len(walk_list)))

        with st.expander("Add a New Walk", expanded=False):
            with st.form(key="new_walk_form"):
                st.write("Fill in the details below:")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    selected_dog = st.selectbox(
                        "Select Dog",
                        options=[dog["name"] for dog in dog_list],
                        key="new_walk_dog"
                    )
                with col2:
                    new_date = st.date_input("Scheduled Date", key="new_walk_date", value=datetime.now().date())
                with col3:
                    new_time = st.time_input("Scheduled Time", key="new_walk_time", value=datetime.now().time())
                with col4:
                    add_walk_button = st.form_submit_button("Add Walk")
                    if add_walk_button:
                        try:
                            selected_dog_id = next(
                                dog["id"] for dog in dog_list if dog["name"] == selected_dog
                            )
                            new_scheduled_at = datetime.combine(new_date, new_time)
                            response = execute_query(
                                st_supabase_client.table("walk")
                                .insert({"dog_id": selected_dog_id, "scheduled_at": str(new_scheduled_at), "status": "Scheduled"}),
                            )
                            if response.data:
                                st.success("New walk added successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to add new walk: {response.model_dump_json()}")
                        except Exception as e:
                            st.error(f"An error occurred while adding the new walk: {e}")
        # Display the list of scheduled walks
        if walk_list:
            st.write("Scheduled Walks:")
            
            for walk in walk_list:
                form_key = f"walk_form_{walk['dog_id']}_{walk['scheduled_at']}"
                status_key = f"status_{walk['dog_id']}_{walk['scheduled_at']}"
                date_key = f"date_{walk['dog_id']}_{walk['scheduled_at']}"
                time_key = f"time_{walk['dog_id']}_{walk['scheduled_at']}"
                with st.form(key=form_key):
            
                    col1, col2, col3 , col4 , col5 = st.columns(5)
                    with col1:
                        scheduled_at = datetime.strptime(walk['scheduled_at'], "%Y-%m-%dT%H:%M:%S.%f")
                        time_diff = scheduled_at - datetime.now()
                        time_ago = f"In {time_diff.days} days" if time_diff.days > 0 else f"In {time_diff.seconds // 3600} hours"
                        st.write(f"{walk['dog_name']} at {scheduled_at.strftime('%H:%M')} on {scheduled_at.strftime('%Y-%m-%d')} ({time_ago})")
                    with col2:
                        st.selectbox(
                            "Change Status", 
                            options=["Scheduled", "Completed", "Cancelled"], 
                            key=status_key
                        )
                    with col3:
                        st.date_input(
                            "Change Date",
                            value=datetime.strptime(walk['scheduled_at'], "%Y-%m-%dT%H:%M:%S.%f").date(),
                            key=date_key
                        )
                    with col4:
                        st.time_input(
                            "Change Time",
                            value=datetime.strptime(walk['scheduled_at'], "%Y-%m-%dT%H:%M:%S.%f").time(),
                            key=time_key
                        )
                    with col5:
                        submit_button = st.form_submit_button("Update Walk")
                        # Store the selected values in session state
                        st.session_state[f"status_{walk['scheduled_at']}"] = st.session_state[status_key]
                        st.session_state[f"date_{walk['scheduled_at']}"] = st.session_state[date_key]
                        st.session_state[f"time_{walk['scheduled_at']}"] = st.session_state[time_key]
                    if submit_button:
                        try:
                            # Update the walk status and date
                            new_status = st.session_state[f"status_{walk['scheduled_at']}"]
                            new_date = st.session_state[f"date_{walk['scheduled_at']}"]
                            new_time = st.session_state[f"time_{walk['scheduled_at']}"]
                            new_scheduled_at = datetime.combine(new_date, new_time)

                            response = execute_query(
                                st_supabase_client.table("walk")
                                .update({"status": new_status, "scheduled_at": str(new_scheduled_at)})
                                .eq("dog_id", walk["dog_id"])
                                .eq("scheduled_at", walk["scheduled_at"])
                            )
                            if response.data:
                                if response.data[0]["status"] == "Cancelled":
                                    st.success("Walk cancelled successfully!")
                                else:
                                    st.success("Walk rescheduled successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to update walk: {response.model_dump_json()}")
                        except Exception as e:
                            st.error(f"An error occurred while updating the walk: {e}")
  
        else:
            st.write("No scheduled walks found.")

    except Exception as e:
        st.error(f"An error occurred while fetching existing walks: {e}")
        walk_list = []

with tab2:
    try:
        calendar_list = execute_query(
            st_supabase_client.table("walk")
            .select("scheduled_at, dog(name)")
            .eq("status", "Scheduled"),
            ttl="0min",
        )
        if calendar_list:
            calendar_list = [
                {"scheduled_at": walk["scheduled_at"], "dog_name": walk["dog"]["name"]}
                for walk in calendar_list.data
            ]
        calendar_list = calendar_list if calendar_list else []
  
        # Prepare events for the calendar
        calendar_events = [
            {"date": walk["scheduled_at"], "title": f"{walk['dog_name']}"}
            for walk in calendar_list
        ]
        print(calendar_events)
        # Display the calendar with events
        the_calendar = calendar(
            events=calendar_events,
            # options=calendar_options,
            # custom_css=custom_css,
            #key='calendar', # Assign a widget key to prevent state loss
            )
    except Exception as e:
        st.error(f"An error occurred while fetching existing walks: {e}")
        calendar_list = []