import 'dart:async';
import 'dart:convert';
import 'dart:io';
import 'package:flutter/foundation.dart';
import 'package:sqflite/sqflite.dart';
import 'package:path/path.dart';
import 'package:path_provider/path_provider.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/conversation.dart';
import '../models/atles_response.dart';
import '../models/sync_message.dart';

class StorageService {
  static const String _dbName = 'atles_mini.db';
  static const int _dbVersion = 1;
  
  Database? _database;
  SharedPreferences? _prefs;
  bool _isInitialized = false;

  // Singleton pattern
  static final StorageService _instance = StorageService._internal();
  factory StorageService() => _instance;
  StorageService._internal();

  // Initialize storage
  Future<void> initialize() async {
    if (_isInitialized) return;
    
    try {
      debugPrint('💾 Initializing ATLES-Mini Storage Service...');
      
      // Initialize SharedPreferences
      _prefs = await SharedPreferences.getInstance();
      
      // Initialize SQLite database
      await _initializeDatabase();
      
      _isInitialized = true;
      debugPrint('✅ Storage Service initialized successfully');
      
    } catch (e) {
      debugPrint('❌ Failed to initialize storage: $e');
      rethrow;
    }
  }

  // Initialize SQLite database
  Future<void> _initializeDatabase() async {
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final path = join(documentsDirectory.path, _dbName);
    
    _database = await openDatabase(
      path,
      version: _dbVersion,
      onCreate: _createDatabase,
      onUpgrade: _upgradeDatabase,
    );
  }

  // Create database tables
  Future<void> _createDatabase(Database db, int version) async {
    debugPrint('📊 Creating database tables...');
    
    // Conversations table
    await db.execute('''
      CREATE TABLE conversations (
        id TEXT PRIMARY KEY,
        title TEXT,
        created_at TEXT NOT NULL,
        updated_at TEXT,
        metadata TEXT,
        message_count INTEGER DEFAULT 0
      )
    ''');

    // Messages table
    await db.execute('''
      CREATE TABLE messages (
        id TEXT PRIMARY KEY,
        conversation_id TEXT NOT NULL,
        content TEXT NOT NULL,
        is_user INTEGER NOT NULL,
        timestamp TEXT NOT NULL,
        type TEXT NOT NULL DEFAULT 'text',
        metadata TEXT,
        FOREIGN KEY (conversation_id) REFERENCES conversations (id) ON DELETE CASCADE
      )
    ''');

    // Response metrics table
    await db.execute('''
      CREATE TABLE response_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id TEXT NOT NULL,
        model TEXT NOT NULL,
        confidence REAL NOT NULL,
        processing_time INTEGER NOT NULL,
        source TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        FOREIGN KEY (message_id) REFERENCES messages (id) ON DELETE CASCADE
      )
    ''');

    // Sync queue table
    await db.execute('''
      CREATE TABLE sync_queue (
        id TEXT PRIMARY KEY,
        type TEXT NOT NULL,
        device_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        priority TEXT NOT NULL DEFAULT 'normal',
        data TEXT NOT NULL,
        synced INTEGER DEFAULT 0
      )
    ''');

    // Create indexes for better performance
    await db.execute('CREATE INDEX idx_conversations_created_at ON conversations(created_at)');
    await db.execute('CREATE INDEX idx_messages_conversation_id ON messages(conversation_id)');
    await db.execute('CREATE INDEX idx_messages_timestamp ON messages(timestamp)');
    await db.execute('CREATE INDEX idx_sync_queue_synced ON sync_queue(synced)');
    
    debugPrint('✅ Database tables created successfully');
  }

  // Upgrade database schema
  Future<void> _upgradeDatabase(Database db, int oldVersion, int newVersion) async {
    debugPrint('🔄 Upgrading database from version $oldVersion to $newVersion');
    // Handle future schema upgrades here
  }

  // CONVERSATION OPERATIONS

  // Save conversation
  Future<void> saveConversation(Conversation conversation) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.transaction((txn) async {
      // Insert or update conversation
      await txn.insert(
        'conversations',
        {
          'id': conversation.id,
          'title': conversation.title,
          'created_at': conversation.createdAt.toIso8601String(),
          'updated_at': conversation.updatedAt?.toIso8601String(),
          'metadata': jsonEncode(conversation.metadata),
          'message_count': conversation.messages.length,
        },
        conflictAlgorithm: ConflictAlgorithm.replace,
      );

      // Delete existing messages for this conversation
      await txn.delete('messages', where: 'conversation_id = ?', whereArgs: [conversation.id]);

      // Insert all messages
      for (final message in conversation.messages) {
        await txn.insert('messages', {
          'id': message.id,
          'conversation_id': conversation.id,
          'content': message.content,
          'is_user': message.isUser ? 1 : 0,
          'timestamp': message.timestamp.toIso8601String(),
          'type': message.type.name,
          'metadata': jsonEncode(message.metadata),
        });
      }
    });

