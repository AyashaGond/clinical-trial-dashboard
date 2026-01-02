import streamlit as st

st.set_page_config(page_title="Test", layout="wide")
st.title("🎯 TEST PAGE")

# Test 1: Basic Streamlit
st.write("✅ Basic Streamlit working")

# Test 2: Login function
try:
    from login import main_login
    st.write("✅ Login module loaded")
    
    # Test login
    if not main_login():
        st.write("🔐 Login screen should appear")
    else:
        st.write("✅ Logged in successfully")
        
except Exception as e:
    st.error(f"❌ Login error: {e}")

# Test 3: Data loading
try:
    from calculations import load_and_process_data
    patients, sites, queries = load_and_process_data()
    st.write(f"✅ Data loaded: {len(patients)} patients")
    
    # Show some data
    st.dataframe(patients.head() if not patients.empty else "No data")
    
except Exception as e:
    st.error(f"❌ Data loading error: {e}")