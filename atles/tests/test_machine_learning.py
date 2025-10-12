#!/usr/bin/env python3
"""
Tests for ATLES Machine Learning System - Phase 2
"""

import pytest
import asyncio
import tempfile
import shutil
from pathlib import Path
from unittest.mock import Mock, patch

from atles.machine_learning import (
    ATLESMachineLearning,
    ConversationPatternLearner,
    ResponseQualityImprover,
    AdaptiveResponseGenerator,
    AdaptiveContext,
    LearningPattern,
    QualityMetric
)


class TestConversationPatternLearner:
    """Test conversation pattern learning functionality."""
    
    @pytest.fixture
    def learner(self, tmp_path):
        """Create a pattern learner with temporary directory."""
        return ConversationPatternLearner(learning_dir=tmp_path)
    
    @pytest.mark.asyncio
    async def test_learn_from_interaction(self, learner):
        """Test learning from a user-AI interaction."""
        context = {"user_preference": "technical", "topic": "programming"}
        
        result = await learner.learn_from_interaction(
            "How do I implement a binary search?",
            "Binary search is an efficient algorithm...",
            0.9,
            context,
            True
        )
        
        assert result != ""
        assert len(learner.patterns) == 1
        
        # Check pattern details
        pattern = list(learner.patterns.values())[0]
        assert pattern.user_intent == "information_request"
        assert pattern.success_rate == 0.9
        assert pattern.usage_count == 1
    
    @pytest.mark.asyncio
    async def test_extract_user_intent(self, learner):
        """Test user intent extraction."""
        intents = [
            ("How do I fix this bug?", "problem_solving"),
            ("Create a new project", "creation_request"),
            ("What is machine learning?", "information_request"),
            ("Thank you for your help", "gratitude"),
            ("Goodbye", "conversation_end"),
            ("Hello there", "general_inquiry")
        ]
        
        for message, expected_intent in intents:
            intent = await learner._extract_user_intent(message)
            assert intent == expected_intent
    
    @pytest.mark.asyncio
    async def test_find_best_pattern(self, learner):
        """Test finding best patterns for a context."""
        # Learn some patterns first
        context = {"user_preference": "technical", "topic": "programming"}
        await learner.learn_from_interaction(
            "How do I implement sorting?",
            "Here are several sorting algorithms...",
            0.8,
            context,
            True
        )
        
        # Find patterns
        patterns = await learner.find_best_pattern(
            "information_request",
            {"user_preference": "technical", "topic": "programming"},
            limit=5
        )
        
        assert len(patterns) > 0
        assert patterns[0].user_intent == "information_request"
    
    @pytest.mark.asyncio
    async def test_context_similarity(self, learner):
        """Test context similarity calculation."""
        pattern_context = {"user_preference": "technical", "topic": "programming"}
        current_context = {"user_preference": "technical", "topic": "web_development"}
        
        similarity = await learner._calculate_context_similarity(
            pattern_context, current_context
        )
        
        assert 0.0 <= similarity <= 1.0
        assert similarity > 0.0  # Should have some similarity
    
    @pytest.mark.asyncio
    async def test_get_pattern_statistics(self, learner):
        """Test pattern statistics generation."""
        # Learn some patterns first
        contexts = [
            {"user_preference": "technical", "topic": "programming"},
            {"user_preference": "casual", "topic": "general"},
            {"user_preference": "detailed", "topic": "machine_learning"}
        ]
        
        for context in contexts:
            await learner.learn_from_interaction(
                "Test message",
                "Test response",
                0.7,
                context,
                True
            )
        
        stats = await learner.get_pattern_statistics()
        assert stats["total_patterns"] == 3
        assert "average_success_rate" in stats
        assert "intent_distribution" in stats


