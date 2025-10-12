import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
// import 'package:flutter_markdown/flutter_markdown.dart';

class MessageBubble extends StatelessWidget {
  final String message;
  final bool isUser;
  final DateTime timestamp;
  final bool isPending;

  const MessageBubble({
    Key? key,
    required this.message,
    required this.isUser,
    required this.timestamp,
    this.isPending = false,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final timeFormat = DateFormat.jm();
    final formattedTime = timeFormat.format(timestamp);
    
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4, horizontal: 8),
      child: Column(
        crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              if (!isUser)
                Padding(
                  padding: const EdgeInsets.only(right: 8.0),
                  child: CircleAvatar(
                    backgroundColor: Colors.blue,
                    child: const Icon(Icons.psychology, color: Colors.white),
                    radius: 16,
                  ),
                ),
              
              // Message container
              Flexible(
                child: Container(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  decoration: BoxDecoration(
                    color: isUser
                        ? Theme.of(context).primaryColor
                        : Theme.of(context).brightness == Brightness.dark
                            ? Colors.grey[800]
                            : Colors.grey[300],
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Column(
                    crossAxisAlignment: isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
                    children: [
                      // Message Content
                      Text(
                        message,
                        style: TextStyle(
                          color: isUser ? Colors.white : null,
                          fontSize: 16,
                        ),
                      ),
                      
                      // Timestamp and Status
                      Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            formattedTime,
                            style: TextStyle(
                              fontSize: 10,
                              color: isUser ? Colors.white70 : Colors.grey,
                            ),
                          ),
                          if (isUser) ...[
                            const SizedBox(width: 4),
                            isPending
                                ? const SizedBox(
                                    width: 12,
                                    height: 12,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      color: Colors.white70,
                                    ),
                                  )
                                : const Icon(
                                    Icons.check,
                                    size: 12,
                                    color: Colors.white70,
                                  ),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
              ),
              
              if (isUser)
                Padding(
                  padding: const EdgeInsets.only(left: 8.0),
                  child: CircleAvatar(
                    backgroundColor: Colors.green,
                    child: const Icon(Icons.person, color: Colors.white),
                    radius: 16,
                  ),
                ),
            ],
          ),
        ],
      ),
    );
  }
}
