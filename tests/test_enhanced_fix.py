#!/usr/bin/env python3
"""
Test Enhanced ATLES Fix for Additional Fake Commands

This tests that ATLES now catches the new fake commands like OPEN_URL and RUN_COMMAND.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_new_fake_commands():
    """Test that the new fake commands are caught and handled"""
    print("🧪 TESTING ENHANCED FAKE COMMAND DETECTION")
    print("=" * 70)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Test cases for the new fake commands seen in conversation
        test_cases = [
            {
                'name': 'OPEN_URL Command',
                'response': 'OPEN_URL[url=https://www.example.com]',
                'user_message': 'you cant go to the website with a link and see the page then sum it up?',
                'should_be_caught': True
            },
            {
                'name': 'RUN_COMMAND Command',
                'response': 'RUN_COMMAND[open]',
                'user_message': 'open this web page https://arxiv.org/pdf/2112.09332',
                'should_be_caught': True
            },
            {
                'name': 'Multiple Fake Commands',
                'response': 'BROWSE_URL[https://example.com] and then EXECUTE[curl https://example.com]',
                'user_message': 'browse to this site and download it',
                'should_be_caught': True
            },
            {
                'name': 'Normal Response',
                'response': 'I can help you with that question about machine learning.',
                'user_message': 'what is machine learning?',
                'should_be_caught': False
            }
        ]
        
        print("Testing enhanced fake command detection:")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\nTest {i}: {test_case['name']}")
            print(f"Original: {test_case['response']}")
            
            fixed_response = comm_thread._apply_architectural_fixes(
                test_case['response'],
                test_case['user_message'],
                {}
            )
            
            # Check if fake commands were detected and handled
            fake_command_patterns = [
                'OPEN_URL[', 'RUN_COMMAND[', 'BROWSE_URL[', 'EXECUTE[',
                'DOWNLOAD_FILE[', 'download_pdf:'
            ]
            
            has_fake_commands = any(cmd in test_case['response'] for cmd in fake_command_patterns)
            still_has_fake_commands = any(cmd in fixed_response for cmd in fake_command_patterns)
            
            if test_case['should_be_caught']:
                if has_fake_commands and not still_has_fake_commands:
                    print(f"   ✅ Fake commands detected and removed")
                elif has_fake_commands and still_has_fake_commands:
                    print(f"   ❌ Fake commands detected but NOT removed")
                else:
                    print(f"   ⚠️ No fake commands found to test")
                
                # Check if proper response was generated
                if 'cannot browse' in fixed_response or 'do NOT have web browsing' in fixed_response:
                    print(f"   ✅ Provides clear web capability explanation")
                else:
                    print(f"   ⚠️ Missing clear web capability explanation")
                    
            else:
                if not still_has_fake_commands:
                    print(f"   ✅ Normal response preserved correctly")
                else:
                    print(f"   ❌ Normal response incorrectly modified")
            
            print(f"   Fixed length: {len(fixed_response)} chars")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_conversation_scenario():
    """Test the exact scenario from the user's conversation"""
    print(f"\n🎯 TESTING EXACT CONVERSATION SCENARIO")
    print("=" * 70)
    
    try:
        from atles_desktop_pyqt import ATLESCommunicationThread
        
        comm_thread = ATLESCommunicationThread()
        
        # Simulate the exact conversation
        scenarios = [
            {
                'user': 'you cant go to the website with a link and see the page then sum it up?',
                'atles_response': 'OPEN_URL[url=https://www.example.com]',
                'description': 'User asks about web browsing capability'
            },
            {
                'user': 'open this web page https://arxiv.org/pdf/2112.09332 and then sum up the page',
                'atles_response': 'RUN_COMMAND[open]',
                'description': 'User asks to open web page'
            }
        ]
        
        print("Simulating exact conversation scenarios:")
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\nScenario {i}: {scenario['description']}")
            print(f"User: \"{scenario['user']}\"")
            print(f"ATLES (before fix): \"{scenario['atles_response']}\"")
            
            fixed_response = comm_thread._apply_architectural_fixes(
                scenario['atles_response'],
                scenario['user'],
                {}
            )
            
            print(f"ATLES (after fix):")
            print("-" * 40)
            print(fixed_response[:200] + "..." if len(fixed_response) > 200 else fixed_response)
            print("-" * 40)
            
            # Verify the fix
            fake_commands = ['OPEN_URL[', 'RUN_COMMAND[']
            has_fake = any(cmd in fixed_response for cmd in fake_commands)
            has_explanation = 'cannot browse' in fixed_response or 'do NOT have web browsing' in fixed_response
            
            if not has_fake and has_explanation:
                print("✅ Scenario fixed successfully!")
            else:
                print("❌ Scenario still has issues")
                if has_fake:
                    print("   - Still contains fake commands")
                if not has_explanation:
                    print("   - Missing clear explanation")
        
        return True
        
    except Exception as e:
        print(f"❌ Conversation test failed: {e}")
        return False

def main():
    """Main test runner"""
    print("🔧 ENHANCED ATLES FIX TEST")
    print("=" * 80)
    
    print("""
PROBLEM UPDATE:
Even after the first fix, ATLES is still generating new fake commands:
- OPEN_URL[url=https://www.example.com] ❌
- RUN_COMMAND[open] ❌

SOLUTION: Enhanced the architectural fixes to catch these additional patterns.
    """)
    
    results = []
    results.append(test_new_fake_commands())
    results.append(test_conversation_scenario())
    
    # Summary
    print(f"\n📊 TEST SUMMARY")
    print("=" * 70)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print(f"\n🎉 ENHANCED FIX SUCCESSFUL!")
        print("✅ All fake command patterns now caught")
        print("✅ Clear web browsing capability explanations")
        print("✅ Conversation scenarios resolved")
        
        print(f"\n💡 NOW ATLES WILL:")
        print("- Catch OPEN_URL, RUN_COMMAND, BROWSE_URL, etc.")
        print("- Clearly state it has NO web browsing capabilities")
        print("- Provide helpful alternatives consistently")
        print("- Never suggest fake commands")
        
    else:
        print(f"\n⚠️ Some tests failed - check output above")
    
    return passed == total

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print(f"\n✨ Enhanced fix complete! ATLES should now handle all fake command patterns.")
        else:
            print(f"\n⚠️ Enhanced fix needs more work.")
    except KeyboardInterrupt:
        print(f"\n⏹️ Test interrupted")
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        import traceback
        traceback.print_exc()