class TestResponseQualityImprover:
    """Test response quality improvement functionality."""
    
    @pytest.fixture
    def improver(self, tmp_path):
        """Create a quality improver with temporary directory."""
        return ResponseQualityImprover(quality_dir=tmp_path)
    
    @pytest.mark.asyncio
    async def test_record_quality_metric(self, improver):
        """Test recording quality metrics."""
        metric_id = await improver.record_quality_metric(
            "session_123",
            "What is Python?",
            "Python is a programming language...",
            0.8,
            {"user_acknowledgment": True}
        )
        
        assert metric_id != ""
        assert len(improver.quality_metrics) == 1
        
        # Check metric details
        metric = improver.quality_metrics[0]
        assert metric.session_id == "session_123"
        assert metric.user_feedback == 0.8
        assert metric.quality_score > 0.0
    
    @pytest.mark.asyncio
    async def test_implicit_feedback_calculation(self, improver):
        """Test implicit feedback calculation."""
        metadata = {"user_acknowledgment": True, "conversation_continued": True}
        
        feedback = await improver._calculate_implicit_feedback(
            "How do neural networks work?",
            "Neural networks are inspired by biological neurons...",
            metadata
        )
        
        assert 0.0 <= feedback <= 1.0
        assert feedback > 0.5  # Should be positive with good metadata
    
    @pytest.mark.asyncio
    async def test_improvement_suggestions(self, improver):
        """Test improvement suggestion generation."""
        # Test low quality response
        suggestions = await improver._generate_improvement_suggestions(
            "What is AI?",
            "AI is technology.",
            0.3,  # Low quality
            {}
        )
        
        assert len(suggestions) > 0
        assert any("below acceptable threshold" in s for s in suggestions)
        
        # Test high quality response
        suggestions = await improver._generate_improvement_suggestions(
            "What is AI?",
            "Artificial Intelligence (AI) is a branch of computer science...",
            0.9,  # High quality
            {}
        )
        
        assert len(suggestions) > 0
        assert any("Maintain current" in s for s in suggestions)
    
    @pytest.mark.asyncio
    async def test_get_quality_insights(self, improver):
        """Test quality insights generation."""
        # Record some metrics first
        await improver.record_quality_metric(
            "session_1", "Test 1", "Response 1", 0.9, {}
        )
        await improver.record_quality_metric(
            "session_2", "Test 2", "Response 2", 0.3, {}
        )
        
        insights = await improver.get_quality_insights()
        assert insights["total_metrics"] == 2
        assert "average_quality" in insights
        assert "quality_distribution" in insights


class TestAdaptiveResponseGenerator:
    """Test adaptive response generation functionality."""
    
    @pytest.fixture
    def generator(self, tmp_path):
        """Create an adaptive response generator."""
        pattern_learner = ConversationPatternLearner(learning_dir=tmp_path)
        quality_improver = ResponseQualityImprover(quality_dir=tmp_path)
        return AdaptiveResponseGenerator(pattern_learner, quality_improver)
    
    @pytest.fixture
    def adaptive_context(self):
        """Create a sample adaptive context."""
        return AdaptiveContext(
            user_id="test_user",
            conversation_history=[
                {"role": "user", "content": "Hello", "metadata": {}},
                {"role": "assistant", "content": "Hi there!", "metadata": {}}
            ],
            learned_patterns=[],
            quality_history=[],
            user_preferences={"conversation_style": "casual"},
            context_embeddings={}
        )
    
    @pytest.mark.asyncio
    async def test_generate_adaptive_response(self, generator, adaptive_context):
        """Test adaptive response generation."""
        response = await generator.generate_adaptive_response(
            "How are you?",
            "I'm doing well, thank you for asking.",
            adaptive_context,
            "test_model"
        )
        
        assert "response" in response
        assert "adaptation_applied" in response
        assert "adaptation_strategy" in response
    
    @pytest.mark.asyncio
    async def test_conversation_context_analysis(self, generator, adaptive_context):
        """Test conversation context analysis."""
        analysis = await generator._analyze_conversation_context(adaptive_context)
        
        assert "conversation_length" in analysis
        assert "topic_consistency" in analysis
        assert "user_engagement" in analysis
    
    @pytest.mark.asyncio
    async def test_adaptation_strategy_generation(self, generator, adaptive_context):
        """Test adaptation strategy generation."""
        strategy = await generator._generate_adaptation_strategy(
            "information_request",
            [],
            {"user_engagement": 0.8},
            {"conversation_style": "casual"}
        )
        
        assert "style_adaptation" in strategy
        assert "detail_level" in strategy
        assert "formality" in strategy
    
    @pytest.mark.asyncio
    async def test_response_adaptations(self, generator):
        """Test various response adaptations."""
        # Test casual adaptation
        casual_response = await generator._make_response_casual("I will help you.")
        assert "I'll" in casual_response
        
        # Test formal adaptation
        formal_response = await generator._make_response_formal("I'll help you.")
        assert "I will" in formal_response
        
        # Test detail increase
        context = AdaptiveContext(
            user_id="test",
            conversation_history=[{"metadata": {"user_topics": {"topics": ["AI"]}}}],
            learned_patterns=[],
            quality_history=[],
            user_preferences={},
            context_embeddings={}
        )
        detailed_response = await generator._increase_response_detail("AI is interesting.", context)
        assert len(detailed_response) > len("AI is interesting.")
        
        # Test detail decrease
        decreased_response = await generator._decrease_response_detail("First sentence. Second sentence. Third sentence.")
        assert decreased_response.count('.') <= 2
        
        # Test engagement boost
        engaged_response = await generator._boost_engagement("This is helpful.")
        assert engaged_response.endswith("?")
        
        # Test context integration
        integrated_response = await generator._integrate_context("Here's the answer.", context)
        assert len(integrated_response) > len("Here's the answer.")


