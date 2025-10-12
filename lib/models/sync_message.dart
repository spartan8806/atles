import 'conversation.dart';

class SyncMessage {
  final String id;
  final SyncMessageType type;
  final String deviceId;
  final DateTime timestamp;
  final Map<String, dynamic> data;
  final SyncPriority priority;

  SyncMessage({
    required this.id,
    required this.type,
    required this.deviceId,
    required this.timestamp,
    required this.data,
    this.priority = SyncPriority.normal,
  });

  // Create specific sync message types
  factory SyncMessage.conversationSync({
    required String deviceId,
    required List<Conversation> conversations,
  }) {
    return SyncMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      type: SyncMessageType.conversationSync,
      deviceId: deviceId,
      timestamp: DateTime.now(),
      data: {
        'conversations': conversations.map((c) => c.toJson()).toList(),
      },
    );
  }

  factory SyncMessage.collaborationRequest({
    required String deviceId,
    required String query,
    required String requestType,
    Map<String, dynamic> context = const {},
  }) {
    return SyncMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      type: SyncMessageType.collaborationRequest,
      deviceId: deviceId,
      timestamp: DateTime.now(),
      priority: SyncPriority.high,
      data: {
        'query': query,
        'request_type': requestType,
        'context': context,
      },
    );
  }

  factory SyncMessage.statusUpdate({
    required String deviceId,
    required DeviceStatus status,
    Map<String, dynamic> details = const {},
  }) {
    return SyncMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      type: SyncMessageType.statusUpdate,
      deviceId: deviceId,
      timestamp: DateTime.now(),
      data: {
        'status': status.name,
        'details': details,
      },
    );
  }

  factory SyncMessage.modelUpdate({
    required String deviceId,
    required String modelName,
    required String version,
    required int sizeBytes,
  }) {
    return SyncMessage(
      id: DateTime.now().millisecondsSinceEpoch.toString(),
      type: SyncMessageType.modelUpdate,
      deviceId: deviceId,
      timestamp: DateTime.now(),
      data: {
        'model_name': modelName,
        'version': version,
        'size_bytes': sizeBytes,
      },
    );
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'type': type.name,
      'device_id': deviceId,
      'timestamp': timestamp.toIso8601String(),
      'data': data,
      'priority': priority.name,
    };
  }

  // Create from JSON
  factory SyncMessage.fromJson(Map<String, dynamic> json) {
    return SyncMessage(
      id: json['id'],
      type: SyncMessageType.values.firstWhere(
        (t) => t.name == json['type'],
      ),
      deviceId: json['device_id'],
      timestamp: DateTime.parse(json['timestamp']),
      data: json['data'],
      priority: SyncPriority.values.firstWhere(
        (p) => p.name == json['priority'],
        orElse: () => SyncPriority.normal,
      ),
    );
  }

  @override
  String toString() {
    return 'SyncMessage(id: $id, type: $type, device: $deviceId, priority: $priority)';
  }
}

enum SyncMessageType {
  conversationSync,     // Sync conversations between devices
  collaborationRequest, // Request help from desktop ATLES
  collaborationResponse,// Response from desktop ATLES
  statusUpdate,         // Device status update
  modelUpdate,          // AI model update notification
  memorySync,           // Memory and preferences sync
  capabilityRequest,    // Request new capabilities
  ping,                 // Keep-alive message
  pong,                 // Keep-alive response
}

enum SyncPriority {
  low,      // Background sync, can be delayed
  normal,   // Regular sync operations
  high,     // Important operations, process quickly
  urgent,   // Critical operations, process immediately
}

enum DeviceStatus {
  online,           // Device is online and ready
  offline,          // Device is offline
  syncing,          // Currently syncing data
  processing,       // Processing AI request
  lowBattery,       // Battery is low
  error,            // Device has an error
  updating,         // Updating models or software
}

