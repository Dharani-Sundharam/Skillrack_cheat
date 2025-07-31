
"""
Build Script for SkillRack Automation Suite
Creates a standalone executable using PyInstaller.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if required packages are installed."""
    required_packages = [
        'pyinstaller',
        'selenium', 
        'beautifulsoup4',
        'requests',
        'pyperclip',
        'pyautogui'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n📦 Install missing packages with:")
        print(f"   pip install {' '.join(missing_packages)}")
        return False
    
    print("✅ All required packages are installed")
    return True

def create_icon():
    """Create a simple icon file for the executable."""
    icon_content = '''
    # This would normally be a .ico file
    # For now, we'll use the default PyInstaller icon
    '''
    # In a real implementation, you'd create or include an .ico file
    return None

def build_executable():
    """Build the executable using PyInstaller."""
    print("🔨 Building SkillRack Automation Suite executable...")
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Hide console window (GUI app)
        '--name=SkillRackAutomation',   # Executable name
        '--distpath=dist',              # Output directory
        '--workpath=build',             # Build directory
        '--specpath=.',                 # Spec file location
        '--clean',                      # Clean build directories
        '--noconfirm',                  # Overwrite existing files
        'skillrack_gui.py'              # Main script
    ]
    
    # Add additional data files
    data_files = [
        'config.json',
        'requirements.txt',
        'README.md'
    ]
    
    for data_file in data_files:
        if os.path.exists(data_file):
            cmd.extend(['--add-data', f'{data_file};.'])
    
    # Add hidden imports that PyInstaller might miss
    hidden_imports = [
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.common.by',
        'selenium.webdriver.support.ui',
        'selenium.webdriver.support.expected_conditions',
        'bs4',
        'requests',
        'pyperclip',
        'pyautogui',
        'tkinter',
        'tkinter.ttk',
        'tkinter.scrolledtext',
        'tkinter.messagebox',
        'tkinter.filedialog'
    ]
    
    for import_name in hidden_imports:
        cmd.extend(['--hidden-import', import_name])
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Executable built successfully!")
            print(f"📁 Output location: {os.path.abspath('dist/SkillRackAutomation.exe')}")
            return True
        else:
            print("❌ Build failed!")
            print("Error output:")
            print(result.stderr)
            return False
            
    except FileNotFoundError:
        print("❌ PyInstaller not found. Install it with: pip install pyinstaller")
        return False
    except Exception as e:
        print(f"❌ Build error: {e}")
        return False

def create_installer_script():
    """Create a simple installer script."""
    installer_content = '''@echo off
echo 🚀 SkillRack Automation Suite Installer
echo =====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python found

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    pause
    exit /b 1
)

echo ✅ pip found

REM Install required packages
echo 📦 Installing required packages...
pip install selenium beautifulsoup4 requests pyperclip pyautogui

REM Check if ChromeDriver is available
chromedriver --version >nul 2>&1
if errorlevel 1 (
    echo ⚠️ ChromeDriver not found in PATH
    echo Please install ChromeDriver:
    echo 1. Download from: https://chromedriver.chromium.org/
    echo 2. Add to PATH or place in project directory
    echo.
)

echo.
echo ✅ Installation completed!
echo.
echo 🚀 You can now run:
echo    python skillrack_gui.py     (GUI version)
echo    python skillrack_automation.py (Command line version)
echo.
pause
'''
    
    with open('install.bat', 'w') as f:
        f.write(installer_content)
    
    print("✅ Installer script created: install.bat")

def create_launcher_script():
    """Create a launcher script for the GUI."""
    launcher_content = '''@echo off
title SkillRack Automation Suite
echo 🚀 Starting SkillRack Automation Suite...
echo.

REM Check if the executable exists
if exist "SkillRackAutomation.exe" (
    echo ✅ Starting executable version...
    start SkillRackAutomation.exe
) else if exist "skillrack_gui.py" (
    echo ✅ Starting Python version...
    python skillrack_gui.py
) else (
    echo ❌ SkillRack Automation not found!
    echo Please ensure the files are in the current directory.
    pause
    exit /b 1
)
'''
    
    with open('launch.bat', 'w') as f:
        f.write(launcher_content)
    
    print("✅ Launcher script created: launch.bat")

