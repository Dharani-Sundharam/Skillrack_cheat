#!/usr/bin/env python3
"""
SkillRack Batch Solver
Automates solving multiple coding challenges sequentially.
"""

import time
import logging
from skillrack_automation import SkillRackAutomator
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

logger = logging.getLogger(__name__)

class SkillRackBatchSolver(SkillRackAutomator):
    def __init__(self, config_file: str = "config.json"):
        """Initialize the batch solver."""
        super().__init__(config_file)
        self.solved_count = 0
        self.failed_count = 0
        
    def find_challenge_links(self):
        """Find all challenge links on the current page."""
        try:
            # Common selectors for challenge links
            link_selectors = [
                "a[href*='program']",
                "a[href*='challenge']",
                "a[href*='problem']",
                ".challenge-link",
                ".problem-link"
            ]
            
            challenge_links = []
            for selector in link_selectors:
                try:
                    links = self.driver.find_elements(By.CSS_SELECTOR, selector)
                    for link in links:
                        href = link.get_attribute('href')
                        if href and href not in challenge_links:
                            challenge_links.append(href)
                except NoSuchElementException:
                    continue
                    
            logger.info(f"Found {len(challenge_links)} challenge links")
            return challenge_links
            
        except Exception as e:
            logger.error(f"Error finding challenge links: {e}")
            return []
            
    def navigate_to_next_challenge(self):
        """Navigate to the next challenge."""
        try:
            # Look for "Next" button or similar navigation
            next_selectors = [
                "//a[contains(text(), 'Next')]",
                "//button[contains(text(), 'Next')]",
                ".next-button",
                ".nav-next"
            ]
            
            for selector in next_selectors:
                try:
                    if selector.startswith("//"):
                        next_button = self.driver.find_element(By.XPATH, selector)
                    else:
                        next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                        
                    if next_button.is_displayed() and next_button.is_enabled():
                        next_button.click()
                        self.human_delay(2, 4)
                        return True
                except NoSuchElementException:
                    continue
                    
            return False
            
        except Exception as e:
            logger.error(f"Error navigating to next challenge: {e}")
            return False
            
    def run_batch_solve(self, max_challenges: int = 10):
        """Run batch solving for multiple challenges."""
        logger.info(f"Starting batch solve for up to {max_challenges} challenges")
        
        for i in range(max_challenges):
            try:
                logger.info(f"Processing challenge {i + 1}/{max_challenges}")
                
                # Solve current challenge
                success = self.solve_current_challenge()
                
                if success:
                    self.solved_count += 1
                    logger.info(f"✅ Challenge {i + 1} solved successfully")
                else:
                    self.failed_count += 1
                    logger.warning(f"❌ Challenge {i + 1} failed")
                
                # Add delay between challenges
                self.human_delay(5, 10)
                
                # Navigate to next challenge
                if i < max_challenges - 1:
                    if not self.navigate_to_next_challenge():
                        logger.info("No more challenges found. Batch processing complete.")
                        break
                        
            except KeyboardInterrupt:
                logger.info("Batch processing interrupted by user")
                break
            except Exception as e:
                logger.error(f"Error processing challenge {i + 1}: {e}")
                self.failed_count += 1
                continue
                
        # Print summary
        total_processed = self.solved_count + self.failed_count
        success_rate = (self.solved_count / total_processed * 100) if total_processed > 0 else 0
        
        print("\n" + "="*50)
        print("BATCH PROCESSING SUMMARY")
        print("="*50)
        print(f"Total Processed: {total_processed}")
        print(f"Successfully Solved: {self.solved_count}")
        print(f"Failed: {self.failed_count}")
        print(f"Success Rate: {success_rate:.1f}%")
        print("="*50)

def main():
    """Main function for batch processing."""
    batch_solver = SkillRackBatchSolver()
    
    try:
        # Setup browser
        batch_solver.setup_driver()
        
        print("SkillRack Batch Solver")
        print("=====================")
        
        input("Please navigate to the SkillRack challenges page and press Enter to continue...")
        
        # Get max challenges from user
        while True:
            try:
                max_challenges = int(input("Enter maximum number of challenges to solve (default: 10): ") or "10")
                break
            except ValueError:
                print("Please enter a valid number.")
                
        # Confirm before starting
        confirm = input(f"This will attempt to solve up to {max_challenges} challenges. Continue? (y/N): ")
        if confirm.lower() != 'y':
            print("Batch processing cancelled.")
            return
            
        # Run batch solve
        batch_solver.run_batch_solve(max_challenges)
        
        input("Press Enter to close the browser...")
        
    except KeyboardInterrupt:
        logger.info("Script interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
    finally:
        batch_solver.close()

if __name__ == "__main__":
    main() 