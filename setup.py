#!/usr/bin/env python3
"""
SkillRack Automation Setup Script
Helps users set up the environment and configure the automation tool.
"""

import os
import sys
import subprocess
import json
import platform
import webbrowser
from pathlib import Path

def print_banner():
    """Print the setup banner."""
    print("="*60)
    print("🚀 SkillRack Automation Suite Setup")
    print("="*60)
    print()

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        print("   Please upgrade Python and try again.")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install Python dependencies."""
    print("\n📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        print("   Please run: pip install -r requirements.txt")
        return False

def check_chrome_installation():
    """Check if Chrome is installed."""
    print("\n🌐 Checking Google Chrome installation...")
    
    system = platform.system().lower()
    chrome_paths = {
        'windows': [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        ],
        'darwin': [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        ],
        'linux': [
            "/usr/bin/google-chrome",
            "/usr/bin/google-chrome-stable",
            "/usr/bin/chromium-browser"
        ]
    }
    
    paths_to_check = chrome_paths.get(system, [])
    
    for path in paths_to_check:
        if os.path.exists(path):
            print("✅ Google Chrome found")
            return True
    
    print("⚠️  Google Chrome not found")
    print("   Please install Chrome from: https://www.google.com/chrome/")
    return False

def check_chromedriver():
    """Check if ChromeDriver is available."""
    print("\n🔧 Checking ChromeDriver...")
    
    try:
        result = subprocess.run(['chromedriver', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ ChromeDriver found: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        pass
    
    print("⚠️  ChromeDriver not found in PATH")
    print("   Installation options:")
    
    system = platform.system().lower()
    if system == 'windows':
        print("   - Using chocolatey: choco install chromedriver")
        print("   - Manual: Download from https://chromedriver.chromium.org/")
    elif system == 'darwin':
        print("   - Using homebrew: brew install chromedriver")
        print("   - Manual: Download from https://chromedriver.chromium.org/")
    else:
        print("   - Ubuntu/Debian: sudo apt-get install chromium-chromedriver")
        print("   - Manual: Download from https://chromedriver.chromium.org/")
    
    return False

def setup_chrome_profile():
    """Help user set up Chrome profile path."""
    print("\n👤 Chrome Profile Setup (Recommended)")
    print("   Using your Chrome profile allows access to logged-in sessions.")
    
    use_profile = input("   Would you like to configure Chrome profile? (y/N): ").lower()
    
    if use_profile != 'y':
        return ""
    
    system = platform.system().lower()
    default_paths = {
        'windows': os.path.expanduser(r"~\AppData\Local\Google\Chrome\User Data"),
        'darwin': os.path.expanduser("~/Library/Application Support/Google/Chrome"),
        'linux': os.path.expanduser("~/.config/google-chrome")
    }
    
    default_path = default_paths.get(system, "")
    
    if default_path and os.path.exists(default_path):
        print(f"   Default Chrome profile found: {default_path}")
        use_default = input("   Use this path? (Y/n): ").lower()
        if use_default != 'n':
            return default_path
    
    custom_path = input("   Enter Chrome profile path (or press Enter to skip): ").strip()
    
    if custom_path and os.path.exists(custom_path):
        print(f"✅ Chrome profile path set: {custom_path}")
        return custom_path
    elif custom_path:
        print(f"⚠️  Path not found: {custom_path}")
        return ""
    
    return ""

def create_config():
    """Create configuration file."""
    print("\n⚙️  Creating configuration file...")
    
    chrome_profile = setup_chrome_profile()
    
    print("\n📝 Configuration Options:")
    print("   1. Fast (less human-like, faster execution)")
    print("   2. Normal (balanced speed and human-like behavior)")
    print("   3. Careful (very human-like, slower but stealthier)")
    
    while True:
        choice = input("   Select option (1-3) [2]: ").strip() or "2"
        if choice in ['1', '2', '3']:
            break
        print("   Please enter 1, 2, or 3")
    
    # Configuration presets
    configs = {
        '1': {  # Fast
            "typing_speed": {"min": 0.01, "max": 0.03},
            "human_delays": {"min": 0.2, "max": 0.5}
        },
        '2': {  # Normal
            "typing_speed": {"min": 0.05, "max": 0.15},
            "human_delays": {"min": 1, "max": 3}
        },
        '3': {  # Careful
            "typing_speed": {"min": 0.08, "max": 0.25},
            "human_delays": {"min": 2, "max": 5}
        }
    }
    
    selected_config = configs[choice]
    
    config = {
        "chrome_profile_path": chrome_profile,
        "typing_speed": selected_config["typing_speed"],
        "human_delays": selected_config["human_delays"],
        "retry_attempts": 3,
        "ollama_enabled": False,
        "ollama_url": "http://localhost:11434",
        "ollama_model": "codellama",
        "headless": False,
        "timeout": 30
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=4)
    
    print("✅ Configuration file created")

def setup_ollama():
    """Ask about Ollama setup."""
    print("\n🤖 Ollama LLM Integration (Optional)")
    print("   Ollama can generate solutions when no solution button is available.")
    
    setup_llm = input("   Would you like to set up Ollama? (y/N): ").lower()
    
    if setup_llm != 'y':
        return
    
    print("\n   Ollama Setup Instructions:")
    print("   1. Install Ollama:")
    
    system = platform.system().lower()
    if system == 'windows':
        print("      - Download from: https://ollama.ai/download/windows")
    elif system == 'darwin':
        print("      - Download from: https://ollama.ai/download/mac")
        print("      - Or using homebrew: brew install ollama")
    else:
        print("      - curl -fsSL https://ollama.ai/install.sh | sh")
    
    print("\n   2. Install a coding model:")
    print("      ollama pull codellama")
    print("      # or")
    print("      ollama pull deepseek-coder")
    
    print("\n   3. Start Ollama service:")
    print("      ollama serve")
    
    open_browser = input("\n   Open Ollama website for download? (y/N): ").lower()
    if open_browser == 'y':
        webbrowser.open('https://ollama.ai/')
    
    # Update config to enable Ollama
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        
        config['ollama_enabled'] = True
        
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=4)
        
        print("✅ Ollama enabled in configuration")
    except:
        print("⚠️  Could not update configuration for Ollama")

def run_test():
    """Ask if user wants to run a test."""
    print("\n🧪 Testing Setup")
    
    run_test = input("   Would you like to run a test? (y/N): ").lower()
    
    if run_test == 'y':
        print("\n   Starting test run...")
        print("   A browser window will open. Navigate to a SkillRack challenge page.")
        
        try:
            subprocess.run([sys.executable, 'skillrack_automation.py'])
        except KeyboardInterrupt:
            print("\n   Test interrupted by user")
        except Exception as e:
            print(f"\n   Test failed: {e}")

def main():
    """Main setup function."""
    print_banner()
    
    # Step 1: Check Python version
    if not check_python_version():
        return
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return
    
    # Step 3: Check Chrome
    chrome_ok = check_chrome_installation()
    
    # Step 4: Check ChromeDriver
    chromedriver_ok = check_chromedriver()
    
    if not chromedriver_ok:
        print("\n⚠️  ChromeDriver is required for the automation to work.")
        print("   Please install ChromeDriver before proceeding.")
        
        continue_anyway = input("   Continue setup anyway? (y/N): ").lower()
        if continue_anyway != 'y':
            print("\n   Setup cancelled. Please install ChromeDriver and run setup again.")
            return
    
    # Step 5: Create configuration
    create_config()
    
    # Step 6: Optional Ollama setup
    setup_ollama()
    
    # Step 7: Optional test run
    run_test()
    
    # Final summary
    print("\n" + "="*60)
    print("🎉 Setup Complete!")
    print("="*60)
    print("\nNext steps:")
    print("1. Ensure you're logged into SkillRack in your browser")
    print("2. Run: python skillrack_automation.py")
    print("3. Navigate to a challenge page when prompted")
    print("4. Watch the automation work!")
    print("\nFor batch processing: python batch_solver.py")
    print("For help: Check README.md")
    print("\nHappy coding! 🚀")

if __name__ == "__main__":
    main() 