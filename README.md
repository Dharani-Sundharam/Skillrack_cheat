# SkillRack Automation Suite 🚀

An intelligent automation tool for SkillRack coding challenges that mimics human behavior to solve programming problems automatically. This tool can extract solutions from the platform or generate them using a local Ollama LLM.

## ✨ Features

- **Human-like Behavior**: Simulates realistic typing patterns with random delays and occasional typos
- **Solution Detection**: Automatically detects and clicks "View Solution" buttons
- **Code Extraction**: Intelligently extracts clean code from highlighted solution blocks
- **Error Handling**: Detects compilation errors and retries automatically
- **Ollama Integration**: Uses local LLM to generate solutions when no solution is provided
- **Batch Processing**: Solve multiple challenges sequentially
- **Stealth Mode**: Bypasses basic automation detection
- **Configurable**: Highly customizable timing, behavior, and retry settings

## 🛠️ Prerequisites

### Required Software

1. **Python 3.8+**
   ```bash
   python --version  # Should be 3.8 or higher
   ```

2. **Google Chrome Browser**
   - Download from [chrome.google.com](https://www.google.com/chrome/)

3. **ChromeDriver**
   - **Option 1 (Recommended)**: Install using Chrome for Testing
     ```bash
     # Windows (using chocolatey)
     choco install chromedriver
     
     # macOS (using homebrew)
     brew install chromedriver
     
     # Linux (manual download)
     # Visit https://chromedriver.chromium.org/downloads
     ```
   
   - **Option 2**: Download manually
     - Visit [ChromeDriver Downloads](https://chromedriver.chromium.org/downloads)
     - Download version matching your Chrome browser
     - Add to PATH or place in project directory

### Optional: Ollama Setup (for AI-generated solutions)

1. **Install Ollama**
   ```bash
   # Windows/macOS/Linux
   curl -fsSL https://ollama.ai/install.sh | sh
   ```

2. **Install a coding model**
   ```bash
   ollama pull codellama
   # or
   ollama pull deepseek-coder
   ```

3. **Start Ollama service**
   ```bash
   ollama serve
   ```

## 📦 Installation

1. **Clone or Download the Project**
   ```bash
   git clone <repository-url>
   cd skillrack-automation
   ```
   
   Or download the files manually and extract them.

2. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python skillrack_automation.py --help
   ```

## ⚙️ Configuration

The script uses a `config.json` file for customization. A default config is created automatically on first run.

### Configuration Options

```json
{
    "chrome_profile_path": "",           // Path to Chrome profile (optional)
    "typing_speed": {
        "min": 0.05,                     // Minimum delay between keystrokes (seconds)
        "max": 0.15                      // Maximum delay between keystrokes (seconds)
    },
    "human_delays": {
        "min": 1,                        // Minimum delay between actions (seconds)
        "max": 3                         // Maximum delay between actions (seconds)
    },
    "retry_attempts": 3,                 // Number of retry attempts for failed solutions
    "ollama_enabled": false,             // Enable Ollama LLM integration
    "ollama_url": "http://localhost:11434", // Ollama server URL
    "ollama_model": "codellama",         // Ollama model to use
    "headless": false,                   // Run browser in headless mode
    "timeout": 30                        // Element wait timeout (seconds)
}
```

### Chrome Profile Setup (Recommended)

Using your existing Chrome profile allows the script to access your logged-in SkillRack session:

1. **Find your Chrome profile path:**
   - **Windows**: `C:\Users\[Username]\AppData\Local\Google\Chrome\User Data`
   - **macOS**: `~/Library/Application Support/Google/Chrome`
   - **Linux**: `~/.config/google-chrome`

2. **Update config.json:**
   ```json
   {
       "chrome_profile_path": "C:\\Users\\YourName\\AppData\\Local\\Google\\Chrome\\User Data"
   }
   ```

## 🚀 Usage

### Single Challenge Mode

1. **Run the script:**
   ```bash
   python skillrack_automation.py
   ```

2. **Follow the prompts:**
   - A Chrome browser will open
   - Navigate to your SkillRack challenge page
   - Press Enter in the terminal to start automation

3. **Watch the magic happen!**
   - The script will detect if a "View Solution" button exists
   - If found, it will click it and extract the solution
   - If not found, it will use Ollama (if enabled) to generate a solution
   - Code will be typed into the editor with human-like behavior
   - The solution will be submitted and tested

### Batch Processing Mode

For solving multiple challenges sequentially:

```bash
python batch_solver.py
```

This mode will:
- Process multiple challenges in sequence
- Navigate between challenges automatically
- Provide a summary report at the end

### Advanced Usage

#### Using with Ollama for Custom Solutions

1. **Enable Ollama in config.json:**
   ```json
   {
       "ollama_enabled": true,
       "ollama_model": "codellama"
   }
   ```

2. **Ensure Ollama is running:**
   ```bash
   ollama serve
   ```

3. **Run the script normally** - it will use AI when no solution button is available

#### Headless Mode (Background Processing)

```json
{
    "headless": true
}
```

#### Custom Timing for Different Behavior

```json
{
    "typing_speed": {"min": 0.02, "max": 0.08},  // Faster typing
    "human_delays": {"min": 0.5, "max": 1.5}     // Shorter delays
}
```

## 📁 Project Structure

```
skillrack-automation/
├── skillrack_automation.py    # Main automation script
├── batch_solver.py           # Batch processing script
├── config.json              # Configuration file
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── skillrack_automation.log # Log file (created after first run)
```

## 🔧 Troubleshooting

### Common Issues

#### ChromeDriver Issues
```
selenium.common.exceptions.WebDriverException: 'chromedriver' executable needs to be in PATH
```
**Solution**: Install ChromeDriver and add to PATH, or place in project directory.

#### Element Not Found Errors
```
selenium.common.exceptions.NoSuchElementException: Unable to locate element
```
**Solutions**:
- Increase timeout in config.json
- Ensure you're on the correct SkillRack page
- Check if page structure has changed

#### Typing Not Working
**Possible causes**:
- Code editor not properly focused
- Page not fully loaded
- JavaScript interference

**Solutions**:
- Increase human_delays in config
- Ensure page is fully loaded before running
- Try different browser profile

#### Ollama Connection Issues
```
requests.exceptions.ConnectionError: Failed to establish a new connection
```
**Solutions**:
- Ensure Ollama is running: `ollama serve`
- Check Ollama URL in config.json
- Verify model is installed: `ollama list`

### Debug Mode

Enable detailed logging by modifying the script:

```python
logging.basicConfig(level=logging.DEBUG)
```

### Performance Optimization

For faster execution (less human-like):
```json
{
    "typing_speed": {"min": 0.01, "max": 0.03},
    "human_delays": {"min": 0.2, "max": 0.5}
}
```

## 🔒 Important Notes

### Legal and Ethical Considerations

- **Use Responsibly**: This tool is for educational purposes and personal learning
- **Respect Platform Terms**: Ensure your usage complies with SkillRack's terms of service
- **Academic Integrity**: Don't use this to cheat in academic assessments
- **Rate Limiting**: The tool includes human-like delays to avoid overwhelming the server

### Security

- The script doesn't collect or transmit any personal data
- All processing happens locally on your machine
- Chrome profile access is read-only for session cookies

### Limitations

- May not work with all SkillRack page layouts (update selectors if needed)
- Requires active internet connection for Ollama features
- Success depends on solution availability or LLM capability

## 🤝 Contributing

### Reporting Issues

1. Check existing issues first
2. Provide detailed error messages and logs
3. Include your configuration (remove sensitive data)
4. Specify your OS and browser versions

### Feature Requests

- New language support
- Different coding platforms
- Enhanced AI integration
- Better stealth features

## 📝 Changelog

### Version 1.0.0
- Initial release with basic automation
- Solution extraction and typing
- Human-like behavior simulation
- Ollama integration
- Batch processing support
- Comprehensive error handling

## 📞 Support

If you encounter issues:

1. **Check the logs**: `skillrack_automation.log`
2. **Review this README**: Most common issues are covered
3. **Update dependencies**: `pip install -r requirements.txt --upgrade`
4. **Check ChromeDriver**: Ensure it matches your Chrome version

## ⚖️ License

This project is for educational purposes only. Use responsibly and in accordance with your local laws and the terms of service of the platforms you're automating.

---

**Happy Coding! 🎉**

*Remember: This tool is designed to help you learn and understand coding patterns. Always strive to understand the solutions rather than just submitting them.* 