
"""
Quick Start Script for SkillRack Automation GUI
Simple launcher that handles common issues and provides helpful messages.
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {sys.version}")
        print("   Please upgrade Python and try again.")
        input("Press Enter to exit...")
        return False
    return True

def check_dependencies():
    """Check if required dependencies are installed."""
    required_packages = [
        ('tkinter', 'tkinter (usually included with Python)'),
        ('selenium', 'selenium'),
        ('bs4', 'beautifulsoup4'),
        ('requests', 'requests'),
        ('pyperclip', 'pyperclip'),
        ('pyautogui', 'pyautogui')
    ]
    
    missing = []
    
    for package, install_name in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
            else:
                importlib.import_module(package)
        except ImportError:
            missing.append(install_name)
    
    if missing:
        print("❌ Missing required packages:")
        for package in missing:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing)}")
        
        auto_install = input("\n🤖 Auto-install missing packages? (y/n): ").lower()
        if auto_install == 'y':
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing, check=True)
                print("✅ Packages installed successfully!")
                return True
            except subprocess.CalledProcessError:
                print("❌ Installation failed. Please install manually.")
                return False
        return False
    
    return True

def main():
    """Main launcher function."""
    print("🚀 SkillRack Automation Suite - GUI Launcher")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check dependencies
    if not check_dependencies():
        input("Press Enter to exit...")
        return
    
    # Check if main GUI file exists
    if not os.path.exists('skillrack_gui.py'):
        print("❌ skillrack_gui.py not found!")
        print("   Please ensure you're in the correct directory.")
        input("Press Enter to exit...")
        return
    
    print("✅ All checks passed!")
    print("🎯 Starting SkillRack Automation GUI...")
    print("=" * 50)
    
    try:
        # Import and run the GUI
        from skillrack_gui import SkillRackGUI
        
        app = SkillRackGUI()
        app.run()
        
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"\n❌ Error starting GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed")
        print("2. Check that skillrack_automation.py exists")
        print("3. Verify Python version is 3.8+")
        input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()