    debugPrint('💾 Saved conversation: ${conversation.id} (${conversation.messages.length} messages)');
  }

  // Load all conversations
  Future<List<Conversation>> loadConversations({
    int? limit,
    int? offset,
    ConversationFilter? filter,
  }) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    String whereClause = '';
    List<dynamic> whereArgs = [];
    
    // Apply filters
    if (filter != null) {
      final conditions = <String>[];
      
      if (filter.startDate != null) {
        conditions.add('created_at >= ?');
        whereArgs.add(filter.startDate!.toIso8601String());
      }
      
      if (filter.endDate != null) {
        conditions.add('created_at <= ?');
        whereArgs.add(filter.endDate!.toIso8601String());
      }
      
      if (conditions.isNotEmpty) {
        whereClause = 'WHERE ${conditions.join(' AND ')}';
      }
    }
    
    // Query conversations
    final conversationMaps = await db.query(
      'conversations',
      where: whereClause.isEmpty ? null : whereClause.replaceFirst('WHERE ', ''),
      whereArgs: whereArgs.isEmpty ? null : whereArgs,
      orderBy: 'updated_at DESC, created_at DESC',
      limit: limit,
      offset: offset,
    );

    final conversations = <Conversation>[];
    
    for (final convMap in conversationMaps) {
      // Load messages for this conversation
      final messageMaps = await db.query(
        'messages',
        where: 'conversation_id = ?',
        whereArgs: [convMap['id']],
        orderBy: 'timestamp ASC',
      );

      final messages = messageMaps.map((msgMap) => Message(
        id: msgMap['id'] as String,
        content: msgMap['content'] as String,
        isUser: (msgMap['is_user'] as int) == 1,
        timestamp: DateTime.parse(msgMap['timestamp'] as String),
        type: MessageType.values.firstWhere(
          (t) => t.name == msgMap['type'],
          orElse: () => MessageType.text,
        ),
        metadata: jsonDecode(msgMap['metadata'] as String? ?? '{}'),
      )).toList();

      final conversation = Conversation(
        id: convMap['id'] as String,
        messages: messages,
        createdAt: DateTime.parse(convMap['created_at'] as String),
        updatedAt: convMap['updated_at'] != null 
            ? DateTime.parse(convMap['updated_at'] as String)
            : null,
        title: convMap['title'] as String?,
        metadata: jsonDecode(convMap['metadata'] as String? ?? '{}'),
      );

      // Apply content-based filters
      if (filter == null || filter.matches(conversation)) {
        conversations.add(conversation);
      }
    }

    debugPrint('📚 Loaded ${conversations.length} conversations');
    return conversations;
  }

  // Load single conversation
  Future<Conversation?> loadConversation(String conversationId) async {
    final conversations = await loadConversations();
    try {
      return conversations.firstWhere((c) => c.id == conversationId);
    } catch (e) {
      return null;
    }
  }

  // Delete conversation
  Future<void> deleteConversation(String conversationId) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.transaction((txn) async {
      await txn.delete('messages', where: 'conversation_id = ?', whereArgs: [conversationId]);
      await txn.delete('conversations', where: 'id = ?', whereArgs: [conversationId]);
    });

    debugPrint('🗑️ Deleted conversation: $conversationId');
  }

  // RESPONSE METRICS

  // Save response metrics
  Future<void> saveResponseMetrics(String messageId, ATLESResponse response) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.insert('response_metrics', {
      'message_id': messageId,
      'model': response.model,
      'confidence': response.confidence,
      'processing_time': response.processingTime,
      'source': response.source.name,
      'timestamp': DateTime.now().toIso8601String(),
    });
  }

  // Load response metrics
  Future<ResponseMetrics> loadResponseMetrics({DateTime? since}) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    String whereClause = '';
    List<dynamic> whereArgs = [];
    
    if (since != null) {
      whereClause = 'WHERE timestamp >= ?';
      whereArgs = [since.toIso8601String()];
    }
    
    final maps = await db.query(
      'response_metrics',
      where: whereClause.isEmpty ? null : whereClause.replaceFirst('WHERE ', ''),
      whereArgs: whereArgs.isEmpty ? null : whereArgs,
    );

    if (maps.isEmpty) {
      return ResponseMetrics(
        averageConfidence: 0.0,
        averageProcessingTime: 0,
        sourceDistribution: {},
        modelUsage: {},
        totalResponses: 0,
      );
    }

    final responses = maps.map((map) => ATLESResponse(
      content: '', // Not needed for metrics
      model: map['model'] as String,
      confidence: map['confidence'] as double,
      processingTime: map['processing_time'] as int,
      source: ResponseSource.values.firstWhere(
        (s) => s.name == map['source'],
        orElse: () => ResponseSource.localMobile,
      ),
    )).toList();

    return ResponseMetrics.fromResponses(responses);
  }

  // SYNC OPERATIONS

  // Add message to sync queue
  Future<void> addToSyncQueue(SyncMessage message) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.insert('sync_queue', {
      'id': message.id,
      'type': message.type.name,
      'device_id': message.deviceId,
      'timestamp': message.timestamp.toIso8601String(),
      'priority': message.priority.name,
      'data': jsonEncode(message.data),
      'synced': 0,
    });

    debugPrint('📤 Added to sync queue: ${message.type} (${message.id})');
  }

  // Get pending sync messages
  Future<List<SyncMessage>> getPendingSyncMessages({int? limit}) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    final maps = await db.query(
      'sync_queue',
      where: 'synced = 0',
      orderBy: 'priority DESC, timestamp ASC',
      limit: limit,
    );

    return maps.map((map) => SyncMessage(
      id: map['id'] as String,
      type: SyncMessageType.values.firstWhere(
        (t) => t.name == map['type'],
      ),
      deviceId: map['device_id'] as String,
      timestamp: DateTime.parse(map['timestamp'] as String),
      priority: SyncPriority.values.firstWhere(
        (p) => p.name == map['priority'],
        orElse: () => SyncPriority.normal,
      ),
      data: jsonDecode(map['data'] as String),
    )).toList();
  }

  // Mark sync message as completed
  Future<void> markSyncCompleted(String messageId) async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.update(
      'sync_queue',
      {'synced': 1},
      where: 'id = ?',
      whereArgs: [messageId],
    );
  }

  // PREFERENCES

  // Save preference
  Future<void> savePreference(String key, dynamic value) async {
    await _ensureInitialized();
    
    final prefs = _prefs!;
    
    if (value is String) {
      await prefs.setString(key, value);
    } else if (value is int) {
      await prefs.setInt(key, value);
    } else if (value is double) {
      await prefs.setDouble(key, value);
    } else if (value is bool) {
      await prefs.setBool(key, value);
    } else if (value is List<String>) {
      await prefs.setStringList(key, value);
    } else {
      await prefs.setString(key, jsonEncode(value));
    }
  }

  // Load preference
  T? loadPreference<T>(String key, {T? defaultValue}) {
    if (!_isInitialized || _prefs == null) return defaultValue;
    
    final prefs = _prefs!;
    
    if (T == String) {
      return prefs.getString(key) as T? ?? defaultValue;
    } else if (T == int) {
      return prefs.getInt(key) as T? ?? defaultValue;
    } else if (T == double) {
      return prefs.getDouble(key) as T? ?? defaultValue;
    } else if (T == bool) {
      return prefs.getBool(key) as T? ?? defaultValue;
    } else {
      final stringValue = prefs.getString(key);
      if (stringValue == null) return defaultValue;
      
      try {
        return jsonDecode(stringValue) as T;
      } catch (e) {
        return defaultValue;
      }
    }
  }

  // UTILITY METHODS

  // Get storage statistics
  Future<Map<String, dynamic>> getStorageStats() async {
    await _ensureInitialized();
    
    final db = _database!;
    
    final conversationCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM conversations')
    ) ?? 0;
    
    final messageCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM messages')
    ) ?? 0;
    
    final syncQueueCount = Sqflite.firstIntValue(
      await db.rawQuery('SELECT COUNT(*) FROM sync_queue WHERE synced = 0')
    ) ?? 0;

    // Get database file size
    final documentsDirectory = await getApplicationDocumentsDirectory();
    final dbPath = join(documentsDirectory.path, _dbName);
    final dbFile = File(dbPath);
    final dbSizeBytes = await dbFile.exists() ? await dbFile.length() : 0;

    return {
      'conversations': conversationCount,
      'messages': messageCount,
      'pending_sync': syncQueueCount,
      'database_size_mb': (dbSizeBytes / (1024 * 1024)).toStringAsFixed(2),
      'database_path': dbPath,
    };
  }

  // Clear all data (for testing/reset)
  Future<void> clearAllData() async {
    await _ensureInitialized();
    
    final db = _database!;
    
    await db.transaction((txn) async {
      await txn.delete('response_metrics');
      await txn.delete('messages');
      await txn.delete('conversations');
      await txn.delete('sync_queue');
    });

    await _prefs!.clear();
    
    debugPrint('🗑️ All data cleared');
  }

  // Ensure service is initialized
  Future<void> _ensureInitialized() async {
    if (!_isInitialized) {
      await initialize();
    }
  }

  // Dispose resources
  Future<void> dispose() async {
    if (_database != null) {
      await _database!.close();
      _database = null;
    }
    _isInitialized = false;
    debugPrint('🔄 Storage Service disposed');
  }
}
