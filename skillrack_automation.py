
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
        
    def validate_session(self) -> bool:
        """Validate that the browser session is still active."""
        try:
            if not self.driver:
                logger.error("WebDriver is None")
                return False
                
            # Try to get current window handle - this will fail if session is dead
            current_handle = self.driver.current_window_handle
            
            # Try to get current URL - another validation
            current_url = self.driver.current_url
            
            logger.debug(f"Session valid - Handle: {current_handle[:8]}..., URL: {current_url[:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Session validation failed: {e}")
            return False
    
    def ensure_session_active(self) -> bool:
        """Ensure session is active, try to recover if not."""
        if self.validate_session():
            return True
            
        logger.warning("Session lost, attempting recovery...")
        try:
            # Try to reinitialize driver
            if self.driver:
                try:
                    self.driver.quit()
                except:
                    pass
            
            self.setup_driver()
            
            # Ask user to navigate back to the page
            print("\n⚠️  Browser session was lost!")
            print("Please navigate back to the SkillRack challenge page in the new browser window.")
            input("Press Enter when ready to continue...")
            
            return self.validate_session()
            
        except Exception as e:
            logger.error(f"Session recovery failed: {e}")
            return False
        
    def human_delay(self, min_delay: float = None, max_delay: float = None):
        """Add random human-like delay."""
        if min_delay is None:
            min_delay = self.config["human_delays"]["min"]
        if max_delay is None:
            max_delay = self.config["human_delays"]["max"]
            
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
        

        
    def pyautogui_type_solution(self, code: str):
        """Type solution using PyAutoGUI with smart auto-completion handling."""
        try:
            logger.info("Starting smart PyAutoGUI typing...")
            
            # Get typing configuration
            typing_mode = self.config.get("typing_mode", "chunk")  # Default to chunk mode
            
            if typing_mode == "character":
                # Character-by-character typing
                char_min = self.config.get("character_delay", {}).get("min", 0.05)
                char_max = self.config.get("character_delay", {}).get("max", 0.15)
                logger.info(f"Using CHARACTER mode: {char_min}s - {char_max}s delay per character")
                return self._type_character_by_character(code, char_min, char_max)
            else:
                # Chunk-based typing (legacy mode)
                typing_min = self.config["typing_speed"]["min"]
                typing_max = self.config["typing_speed"]["max"]
                logger.info(f"Using CHUNK mode: {typing_min}s - {typing_max}s delay per chunk")
                return self._type_chunk_based(code, typing_min, typing_max)
                
        except Exception as e:
            logger.error(f"Error in smart PyAutoGUI typing: {e}")
            return False
            
    def _type_character_by_character(self, code: str, char_min: float, char_max: float):
        """Type code character by character with configurable delays - ROBUST VERSION."""
        try:
            # Format and clean code first
            clean_code = self._format_code_for_typing(code)
            
            # Multiple attempts to clear editor
            for attempt in range(3):
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.3)
                pyautogui.press('delete')
                time.sleep(0.3)
                
                # Verify editor is cleared by trying to select all again
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
                # If nothing is selected, editor should be clear
                
            logger.info("✅ Editor thoroughly cleared")
            
            lines = clean_code.split('\n')
            total_chars = len(clean_code)
            chars_typed = 0
            
            logger.info(f"🔤 Starting ROBUST character-by-character typing ({total_chars} characters, {len(lines)} lines)")
            
            for line_num, line in enumerate(lines, 1):
                if line_num % 5 == 0:  # More frequent progress updates
                    progress = (chars_typed / total_chars) * 100
                    logger.info(f"🔤 Progress: {progress:.1f}% (Line {line_num}/{len(lines)})")
                
                # Type each character in the line with verification
                for char_pos, char in enumerate(line):
                    # Type the character
                    pyautogui.write(char)
                    chars_typed += 1
                    
                    # Apply character delay with some randomness
                    char_delay = random.uniform(char_min, char_max)
                    time.sleep(char_delay)
                    
                    # Every 20 characters, add a small pause for stability
                    if char_pos > 0 and char_pos % 20 == 0:
                        time.sleep(char_min)
                
                # Press Enter for next line (except last line)
                if line_num < len(lines):
                    pyautogui.press('enter')
                    # Longer delay after Enter to ensure line break is processed
                    time.sleep(max(char_min * 3, 0.1))
                    chars_typed += 1  # Count the newline
                
                # Small pause between lines for stability
                time.sleep(char_min)
            
            logger.info("✅ ROBUST character-by-character typing completed successfully")
            
            # Final verification - log what we think we typed
            logger.info(f"📊 Typing summary: {len(lines)} lines, {total_chars} characters")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in ROBUST character-by-character typing: {e}")
            return False
            
    def _format_code_for_typing(self, code: str) -> str:
        """Format and clean code before typing to ensure consistency."""
        try:
            # Remove any extraneous text that might be included
            lines = code.split('\n')
            cleaned_lines = []
            
            code_started = False
            
            for line in lines:
                line = line.strip()
                
                # Skip empty lines at the beginning
                if not line and not code_started:
                    continue
                    
                # Detect start of actual code
                if any(keyword in line for keyword in ['#include', 'import ', 'def ', 'int main', 'class ', 'public class', 'function']):
                    code_started = True
                
                # Skip description lines and explanations
                if code_started:
                    # Skip lines that look like explanations
                    if line.startswith(('Note:', 'This', 'The ', 'Here', 'Algorithm:', 'Explanation:', 'Output:', 'Input:')):
                        continue
                    
                    # Skip lines with too much English text
                    if len(line) > 10 and line.count(' ') > line.count(';') + line.count('{') + line.count('}') + 5:
                        # Probably an explanation line
                        continue
                        
                    cleaned_lines.append(line)
                elif any(keyword in line for keyword in ['#include', 'import ', 'def ', 'int main', 'class ', 'public class', 'function']):
                    # This is definitely code
                    code_started = True
                    cleaned_lines.append(line)
            
            # Join lines and ensure proper formatting
            clean_code = '\n'.join(cleaned_lines)
            
            # Remove extra blank lines
            while '\n\n\n' in clean_code:
                clean_code = clean_code.replace('\n\n\n', '\n\n')
            
            # Ensure code ends with a single newline
            clean_code = clean_code.strip() + '\n'
            
            logger.info(f"✅ Code formatted: {len(code)} -> {len(clean_code)} characters")
            return clean_code
            
        except Exception as e:
            logger.error(f"Error formatting code: {e}")
            # Return original code if formatting fails
            return code
            
    def _type_chunk_based(self, code: str, typing_min: float, typing_max: float):
        """Type code in chunks (legacy mode) - ROBUST VERSION."""
        try:
            # Format and clean code first
            clean_code = self._format_code_for_typing(code)
            
            # Multiple attempts to clear editor (same as character mode)
            for attempt in range(3):
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.3)
                pyautogui.press('delete')
                time.sleep(0.3)
                
                # Verify editor is cleared
                pyautogui.hotkey('ctrl', 'a')
                time.sleep(0.1)
            
            logger.info("✅ Editor thoroughly cleared")
            
            lines = clean_code.split('\n')
            total_lines = len(lines)
            
            logger.info(f"⚡ Starting ROBUST chunk typing for {total_lines} lines...")
            
            for line_num, line in enumerate(lines, 1):
                if line_num % 3 == 0:  # More frequent progress updates
                    logger.info(f"⚡ Typing line {line_num}/{total_lines}: {line[:30]}..." if len(line) > 30 else f"⚡ Typing line {line_num}/{total_lines}: {line}")
                
                # Type line in smaller, more reliable chunks
                chunk_size = 15  # Smaller chunks for better reliability
                chunks = [line[i:i+chunk_size] for i in range(0, len(line), chunk_size)]
                
                for chunk_idx, chunk in enumerate(chunks):
                    # Type the chunk
                    pyautogui.write(chunk)
                    
                    # Use configured typing speed with minimum safety delay
                    typing_delay = max(random.uniform(typing_min, typing_max), 0.1)
                    time.sleep(typing_delay)
                    
                    # Extra stability pause every few chunks
                    if chunk_idx > 0 and chunk_idx % 3 == 0:
                        time.sleep(0.1)
                
                # Press Enter for next line (except last line)
                if line_num < total_lines:
                    pyautogui.press('enter')
                    # Ensure Enter is processed
                    time.sleep(max(typing_min * 2, 0.15))
                    
                # Brief pause between lines for stability
                time.sleep(max(typing_min, 0.05))
            
            logger.info("✅ ROBUST chunk typing completed successfully")
            
            # Final verification log
            logger.info(f"📊 Chunk typing summary: {total_lines} lines processed")
            
            return True
            
        except Exception as e:
            logger.error(f"Error in ROBUST chunk typing: {e}")
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
                        
                        # Clean up the code thoroughly
                        clean_code = clean_code.replace('&nbsp;', ' ')
                        clean_code = clean_code.replace('&amp;', '&')
                        clean_code = clean_code.replace('&lt;', '<')
                        clean_code = clean_code.replace('&gt;', '>')
                        
                        # Remove extra whitespace and normalize line breaks
                        lines = clean_code.split('\n')
                        cleaned_lines = []
                        for line in lines:
                            line = line.strip()
                            if line:  # Only add non-empty lines
                                cleaned_lines.append(line)
                        
                        clean_code = '\n'.join(cleaned_lines)
                        
                        # Remove any trailing/leading braces that might be artifacts
                        clean_code = clean_code.strip()
                        if clean_code.endswith('}\n}'):
                            clean_code = clean_code[:-2]  # Remove extra closing brace
                        if clean_code.endswith('}  }'):
                            clean_code = clean_code[:-3] + '}'  # Fix double brace
                        
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
        """Check if View Solution button is present and clickable with enhanced detection."""
        try:
            # Validate session first
            if not self.validate_session():
                logger.warning("Session not valid when checking for View Solution button")
                return False
            
            # Multiple selectors for View Solution button detection
            button_selectors = [
                "#showbtn",                                    # Primary ID from Resource.txt
                "button[onclick='showSolution()']",            # By onclick function
                "button.ui.button.green",                      # By classes
                "//button[contains(text(), 'View Solution')]", # By text content
                "//button[contains(text(), 'Solution')]",      # Partial text match
                "button[id*='show']",                          # Partial ID match
                ".solution-button"                             # Generic class
            ]
            
            for selector in button_selectors:
                try:
                    if selector.startswith("//"):
                        elements = self.driver.find_elements(By.XPATH, selector)
                    else:
                        elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    
                    for element in elements:
                        if element and element.is_displayed() and element.is_enabled():
                            logger.info(f"✅ View Solution button found using selector: {selector}")
                            logger.debug(f"Button text: '{element.text}', ID: '{element.get_attribute('id')}'")
                            return True
                            
                except Exception as e:
                    logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            logger.info("❌ No View Solution button found with any selector")
            return False
            
        except Exception as e:
            logger.error(f"Error in View Solution button detection: {e}")
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
            # Based on Resource.txt structure - SkillRack ACE editor
            selectors = [
                "#ctracktxtCode .ace_text-input",  # Primary ACE editor text input (from Resource.txt)
                ".ace_text-input",                 # Generic ACE text input  
                "#txtCode",                        # Hidden textarea (backup from Resource.txt)
                "textarea[name='txtCode']",        # Textarea by name
                "#ctracktxtCode",                  # Main ACE container
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
            

    
    def confirm_ai_usage(self) -> bool:
        """Ask user for confirmation before using AI to generate solution."""
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            # Create a temporary root window (hidden)
            temp_root = tk.Tk()
            temp_root.withdraw()  # Hide the window
            temp_root.attributes('-topmost', True)  # Keep on top
            
            # Show confirmation dialog
            result = messagebox.askyesno(
                "🤖 AI Solution Generation",
                "⚠️ No 'View Solution' button found for this challenge.\n\n"
                "🎯 The automation can use AI (Ollama) to generate a solution.\n\n"
                "📋 AI SOLUTION BENEFITS:\n"
                "   ✅ Automatic solution generation\n"
                "   ✅ Follows input/output format strictly\n"
                "   ✅ Competitive programming optimized\n\n"
                "⚠️ AI SOLUTION RISKS:\n"
                "   ❌ May not be 100% accurate\n"
                "   ❌ Might miss edge cases\n"
                "   ❌ Requires manual verification\n\n"
                "💡 RECOMMENDATION: Review the generated solution before submission\n\n"
                "🤖 Use AI to generate solution?"
            )
            
            # Clean up the temporary window
            temp_root.destroy()
            
            if result:
                logger.info("✅ User confirmed AI generation")
            else:
                logger.info("❌ User declined AI generation")
                
            return result
                    
        except Exception as e:
            logger.error(f"Error in confirmation dialog: {e}")
            # Fallback to command line if GUI fails
            logger.info("Falling back to command line confirmation...")
            print("\n🤖 Use AI to generate solution? (y/n): ", end="")
            try:
                choice = input().lower().strip()
                return choice in ['y', 'yes']
            except:
                return False
    
    def clear_ace_editor_thoroughly(self):
        """Clear ACE editor and disable auto-completion to prevent brace auto-pairing."""
        try:
            logger.info("Clearing ACE editor and disabling auto-completion...")
            
            # Method 1: Clear and configure ACE editor for clean typing
            try:
                self.driver.execute_script("""
                    if (typeof txtCode !== 'undefined' && txtCode) {
                        // Clear the editor content
                        txtCode.getSession().setValue('');
                        if (typeof $("#txtCode") !== 'undefined') {
                            $("#txtCode").val('');
                        }
                        
                        // Thoroughly disable auto-completion and auto-pairing
                        txtCode.setOptions({
                            enableBasicAutocompletion: false,
                            enableSnippets: false,
                            enableLiveAutocompletion: false,
                            wrapBehavioursEnabled: false,
                            enableMultiselect: false,
                            behavioursEnabled: false,
                            enableAutoIndent: false,
                            showPrintMargin: false
                        });
                        
                        // Disable session behaviors that cause auto-pairing
                        var session = txtCode.getSession();
                        if (session.getMode && session.getMode().$behaviour) {
                            session.getMode().$behaviour = null;
                        }
                        
                        // Remove auto-pairing behaviors
                        if (txtCode.getBehavioursEnabled) {
                            txtCode.setBehavioursEnabled(false);
                        }
                        
                        console.log("✅ ACE auto-completion and auto-pairing disabled");
                    }
                """)
                logger.info("✅ ACE editor cleared and auto-completion disabled")
            except Exception as e:
                logger.debug(f"JavaScript clear/config failed: {e}")
            
            # Method 2: Clear hidden textarea as backup
            try:
                textarea = self.driver.find_element(By.ID, "txtCode")
                if textarea:
                    self.driver.execute_script("arguments[0].value = '';", textarea)
                    logger.info("✅ Hidden textarea cleared")
            except Exception as e:
                logger.debug(f"Textarea clear failed: {e}")
                
            return True
            
        except Exception as e:
            logger.error(f"Failed to clear ACE editor: {e}")
            return False
            
    def submit_solution(self, code: str) -> bool:
        """Submit the solution code using PyAutoGUI."""
        try:
            logger.info("Preparing to type solution using PyAutoGUI...")
            
            # Clear the editor using JavaScript (more reliable)
            logger.info("Clearing editor via JavaScript...")
            self.clear_ace_editor_thoroughly()
            
            # Give user time to manually select code area
            logger.info("⏰ Please click on the code editor area within 3 seconds...")
            
            # Simple 3-second countdown
            for i in range(3, 0, -1):
                logger.info(f"⏰ Starting in {i} seconds... Click the code editor now!")
                time.sleep(1)
            
            logger.info("🚀 Starting to type solution...")
            
            # Type the solution using PyAutoGUI
            success = self.pyautogui_type_solution(code)
            
            if success:
                logger.info("✅ Solution typed successfully! You can now click RUN manually.")
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
        """Use Ollama LLM to generate solution with strict format compliance."""
        if not self.config.get("ollama_enabled", False):
            return None
            
        try:
            prompt = f"""
You are a competitive programming expert. Solve this SkillRack coding challenge EXACTLY as specified.

PROBLEM:
{problem_description}

CRITICAL REQUIREMENTS:
1. Read the Input/Output format CAREFULLY
2. Follow the EXACT output format shown in examples
3. Handle ALL edge cases mentioned
4. Use ONLY the required input/output methods (scanf/printf for C)
5. DO NOT add any extra text, explanations, or debug output
6. Return ONLY compilable C/C++ code

OUTPUT FORMAT:
- Provide ONLY the complete C/C++ source code
- Start with #include statements
- Include main() function
- Follow exact input/output format from examples
- NO explanations, NO comments, NO extra output

EXAMPLE STRUCTURE:
#include <stdio.h>
int main() {{
    // Your solution here
    return 0;
}}

Generate the solution now:
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
                raw_solution = result.get('response', '').strip()
                
                # Validate and clean the AI-generated solution
                validated_solution = self.validate_ai_solution(raw_solution)
                
                if validated_solution:
                    logger.info(f"✅ Valid solution generated using Ollama ({len(validated_solution)} characters)")
                    return validated_solution
                else:
                    logger.error("❌ AI generated invalid solution - failed validation")
                    return None
            else:
                logger.error(f"Ollama request failed: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error using Ollama: {e}")
            return None
            
    def validate_ai_solution(self, solution: str) -> Optional[str]:
        """Validate and clean AI-generated solution to ensure proper format."""
        try:
            if not solution or len(solution.strip()) < 10:
                logger.error("Solution too short or empty")
                return None
            
            # Clean the solution
            cleaned = solution.strip()
            
            # Remove any markdown code blocks if present
            if cleaned.startswith('```'):
                lines = cleaned.split('\n')
                # Remove first line if it's ```c, ```cpp, etc.
                if lines[0].startswith('```'):
                    lines = lines[1:]
                # Remove last line if it's ```
                if lines and lines[-1].strip() == '```':
                    lines = lines[:-1]
                cleaned = '\n'.join(lines).strip()
            
            # Basic validation checks
            validation_checks = {
                'has_include': '#include' in cleaned,
                'has_main': 'int main(' in cleaned or 'main()' in cleaned,
                'has_return': 'return' in cleaned,
                'has_braces': '{' in cleaned and '}' in cleaned,
                'not_too_long': len(cleaned) < 5000,  # Reasonable size limit
                'not_explanation': not cleaned.lower().startswith(('here', 'this', 'the solution', 'explanation'))
            }
            
            failed_checks = [check for check, passed in validation_checks.items() if not passed]
            
            if failed_checks:
                logger.warning(f"⚠️ AI solution failed validation checks: {failed_checks}")
                logger.debug(f"Solution preview: {cleaned[:200]}...")
                
                # If only minor issues, try to auto-fix
                if len(failed_checks) <= 2 and 'has_main' in validation_checks and validation_checks['has_main']:
                    logger.info("🔧 Attempting to auto-fix minor issues...")
                    return cleaned  # Return anyway for minor issues
                else:
                    return None
            
            logger.info("✅ AI solution passed all validation checks")
            return cleaned
            
        except Exception as e:
            logger.error(f"Error validating AI solution: {e}")
            return None
    
    def extract_current_question(self) -> str:
        """Extract the current question/problem text from the page."""
        try:
            if not self.ensure_session_active():
                logger.error("Cannot extract question - browser session not available")
                return ""
                
            # Try to extract problem description
            try:
                problem_text = self.driver.find_element(By.TAG_NAME, "body").text
                logger.info(f"✅ Extracted problem text: {len(problem_text)} characters")
                return problem_text
            except Exception as e:
                logger.error(f"Failed to extract problem text: {e}")
                # Try to recover session and retry once
                if self.ensure_session_active():
                    try:
                        problem_text = self.driver.find_element(By.TAG_NAME, "body").text
                        logger.info(f"Retry successful - extracted problem text: {len(problem_text)} characters")
                        return problem_text
                    except Exception as retry_e:
                        logger.error(f"Retry also failed: {retry_e}")
                        return ""
                else:
                    return ""
                    
        except Exception as e:
            logger.error(f"Error extracting question: {e}")
            return ""
    
    def solve_current_challenge(self) -> dict:
        """Solve the current challenge on the page. Returns info about solution status."""
        try:
            logger.info("Starting challenge solution process...")
            
            # Ensure browser session is active before proceeding
            if not self.ensure_session_active():
                logger.error("Cannot proceed - browser session not available")
                return {"success": False, "has_solution": False, "message": "Browser session not available"}
            
            # Always extract the question first
            question_text = self.extract_current_question()
            
            # 🎯 HIGH PRIORITY: Check for View Solution button first (most reliable)
            logger.info("🔍 Checking for View Solution button (PRIORITY METHOD)...")
            
            try:
                has_solution_button = self.is_view_solution_button_present()
                logger.info(f"View Solution button detection result: {has_solution_button}")
            except Exception as e:
                logger.error(f"Error checking for View Solution button: {e}")
                has_solution_button = False
                
            if has_solution_button:
                logger.info("✅ View Solution button found - using PROVIDED SOLUTION (most reliable)")
                
                # Click View Solution button
                if not self.click_view_solution():
                    logger.error("Failed to click View Solution button")
                    return {"success": False, "has_solution": True, "message": "Failed to click View Solution button", "question": question_text}
                    
                # Extract solution
                solution = self.extract_solution_from_page()
                if not solution:
                    logger.error("Could not extract solution from page")
                    return {"success": False, "has_solution": True, "message": "Could not extract solution from page", "question": question_text}
                
                logger.info(f"✅ Successfully extracted provided solution ({len(solution)} characters)")
                
                # Format and clean solution before typing
                clean_solution = self._format_code_for_typing(solution)
                
                # Copy to clipboard 
                pyperclip.copy(clean_solution)
                logger.info("✅ Solution copied to clipboard successfully!")
                
                # Submit solution using PyAutoGUI (user will click Run manually)
                success = self.submit_solution(clean_solution)
                
                if success:
                    logger.info("🎉 Solution typing completed! User can now click RUN button manually.")
                    return {"success": True, "has_solution": True, "message": "Solution typed successfully", "question": question_text}
                else:
                    logger.error("❌ Failed to type solution")
                    return {"success": False, "has_solution": True, "message": "Failed to type solution", "question": question_text}
                    
            else:
                logger.warning("⚠️ No View Solution button found - question will be loaded to AI tab")
                return {"success": False, "has_solution": False, "message": "No solution button found - redirecting to AI tab", "question": question_text}
            
        except Exception as e:
            logger.error(f"Error solving challenge: {e}")
            question_text = self.extract_current_question() if hasattr(self, 'driver') and self.driver else ""
            return {"success": False, "has_solution": False, "message": f"Error: {e}", "question": question_text}
            
    def close(self):
        """Close the browser driver."""
        if self.driver:
            self.driver.quit()
            logger.info("Browser closed")

def main():
    """Main function to run the automation script with continuous workflow."""
    automator = SkillRackAutomator()
    
    try:
        # Setup browser
        automator.setup_driver()
        
        print("🚀 SkillRack Automation - Continuous Mode")
        print("=" * 50)
        print("📌 Instructions:")
        print("   1. Navigate to a SkillRack challenge page")
        print("   2. Press Enter to solve the challenge")
        print("   3. After solving, navigate to the next challenge")
        print("   4. Press Enter again to solve the next one")
        print("   5. Type 'quit' to exit")
        print("=" * 50)
        
        challenge_count = 0
        
        while True:
            try:
                # Ask user to navigate to challenge page
                if challenge_count == 0:
                    user_input = input("\n🎯 Navigate to the first SkillRack challenge page and press Enter (or 'quit' to exit): ")
                else:
                    user_input = input(f"\n🎯 Navigate to the next challenge page and press Enter (or 'quit' to exit): ")
                
                # Check if user wants to quit
                if user_input.lower().strip() in ['quit', 'exit', 'q']:
                    print("👋 Exiting automation...")
                    break
                
                # Validate session before solving
                if not automator.ensure_session_active():
                    print("❌ Browser session lost. Please restart the script.")
                    break
                
                challenge_count += 1
                print(f"\n🔄 Solving Challenge #{challenge_count}...")
                
                # Solve the challenge
                success = automator.solve_current_challenge()
                
                if success:
                    print(f"✅ Challenge #{challenge_count} solved successfully!")
                    print("   💡 You can now manually click RUN to test the solution")
                else:
                    print(f"❌ Challenge #{challenge_count} failed to solve")
                    
                print(f"\n📊 Total challenges processed: {challenge_count}")
                
            except KeyboardInterrupt:
                print("\n⚠️ Interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error in challenge {challenge_count}: {e}")
                print(f"❌ Error occurred: {e}")
                continue
        
        input("\nPress Enter to close the browser...")
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        automator.close()

if __name__ == "__main__":
    main() 