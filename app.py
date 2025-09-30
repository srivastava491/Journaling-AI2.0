import streamlit as st
import streamlit_authenticator as stauth
from modules import database
import bcrypt

st.set_page_config(page_title="AI Journal Login", page_icon="🧠", layout="centered")

users = database.get_all_users()
credentials = {"usernames": {user['username']: {"name": user['username'], "password": user['password_hash'], "email": user['email']} for user in users}}

authenticator = stauth.Authenticate(credentials, "ai_journal_cookie", "ai_journal_key", 30)

st.title("🧠 AI-Powered Journal")
st.write("Your private, intelligent space to reflect and grow.")

if 'registration_success' not in st.session_state: st.session_state.registration_success = False
if st.session_state.registration_success: st.success("Registration successful! Please login.")
st.session_state.registration_success = False

if not st.session_state.get("authentication_status"):
    authenticator.login(location="main")

if st.session_state.get("authentication_status"):
    st.sidebar.success("Login successful!")
    st.sidebar.write(f"Welcome, *{st.session_state.name}*")
    authenticator.logout('Logout', 'sidebar')
    
    user_info = database.get_user(st.session_state.username)
    st.session_state.user_id = user_info['id']
    
    st.write("Please navigate to the 'Journal' page in the sidebar.")

elif st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please login or register.")

if not st.session_state.get("authentication_status"):
    st.subheader("Register New Account")
    try:
        with st.form("Registration Form"):
            email, username, password, confirm = st.text_input("Email*"), st.text_input("Username*"), st.text_input("Password*", type="password"), st.text_input("Confirm Password*", type="password")
            if st.form_submit_button("Register"):
                if not all([email, username, password, confirm]):
                    st.warning("Please fill out all fields.")
                elif password != confirm:
                    st.error("Passwords do not match.")
                elif database.get_user(username) or database.get_user_by_email(email):
                    st.error("Username or email already exists.")
                else:
                    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                    if database.add_user(username, email, hashed):
                        st.session_state.registration_success = True
                        st.rerun()
                    else:
                        st.error("Registration failed.")
    except Exception as e:
        st.error(e)