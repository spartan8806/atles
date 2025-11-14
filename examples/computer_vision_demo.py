#!/usr/bin/env python3
"""
ATLES Computer Vision Foundation Demo

This script demonstrates the comprehensive computer vision capabilities
including image processing, object detection, and visual data interpretation.
"""

import asyncio
import logging
import sys
from pathlib import Path

# Add the atles package to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from atles.computer_vision import (
    ComputerVisionAPI, 
    ImageProcessor, 
    ObjectDetector, 
    ImageAnalyzer
)
from atles.brain import ATLESBrain

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


async def demo_image_processing():
    """Demonstrate basic image processing capabilities."""
    print("\n🔍 Image Processing Demo")
    print("=" * 50)
    
    # Initialize the image processor
    processor = ImageProcessor()
    
    # Create a sample image path (you would replace this with an actual image)
    sample_image_path = "sample_image.jpg"
    
    print(f"📸 Processing image: {sample_image_path}")
    
    # Check if sample image exists, if not create a placeholder
    if not Path(sample_image_path).exists():
        print("⚠️  Sample image not found. Creating a placeholder for demonstration...")
        # In a real scenario, you would have actual images to process
        print("💡 To test with real images, place image files in the examples directory")
        return
    
    try:
        # Load image
        print("🔄 Loading image...")
        image = await processor.load_image(sample_image_path)
        if image is not None:
            print(f"✅ Image loaded successfully - Shape: {image.shape}")
            
            # Extract features
            print("🔍 Extracting image features...")
            features = await processor.extract_features(image)
            print(f"📊 Features extracted: {len(features)} properties")
            
            # Apply filters
            print("🎨 Applying filters...")
            filters_to_test = ["blur", "sharpen", "grayscale", "sepia"]
            
            for filter_type in filters_to_test:
                print(f"  - Applying {filter_type} filter...")
                filtered_image = await processor.apply_filters(image, filter_type)
                print(f"    ✅ {filter_type} filter applied")
            
            # Resize image
            print("📏 Resizing image...")
            resized = await processor.resize_image(image, (256, 256))
            print(f"✅ Image resized to 256x256")
            
        else:
            print("❌ Failed to load image")
            
    except Exception as e:
        print(f"❌ Error in image processing demo: {e}")


async def demo_object_detection():
    """Demonstrate object detection capabilities."""
    print("\n🎯 Object Detection Demo")
    print("=" * 50)
    
    # Initialize the object detector
    detector = ObjectDetector()
    
    print("🤖 Loading object detection model...")
    try:
        # Load a lightweight model for demonstration
        success = await detector.load_model("microsoft/resnet-50")
        if success:
            print("✅ Object detection model loaded successfully")
            
            # Create a sample image path
            sample_image_path = "sample_image.jpg"
            
            if Path(sample_image_path).exists():
                print(f"🔍 Detecting objects in: {sample_image_path}")
                
                # Load image for detection
                processor = ImageProcessor()
                image = await processor.load_image(sample_image_path)
                
                if image is not None:
                    # Detect objects
                    detections = await detector.detect_objects(image, confidence_threshold=0.3)
                    
                    if "detections" in detections:
                        print(f"🎯 Detected {len(detections['detections'])} objects:")
                        for i, detection in enumerate(detections['detections'][:5]):  # Show top 5
                            print(f"  {i+1}. {detection['category']} (confidence: {detection['confidence']:.2f})")
                    else:
                        print("❌ No objects detected or error occurred")
                        
                    # Draw detections on image
                    print("🎨 Drawing detection results...")
                    annotated_image = await detector.draw_detections(image, detections.get('detections', []))
                    print("✅ Detection annotations added to image")
                    
                else:
                    print("❌ Failed to load image for object detection")
            else:
                print("⚠️  Sample image not found. Skipping object detection demo.")
                
        else:
            print("❌ Failed to load object detection model")
            
    except Exception as e:
        print(f"❌ Error in object detection demo: {e}")


async def demo_image_analysis():
    """Demonstrate comprehensive image analysis."""
    print("\n📊 Image Analysis Demo")
    print("=" * 50)
    
    # Initialize the image analyzer
    analyzer = ImageAnalyzer()
    
    # Create a sample image path
    sample_image_path = "sample_image.jpg"
    
    if Path(sample_image_path).exists():
        print(f"🔍 Analyzing image: {sample_image_path}")
        
        try:
            # Perform comprehensive analysis
            analysis = await analyzer.analyze_image(sample_image_path)
            
            if "error" not in analysis:
                print("✅ Image analysis completed successfully")
                
                # Display analysis results
                if "basic_features" in analysis:
                    features = analysis["basic_features"]
                    print(f"📏 Image dimensions: {features.get('shape', 'Unknown')}")
                    print(f"🎨 Color channels: {features.get('channels', 'Unknown')}")
                    print(f"💾 File size: {features.get('size_bytes', 0) / 1024:.1f} KB")
                
                if "object_detection" in analysis:
                    detections = analysis["object_detection"]
                    print(f"🎯 Objects detected: {detections.get('total_objects', 0)}")
                
                if "composition_analysis" in analysis:
                    composition = analysis["composition_analysis"]
                    if "rule_of_thirds" in composition:
                        balance = composition["rule_of_thirds"]["composition_balance"]
                        print(f"📐 Composition balance: {balance:.2f}")
                    
                    if "color_harmony" in composition:
                        hue_var = composition["color_harmony"]["hue_variance"]
                        print(f"🌈 Color diversity: {'High' if hue_var > 5000 else 'Low'}")
                
                if "summary" in analysis:
                    print(f"\n📝 Analysis Summary:")
                    print(f"   {analysis['summary']}")
                    
            else:
                print(f"❌ Analysis failed: {analysis['error']}")
                
        except Exception as e:
            print(f"❌ Error in image analysis demo: {e}")
    else:
        print("⚠️  Sample image not found. Skipping image analysis demo.")


