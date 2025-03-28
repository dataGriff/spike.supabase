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

tab1, tab2, tab3  = st.tabs([ "View Scheduled Walks", "Manage Walks", "Calendar View" ])

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

        # Display the list of scheduled walks
        if walk_list:
            st.write("Scheduled Walks:")
            for walk in walk_list:
                with st.form(key=f"walk_form_{walk['scheduled_at']}"):
                    st.write(f"Dog: {walk['dog_name']}, Scheduled: {walk['scheduled_at']}, Status: {walk['status']}")
                    reschedule_button = st.form_submit_button("Reschedule Walk")
                    if reschedule_button:
                        new_scheduled_at = st.date_input(
                            "Reschedule Date",
                            value=datetime.strptime(walk['scheduled_at'], "%Y-%m-%dT%H:%M:%S").date()
                        )
                        new_scheduled_time = st.time_input(
                            "Reschedule Time",
                            value=datetime.strptime(walk['scheduled_at'], "%Y-%m-%dT%H:%M:%S").time()
                        )
                        new_scheduled_datetime = datetime.combine(new_scheduled_at, new_scheduled_time)
                        confirm_reschedule_button = st.form_submit_button("Confirm Reschedule Walk")
                        if confirm_reschedule_button:
                            try:
                                # Update the walk with the new scheduled time
                                response = execute_query(
                                    st_supabase_client.table("walk")
                                    .update({"scheduled_at": str(new_scheduled_datetime)})
                                    .eq("dog_id", walk["dog_id"])
                                )
                                if response.data:
                                    st.success("Walk rescheduled successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to reschedule walk: {response.model_dump_json()}")
                            except Exception as e:
                                st.error(f"An error occurred while rescheduling the walk: {e}")
                    cancel_button = st.form_submit_button("Cancel Walk")
                    if cancel_button:
                        try:
                            # Cancel the walk
                            response = execute_query(
                                st_supabase_client.table("walk")
                                .update({"status": "Cancelled"})
                                .eq("dog_id", walk["dog_id"])
                            )
                            if response.data:
                                st.success("Walk cancelled successfully!")
                                st.rerun()
                            else:
                                st.error(f"Failed to cancel walk: {response.model_dump_json()}")
                        except Exception as e:
                            st.error(f"An error occurred while cancelling the walk: {e}")
        else:
            st.write("No scheduled walks found.")

    except Exception as e:
        st.error(f"An error occurred while fetching existing walks: {e}")
        walk_list = []

with tab2:
    try:

        # Dog selection
        selected_dog = st.selectbox("Select a Dog", options=dog_list, format_func=lambda x: x["name"])
        
        # Date input
        selected_date = st.date_input("Select a Date")
        selected_time = st.time_input("Select a Time")
        scheduled_date = datetime.combine(selected_date, selected_time)
        
        # Submit button
        if st.button("Schedule Walk"):
            if selected_dog and scheduled_date:
                try:
                    # Schedule the walk
                    response = execute_query(
                        st_supabase_client.table("walk").insert(
                            {
                                "scheduled_at": str(scheduled_date),
                                "dog_id": selected_dog["id"],
                                "status": "Scheduled"
                            }
                        ),
                        ttl="10min",
                    )
                    if response.data:
                        st.success("Walk scheduled successfully!")
                        st.rerun()
                    else:
                        st.error(f"Failed to schedule walk: {response.model_dump_json()}")
                except Exception as e:
                    st.error(f"An error occurred while scheduling the walk: {e}")
    except Exception as e:
        st.error(f"An error occurred while fetching available dogs: {e}")

with tab3:
    try:
        calendar_list = execute_query(
            st_supabase_client.table("walk")
            .select("scheduled_at, dog(name)"),
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
        print("Events for calendar:")
        print(calendar_events)
        # Display the calendar with events
        the_calendar = calendar(
            events=calendar_events,
            # options=calendar_options,
            # custom_css=custom_css,
            #key='calendar', # Assign a widget key to prevent state loss
            )
        st.write(the_calendar)
    except Exception as e:
        st.error(f"An error occurred while fetching existing walks: {e}")
        calendar_list = []