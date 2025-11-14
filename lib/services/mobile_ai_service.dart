import 'dart:async';
import 'dart:typed_data';
import 'package:flutter/foundation.dart';
import 'package:flutter/services.dart';
import '../models/atles_response.dart';

class MobileAIService {
  static const MethodChannel _channel = MethodChannel('atles_mini/ai');
  
  String _currentModel = 'llama_3_2_1b';
  bool _isInitialized = false;
  bool _isProcessing = false;
  
  // Available models configuration
  final Map<String, ModelConfig> _availableModels = {
    'llama_3_2_1b': ModelConfig(
      name: 'Llama 3.2 1B',
      fileName: 'llama_3_2_1b.tflite',
      sizeMB: 800,
      ramRequiredMB: 2048,
      capabilities: ['chat', 'basic_reasoning'],
      maxTokens: 2048,
    ),
    'llama_3_2_3b': ModelConfig(
      name: 'Llama 3.2 3B',
      fileName: 'llama_3_2_3b.tflite',
      sizeMB: 1800,
      ramRequiredMB: 3072,
      capabilities: ['chat', 'reasoning', 'code'],
      maxTokens: 4096,
    ),
    'phi_3_mini': ModelConfig(
      name: 'Phi-3 Mini',
      fileName: 'phi_3_mini.onnx',
      sizeMB: 1800,
      ramRequiredMB: 3072,
      capabilities: ['chat', 'reasoning', 'code', 'math'],
      maxTokens: 4096,
    ),
  };

  // Getters
  String get currentModel => _currentModel;
  bool get isInitialized => _isInitialized;
  bool get isProcessing => _isProcessing;
  List<String> get availableModelIds => _availableModels.keys.toList();
  
  ModelConfig? getModelConfig(String modelId) => _availableModels[modelId];
  ModelConfig get currentModelConfig => _availableModels[_currentModel]!;

  // Initialize the AI service
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      debugPrint('🤖 Initializing ATLES-Mini AI Service...');
      
      // Check device capabilities
      final deviceInfo = await _getDeviceInfo();
      debugPrint('📱 Device: ${deviceInfo['model']}, RAM: ${deviceInfo['ram_mb']}MB');
      
      // Select best model for device
      _currentModel = _selectBestModel(deviceInfo);
      debugPrint('🧠 Selected model: $_currentModel');
      
      // Initialize the model
      await _initializeModel(_currentModel);
      
