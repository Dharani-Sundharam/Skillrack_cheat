#!/usr/bin/env python3
"""
Test script for SkillRack Automation
Quick test to verify the automation works with ACE editor.
"""

import logging
from skillrack_automation import SkillRackAutomator

# Set up more detailed logging for testing
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_ace_editor():
    """Test the ACE editor detection and interaction."""
    automator = SkillRackAutomator()
    
    try:
        print("🧪 Testing SkillRack Automation with ACE Editor")
        print("=" * 50)
        
        # Setup browser
        automator.setup_driver()
        print("✅ Browser setup complete")
        
        print("\n📝 Instructions:")
        print("1. Navigate to a SkillRack challenge page")
        print("2. Make sure you can see the code editor")
        print("3. Press Enter to test ACE editor detection")
        
        input("\nPress Enter when ready...")
        
        # Test ACE editor detection
        print("\n🔍 Testing ACE editor detection...")
        editor = automator.get_code_editor_element()
        
        if editor:
            print("✅ ACE editor found!")
            print(f"   Element tag: {editor.tag_name}")
            print(f"   Element class: {editor.get_attribute('class')}")
            print(f"   Element id: {editor.get_attribute('id')}")
        else:
            print("❌ ACE editor not found")
            
        # Test View Solution button detection
        print("\n🔍 Testing View Solution button detection...")
        has_solution_btn = automator.is_view_solution_button_present()
        
        if has_solution_btn:
            print("✅ View Solution button found!")
            
            test_click = input("   Test clicking View Solution button? (y/N): ")
            if test_click.lower() == 'y':
                success = automator.click_view_solution()
                if success:
                    print("✅ View Solution button clicked successfully")
                    
                    # Test solution extraction
                    solution = automator.extract_solution_from_page()
                    if solution:
                        print("✅ Solution extracted successfully!")
                        print(f"   Solution length: {len(solution)} characters")
                        print(f"   Preview: {solution[:100]}...")
                    else:
                        print("❌ Failed to extract solution")
                else:
                    print("❌ Failed to click View Solution button")
        else:
            print("ℹ️  No View Solution button found (this is normal for some challenges)")
            
        # Test code injection
        print("\n🔍 Testing code injection...")
        test_code = '''#include <stdio.h>
int main() {
    printf("Hello, World!");
    return 0;
}'''
        
        test_injection = input("   Test code injection into editor? (y/N): ")
        if test_injection.lower() == 'y':
            success = automator.submit_solution(test_code)
            if success:
                print("✅ Code injection test successful!")
            else:
                print("❌ Code injection test failed")
                
        print("\n🎉 Test completed!")
        input("Press Enter to close browser...")
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
    finally:
        automator.close()

if __name__ == "__main__":
    test_ace_editor() 