import streamlit as st
from st_supabase_connection import SupabaseConnection, execute_query
from streamlit_calendar import calendar
from datetime import datetime, timedelta

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
)

if dog_list:
    dog_list = [
        {"id": dog["id"], "name": dog["name"]}
        for dog in dog_list.data
    ]
    dog_list = dog_list if dog_list else []

tab1, tab2  = st.tabs([ "View Scheduled Walks", "Calendar View" ])

walk_list = execute_query(
    st_supabase_client.table("walk")
    .select("id, scheduled_date,scheduled_time, dog(name), status, dog_id")
    .eq("status", "Scheduled")
    .order("scheduled_date"),
    ttl="0min",
)

try:
    if walk_list:
        walk_list = [
        {"id": walk["id"],"scheduled_date": walk["scheduled_date"],"scheduled_time": walk["scheduled_time"],"dog_name": walk["dog"]["name"],"status": walk["status"],"dog_id": walk["dog_id"], }
        for walk in walk_list.data
        ]
        walk_list = walk_list if walk_list else []
    else:
        st.write("No scheduled walks found.")

except Exception as e:
    st.error(f"An error occurred while fetching existing walks: {e}")
    walk_list = []

with tab1:
        walks_total = len(walk_list) if walk_list else 0
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        walks_today = len([walk for walk in walk_list if walk['scheduled_date'] == str(today)])
        walks_tomorrow = len([walk for walk in walk_list if walk['scheduled_date'] == str(tomorrow)])
        # Use `st.container` with `st.columns` to ensure proper layout on mobile
        with st.container():
            col1, col2, col3 = st.columns(3, gap="small")
            with col1:  
                st.write("Total: {}".format(walks_total))
            with col2:
                st.write("Today: {}".format(walks_today))
            with col3:
                st.write("Tomorrow: {}".format(walks_tomorrow))

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
                    new_date = st.date_input("Scheduled Date", key="new_walk_date")
                with col3:
                    new_time = st.time_input("Scheduled Time", key="new_walk_time")
                with col4:
                    add_walk_button = st.form_submit_button("Add Walk")
                    if add_walk_button:
                        try:
                            selected_dog_id = next(
                                dog["id"] for dog in dog_list if dog["name"] == selected_dog
                            )
                            response = execute_query(
                                st_supabase_client.table("walk")
                                .insert({"dog_id": selected_dog_id, "scheduled_date": str(new_date),"scheduled_time": str(new_time), "status": "Scheduled"}),
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
                form_key = f"walk_form_{walk['id']}"
                status_key = f"status_{walk['id']}"
                date_key = f"date_{walk['id']}"
                time_key = f"time_{walk['id']}"
                with st.form(key=form_key):
                    # scheduled_at = datetime.strptime(walk['scheduled_date'], "%Y-%m-%dT%H:%M:%S.%f")
                    # time_diff = scheduled_at - datetime.now()
                    # time_ago = f"In {time_diff.days} days" if time_diff.days > 0 else f"In {time_diff.seconds // 3600} hours"
                    # st.write(f"{walk['dog_name']} at {scheduled_at.strftime('%H:%M')} on {scheduled_at.strftime('%Y-%m-%d')} ({time_ago})")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"{walk['dog_name']} on {walk['scheduled_date']} at {walk['scheduled_time'][:-3]}")
                    with col2:
                        cancel_button = st.form_submit_button("Cancel")
                        if cancel_button:
                            try:
                                response = execute_query(
                                    st_supabase_client.table("walk")
                                    .update({"status": "Cancelled"})
                                    .eq("id", walk["id"])
                                )
                                if response.data:
                                    st.success("Walk cancelled successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to cancel walk: {response.model_dump_json()}")
                            except Exception as e:
                                st.error(f"An error occurred while cancelling the walk: {e}")
                    with col3:
                        complete_button = st.form_submit_button("Complete")
                        if complete_button:
                            try:
                                response = execute_query(
                                    st_supabase_client.table("walk")
                                    .update({"status": "Completed"})
                                    .eq("id", walk["id"])
                                )
                                if response.data:
                                    st.success("Walk completed successfully!")
                                    st.rerun()
                                else:
                                    st.error(f"Failed to complete walk: {response.model_dump_json()}")
                            except Exception as e:
                                st.error(f"An error occurred while completing the walk: {e}")
                    with st.expander("Reschedule walk", expanded=False):
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.date_input(
                                "Change Date",
                                value=walk['scheduled_date'],
                                key=date_key
                            )
                        with col2:
                            st.time_input(
                                "Change Time",
                                value=walk['scheduled_time'],
                                key=time_key
                            )
                        with col3:
                            submit_button = st.form_submit_button("Reschedule")
                            # Store the selected values in session state
                            # st.session_state[f"status_{walk['scheduled_at']}"] = st.session_state[status_key]
                            # st.session_state[f"date_{walk['scheduled_at']}"] = st.session_state[date_key]
                            # st.session_state[f"time_{walk['scheduled_at']}"] = st.session_state[time_key]
                        if submit_button:
                            try:
                                # Update the walk status and date
                                new_date = st.session_state[date_key]
                                new_time = st.session_state[time_key]
                        
                                response = execute_query(
                                    st_supabase_client.table("walk")
                                    .update({"scheduled_date": str(new_date),"scheduled_time": str(new_time),})
                                    .eq("id", walk["id"])
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
  

with tab2:
    try:
        calendar_events = [
            {
                "start": f"{walk['scheduled_date']}T{walk['scheduled_time']}",
                "end": f"{walk['scheduled_date']}T{(datetime.strptime(walk['scheduled_time'], '%H:%M:%S') + timedelta(hours=1)).strftime('%H:%M:%S')}",
                "title": walk['dog_name']
            }
            for walk in walk_list
        ]
        calendar(
            events=calendar_events,
            key='calendar_view'
        )
    except Exception as e:
        st.error(f"An error occurred while displaying the calendar: {e}")