# setup.py - Run this to create all files automatically
import os

# Create directory structure
os.makedirs('data', exist_ok=True)
os.makedirs('utils', exist_ok=True)

# Create empty __init__.py
open('utils/__init__.py', 'w').close()

print("✅ Created folder structure")

# Ask which file to create
print("\nWhich file do you want to create?")
print("1. login.py")
print("2. app.py (Professional version)")
print("3. All files")
choice = input("Enter choice (1/2/3): ")

if choice in ['1', '3']:
    # Login.py content
    login_content = '''# login.py - Copy the ENTIRE login.py code I provided here'''
    with open('login.py', 'w') as f:
        f.write("# Paste login.py code here\n")
    print("📄 Created login.py - Open and paste the code")

if choice in ['2', '3']:
    # app.py content  
    with open('app.py', 'w') as f:
        f.write("# Paste app.py code here\n")
    print("📄 Created app.py - Open and paste the code")

print("\n🎯 NEXT: Open each .py file and paste the code I provided")