import 'package:flutter/foundation.dart';
import '../models/conversation.dart';
import '../models/atles_response.dart';
import '../services/mobile_ai_service.dart';
import '../services/sync_service.dart';

class ATLESProvider extends ChangeNotifier {
  final MobileAIService _aiService = MobileAIService();
  final SyncService _syncService = SyncService();
  
  List<Conversation> _conversations = [];
  bool _isProcessing = false;
  bool _isConnectedToDesktop = false;
  String _currentModel = 'llama_3_2_1b';
  
  // Getters
  List<Conversation> get conversations => _conversations;
  bool get isProcessing => _isProcessing;
  bool get isConnectedToDesktop => _isConnectedToDesktop;
  String get currentModel => _currentModel;
  
  // Initialize ATLES-Mini
  Future<void> initialize() async {
    try {
      await _aiService.initialize();
      await _checkDesktopConnection();
      notifyListeners();
    } catch (e) {
      debugPrint('ATLES initialization failed: $e');
    }
  }
  
  // Send message to ATLES-Mini
  Future<void> sendMessage(String message) async {
    if (_isProcessing) return;
    
    _isProcessing = true;
    notifyListeners();
    
    try {
      // Add user message to conversation
      final userMessage = Message(
        content: message,
        isUser: true,
        timestamp: DateTime.now(),
      );
      
      if (_conversations.isEmpty) {
        _conversations.add(Conversation(
          id: DateTime.now().millisecondsSinceEpoch.toString(),
          messages: [userMessage],
          createdAt: DateTime.now(),
        ));
      } else {
        _conversations.last.messages.add(userMessage);
      }
      
      notifyListeners();
      
      // Get AI response
      ATLESResponse response;
      
      if (_isConnectedToDesktop && _shouldUseDesktopATLES(message)) {
        // Use desktop ATLES for complex queries
        response = await _syncService.collaborateWithDesktop(message);
      } else {
        // Use local mobile AI
        response = await _aiService.generateResponse(message);
      }
      
      // Add AI response to conversation
      final aiMessage = Message(
        content: response.content,
        isUser: false,
        timestamp: DateTime.now(),
        metadata: {
          'model': response.model,
          'confidence': response.confidence,
          'processing_time': response.processingTime,
        },
      );
      
      _conversations.last.messages.add(aiMessage);
      
      // Sync with desktop if connected
      if (_isConnectedToDesktop) {
        await _syncService.syncConversation(_conversations.last);
      }
      
    } catch (e) {
      debugPrint('Error sending message: $e');
      
      // Add error message
      final errorMessage = Message(
        content: 'Sorry, I encountered an error processing your message. Please try again.',
        isUser: false,
        timestamp: DateTime.now(),
        metadata: {'error': e.toString()},
      );
      
      _conversations.last.messages.add(errorMessage);
    } finally {
      _isProcessing = false;
      notifyListeners();
    }
  }
  
  // Check connection to desktop ATLES
  Future<void> _checkDesktopConnection() async {
    try {
      _isConnectedToDesktop = await _syncService.checkConnection();
      if (_isConnectedToDesktop) {
        await _syncService.syncAllConversations(_conversations);
      }
    } catch (e) {
      _isConnectedToDesktop = false;
      debugPrint('Desktop connection check failed: $e');
    }
  }
  
  // Determine if query should use desktop ATLES
  bool _shouldUseDesktopATLES(String message) {
    // Use desktop for complex queries
    final complexKeywords = [
      'code', 'programming', 'debug', 'analyze', 'complex',
      'detailed', 'research', 'calculate', 'solve'
    ];
    
    return complexKeywords.any((keyword) => 
      message.toLowerCase().contains(keyword));
  }
  
  // Start new conversation
  void startNewConversation() {
    final newConversation = Conversation(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      messages: [],
      createdAt: DateTime.now(),
    );
    
    _conversations.add(newConversation);
    notifyListeners();
  }
  
  // Delete conversation
  void deleteConversation(String conversationId) {
    _conversations.removeWhere((conv) => conv.id == conversationId);
    notifyListeners();
  }
  
  // Switch AI model
  Future<void> switchModel(String modelName) async {
    if (_currentModel == modelName) return;
    
    try {
      await _aiService.switchModel(modelName);
      _currentModel = modelName;
      notifyListeners();
    } catch (e) {
      debugPrint('Failed to switch model: $e');
    }
  }
  
  // Sync with desktop
  Future<void> syncWithDesktop() async {
    try {
      await _checkDesktopConnection();
      if (_isConnectedToDesktop) {
        await _syncService.syncAllConversations(_conversations);
      }
    } catch (e) {
      debugPrint('Sync failed: $e');
    }
  }
  
  @override
  void dispose() {
    _aiService.dispose();
    _syncService.dispose();
    super.dispose();
  }
}
