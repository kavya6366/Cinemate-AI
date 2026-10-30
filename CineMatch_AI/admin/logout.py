
import streamlit as st


def render_admin_logout():
    # Step 1: Ask for confirmation only after Logout is clicked
    if "confirm_admin_logout" not in st.session_state:
        st.session_state["confirm_admin_logout"] = False

    if not st.session_state["confirm_admin_logout"]:
        if st.button("Logout", use_container_width=True):
            st.session_state["confirm_admin_logout"] = True
            st.rerun()

        return

    # Step 2: Show confirmation
    st.markdown("## Confirm Logout")
    st.warning("Are you sure you want to log out of your admin account?")

    left, right = st.columns(2)

    with left:
        if st.button("Yes, Sign out", use_container_width=True):
            st.session_state.clear()
            st.session_state["page"] = "Home"
            st.rerun()

    with right:
        if st.button("Cancel", use_container_width=True):
            st.session_state["confirm_admin_logout"] = False
            st.session_state["page"] = "Admin Dashboard"
            st.rerun()
