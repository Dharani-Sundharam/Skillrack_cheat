
"""
Test script for SkillRack Automation Tool
Tests basic functionality and AI integration
"""

import os
import sys
import json
import time

def test_basic_processing():
    """Test basic mathematical expression processing."""
    print("\n🧮 Testing Basic Mathematical Processing...")
    
    print("✅ Basic processing initialized")
    
    # Test expression parsing
    test_expressions = [
        "15+23",
        "42 - 17", 
        "8 * 9",
        "100/4"
    ]
    
    expected_results = [38, 25, 72, 25]
    
    for i, expr in enumerate(test_expressions):
        result = calculate_test_expression(expr)
        expected = expected_results[i]
        if result == expected:
            print(f"✅ Expression '{expr}' = {result} (correct)")
        else:
            print(f"❌ Expression '{expr}' = {result}, expected {expected}")

def calculate_test_expression(expression):
    """Test version of expression calculator."""
    import re
    
    # Clean and parse
    expression = expression.replace(" ", "")
    pattern = r'(\d+)\s*([+\-*/])\s*(\d+)'
    match = re.match(pattern, expression)
    
    if not match:
        return None
        
    num1, operator, num2 = match.groups()
    num1, num2 = int(num1), int(num2)
    
    if operator == '+':
        return num1 + num2
    elif operator == '-':
        return num1 - num2
    elif operator == '*':
        return num1 * num2
    elif operator == '/':
        return num1 // num2 if num2 != 0 else None
    
    return None

def test_ai_connection():
    """Test AI/Ollama connection."""
    print("\n🤖 Testing AI Connection...")
    
    try:
        import requests
        
        # Test if Ollama is running
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        
        if response.status_code == 200:
            models = response.json().get('models', [])
            print(f"✅ Ollama is running with {len(models)} models")
            
            for model in models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 0) // (1024*1024*1024)  # Convert to GB
                print(f"   📦 {name} ({size}GB)")
                
            # Test a simple generation
            if models:
                test_model = models[0]['name']
                print(f"\n🧪 Testing generation with {test_model}...")
                
                test_response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={
                        "model": test_model,
                        "prompt": "What is 2 + 2? Answer with just the number.",
                        "stream": False
                    },
                    timeout=10
                )
                
                if test_response.status_code == 200:
                    result = test_response.json().get('response', '').strip()
                    print(f"✅ AI Response: '{result}'")
                else:
                    print(f"❌ AI Generation failed: {test_response.status_code}")
            else:
                print("⚠️ No models installed. Run: ollama pull codellama:7b")
                
        else:
            print("❌ Ollama not running. Start with: ollama serve")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to Ollama (not installed or not running)")
        print("   Install: https://ollama.ai")
        print("   Start: ollama serve")
    except Exception as e:
        print(f"❌ AI test error: {e}")

def test_gui_dependencies():
    """Test GUI and automation dependencies."""
    print("\n🎨 Testing GUI Dependencies...")
    
    try:
        import tkinter as tk
        print("✅ Tkinter (GUI) available")
    except ImportError:
        print("❌ Tkinter not available (install python3-tk on Linux)")
    
    try:
        import selenium
        print("✅ Selenium imported")
    except ImportError:
        print("❌ Selenium not available")
    
    try:
        import pyautogui
        print("✅ PyAutoGUI imported")
    except ImportError:
        print("❌ PyAutoGUI not available")

def test_config_file():
    """Test configuration file."""
    print("\n⚙️ Testing Configuration...")
    
    if os.path.exists("config.json"):
        try:
            with open("config.json", 'r') as f:
                config = json.load(f)
            
            print("✅ config.json loaded successfully")
            
            # Check required keys
            required_keys = [
                "driver_wait_time", "typing_speed", "human_delays",
                "ollama_enabled", "ollama_url", "ollama_model"
            ]
            
            for key in required_keys:
                if key in config:
                    print(f"   ✅ {key}: {config[key]}")
                else:
                    print(f"   ❌ Missing: {key}")
                    
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config.json: {e}")
    else:
        print("⚠️ config.json not found (will use defaults)")

def run_all_tests():
    """Run all tests."""
    print("🧪 SkillRack Automation Tool - System Test")
    print("=" * 50)
    
    test_gui_dependencies()
    test_config_file()
    test_basic_processing()
    test_ai_connection()
    
    print("\n" + "=" * 50)
    print("🎯 Test Summary:")
    print("   - If all tests pass ✅, you're ready to go!")
    print("   - If any tests fail ❌, check the installation guide")
    print("   - For AI features, make sure Ollama is installed and running")
    print("\n🚀 Start the application with: python run_gui.py")

if __name__ == "__main__":
    run_all_tests()