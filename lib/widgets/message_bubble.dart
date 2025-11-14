import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import '../models/conversation.dart';

class MessageBubble extends StatelessWidget {
  final Message message;
  final Function(String)? onCopy;
  
  const MessageBubble({
    super.key,
    required this.message,
    this.onCopy,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isUser = message.isUser;
    
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
      child: Row(
        mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            CircleAvatar(
              radius: 16,
              backgroundColor: theme.colorScheme.primary,
              child: Icon(
                _getMessageIcon(),
                color: Colors.white,
                size: 16,
              ),
            ),
            const SizedBox(width: 8),
          ],
          
          Flexible(
            child: Container(
              constraints: BoxConstraints(
                maxWidth: MediaQuery.of(context).size.width * 0.75,
              ),
              child: Column(
                crossAxisAlignment: isUser 
                    ? CrossAxisAlignment.end 
                    : CrossAxisAlignment.start,
                children: [
                  // Message bubble
                  GestureDetector(
                    onLongPress: () => _showMessageOptions(context),
                    child: Container(
                      padding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                      decoration: BoxDecoration(
                        color: isUser
                            ? theme.colorScheme.primary
                            : theme.colorScheme.surfaceVariant,
                        borderRadius: BorderRadius.circular(20).copyWith(
                          bottomLeft: isUser ? const Radius.circular(20) : const Radius.circular(4),
                          bottomRight: isUser ? const Radius.circular(4) : const Radius.circular(20),
                        ),
                      ),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          // Message content
                          SelectableText(
                            message.displayContent,
                            style: theme.textTheme.bodyMedium?.copyWith(
                              color: isUser
                                  ? Colors.white
                                  : theme.colorScheme.onSurfaceVariant,
                            ),
                          ),
                          
                          // Message metadata for AI responses
                          if (!isUser && _hasMetadata()) ...[
                            const SizedBox(height: 8),
                            _buildMetadata(context),
                          ],
                        ],
                      ),
                    ),
                  ),
                  
                  // Timestamp and status
                  Padding(
                    padding: const EdgeInsets.only(top: 4),
                    child: Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        Text(
                          _formatTimestamp(),
                          style: theme.textTheme.bodySmall?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.6),
                          ),
                        ),
                        if (!isUser && message.confidence != null) ...[
                          const SizedBox(width: 4),
                          Icon(
                            _getConfidenceIcon(),
                            size: 12,
                            color: _getConfidenceColor(theme),
                          ),
                        ],
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          
          if (isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              radius: 16,
              backgroundColor: theme.colorScheme.secondary,
              child: const Icon(
                Icons.person,
                color: Colors.white,
                size: 16,
              ),
            ),
          ],
        ],
      ),
    );
  }

  IconData _getMessageIcon() {
    switch (message.type) {
      case MessageType.voice:
        return Icons.mic;
      case MessageType.image:
        return Icons.camera_alt;
      case MessageType.error:
        return Icons.error;
      case MessageType.system:
        return Icons.settings;
      default:
        return Icons.psychology;
    }
  }

  bool _hasMetadata() {
    return message.model != null || 
           message.confidence != null || 
           message.processingTime != null;
  }

  Widget _buildMetadata(BuildContext context) {
    final theme = Theme.of(context);
    
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: theme.colorScheme.surface.withOpacity(0.3),
        borderRadius: BorderRadius.circular(8),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (message.model != null) ...[
            Icon(
              Icons.memory,
              size: 12,
              color: theme.colorScheme.onSurfaceVariant.withOpacity(0.7),
            ),
            const SizedBox(width: 4),
            Text(
              message.model!,
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.onSurfaceVariant.withOpacity(0.7),
                fontSize: 10,
              ),
            ),
          ],
          if (message.processingTime != null) ...[
            if (message.model != null) const SizedBox(width: 8),
            Icon(
              Icons.speed,
              size: 12,
              color: theme.colorScheme.onSurfaceVariant.withOpacity(0.7),
            ),
            const SizedBox(width: 4),
            Text(
              '${message.processingTime}ms',
              style: theme.textTheme.bodySmall?.copyWith(
                color: theme.colorScheme.onSurfaceVariant.withOpacity(0.7),
                fontSize: 10,
              ),
            ),
          ],
        ],
      ),
    );
  }

  IconData _getConfidenceIcon() {
    final confidence = message.confidence ?? 0.0;
    if (confidence > 0.8) return Icons.check_circle;
    if (confidence > 0.5) return Icons.help;
    return Icons.warning;
  }

  Color _getConfidenceColor(ThemeData theme) {
    final confidence = message.confidence ?? 0.0;
    if (confidence > 0.8) return Colors.green;
    if (confidence > 0.5) return Colors.orange;
    return Colors.red;
  }

  String _formatTimestamp() {
    final now = DateTime.now();
    final messageTime = message.timestamp;
    
    if (now.day == messageTime.day &&
        now.month == messageTime.month &&
        now.year == messageTime.year) {
      // Same day - show time only
      return '${messageTime.hour.toString().padLeft(2, '0')}:${messageTime.minute.toString().padLeft(2, '0')}';
    } else {
      // Different day - show date and time
      return '${messageTime.day}/${messageTime.month} ${messageTime.hour.toString().padLeft(2, '0')}:${messageTime.minute.toString().padLeft(2, '0')}';
    }
  }

  void _showMessageOptions(BuildContext context) {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.copy),
              title: const Text('Copy message'),
              onTap: () {
                Navigator.of(context).pop();
                onCopy?.call(message.content);
              },
            ),
            if (!message.isUser && message.model != null) ...[
              ListTile(
                leading: const Icon(Icons.info),
                title: const Text('Message details'),
                onTap: () {
                  Navigator.of(context).pop();
                  _showMessageDetails(context);
                },
              ),
            ],
          ],
        ),
      ),
    );
  }

  void _showMessageDetails(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Message Details'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            if (message.model != null) ...[
              Text('Model: ${message.model}'),
              const SizedBox(height: 8),
            ],
            if (message.confidence != null) ...[
              Text('Confidence: ${(message.confidence! * 100).toStringAsFixed(1)}%'),
              const SizedBox(height: 8),
            ],
            if (message.processingTime != null) ...[
              Text('Processing Time: ${message.processingTime}ms'),
              const SizedBox(height: 8),
            ],
            Text('Type: ${message.type.name}'),
            const SizedBox(height: 8),
            Text('Timestamp: ${message.timestamp}'),
            if (message.metadata.isNotEmpty) ...[
              const SizedBox(height: 8),
              const Text('Metadata:'),
              Text(
                message.metadata.toString(),
                style: Theme.of(context).textTheme.bodySmall,
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
          TextButton(
            onPressed: () {
              Clipboard.setData(ClipboardData(
                text: 'Message: ${message.content}\n'
                      'Model: ${message.model}\n'
                      'Confidence: ${message.confidence}\n'
                      'Processing Time: ${message.processingTime}ms\n'
                      'Timestamp: ${message.timestamp}',
              ));
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Details copied to clipboard'),
                  duration: Duration(seconds: 2),
                ),
              );
            },
            child: const Text('Copy Details'),
          ),
        ],
      ),
    );
  }
}