async def demo_computer_vision_api():
    """Demonstrate the main Computer Vision API."""
    print("\n🚀 Computer Vision API Demo")
    print("=" * 50)
    
    # Initialize the main API
    cv_api = ComputerVisionAPI()
    
    # Get system information
    print("ℹ️  Getting system information...")
    try:
        system_info = await cv_api.get_system_info()
        print(f"✅ OpenCV version: {system_info['opencv_version']}")
        print(f"✅ Pillow version: {system_info['pillow_version']}")
        print(f"✅ PyTorch version: {system_info['torch_version']}")
        print(f"✅ Supported formats: {', '.join(system_info['supported_formats'])}")
        print(f"✅ Available operations: {', '.join(system_info['available_operations'])}")
        
    except Exception as e:
        print(f"❌ Error getting system info: {e}")
    
    # Test batch processing
    print("\n🔄 Testing batch processing capabilities...")
    sample_images = ["sample_image.jpg", "another_image.jpg"]
    
    # Filter out non-existent images
    existing_images = [img for img in sample_images if Path(img).exists()]
    
    if existing_images:
        operations = ["features", "detect"]
        print(f"📋 Processing {len(existing_images)} images with operations: {operations}")
        
        try:
            batch_results = await cv_api.batch_process(existing_images, operations)
            print(f"✅ Batch processing completed for {len(batch_results)} images")
            
            for result in batch_results:
                if "error" not in result:
                    print(f"  📸 {result['image_path']}: Success")
                else:
                    print(f"  ❌ {result['image_path']}: {result['error']}")
                    
        except Exception as e:
            print(f"❌ Error in batch processing: {e}")
    else:
        print("⚠️  No sample images found. Skipping batch processing demo.")


async def demo_atles_brain_integration():
    """Demonstrate integration with ATLES Brain."""
    print("\n🧠 ATLES Brain Integration Demo")
    print("=" * 50)
    
    try:
        # Initialize ATLES Brain
        print("🧠 Initializing ATLES Brain...")
        brain = ATLESBrain()
        print("✅ ATLES Brain initialized successfully")
        
        # Test computer vision methods
        sample_image_path = "sample_image.jpg"
        
        if Path(sample_image_path).exists():
            print(f"🔍 Testing image processing through ATLES Brain...")
            
            # Test image processing
            operations = ["features", "detect"]
            result = await brain.process_image(sample_image_path, operations)
            
            if result["success"]:
                print("✅ Image processing successful through ATLES Brain")
                print(f"   Operations performed: {result['operations']}")
            else:
                print(f"❌ Image processing failed: {result['error']}")
            
            # Test object detection
            print("🎯 Testing object detection through ATLES Brain...")
            detection_result = await brain.detect_objects(sample_image_path)
            
            if detection_result["success"]:
                print("✅ Object detection successful through ATLES Brain")
                obj_count = detection_result["result"].get("total_objects", 0)
                print(f"   Objects detected: {obj_count}")
            else:
                print(f"❌ Object detection failed: {detection_result['error']}")
                
        else:
            print("⚠️  Sample image not found. Skipping ATLES Brain integration demo.")
            
    except Exception as e:
        print(f"❌ Error in ATLES Brain integration demo: {e}")


async def create_sample_image():
    """Create a sample image for demonstration purposes."""
    print("\n🎨 Creating Sample Image")
    print("=" * 50)
    
    try:
        from PIL import Image, ImageDraw, ImageFont
        
        # Create a simple sample image
        width, height = 400, 300
        image = Image.new('RGB', (width, height), color='lightblue')
        draw = ImageDraw.Draw(image)
        
        # Add some shapes and text
        draw.rectangle([50, 50, 150, 150], fill='red', outline='black')
        draw.ellipse([200, 50, 300, 150], fill='green', outline='black')
        draw.polygon([(100, 200), (150, 250), (200, 200)], fill='yellow', outline='black')
        
        # Add text
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((50, 270), "ATLES Computer Vision Demo", fill='black', font=font)
        
        # Save the image
        sample_path = "sample_image.jpg"
        image.save(sample_path, "JPEG")
        print(f"✅ Sample image created: {sample_path}")
        print(f"   Dimensions: {width}x{height} pixels")
        print(f"   Format: JPEG")
        
    except Exception as e:
        print(f"❌ Error creating sample image: {e}")


async def main():
    """Main demonstration function."""
    print("🚀 ATLES Computer Vision Foundation Demo")
    print("=" * 60)
    print("This demo showcases the comprehensive computer vision capabilities")
    print("including image processing, object detection, and visual analysis.")
    print("=" * 60)
    
    # Create a sample image for demonstration
    await create_sample_image()
    
    # Run all demos
    await demo_image_processing()
    await demo_object_detection()
    await demo_image_analysis()
    await demo_computer_vision_api()
    await demo_atles_brain_integration()
    
    print("\n🎉 Computer Vision Demo Completed!")
    print("=" * 60)
    print("Key Features Demonstrated:")
    print("✅ Image loading and processing")
    print("✅ Feature extraction and analysis")
    print("✅ Filter application (blur, sharpen, grayscale, sepia)")
    print("✅ Image resizing and manipulation")
    print("✅ Object detection and recognition")
    print("✅ Composition and color analysis")
    print("✅ Batch processing capabilities")
    print("✅ Integration with ATLES Brain")
    print("\n💡 To use with your own images:")
    print("   1. Place image files in the examples directory")
    print("   2. Update the image paths in the demo functions")
    print("   3. Run: python computer_vision_demo.py")


if __name__ == "__main__":
    # Run the demo
    asyncio.run(main())
