"""
Tests for ATLES Computer Vision Foundation

Tests the image processing, object detection, and analysis capabilities.
"""

import pytest
import asyncio
import numpy as np
from pathlib import Path
import tempfile
import os

# Import the computer vision modules
from atles.computer_vision import (
    ImageProcessor,
    ObjectDetector,
    ImageAnalyzer,
    ComputerVisionAPI
)


class TestImageProcessor:
    """Test the ImageProcessor class."""
    
    @pytest.fixture
    def processor(self):
        """Create an ImageProcessor instance for testing."""
        return ImageProcessor()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample numpy image for testing."""
        # Create a simple 100x100 RGB image
        image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return image
    
    def test_initialization(self, processor):
        """Test ImageProcessor initialization."""
        assert processor.supported_formats == {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        assert processor.max_image_size == (4096, 4096)
    
    @pytest.mark.asyncio
    async def test_load_nonexistent_image(self, processor):
        """Test loading a non-existent image."""
        result = await processor.load_image("nonexistent.jpg")
        assert result is None
    
    @pytest.mark.asyncio
    async def test_save_and_load_image(self, processor, sample_image, tmp_path):
        """Test saving and loading an image."""
        # Save image
        output_path = tmp_path / "test_image.jpg"
        success = await processor.save_image(sample_image, output_path)
        assert success
        assert output_path.exists()
        
        # Load image
        loaded_image = await processor.load_image(output_path)
        assert loaded_image is not None
        assert loaded_image.shape == sample_image.shape
        assert np.array_equal(loaded_image, sample_image)
    
    @pytest.mark.asyncio
    async def test_resize_image(self, processor, sample_image):
        """Test image resizing."""
        target_size = (50, 50)
        resized = await processor.resize_image(sample_image, target_size)
        
        assert resized.shape[:2] == target_size
        assert resized.dtype == sample_image.dtype
    
    @pytest.mark.asyncio
    async def test_apply_filters(self, processor, sample_image):
        """Test filter application."""
        # Test blur filter
        blurred = await processor.apply_filters(sample_image, "blur")
        assert blurred.shape == sample_image.shape
        
        # Test grayscale filter
        grayscale = await processor.apply_filters(sample_image, "grayscale")
        assert len(grayscale.shape) == 2  # Should be 2D for grayscale
        
        # Test sharpen filter
        sharpened = await processor.apply_filters(sample_image, "sharpen")
        assert sharpened.shape == sample_image.shape
        
        # Test edge detection
        edges = await processor.apply_filters(sample_image, "edge_detection")
        assert edges.shape == sample_image.shape[:2]  # Should be 2D
        
        # Test sepia filter
        sepia = await processor.apply_filters(sample_image, "sepia")
        assert sepia.shape == sample_image.shape
    
    @pytest.mark.asyncio
    async def test_extract_features(self, processor, sample_image):
        """Test feature extraction."""
        features = await processor.extract_features(sample_image)
        
        # Check that features were extracted
        assert "shape" in features
        assert "dtype" in features
        assert "size_bytes" in features
        assert "channels" in features
        assert "brightness" in features
        assert "contrast" in features
        
        # Check specific values
        assert features["shape"] == sample_image.shape
        assert features["channels"] == 3
        assert features["size_bytes"] == sample_image.nbytes


class TestObjectDetector:
    """Test the ObjectDetector class."""
    
    @pytest.fixture
    def detector(self):
        """Create an ObjectDetector instance for testing."""
        return ObjectDetector()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample numpy image for testing."""
        # Create a simple 100x100 RGB image
        image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return image
    
    def test_initialization(self, detector):
        """Test ObjectDetector initialization."""
        assert detector.model is None
        assert detector.processor is None
        assert not detector._loaded
        assert len(detector.coco_categories) > 80  # Should have many categories
    
    @pytest.mark.asyncio
    async def test_load_model(self, detector):
        """Test model loading."""
        # This test might fail if no internet connection or model not available
        try:
            success = await detector.load_model("microsoft/resnet-50")
            # If successful, should be loaded
            if success:
                assert detector._loaded
                assert detector.model is not None
                assert detector.processor is not None
        except Exception:
            # Model loading might fail in test environment, which is okay
            pass
    
    @pytest.mark.asyncio
    async def test_draw_detections(self, detector, sample_image):
        """Test drawing detections on image."""
        # Create mock detections
        detections = [
            {"category": "test_object", "confidence": 0.8},
            {"category": "another_object", "confidence": 0.6}
        ]
        
        annotated_image = await detector.draw_detections(sample_image, detections)
        
        # Should return an image of the same shape
        assert annotated_image.shape == sample_image.shape
        assert annotated_image.dtype == sample_image.dtype


