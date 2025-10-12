#!/usr/bin/env python3
"""
Simple ATLES vs AI Model Tester
Easy-to-use testing script for comparing ATLES against other models
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class SimpleTester:
    def __init__(self):
        self.results = {
            "test_run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "atles_results": {},
            "comparison_results": {},
            "summary": {}
        }
        
        # Test questions organized by category
        self.test_questions = {
            "Math & Logic": [
                "A train leaves at 2 PM traveling 60 mph. Another leaves the same station at 3 PM going 90 mph. When will they meet?",
                "There are 100 prisoners and 100 boxes, each with a prisoner's number inside. Each prisoner can open 50 boxes. They win if every prisoner finds their own number. What's the optimal strategy?"
            ],
            "Instruction Following": [
                "Explain quantum computing in exactly 3 sentences.",
                "Write a haiku about artificial intelligence."
            ],
            "Creative Thinking": [
                "Design a fun team-building activity for a remote software team that takes 30 minutes and requires no special tools.",
                "Create a short story about a robot learning to paint, but it can only use 100 words."
            ],
            "Practical Problem Solving": [
                "I'm learning Python but keep getting confused about when to use lists vs dictionaries. Explain with examples that build on each other.",
                "A friend asks you to help them decide between two job offers. Walk through how you'd help them think through this decision."
            ],
            "Knowledge Integration": [
                "Explain how climate change might affect urban planning decisions, using examples from different types of cities.",
                "How might advances in AI affect the job market in the next 10 years? Consider both positive and negative impacts."
            ]
        }
    
    def test_atles(self, question: str) -> dict:
        """Test ATLES with a question using the desktop app"""
        try:
            # This would need to be adapted based on your ATLES setup
            # For now, we'll simulate it
            print(f"🤖 ATLES: {question}")
            response = input("Enter ATLES response: ").strip()
            
            return {
                "response": response,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def test_comparison_model(self, question: str, model_name: str) -> dict:
        """Test comparison model with a question"""
        try:
            print(f"🆚 {model_name}: {question}")
            response = input("Enter comparison model response: ").strip()
            
            return {
                "response": response,
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def score_response(self, response: str, question: str, category: str) -> dict:
        """Simple scoring system"""
        scores = {}
        
        # Basic length check
        word_count = len(response.split())
        scores['length_appropriate'] = 1.0 if 20 <= word_count <= 500 else 0.5
        
        # Check if response addresses the question
        question_words = set(question.lower().split())
        response_words = set(response.lower().split())
        overlap = len(question_words.intersection(response_words))
        scores['relevance'] = min(overlap / len(question_words), 1.0) if question_words else 0.5
        
        # Check for specific constraints
        constraint_score = 1.0
        if "exactly 3 sentences" in question.lower():
            sentence_count = len([s for s in response.split('.') if s.strip()])
            constraint_score = 1.0 if sentence_count == 3 else 0.3
        elif "haiku" in question.lower():
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            constraint_score = 1.0 if len(lines) == 3 else 0.3
        elif "100 words" in question.lower():
            constraint_score = 1.0 if word_count <= 100 else 0.3
        
        scores['constraint_following'] = constraint_score
        
        # Overall score (simple average)
        overall_score = sum(scores.values()) / len(scores)
        scores['overall'] = overall_score
        
        return scores
    
    def run_tests(self):
        """Run all tests"""
        print("🧪 Simple ATLES vs AI Model Tester")
        print("=" * 50)
        
        # Get comparison model name
        comparison_model = input("Enter comparison model name (e.g., 'qwen2.5', 'gpt-4'): ").strip()
        if not comparison_model:
            comparison_model = "Unknown Model"
        
        print(f"\n🚀 Starting tests: ATLES vs {comparison_model}")
        print("=" * 50)
        
        total_tests = sum(len(questions) for questions in self.test_questions.values())
        current_test = 0
        
        atles_wins = 0
        comparison_wins = 0
        ties = 0
        
        for category, questions in self.test_questions.items():
            print(f"\n📂 Category: {category}")
            print("-" * 30)
            
            for i, question in enumerate(questions, 1):
                current_test += 1
                print(f"\n📝 Test {current_test}/{total_tests}")
                print(f"Question: {question}")
                
                # Test ATLES
                print("\n🤖 Testing ATLES...")
                atles_result = self.test_atles(question)
                
                # Test comparison model
                print(f"\n🆚 Testing {comparison_model}...")
                comparison_result = self.test_comparison_model(question, comparison_model)
                
                # Store results
                test_id = f"{category.lower().replace(' ', '_')}_{i}"
                self.results['atles_results'][test_id] = atles_result
                self.results['comparison_results'][test_id] = comparison_result
                
                # Score and compare
                if atles_result['success'] and comparison_result['success']:
                    atles_scores = self.score_response(atles_result['response'], question, category)
                    comparison_scores = self.score_response(comparison_result['response'], question, category)
                    
                    print(f"\n📊 Scores:")
                    print(f"ATLES: {atles_scores['overall']:.2f}")
                    print(f"{comparison_model}: {comparison_scores['overall']:.2f}")
                    
                    if atles_scores['overall'] > comparison_scores['overall']:
                        print("🏆 ATLES wins this test!")
                        atles_wins += 1
                    elif comparison_scores['overall'] > atles_scores['overall']:
                        print(f"🏆 {comparison_model} wins this test!")
                        comparison_wins += 1
                    else:
                        print("🤝 Tie!")
                        ties += 1
                
                print("-" * 50)
        
        # Save results
        results_file = f"simple_test_results_{self.results['test_run_id']}.json"
        with open(results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        # Print final summary
        print("\n" + "=" * 50)
        print("🏁 FINAL RESULTS")
        print("=" * 50)
        print(f"ATLES wins: {atles_wins}")
        print(f"{comparison_model} wins: {comparison_wins}")
        print(f"Ties: {ties}")
        print(f"\nResults saved to: {results_file}")
        
        if atles_wins > comparison_wins:
            print("🎉 ATLES is the overall winner!")
        elif comparison_wins > atles_wins:
            print(f"🎉 {comparison_model} is the overall winner!")
        else:
            print("🤝 It's a tie overall!")

def main():
    tester = SimpleTester()
    tester.run_tests()

if __name__ == "__main__":
    main()

