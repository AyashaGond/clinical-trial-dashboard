# login.py
import streamlit as st
import hashlib
import json
import os
from datetime import datetime

class LoginSystem:
    """Secure login system for clinical trial dashboard"""
    
    def __init__(self):
        self.users_file = 'data/users.json'
        self.session_file = 'data/session.json'
        self.initialize_users()
    
    def initialize_users(self):
        """Create default users if file doesn't exist"""
        if not os.path.exists(self.users_file):
            default_users = {
                "admin": {
                    "password": self.hash_password("admin123"),
                    "role": "Admin",
                    "name": "System Administrator",
                    "email": "admin@novartis.com"
                },
                "cra": {
                    "password": self.hash_password("cra123"),
                    "role": "CRA",
                    "name": "Clinical Research Associate",
                    "email": "cra@novartis.com"
                },
                "doctor": {
                    "password": self.hash_password("doctor123"),
                    "role": "Doctor",
                    "name": "Medical Doctor",
                    "email": "doctor@hospital.com"
                }
            }
            os.makedirs('data', exist_ok=True)
            with open(self.users_file, 'w') as f:
                json.dump(default_users, f)
    
    def hash_password(self, password):
        """Hash password for security"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user"""
        try:
            with open(self.users_file, 'r') as f:
                users = json.load(f)
            
            if username in users and users[username]['password'] == self.hash_password(password):
                return {
                    'username': username,
                    'role': users[username]['role'],
                    'name': users[username]['name'],
                    'email': users[username]['email']
                }
        except:
            pass
        return None
    
    def save_session(self, user_data):
        """Save user session"""
        session_data = {
            'user': user_data,
            'login_time': datetime.now().isoformat(),
            'active': True
        }
        with open(self.session_file, 'w') as f:
            json.dump(session_data, f)
    
    def load_session(self):
        """Load existing session"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r') as f:
                    return json.load(f)
        except:
            pass
        return None
    
    def logout(self):
        """Logout user"""
        if os.path.exists(self.session_file):
            os.remove(self.session_file)

def show_login_page():
    """Display login page"""
    
    # Custom CSS for login page
    st.markdown("""
    <style>
        .login-container {
            max-width: 400px;
            margin: 100px auto;
            padding: 40px;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }
        .login-header h1 {
            color: #1f3c88;
            font-size: 28px;
            margin-bottom: 10px;
        }
        .login-header p {
            color: #6c757d;
            font-size: 14px;
        }
        .stTextInput>div>div>input {
            border-radius: 8px;
            border: 1px solid #ddd;
            padding: 12px;
        }
        .stSelectbox>div>div>div {
            border-radius: 8px;
            border: 1px solid #ddd;
        }
        .login-button {
            width: 100%;
            border-radius: 8px;
            padding: 12px;
            font-weight: bold;
            background: linear-gradient(135deg, #1f3c88, #4a6fc1);
            color: white;
            border: none;
        }
        .hospital-icon {
            font-size: 48px;
            color: #1f3c88;
            margin-bottom: 20px;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Login container
    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Header with hospital icon
    st.markdown('<div class="login-header">', unsafe_allow_html=True)
    st.markdown('<div class="hospital-icon">🏥</div>', unsafe_allow_html=True)
    st.markdown('<h1>Clinical Intelligence Platform</h1>', unsafe_allow_html=True)
    st.markdown('<p>Secure access to clinical trial management</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Login form
    login_system = LoginSystem()
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("👤 Username", placeholder="Enter username")
    with col2:
        role = st.selectbox("👥 Role", ["Admin", "CRA", "Doctor"])
    
    col1, col2 = st.columns([3, 1])
    with col1:
        password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
    with col2:
        show_password = st.checkbox("👁️")
    
    if show_password:
        st.text_input("Password (visible)", value=password, type="default", disabled=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        remember_me = st.checkbox("Remember me")
    
    if st.button("🚀 Login", use_container_width=True, type="primary"):
        if username and password:
            user = login_system.authenticate(username, password)
            if user:
                login_system.save_session(user)
                st.success(f"Welcome, {user['name']}!")
                st.session_state['logged_in'] = True
                st.session_state['user'] = user
                st.rerun()
            else:
                st.error("Invalid username or password")
        else:
            st.warning("Please enter username and password")
    
    # Forgot password
    st.markdown("---")
    if st.button("🔓 Forgot Password?"):
        st.info("Please contact system administrator at admin@novartis.com")
    
    st.markdown('</div>', unsafe_allow_html=True)

def main_login():
    """Main login flow"""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    login_system = LoginSystem()
    session = login_system.load_session()
    
    if session and session.get('active'):
        st.session_state['logged_in'] = True
        st.session_state['user'] = session['user']
    
    if not st.session_state['logged_in']:
        show_login_page()
        return False
    return True