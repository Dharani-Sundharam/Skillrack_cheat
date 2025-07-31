
"""
Offline Demo of SkillRack Automation Tool
Demonstrates GUI features without browser automation
"""

import tkinter as tk
from tkinter import messagebox
import threading
import time

class OfflineDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🚀 SkillRack Automation - Offline Demo")
        self.root.geometry("800x600")
        self.root.configure(bg='#2c3e50')
        
        self.create_demo_ui()
        
    def create_demo_ui(self):
        """Create demo interface."""
        # Header
        header = tk.Label(self.root, text="🎯 SkillRack Automation Tool - Demo Mode", 
                         font=('Arial', 18, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        header.pack(pady=20)
        
        # Info panel
        info_frame = tk.Frame(self.root, bg='#34495e', relief='raised', bd=2)
        info_frame.pack(fill=tk.X, padx=20, pady=10)
        
        info_text = """
🎮 Demo Features Available:
• 🔢 Captcha solving simulation
• 🤖 AI chat interface (mock responses)
• ⚙️ Configuration testing
• 📋 Log display
• 🎨 GUI themes and layouts

⚠️ Note: Browser automation disabled in demo mode
        """
        
        tk.Label(info_frame, text=info_text, font=('Arial', 11), 
                bg='#34495e', fg='#ecf0f1', justify='left').pack(pady=15, padx=15)
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='#2c3e50')
        button_frame.pack(pady=20)
        
        # Demo buttons
        buttons = [
            ("🔢 Demo Captcha Solving", self.demo_captcha, '#e74c3c'),
            ("🤖 Demo AI Chat", self.demo_ai_chat, '#9b59b6'),
            ("📊 Demo Statistics", self.demo_stats, '#3498db'),
            ("🧪 Run System Tests", self.run_tests, '#27ae60'),
            ("🚀 Launch Full GUI", self.launch_full_gui, '#f39c12'),
        ]
        
        for text, command, color in buttons:
            btn = tk.Button(button_frame, text=text, command=command,
                          bg=color, fg='white', font=('Arial', 12, 'bold'),
                          width=20, height=2, cursor='hand2')
            btn.pack(pady=5)
        
        # Status area
        self.status_frame = tk.Frame(self.root, bg='#1a252f', relief='sunken', bd=2)
        self.status_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        tk.Label(self.status_frame, text="📋 Demo Console", 
                font=('Arial', 12, 'bold'), bg='#1a252f', fg='#00ff00').pack(pady=5)
        
        self.console = tk.Text(self.status_frame, bg='#1a252f', fg='#00ff00',
                              font=('Consolas', 10), wrap=tk.WORD)
        self.console.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.log("🎯 Welcome to SkillRack Automation Demo!")
        self.log("💡 Click buttons above to test different features")
        
    def log(self, message):
        """Add message to console."""
        timestamp = time.strftime("%H:%M:%S")
        self.console.insert(tk.END, f"[{timestamp}] {message}\n")
        self.console.see(tk.END)
        self.root.update()
        
    def demo_captcha(self):
        """Demonstrate captcha solving."""
        self.log("🔢 Starting captcha solving demo...")
        
        # Simulate captcha processing
        test_expressions = ["15 + 23", "42 - 17", "8 * 9", "64 / 8"]
        results = [38, 25, 72, 8]
        
        for expr, result in zip(test_expressions, results):
            self.log(f"🖼️ Processing captcha image...")
            time.sleep(0.5)
            self.log(f"🧮 Found expression: {expr}")
            time.sleep(0.3)
            self.log(f"✅ Calculated result: {result}")
            time.sleep(0.3)
            self.log(f"💉 Entered result in captcha field")
            time.sleep(0.5)
            
        self.log("🎉 Captcha solving demo completed!")
        
    def demo_ai_chat(self):
        """Demonstrate AI chat."""
        self.log("🤖 Starting AI chat demo...")
        
        # Simulate AI conversation
        conversations = [
            ("User", "Analyze this array problem"),
            ("AI", "This is a classic array manipulation problem requiring O(n) time complexity..."),
            ("User", "Generate a solution"),
            ("AI", "Here's a complete C++ solution:\n\n#include <iostream>\nusing namespace std;\n\nint main() {\n    // Solution code here\n    return 0;\n}"),
            ("User", "Can you optimize this?"),
            ("AI", "Yes! We can improve space complexity from O(n) to O(1) by using two pointers...")
        ]
        
        for sender, message in conversations:
            self.log(f"💬 {sender}: {message[:50]}{'...' if len(message) > 50 else ''}")
            time.sleep(1)
            
        self.log("✅ AI chat demo completed!")
        
    def demo_stats(self):
        """Show demo statistics."""
        self.log("📊 Generating demo statistics...")
        
        stats = [
            "🎯 Challenges solved: 15",
            "⚡ Success rate: 93%",
            "🔢 Captchas solved: 8",
            "🤖 AI solutions generated: 3",
            "⏱️ Average solve time: 45s",
            "🚀 Total session time: 12m 30s"
        ]
        
        for stat in stats:
            self.log(stat)
            time.sleep(0.3)
            
        self.log("📈 Statistics demo completed!")
        
    def run_tests(self):
        """Run system tests."""
        self.log("🧪 Running system tests...")
        
        # Run in background thread
        threading.Thread(target=self.test_runner, daemon=True).start()
        
    def test_runner(self):
        """Background test runner."""
        tests = [
            ("Testing GUI dependencies", True),
            ("Testing OpenCV installation", True),
            ("Testing AI connection", False),
            ("Testing configuration file", True),
            ("Testing captcha processing", True),
        ]
        
        for test_name, success in tests:
            self.log(f"🔍 {test_name}...")
            time.sleep(1)
            
            if success:
                self.log(f"✅ {test_name}: PASSED")
            else:
                self.log(f"❌ {test_name}: FAILED (Ollama not running)")
                
        self.log("🎉 System tests completed!")
        self.log("💡 For AI features, install and start Ollama")
        
    def launch_full_gui(self):
        """Launch the full GUI."""
        self.log("🚀 Launching full SkillRack Automation GUI...")
        
        result = messagebox.askyesno(
            "Launch Full GUI",
            "This will close the demo and launch the full automation tool.\n\n"
            "The full GUI includes:\n"
            "• Real browser automation\n"
            "• Live SkillRack integration\n"
            "• Complete AI chat features\n"
            "• Actual captcha solving\n\n"
            "Continue?"
        )
        
        if result:
            self.log("🔄 Starting full application...")
            self.root.destroy()
            
            # Import and run the full GUI
            try:
                import subprocess
                subprocess.Popen(['python', 'run_gui.py'])
            except Exception as e:
                print(f"Error launching full GUI: {e}")
                print("Please run: python run_gui.py")
        
    def run(self):
        """Start the demo."""
        # Add instructions
        self.log("📖 Instructions:")
        self.log("   • This is a safe demo mode with no browser automation")
        self.log("   • Test all features before using the full version")
        self.log("   • Click '🚀 Launch Full GUI' when ready for real automation")
        self.log("")
        
        self.root.mainloop()

if __name__ == "__main__":
    print("🎮 Starting SkillRack Automation Demo...")
    demo = OfflineDemo()
    demo.run()