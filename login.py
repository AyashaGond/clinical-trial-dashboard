# login.py - Simple login system for clinical trial dashboard

import streamlit as st
import hashlib
import json
import os
from datetime import datetime

import streamlit as st

# Rest of your login code...

class LoginSystem:
    def __init__(self):
        self.users_file = 'users.json'
        self.load_users()
    
    def load_users(self):
        """Load users from file or create default users"""
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            # Create default users
            self.users = {
                'admin': {
                    'password': self.hash_password('admin123'),
                    'role': 'Admin',
                    'name': 'System Administrator',
                    'email': 'admin@clinicaltrial.com'
                },
                'cra': {
                    'password': self.hash_password('cra123'),
                    'role': 'Clinical Research Associate',
                    'name': 'John Smith',
                    'email': 'john.smith@clinicaltrial.com'
                },
                'doctor': {
                    'password': self.hash_password('doctor123'),
                    'role': 'Principal Investigator',
                    'name': 'Dr. Sarah Johnson',
                    'email': 'sarah.j@hospital.org'
                }
            }
            self.save_users()
    
    def save_users(self):
        """Save users to file"""
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f, indent=2)
    
    def hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user"""
        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username]['password'] == hashed_password:
                return True
        return False
    
    def get_user_info(self, username):
        """Get user information"""
        if username in self.users:
            user_info = self.users[username].copy()
            user_info['username'] = username
            user_info.pop('password', None)  # Remove password for security
            return user_info
        return None
    
    def logout(self):
        """Logout user"""
        for key in ['logged_in', 'user', 'username']:
            if key in st.session_state:
                del st.session_state[key]

def main_login():
    """Main login function - returns True if authenticated, False otherwise"""
    
    # Check if already logged in
    if st.session_state.get('logged_in', False):
        return True
    
    # Create login system
    login_system = LoginSystem()
    
    # Login form
    st.markdown("""
    <div style="
        max-width: 400px;
        margin: 100px auto;
        padding: 36px;
        background: white;
        border-radius: 15px;
        box-shadow: 10px 40px 50px rgba(0.1,0.1,0.1,0.1);
        text-align: center;
    ">
        <h1 style="color: #1f3c88; margin-bottom: 30px;">🏥 Clinical Intelligence Platform</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Secure Login")
        
        # Login form
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            
            # Pre-filled demo accounts
            st.caption("**Demo Accounts:**")
            st.caption("• **Admin:** admin / admin123")
            st.caption("• **CRA:** cra / cra123")
            st.caption("• **Doctor:** doctor / doctor123")
            
            submitted = st.form_submit_button("Login", type="primary", use_container_width=True)
            
            if submitted:
                if not username or not password:
                    st.error("Please enter both username and password")
                elif login_system.authenticate(username, password):
                    # Store user info in session state
                    st.session_state['logged_in'] = True
                    st.session_state['username'] = username
                    st.session_state['user'] = login_system.get_user_info(username)
                    st.session_state['login_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    
                    # Show success and rerun
                    st.success("✅ Login successful! Redirecting...")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
        
        # Forgot password link
        st.markdown("---")
        st.caption("[Forgot Password?](#)")
        st.caption("Need access? Contact administrator")
    
    # Return False if not logged in
    return False

# Quick test function
def quick_login():
    """Quick login for demo purposes"""
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = True
        st.session_state['user'] = {
            'name': 'Demo User',
            'role': 'Clinical Research Associate',
            'username': 'demo'
        }

if __name__ == "__main__":
    # Test the login system
    st.set_page_config(page_title="Login Test", page_icon="🔐")
    main_login()