// Sync statistics and monitoring
class SyncStats {
  final int totalMessagesSent;
  final int totalMessagesReceived;
  final int conversationsSynced;
  final int collaborationRequests;
  final DateTime lastSyncTime;
  final Duration averageSyncTime;
  final Map<SyncMessageType, int> messageTypeDistribution;

  SyncStats({
    required this.totalMessagesSent,
    required this.totalMessagesReceived,
    required this.conversationsSynced,
    required this.collaborationRequests,
    required this.lastSyncTime,
    required this.averageSyncTime,
    required this.messageTypeDistribution,
  });

  // Calculate sync efficiency
  double get syncEfficiency {
    if (totalMessagesSent == 0) return 0.0;
    return totalMessagesReceived / totalMessagesSent;
  }

  // Get most common message type
  SyncMessageType? get mostCommonMessageType {
    if (messageTypeDistribution.isEmpty) return null;
    return messageTypeDistribution.entries
        .reduce((a, b) => a.value > b.value ? a : b)
        .key;
  }

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'total_messages_sent': totalMessagesSent,
      'total_messages_received': totalMessagesReceived,
      'conversations_synced': conversationsSynced,
      'collaboration_requests': collaborationRequests,
      'last_sync_time': lastSyncTime.toIso8601String(),
      'average_sync_time_ms': averageSyncTime.inMilliseconds,
      'message_type_distribution': messageTypeDistribution.map(
        (key, value) => MapEntry(key.name, value),
      ),
    };
  }

  // Create from JSON
  factory SyncStats.fromJson(Map<String, dynamic> json) {
    final messageTypeDistribution = <SyncMessageType, int>{};
    final distribution = json['message_type_distribution'] as Map<String, dynamic>?;
    
    if (distribution != null) {
      for (final entry in distribution.entries) {
        final type = SyncMessageType.values.firstWhere(
          (t) => t.name == entry.key,
          orElse: () => SyncMessageType.ping,
        );
        messageTypeDistribution[type] = entry.value;
      }
    }

    return SyncStats(
      totalMessagesSent: json['total_messages_sent'],
      totalMessagesReceived: json['total_messages_received'],
      conversationsSynced: json['conversations_synced'],
      collaborationRequests: json['collaboration_requests'],
      lastSyncTime: DateTime.parse(json['last_sync_time']),
      averageSyncTime: Duration(milliseconds: json['average_sync_time_ms']),
      messageTypeDistribution: messageTypeDistribution,
    );
  }

  @override
  String toString() {
    return 'SyncStats(sent: $totalMessagesSent, received: $totalMessagesReceived, efficiency: ${(syncEfficiency * 100).toStringAsFixed(1)}%)';
  }
}

// Device information for sync
class DeviceInfo {
  final String deviceId;
  final String deviceName;
  final String model;
  final String osVersion;
  final int ramMB;
  final int availableStorageMB;
  final List<String> capabilities;
  final Map<String, String> installedModels;

  DeviceInfo({
    required this.deviceId,
    required this.deviceName,
    required this.model,
    required this.osVersion,
    required this.ramMB,
    required this.availableStorageMB,
    required this.capabilities,
    required this.installedModels,
  });

  // Convert to JSON
  Map<String, dynamic> toJson() {
    return {
      'device_id': deviceId,
      'device_name': deviceName,
      'model': model,
      'os_version': osVersion,
      'ram_mb': ramMB,
      'available_storage_mb': availableStorageMB,
      'capabilities': capabilities,
      'installed_models': installedModels,
    };
  }

  // Create from JSON
  factory DeviceInfo.fromJson(Map<String, dynamic> json) {
    return DeviceInfo(
      deviceId: json['device_id'],
      deviceName: json['device_name'],
      model: json['model'],
      osVersion: json['os_version'],
      ramMB: json['ram_mb'],
      availableStorageMB: json['available_storage_mb'],
      capabilities: List<String>.from(json['capabilities']),
      installedModels: Map<String, String>.from(json['installed_models']),
    );
  }

  @override
  String toString() {
    return 'DeviceInfo(id: $deviceId, model: $model, ram: ${ramMB}MB)';
  }
}