class TestATLESMachineLearning:
    """Test the main machine learning coordinator."""
    
    @pytest.fixture
    def ml_system(self, tmp_path):
        """Create a machine learning system with temporary directory."""
        return ATLESMachineLearning(learning_dir=tmp_path)
    
    @pytest.mark.asyncio
    async def test_learn_from_interaction(self, ml_system):
        """Test learning from interaction."""
        result = await ml_system.learn_from_interaction(
            "Test message",
            "Test response",
            0.8,
            {"context": "test"},
            "session_123",
            True
        )
        
        assert result["success"] is True
        assert "pattern_learned" in result
        assert "quality_recorded" in result
    
    @pytest.mark.asyncio
    async def test_generate_adaptive_response(self, ml_system):
        """Test adaptive response generation."""
        context = AdaptiveContext(
            user_id="test",
            conversation_history=[],
            learned_patterns=[],
            quality_history=[],
            user_preferences={},
            context_embeddings={}
        )
        
        response = await ml_system.generate_adaptive_response(
            "Test message",
            "Test response",
            context,
            "test_model"
        )
        
        assert "response" in response
        assert "adaptation_applied" in response
    
    @pytest.mark.asyncio
    async def test_get_learning_insights(self, ml_system):
        """Test learning insights generation."""
        insights = await ml_system.get_learning_insights()
        
        assert "pattern_learning" in insights
        assert "quality_improvement" in insights
        assert "system_status" in insights
    
    @pytest.mark.asyncio
    async def test_export_import_learning_data(self, ml_system, tmp_path):
        """Test learning data export and import."""
        # Learn some data first
        await ml_system.learn_from_interaction(
            "Test message",
            "Test response",
            0.8,
            {"context": "test"},
            "session_123",
            True
        )
        
        # Export data
        export_path = tmp_path / "export.pkl"
        export_success = await ml_system.export_learning_data(export_path)
        assert export_success is True
        
        # Import data
        import_success = await ml_system.import_learning_data(export_path)
        assert import_success is True


class TestIntegration:
    """Test integration between components."""
    
    @pytest.mark.asyncio
    async def test_full_learning_cycle(self, tmp_path):
        """Test a complete learning cycle."""
        ml_system = ATLESMachineLearning(learning_dir=tmp_path)
        
        # 1. Learn from interaction
        learning_result = await ml_system.learn_from_interaction(
            "How do I implement a binary search?",
            "Binary search is an efficient algorithm...",
            0.9,
            {"user_preference": "technical", "topic": "programming"},
            "session_1",
            True
        )
        assert learning_result["success"] is True
        
        # 2. Generate adaptive response
        context = AdaptiveContext(
            user_id="test_user",
            conversation_history=[
                {"role": "user", "content": "I need help with algorithms", "metadata": {}},
                {"role": "assistant", "content": "I can help with algorithms!", "metadata": {}}
            ],
            learned_patterns=[],
            quality_history=[],
            user_preferences={"conversation_style": "technical"},
            context_embeddings={}
        )
        
        adaptive_response = await ml_system.generate_adaptive_response(
            "What about merge sort?",
            "Merge sort is a divide-and-conquer algorithm...",
            context,
            "test_model"
        )
        assert adaptive_response["adaptation_applied"] is True
        
        # 3. Get insights
        insights = await ml_system.get_learning_insights()
        assert insights["pattern_learning"]["total_patterns"] > 0
        assert insights["quality_improvement"]["total_metrics"] > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
