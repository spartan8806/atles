import 'package:flutter/material.dart';

void main() {
  runApp(const ATLESMiniApp());
}

class ATLESMiniApp extends StatelessWidget {
  const ATLESMiniApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'ATLES-Mini',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: const Color(0xFF00D4FF),
          brightness: Brightness.dark,
        ),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
    );
  }
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final TextEditingController _messageController = TextEditingController();
  final List<String> _messages = ['🎉 ATLES-Mini is live on your Pixel 9 with Android 16! 🚀'];

  void _sendMessage() {
    final message = _messageController.text.trim();
    if (message.isEmpty) return;

    setState(() {
      _messages.add('You: $message');
      _messages.add('ATLES-Mini: I received "$message" - I\'m your AI companion! 🤖✨');
    });
    
    _messageController.clear();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: const Color(0xFF00D4FF),
        title: const Row(
          children: [
            Icon(Icons.psychology, color: Colors.white, size: 24),
            SizedBox(width: 8),
            Text('ATLES-Mini', style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
      body: Column(
        children: [
          // Welcome banner
          Container(
            width: double.infinity,
            padding: const EdgeInsets.all(16),
            color: const Color(0xFF00D4FF).withOpacity(0.1),
            child: const Column(
              children: [
                Icon(Icons.psychology, size: 48, color: Color(0xFF00D4FF)),
                SizedBox(height: 8),
                Text('🎉 ATLES-Mini Working!', 
                     style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                Text('Your AI companion on Android 16'),
              ],
            ),
          ),
          
          // Messages
          Expanded(
            child: ListView.builder(
              padding: const EdgeInsets.all(16),
              itemCount: _messages.length,
              itemBuilder: (context, index) {
                final message = _messages[index];
                final isUser = message.startsWith('You:');
                
                return Padding(
                  padding: const EdgeInsets.symmetric(vertical: 4),
                  child: Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: isUser ? const Color(0xFF00D4FF) : Colors.grey[800],
                      borderRadius: BorderRadius.circular(16),
                    ),
                    child: Text(
                      message,
                      style: TextStyle(
                        color: isUser ? Colors.black : Colors.white,
                      ),
                    ),
                  ),
                );
              },
            ),
          ),
          
          // Input
          Container(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _messageController,
                    decoration: InputDecoration(
                      hintText: 'Chat with ATLES-Mini...',
                      border: OutlineInputBorder(
                        borderRadius: BorderRadius.circular(24),
                      ),
                    ),
                    onSubmitted: (_) => _sendMessage(),
                  ),
                ),
                const SizedBox(width: 8),
                FloatingActionButton(
                  onPressed: _sendMessage,
                  backgroundColor: const Color(0xFF00D4FF),
                  child: const Icon(Icons.send, color: Colors.white),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}