import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/theme_provider.dart';
import '../providers/atles_provider.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);
    final atlesProvider = Provider.of<AtlesProvider>(context);
    
    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
      ),
      body: ListView(
        children: [
          // App Settings
          const ListTile(
            title: Text(
              'App Settings',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          
          // Theme Settings
          ListTile(
            title: const Text('Theme'),
            subtitle: const Text('Choose app appearance'),
            leading: const Icon(Icons.color_lens_outlined),
            trailing: DropdownButton<ThemeMode>(
              value: themeProvider.themeMode,
              onChanged: (ThemeMode? newValue) {
                if (newValue != null) {
                  themeProvider.setThemeMode(newValue);
                }
              },
              items: const [
                DropdownMenuItem(
                  value: ThemeMode.system,
                  child: Text('System'),
                ),
                DropdownMenuItem(
                  value: ThemeMode.light,
                  child: Text('Light'),
                ),
                DropdownMenuItem(
                  value: ThemeMode.dark,
                  child: Text('Dark'),
                ),
              ],
            ),
          ),
          
          const Divider(),
          
          // Server Settings
          const ListTile(
            title: Text(
              'Server Settings',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          
          // Server Status
          ListTile(
            title: const Text('Connection Status'),
            subtitle: Text(atlesProvider.isConnected ? 'Connected' : 'Disconnected'),
            leading: const Icon(Icons.cloud_outlined),
            trailing: atlesProvider.isConnected
                ? const Icon(Icons.check_circle, color: Colors.green)
                : const Icon(Icons.error_outline, color: Colors.red),
          ),
          
          // Server IP
          ListTile(
            title: const Text('Server IP'),
            subtitle: Text(atlesProvider.serverIp.isEmpty ? 'Not set' : atlesProvider.serverIp),
            leading: const Icon(Icons.computer),
          ),
          
          // Server Port
          ListTile(
            title: const Text('Server Port'),
            subtitle: Text(atlesProvider.serverPort.toString()),
            leading: const Icon(Icons.router),
          ),
          
          // Reconnect Button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
            child: ElevatedButton(
              onPressed: () async {
                // Show loading dialog
                showDialog(
                  context: context,
                  barrierDismissible: false,
                  builder: (ctx) => const AlertDialog(
                    content: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        CircularProgressIndicator(),
                        SizedBox(height: 16),
                        Text('Connecting to server...'),
                      ],
                    ),
                  ),
                );
                
                // Try to connect
                final connected = await atlesProvider.checkConnection();
                
                // Close the dialog
                Navigator.of(context).pop();
                
                // Show result
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(
                    content: Text(
                      connected ? 'Connected successfully' : 'Failed to connect',
                    ),
                    backgroundColor: connected ? Colors.green : Colors.red,
                  ),
                );
              },
              child: const Text('Reconnect to Server'),
            ),
          ),
          
          const Divider(),
          
          // About Section
          const ListTile(
            title: Text(
              'About',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
          ),
          
          // App Version
          const ListTile(
            title: Text('App Version'),
            subtitle: Text('1.0.0'),
            leading: Icon(Icons.info_outline),
          ),
          
          // ATLES Status
          ListTile(
            title: const Text('ATLES Status'),
            subtitle: Text(atlesProvider.isConnected && atlesProvider.serverStatus.atlesAvailable
                ? 'Available'
                : 'Unavailable'),
            leading: const Icon(Icons.psychology_outlined),
            trailing: atlesProvider.isConnected && atlesProvider.serverStatus.atlesAvailable
                ? const Icon(Icons.check_circle, color: Colors.green)
                : const Icon(Icons.error_outline, color: Colors.red),
          ),
          
          // Constitutional Protection
          if (atlesProvider.isConnected)
            ListTile(
              title: const Text('Constitutional Protection'),
              subtitle: Text(atlesProvider.serverStatus.constitutionalProtection
                  ? 'Enabled'
                  : 'Disabled'),
              leading: const Icon(Icons.security),
              trailing: atlesProvider.serverStatus.constitutionalProtection
                  ? const Icon(Icons.check_circle, color: Colors.green)
                  : const Icon(Icons.error_outline, color: Colors.red),
            ),
          
          // Reset Button
          Padding(
            padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 16),
            child: OutlinedButton(
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Reset Connection'),
                    content: const Text(
                      'This will clear your server settings and return to the connection screen. Continue?',
                    ),
                    actions: [
                      TextButton(
                        onPressed: () => Navigator.of(ctx).pop(),
                        child: const Text('Cancel'),
                      ),
                      TextButton(
                        onPressed: () {
                          Navigator.of(ctx).pop();
                          atlesProvider.setServerSettings('', 8080);
                          Navigator.of(context).pushReplacementNamed('/');
                        },
                        child: const Text('Reset'),
                      ),
                    ],
                  ),
                );
              },
              child: const Text('Reset Connection'),
            ),
          ),
        ],
      ),
    );
  }
}
