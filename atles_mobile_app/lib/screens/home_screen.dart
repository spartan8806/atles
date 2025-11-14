import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/atles_provider.dart';
import '../widgets/server_status_indicator.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _ipController = TextEditingController();
  final _portController = TextEditingController();
  bool _connecting = false;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addPostFrameCallback((_) {
      final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
      _ipController.text = atlesProvider.serverIp;
      _portController.text = atlesProvider.serverPort.toString();
      
      if (atlesProvider.isConnected) {
        _navigateToChat();
      }
    });
  }

  @override
  void dispose() {
    _ipController.dispose();
    _portController.dispose();
    super.dispose();
  }

  Future<void> _connectToServer() async {
    if (_ipController.text.isEmpty) {
      _showError('Please enter a server IP address');
      return;
    }
    
    int? port;
    try {
      port = int.parse(_portController.text);
    } catch (e) {
      _showError('Please enter a valid port number');
      return;
    }
    
    setState(() {
      _connecting = true;
    });
    
    final atlesProvider = Provider.of<AtlesProvider>(context, listen: false);
    await atlesProvider.setServerSettings(_ipController.text, port);
    
    final connected = await atlesProvider.checkConnection();
    
    setState(() {
      _connecting = false;
    });
    
    if (connected) {
      _navigateToChat();
    } else {
      _showError('Could not connect to ATLES server. Please check the settings and ensure the server is running.');
    }
  }

  void _navigateToChat() {
    Navigator.of(context).pushReplacementNamed('/chat');
  }

  void _showError(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: Colors.red,
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final atlesProvider = Provider.of<AtlesProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('ATLES Mobile'),
        actions: [
          IconButton(
            icon: const Icon(Icons.settings),
            onPressed: () => Navigator.of(context).pushNamed('/settings'),
          ),
        ],
      ),
      body: Center(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              // ATLES Logo
              Icon(
                Icons.psychology,
                size: 80,
                color: Theme.of(context).primaryColor,
              ),
              const SizedBox(height: 20),
              
              // Title
              Text(
                'ATLES Mobile',
                style: Theme.of(context).textTheme.headline4,
              ),
              const SizedBox(height: 10),
              
              // Subtitle
              Text(
                'Connect to your ATLES server',
                style: Theme.of(context).textTheme.subtitle1,
              ),
              const SizedBox(height: 40),
              
              // Server Status
              const ServerStatusIndicator(),
              const SizedBox(height: 20),
              
              // IP Address Input
              TextField(
                controller: _ipController,
                decoration: const InputDecoration(
                  labelText: 'Server IP Address',
                  hintText: 'e.g. 192.168.1.100',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.computer),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 20),
              
              // Port Input
              TextField(
                controller: _portController,
                decoration: const InputDecoration(
                  labelText: 'Server Port',
                  hintText: '8080',
                  border: OutlineInputBorder(),
                  prefixIcon: Icon(Icons.router),
                ),
                keyboardType: TextInputType.number,
              ),
              const SizedBox(height: 30),
              
              // Connect Button
              SizedBox(
                width: double.infinity,
                height: 50,
                child: ElevatedButton(
                  onPressed: _connecting ? null : _connectToServer,
                  child: _connecting
                      ? const CircularProgressIndicator(color: Colors.white)
                      : const Text('Connect to ATLES', style: TextStyle(fontSize: 18)),
                ),
              ),
              const SizedBox(height: 20),
              
              // Help Text
              const Text(
                'Make sure the ATLES API Server is running on your PC',
                textAlign: TextAlign.center,
                style: TextStyle(fontStyle: FontStyle.italic),
              ),
              const SizedBox(height: 40),
              
              // Version Info
              Text(
                'ATLES Mobile v1.0.0',
                style: Theme.of(context).textTheme.caption,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