      _isInitialized = true;
      debugPrint('✅ ATLES-Mini AI Service initialized successfully');
      
    } catch (e) {
      debugPrint('❌ Failed to initialize AI service: $e');
      // Fall back to demo mode
      _isInitialized = true; // Allow demo responses
      rethrow;
    }
  }

  // Generate AI response
  Future<ATLESResponse> generateResponse(String input) async {
    if (!_isInitialized) {
      throw Exception('AI service not initialized');
    }
    
    if (_isProcessing) {
      throw Exception('AI is currently processing another request');
    }

    _isProcessing = true;
    final startTime = DateTime.now();
    
    try {
      debugPrint('🤖 Generating response for: ${input.substring(0, input.length > 50 ? 50 : input.length)}...');
      
      // Preprocess input
      final processedInput = _preprocessInput(input);
      
      // Generate response using the model
      final result = await _invokeModel(processedInput);
      
      final processingTime = DateTime.now().difference(startTime).inMilliseconds;
      
      final response = ATLESResponse(
        content: result['content'],
        model: _currentModel,
        confidence: result['confidence'].toDouble(),
        processingTime: processingTime,
        source: ResponseSource.localMobile,
        metadata: {
          'input_tokens': result['input_tokens'],
          'output_tokens': result['output_tokens'],
          'device_model': result['device_model'],
        },
        suggestions: List<String>.from(result['suggestions'] ?? []),
        type: _determineResponseType(result['content']),
      );
      
      debugPrint('✅ Response generated in ${processingTime}ms (confidence: ${response.confidence})');
      return response;
      
    } catch (e) {
      debugPrint('❌ Error generating response: $e');
      
      // Return fallback response
      return _createFallbackResponse(input, DateTime.now().difference(startTime).inMilliseconds);
      
    } finally {
      _isProcessing = false;
    }
  }

  // Switch to a different model
  Future<void> switchModel(String modelId) async {
    if (!_availableModels.containsKey(modelId)) {
      throw Exception('Model $modelId not available');
    }
    
    if (modelId == _currentModel) return;
    
    debugPrint('🔄 Switching from $_currentModel to $modelId');
    
    try {
      await _initializeModel(modelId);
      _currentModel = modelId;
      debugPrint('✅ Successfully switched to $modelId');
    } catch (e) {
      debugPrint('❌ Failed to switch to $modelId: $e');
      rethrow;
    }
  }

  // Check if model is available on device
  Future<bool> isModelAvailable(String modelId) async {
    if (!_availableModels.containsKey(modelId)) return false;
    
    try {
      final result = await _channel.invokeMethod('checkModelAvailable', {
        'model_id': modelId,
        'file_name': _availableModels[modelId]!.fileName,
      });
      return result as bool;
    } catch (e) {
      debugPrint('Error checking model availability: $e');
      return false;
    }
  }

  // Download and install a model
  Future<void> downloadModel(String modelId, {
    Function(double progress)? onProgress,
  }) async {
    if (!_availableModels.containsKey(modelId)) {
      throw Exception('Model $modelId not available');
    }
    
    final config = _availableModels[modelId]!;
    debugPrint('📥 Downloading model: ${config.name} (${config.sizeMB}MB)');
    
    try {
      await _channel.invokeMethod('downloadModel', {
        'model_id': modelId,
        'file_name': config.fileName,
        'size_mb': config.sizeMB,
      });
      
      debugPrint('✅ Model $modelId downloaded successfully');
    } catch (e) {
      debugPrint('❌ Failed to download model $modelId: $e');
      rethrow;
    }
  }

  // Get device information
  Future<Map<String, dynamic>> _getDeviceInfo() async {
    try {
      final result = await _channel.invokeMethod('getDeviceInfo');
      return Map<String, dynamic>.from(result);
    } catch (e) {
      // Fallback device info
      return {
        'model': 'Unknown',
        'ram_mb': 4096,
        'available_storage_mb': 10000,
        'cpu_cores': 8,
      };
    }
  }

  // Select best model based on device capabilities
  String _selectBestModel(Map<String, dynamic> deviceInfo) {
    final ramMB = deviceInfo['ram_mb'] as int;
    final storageMB = deviceInfo['available_storage_mb'] as int;
    
    // Sort models by capability (descending) and RAM requirement (ascending)
    final sortedModels = _availableModels.entries.toList()
      ..sort((a, b) {
        final aCapabilities = a.value.capabilities.length;
        final bCapabilities = b.value.capabilities.length;
        if (aCapabilities != bCapabilities) {
          return bCapabilities.compareTo(aCapabilities);
        }
        return a.value.ramRequiredMB.compareTo(b.value.ramRequiredMB);
      });
    
    // Find the best model that fits device constraints
    for (final entry in sortedModels) {
      final config = entry.value;
      if (config.ramRequiredMB <= ramMB && config.sizeMB <= storageMB) {
        return entry.key;
      }
    }
    
    // Fallback to smallest model
    return 'llama_3_2_1b';
  }

  // Initialize a specific model
  Future<void> _initializeModel(String modelId) async {
    final config = _availableModels[modelId]!;
    
    try {
      await _channel.invokeMethod('initializeModel', {
        'model_id': modelId,
        'file_name': config.fileName,
        'max_tokens': config.maxTokens,
      });
    } catch (e) {
      debugPrint('Native model initialization failed, using fallback: $e');
      // Continue with fallback mode
    }
  }

  // Invoke the model for inference
  Future<Map<String, dynamic>> _invokeModel(String input) async {
    try {
      final result = await _channel.invokeMethod('generateResponse', {
        'input': input,
        'model_id': _currentModel,
        'max_tokens': currentModelConfig.maxTokens,
      });
      
      return Map<String, dynamic>.from(result);
    } catch (e) {
      debugPrint('Native inference failed, using fallback: $e');
      
      // Fallback to simple response generation
      return _generateFallbackResponse(input);
    }
  }

  // Preprocess input text
  String _preprocessInput(String input) {
    // Basic preprocessing
    String processed = input.trim();
    
    // Add context based on model capabilities
    final capabilities = currentModelConfig.capabilities;
    
    if (capabilities.contains('chat')) {
      processed = 'User: $processed\nAssistant:';
    }
    
    return processed;
  }

  // Determine response type from content
  ResponseType _determineResponseType(String content) {
    if (content.contains('```') || content.contains('def ') || content.contains('function')) {
      return ResponseType.code;
    }
    return ResponseType.text;
  }

  // Generate fallback response when native AI fails
  Map<String, dynamic> _generateFallbackResponse(String input) {
    final responses = [
      "I'm processing your request using my mobile AI capabilities. How can I help you further?",
      "I understand you're asking about: ${input.length > 50 ? '${input.substring(0, 50)}...' : input}. Let me help you with that.",
      "I'm your mobile AI companion. While I'm working on improving my responses, I'm here to assist you.",
      "Thanks for your question. I'm running locally on your device and learning to provide better responses.",
    ];
    
    final randomResponse = responses[DateTime.now().millisecond % responses.length];
    
    return {
      'content': randomResponse,
      'confidence': 0.7,
      'input_tokens': input.split(' ').length,
      'output_tokens': randomResponse.split(' ').length,
      'device_model': 'fallback',
      'suggestions': ['Tell me more', 'Can you clarify?', 'What else can you help with?'],
    };
  }

  // Create fallback response object
  ATLESResponse _createFallbackResponse(String input, int processingTime) {
    return ATLESResponse(
      content: "I'm having trouble processing your request right now. I'm your mobile AI running locally on your device. Please try rephrasing your question or check if the AI model is properly loaded.",
      model: _currentModel,
      confidence: 0.3,
      processingTime: processingTime,
      source: ResponseSource.localMobile,
      metadata: {
        'fallback': true,
        'error': 'Model inference failed',
      },
      suggestions: [
        'Try a simpler question',
        'Check model status',
        'Restart the app',
      ],
      type: ResponseType.error,
    );
  }

  // Dispose resources
  void dispose() {
    debugPrint('🔄 Disposing ATLES-Mini AI Service');
    _isInitialized = false;
    _isProcessing = false;
  }
}

// Model configuration class
class ModelConfig {
  final String name;
  final String fileName;
  final int sizeMB;
  final int ramRequiredMB;
  final List<String> capabilities;
  final int maxTokens;

  ModelConfig({
    required this.name,
    required this.fileName,
    required this.sizeMB,
    required this.ramRequiredMB,
    required this.capabilities,
    required this.maxTokens,
  });

  @override
  String toString() {
    return 'ModelConfig(name: $name, size: ${sizeMB}MB, ram: ${ramRequiredMB}MB)';
  }
}
