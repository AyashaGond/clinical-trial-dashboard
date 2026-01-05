# auth.py - Professional Authentication System
import streamlit as st
import hashlib

class AuthSystem:
    def __init__(self):
        self.users = {
            'admin': {
                'password': self.hash_password('admin123'),
                'name': 'System Administrator',
                'role': 'Admin',
                'email': 'admin@clinicaltrials.com',
                'department': 'Clinical Operations'
            },
            'cra': {
                'password': self.hash_password('cra123'),
                'name': 'Dr. Sarah Johnson',
                'role': 'Clinical Research Associate',
                'email': 's.johnson@clinicaltrials.com',
                'department': 'Monitoring'
            },
            'investigator': {
                'password': self.hash_password('doctor123'),
                'name': 'Dr. Michael Chen',
                'role': 'Principal Investigator',
                'email': 'm.chen@hospital.com',
                'department': 'Oncology'
            }
        }
    
    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        if username in self.users:
            hashed_password = self.hash_password(password)
            if self.users[username]['password'] == hashed_password:
                return self.users[username]
        return None
    
    def logout(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()