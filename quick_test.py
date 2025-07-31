#!/usr/bin/env python3
"""
Quick Test for SkillRack Automation
Tests the core functionality after navigating to SkillRack.
"""

from skillrack_automation import SkillRackAutomator
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

def main():
    """Quick test of the automation."""
    automator = SkillRackAutomator()
    
    try:
        print("🚀 SkillRack Quick Test")
        print("=" * 30)
        
        # Setup browser
        automator.setup_driver()
        print("✅ Browser opened")
        
        print("\n📋 Instructions:")
        print("1. Navigate to a SkillRack challenge page")
        print("2. Make sure you can see the code editor and problem")
        print("3. Press Enter to start the automation")
        
        input("\nPress Enter when ready...")
        
        # Run the full automation
        print("\n🔄 Starting automation...")
        success = automator.solve_current_challenge()
        
        if success:
            print("\n✅ SUCCESS! Challenge automation completed")
        else:
            print("\n❌ FAILED! Check the log for details")
            
        print("\n📊 Check skillrack_automation.log for detailed information")
        input("\nPress Enter to close...")
        
    except KeyboardInterrupt:
        print("\n⚠️ Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        automator.close()

if __name__ == "__main__":
    main() 