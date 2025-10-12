class Message {
  final String id;
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final bool isPending;

  Message({
    required this.id,
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.isPending = false,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'content': content,
      'isUser': isUser,
      'timestamp': timestamp.toIso8601String(),
      'isPending': isPending,
    };
  }

  factory Message.fromJson(Map<String, dynamic> json) {
    return Message(
      id: json['id'],
      content: json['content'],
      isUser: json['isUser'],
      timestamp: DateTime.parse(json['timestamp']),
      isPending: json['isPending'] ?? false,
    );
  }
}

class ChatSession {
  final String id;
  final String title;
  final DateTime createdAt;
  final List<Message> messages;

  ChatSession({
    required this.id,
    required this.title,
    required this.createdAt,
    required this.messages,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'createdAt': createdAt.toIso8601String(),
      'messages': messages.map((m) => m.toJson()).toList(),
    };
  }

  factory ChatSession.fromJson(Map<String, dynamic> json) {
    return ChatSession(
      id: json['id'],
      title: json['title'],
      createdAt: DateTime.parse(json['createdAt']),
      messages: (json['messages'] as List).map((m) => Message.fromJson(m)).toList(),
    );
  }
}

class ServerStatus {
  final bool isOnline;
  final bool atlesAvailable;
  final String version;
  final int activeSessions;
  final bool constitutionalProtection;

  ServerStatus({
    required this.isOnline,
    required this.atlesAvailable,
    required this.version,
    required this.activeSessions,
    required this.constitutionalProtection,
  });

  factory ServerStatus.fromJson(Map<String, dynamic> json) {
    return ServerStatus(
      isOnline: json['server']['status'] == 'online',
      atlesAvailable: json['atles']['available'],
      version: json['server']['version'],
      activeSessions: json['sessions']['active_count'],
      constitutionalProtection: json['atles']['constitutional_protection'],
    );
  }

  factory ServerStatus.offline() {
    return ServerStatus(
      isOnline: false,
      atlesAvailable: false,
      version: 'unknown',
      activeSessions: 0,
      constitutionalProtection: false,
    );
  }
}
