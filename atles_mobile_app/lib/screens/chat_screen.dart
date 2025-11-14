import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import '../providers/atles_provider.dart';
import '../widgets/message_bubble.dart';

class ChatScreen extends StatefulWidget {
  const ChatScreen({Key? key}) : super(key: key);

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final _messageController = TextEditingController();
  final _scrollController = ScrollController();
  bool _sendingMessage = false;

  @override
  void initState() {
    super.initState();
    // Ensure we refresh the messages when opening the chat
    WidgetsBinding.instance.addPostFrameCallback((_) {
      _checkConnection();
    });
  }

  @override
  void dispose() {
    _messageController.dispose();
    _scrollController.dispose();
    super.dispose();
  }

  Future<void> _checkConnection() async {
    final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
    if (!atlesProvider.isConnected) {
      final connected = await atlesProvider.checkConnection();
      if (!connected && mounted) {
        _showConnectionError();
      }
    }
  }

  void _showConnectionError() {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: const Text('Not connected to ATLES server'),
        backgroundColor: Colors.red,
        action: SnackBarAction(
          label: 'Connect',
          onPressed: () => Navigator.of(context).pushReplacementNamed('/'),
        ),
      ),
    );
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

  Future<void> _sendMessage() async {
    if (_messageController.text.trim().isEmpty) return;
    
    final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
    if (!atlesProvider.isConnected) {
      _showConnectionError();
      return;
    }
    
    setState(() {
      _sendingMessage = true;
    });
    
    final message = _messageController.text;
    _messageController.clear();
    
    await atlesProvider.sendMessage(message);
    
    setState(() {
      _sendingMessage = false;
    });
    
    // Wait a bit for the UI to update with new messages
    Future.delayed(const Duration(milliseconds: 100), _scrollToBottom);
  }

  void _startNewChat() {
    final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
    atlesProvider.startNewChat();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Chat with ATLES'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: () {
              final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
              atlesProvider.refresh();
            },
          ),
          IconButton(
            icon: const Icon(Icons.add),
            onPressed: _startNewChat,
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => Navigator.of(context).pushNamed('/settings'),
          ),
        ],
      ),
      body: Column(
        children: [
          // Chat Messages
          Expanded(
            child: Consumer<AtlesProvider>(
              builder: (context, atlesProvider, _) {
                final messages = atlesProvider.currentMessages;
                
                if (messages.isEmpty) {
                  return Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(
                          Icons.chat_bubble_outline,
                          size: 60,
                          color: Colors.grey[400],
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Start a conversation with ATLES',
                          style: TextStyle(
                            fontSize: 16,
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    ),
                  );
                }
                
                WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());
                
                return ListView.builder(
                  controller: _scrollController,
                  padding: const EdgeInsets.symmetric(vertical: 16, horizontal: 8),
                  itemCount: messages.length,
                  itemBuilder: (context, index) {
                    final message = messages[index];
                    return MessageBubble(
                      message: message.content,
                      isUser: message.isUser,
                      timestamp: message.timestamp,
                      isPending: message.isPending,
                    );
                  },
                );
              },
            ),
          ),
          
          // Input Field
          Container(
            decoration: BoxDecoration(
              color: Theme.of(context).cardColor,
              boxShadow: [
                BoxShadow(
                  color: Colors.black.withOpacity(0.1),
                  blurRadius: 5,
                  offset: const Offset(0, -1),
                ),
              ],
            ),
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
            child: Row(
              children: [
                // Input Text Field
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: const InputDecoration(
                      hintText: 'Type a message...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.all(Radius.circular(24)),
                      ),
                      contentPadding: EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                    ),
                    maxLines: 4,
                    minLines: 1,
                    textCapitalization: TextCapitalization.sentences,
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                
                // Send Button
                Material(
                  color: Theme.of(context).primaryColor,
                  borderRadius: BorderRadius.circular(24),
                  child: InkWell(
                    borderRadius: BorderRadius.circular(24),
                    onTap: _sendingMessage ? null : _sendMessage,
                    child: Container(
                      padding: const EdgeInsets.all(12),
                      child: _sendingMessage
                          ? const SizedBox(
                              width: 24,
                              height: 24,
                              child: CircularProgressIndicator(
                                strokeWidth: 2,
                                color: Colors.white,
                              ),
                            )
                          : const Icon(
                              Icons.send,
                              color: Colors.white,
                            ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
