import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';
import '../providers/atles_provider.dart';
import '../widgets/message_bubble.dart';
import '../widgets/voice_button.dart';

class ChatScreen extends StatefulWidget {
  final String? conversationId;
  
  const ChatScreen({
    super.key,
    this.conversationId,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final FocusNode _messageFocusNode = FocusNode();
  
  bool _isComposing = false;

  @override
  void initState() {
    super.initState();
    _messageController.addListener(_onMessageChanged);
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    _messageFocusNode.dispose();
    super.dispose();
  }

  void _onMessageChanged() {
    setState(() {
      _isComposing = _messageController.text.trim().isNotEmpty;
    });
  }

  void _sendMessage() {
    final message = _messageController.text.trim();
    if (message.isEmpty) return;

    // Clear input immediately for better UX
    _messageController.clear();
    setState(() => _isComposing = false);

    // Send message to ATLES
    context.read<ATLESProvider>().sendMessage(message);

    // Scroll to bottom after a short delay
    Future.delayed(const Duration(milliseconds: 100), () {
      _scrollToBottom();
    });
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  void _onVoiceMessage(String message) {
    if (message.isNotEmpty) {
      context.read<ATLESProvider>().sendMessage(message);
      _scrollToBottom();
    }
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      appBar: widget.conversationId != null
          ? AppBar(
              title: const Text('Conversation'),
              actions: [
                Consumer<ATLESProvider>(
                  builder: (context, provider, child) {
                    return IconButton(
                      icon: Icon(
                        provider.isConnectedToDesktop
                            ? Icons.cloud_done
                            : Icons.cloud_off,
                      ),
                      onPressed: () => provider.syncWithDesktop(),
                      tooltip: provider.isConnectedToDesktop
                          ? 'Connected to desktop'
                          : 'Sync with desktop',
                    );
                  },
                ),
              ],
            )
          : null,
      body: Column(
        children: [
          // Status bar
          Consumer<ATLESProvider>(
            builder: (context, provider, child) {
              if (!provider.isProcessing && provider.conversations.isEmpty) {
                return Container(
                  width: double.infinity,
                  padding: const EdgeInsets.all(16),
                  color: theme.colorScheme.primaryContainer,
                  child: Column(
                    children: [
                      Icon(
                        Icons.psychology,
                        size: 48,
                        color: theme.colorScheme.primary,
                      ),
                      const SizedBox(height: 8),
                      Text(
                        'Welcome to ATLES-Mini!',
                        style: theme.textTheme.titleLarge?.copyWith(
                          color: theme.colorScheme.onPrimaryContainer,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 4),
                      Text(
                        'Your AI companion running locally on your device',
                        style: theme.textTheme.bodyMedium?.copyWith(
                          color: theme.colorScheme.onPrimaryContainer.withOpacity(0.8),
                        ),
                      ),
                      const SizedBox(height: 8),
                      Wrap(
                        spacing: 8,
                        children: [
                          Chip(
                            label: const Text('🔋 Offline-First'),
                            backgroundColor: theme.colorScheme.surface,
                          ),
                          Chip(
                            label: const Text('🔒 Privacy-First'),
                            backgroundColor: theme.colorScheme.surface,
                          ),
                          Chip(
                            label: Text('🤖 ${provider.currentModel}'),
                            backgroundColor: theme.colorScheme.surface,
                          ),
                        ],
                      ),
                    ],
                  ),
                );
              }
              return const SizedBox.shrink();
            },
          ),
          
          // Messages list
          Expanded(
            child: Consumer<ATLESProvider>(
              builder: (context, provider, child) {
                final conversation = provider.conversations.isNotEmpty
                    ? provider.conversations.last
                    : null;
                
                if (conversation == null || conversation.messages.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.chat_bubble_outline,
                          size: 64,
                          color: theme.colorScheme.onSurface.withOpacity(0.3),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Start a conversation',
                          style: theme.textTheme.titleMedium?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.6),
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          'Ask me anything! I\'m running locally on your device.',
                          textAlign: TextAlign.center,
                          style: theme.textTheme.bodyMedium?.copyWith(
                            color: theme.colorScheme.onSurface.withOpacity(0.5),
                          ),
                        ),
                      ],
                    ),
                  );
                }
                
                return ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  itemCount: conversation.messages.length + (provider.isProcessing ? 1 : 0),
                  itemBuilder: (context, index) {
                    // Show typing indicator
                    if (index == conversation.messages.length && provider.isProcessing) {
                      return Padding(
                        padding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 8,
                        ),
                        child: Row(
                          children: [
                            CircleAvatar(
                              radius: 16,
                              backgroundColor: theme.colorScheme.primary,
                              child: const Icon(
                                Icons.psychology,
                                color: Colors.white,
                                size: 16,
                              ),
                            ),
                            const SizedBox(width: 12),
                            Container(
                              padding: const EdgeInsets.symmetric(
                                horizontal: 16,
                                vertical: 12,
                              ),
                              decoration: BoxDecoration(
                                color: theme.colorScheme.surfaceVariant,
                                borderRadius: BorderRadius.circular(20),
                              ),
                              child: Row(
                                mainAxisSize: MainAxisSize.min,
                                children: [
                                  SizedBox(
                                    width: 16,
                                    height: 16,
                                    child: CircularProgressIndicator(
                                      strokeWidth: 2,
                                      color: theme.colorScheme.primary,
                                    ),
                                  ),
                                  const SizedBox(width: 8),
                                  Text(
                                    'Thinking...',
                                    style: theme.textTheme.bodyMedium?.copyWith(
                                      color: theme.colorScheme.onSurfaceVariant,
                                    ),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      );
                    }
                    
                    final message = conversation.messages[index];
                    return MessageBubble(
                      message: message,
                      onCopy: (text) {
                        Clipboard.setData(ClipboardData(text: text));
                        ScaffoldMessenger.of(context).showSnackBar(
                          const SnackBar(
                            content: Text('Message copied to clipboard'),
                            duration: Duration(seconds: 2),
                          ),
                        );
                      },
                    );
                  },
                );
              },
            ),
          ),
          
          // Input area
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: theme.colorScheme.surface,
              border: Border(
                top: BorderSide(
                  color: theme.colorScheme.outline.withOpacity(0.2),
                ),
              ),
            ),
            child: SafeArea(
              child: Row(
                children: [
                  // Voice input button
                  VoiceButton(
                    onVoiceMessage: _onVoiceMessage,
                  ),
                  const SizedBox(width: 8),
                  
                  // Text input
                  Expanded(
                    child: TextField(
                      controller: _messageController,
                      focusNode: _messageFocusNode,
                      decoration: InputDecoration(
                        hintText: 'Ask ATLES-Mini anything...',
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(24),
                          borderSide: BorderSide.none,
                        ),
                        filled: true,
                        fillColor: theme.colorScheme.surfaceVariant,
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 16,
                          vertical: 12,
                        ),
                      ),
                      maxLines: null,
                      textCapitalization: TextCapitalization.sentences,
                      onSubmitted: (_) => _sendMessage(),
                    ),
                  ),
                  const SizedBox(width: 8),
                  
                  // Send button
                  Consumer<ATLESProvider>(
                    builder: (context, provider, child) {
                      return AnimatedContainer(
                        duration: const Duration(milliseconds: 200),
                        child: IconButton(
                          onPressed: (_isComposing && !provider.isProcessing)
                              ? _sendMessage
                              : null,
                          icon: Icon(
                            Icons.send,
                            color: (_isComposing && !provider.isProcessing)
                                ? theme.colorScheme.primary
                                : theme.colorScheme.onSurface.withOpacity(0.3),
                          ),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}
