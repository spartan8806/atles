import 'package:uuid/uuid.dart';

class Conversation {
  final String id;
  final List<Message> messages;
  final DateTime createdAt;
  final DateTime? updatedAt;
  final String? title;
  final Map<String, dynamic> metadata;

  Conversation({
    String? id,
    required this.messages,
    required this.createdAt,
    this.updatedAt,
    this.title,
    this.metadata = const {},
  }) : id = id ?? const Uuid().v4();

  // Auto-generate title from first message
  String get displayTitle {
    if (title != null && title!.isNotEmpty) return title!;
    if (messages.isEmpty) return 'New Conversation';
    
    final firstUserMessage = messages.firstWhere(
      (msg) => msg.isUser,
      orElse: () => messages.first,
    );
    
    String content = firstUserMessage.content;
    if (content.length > 50) {
      content = '${content.substring(0, 47)}...';
    }
    return content;
  }

  // Get conversation summary stats
  Map<String, int> get stats {
    int userMessages = messages.where((msg) => msg.isUser).length;
    int aiMessages = messages.where((msg) => !msg.isUser).length;
    
    return {
      'total_messages': messages.length,
      'user_messages': userMessages,
      'ai_messages': aiMessages,
    };
  }

  // Create copy with updated fields
  Conversation copyWith({
    String? id,
    List<Message>? messages,
    DateTime? createdAt,
    DateTime? updatedAt,
    String? title,
    Map<String, dynamic>? metadata,
  }) {
    return Conversation(
      id: id ?? this.id,
      messages: messages ?? this.messages,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? DateTime.now(),
      title: title ?? this.title,
      metadata: metadata ?? this.metadata,
    );
  }

  // Convert to JSON for storage
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'messages': messages.map((msg) => msg.toJson()).toList(),
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt?.toIso8601String(),
      'title': title,
      'metadata': metadata,
    };
  }

  // Create from JSON
  factory Conversation.fromJson(Map<String, dynamic> json) {
    return Conversation(
      id: json['id'],
      messages: (json['messages'] as List)
          .map((msgJson) => Message.fromJson(msgJson))
          .toList(),
      createdAt: DateTime.parse(json['created_at']),
      updatedAt: json['updated_at'] != null 
          ? DateTime.parse(json['updated_at']) 
          : null,
      title: json['title'],
      metadata: json['metadata'] ?? {},
    );
  }

  @override
  String toString() {
    return 'Conversation(id: $id, messages: ${messages.length}, title: $displayTitle)';
  }
}

class Message {
  final String id;
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final Map<String, dynamic> metadata;
  final MessageType type;

  Message({
    String? id,
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.metadata = const {},
    this.type = MessageType.text,
  }) : id = id ?? const Uuid().v4();

  // Get message display info
  String get displayContent {
    switch (type) {
      case MessageType.text:
        return content;
      case MessageType.voice:
        return '🎤 Voice message: $content';
      case MessageType.image:
        return '📸 Image analysis: $content';
      case MessageType.error:
        return '❌ Error: $content';
      case MessageType.system:
        return '🔧 System: $content';
    }
  }

  // Get processing info from metadata
  String? get model => metadata['model'];
  double? get confidence => metadata['confidence'];
  int? get processingTime => metadata['processing_time'];
  String? get error => metadata['error'];

  // Check if message has attachments
  bool get hasAttachments => metadata.containsKey('attachments');
  List<dynamic> get attachments => metadata['attachments'] ?? [];

  // Create copy with updated fields
  Message copyWith({
    String? id,
    String? content,
    bool? isUser,
    DateTime? timestamp,
    Map<String, dynamic>? metadata,
    MessageType? type,
  }) {
    return Message(
      id: id ?? this.id,
      content: content ?? this.content,
      isUser: isUser ?? this.isUser,
      timestamp: timestamp ?? this.timestamp,
      metadata: metadata ?? this.metadata,
      type: type ?? this.type,
    );
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'content': content,
      'is_user': isUser,
      'timestamp': timestamp.toIso8601String(),
      'metadata': metadata,
      'type': type.name,
    };
  }

  // Create from JSON
  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      isUser: json['is_user'],
      timestamp: DateTime.parse(json['timestamp']),
      metadata: json['metadata'] ?? {},
      type: MessageType.values.firstWhere(
        (t) => t.name == json['type'],
        orElse: () => MessageType.text,
      ),
    );
  }

  @override
  String toString() {
    return 'Message(id: $id, isUser: $isUser, type: $type, content: ${content.substring(0, content.length > 50 ? 50 : content.length)}...)';
  }
}

enum MessageType {
  text,
  voice,
  image,
  error,
  system,
}

// Conversation filter and search
class ConversationFilter {
  final String? searchQuery;
  final DateTime? startDate;
  final DateTime? endDate;
  final bool? hasUserMessages;
  final bool? hasAiMessages;
  final MessageType? messageType;

  ConversationFilter({
    this.searchQuery,
    this.startDate,
    this.endDate,
    this.hasUserMessages,
    this.hasAiMessages,
    this.messageType,
  });

  bool matches(Conversation conversation) {
    // Search query filter
    if (searchQuery != null && searchQuery!.isNotEmpty) {
      final query = searchQuery!.toLowerCase();
      final titleMatch = conversation.displayTitle.toLowerCase().contains(query);
      final contentMatch = conversation.messages.any(
        (msg) => msg.content.toLowerCase().contains(query),
      );
      if (!titleMatch && !contentMatch) return false;
    }

    // Date range filter
    if (startDate != null && conversation.createdAt.isBefore(startDate!)) {
      return false;
    }
    if (endDate != null && conversation.createdAt.isAfter(endDate!)) {
      return false;
    }

    // Message type filters
    if (hasUserMessages != null) {
      final hasUser = conversation.messages.any((msg) => msg.isUser);
      if (hasUser != hasUserMessages) return false;
    }

    if (hasAiMessages != null) {
      final hasAi = conversation.messages.any((msg) => !msg.isUser);
      if (hasAi != hasAiMessages) return false;
    }

    if (messageType != null) {
      final hasType = conversation.messages.any((msg) => msg.type == messageType);
      if (!hasType) return false;
    }

    return true;
  }
}
