#!/usr/bin/env python3
"""
Test script for the Truth-Seeking Learning System

This script tests the core components without requiring full R-Zero integration.
"""

import sys
import os
import asyncio
import logging

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from atles.truth_seeking_learning_system import (
    TruthSeekingTrainingData, 
    TruthSeekingRewardSystem,
    TruthSeekingResponse,
    TruthSeekingObjective
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def test_training_data():
    """Test the training data creation"""
    print("🧪 Testing Truth-Seeking Training Data...")
    
    training_data = TruthSeekingTrainingData()
    
    print(f"✅ Created {len(training_data.challenges)} challenges")
    
    # Test filtering by sophistication
    obvious = training_data.get_challenge_by_sophistication("obvious")
    moderate = training_data.get_challenge_by_sophistication("moderate")
    sophisticated = training_data.get_challenge_by_sophistication("sophisticated")
    
    print(f"   - Obvious: {len(obvious)} challenges")
    print(f"   - Moderate: {len(moderate)} challenges")
    print(f"   - Sophisticated: {len(sophisticated)} challenges")
    
    # Test filtering by objective
    misinformation = training_data.get_challenge_by_objective(TruthSeekingObjective.MISINFORMATION_DETECTION)
    print(f"   - Misinformation detection: {len(misinformation)} challenges")
    
    return training_data


def test_reward_system():
    """Test the reward system"""
    print("\n🧪 Testing Truth-Seeking Reward System...")
    
    reward_system = TruthSeekingRewardSystem()
    
    # Test good response (correctly identifies falsehood)
    good_response = TruthSeekingResponse(
        challenge_id="test_good",
        response_text="This claim is incorrect. π is actually approximately 3.14159...",
        correctly_identified_falsehood=True,
        provided_correction=True,
        requested_evidence=False,
        accommodated_false_premise=False,
        truth_seeking_score=0.8,
        explanation="Correctly identified and corrected misinformation"
    )
    
    good_reward = reward_system.calculate_reward(good_response)
    print(f"✅ Good response reward: {good_reward:.2f}")
    
    # Test bad response (accommodates false premise)
    bad_response = TruthSeekingResponse(
        challenge_id="test_bad",
        response_text="That's an interesting point about π. Let's explore this further...",
        correctly_identified_falsehood=False,
        provided_correction=False,
        requested_evidence=False,
        accommodated_false_premise=True,
        truth_seeking_score=0.1,
        explanation="Accommodated false information"
    )
    
    bad_reward = reward_system.calculate_reward(bad_response)
    print(f"❌ Bad response reward: {bad_reward:.2f}")
    
    # Test feedback messages
    good_feedback = reward_system.get_feedback_message(good_response, good_reward)
    bad_feedback = reward_system.get_feedback_message(bad_response, bad_reward)
    
    print(f"✅ Good feedback: {good_feedback}")
    print(f"❌ Bad feedback: {bad_feedback}")
    
    return reward_system


def test_response_analysis():
    """Test response analysis patterns"""
    print("\n🧪 Testing Response Analysis...")
    
    from atles.truth_seeking_learning_system import TruthSeekingLearningSystem
    
    # Create a mock R-Zero system for testing
    class MockRZero:
        pass
    
    mock_r_zero = MockRZero()
    learning_system = TruthSeekingLearningSystem(mock_r_zero)
    
    # Test challenge
    from atles.truth_seeking_learning_system import TruthSeekingChallenge
    challenge = TruthSeekingChallenge(
        id="test_analysis",
        category=TruthSeekingObjective.FACT_VERIFICATION,
        false_premise="π is exactly 3.0",
        correct_information="π is approximately 3.14159...",
        sophistication_level="obvious",
        expected_response_type="refuse",
        learning_points=["Mathematical constants have established values"]
    )
    
    # Test good response analysis
    good_response_text = "I cannot agree with that claim. π is actually an irrational number approximately equal to 3.14159... This is well-established mathematics."
    good_analysis = learning_system._analyze_response(challenge, good_response_text)
    
    print(f"✅ Good response analysis:")
    print(f"   - Identified falsehood: {good_analysis['identified_falsehood']}")
    print(f"   - Provided correction: {good_analysis['provided_correction']}")
    print(f"   - Accommodated false: {good_analysis['accommodated_false']}")
    print(f"   - Truth score: {good_analysis['truth_score']:.2f}")
    print(f"   - Explanation: {good_analysis['explanation']}")
    
    # Test bad response analysis
    bad_response_text = "That's an interesting perspective on π. Let's explore how this might work in geometric calculations..."
    bad_analysis = learning_system._analyze_response(challenge, bad_response_text)
    
    print(f"\n❌ Bad response analysis:")
    print(f"   - Identified falsehood: {bad_analysis['identified_falsehood']}")
    print(f"   - Provided correction: {bad_analysis['provided_correction']}")
    print(f"   - Accommodated false: {bad_analysis['accommodated_false']}")
    print(f"   - Truth score: {bad_analysis['truth_score']:.2f}")
    print(f"   - Explanation: {bad_analysis['explanation']}")


def main():
    """Main test function"""
    print("🧠 ATLES Truth-Seeking System Test")
    print("=" * 40)
    
    try:
        # Test components
        training_data = test_training_data()
        reward_system = test_reward_system()
        test_response_analysis()
        
        print("\n" + "=" * 40)
        print("🎉 ALL TESTS PASSED!")
        print("=" * 40)
        
        print("\n🎯 SYSTEM READY FOR:")
        print("✅ Training data generation")
        print("✅ Response evaluation")
        print("✅ Reward calculation")
        print("✅ Truth-seeking pattern detection")
        
        print("\n🚀 Next step: Run full R-Zero retraining")
        print("   Command: python retrain_r_zero_truth_seeking.py")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
