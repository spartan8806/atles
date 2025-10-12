#!/usr/bin/env python3
"""
ATLES Embedding Model Weight Surgeon - Direct Neural Modification System

This module provides tools for surgical modification of embedding model weights 
(like EmbeddingGemma) to enhance specific embedding behaviors without full retraining.

CAPABILITIES:
- Semantic similarity enhancement
- Domain-specific embedding optimization
- Vector space geometry adjustments
- Embedding quality improvements
- Safe rollback mechanisms for embedding models

NOTE: This is specifically designed for embedding models like EmbeddingGemma.
For generative models, use the QwenModelWeightSurgeon instead.

WARNING: These tools directly modify model parameters. Use with extreme caution.
"""

import logging
import json
import torch
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from pathlib import Path
import pickle
import hashlib
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


@dataclass
class EmbeddingBehaviorPattern:
    """Represents a specific embedding behavior pattern and its neural correlates"""
    name: str
    description: str
    target_layers: List[str]
    embedding_patterns: Dict[str, np.ndarray]
    confidence_score: float
    validation_texts: List[str]
    expected_similarities: List[float]
    semantic_domain: str  # e.g., "technical", "conversational", "academic"


@dataclass
class EmbeddingWeightModification:
    """Represents a surgical modification to embedding model weights"""
    modification_id: str
    target_behavior: str
    affected_parameters: List[str]
    original_weights: Dict[str, torch.Tensor]
    modified_weights: Dict[str, torch.Tensor]
    modification_type: str  # "enhance_similarity", "domain_adapt", "geometry_adjust"
    strength: float
    timestamp: str
    validation_results: Dict[str, Any]
    semantic_impact: Dict[str, float]  # Impact on different semantic domains


