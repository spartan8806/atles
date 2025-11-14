import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../models/atles_models.dart';

class AtlesProvider with ChangeNotifier {
  String _serverIp = '';
  int _serverPort = 8080;
  bool _isConnected = false;
  bool _isConnecting = false;
  String _currentSessionId = '';
  List<ChatSession> _sessions = [];
  List<Message> _currentMessages = [];
  ServerStatus _serverStatus = ServerStatus.offline();

  bool get isConnected => _isConnected;
  bool get isConnecting => _isConnecting;
  String get serverIp => _serverIp;
  int get serverPort => _serverPort;
  String get serverUrl => 'http://$_serverIp:$_serverPort';
  String get currentSessionId => _currentSessionId;
  List<ChatSession> get sessions => _sessions;
  List<Message> get currentMessages => _currentMessages;
  ServerStatus get serverStatus => _serverStatus;

  AtlesProvider() {
    _loadServerSettings();
  }

  Future<void> _loadServerSettings() async {
    final prefs = await SharedPreferences.getInstance();
    _serverIp = prefs.getString('server_ip') ?? '';
    _serverPort = prefs.getInt('server_port') ?? 8080;
    notifyListeners();
    
    if (_serverIp.isNotEmpty) {
      checkConnection();
    }
  }

  Future<void> setServerSettings(String ip, int port) async {
    _serverIp = ip;
    _serverPort = port;
    
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString('server_ip', ip);
    await prefs.setInt('server_port', port);
    
    notifyListeners();
  }

  Future<bool> checkConnection() async {
    if (_serverIp.isEmpty) return false;
    
    _isConnecting = true;
    notifyListeners();
    
    try {
      final response = await http.get(
        Uri.parse('$serverUrl/api/health'),
      ).timeout(const Duration(seconds: 5));
      
      _isConnected = response.statusCode == 200;
      
      if (_isConnected) {
        await _fetchServerStatus();
        await _fetchSessions();
      }
    } catch (e) {
      _isConnected = false;
      print('Connection error: $e');
    }
    
    _isConnecting = false;
    notifyListeners();
    return _isConnected;
  }

  Future<void> _fetchServerStatus() async {
    try {
      final response = await http.get(
        Uri.parse('$serverUrl/api/status'),
      ).timeout(const Duration(seconds: 5));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        _serverStatus = ServerStatus.fromJson(data);
      }
    } catch (e) {
      print('Error fetching server status: $e');
    }
  }

  Future<void> _fetchSessions() async {
    try {
      final response = await http.get(
        Uri.parse('$serverUrl/api/sessions'),
      ).timeout(const Duration(seconds: 5));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body) as Map<String, dynamic>;
        // Transform sessions
        _sessions = [];
        data.forEach((id, sessionData) {
          _sessions.add(ChatSession(
            id: id,
            title: 'Chat ${_sessions.length + 1}',
            createdAt: DateTime.parse(sessionData['created_at']),
            messages: [],
          ));
        });
        
        // Sort by most recent
        _sessions.sort((a, b) => b.createdAt.compareTo(a.createdAt));
        
        notifyListeners();
      }
    } catch (e) {
      print('Error fetching sessions: $e');
    }
  }

  Future<void> fetchSessionMessages(String sessionId) async {
    _currentSessionId = sessionId;
    
    try {
      final response = await http.get(
        Uri.parse('$serverUrl/api/sessions/$sessionId'),
      ).timeout(const Duration(seconds: 5));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        List<dynamic> messages = data['messages'];
        
        _currentMessages = messages.map((msg) {
          return Message(
            id: DateTime.now().millisecondsSinceEpoch.toString() + msg['role'],
            content: msg['content'],
            isUser: msg['role'] == 'user',
            timestamp: DateTime.parse(msg['timestamp']),
          );
        }).toList();
        
        notifyListeners();
      }
    } catch (e) {
      print('Error fetching session messages: $e');
    }
  }

  Future<void> sendMessage(String message) async {
    if (!_isConnected) {
      await checkConnection();
      if (!_isConnected) return;
    }
    
    // Add pending message locally
    final pendingMessage = Message(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      content: message,
      isUser: true,
      timestamp: DateTime.now(),
      isPending: true,
    );
    
    _currentMessages.add(pendingMessage);
    notifyListeners();
    
    try {
      final response = await http.post(
        Uri.parse('$serverUrl/api/chat'),
        headers: {'Content-Type': 'application/json'},
        body: json.encode({
          'message': message,
          'session_id': _currentSessionId.isEmpty ? null : _currentSessionId,
        }),
      ).timeout(const Duration(seconds: 30));
      
      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        
        // Update pending message to sent
        final msgIndex = _currentMessages.indexWhere((m) => m.id == pendingMessage.id);
        if (msgIndex != -1) {
          _currentMessages[msgIndex] = Message(
            id: pendingMessage.id,
            content: message,
            isUser: true,
            timestamp: DateTime.now(),
            isPending: false,
          );
        }
        
        // Add ATLES response
        _currentMessages.add(Message(
          id: DateTime.now().millisecondsSinceEpoch.toString() + 'atles',
          content: data['response'],
          isUser: false,
          timestamp: DateTime.now(),
        ));
        
        // Set or update session ID
        if (_currentSessionId.isEmpty) {
          _currentSessionId = data['session_id'];
          await _fetchSessions(); // Refresh sessions list
        }
        
        notifyListeners();
      } else {
        _handleSendError(pendingMessage);
      }
    } catch (e) {
      print('Error sending message: $e');
      _handleSendError(pendingMessage);
    }
  }

  void _handleSendError(Message pendingMessage) {
    // Mark message as error
    final msgIndex = _currentMessages.indexWhere((m) => m.id == pendingMessage.id);
    if (msgIndex != -1) {
      _currentMessages[msgIndex] = Message(
        id: pendingMessage.id,
        content: pendingMessage.content + ' (Failed to send)',
        isUser: true,
        timestamp: pendingMessage.timestamp,
        isPending: false,
      );
    }
    
    // Add error message from system
    _currentMessages.add(Message(
      id: DateTime.now().millisecondsSinceEpoch.toString() + 'error',
      content: 'Failed to communicate with ATLES. Please check your connection.',
      isUser: false,
      timestamp: DateTime.now(),
    ));
    
    notifyListeners();
  }

  void startNewChat() {
    _currentSessionId = '';
    _currentMessages = [];
    notifyListeners();
  }

  Future<void> refresh() async {
    if (_isConnected) {
      await _fetchServerStatus();
      await _fetchSessions();
      if (_currentSessionId.isNotEmpty) {
        await fetchSessionMessages(_currentSessionId);
      }
    }
  }
}
