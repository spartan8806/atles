import 'package:flutter/material.dart';
import 'package:flutter/services.dart';

class VoiceButton extends StatefulWidget {
  final Function(String) onVoiceMessage;
  
  const VoiceButton({
    super.key,
    required this.onVoiceMessage,
  });

  @override
  State<VoiceButton> createState() => _VoiceButtonState();
}

class _VoiceButtonState extends State<VoiceButton>
    with TickerProviderStateMixin {
  bool _isListening = false;
  bool _isProcessing = false;
  String _recognizedText = '';
  
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;
  late AnimationController _scaleController;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    
    _pulseController = AnimationController(
      duration: const Duration(milliseconds: 1000),
      vsync: this,
    );
    _pulseAnimation = Tween<double>(
      begin: 1.0,
      end: 1.2,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));
    
    _scaleController = AnimationController(
      duration: const Duration(milliseconds: 150),
      vsync: this,
    );
    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 0.95,
    ).animate(CurvedAnimation(
      parent: _scaleController,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _pulseController.dispose();
    _scaleController.dispose();
    super.dispose();
  }

  Future<void> _startListening() async {
    if (_isListening || _isProcessing) return;
    
    try {
      setState(() {
        _isListening = true;
        _recognizedText = '';
      });
      
      _pulseController.repeat(reverse: true);
      HapticFeedback.lightImpact();
      
      // Simulate voice recognition
      // In a real implementation, this would use speech_to_text package
      await _simulateVoiceRecognition();
      
    } catch (e) {
      _showError('Voice recognition failed: $e');
    }
  }

  Future<void> _stopListening() async {
    if (!_isListening) return;
    
    setState(() {
      _isListening = false;
      _isProcessing = true;
    });
    
    _pulseController.stop();
    _pulseController.reset();
    HapticFeedback.mediumImpact();
    
    // Process the recognized text
    if (_recognizedText.isNotEmpty) {
      widget.onVoiceMessage(_recognizedText);
    }
    
    setState(() {
      _isProcessing = false;
      _recognizedText = '';
    });
  }

  Future<void> _simulateVoiceRecognition() async {
    // Simulate voice recognition process
    final messages = [
      'Hello ATLES-Mini',
      'What can you help me with?',
      'Tell me about artificial intelligence',
      'How does machine learning work?',
      'Can you explain quantum computing?',
      'What\'s the weather like today?',
    ];
    
    // Simulate listening for 2-3 seconds
    await Future.delayed(const Duration(milliseconds: 2000));
    
    if (_isListening) {
      setState(() {
        _recognizedText = messages[DateTime.now().millisecond % messages.length];
      });
    }
  }

  void _showError(String message) {
    setState(() {
      _isListening = false;
      _isProcessing = false;
    });
    
    _pulseController.stop();
    _pulseController.reset();
    
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return GestureDetector(
      onTapDown: (_) => _scaleController.forward(),
      onTapUp: (_) => _scaleController.reverse(),
      onTapCancel: () => _scaleController.reverse(),
      onTap: _isListening ? _stopListening : _startListening,
      child: AnimatedBuilder(
        animation: Listenable.merge([_pulseAnimation, _scaleAnimation]),
        builder: (context, child) {
          return Transform.scale(
            scale: _scaleAnimation.value,
            child: Container(
              width: 48,
              height: 48,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: _getButtonColor(theme),
                boxShadow: _isListening
                    ? [
                        BoxShadow(
                          color: theme.colorScheme.primary.withOpacity(0.3),
                          blurRadius: 8 * _pulseAnimation.value,
                          spreadRadius: 2 * _pulseAnimation.value,
                        ),
                      ]
                    : null,
              ),
              child: _buildButtonContent(theme),
            ),
          );
        },
      ),
    );
  }

  Color _getButtonColor(ThemeData theme) {
    if (_isListening) {
      return Colors.red;
    } else if (_isProcessing) {
      return theme.colorScheme.secondary;
    } else {
      return theme.colorScheme.primary;
    }
  }

  Widget _buildButtonContent(ThemeData theme) {
    if (_isProcessing) {
      return const Center(
        child: SizedBox(
          width: 24,
          height: 24,
          child: CircularProgressIndicator(
            strokeWidth: 2,
            color: Colors.white,
          ),
        ),
      );
    }
    
    return Icon(
      _isListening ? Icons.stop : Icons.mic,
      color: Colors.white,
      size: 24,
    );
  }
}

// Voice recognition service (placeholder)
class VoiceRecognitionService {
  static const MethodChannel _channel = MethodChannel('atles_mini/voice');
  
  static Future<bool> isAvailable() async {
    try {
      final result = await _channel.invokeMethod('isAvailable');
      return result as bool;
    } catch (e) {
      return false;
    }
  }
  
  static Future<void> startListening() async {
    try {
      await _channel.invokeMethod('startListening');
    } catch (e) {
      throw Exception('Failed to start voice recognition: $e');
    }
  }
  
  static Future<String> stopListening() async {
    try {
      final result = await _channel.invokeMethod('stopListening');
      return result as String;
    } catch (e) {
      throw Exception('Failed to stop voice recognition: $e');
    }
  }
  
  static Future<void> cancel() async {
    try {
      await _channel.invokeMethod('cancel');
    } catch (e) {
      // Ignore cancellation errors
    }
  }
}
