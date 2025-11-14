import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;
import 'package:web_socket_channel/web_socket_channel.dart';
import 'package:web_socket_channel/status.dart' as status;
import '../models/conversation.dart';
import '../models/atles_response.dart';
import '../models/sync_message.dart';
import 'storage_service.dart';

class SyncService {
  final StorageService _storage = StorageService();
  
  String? _serverHost;
  int _serverPort = 8081;
  bool _isConnected = false;
  WebSocketChannel? _webSocket;
  Timer? _heartbeatTimer;
  Timer? _syncTimer;
  
  // Device info
  late DeviceInfo _deviceInfo;
  
  // Connection settings
  Duration _connectionTimeout = const Duration(seconds: 10);
  Duration _heartbeatInterval = const Duration(seconds: 30);
  Duration _syncInterval = const Duration(minutes: 5);
  
  // Getters
  bool get isConnected => _isConnected;
  String? get serverHost => _serverHost;
  int get serverPort => _serverPort;
  DeviceInfo get deviceInfo => _deviceInfo;

  // Initialize sync service
  Future<void> initialize() async {
    debugPrint('🔄 Initializing Sync Service...');
    
    // Initialize device info
    await _initializeDeviceInfo();
    
    // Load saved server settings
    await _loadServerSettings();
    
    // Start background sync if server is configured
    if (_serverHost != null) {
      _startBackgroundSync();
    }
    
    debugPrint('✅ Sync Service initialized');
  }

  // Configure server connection
  Future<void> configureServer(String host, int port) async {
    _serverHost = host;
    _serverPort = port;
    
    // Save settings
    await _storage.savePreference('sync_server_host', host);
    await _storage.savePreference('sync_server_port', port);
    
    debugPrint('🔧 Server configured: $host:$port');
    
    // Test connection
    await checkConnection();
  }

