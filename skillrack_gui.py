#!/usr/bin/env python3
"""
SkillRack Automation GUI
Beautiful, modern interface for SkillRack coding challenge automation.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import json
import os
import sys
import time
from datetime import datetime
import queue
import webbrowser
from skillrack_automation import SkillRackAutomator
from selenium.webdriver.common.by import By

import re

class SkillRackGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.automator = None
        self.is_running = False
        self.challenges_solved = 0
        self.log_queue = queue.Queue()
        
        # Configure main window
        self.setup_main_window()
        self.create_styles()
        self.create_widgets()
        self.load_config()
        
        # Start log monitoring
        self.check_log_queue()
        
    def setup_main_window(self):
        """Configure the main application window."""
        self.root.title("🚀 SkillRack Automation Suite")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Set icon and colors
        self.root.configure(bg='#2c3e50')
        
        # Center window on screen
        self.center_window()
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
    def create_styles(self):
        """Create modern styling for the interface."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Configure custom styles
        self.style.configure('Title.TLabel', 
                           font=('Arial', 24, 'bold'), 
                           foreground='#ecf0f1',
                           background='#2c3e50')
        
        self.style.configure('Subtitle.TLabel',
                           font=('Arial', 12),
                           foreground='#bdc3c7',
                           background='#2c3e50')
        
        self.style.configure('Status.TLabel',
                           font=('Arial', 11, 'bold'),
                           foreground='#27ae60',
                           background='#34495e')
        
        self.style.configure('Action.TButton',
                           font=('Arial', 11, 'bold'),
                           padding=(20, 10))
        
    def create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#2c3e50')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Header section
        self.create_header(main_frame)
        
        # Create notebook for tabbed interface
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        
        # Create tabs
        self.create_automation_tab()
        self.create_ai_chat_tab()
        self.create_config_tab()
        self.create_logs_tab()
        self.create_about_tab()
        
    def create_header(self, parent):
        """Create the header section."""
        header_frame = tk.Frame(parent, bg='#2c3e50')
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title and subtitle
        title_label = ttk.Label(header_frame, 
                               text="🚀 SkillRack Automation Suite",
                               style='Title.TLabel')
        title_label.pack()
        
        subtitle_label = ttk.Label(header_frame,
                                  text="Intelligent coding challenge automation with AI integration",
                                  style='Subtitle.TLabel')
        subtitle_label.pack(pady=(5, 0))
        
        # Status bar
        self.status_frame = tk.Frame(header_frame, bg='#34495e', height=40)
        self.status_frame.pack(fill=tk.X, pady=(15, 0))
        self.status_frame.pack_propagate(False)
        
        self.status_label = ttk.Label(self.status_frame,
                                     text="Ready to start automation",
                                     style='Status.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=20, pady=10)
        
        self.challenges_label = ttk.Label(self.status_frame,
                                         text="Challenges solved: 0",
                                         style='Status.TLabel')
        self.challenges_label.pack(side=tk.RIGHT, padx=20, pady=10)
        
    def create_automation_tab(self):
        """Create the main automation control tab."""
        self.auto_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.auto_frame, text="🎯 Automation Control")
        
        # Left panel - Controls
        left_panel = tk.Frame(self.auto_frame, bg='#34495e', width=400)
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left_panel.pack_propagate(False)
        
        # Control buttons
        controls_frame = tk.Frame(left_panel, bg='#34495e')
        controls_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(controls_frame, text="🎮 Automation Controls", 
                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 15))
        
        # Step 1: Open Browser
        self.browser_btn = tk.Button(controls_frame, text="🌐 Step 1: Open Browser & SkillRack",
                                    command=self.open_browser_step,
                                    bg='#3498db', fg='white', font=('Arial', 12, 'bold'),
                                    height=2, cursor='hand2')
        self.browser_btn.pack(fill=tk.X, pady=5)
        
        # Step 2: Solve Current Challenge  
        self.solve_btn = tk.Button(controls_frame, text="🎯 Step 2: Solve Current Challenge",
                                  command=self.solve_current_challenge,
                                  bg='#27ae60', fg='white', font=('Arial', 12, 'bold'),
                                  height=2, cursor='hand2', state=tk.DISABLED)
        self.solve_btn.pack(fill=tk.X, pady=5)
        
        # Continuous Mode
        self.continuous_btn = tk.Button(controls_frame, text="🔄 Continuous Mode",
                                       command=self.start_continuous_mode,
                                       bg='#9b59b6', fg='white', font=('Arial', 12, 'bold'),
                                       height=2, cursor='hand2', state=tk.DISABLED)
        self.continuous_btn.pack(fill=tk.X, pady=5)
        
        # Stop Button
        self.stop_btn = tk.Button(controls_frame, text="⏹️ Stop All",
                                 command=self.stop_automation,
                                 bg='#e74c3c', fg='white', font=('Arial', 12, 'bold'),
                                 height=2, cursor='hand2', state=tk.DISABLED)
        self.stop_btn.pack(fill=tk.X, pady=5)
        

        
        # Quick actions and shortcuts
        quick_frame = tk.Frame(left_panel, bg='#34495e')
        quick_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(quick_frame, text="⚡ Quick Actions & Shortcuts", 
                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 15))
        
        self.test_btn = tk.Button(quick_frame, text="🧪 Test Connection",
                                 command=self.test_connection,
                                 bg='#f39c12', fg='white', font=('Arial', 11),
                                 height=1, cursor='hand2')
        self.test_btn.pack(fill=tk.X, pady=2)
        
        self.clear_logs_btn = tk.Button(quick_frame, text="🗑️ Clear Logs",
                                       command=self.clear_logs,
                                       bg='#95a5a6', fg='white', font=('Arial', 11),
                                       height=1, cursor='hand2')
        self.clear_logs_btn.pack(fill=tk.X, pady=2)
        
        # Keyboard shortcuts info
        shortcuts_text = tk.Text(quick_frame, height=4, bg='#2c3e50', fg='#bdc3c7',
                                font=('Consolas', 9), wrap=tk.WORD, state=tk.DISABLED,
                                borderwidth=0)
        shortcuts_text.pack(fill=tk.X, pady=(10, 0))
        
        shortcuts_info = "⌨️ Keyboard Shortcuts:\nCtrl+Enter or F5: Solve Challenge\nCtrl+Q: Stop All"
        shortcuts_text.config(state=tk.NORMAL)
        shortcuts_text.insert(tk.END, shortcuts_info)
        shortcuts_text.config(state=tk.DISABLED)
        
        # Statistics panel
        stats_frame = tk.Frame(left_panel, bg='#34495e')
        stats_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Label(stats_frame, text="📊 Session Statistics", 
                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 15))
        
        self.stats_text = tk.Text(stats_frame, height=8, bg='#2c3e50', fg='#ecf0f1',
                                 font=('Consolas', 10), wrap=tk.WORD, state=tk.DISABLED)
        self.stats_text.pack(fill=tk.X)
        
        # Right panel - Real-time logs
        right_panel = tk.Frame(self.auto_frame, bg='#2c3e50')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        tk.Label(right_panel, text="📋 Real-time Logs", 
                font=('Arial', 14, 'bold'), fg='#ecf0f1', bg='#2c3e50').pack(pady=(10, 5))
        
        self.log_display = scrolledtext.ScrolledText(right_panel, 
                                                    bg='#1a252f', fg='#00ff00',
                                                    font=('Consolas', 10),
                                                    wrap=tk.WORD)
        self.log_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
    def create_ai_chat_tab(self):
        """Create the AI chat tab."""
        self.ai_chat_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.ai_chat_frame, text="🤖 AI Chat")
        
        # Main container
        main_container = tk.Frame(self.ai_chat_frame, bg='#ecf0f1')
        main_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Top section - Question and Controls
        top_section = tk.Frame(main_container, bg='#34495e', height=120)
        top_section.pack(fill=tk.X, pady=(0, 10))
        top_section.pack_propagate(False)
        
        tk.Label(top_section, text="📋 Current Question", 
                font=('Arial', 12, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=5)
        
        # Question display area
        self.question_display = scrolledtext.ScrolledText(top_section, height=4, 
                                                         bg='#2c3e50', fg='#ecf0f1',
                                                         font=('Arial', 10), wrap=tk.WORD)
        self.question_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        
        # Control buttons
        button_frame = tk.Frame(top_section, bg='#34495e')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        self.scrape_btn = tk.Button(button_frame, text="📄 Scrape Question",
                                   command=self.scrape_question,
                                   bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                   cursor='hand2')
        self.scrape_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.analyze_btn = tk.Button(button_frame, text="🧠 Analyze Question", 
                                    command=self.analyze_question,
                                    bg='#9b59b6', fg='white', font=('Arial', 10, 'bold'),
                                    cursor='hand2', state=tk.DISABLED)
        self.analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.generate_btn = tk.Button(button_frame, text="⚡ Generate Solution",
                                     command=self.generate_solution,
                                     bg='#e67e22', fg='white', font=('Arial', 10, 'bold'),
                                     cursor='hand2', state=tk.DISABLED)
        self.generate_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.inject_btn = tk.Button(button_frame, text="💉 Inject Code",
                                   command=self.inject_code,
                                   bg='#27ae60', fg='white', font=('Arial', 10, 'bold'),
                                   cursor='hand2', state=tk.DISABLED)
        self.inject_btn.pack(side=tk.RIGHT)
        
        # Middle section - Chat History
        chat_section = tk.Frame(main_container, bg='#ecf0f1')
        chat_section.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        tk.Label(chat_section, text="💬 AI Chat History", 
                font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#ecf0f1').pack(pady=(0, 5))
        
        # Chat display with scrollbar
        chat_container = tk.Frame(chat_section, bg='#ecf0f1')
        chat_container.pack(fill=tk.BOTH, expand=True)
        
        self.chat_display = scrolledtext.ScrolledText(chat_container,
                                                     bg='#ffffff', fg='#2c3e50',
                                                     font=('Arial', 11), wrap=tk.WORD,
                                                     state=tk.DISABLED)
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        
        # Configure chat display tags for styling
        self.chat_display.tag_configure("user", foreground="#2980b9", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("ai", foreground="#8e44ad", font=('Arial', 11, 'bold'))
        self.chat_display.tag_configure("system", foreground="#27ae60", font=('Arial', 10, 'italic'))
        self.chat_display.tag_configure("code", background="#f8f9fa", font=('Consolas', 10))
        
        # Bottom section - Input area
        input_section = tk.Frame(main_container, bg='#ecf0f1', height=100)
        input_section.pack(fill=tk.X)
        input_section.pack_propagate(False)
        
        tk.Label(input_section, text="✍️ Ask the AI", 
                font=('Arial', 12, 'bold'), fg='#2c3e50', bg='#ecf0f1').pack(pady=(0, 5))
        
        # Input frame
        input_frame = tk.Frame(input_section, bg='#ecf0f1')
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Text input area
        self.user_input = tk.Text(input_frame, height=3, bg='#ffffff', fg='#2c3e50',
                                 font=('Arial', 11), wrap=tk.WORD)
        self.user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Send button
        self.send_btn = tk.Button(input_frame, text="📤\nSend",
                                 command=self.send_message,
                                 bg='#3498db', fg='white', font=('Arial', 10, 'bold'),
                                 cursor='hand2', width=8)
        self.send_btn.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind Enter key to send message
        self.user_input.bind('<Control-Return>', lambda e: self.send_message())
        
        # Initialize variables
        self.current_question = ""
        self.current_solution = ""
        self.chat_history = []
        
        # Add welcome message
        self.add_chat_message("system", "Welcome to AI Chat! 🤖\n" +
                             "1. Scrape question from current page\n" +
                             "2. Ask AI to analyze or generate solutions\n" +
                             "3. Inject code when ready\n" +
                             "Use Ctrl+Enter to send messages")
        
    def create_config_tab(self):
        """Create the configuration tab."""
        self.config_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.config_frame, text="⚙️ Configuration")
        
        # Create scrollable frame
        canvas = tk.Canvas(self.config_frame, bg='#ecf0f1')
        scrollbar = ttk.Scrollbar(self.config_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#ecf0f1')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configuration sections
        self.create_config_sections(scrollable_frame)
        
    def create_config_sections(self, parent):
        """Create configuration sections."""
        # Chrome Settings
        chrome_frame = tk.LabelFrame(parent, text="🌐 Chrome Settings", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1')
        chrome_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(chrome_frame, text="Chrome Profile Path:", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.chrome_path_var = tk.StringVar()
        chrome_entry = tk.Entry(chrome_frame, textvariable=self.chrome_path_var, width=50)
        chrome_entry.grid(row=0, column=1, padx=10, pady=5)
        
        tk.Button(chrome_frame, text="Browse", command=self.browse_chrome_path,
                 bg='#3498db', fg='white', cursor='hand2').grid(row=0, column=2, padx=10, pady=5)
        
        self.headless_var = tk.BooleanVar()
        tk.Checkbutton(chrome_frame, text="Headless Mode (Background)", 
                      variable=self.headless_var, bg='#ecf0f1').grid(row=1, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        # Typing Settings
        typing_frame = tk.LabelFrame(parent, text="⌨️ Typing Settings", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1')
        typing_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(typing_frame, text="Typing Speed (min-max seconds):", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        typing_speed_frame = tk.Frame(typing_frame, bg='#ecf0f1')
        typing_speed_frame.grid(row=0, column=1, padx=10, pady=5)
        
        self.typing_min_var = tk.DoubleVar(value=0.01)
        self.typing_max_var = tk.DoubleVar(value=0.04)
        
        tk.Label(typing_speed_frame, text="Min:", bg='#ecf0f1').pack(side=tk.LEFT)
        tk.Entry(typing_speed_frame, textvariable=self.typing_min_var, width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(typing_speed_frame, text="Max:", bg='#ecf0f1').pack(side=tk.LEFT, padx=(10, 0))
        tk.Entry(typing_speed_frame, textvariable=self.typing_max_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Delay Settings
        delay_frame = tk.LabelFrame(parent, text="⏱️ Delay Settings", 
                                  font=('Arial', 12, 'bold'), bg='#ecf0f1')
        delay_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(delay_frame, text="Human Delays (min-max seconds):", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        
        delay_speed_frame = tk.Frame(delay_frame, bg='#ecf0f1')
        delay_speed_frame.grid(row=0, column=1, padx=10, pady=5)
        
        self.delay_min_var = tk.DoubleVar(value=0.3)
        self.delay_max_var = tk.DoubleVar(value=0.8)
        
        tk.Label(delay_speed_frame, text="Min:", bg='#ecf0f1').pack(side=tk.LEFT)
        tk.Entry(delay_speed_frame, textvariable=self.delay_min_var, width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(delay_speed_frame, text="Max:", bg='#ecf0f1').pack(side=tk.LEFT, padx=(10, 0))
        tk.Entry(delay_speed_frame, textvariable=self.delay_max_var, width=8).pack(side=tk.LEFT, padx=5)
        
        # Ollama Settings
        ollama_frame = tk.LabelFrame(parent, text="🤖 AI (Ollama) Settings", 
                                   font=('Arial', 12, 'bold'), bg='#ecf0f1')
        ollama_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.ollama_enabled_var = tk.BooleanVar(value=True)
        tk.Checkbutton(ollama_frame, text="Enable AI Solution Generation", 
                      variable=self.ollama_enabled_var, bg='#ecf0f1').grid(row=0, column=0, columnspan=2, sticky='w', padx=10, pady=5)
        
        tk.Label(ollama_frame, text="Ollama URL:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.ollama_url_var = tk.StringVar(value="http://localhost:11434")
        tk.Entry(ollama_frame, textvariable=self.ollama_url_var, width=30).grid(row=1, column=1, padx=10, pady=5)
        
        tk.Label(ollama_frame, text="Model:", bg='#ecf0f1').grid(row=2, column=0, sticky='w', padx=10, pady=5)
        self.ollama_model_var = tk.StringVar(value="codellama")
        tk.Entry(ollama_frame, textvariable=self.ollama_model_var, width=30).grid(row=2, column=1, padx=10, pady=5)
        
        # Other Settings
        other_frame = tk.LabelFrame(parent, text="🔧 Other Settings", 
                                  font=('Arial', 12, 'bold'), bg='#ecf0f1')
        other_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(other_frame, text="Timeout (seconds):", bg='#ecf0f1').grid(row=0, column=0, sticky='w', padx=10, pady=5)
        self.timeout_var = tk.IntVar(value=30)
        tk.Entry(other_frame, textvariable=self.timeout_var, width=10).grid(row=0, column=1, padx=10, pady=5)
        
        tk.Label(other_frame, text="Retry Attempts:", bg='#ecf0f1').grid(row=1, column=0, sticky='w', padx=10, pady=5)
        self.retry_var = tk.IntVar(value=3)
        tk.Entry(other_frame, textvariable=self.retry_var, width=10).grid(row=1, column=1, padx=10, pady=5)
        
        # Save/Load buttons
        button_frame = tk.Frame(parent, bg='#ecf0f1')
        button_frame.pack(fill=tk.X, padx=20, pady=20)
        
        tk.Button(button_frame, text="💾 Save Configuration", command=self.save_config,
                 bg='#27ae60', fg='white', font=('Arial', 11, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="🔄 Load Configuration", command=self.load_config,
                 bg='#3498db', fg='white', font=('Arial', 11, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=10)
        
        tk.Button(button_frame, text="🔧 Reset to Defaults", command=self.reset_config,
                 bg='#f39c12', fg='white', font=('Arial', 11, 'bold'), cursor='hand2').pack(side=tk.LEFT, padx=10)
        
    def create_logs_tab(self):
        """Create the logs viewing tab."""
        self.logs_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.logs_frame, text="📋 Logs")
        
        # Logs display
        logs_display = scrolledtext.ScrolledText(self.logs_frame, 
                                                bg='#1a252f', fg='#00ff00',
                                                font=('Consolas', 10))
        logs_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Load existing logs
        try:
            with open('skillrack_automation.log', 'r') as f:
                logs_display.insert(tk.END, f.read())
        except FileNotFoundError:
            logs_display.insert(tk.END, "No log file found yet. Logs will appear here once automation starts.\n")
        
        logs_display.config(state=tk.DISABLED)
        
    def create_about_tab(self):
        """Create the about tab."""
        self.about_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.about_frame, text="ℹ️ About")
        
        # About content
        about_content = tk.Text(self.about_frame, wrap=tk.WORD, bg='#ecf0f1', 
                               font=('Arial', 11), padx=20, pady=20)
        about_content.pack(fill=tk.BOTH, expand=True)
        
        about_text = """
🚀 SkillRack Automation Suite v2.0

A sophisticated automation tool for solving SkillRack coding challenges with intelligent behavior simulation and AI integration.

✨ FEATURES:
• Automatic View Solution detection and extraction
• AI-powered solution generation using Ollama
• Human-like typing patterns to bypass detection
• Automatic code editor detection and clearing  
• Session management and error recovery
• Continuous workflow for multiple challenges
• Comprehensive logging and monitoring

🎯 HOW IT WORKS:
1. Prioritizes View Solution buttons (most reliable)
2. Falls back to AI generation when needed (with user confirmation)
3. Automatically clicks and clears code editor
4. Types solutions with human-like speed and patterns
5. Handles multiple challenges in continuous workflow

🤖 AI INTEGRATION:
• Uses Ollama for local AI solution generation
• Strict input/output format compliance
• Solution validation and cleaning
• User confirmation before AI usage

⚙️ CONFIGURATION:
• Customizable typing speeds and delays
• Chrome profile integration
• Headless mode support
• Comprehensive error handling

🔒 ETHICAL USAGE:
This tool is designed for educational purposes and learning coding patterns. 
Always strive to understand the solutions rather than just submitting them.
Respect platform terms of service and academic integrity guidelines.

📧 SUPPORT:
For issues, updates, or contributions, please check the documentation
and log files for troubleshooting information.

Made with ❤️ for the coding community
        """
        
        about_content.insert(tk.END, about_text)
        about_content.config(state=tk.DISABLED)
        
    def browse_chrome_path(self):
        """Browse for Chrome profile path."""
        path = filedialog.askdirectory(title="Select Chrome Profile Directory")
        if path:
            self.chrome_path_var.set(path)
            
    def load_config(self):
        """Load configuration from file."""
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                
            self.chrome_path_var.set(config.get('chrome_profile_path', ''))
            self.headless_var.set(config.get('headless', False))
            
            typing_speed = config.get('typing_speed', {})
            self.typing_min_var.set(typing_speed.get('min', 0.01))
            self.typing_max_var.set(typing_speed.get('max', 0.04))
            
            human_delays = config.get('human_delays', {})
            self.delay_min_var.set(human_delays.get('min', 0.3))
            self.delay_max_var.set(human_delays.get('max', 0.8))
            
            self.ollama_enabled_var.set(config.get('ollama_enabled', True))
            self.ollama_url_var.set(config.get('ollama_url', 'http://localhost:11434'))
            self.ollama_model_var.set(config.get('ollama_model', 'codellama'))
            
            self.timeout_var.set(config.get('timeout', 30))
            self.retry_var.set(config.get('retry_attempts', 3))
            
            self.log_message("✅ Configuration loaded successfully")
            
        except FileNotFoundError:
            self.log_message("ℹ️ No config file found, using defaults")
        except Exception as e:
            self.log_message(f"❌ Error loading config: {e}")
            
    def save_config(self):
        """Save configuration to file."""
        try:
            config = {
                'chrome_profile_path': self.chrome_path_var.get(),
                'headless': self.headless_var.get(),
                'typing_speed': {
                    'min': self.typing_min_var.get(),
                    'max': self.typing_max_var.get()
                },
                'human_delays': {
                    'min': self.delay_min_var.get(),
                    'max': self.delay_max_var.get()
                },
                'ollama_enabled': self.ollama_enabled_var.get(),
                'ollama_url': self.ollama_url_var.get(),
                'ollama_model': self.ollama_model_var.get(),
                'timeout': self.timeout_var.get(),
                'retry_attempts': self.retry_var.get()
            }
            
            with open('config.json', 'w') as f:
                json.dump(config, f, indent=4)
                
            self.log_message("✅ Configuration saved successfully")
            messagebox.showinfo("Success", "Configuration saved successfully!")
            
        except Exception as e:
            self.log_message(f"❌ Error saving config: {e}")
            messagebox.showerror("Error", f"Error saving configuration: {e}")
            
    def reset_config(self):
        """Reset configuration to defaults."""
        if messagebox.askyesno("Confirm Reset", "Reset all settings to defaults?"):
            self.chrome_path_var.set('')
            self.headless_var.set(False)
            self.typing_min_var.set(0.01)
            self.typing_max_var.set(0.04)
            self.delay_min_var.set(0.3)
            self.delay_max_var.set(0.8)
            self.ollama_enabled_var.set(True)
            self.ollama_url_var.set('http://localhost:11434')
            self.ollama_model_var.set('codellama')
            self.timeout_var.set(30)
            self.retry_var.set(3)
            
            self.log_message("🔄 Configuration reset to defaults")
            
    def open_browser_step(self):
        """Step 1: Open browser and prepare for navigation."""
        try:
            # Save current config
            self.save_config()
            
            # Create automator instance
            self.automator = SkillRackAutomator("config.json")
            
            self.log_message("🌐 Opening browser...")
            self.update_status("🌐 Opening browser...")
            
            # Setup browser in separate thread to avoid GUI freeze
            browser_thread = threading.Thread(target=self.setup_browser)
            browser_thread.daemon = True
            browser_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Error opening browser: {e}")
            messagebox.showerror("Error", f"Failed to open browser: {e}")
            
    def setup_browser(self):
        """Setup browser in background thread."""
        try:
            self.automator.setup_driver()
            
            # Navigate to SkillRack
            self.automator.driver.get("https://www.skillrack.com/")
            
            # Update UI on main thread
            self.root.after(0, self.browser_ready)
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.log_message(f"❌ Browser setup failed: {error_msg}"))
            self.root.after(0, self.browser_setup_failed)
            
    def browser_ready(self):
        """Called when browser is ready."""
        self.log_message("✅ Browser opened and SkillRack loaded!")
        self.update_status("✅ Ready - Navigate to a challenge page")
        
        # Enable solve button, disable browser button
        self.browser_btn.config(state=tk.DISABLED, text="✅ SkillRack Open")
        self.solve_btn.config(state=tk.NORMAL)
        self.continuous_btn.config(state=tk.NORMAL)

        self.stop_btn.config(state=tk.NORMAL)
        
        # Simple notification in logs instead of popup
        self.log_message("📍 Next: Navigate to a challenge page and click 'Solve Current Challenge'")
        
    def browser_setup_failed(self):
        """Called when browser setup fails."""
        self.log_message("❌ Browser setup failed")
        self.update_status("❌ Browser setup failed")
        
        # Reset browser button
        self.browser_btn.config(state=tk.NORMAL, text="🌐 Step 1: Open Browser & SkillRack")
        
    def solve_current_challenge(self):
        """Step 2: Solve the current challenge (like pressing Enter in CLI)."""
        if not self.automator:
            messagebox.showerror("Error", "Please open browser first!")
            return
            
        try:
            self.log_message("🎯 Starting to solve current challenge...")
            self.update_status("🔄 Solving current challenge...")
            
            # Disable solve button during processing
            self.solve_btn.config(state=tk.DISABLED, text="🔄 Solving...")
            
            # Solve in separate thread
            solve_thread = threading.Thread(target=self.solve_challenge_thread)
            solve_thread.daemon = True
            solve_thread.start()
            
        except Exception as e:
            self.log_message(f"❌ Error starting challenge solve: {e}")
            messagebox.showerror("Error", f"Failed to solve challenge: {e}")
            self.solve_btn.config(state=tk.NORMAL, text="🎯 Step 2: Solve Current Challenge")
            
    def solve_challenge_thread(self):
        """Solve challenge in background thread."""
        try:
            # Update status
            self.root.after(0, lambda: self.log_message("🎯 Solving challenge..."))
            
            # Solve the challenge
            success = self.automator.solve_current_challenge()
            
            # Update UI on main thread
            self.root.after(0, lambda: self.challenge_solved(success))
            
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.challenge_solve_error(error_msg))
            
    def challenge_solved(self, success):
        """Called when challenge solving is complete."""
        if success:
            self.challenges_solved += 1
            self.log_message(f"✅ Challenge #{self.challenges_solved} solved successfully!")
            self.update_status(f"✅ Challenge completed - Total: {self.challenges_solved}")
            self.update_challenges_count()
            
            # Simple completion notification - no popup
            self.log_message("🎯 Ready for next challenge! Navigate to next page and click 'Solve Current Challenge'")
            
        else:
            self.log_message("❌ Challenge solving failed - Check logs for details")
            self.update_status("❌ Challenge failed - Check logs")
        
        # Re-enable solve button
        self.solve_btn.config(state=tk.NORMAL, text="🎯 Step 2: Solve Current Challenge")
        
    def challenge_solve_error(self, error):
        """Called when challenge solving encounters an error."""
        self.log_message(f"❌ Challenge solve error: {error}")
        self.update_status("❌ Error occurred - Check logs for details")
        
        # Just log the error, no popup
        self.solve_btn.config(state=tk.NORMAL, text="🎯 Step 2: Solve Current Challenge")
        
    def start_continuous_mode(self):
        """Start continuous mode for multiple challenges."""
        if not self.automator:
            messagebox.showerror("Error", "Please open browser first!")
            return
            
        confirm = messagebox.askyesno(
            "🔄 Continuous Mode",
            "🔄 Start continuous mode?\n\n" +
            "This will:\n" +
            "• Solve current challenge\n" +
            "• Ask you to navigate to next\n" +
            "• Repeat until you stop\n\n" +
            "Continue?"
        )
        
        if confirm:
            self.is_running = True
            self.continuous_btn.config(state=tk.DISABLED, text="🔄 Running...")
            self.solve_btn.config(state=tk.DISABLED)
            
            # Start continuous mode in thread
            continuous_thread = threading.Thread(target=self.run_continuous_mode)
            continuous_thread.daemon = True
            continuous_thread.start()
            
    def run_continuous_mode(self):
        """Run continuous mode for multiple challenges."""
        challenge_count = 0
        
        while self.is_running:
            try:
                challenge_count += 1
                # Use variables to avoid lambda closure issues
                count = challenge_count
                self.root.after(0, lambda c=count: self.log_message(f"🎯 Continuous Mode - Challenge #{c}"))
                self.root.after(0, lambda c=count: self.update_status(f"🔄 Continuous Mode - Solving Challenge #{c}"))
                
                # Solve current challenge
                success = self.automator.solve_current_challenge()
                
                if success:
                    self.challenges_solved += 1
                    count = challenge_count
                    self.root.after(0, lambda c=count: self.log_message(f"✅ Challenge #{c} solved!"))
                    self.root.after(0, self.update_challenges_count)
                else:
                    count = challenge_count
                    self.root.after(0, lambda c=count: self.log_message(f"❌ Challenge #{c} failed"))
                
                # Simple prompt for next action
                if self.is_running:
                    continue_next = self.ask_continue_next_simple(challenge_count, success)
                    if not continue_next:
                        break
                        
            except Exception as e:
                error_msg = str(e)
                self.root.after(0, lambda err=error_msg: self.log_message(f"❌ Error in continuous mode: {err}"))
                break
        
        # Cleanup continuous mode
        self.root.after(0, self.continuous_mode_ended)
        
    def ask_continue_next_simple(self, challenge_count, success):
        """Simple prompt for next challenge."""
        status_text = "✅ Solved" if success else "❌ Failed"
        
        result = messagebox.askyesno(
            "Continue?",
            f"Challenge #{challenge_count}: {status_text}\n" +
            f"Total solved: {self.challenges_solved}\n\n" +
            "Continue to next challenge?"
        )
        
        if result:
            self.log_message("📍 Navigate to next challenge page")
            return True
        else:
            self.log_message("⏹️ Continuous mode stopped")
            return False
            
    def continuous_mode_ended(self):
        """Called when continuous mode ends."""
        self.is_running = False
        self.continuous_btn.config(state=tk.NORMAL, text="🔄 Continuous Mode")
        self.solve_btn.config(state=tk.NORMAL)
        self.update_status("⏹️ Continuous mode ended")
        self.log_message("🔄 Continuous mode ended")
            
    def run_automation(self):
        """Run the automation process."""
        try:
            # Setup browser
            self.log_message("🌐 Initializing Chrome browser...")
            self.automator.setup_driver()
            
            self.log_message("✅ Browser initialized successfully")
            self.update_status("🌐 Browser ready - Navigate to SkillRack challenge")
            
            # Wait for user to navigate
            self.root.after(0, lambda: messagebox.showinfo(
                "Ready to Start", 
                "Browser opened successfully!\n\n" +
                "1. Navigate to a SkillRack challenge page\n" +
                "2. Click 'Continue' when ready\n" +
                "3. The automation will solve the challenge"
            ))
            
            challenge_count = 0
            
            while self.is_running:
                try:
                    challenge_count += 1
                    self.log_message(f"🎯 Processing Challenge #{challenge_count}")
                    self.update_status(f"🔄 Solving Challenge #{challenge_count}...")
                    
                    # Solve challenge
                    success = self.automator.solve_current_challenge()
                    
                    if success:
                        self.challenges_solved += 1
                        self.log_message(f"✅ Challenge #{challenge_count} solved successfully!")
                        self.update_challenges_count()
                        self.update_status(f"✅ Challenge #{challenge_count} completed")
                    else:
                        self.log_message(f"❌ Challenge #{challenge_count} failed")
                        self.update_status(f"❌ Challenge #{challenge_count} failed")
                    
                    # Ask user for next action
                    if self.is_running:
                        next_action = messagebox.askyesnocancel(
                            "Challenge Complete",
                            f"Challenge #{challenge_count} processed!\n\n" +
                            "Continue with next challenge?\n\n" +
                            "Yes = Continue\n" +
                            "No = Stop automation\n" +
                            "Cancel = Pause"
                        )
                        
                        if next_action is None:  # Cancel (Pause)
                            self.update_status("⏸️ Automation paused")
                            break
                        elif not next_action:  # No (Stop)
                            self.update_status("⏹️ Automation stopped by user")
                            break
                        # Yes continues the loop
                        
                except Exception as e:
                    self.log_message(f"❌ Error in challenge {challenge_count}: {e}")
                    
                    retry = messagebox.askyesno(
                        "Challenge Error",
                        f"Error occurred in challenge {challenge_count}:\n{e}\n\nRetry this challenge?"
                    )
                    
                    if not retry:
                        break
                        
        except Exception as e:
            self.log_message(f"❌ Critical error in automation: {e}")
            self.update_status("❌ Automation failed")
            
        finally:
            self.stop_automation()
            
    def stop_automation(self):
        """Stop all automation processes."""
        self.is_running = False
        
        if self.automator:
            try:
                self.automator.close()
                self.log_message("🌐 Browser closed")
            except:
                pass
            self.automator = None
            
        # Reset UI to initial state
        self.browser_btn.config(state=tk.NORMAL, text="🌐 Step 1: Open Browser & SkillRack")
        self.solve_btn.config(state=tk.DISABLED, text="🎯 Step 2: Solve Current Challenge")
        self.continuous_btn.config(state=tk.DISABLED, text="🔄 Continuous Mode")

        self.stop_btn.config(state=tk.DISABLED)
        
        self.update_status("⏹️ All automation stopped")
        self.log_message("🛑 All automation stopped")
            
    def test_connection(self):
        """Test various connections and configurations."""
        self.log_message("🧪 Testing connections...")
        
        # Test Ollama connection if enabled
        if self.ollama_enabled_var.get():
            try:
                import requests
                response = requests.get(f"{self.ollama_url_var.get()}/api/tags", timeout=5)
                if response.status_code == 200:
                    self.log_message("✅ Ollama connection: SUCCESS")
                else:
                    self.log_message("❌ Ollama connection: FAILED")
            except Exception as e:
                self.log_message(f"❌ Ollama connection error: {e}")
        else:
            self.log_message("ℹ️ Ollama testing skipped (disabled)")
            
        # Test Chrome path
        chrome_path = self.chrome_path_var.get()
        if chrome_path and os.path.exists(chrome_path):
            self.log_message("✅ Chrome profile path: VALID")
        elif chrome_path:
            self.log_message("❌ Chrome profile path: INVALID")
        else:
            self.log_message("ℹ️ Chrome profile path: NOT SET (will use default)")
            
        self.log_message("🧪 Connection test completed")
        
    def clear_logs(self):
        """Clear the log display."""
        self.log_display.delete(1.0, tk.END)
        self.log_message("🗑️ Logs cleared")
        
    def log_message(self, message):
        """Add a message to the log display."""
        timestamp = datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}\n"
        
        self.log_queue.put(formatted_message)
        
    def check_log_queue(self):
        """Check for new log messages and update display."""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_display.insert(tk.END, message)
                self.log_display.see(tk.END)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.check_log_queue)
        
    def update_status(self, status):
        """Update the status label."""
        self.status_label.config(text=status)
        
    def update_challenges_count(self):
        """Update the challenges solved counter."""
        self.challenges_label.config(text=f"Challenges solved: {self.challenges_solved}")
        
        # Update statistics
        self.update_statistics()
        
    def update_statistics(self):
        """Update the statistics display."""
        stats = f"""
Session Statistics:
==================
Challenges Solved: {self.challenges_solved}
Success Rate: 100% (when completed)
Status: {'Running' if self.is_running else 'Stopped'}

Configuration:
=============
AI Enabled: {'Yes' if self.ollama_enabled_var.get() else 'No'}
Typing Speed: {self.typing_min_var.get():.3f}-{self.typing_max_var.get():.3f}s
Headless Mode: {'Yes' if self.headless_var.get() else 'No'}
        """
        
        self.stats_text.config(state=tk.NORMAL)
        self.stats_text.delete(1.0, tk.END)
        self.stats_text.insert(tk.END, stats.strip())
        self.stats_text.config(state=tk.DISABLED)
        
    # AI Chat Methods
    def add_chat_message(self, sender, message):
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if sender == "user":
            self.chat_display.insert(tk.END, f"[{timestamp}] You: ", "user")
        elif sender == "ai":
            self.chat_display.insert(tk.END, f"[{timestamp}] AI: ", "ai")
        else:
            self.chat_display.insert(tk.END, f"[{timestamp}] System: ", "system")
        
        # Add message content
        self.chat_display.insert(tk.END, f"{message}\n\n")
        
        # Scroll to bottom
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
        
        # Store in history
        self.chat_history.append({"sender": sender, "message": message, "timestamp": timestamp})
        
    def scrape_question(self):
        """Scrape the current question from the page."""
        if not self.automator or not self.automator.driver:
            self.add_chat_message("system", "❌ No browser session active. Please open browser first.")
            return
            
        try:
            self.add_chat_message("system", "📄 Scraping question from current page...")
            
            # Extract question text using multiple selectors
            question_selectors = [
                ".ui-card-content",                    # Main content area
                ".problem-statement",                  # Problem statement
                "[class*='problem']",                  # Any element with 'problem' in class
                ".question-content",                   # Question content
                "body"                                 # Fallback to entire body
            ]
            
            question_text = ""
            for selector in question_selectors:
                try:
                    elements = self.automator.driver.find_elements(By.CSS_SELECTOR, selector)
                    if elements:
                        element = elements[0]
                        text = element.text.strip()
                        if text and len(text) > 100:  # Minimum length check
                            question_text = text
                            break
                except Exception as e:
                    continue
            
            if question_text:
                # Clean and format the question
                self.current_question = self.clean_question_text(question_text)
                
                # Update question display
                self.question_display.delete(1.0, tk.END)
                self.question_display.insert(1.0, self.current_question)
                
                # Enable buttons
                self.analyze_btn.config(state=tk.NORMAL)
                self.generate_btn.config(state=tk.NORMAL)
                
                self.add_chat_message("system", f"✅ Question scraped successfully! ({len(self.current_question)} characters)")
                self.add_chat_message("system", "You can now analyze the question or generate a solution.")
                
            else:
                self.add_chat_message("system", "❌ Could not extract question text. Try navigating to a challenge page.")
                
        except Exception as e:
            self.add_chat_message("system", f"❌ Error scraping question: {e}")
            
    def clean_question_text(self, text):
        """Clean and format the scraped question text."""
        import re
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Split into lines and clean
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('×'):  # Remove close buttons
                cleaned_lines.append(line)
        
        # Join and limit length
        cleaned_text = '\n'.join(cleaned_lines)
        
        # Limit to reasonable length
        if len(cleaned_text) > 2000:
            cleaned_text = cleaned_text[:2000] + "... (truncated)"
            
        return cleaned_text
        
    def analyze_question(self):
        """Send question to AI for analysis."""
        if not self.current_question:
            self.add_chat_message("system", "❌ No question available. Please scrape a question first.")
            return
            
        if not self.ollama_enabled_var.get():
            self.add_chat_message("system", "❌ AI is disabled. Please enable Ollama in Configuration tab.")
            return
            
        self.add_chat_message("user", "Please analyze this programming question and explain the approach.")
        
        # Send to AI in background
        threading.Thread(target=self.ai_analyze_thread, daemon=True).start()
        
    def ai_analyze_thread(self):
        """Background thread for AI analysis."""
        try:
            prompt = f"""
Analyze this programming problem and provide a clear explanation:

PROBLEM:
{self.current_question}

Please provide:
1. Problem understanding
2. Input/Output format
3. Approach/Algorithm
4. Key insights
5. Time/Space complexity considerations

Be clear and educational.
"""
            
            response = self.send_to_ollama(prompt)
            if response == "AI_NOT_AVAILABLE":
                self.root.after(0, lambda: self.add_chat_message("system", "❌ AI not found! Please install and configure Ollama with CodeLlama model.\n\n📞 Visit Support for installation instructions."))
            elif response:
                self.root.after(0, lambda: self.add_chat_message("ai", response))
            else:
                self.root.after(0, lambda: self.add_chat_message("system", "❌ AI analysis failed. Check Ollama connection."))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message("system", f"❌ Error in AI analysis: {e}"))
            
    def generate_solution(self):
        """Generate code solution using AI."""
        if not self.current_question:
            self.add_chat_message("system", "❌ No question available. Please scrape a question first.")
            return
            
        if not self.ollama_enabled_var.get():
            self.add_chat_message("system", "❌ AI is disabled. Please enable Ollama in Configuration tab.")
            return
            
        self.add_chat_message("user", "Please generate a complete code solution for this problem.")
        
        # Send to AI in background
        threading.Thread(target=self.ai_generate_thread, daemon=True).start()
        
    def ai_generate_thread(self):
        """Background thread for AI code generation."""
        try:
            prompt = f"""
You are a competitive programming expert. Generate a complete, working solution for this problem:

PROBLEM:
{self.current_question}

REQUIREMENTS:
1. Provide ONLY complete, compilable code
2. Follow the exact input/output format
3. Use efficient algorithms
4. Include necessary headers
5. Use C/C++ language
6. Handle edge cases

Generate the solution now:
"""
            
            response = self.send_to_ollama(prompt)
            if response == "AI_NOT_AVAILABLE":
                self.root.after(0, lambda: self.add_chat_message("system", "❌ AI not found! Please install and configure Ollama with CodeLlama model.\n\n📞 Visit Support for installation instructions."))
            elif response:
                # Extract code from response
                code = self.extract_code_from_response(response)
                if code:
                    self.current_solution = code
                    self.root.after(0, lambda: self.solution_generated(response, code))
                else:
                    self.root.after(0, lambda: self.add_chat_message("ai", response))
            else:
                self.root.after(0, lambda: self.add_chat_message("system", "❌ Code generation failed. Check Ollama connection."))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message("system", f"❌ Error in code generation: {e}"))
            
    def solution_generated(self, full_response, code):
        """Handle successful code generation."""
        self.add_chat_message("ai", full_response)
        
        # Enable inject button
        self.inject_btn.config(state=tk.NORMAL)
        
        self.add_chat_message("system", f"✅ Code solution generated! ({len(code)} characters)\n" +
                             "You can now inject the code or ask for modifications.")
        
    def extract_code_from_response(self, response):
        """Extract clean code from AI response."""
        import re
        
        # Look for code blocks
        code_patterns = [
            r'```(?:c|cpp|c\+\+)?\s*\n(.*?)\n```',  # Markdown code blocks
            r'```\s*\n(.*?)\n```',                    # Plain code blocks
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, response, re.DOTALL)
            if matches:
                return matches[0].strip()
        
        # If no code blocks, look for include statements
        if '#include' in response:
            lines = response.split('\n')
            code_lines = []
            in_code = False
            
            for line in lines:
                if '#include' in line or 'int main' in line:
                    in_code = True
                
                if in_code:
                    code_lines.append(line)
                    
                if in_code and line.strip() == '}' and 'main' in '\n'.join(code_lines[-10:]):
                    break
            
            if code_lines:
                return '\n'.join(code_lines).strip()
        
        return None
        
    def send_message(self):
        """Send user message to AI."""
        user_message = self.user_input.get(1.0, tk.END).strip()
        if not user_message:
            return
            
        if not self.ollama_enabled_var.get():
            self.add_chat_message("system", "❌ AI is disabled. Please enable Ollama in Configuration tab.")
            return
            
        # Clear input
        self.user_input.delete(1.0, tk.END)
        
        # Add user message to chat
        self.add_chat_message("user", user_message)
        
        # Send to AI in background
        threading.Thread(target=self.ai_chat_thread, args=(user_message,), daemon=True).start()
        
    def ai_chat_thread(self, message):
        """Background thread for AI chat."""
        try:
            # Build context with question if available
            context = ""
            if self.current_question:
                context = f"CURRENT PROBLEM:\n{self.current_question}\n\n"
            
            prompt = f"""{context}USER MESSAGE: {message}

Please provide a helpful response. If the user is asking about the problem, refer to the current problem above. 
If they're asking for code modifications, provide clear explanations and updated code if needed."""
            
            response = self.send_to_ollama(prompt)
            if response == "AI_NOT_AVAILABLE":
                self.root.after(0, lambda: self.add_chat_message("system", "❌ AI not found! Please install and configure Ollama with CodeLlama model.\n\n📞 Visit Support for installation instructions."))
            elif response:
                self.root.after(0, lambda: self.add_chat_message("ai", response))
            else:
                self.root.after(0, lambda: self.add_chat_message("system", "❌ AI response failed. Check Ollama connection."))
                
        except Exception as e:
            self.root.after(0, lambda: self.add_chat_message("system", f"❌ Error in AI chat: {e}"))
            
    def send_to_ollama(self, prompt):
        """Send prompt to Ollama and get response."""
        try:
            import requests
            
            # Check if Ollama is available
            try:
                # First, check if Ollama service is running
                health_response = requests.get(f"{self.ollama_url_var.get()}/api/tags", timeout=5)
                if health_response.status_code != 200:
                    raise Exception("Ollama service not responding")
                    
                # Check if the model is available
                models = health_response.json().get('models', [])
                model_names = [model.get('name', '') for model in models]
                
                if not any(self.ollama_model_var.get() in name for name in model_names):
                    raise Exception(f"Model {self.ollama_model_var.get()} not found")
                    
            except Exception as e:
                # Ollama not available - return special error message
                return "AI_NOT_AVAILABLE"
            
            response = requests.post(
                f"{self.ollama_url_var.get()}/api/generate",
                json={
                    "model": self.ollama_model_var.get(),
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get('response', '').strip()
            else:
                return "AI_NOT_AVAILABLE"
                
        except Exception as e:
            return "AI_NOT_AVAILABLE"
            
    def inject_code(self):
        """Inject the generated code into the editor."""
        if not self.current_solution:
            self.add_chat_message("system", "❌ No code solution available. Generate a solution first.")
            return
            
        if not self.automator or not self.automator.driver:
            self.add_chat_message("system", "❌ No browser session active. Please open browser first.")
            return
            
        # Disable inject button during injection
        self.inject_btn.config(state=tk.DISABLED, text="💉 Injecting...")
        
        # Run injection in separate thread
        threading.Thread(target=self.inject_code_thread, daemon=True).start()
        
    def inject_code_thread(self):
        """Background thread for code injection."""
        try:
            self.root.after(0, lambda: self.add_chat_message("system", "💉 Starting code injection..."))
            
            # Clear the editor first
            self.automator.clear_ace_editor_thoroughly()
            
            # Give user time to position cursor
            self.root.after(0, lambda: self.add_chat_message("system", "⏰ Position your cursor in the code editor..."))
            
            # 3-second countdown
            for i in range(3, 0, -1):
                self.root.after(0, lambda count=i: self.add_chat_message("system", f"⏰ Injecting in {count} seconds..."))
                time.sleep(1)
            
            # Type the solution
            success = self.automator.pyautogui_type_solution(self.current_solution)
            
            if success:
                self.root.after(0, lambda: self.add_chat_message("system", "✅ Code injected successfully! You can now test it."))
            else:
                self.root.after(0, lambda: self.add_chat_message("system", "❌ Code injection failed."))
                
        except Exception as e:
            error_msg = str(e)
            self.root.after(0, lambda: self.add_chat_message("system", f"❌ Error injecting code: {error_msg}"))
        finally:
            # Re-enable inject button
            self.root.after(0, lambda: self.inject_btn.config(state=tk.NORMAL, text="💉 Inject Code"))
            

            

            

        
    def run(self):
        """Start the GUI application."""
        # Initialize statistics
        self.update_statistics()
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-Return>', lambda e: self.solve_current_challenge())
        self.root.bind('<F5>', lambda e: self.solve_current_challenge())
        self.root.bind('<Control-q>', lambda e: self.stop_automation())
        
        # Focus the main window
        self.root.focus_set()
        
        # Start the main loop
        self.root.mainloop()


def main():
    """Main function to run the GUI application."""
    try:
        app = SkillRackGUI()
        app.run()
    except KeyboardInterrupt:
        print("Application interrupted by user")
    except Exception as e:
        print(f"Error starting application: {e}")


if __name__ == "__main__":
    main()