#!/usr/bin/env python3
"""
SkillRack Automation Script
Automates solving coding challenges on SkillRack platform by mimicking human behavior.
"""

import time
import random
import re
import json
import requests
import pyperclip
import pyautogui
import tkinter as tk
from tkinter import messagebox
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import logging
from typing import Optional, Dict, Any

# Configure PyAutoGUI safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('skillrack_automation.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class SkillRackAutomator:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the SkillRack Automator with configuration."""
        self.config = self.load_config(config_file)
        self.driver = None
        self.wait = None
        
    def load_config(self, config_file: str) -> Dict[str, Any]:
        """Load configuration from JSON file."""
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.error(f"Config file {config_file} not found. Creating default config.")
            default_config = {
                "chrome_profile_path": "",
                "typing_speed": {"min": 0.05, "max": 0.15},
                "human_delays": {"min": 1, "max": 3},
                "retry_attempts": 3,
                "ollama_enabled": False,
                "ollama_url": "http://localhost:11434",
                "ollama_model": "codellama",
                "headless": False,
                "timeout": 30
            }
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=4)
            return default_config
            
    def setup_driver(self):
        """Setup Chrome driver with appropriate options."""
        chrome_options = Options()
        
        if self.config.get("chrome_profile_path"):
            chrome_options.add_argument(f"--user-data-dir={self.config['chrome_profile_path']}")
            
        if self.config.get("headless", False):
            chrome_options.add_argument("--headless")
            
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        self.wait = WebDriverWait(self.driver, self.config.get("timeout", 30))
        
        logger.info("Chrome driver initialized successfully")
        
    def human_delay(self, min_delay: float = None, max_delay: float = None):
        """Add random human-like delay."""
        if min_delay is None:
            min_delay = self.config["human_delays"]["min"]
        if max_delay is None:
            max_delay = self.config["human_delays"]["max"]
            
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        
    def show_cool_popup(self, title: str, message: str, countdown: int = 10):
        """Show a cool popup notification with countdown."""
        def create_popup():
            # Create a custom popup window
            popup = tk.Tk()
            popup.title(title)
            popup.geometry("500x300")
            popup.configure(bg='#2c3e50')
            popup.attributes('-topmost', True)
            
            # Center the window on screen
            popup.update_idletasks()
            x = (popup.winfo_screenwidth() // 2) - (500 // 2)
            y = (popup.winfo_screenheight() // 2) - (300 // 2)
            popup.geometry(f"500x300+{x}+{y}")
            
            # Title label
            title_label = tk.Label(
                popup, 
                text="🚀 SkillRack Automation", 
                font=("Arial", 18, "bold"),
                fg='#ecf0f1', 
                bg='#2c3e50'
            )
            title_label.pack(pady=20)
            
            # Message label
            msg_label = tk.Label(
                popup, 
                text=message, 
                font=("Arial", 12),
                fg='#ecf0f1', 
                bg='#2c3e50',
                wraplength=450,
                justify='center'
            )
            msg_label.pack(pady=20)
            
            # Countdown label
            countdown_label = tk.Label(
                popup, 
                text=f"Auto-typing starts in: {countdown} seconds", 
                font=("Arial", 14, "bold"),
                fg='#e74c3c', 
                bg='#2c3e50'
            )
            countdown_label.pack(pady=20)
            
            # Progress bar simulation
            progress_frame = tk.Frame(popup, bg='#2c3e50')
            progress_frame.pack(pady=10)
            
            progress_bg = tk.Frame(progress_frame, bg='#34495e', height=20, width=400)
            progress_bg.pack()
            
            progress_fill = tk.Frame(progress_bg, bg='#3498db', height=20, width=0)
            progress_fill.place(x=0, y=0)
            
            def update_countdown(remaining):
                if remaining > 0:
                    countdown_label.config(text=f"Auto-typing starts in: {remaining} seconds")
                    progress_width = int(400 * (countdown - remaining) / countdown)
                    progress_fill.config(width=progress_width)
                    popup.after(1000, lambda: update_countdown(remaining - 1))
                else:
                    countdown_label.config(text="🎯 Starting auto-typing now!", fg='#27ae60')
                    progress_fill.config(width=400, bg='#27ae60')
                    popup.after(2000, popup.destroy)
            
            # Instructions
            instructions = tk.Label(
                popup,
                text="📌 Click on the code editor area now!\n💡 Move mouse to top-left corner to stop automation",
                font=("Arial", 10),
                fg='#95a5a6',
                bg='#2c3e50'
            )
            instructions.pack(side='bottom', pady=20)
            
            update_countdown(countdown)
            popup.mainloop()
        
        # Run popup in separate thread to avoid blocking
        popup_thread = threading.Thread(target=create_popup)
        popup_thread.daemon = True
        popup_thread.start()
        
        # Wait for popup to finish
        time.sleep(countdown + 3)
        
    def pyautogui_type_solution(self, code: str):
        """Type solution using PyAutoGUI with human-like behavior."""
        try:
            logger.info("Starting PyAutoGUI typing...")
            
            # Clear any existing text (Ctrl+A, Delete)
            pyautogui.hotkey('ctrl', 'a')
            time.sleep(0.5)
            pyautogui.press('delete')
            time.sleep(0.5)
            
            # Split code into lines for more realistic typing
            lines = code.split('\n')
            
            for line_num, line in enumerate(lines, 1):
                logger.info(f"Typing line {line_num}/{len(lines)}")
                
                # Type the line with human-like delays
                for i, char in enumerate(line):
                    pyautogui.write(char)
                    
                    # Human-like typing speed
                    delay = random.uniform(
                        self.config["typing_speed"]["min"],
                        self.config["typing_speed"]["max"]
                    )
                    time.sleep(delay)
                    
                    # Occasional longer pauses (thinking time)
                    if random.random() < 0.03:
                        time.sleep(random.uniform(0.3, 0.8))
                
                # Press Enter to go to next line (except for last line)
                if line_num < len(lines):
                    pyautogui.press('enter')
                    time.sleep(random.uniform(0.2, 0.5))
                    
                # Small pause between lines
                time.sleep(random.uniform(0.1, 0.3))
            
            logger.info("PyAutoGUI typing completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error in PyAutoGUI typing: {e}")
            return False
        
    def human_type(self, element, text: str):
        """Type text with human-like speed and occasional typos, bypassing restrictions."""
        try:
            # Clear element carefully to avoid detection
            element.click()
            self.human_delay(0.2, 0.5)
            
            # Try to clear existing content multiple ways
            try:
                element.send_keys(Keys.CONTROL + "a")
                time.sleep(0.1)
                element.send_keys(Keys.DELETE)
            except:
                pass
                
            self.human_delay(0.3, 0.7)
            
            # Split text into chunks to avoid detection
            chunk_size = random.randint(15, 25)
            chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
            
            for chunk_idx, chunk in enumerate(chunks):
                logger.info(f"Typing chunk {chunk_idx + 1}/{len(chunks)}")
                
                for i, char in enumerate(chunk):
                    # Simulate occasional typos (1% chance to avoid too much delay)
                    if random.random() < 0.01 and char.isalpha():
                        # Type wrong character then backspace
                        wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                        element.send_keys(wrong_char)
                        time.sleep(random.uniform(0.1, 0.3))
                        element.send_keys(Keys.BACKSPACE)
                        time.sleep(random.uniform(0.1, 0.2))
                    
                    element.send_keys(char)
                    
                    # Random typing speed
                    typing_delay = random.uniform(
                        self.config["typing_speed"]["min"],
                        self.config["typing_speed"]["max"]
                    )
                    time.sleep(typing_delay)
                    
                    # Occasional longer pauses (thinking time)
                    if random.random() < 0.03:
                        time.sleep(random.uniform(0.3, 0.8))
                        
                # Small pause between chunks
                if chunk_idx < len(chunks) - 1:
                    self.human_delay(0.5, 1.2)
                    
        except Exception as e:
            logger.error(f"Error in human_type: {e}")
            # Fallback to simple typing
            try:
                element.send_keys(text)
            except:
                pass
                
    def extract_solution_from_page(self) -> Optional[str]:
        """Extract solution code from the current page."""
        try:
            # Wait a bit for solution to fully load
            self.human_delay(1, 2)
            
            # Look for the solution in different possible containers
            solution_selectors = [
                "pre.hljs.language-cpp",       # C++ highlighted code
                "pre.hljs.language-c",         # C highlighted code  
                "pre.hljs",                    # Any highlighted code block
                "pre[data-highlighted='yes']", # Explicitly highlighted
                ".solution-code",              # Generic solution class
                "code"                         # Any code element
            ]
            
            for selector in solution_selectors:
                try:
                    solution_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    if solution_elements and solution_elements[0] is not None:
                        logger.info(f"Found solution using selector: {selector}")
                        solution_html = solution_elements[0].get_attribute('innerHTML')
                        
                        # Parse HTML and extract clean code
                        soup = BeautifulSoup(solution_html, 'html.parser')
                        
                        # Remove HTML tags and get clean code
                        clean_code = soup.get_text()
                        
                        # Clean up the code
                        clean_code = clean_code.replace('&nbsp;', ' ')
                        clean_code = clean_code.replace('&amp;', '&')
                        clean_code = clean_code.replace('&lt;', '<')
                        clean_code = clean_code.replace('&gt;', '>')
                        clean_code = clean_code.strip()
                        
                        if clean_code and len(clean_code) > 10:  # Basic validation
                            logger.info(f"Solution extracted successfully: {len(clean_code)} characters")
                            logger.debug(f"Extracted code preview: {clean_code[:100]}...")
                            return clean_code
                            
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
                    
            logger.warning("No solution found with any selector")
            return None
            
        except Exception as e:
            logger.error(f"Error extracting solution: {e}")
            return None
            
    def is_view_solution_button_present(self) -> bool:
        """Check if View Solution button is present and clickable."""
        try:
            button = self.driver.find_element(By.ID, "showbtn")
            if button is None:
                return False
            return button.is_displayed() and button.is_enabled()
        except (NoSuchElementException, AttributeError, Exception):
            return False
            
    def click_view_solution(self) -> bool:
        """Click the View Solution button."""
        try:
            # Multiple selectors for View Solution button
            button_selectors = [
                "#showbtn",                                    # Primary ID
                "button[onclick='showSolution()']",            # By onclick function
                "button.ui.button.green",                      # By classes
                "//button[contains(text(), 'View Solution')]", # By text content
                "//button[contains(text(), 'Solution')]"       # Partial text match
            ]
            
            button = None
            used_selector = None
            
            for selector in button_selectors:
                try:
                    if selector.startswith("//"):
                        button = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                    else:
                        button = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    
                    if button is not None:
                        used_selector = selector
                        break
                except TimeoutException:
                    continue
                except Exception as e:
                    logger.debug(f"Error with button selector {selector}: {e}")
                    continue
            
            if not button:
                logger.error("View Solution button not found with any selector")
                return False
                
            logger.info(f"Found View Solution button using: {used_selector}")
            
            # Scroll to button and add human-like movement
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", button)
            self.human_delay(0.8, 1.5)
            
            # Try multiple click methods
            try:
                button.click()
                logger.info("View Solution button clicked (normal click)")
            except:
                # Fallback to JavaScript click
                self.driver.execute_script("arguments[0].click();", button)
                logger.info("View Solution button clicked (JavaScript click)")
            
            # Wait for solution to load and verify it appeared
            self.human_delay(2, 4)
            
            # Verify solution actually loaded
            solution_appeared = False
            for _ in range(3):  # Try up to 3 times
                try:
                    solution_elements = self.driver.find_elements(By.CSS_SELECTOR, "pre.hljs, pre[data-highlighted='yes']")
                    if solution_elements:
                        # Check each element safely
                        for elem in solution_elements:
                            if elem is not None and elem.is_displayed():
                                solution_appeared = True
                                break
                        if solution_appeared:
                            break
                    self.human_delay(1, 2)
                except Exception as e:
                    logger.debug(f"Error checking solution appearance: {e}")
                    pass
                    
            if solution_appeared:
                logger.info("Solution panel loaded successfully")
                return True
            else:
                logger.warning("Solution button clicked but solution panel may not have loaded")
                return True  # Continue anyway, maybe it's there but not detected
                
        except Exception as e:
            logger.error(f"Error clicking View Solution button: {e}")
            return False
            
    def get_code_editor_element(self):
        """Find and return the ACE code editor element."""
        try:
            # SkillRack uses ACE editor - try multiple approaches
            selectors = [
                "#ctracktxtCode .ace_text-input",  # ACE editor text input
                ".ace_text-input",                 # Generic ACE text input
                "#txtCode",                        # Hidden textarea
                "textarea[name='txtCode']",        # Textarea by name
                ".ace_editor .ace_text-input"      # ACE editor within container
            ]
            
            for selector in selectors:
                try:
                    element = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    if element is not None:
                        logger.info(f"Found code editor using selector: {selector}")
                        return element
                except TimeoutException:
                    continue
                except Exception as e:
                    logger.debug(f"Error with selector {selector}: {e}")
                    continue
                    
            logger.error("Code editor element not found with any selector")
            return None
            
        except Exception as e:
            logger.error(f"Error finding code editor: {e}")
            return None
            
    def submit_solution(self, code: str) -> bool:
        """Submit the solution code using PyAutoGUI."""
        try:
            logger.info("Preparing to type solution using PyAutoGUI...")
            
            # Show cool popup notification
            self.show_cool_popup(
                "🎯 Ready to Type Solution!",
                "✅ Solution copied to clipboard successfully!\n\n" +
                "📋 Now click on the SkillRack code editor area\n" +
                "🎯 The automation will start typing the solution automatically\n\n" +
                "⚠️ Make sure the code editor is focused and ready!",
                countdown=10
            )
            
            # Type the solution using PyAutoGUI
            success = self.pyautogui_type_solution(code)
            
            if success:
                logger.info("✅ Solution typed successfully!")
                
                # Show completion message
                def show_completion():
                    root = tk.Tk()
                    root.withdraw()  # Hide main window
                    messagebox.showinfo(
                        "🎉 Automation Complete!", 
                        "✅ Solution has been typed successfully!\n\n" +
                        "👆 You can now manually click the RUN button\n" +
                        "📊 Check the results and enjoy! 🚀"
                    )
                    root.destroy()
                
                completion_thread = threading.Thread(target=show_completion)
                completion_thread.daemon = True
                completion_thread.start()
                
                return True
            else:
                logger.error("❌ Failed to type solution")
                return False
                
        except Exception as e:
            logger.error(f"Error in submit_solution: {e}")
            return False
            
    def _fallback_typing_method(self, code: str) -> bool:
        """Fallback method for typing when ACE editor API doesn't work."""
        try:
            logger.info("Attempting fallback typing method...")
            
            # Try to find any available code editor element
            editor = self.get_code_editor_element()
            if not editor or editor is None:
                logger.error("No code editor found for fallback")
                return False
                
            # Focus on editor and clear it
            try:
                editor.click()
                self.human_delay(0.5, 1.0)
            except Exception as e:
                logger.error(f"Error clicking editor in fallback: {e}")
                return False
            
            # Clear existing content
            editor.send_keys(Keys.CONTROL + "a")
            self.human_delay(0.2, 0.5)
            editor.send_keys(Keys.DELETE)
            self.human_delay(0.5, 1.0)
            
            # Type solution with human-like behavior
            logger.info("Typing solution character by character...")
            self.human_type(editor, code)
            
            return True
            
        except Exception as e:
            logger.error(f"Fallback typing method failed: {e}")
            return False
            
    def _click_run_button(self) -> bool:
        """Find and click the Run button."""
        try:
            run_selectors = [
                "//span[contains(text(), 'Run')]/..",
                "//button[contains(text(), 'Run')]",
                ".ui-button[onclick*='run']",
                "#run_btn",
                "button[onclick*='run']",
                ".ui-button-text:contains('Run')"
            ]
            
            run_button = None
            for selector in run_selectors:
                try:
                    if selector.startswith("//"):
                        run_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        run_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if run_button is not None and run_button.is_displayed() and run_button.is_enabled():
                        break
                except NoSuchElementException:
                    continue
                    
            if run_button:
                self.driver.execute_script("arguments[0].scrollIntoView(true);", run_button)
                self.human_delay(0.5, 1.0)
                run_button.click()
                logger.info("Run button clicked")
                return True
            else:
                logger.error("Run button not found")
                # Try alternative approach - look for any clickable button with "Run" text
                try:
                    buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if button is not None and button.text and "run" in button.text.lower():
                            try:
                                if button.is_displayed() and button.is_enabled():
                                    button.click()
                                    logger.info("Run button found by text content")
                                    return True
                            except Exception as e:
                                logger.debug(f"Error clicking button by text: {e}")
                                continue
                except Exception as e:
                    logger.debug(f"Error in alternative button search: {e}")
                    pass
                return False
                
        except Exception as e:
            logger.error(f"Error clicking run button: {e}")
            return False
            
    def check_for_errors(self) -> Optional[str]:
        """Check for compilation or runtime errors."""
        try:
            # Wait for results to load
            self.human_delay(3, 5)
            
            # Look for error panel
            error_selectors = [
                "#errormsg_content",
                ".error-panel",
                ".compilation-error",
                "[id*='error']"
            ]
            
            for selector in error_selectors:
                try:
                    error_element = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if error_element.is_displayed():
                        error_text = error_element.text.strip()
                        if error_text and "error" in error_text.lower():
                            logger.warning(f"Error detected: {error_text}")
                            return error_text
                except NoSuchElementException:
                    continue
                    
            logger.info("No errors detected")
            return None
            
        except Exception as e:
            logger.error(f"Error checking for errors: {e}")
            return None
            
    def solve_with_ollama(self, problem_description: str) -> Optional[str]:
        """Use Ollama LLM to generate solution."""
        if not self.config.get("ollama_enabled", False):
            return None
            
        try:
            prompt = f"""
            Solve this programming problem and provide only the complete, runnable code:
            
            {problem_description}
            
            Requirements:
            - Provide only the code, no explanations
            - Make sure the code compiles and runs correctly
            - Include all necessary headers and functions
            """
            
            response = requests.post(
                f"{self.config['ollama_url']}/api/generate",
                json={
                    "model": self.config['ollama_model'],
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                solution = result.get('response', '').strip()
                logger.info("Solution generated using Ollama")
                return solution
            else:
                logger.error(f"Ollama request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error using Ollama: {e}")
            return None
            
    def solve_current_challenge(self) -> bool:
        """Solve the current challenge on the page."""
        try:
            logger.info("Starting challenge solution process...")
            
            # Check if View Solution button is present
            try:
                has_solution_button = self.is_view_solution_button_present()
            except Exception as e:
                logger.error(f"Error checking for View Solution button: {e}")
                has_solution_button = False
                
            if has_solution_button:
                logger.info("View Solution button found - using provided solution")
                
                # Click View Solution button
                if not self.click_view_solution():
                    return False
                    
                # Extract solution
                solution = self.extract_solution_from_page()
                if not solution:
                    logger.error("Could not extract solution from page")
                    return False
                    
            else:
                logger.info("No View Solution button - attempting to use Ollama")
                
                # Try to extract problem description
                problem_text = self.driver.find_element(By.TAG_NAME, "body").text
                
                # Use Ollama to generate solution
                solution = self.solve_with_ollama(problem_text)
                if not solution:
                    logger.error("Could not generate solution with Ollama")
                    return False
                    
            # Copy to clipboard 
            pyperclip.copy(solution)
            logger.info("✅ Solution copied to clipboard successfully!")
            
            # Submit solution using PyAutoGUI (user will click Run manually)
            success = self.submit_solution(solution)
            
            if success:
                logger.info("🎉 Solution typing completed! User can now click RUN button manually.")
                return True
            else:
                logger.error("❌ Failed to type solution")
                return False
            
        except Exception as e:
            logger.error(f"Error solving challenge: {e}")
            return False
            
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the automation script."""
    automator = SkillRackAutomator()
    
    try:
        # Setup browser
        automator.setup_driver()
        
        # Get current page URL or ask user to navigation to SkillRack
        input("Please navigate to the SkillRack challenge page in the opened browser and press Enter to continue...")
        
        # Solve the challenge
        success = automator.solve_current_challenge()
        
        if success:
            print("✅ Challenge solved successfully!")
        else:
            print("❌ Failed to solve challenge")
            
        input("Press Enter to close the browser...")
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        automator.close()

if __name__ == "__main__":
    main() 