  // Check connection to desktop ATLES
  Future<bool> checkConnection() async {
    if (_serverHost == null) return false;
    
    try {
      debugPrint('🔍 Checking connection to $_serverHost:$_serverPort...');
      
      final response = await http.get(
        Uri.parse('http://$_serverHost:$_serverPort/api/mobile/status/${_deviceInfo.deviceId}'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(_connectionTimeout);
      
      _isConnected = response.statusCode == 200 || response.statusCode == 404; // 404 means server is up but device not registered
      
      if (_isConnected && response.statusCode == 404) {
        // Register device if not found
        await _registerDevice();
      }
      
      debugPrint(_isConnected ? '✅ Connection successful' : '❌ Connection failed');
      return _isConnected;
      
    } catch (e) {
      _isConnected = false;
      debugPrint('❌ Connection check failed: $e');
      return false;
    }
  }

  // Register device with desktop ATLES
  Future<void> _registerDevice() async {
    if (_serverHost == null) return;
    
    try {
      debugPrint('📝 Registering device with desktop ATLES...');
      
      final response = await http.post(
        Uri.parse('http://$_serverHost:$_serverPort/api/mobile/register'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(_deviceInfo.toJson()),
      ).timeout(_connectionTimeout);
      
      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        debugPrint('✅ Device registered successfully: ${result['device_id']}');
        
        // Save recommended models info
        final recommendedModels = result['recommended_models'] as List?;
        if (recommendedModels != null) {
          await _storage.savePreference('recommended_models', recommendedModels);
        }
      } else {
        debugPrint('❌ Device registration failed: ${response.statusCode}');
      }
      
    } catch (e) {
      debugPrint('❌ Device registration error: $e');
    }
  }

  // Sync single conversation
  Future<void> syncConversation(Conversation conversation) async {
    if (!_isConnected) return;
    
    try {
      final syncMessage = SyncMessage.conversationSync(
        deviceId: _deviceInfo.deviceId,
        conversations: [conversation],
      );
      
      await _sendSyncMessage(syncMessage);
      debugPrint('📤 Synced conversation: ${conversation.id}');
      
    } catch (e) {
      debugPrint('❌ Failed to sync conversation: $e');
      // Add to local sync queue for retry
      await _storage.addToSyncQueue(SyncMessage.conversationSync(
        deviceId: _deviceInfo.deviceId,
        conversations: [conversation],
      ));
    }
  }

  // Sync all conversations
  Future<void> syncAllConversations(List<Conversation> conversations) async {
    if (!_isConnected || conversations.isEmpty) return;
    
    try {
      debugPrint('📤 Syncing ${conversations.length} conversations...');
      
      // Split into batches to avoid large payloads
      const batchSize = 10;
      for (int i = 0; i < conversations.length; i += batchSize) {
        final batch = conversations.skip(i).take(batchSize).toList();
        
        final syncMessage = SyncMessage.conversationSync(
          deviceId: _deviceInfo.deviceId,
          conversations: batch,
        );
        
        await _sendSyncMessage(syncMessage);
        
        // Small delay between batches
        if (i + batchSize < conversations.length) {
          await Future.delayed(const Duration(milliseconds: 100));
        }
      }
      
      debugPrint('✅ All conversations synced successfully');
      
    } catch (e) {
      debugPrint('❌ Failed to sync conversations: $e');
    }
  }

  // Collaborate with desktop ATLES
  Future<ATLESResponse> collaborateWithDesktop(String query, {
    String requestType = 'complex_reasoning',
    Map<String, dynamic> context = const {},
  }) async {
    if (!_isConnected) {
      throw Exception('Not connected to desktop ATLES');
    }
    
    try {
      debugPrint('🤝 Collaborating with desktop ATLES: $requestType');
      
      final response = await http.post(
        Uri.parse('http://$_serverHost:$_serverPort/api/mobile/collaborate'),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode({
          'device_id': _deviceInfo.deviceId,
          'request_type': requestType,
          'content': query,
          'context': context,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        final result = jsonDecode(response.body);
        
        return ATLESResponse(
          content: result['response'],
          model: result['source'] == 'atles_prime' ? 'ATLES-Prime' : 'Desktop-Sync',
          confidence: 0.9, // High confidence for desktop responses
          processingTime: 0, // Network time not included
          source: ResponseSource.desktopATLES,
          metadata: {
            'collaboration_type': requestType,
            'desktop_source': result['source'],
            'timestamp': result['timestamp'],
          },
          type: ResponseType.text,
        );
      } else {
        throw Exception('Desktop collaboration failed: ${response.statusCode}');
      }
      
    } catch (e) {
      debugPrint('❌ Desktop collaboration failed: $e');
      rethrow;
    }
  }

  // Send sync message to desktop
  Future<void> _sendSyncMessage(SyncMessage message) async {
    if (_serverHost == null) return;
    
    final response = await http.post(
      Uri.parse('http://$_serverHost:$_serverPort/api/mobile/sync'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(message.toJson()),
    ).timeout(_connectionTimeout);
    
    if (response.statusCode != 200) {
      throw Exception('Sync failed: ${response.statusCode}');
    }
  }

  // Start WebSocket connection for real-time sync
  Future<void> _startWebSocketConnection() async {
    if (_serverHost == null || _webSocket != null) return;
    
    try {
      debugPrint('🔌 Starting WebSocket connection...');
      
      final uri = Uri.parse('ws://$_serverHost:$_serverPort/ws/mobile/${_deviceInfo.deviceId}');
      _webSocket = WebSocketChannel.connect(uri);
      
      // Listen for messages
      _webSocket!.stream.listen(
        (message) => _handleWebSocketMessage(message),
        onError: (error) => _handleWebSocketError(error),
        onDone: () => _handleWebSocketClosed(),
      );
      
      // Start heartbeat
      _startHeartbeat();
      
      debugPrint('✅ WebSocket connected');
      
    } catch (e) {
      debugPrint('❌ WebSocket connection failed: $e');
      _webSocket = null;
    }
  }

  // Handle WebSocket messages
  void _handleWebSocketMessage(dynamic message) {
    try {
      final data = jsonDecode(message);
      final messageType = data['type'];
      
      debugPrint('📨 WebSocket message: $messageType');
      
      switch (messageType) {
        case 'pong':
          // Heartbeat response
          break;
          
        case 'sync_response':
          // Sync acknowledgment
          break;
          
        case 'collaboration_response':
          // Real-time collaboration response
          _handleCollaborationResponse(data['data']);
          break;
          
        default:
          debugPrint('❓ Unknown WebSocket message type: $messageType');
      }
      
    } catch (e) {
      debugPrint('❌ Error handling WebSocket message: $e');
    }
  }

  // Handle collaboration response
  void _handleCollaborationResponse(Map<String, dynamic> data) {
    // This would be handled by the UI layer through callbacks
    debugPrint('🤝 Collaboration response received');
  }

  // Handle WebSocket errors
  void _handleWebSocketError(dynamic error) {
    debugPrint('❌ WebSocket error: $error');
    _webSocket = null;
  }

  // Handle WebSocket closed
  void _handleWebSocketClosed() {
    debugPrint('🔌 WebSocket connection closed');
    _webSocket = null;
    _heartbeatTimer?.cancel();
    
    // Attempt to reconnect after delay
    Timer(const Duration(seconds: 5), () {
      if (_isConnected) {
        _startWebSocketConnection();
      }
    });
  }

  // Start heartbeat to keep connection alive
  void _startHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(_heartbeatInterval, (timer) {
      if (_webSocket != null) {
        _webSocket!.sink.add(jsonEncode({
          'type': 'ping',
          'timestamp': DateTime.now().toIso8601String(),
        }));
      } else {
        timer.cancel();
      }
    });
  }

  // Start background sync
  void _startBackgroundSync() {
    _syncTimer?.cancel();
    _syncTimer = Timer.periodic(_syncInterval, (timer) async {
      if (_isConnected) {
        await _processPendingSync();
      }
    });
  }

  // Process pending sync messages
  Future<void> _processPendingSync() async {
    try {
      final pendingMessages = await _storage.getPendingSyncMessages(limit: 50);
      
      if (pendingMessages.isEmpty) return;
      
      debugPrint('📤 Processing ${pendingMessages.length} pending sync messages...');
      
      for (final message in pendingMessages) {
        try {
          await _sendSyncMessage(message);
          await _storage.markSyncCompleted(message.id);
        } catch (e) {
          debugPrint('❌ Failed to sync message ${message.id}: $e');
          // Leave in queue for retry
        }
      }
      
    } catch (e) {
      debugPrint('❌ Error processing pending sync: $e');
    }
  }

  // Initialize device information
  Future<void> _initializeDeviceInfo() async {
    // Get device info (this would be implemented with platform channels)
    _deviceInfo = DeviceInfo(
      deviceId: 'pixel9_${DateTime.now().millisecondsSinceEpoch}',
      deviceName: 'Google Pixel 9',
      model: 'Pixel 9',
      osVersion: 'Android 14',
      ramMB: 12288, // 12GB
      availableStorageMB: 50000, // 50GB available
      capabilities: ['camera', 'microphone', 'location', 'sensors'],
      installedModels: {
        'llama_3_2_1b': '1.0.0',
      },
    );
  }

  // Load server settings from storage
  Future<void> _loadServerSettings() async {
    _serverHost = _storage.loadPreference<String>('sync_server_host');
    _serverPort = _storage.loadPreference<int>('sync_server_port', defaultValue: 8081)!;
    
    if (_serverHost != null) {
      debugPrint('📡 Loaded server settings: $_serverHost:$_serverPort');
    }
  }

  // Get sync statistics
  Future<SyncStats> getSyncStats() async {
    // This would be implemented by tracking sync operations
    return SyncStats(
      totalMessagesSent: 0,
      totalMessagesReceived: 0,
      conversationsSynced: 0,
      collaborationRequests: 0,
      lastSyncTime: DateTime.now(),
      averageSyncTime: const Duration(seconds: 2),
      messageTypeDistribution: {},
    );
  }

  // Disconnect from server
  Future<void> disconnect() async {
    _isConnected = false;
    
    _heartbeatTimer?.cancel();
    _syncTimer?.cancel();
    
    if (_webSocket != null) {
      await _webSocket!.sink.close(status.goingAway);
      _webSocket = null;
    }
    
    debugPrint('🔌 Disconnected from server');
  }

  // Dispose resources
  void dispose() {
    disconnect();
    debugPrint('🔄 Sync Service disposed');
  }
}