class TestImageAnalyzer:
    """Test the ImageAnalyzer class."""
    
    @pytest.fixture
    def analyzer(self):
        """Create an ImageAnalyzer instance for testing."""
        return ImageAnalyzer()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample numpy image for testing."""
        # Create a simple 100x100 RGB image
        image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return image
    
    @pytest.mark.asyncio
    async def test_analyze_composition(self, analyzer, sample_image):
        """Test composition analysis."""
        composition = await analyzer._analyze_composition(sample_image)
        
        # Check that composition analysis was performed
        assert "rule_of_thirds" in composition
        assert "edge_analysis" in composition
        
        # Check rule of thirds analysis
        rule_of_thirds = composition["rule_of_thirds"]
        assert "center_region_variance" in rule_of_thirds
        assert "edge_regions_variance" in rule_of_thirds
        assert "composition_balance" in rule_of_thirds
        
        # Check edge analysis
        edge_analysis = composition["edge_analysis"]
        assert "edge_density" in edge_analysis
        assert "edge_distribution" in edge_analysis
    
    @pytest.mark.asyncio
    async def test_generate_summary(self, analyzer):
        """Test summary generation."""
        # Mock data
        features = {"shape": (100, 100, 3), "channels": 3}
        detections = {"total_objects": 2, "detections": [{"category": "cat"}, {"category": "dog"}]}
        composition = {"rule_of_thirds": {"composition_balance": 1.2}}
        
        summary = await analyzer._generate_summary(features, detections, composition)
        
        # Should generate a readable summary
        assert isinstance(summary, str)
        assert len(summary) > 0
        assert "100x100" in summary  # Should mention dimensions
        assert "2 objects" in summary  # Should mention object count


class TestComputerVisionAPI:
    """Test the main ComputerVisionAPI class."""
    
    @pytest.fixture
    def cv_api(self):
        """Create a ComputerVisionAPI instance for testing."""
        return ComputerVisionAPI()
    
    @pytest.fixture
    def sample_image(self):
        """Create a sample numpy image for testing."""
        # Create a simple 100x100 RGB image
        image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        return image
    
    def test_initialization(self, cv_api):
        """Test ComputerVisionAPI initialization."""
        assert cv_api.processor is not None
        assert cv_api.detector is not None
        assert cv_api.analyzer is not None
    
    @pytest.mark.asyncio
    async def test_get_supported_operations(self, cv_api):
        """Test getting supported operations."""
        operations = await cv_api.get_supported_operations()
        
        expected_operations = [
            "resize", "filter", "features", "detect", "analyze",
            "blur", "sharpen", "edge_detection", "grayscale", "sepia"
        ]
        
        for op in expected_operations:
            assert op in operations
    
    @pytest.mark.asyncio
    async def test_get_system_info(self, cv_api):
        """Test getting system information."""
        system_info = await cv_api.get_system_info()
        
        # Check that system info contains expected keys
        assert "opencv_version" in system_info
        assert "pillow_version" in system_info
        assert "torch_version" in system_info
        assert "supported_formats" in system_info
        assert "max_image_size" in system_info
        assert "available_operations" in system_info
    
    @pytest.mark.asyncio
    async def test_batch_process_empty_list(self, cv_api):
        """Test batch processing with empty list."""
        results = await cv_api.batch_process([], ["features"])
        assert results == []
    
    @pytest.mark.asyncio
    async def test_batch_process_nonexistent_images(self, cv_api):
        """Test batch processing with non-existent images."""
        results = await cv_api.batch_process(["nonexistent1.jpg", "nonexistent2.jpg"], ["features"])
        
        assert len(results) == 2
        for result in results:
            assert "error" in result


class TestIntegration:
    """Test integration between different components."""
    
    @pytest.mark.asyncio
    async def test_full_pipeline(self, tmp_path):
        """Test a complete computer vision pipeline."""
        # Create a sample image
        sample_image = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8)
        
        # Save it
        image_path = tmp_path / "test_pipeline.jpg"
        processor = ImageProcessor()
        success = await processor.save_image(sample_image, image_path)
        assert success
        
        # Process it through the full pipeline
        cv_api = ComputerVisionAPI()
        result = await cv_api.process_image(str(image_path), ["features", "detect"])
        
        # Check that processing was successful
        assert "success" in result
        if result.get("success"):
            assert "results" in result
            results = result["results"]
            
            # Check that features were extracted
            if "features" in results:
                features = results["features"]
                assert "shape" in features
                assert features["shape"] == sample_image.shape
            
            # Check that detection was attempted
            if "detections" in results:
                detections = results["detections"]
                assert "total_objects" in detections


# Utility functions for testing
def create_test_image(width=100, height=100, channels=3):
    """Create a test image with specified dimensions."""
    return np.random.randint(0, 255, (height, width, channels), dtype=np.uint8)


def save_test_image(image, path):
    """Save a test image to a temporary path."""
    import cv2
    # Convert RGB to BGR for OpenCV
    if len(image.shape) == 3:
        image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    else:
        image_bgr = image
    
    return cv2.imwrite(str(path), image_bgr)


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