def create_readme_for_executable():
    """Create a README for the executable distribution."""
    readme_content = '''# SkillRack Automation Suite - Executable Version

## 🚀 Quick Start

### Option 1: Run the Executable (Recommended)
1. Double-click `SkillRackAutomation.exe`
2. The GUI will open automatically
3. Configure your settings in the Configuration tab
4. Click "Start Automation" to begin

### Option 2: Use the Launcher
1. Double-click `launch.bat`
2. This will automatically detect and run the best available version

## 📋 Requirements

### For Executable Version:
- Windows 10/11 (64-bit)
- Google Chrome browser
- ChromeDriver (download from https://chromedriver.chromium.org/)

### For Python Version:
- Python 3.8+
- Run `install.bat` to install all dependencies

## ⚙️ Setup

1. **Install ChromeDriver:**
   - Download from: https://chromedriver.chromium.org/
   - Make sure it matches your Chrome version
   - Add to PATH or place in the same folder as the executable

2. **Configure Chrome Profile (Optional but Recommended):**
   - In the GUI, go to Configuration tab
   - Set your Chrome profile path for automatic login

3. **Setup Ollama (Optional for AI features):**
   - Install Ollama from: https://ollama.ai/
   - Run: `ollama pull codellama`
   - Start service: `ollama serve`

## 🎯 How to Use

1. **Start the Application:**
   - Run `SkillRackAutomation.exe` or `launch.bat`

2. **Configure Settings:**
   - Go to Configuration tab
   - Adjust typing speed, delays, and AI settings
   - Save configuration

3. **Run Automation:**
   - Click "🚀 Start Automation"
   - Navigate to SkillRack challenge page
   - The automation will solve challenges automatically

4. **Monitor Progress:**
   - Watch real-time logs in the Automation Control tab
   - Check statistics and status updates

## 🔧 Troubleshooting

### Common Issues:

1. **"ChromeDriver not found"**
   - Download ChromeDriver matching your Chrome version
   - Add to system PATH or place in executable folder

2. **"Session lost" errors**
   - Set Chrome profile path in configuration
   - Ensure Chrome is not running other instances

3. **AI generation fails**
   - Check if Ollama is running: `ollama serve`
   - Verify model is installed: `ollama list`

4. **Typing too fast/slow**
   - Adjust typing speed in Configuration tab
   - Try different delay settings

### Getting Help:
- Check the Logs tab for detailed error information
- Review configuration settings
- Ensure all requirements are met

## 📝 Files Included

- `SkillRackAutomation.exe` - Main executable
- `launch.bat` - Launcher script
- `install.bat` - Dependency installer (for Python version)
- `config.json` - Configuration file
- `README.md` - This file

## ⚖️ Legal Notice

This tool is for educational purposes only. Use responsibly and in accordance with SkillRack's terms of service and your academic institution's policies.

## 🎉 Enjoy!

Happy coding and good luck with your challenges! 🚀
'''
    
    with open('README_EXECUTABLE.md', 'w') as f:
        f.write(readme_content)
    
    print("✅ Executable README created: README_EXECUTABLE.md")

def package_distribution():
    """Package everything for distribution."""
    if not os.path.exists('dist/SkillRackAutomation.exe'):
        print("❌ Executable not found. Build it first.")
        return False
    
    # Create distribution folder
    dist_folder = Path('SkillRackAutomation_Distribution')
    if dist_folder.exists():
        shutil.rmtree(dist_folder)
    
    dist_folder.mkdir()
    
    # Copy files
    files_to_copy = [
        ('dist/SkillRackAutomation.exe', 'SkillRackAutomation.exe'),
        ('launch.bat', 'launch.bat'),
        ('install.bat', 'install.bat'),
        ('config.json', 'config.json'),
        ('README_EXECUTABLE.md', 'README.md'),
        ('requirements.txt', 'requirements.txt')
    ]
    
    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, dist_folder / dst)
            print(f"✅ Copied {src} → {dst}")
    
    print(f"\n📦 Distribution package created: {dist_folder.absolute()}")
    print("\n🎉 Ready for distribution!")
    print("\nContents:")
    for item in dist_folder.iterdir():
        print(f"   - {item.name}")
    
    return True

def main():
    """Main build function."""
    print("🔨 SkillRack Automation Suite - Build Script")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        return
    
    # Create supporting files
    create_installer_script()
    create_launcher_script() 
    create_readme_for_executable()
    
    # Build executable
    print("\n🔨 Building executable...")
    if build_executable():
        print("\n📦 Packaging distribution...")
        package_distribution()
        
        print("\n" + "=" * 50)
        print("🎉 BUILD COMPLETED SUCCESSFULLY!")
        print("=" * 50)
        print("\n📁 Files created:")
        print("   - dist/SkillRackAutomation.exe (Main executable)")
        print("   - SkillRackAutomation_Distribution/ (Distribution package)")
        print("   - launch.bat (Launcher script)")
        print("   - install.bat (Installer script)")
        print("\n🚀 To test: Double-click SkillRackAutomation.exe")
        print("📦 To distribute: Share the SkillRackAutomation_Distribution folder")
    else:
        print("\n❌ Build failed. Check errors above.")

if __name__ == "__main__":
    main()