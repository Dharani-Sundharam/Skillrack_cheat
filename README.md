# 🚀 SkillRack Automation Tool

**Professional automation solution for SkillRack coding challenges with AI integration.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey.svg)

## ⚠️ **Important Disclaimers**

### 🎯 **Solution Availability**
**This tool ONLY works for SkillRack problems that have a "View Solution" button available.** The automation primarily:
- ✅ **Extracts existing solutions** from problems with "View Solution" 
- ✅ **Uses AI as backup** when solutions aren't available (with user confirmation)
- ❌ **Cannot solve problems without solutions** unless AI generates working code

### 🐛 **Bug Reporting**
This tool is in active development and may contain bugs. If you encounter any issues:

1. **🔍 Check existing issues**: [GitHub Issues](https://github.com/Dharani-Sundharam/Skillrack_cheat/issues)
2. **📝 Report new bugs**: [Create New Issue](https://github.com/Dharani-Sundharam/Skillrack_cheat/issues/new)
3. **📋 Include details**: Error messages, screenshots, steps to reproduce
4. **⚡ Get support**: Community help and developer responses

### 📚 **Educational Use**
This tool is intended for educational purposes and learning automation concepts. Use responsibly and in accordance with SkillRack's terms of service.

## ✨ Features

### 🎯 **Core Automation**
- **Smart Solution Detection** - Automatically finds and extracts "View Solution" content
- **AI-Powered Code Generation** - Uses Ollama/CodeLlama when solutions aren't available
- **Intelligent Typing** - Human-like typing with auto-completion handling
- **Session Management** - Robust browser session handling with auto-recovery
- **Auto-Completion Bypass** - Smart handling of SkillRack's ACE editor auto-pairing

### 🤖 **AI Integration**
- **Interactive AI Chat** - Real-time conversation with coding assistant
- **Question Analysis** - Detailed problem breakdown and approach suggestions
- **Code Generation** - Complete solution generation with multiple attempts
- **Code Injection** - Controlled code insertion with user confirmation

### 🎨 **User Interface**
- **Modern GUI** - Beautiful, intuitive interface with dark theme
- **Multi-Tab Layout** - Automation Control, AI Chat, Configuration, Logs
- **Real-Time Feedback** - Live status updates and progress tracking
- **Keyboard Shortcuts** - Quick actions with Ctrl+Enter, F5, etc.

### 🔒 **Anti-Detection**
- **Human-like Behavior** - Random delays, realistic typing patterns
- **WebDriver Masking** - Removes automation signatures
- **Session Validation** - Maintains stable browser connections
- **Smart Error Recovery** - Automatic handling of page errors

## 📋 Requirements

### 💻 **System Requirements**
- **Python 3.8+** (tested on 3.8, 3.9, 3.10, 3.11)
- **Chrome Browser** (latest version recommended)
- **Windows 10/11, macOS 10.14+, or Linux** (Ubuntu 18.04+)
- **4GB RAM minimum** (8GB recommended for AI features)
- **Internet connection** for SkillRack access and AI models

### 🛠 **Dependencies**
All dependencies are automatically installed via `requirements.txt`:
- `selenium` - Web automation and browser control
- `beautifulsoup4` - HTML parsing and content extraction
- `pyautogui` - Keyboard and mouse automation
- `requests` - HTTP requests for AI integration
- `pyperclip` - Clipboard operations
- `lxml` - XML/HTML processing

## 🚀 Quick Start

### 1️⃣ **Installation**

```bash
# Clone the repository
git clone https://github.com/yourusername/skillrack-automation.git
cd skillrack-automation

# Install dependencies
pip install -r requirements.txt

# Install Chrome WebDriver (automatic)
python run_gui.py  # Will guide you through setup
```

### 2️⃣ **Setup AI (Optional but Recommended)**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh  # Linux/macOS
# Or download from https://ollama.ai for Windows

# Start Ollama service
ollama serve

# Install CodeLlama model (recommended)
ollama pull codellama:7b

# Or install other models
ollama pull llama2:7b
ollama pull mistral:7b
```

### 3️⃣ **Launch the Application**

```bash
# Option 1: GUI (Recommended)
python run_gui.py

# Option 2: Command Line
python skillrack_automation.py

# Option 3: Create Executable
python build_executable.py
./dist/skillrack_gui.exe  # Windows
./dist/skillrack_gui      # Linux/macOS
```

## 📖 User Guide

### 🎮 **Using the GUI**

#### **Step 1: Open Browser & SkillRack**
1. Launch the GUI: `python run_gui.py`
2. Click **🌐 Step 1: Open Browser & SkillRack**
3. Login to your SkillRack account
4. Navigate to any coding challenge

#### **Step 2: Choose Your Workflow**

##### **🎯 Automation Control Tab**
- **🎯 Solve Current Challenge** - Auto-solve the current problem
- **🔄 Continuous Mode** - Solve multiple challenges in sequence
- **⏹️ Stop All** - Emergency stop for all automation

##### **🤖 AI Chat Tab**
1. **📄 Scrape Question** - Extract problem text from current page
2. **🧠 Analyze Question** - Get AI analysis and approach
3. **⚡ Generate Solution** - Create complete code solution
4. **💬 Free Chat** - Ask AI anything about the problem
5. **💉 Inject Code** - Insert generated code with 3-second countdown
6. **⚙️ Configure Settings** - Adjust typing speed, delays, and AI options

##### **⚙️ Configuration Tab**
- Adjust typing speeds, delays, AI settings
- Enable/disable features
- Configure Ollama connection
- Set browser preferences

##### **📋 Logs Tab**
- Real-time operation logs
- Error messages and debugging info
- Export logs for troubleshooting

### ⚡ **Keyboard Shortcuts**
- **Ctrl+Enter** or **F5** - Solve current challenge
- **Ctrl+Q** - Stop all automation
- **Ctrl+Return** (in AI chat) - Send message

### 🤖 **Auto-Completion Handling**

The tool intelligently handles SkillRack's ACE editor auto-completion:

1. **Disable Auto-pairing** - Turns off automatic brace/bracket insertion
2. **Smart Typing** - Handles any remaining auto-completion gracefully  
3. **Brace Management** - Ensures proper code formatting without extra characters
4. **Fast Processing** - Maintains typing speed while preventing formatting issues

**Example**: Types `{` without auto-inserted `}` → Clean, properly formatted code

## ⚙️ Configuration

### 📝 **config.json Settings**

```json
{
  "driver_wait_time": 10,
  "typing_speed": {
    "min": 0.01,
    "max": 0.04
  },
  "human_delays": {
    "min": 0.3,
    "max": 0.8
  },
  "ollama_enabled": true,
  "ollama_url": "http://localhost:11434",
  "ollama_model": "codellama:7b",
  "headless": false,
  "window_size": [1920, 1080],
  "auto_close_browser": true,
  "max_retry_attempts": 3,
  "session_timeout": 300
}
```

### 🎯 **Key Settings Explained**

| Setting | Description | Recommended Value |
|---------|-------------|-------------------|
| `typing_speed.min/max` | Typing delay range (seconds) | 0.01 - 0.04 |
| `human_delays.min/max` | Pause between actions | 0.3 - 0.8 |
| `ollama_model` | AI model to use | `codellama:7b` |
| `headless` | Run browser in background | `false` |
| `session_timeout` | Browser timeout (seconds) | 300 |

## 🤖 AI Integration

### 📋 **Supported Models**
- **CodeLlama** (Recommended) - Specialized for coding
- **Llama2** - General purpose, good for explanations  
- **Mistral** - Fast and efficient
- **Custom models** - Any Ollama-compatible model

### 💬 **AI Chat Features**

#### **Question Analysis**
```
User: "Analyze this problem"
AI: "This is a dynamic programming problem requiring:
     1. Understanding optimal substructure
     2. Memoization for efficiency
     3. Bottom-up approach recommended..."
```

#### **Code Generation**
```
User: "Generate solution"
AI: "Here's the complete C++ solution:

#include <iostream>
#include <vector>
using namespace std;

int main() {
    // Complete working solution...
}"
```

#### **Interactive Help**
```
User: "How can I optimize this solution?"
AI: "You can improve performance by:
     1. Using iterative instead of recursive approach
     2. Reducing space complexity from O(n) to O(1)
     3. Early termination for edge cases..."
```

## 🔧 Troubleshooting

### ❌ **Common Issues & Solutions**

#### **🌐 Browser Issues**
```bash
# Issue: ChromeDriver not found
Solution: 
- Update Chrome browser
- Download ChromeDriver from https://chromedriver.chromium.org/
- Place in system PATH or project directory

# Issue: Browser crashes/closes
Solution:
- Check available memory (close other applications)
- Disable other Chrome extensions
- Run with --headless mode
```

#### **🤖 AI Issues**
```bash
# Issue: "AI not found" message
Solution:
1. Install Ollama: https://ollama.ai
2. Start service: ollama serve
3. Install model: ollama pull codellama:7b
4. Check config.json settings

# Issue: Slow AI responses
Solution:
- Use smaller models (7b instead of 13b)
- Increase timeout in config
- Check system resources
```

#### **🤖 Auto-Completion Issues**
```bash
# Issue: Extra braces or brackets in typed code
Solution:
- Tool automatically disables auto-completion
- Smart typing handles remaining auto-pairing
- If issues persist, report with code example
- Manual editing may be needed in rare cases
```

#### **⌨️ Typing Issues**
```bash
# Issue: Code not typed correctly
Solution:
- Click on code editor area manually
- Check PyAutoGUI permissions (macOS/Linux)
- Increase typing delays in config
- Verify browser focus
```

### 🔍 **Debug Mode**

Enable detailed logging:
```bash
# GUI with debug
python run_gui.py --debug

# Command line with verbose logs
python skillrack_automation.py --verbose

# Check log files
tail -f skillrack_automation.log
```

### 📊 **Performance Optimization**

```bash
# For faster operation
{
  "typing_speed": {"min": 0.005, "max": 0.02},
  "human_delays": {"min": 0.1, "max": 0.3},
  "headless": true
}

# For stealth operation  
{
  "typing_speed": {"min": 0.05, "max": 0.15},
  "human_delays": {"min": 1.0, "max": 3.0},
  "headless": false
}
```

## 🏗️ Advanced Usage

### 🔄 **Batch Processing**
```bash
# Process multiple challenges
python batch_solver.py --count 10 --delay 30

# With specific URLs
python batch_solver.py --urls urls.txt --ai-fallback
```

### 🎮 **Custom Workflows**
```python
from skillrack_automation import SkillRackAutomator

# Custom automation script
automator = SkillRackAutomator()
automator.setup_driver()

# Your custom logic here
success = automator.solve_current_challenge()
```

### 📦 **Building Executables**
```bash
# Create standalone executable
python build_executable.py

# Custom build options
pyinstaller --onefile --noconsole skillrack_gui.py
```

## 🤝 Contributing

### 🌟 **How to Contribute**

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open Pull Request**

### 🐛 **Reporting Issues**

When reporting bugs, please include:
- Operating system and version
- Python version
- Chrome/ChromeDriver versions
- Error logs from `skillrack_automation.log`
- Steps to reproduce
- Screenshots if applicable

### 💡 **Feature Requests**

We welcome suggestions for:
- New AI models and integrations
- Additional automation features
- UI/UX improvements
- Performance optimizations
- Security enhancements

## 📄 Legal & Ethics

### ⚖️ **Disclaimer**

This tool is intended for:
- **Educational purposes** - Learning automation and AI concepts
- **Personal practice** - Improving programming skills
- **Research** - Understanding web automation techniques

### 📋 **Responsible Usage**

- **Respect SkillRack's Terms of Service**
- **Don't use for unfair advantages in competitions**
- **Rate limit your usage** to avoid server overload
- **Report security issues** responsibly

### 🔒 **Privacy & Security**

- **No data collection** - All processing is local
- **Secure credentials** - Use environment variables for sensitive data
- **Open source** - Full transparency in code

## 📞 Support & Community

### 🆘 **Getting Help**

1. **📖 Check this README** - Most questions are answered here
2. **🔍 Search Issues** - Someone might have had the same problem
3. **📝 Create New Issue** - Provide detailed information
4. **💬 Discussions** - General questions and feature ideas

### 🌐 **Community Links**

- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: General help and community chat
- **Wiki**: Extended documentation and tutorials
- **Releases**: Latest versions and changelogs

### 📧 **Contact**

- **GitHub**: [@yourusername](https://github.com/yourusername)
- **Issues**: [Project Issues](https://github.com/yourusername/skillrack-automation/issues)
- **Email**: support@yourproject.com (for security issues only)

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/skillrack-automation?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/skillrack-automation?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/skillrack-automation)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/skillrack-automation)

## 📈 Changelog

### 🚀 **v2.0.0** (Latest)
- ✨ Added comprehensive AI Chat interface
- 🤖 Implemented smart auto-completion handling
- 🎨 Complete GUI redesign with modern dark theme
- 🧠 Enhanced AI integration with multiple models
- 🔧 Improved error handling and session management
- 📋 Real-time logging and status updates
- ⚡ Performance optimizations and bug fixes

### 📜 **Previous Versions**
- **v1.2.0** - Added basic AI integration
- **v1.1.0** - Introduced GUI interface  
- **v1.0.0** - Initial release with CLI automation

## 📄 License

```
MIT License

Copyright (c) 2024 SkillRack Automation Project

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

<div align="center">

**⭐ If you find this tool helpful, please give it a star! ⭐**

**🚀 Ready to automate your SkillRack journey? Let's get started! 🚀**

</div>
