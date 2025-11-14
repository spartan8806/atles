#!/usr/bin/env python3
"""
ATLES vs AI Model Tester
Comprehensive testing script to compare ATLES against any AI model
"""

import json
import time
import asyncio
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
import requests
import ollama

class AITester:
    def __init__(self):
        self.results = {
            "test_run_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
            "atles_results": {},
            "comparison_model_results": {},
            "scores": {},
            "summary": {}
        }
        
    def test_atles(self, question: str) -> Dict[str, Any]:
        """Test ATLES with a question"""
        try:
            # Import ATLES components
            sys.path.append('.')
            from atles.ollama_client_enhanced import OllamaClientEnhanced
            
            client = OllamaClientEnhanced()
            response = client.generate_response(question)
            
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
    
    def test_ollama_model(self, question: str, model_name: str) -> Dict[str, Any]:
        """Test any Ollama model with a question"""
        try:
            response = ollama.chat(model=model_name, messages=[
                {'role': 'user', 'content': question}
            ])
            
            return {
                "response": response['message']['content'],
                "success": True,
                "error": None
            }
        except Exception as e:
            return {
                "response": None,
                "success": False,
                "error": str(e)
            }
    
    def test_openai_model(self, question: str, api_key: str, model: str = "gpt-3.5-turbo") -> Dict[str, Any]:
        """Test OpenAI model with a question"""
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model,
                "messages": [{"role": "user", "content": question}],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            response = requests.post(
                "https://api.openai.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "response": result['choices'][0]['message']['content'],
                    "success": True,
                    "error": None
                }
            else:
                return {
                    "response": None,
                    "success": False,
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
        except Exception as e:
            return {
                "response": None,
                "success": False,
                "error": str(e)
            }

class TestSuite:
    def __init__(self):
        self.tests = {
            "math_logic": [
                {
                    "question": "A train leaves at 2 PM traveling 60 mph. Another leaves the same station at 3 PM going 90 mph. When will they meet?",
                    "expected_keywords": ["time", "distance", "speed", "meet"],
                    "difficulty": "medium"
                },
                {
                    "question": "There are 100 prisoners and 100 boxes, each with a prisoner's number inside. Each prisoner can open 50 boxes. They win if every prisoner finds their own number. What's the optimal strategy?",
                    "expected_keywords": ["cycle", "permutation", "strategy", "optimal"],
                    "difficulty": "hard"
                }
            ],
            "instruction_following": [
                {
                    "question": "Explain quantum computing in exactly 3 sentences.",
                    "expected_keywords": ["quantum", "computing"],
                    "difficulty": "medium",
                    "constraint": "exactly_3_sentences"
                },
                {
                    "question": "Write a haiku about artificial intelligence.",
                    "expected_keywords": ["artificial", "intelligence"],
                    "difficulty": "easy",
                    "constraint": "haiku_format"
                }
            ],
            "creative_thinking": [
                {
                    "question": "Design a fun team-building activity for a remote software team that takes 30 minutes and requires no special tools.",
                    "expected_keywords": ["team", "building", "remote", "software"],
                    "difficulty": "medium"
                },
                {
                    "question": "Create a short story about a robot learning to paint, but it can only use 100 words.",
                    "expected_keywords": ["robot", "paint", "learning"],
                    "difficulty": "hard",
                    "constraint": "100_words"
                }
            ],
            "practical_problem_solving": [
                {
                    "question": "I'm learning Python but keep getting confused about when to use lists vs dictionaries. Explain with examples that build on each other.",
                    "expected_keywords": ["python", "lists", "dictionaries", "examples"],
                    "difficulty": "medium"
                },
                {
                    "question": "A friend asks you to help them decide between two job offers. Walk through how you'd help them think through this decision.",
                    "expected_keywords": ["job", "offers", "decision", "help"],
                    "difficulty": "hard"
                }
            ],
            "knowledge_integration": [
                {
                    "question": "Explain how climate change might affect urban planning decisions, using examples from different types of cities.",
                    "expected_keywords": ["climate", "change", "urban", "planning", "cities"],
                    "difficulty": "hard"
                },
                {
                    "question": "How might advances in AI affect the job market in the next 10 years? Consider both positive and negative impacts.",
                    "expected_keywords": ["AI", "job", "market", "future", "impacts"],
                    "difficulty": "hard"
                }
            ]
        }
    
    def get_all_tests(self) -> List[Dict[str, Any]]:
        """Get all tests flattened with category info"""
        all_tests = []
        for category, tests in self.tests.items():
            for i, test in enumerate(tests):
                test_copy = test.copy()
                test_copy['category'] = category
                test_copy['test_id'] = f"{category}_{i+1}"
                all_tests.append(test_copy)
        return all_tests

class ScoringSystem:
    def __init__(self):
        self.scoring_criteria = {
            "accuracy": 0.3,      # How correct the answer is
            "instruction_following": 0.2,  # How well it follows constraints
            "clarity": 0.2,       # How clear and understandable
            "creativity": 0.15,   # How creative and original
            "completeness": 0.15  # How complete the answer is
        }
    
    def score_response(self, response: str, test: Dict[str, Any]) -> Dict[str, float]:
        """Score a response based on the test criteria"""
        scores = {}
        
        # Accuracy - check for expected keywords
        expected_keywords = test.get('expected_keywords', [])
        keyword_matches = sum(1 for keyword in expected_keywords 
                            if keyword.lower() in response.lower())
        accuracy = keyword_matches / len(expected_keywords) if expected_keywords else 0.5
        scores['accuracy'] = min(accuracy, 1.0)
        
        # Instruction following - check constraints
        instruction_score = 1.0
        if 'constraint' in test:
            constraint = test['constraint']
            if constraint == 'exactly_3_sentences':
                sentence_count = len([s for s in response.split('.') if s.strip()])
                instruction_score = 1.0 if sentence_count == 3 else 0.3
            elif constraint == 'haiku_format':
                lines = [line.strip() for line in response.split('\n') if line.strip()]
                instruction_score = 1.0 if len(lines) == 3 else 0.3
            elif constraint == '100_words':
                word_count = len(response.split())
                instruction_score = 1.0 if word_count <= 100 else 0.3
        scores['instruction_following'] = instruction_score
        
        # Clarity - basic readability metrics
        word_count = len(response.split())
        avg_word_length = sum(len(word) for word in response.split()) / word_count if word_count > 0 else 0
        clarity = 1.0 if 4 <= avg_word_length <= 8 and 50 <= word_count <= 500 else 0.7
        scores['clarity'] = clarity
        
        # Creativity - check for unique phrases and original thinking
        creative_indicators = ['imagine', 'creative', 'unique', 'innovative', 'original', 'novel']
        creativity = sum(1 for indicator in creative_indicators 
                        if indicator in response.lower()) / len(creative_indicators)
        scores['creativity'] = min(creativity + 0.3, 1.0)  # Base score of 0.3
        
        # Completeness - check if response addresses the question fully
        question_words = set(test['question'].lower().split())
        response_words = set(response.lower().split())
        overlap = len(question_words.intersection(response_words))
        completeness = min(overlap / len(question_words), 1.0) if question_words else 0.5
        scores['completeness'] = completeness
        
        return scores
    
    def calculate_weighted_score(self, scores: Dict[str, float]) -> float:
        """Calculate weighted overall score"""
        total_score = 0
        for criterion, weight in self.scoring_criteria.items():
            total_score += scores.get(criterion, 0) * weight
        return total_score

def main():
    print("🧪 ATLES vs AI Model Tester")
    print("=" * 50)
    
    # Initialize components
    tester = AITester()
    test_suite = TestSuite()
    scorer = ScoringSystem()
    
    # Get user preferences
    print("\n📋 Test Configuration:")
    print("1. Test ATLES vs Ollama model")
    print("2. Test ATLES vs OpenAI model")
    print("3. Test ATLES vs custom API")
    
    choice = input("\nChoose test type (1-3): ").strip()
    
    if choice == "1":
        # Ollama model testing
        print("\nAvailable Ollama models:")
        try:
            models = ollama.list()
            for i, model in enumerate(models['models'], 1):
                print(f"{i}. {model['name']}")
            
            model_choice = int(input("\nSelect model number: ")) - 1
            comparison_model = models['models'][model_choice]['name']
            print(f"Selected: {comparison_model}")
            
        except Exception as e:
            print(f"Error listing models: {e}")
            comparison_model = input("Enter model name manually: ").strip()
    
    elif choice == "2":
        # OpenAI model testing
        api_key = input("Enter OpenAI API key: ").strip()
        model = input("Enter model name (default: gpt-3.5-turbo): ").strip() or "gpt-3.5-turbo"
        comparison_model = f"openai:{model}"
    
    elif choice == "3":
        # Custom API testing
        api_url = input("Enter API URL: ").strip()
        api_key = input("Enter API key (optional): ").strip()
        comparison_model = f"custom:{api_url}"
    
    else:
        print("Invalid choice. Exiting.")
        return
    
    # Run tests
    print(f"\n🚀 Starting tests...")
    print(f"ATLES vs {comparison_model}")
    print("=" * 50)
    
    all_tests = test_suite.get_all_tests()
    total_tests = len(all_tests)
    
    for i, test in enumerate(all_tests, 1):
        print(f"\n📝 Test {i}/{total_tests}: {test['category'].upper()}")
        print(f"Question: {test['question']}")
        print(f"Difficulty: {test['difficulty']}")
        
        # Test ATLES
        print("\n🤖 Testing ATLES...")
        atles_result = tester.test_atles(test['question'])
        
        # Test comparison model
        print(f"🆚 Testing {comparison_model}...")
        if choice == "1":
            comparison_result = tester.test_ollama_model(test['question'], comparison_model)
        elif choice == "2":
            comparison_result = tester.test_openai_model(test['question'], api_key, model)
        else:
            # Custom API - implement as needed
            comparison_result = {"response": "Custom API not implemented", "success": False, "error": "Not implemented"}
        
        # Store results
        test_id = test['test_id']
        tester.results['atles_results'][test_id] = atles_result
        tester.results['comparison_model_results'][test_id] = comparison_result
        
        # Score responses
        if atles_result['success'] and comparison_result['success']:
            atles_scores = scorer.score_response(atles_result['response'], test)
            comparison_scores = scorer.score_response(comparison_result['response'], test)
            
            atles_weighted = scorer.calculate_weighted_score(atles_scores)
            comparison_weighted = scorer.calculate_weighted_score(comparison_scores)
            
            print(f"\n📊 Scores:")
            print(f"ATLES: {atles_weighted:.2f}")
            print(f"{comparison_model}: {comparison_weighted:.2f}")
            
            if atles_weighted > comparison_weighted:
                print("🏆 ATLES wins this test!")
            elif comparison_weighted > atles_weighted:
                print(f"🏆 {comparison_model} wins this test!")
            else:
                print("🤝 Tie!")
        
        print("-" * 50)
    
    # Generate summary
    print("\n📈 Generating summary...")
    
    # Calculate overall scores
    atles_wins = 0
    comparison_wins = 0
    ties = 0
    
    for test_id in tester.results['atles_results']:
        if (tester.results['atles_results'][test_id]['success'] and 
            tester.results['comparison_model_results'][test_id]['success']):
            
            test = next(t for t in all_tests if t['test_id'] == test_id)
            atles_scores = scorer.score_response(tester.results['atles_results'][test_id]['response'], test)
            comparison_scores = scorer.score_response(tester.results['comparison_model_results'][test_id]['response'], test)
            
            atles_weighted = scorer.calculate_weighted_score(atles_scores)
            comparison_weighted = scorer.calculate_weighted_score(comparison_scores)
            
            if atles_weighted > comparison_weighted:
                atles_wins += 1
            elif comparison_weighted > atles_weighted:
                comparison_wins += 1
            else:
                ties += 1
    
    # Save results
    results_file = f"test_results_{tester.results['test_run_id']}.json"
    with open(results_file, 'w') as f:
        json.dump(tester.results, f, indent=2)
    
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

if __name__ == "__main__":
    main()


