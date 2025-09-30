#!/usr/bin/env python3
"""
Setup script for AI-Powered Journal
This script helps set up the environment and install dependencies.
"""

import os
import subprocess
import sys

def install_requirements():
    """Install required packages."""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing requirements: {e}")
        return False

def create_env_file():
    """Create .env file from template if it doesn't exist."""
    if not os.path.exists(".env"):
        if os.path.exists("env_template.txt"):
            print("Creating .env file from template...")
            with open("env_template.txt", "r") as template:
                content = template.read()
            with open(".env", "w") as env_file:
                env_file.write(content)
            print("✓ .env file created. Please edit it with your actual credentials.")
            return True
        else:
            print("✗ env_template.txt not found")
            return False
    else:
        print("✓ .env file already exists")
        return True

def check_database_connection():
    """Check if database connection can be established."""
    print("Checking database connection...")
    try:
        from modules import database
        users = database.get_all_users()
        print("✓ Database connection successful")
        return True
    except Exception as e:
        print(f"✗ Database connection failed: {e}")
        print("Please check your database configuration in .env file")
        return False

def main():
    """Main setup function."""
    print("🧠 AI-Powered Journal Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        print("Setup failed at requirements installation")
        return False
    
    # Create .env file
    if not create_env_file():
        print("Setup failed at .env file creation")
        return False
    
    print("\n" + "=" * 40)
    print("Setup completed!")
    print("\nNext steps:")
    print("1. Edit .env file with your database and API credentials")
    print("2. Set up your MySQL database and run sql/schema.sql")
    print("3. Run: streamlit run app.py")
    print("4. After adding entries, run: python scripts/build_index.py")
    
    return True

if __name__ == "__main__":
    main()