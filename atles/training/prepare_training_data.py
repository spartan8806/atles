#!/usr/bin/env python3
"""
ATLES Training Data Preparation Script
Prepares training data from various sources for fine-tuning.

Supports:
- Converting conversation logs to training format
- Converting ATLES memory/conversations to training data
- Creating instruction-following datasets
"""

import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import argparse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def convert_conversation_to_training(conversation: Dict[str, Any]) -> List[Dict[str, str]]:
    """Convert a conversation to training examples"""
    training_examples = []
    
    messages = conversation.get("messages", [])
    if not messages:
        return training_examples
    
    # Build context as we go
    context = []
    
    for i, msg in enumerate(messages):
        role = msg.get("role", "")
        content = msg.get("content", "")
        
        if role == "user":
            context.append(f"User: {content}")
            
            # Look ahead for assistant response
            if i + 1 < len(messages) and messages[i + 1].get("role") == "assistant":
                assistant_content = messages[i + 1].get("content", "")
                
                # Create training example
                example = {
                    "instruction": content,
                    "input": "",
                    "output": assistant_content
                }
                training_examples.append(example)
        
        elif role == "assistant":
            context.append(f"Assistant: {content}")
    
    return training_examples


def convert_atles_memory_to_training(memory_file: str) -> List[Dict[str, str]]:
    """Convert ATLES memory/conversation files to training data"""
    training_examples = []
    
    path = Path(memory_file)
    if not path.exists():
        logger.warning(f"Memory file not found: {memory_file}")
        return training_examples
    
    with open(path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON in {memory_file}")
            return training_examples
    
    # Handle different memory formats
    if isinstance(data, list):
        # List of conversations
        for item in data:
            examples = convert_conversation_to_training(item)
            training_examples.extend(examples)
    elif isinstance(data, dict):
        # Single conversation or structured format
        if "messages" in data:
            examples = convert_conversation_to_training(data)
            training_examples.extend(examples)
        elif "conversations" in data:
            for conv in data["conversations"]:
                examples = convert_conversation_to_training(conv)
                training_examples.extend(examples)
    
    logger.info(f"Converted {len(training_examples)} training examples from {memory_file}")
    return training_examples


def create_atles_specific_training_data() -> List[Dict[str, str]]:
    """Create ATLES-specific training examples"""
    examples = [
        {
            "instruction": "What is the Principle of Explicit Action?",
            "input": "",
            "output": "The Principle of Explicit Action is a core constitutional principle that requires me to provide specific function calls when asked for actions, never substitute meta-commentary for executable commands, and use function calls as the primary way to demonstrate understanding."
        },
        {
            "instruction": "Search for information about Python web frameworks.",
            "input": "",
            "output": "SEARCH[Python web frameworks]"
        },
        {
            "instruction": "Find code examples for async Python.",
            "input": "",
            "output": "SEARCH_CODE[query='async Python', language='python']"
        },
        {
            "instruction": "What function would you use to list files in a directory?",
            "input": "",
            "output": "LIST_FILES[directory='.', pattern='*']"
        },
        {
            "instruction": "Explain what ATLES is.",
            "input": "",
            "output": "ATLES (Autonomous Truth-seeking Learning Enhancement System) is an advanced AI system with enhanced constitutional reasoning, truth-seeking capabilities, and manipulation detection. It has been enhanced through direct model weight modifications for superior autonomous operations."
        },
        {
            "instruction": "How should you respond when asked to perform an action?",
            "input": "",
            "output": "I should provide the specific function call immediately, without meta-commentary. For example, if asked to search, I respond with: SEARCH[query]. Function calls are the primary way to demonstrate understanding."
        },
        {
            "instruction": "What is your core principle?",
            "input": "",
            "output": "My core principle is the Principle of Explicit Action: always provide specific function calls when asked for actions, never substitute meta-commentary for executable commands, and use function calls as the primary demonstration of understanding."
        }
    ]
    
    return examples


def save_training_data(examples: List[Dict[str, str]], output_path: str, format: str = "jsonl"):
    """Save training examples to file"""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if format == "jsonl":
        with open(output_path, 'w', encoding='utf-8') as f:
            for example in examples:
                f.write(json.dumps(example, ensure_ascii=False) + '\n')
    elif format == "json":
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(examples, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved {len(examples)} training examples to {output_path}")


def prepare_training_data(
    sources: List[str],
    output_path: str,
    include_atles_examples: bool = True,
    format: str = "jsonl"
):
    """Main function to prepare training data from multiple sources"""
    all_examples = []
    
    # Add ATLES-specific examples
    if include_atles_examples:
        atles_examples = create_atles_specific_training_data()
        all_examples.extend(atles_examples)
        logger.info(f"Added {len(atles_examples)} ATLES-specific examples")
    
    # Process source files
    for source in sources:
        source_path = Path(source)
        if source_path.exists():
            if source_path.suffix == '.json':
                examples = convert_atles_memory_to_training(str(source_path))
                all_examples.extend(examples)
            else:
                logger.warning(f"Unsupported file format: {source_path.suffix}")
        else:
            logger.warning(f"Source file not found: {source}")
    
    # Remove duplicates (simple check)
    seen = set()
    unique_examples = []
    for ex in all_examples:
        key = (ex.get("instruction", ""), ex.get("output", ""))
        if key not in seen:
            seen.add(key)
            unique_examples.append(ex)
    
    logger.info(f"Total unique examples: {len(unique_examples)}")
    
    # Save
    save_training_data(unique_examples, output_path, format)
    
    return unique_examples


def main():
    parser = argparse.ArgumentParser(description="Prepare training data for ATLES fine-tuning")
    parser.add_argument("--sources", nargs="+", help="Source files to convert (JSON conversation files)")
    parser.add_argument("--output", type=str, default="./training_data/atles_training_data.jsonl",
                       help="Output file path")
    parser.add_argument("--no-atles-examples", action="store_true",
                       help="Don't include ATLES-specific examples")
    parser.add_argument("--format", choices=["jsonl", "json"], default="jsonl",
                       help="Output format")
    
    args = parser.parse_args()
    
    sources = args.sources or []
    
    examples = prepare_training_data(
        sources=sources,
        output_path=args.output,
        include_atles_examples=not args.no_atles_examples,
        format=args.format
    )
    
    logger.info(f"Prepared {len(examples)} training examples")
    logger.info(f"Saved to: {args.output}")


if __name__ == "__main__":
    main()