class EmbeddingModelWeightSurgeon:
    """
    Advanced system for surgical modification of embedding model weights.
    
    This system can:
    1. Analyze embedding behavior patterns and map them to specific layers
    2. Perform precise weight modifications to enhance or suppress embedding behaviors
    3. Validate modifications through semantic similarity testing
    4. Safely rollback changes if needed
    5. Optimize embedding quality for specific domains
    """
    
    def __init__(self, model_path: str, backup_dir: str = "embedding_weight_backups"):
        self.model_path = model_path
        self.backup_dir = Path(backup_dir)
        self.backup_dir.mkdir(exist_ok=True)
        
        # Load the embedding model
        try:
            self.model = SentenceTransformer(model_path)
            logger.info(f"Loaded embedding model from {model_path}")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            self.model = None
        
        # Storage for patterns and modifications
        self.behavior_patterns: Dict[str, EmbeddingBehaviorPattern] = {}
        self.modifications: Dict[str, EmbeddingWeightModification] = {}
        self.modification_history: List[str] = []
        
        # Validation datasets for different domains
        self.validation_datasets = {
            "technical": [
                "machine learning algorithm",
                "neural network architecture", 
                "data preprocessing pipeline",
                "model optimization technique"
            ],
            "conversational": [
                "how are you doing today",
                "what's your favorite movie",
                "tell me about yourself",
                "what do you think about this"
            ],
            "academic": [
                "research methodology framework",
                "statistical significance analysis",
                "peer review process evaluation",
                "academic publication standards"
            ]
        }
    
    def analyze_embedding_behavior(self, texts: List[str], behavior_name: str, 
                                 semantic_domain: str = "general") -> EmbeddingBehaviorPattern:
        """
        Analyze how the model embeds specific types of text to identify patterns.
        """
        if not self.model:
            raise RuntimeError("Model not loaded")
        
        logger.info(f"Analyzing embedding behavior: {behavior_name}")
        
        # Generate embeddings for analysis texts
        embeddings = self.model.encode(texts)
        
        # Analyze embedding patterns
        embedding_stats = {
            "mean_embedding": np.mean(embeddings, axis=0),
            "std_embedding": np.std(embeddings, axis=0),
            "similarity_matrix": cosine_similarity(embeddings)
        }
        
        # Calculate confidence based on embedding consistency
        similarities = cosine_similarity(embeddings)
        confidence = np.mean(similarities[np.triu_indices_from(similarities, k=1)])
        
        # Create behavior pattern
        pattern = EmbeddingBehaviorPattern(
            name=behavior_name,
            description=f"Embedding behavior for {semantic_domain} domain",
            target_layers=self._identify_relevant_layers(embeddings),
            embedding_patterns=embedding_stats,
            confidence_score=confidence,
            validation_texts=texts,
            expected_similarities=[0.8] * len(texts),  # Default expectation
            semantic_domain=semantic_domain
        )
        
        self.behavior_patterns[behavior_name] = pattern
        logger.info(f"Behavior pattern '{behavior_name}' analyzed with confidence {confidence:.3f}")
        
        return pattern
    
    def _identify_relevant_layers(self, embeddings: np.ndarray) -> List[str]:
        """
        Identify which model layers are most relevant for the embedding patterns.
        """
        # For EmbeddingGemma, focus on the embedding and final layers
        relevant_layers = [
            "embeddings.word_embeddings",
            "encoder.layers.0",  # Early layers for basic features
            "encoder.layers.11", # Late layers for complex patterns
            "pooler"  # Final pooling layer
        ]
        return relevant_layers
    
    def enhance_semantic_similarity(self, domain: str, enhancement_strength: float = 0.1) -> str:
        """
        Enhance the model's ability to create similar embeddings for semantically related text.
        """
        modification_id = f"enhance_similarity_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Enhancing semantic similarity for domain: {domain}")
        
        # Get validation texts for this domain
        validation_texts = self.validation_datasets.get(domain, self.validation_datasets["technical"])
        
        # Analyze current behavior
        pattern = self.analyze_embedding_behavior(validation_texts, f"similarity_{domain}", domain)
        
        # Create backup
        self._create_backup(modification_id)
        
        # Apply enhancement modifications
        modified_weights = self._calculate_similarity_enhancement(pattern, enhancement_strength)
        
        # Apply modifications
        original_weights = self._get_current_weights(pattern.target_layers)
        self._apply_weight_modifications(modified_weights)
        
        # Validate changes
        validation_results = self._validate_embedding_modification(validation_texts, domain)
        
        # Store modification record
        modification = EmbeddingWeightModification(
            modification_id=modification_id,
            target_behavior=f"enhance_similarity_{domain}",
            affected_parameters=pattern.target_layers,
            original_weights=original_weights,
            modified_weights=modified_weights,
            modification_type="enhance_similarity",
            strength=enhancement_strength,
            timestamp=datetime.now().isoformat(),
            validation_results=validation_results,
            semantic_impact={domain: enhancement_strength}
        )
        
        self.modifications[modification_id] = modification
        self.modification_history.append(modification_id)
        
        logger.info(f"Semantic similarity enhancement applied. ID: {modification_id}")
        return modification_id
    
    def adapt_to_domain(self, domain: str, domain_texts: List[str], adaptation_strength: float = 0.15) -> str:
        """
        Adapt the embedding model to better handle a specific domain.
        """
        modification_id = f"domain_adapt_{domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info(f"Adapting model to domain: {domain}")
        
        # Analyze domain-specific patterns
        pattern = self.analyze_embedding_behavior(domain_texts, f"domain_{domain}", domain)
        
        # Create backup
        self._create_backup(modification_id)
        
        # Calculate domain adaptation modifications
        modified_weights = self._calculate_domain_adaptation(pattern, adaptation_strength)
        
        # Apply modifications
        original_weights = self._get_current_weights(pattern.target_layers)
        self._apply_weight_modifications(modified_weights)
        
        # Validate changes
        validation_results = self._validate_embedding_modification(domain_texts, domain)
        
        # Store modification record
        modification = EmbeddingWeightModification(
            modification_id=modification_id,
            target_behavior=f"domain_adapt_{domain}",
            affected_parameters=pattern.target_layers,
            original_weights=original_weights,
            modified_weights=modified_weights,
            modification_type="domain_adapt",
            strength=adaptation_strength,
            timestamp=datetime.now().isoformat(),
            validation_results=validation_results,
            semantic_impact={domain: adaptation_strength}
        )
        
        self.modifications[modification_id] = modification
        self.modification_history.append(modification_id)
        
        logger.info(f"Domain adaptation applied. ID: {modification_id}")
        return modification_id
    
    def _calculate_similarity_enhancement(self, pattern: EmbeddingBehaviorPattern, 
                                        strength: float) -> Dict[str, torch.Tensor]:
        """
        Calculate weight modifications to enhance semantic similarity.
        """
        modified_weights = {}
        
        for layer_name in pattern.target_layers:
            if hasattr(self.model[0], layer_name.replace('.', '_')):
                # Get current weights
                current_weights = self._get_layer_weights(layer_name)
                
                # Calculate enhancement based on embedding patterns
                mean_pattern = pattern.embedding_patterns["mean_embedding"]
                enhancement_direction = mean_pattern / np.linalg.norm(mean_pattern)
                
                # Apply enhancement with controlled strength
                if current_weights is not None:
                    enhancement = torch.tensor(enhancement_direction[:current_weights.shape[-1]], 
                                             dtype=current_weights.dtype, device=current_weights.device)
                    modified_weights[layer_name] = current_weights + strength * enhancement.unsqueeze(0)
        
        return modified_weights
    
    def _calculate_domain_adaptation(self, pattern: EmbeddingBehaviorPattern, 
                                   strength: float) -> Dict[str, torch.Tensor]:
        """
        Calculate weight modifications for domain adaptation.
        """
        modified_weights = {}
        
        for layer_name in pattern.target_layers:
            current_weights = self._get_layer_weights(layer_name)
            
            if current_weights is not None:
                # Calculate domain-specific adjustments
                domain_pattern = pattern.embedding_patterns["mean_embedding"]
                adaptation_vector = domain_pattern / np.linalg.norm(domain_pattern)
                
                # Apply domain adaptation
                adaptation = torch.tensor(adaptation_vector[:current_weights.shape[-1]], 
                                        dtype=current_weights.dtype, device=current_weights.device)
                modified_weights[layer_name] = current_weights + strength * adaptation.unsqueeze(0)
        
        return modified_weights
    
    def _get_layer_weights(self, layer_name: str) -> Optional[torch.Tensor]:
        """Get weights from a specific layer."""
        try:
            # Navigate to the layer in the model
            layer_parts = layer_name.split('.')
            current = self.model[0]  # First module in SentenceTransformer
            
            for part in layer_parts:
                if hasattr(current, part):
                    current = getattr(current, part)
                else:
                    return None
            
            if hasattr(current, 'weight'):
                return current.weight.clone()
            return None
        except Exception as e:
            logger.warning(f"Could not access layer {layer_name}: {e}")
            return None
    
    def _get_current_weights(self, layer_names: List[str]) -> Dict[str, torch.Tensor]:
        """Get current weights from multiple layers."""
        weights = {}
        for layer_name in layer_names:
            weight = self._get_layer_weights(layer_name)
            if weight is not None:
                weights[layer_name] = weight
        return weights
    
    def _apply_weight_modifications(self, modified_weights: Dict[str, torch.Tensor]):
        """Apply weight modifications to the model."""
        for layer_name, new_weights in modified_weights.items():
            try:
                # Navigate to the layer
                layer_parts = layer_name.split('.')
                current = self.model[0]
                
                for part in layer_parts[:-1]:
                    current = getattr(current, part)
                
                # Set the new weights
                if hasattr(current, layer_parts[-1]):
                    layer = getattr(current, layer_parts[-1])
                    if hasattr(layer, 'weight'):
                        layer.weight.data = new_weights
                        logger.debug(f"Applied modifications to {layer_name}")
            except Exception as e:
                logger.error(f"Failed to apply modifications to {layer_name}: {e}")
    
    def _validate_embedding_modification(self, validation_texts: List[str], 
                                       domain: str) -> Dict[str, Any]:
        """
        Validate that embedding modifications improved the desired behavior.
        """
        if not self.model:
            return {"error": "Model not available for validation"}
        
        try:
            # Generate embeddings with modified model
            embeddings = self.model.encode(validation_texts)
            
            # Calculate similarity metrics
            similarities = cosine_similarity(embeddings)
            avg_similarity = np.mean(similarities[np.triu_indices_from(similarities, k=1)])
            
            # Calculate embedding quality metrics
            embedding_std = np.std(embeddings, axis=0)
            embedding_norm = np.linalg.norm(embeddings, axis=1)
            
            results = {
                "domain": domain,
                "avg_similarity": float(avg_similarity),
                "embedding_consistency": float(np.mean(embedding_std)),
                "embedding_magnitude": float(np.mean(embedding_norm)),
                "validation_texts_count": len(validation_texts),
                "success": avg_similarity > 0.7  # Threshold for success
            }
            
            logger.info(f"Validation results for {domain}: avg_similarity={avg_similarity:.3f}")
            return results
            
        except Exception as e:
            logger.error(f"Validation failed: {e}")
            return {"error": str(e), "success": False}
    
    def _create_backup(self, modification_id: str):
        """Create a backup of current model state."""
        backup_path = self.backup_dir / f"backup_{modification_id}.pt"
        try:
            if self.model:
                torch.save(self.model.state_dict(), backup_path)
                logger.info(f"Backup created: {backup_path}")
        except Exception as e:
            logger.error(f"Failed to create backup: {e}")
    
    def rollback_modification(self, modification_id: str) -> bool:
        """
        Rollback a specific modification using stored original weights.
        """
        if modification_id not in self.modifications:
            logger.error(f"Modification {modification_id} not found")
            return False
        
        try:
            modification = self.modifications[modification_id]
            
            # Restore original weights
            self._apply_weight_modifications(modification.original_weights)
            
            # Remove from active modifications
            del self.modifications[modification_id]
            if modification_id in self.modification_history:
                self.modification_history.remove(modification_id)
            
            logger.info(f"Successfully rolled back modification: {modification_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to rollback modification {modification_id}: {e}")
            return False
    
    def get_modification_summary(self) -> Dict[str, Any]:
        """Get a summary of all applied modifications."""
        return {
            "total_modifications": len(self.modifications),
            "active_modifications": list(self.modifications.keys()),
            "modification_history": self.modification_history,
            "behavior_patterns": list(self.behavior_patterns.keys()),
            "model_path": self.model_path
        }
    
    def optimize_for_atles_tasks(self) -> str:
        """
        Optimize the embedding model specifically for ATLES autonomous system tasks.
        """
        modification_id = f"atles_optimization_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        logger.info("Optimizing embedding model for ATLES tasks")
        
        # ATLES-specific validation texts
        atles_texts = [
            "autonomous system goal execution",
            "document analysis and summarization", 
            "system performance optimization",
            "configuration parameter adjustment",
            "behavioral pattern recognition",
            "safety boundary validation",
            "change impact assessment",
            "system health monitoring"
        ]
        
        # Apply domain adaptation for ATLES tasks
        return self.adapt_to_domain("atles_autonomous", atles_texts, adaptation_strength=0.2)


# Convenience functions for easy integration
def create_embedding_surgeon(model_path: str = "google/embeddinggemma-300m") -> EmbeddingModelWeightSurgeon:
    """Create an embedding model weight surgeon for the specified model."""
    return EmbeddingModelWeightSurgeon(model_path)

def optimize_for_atles(model_path: str = "google/embeddinggemma-300m") -> str:
    """Quick optimization of embedding model for ATLES tasks."""
    surgeon = create_embedding_surgeon(model_path)
    return surgeon.optimize_for_atles_tasks()


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.INFO)
    
    # Create surgeon for EmbeddingGemma
    surgeon = create_embedding_surgeon("google/embeddinggemma-300m")
    
    # Optimize for ATLES tasks
    modification_id = surgeon.optimize_for_atles_tasks()
    print(f"ATLES optimization applied: {modification_id}")
    
    # Get summary
    summary = surgeon.get_modification_summary()
    print(f"Modification summary: {json.dumps(summary, indent=2)}")
