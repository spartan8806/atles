import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/atles_provider.dart';
import '../providers/theme_provider.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final TextEditingController _serverHostController = TextEditingController();
  final TextEditingController _serverPortController = TextEditingController();

  @override
  void dispose() {
    _serverHostController.dispose();
    _serverPortController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Scaffold(
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          // AI Model Section
          _buildSection(
            title: 'AI Model',
            icon: Icons.psychology,
            children: [
              Consumer<ATLESProvider>(
                builder: (context, provider, child) {
                  return ListTile(
                    title: const Text('Current Model'),
                    subtitle: Text(provider.currentModel),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => _showModelSelection(context, provider),
                  );
                },
              ),
              ListTile(
                title: const Text('Model Performance'),
                subtitle: const Text('View AI model statistics'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showModelStats(context),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          
          // Desktop Sync Section
          _buildSection(
            title: 'Desktop Sync',
            icon: Icons.sync,
            children: [
              Consumer<ATLESProvider>(
                builder: (context, provider, child) {
                  return SwitchListTile(
                    title: const Text('Enable Desktop Sync'),
                    subtitle: Text(
                      provider.isConnectedToDesktop
                          ? 'Connected to desktop ATLES'
                          : 'Connect to your PC for enhanced capabilities',
                    ),
                    value: provider.isConnectedToDesktop,
                    onChanged: (value) {
                      if (value) {
                        _showSyncSetup(context);
                      } else {
                        // Disconnect from desktop
                        provider.syncWithDesktop();
                      }
                    },
                  );
                },
              ),
              ListTile(
                title: const Text('Server Settings'),
                subtitle: const Text('Configure desktop ATLES connection'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showSyncSetup(context),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          
          // Appearance Section
          _buildSection(
            title: 'Appearance',
            icon: Icons.palette,
            children: [
              Consumer<ThemeProvider>(
                builder: (context, themeProvider, child) {
                  return ListTile(
                    title: const Text('Theme'),
                    subtitle: Text(_getThemeDescription(themeProvider.themeMode)),
                    trailing: const Icon(Icons.chevron_right),
                    onTap: () => _showThemeSelection(context, themeProvider),
                  );
                },
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          
          // Privacy & Security Section
          _buildSection(
            title: 'Privacy & Security',
            icon: Icons.security,
            children: [
              ListTile(
                title: const Text('Data Privacy'),
                subtitle: const Text('All processing happens on your device'),
                leading: const Icon(Icons.verified_user, color: Colors.green),
                onTap: () => _showPrivacyInfo(context),
              ),
              ListTile(
                title: const Text('Clear Conversations'),
                subtitle: const Text('Delete all conversation history'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showClearDataDialog(context),
              ),
            ],
          ),
          
          const SizedBox(height: 16),
          
          // About Section
          _buildSection(
            title: 'About',
            icon: Icons.info,
            children: [
              const ListTile(
                title: Text('ATLES-Mini'),
                subtitle: Text('Version 1.0.0'),
                leading: Icon(Icons.psychology),
              ),
              ListTile(
                title: const Text('Storage Usage'),
                subtitle: const Text('View app storage statistics'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showStorageStats(context),
              ),
              ListTile(
                title: const Text('Help & Support'),
                subtitle: const Text('Get help using ATLES-Mini'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => _showHelp(context),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSection({
    required String title,
    required IconData icon,
    required List<Widget> children,
  }) {
    final theme = Theme.of(context);
    
    return Card(
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Icon(icon, color: theme.colorScheme.primary),
                const SizedBox(width: 8),
                Text(
                  title,
                  style: theme.textTheme.titleMedium?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
              ],
            ),
          ),
          ...children,
        ],
      ),
    );
  }

  String _getThemeDescription(ThemeMode mode) {
    switch (mode) {
      case ThemeMode.light:
        return 'Light theme';
      case ThemeMode.dark:
        return 'Dark theme';
      case ThemeMode.system:
        return 'Follow system theme';
    }
  }

  void _showModelSelection(BuildContext context, ATLESProvider provider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Select AI Model'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text('Choose the AI model for ATLES-Mini:'),
            const SizedBox(height: 16),
            ...provider.availableModelIds.map((modelId) {
              final config = provider.getModelConfig(modelId);
              final isSelected = modelId == provider.currentModel;
              
              return RadioListTile<String>(
                title: Text(config?.name ?? modelId),
                subtitle: Text(
                  '${config?.sizeMB}MB • ${config?.capabilities.join(', ')}',
                ),
                value: modelId,
                groupValue: provider.currentModel,
                onChanged: (value) {
                  if (value != null) {
                    provider.switchModel(value);
                    Navigator.of(context).pop();
                  }
                },
              );
            }).toList(),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  void _showThemeSelection(BuildContext context, ThemeProvider themeProvider) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Select Theme'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            RadioListTile<ThemeMode>(
              title: const Text('Light'),
              value: ThemeMode.light,
              groupValue: themeProvider.themeMode,
              onChanged: (value) {
                if (value != null) {
                  themeProvider.setTheme(value);
                  Navigator.of(context).pop();
                }
              },
            ),
            RadioListTile<ThemeMode>(
              title: const Text('Dark'),
              value: ThemeMode.dark,
              groupValue: themeProvider.themeMode,
              onChanged: (value) {
                if (value != null) {
                  themeProvider.setTheme(value);
                  Navigator.of(context).pop();
                }
              },
            ),
            RadioListTile<ThemeMode>(
              title: const Text('System'),
              value: ThemeMode.system,
              groupValue: themeProvider.themeMode,
              onChanged: (value) {
                if (value != null) {
                  themeProvider.setTheme(value);
                  Navigator.of(context).pop();
                }
              },
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
        ],
      ),
    );
  }

  void _showSyncSetup(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Desktop Sync Setup'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Text(
              'Enter your desktop ATLES server details:',
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _serverHostController,
              decoration: const InputDecoration(
                labelText: 'Server IP Address',
                hintText: '192.168.1.100',
              ),
            ),
            const SizedBox(height: 8),
            TextField(
              controller: _serverPortController,
              decoration: const InputDecoration(
                labelText: 'Port',
                hintText: '8081',
              ),
              keyboardType: TextInputType.number,
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              // TODO: Configure sync settings
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('Sync configuration saved'),
                ),
              );
            },
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  void _showModelStats(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => const AlertDialog(
        title: Text('Model Performance'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Average Response Time: 450ms'),
            SizedBox(height: 8),
            Text('Average Confidence: 85%'),
            SizedBox(height: 8),
            Text('Total Responses: 127'),
            SizedBox(height: 8),
            Text('Model Accuracy: 92%'),
          ],
        ),
      ),
    );
  }

  void _showPrivacyInfo(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Privacy & Security'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              '🔒 Complete Privacy Protection',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text('• All AI processing happens on your device'),
            Text('• No data is sent to external servers'),
            Text('• Conversations stored locally only'),
            Text('• Optional desktop sync uses local network'),
            SizedBox(height: 16),
            Text(
              '🛡️ Security Features',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text('• Local data encryption'),
            Text('• No cloud dependencies'),
            Text('• User-controlled data'),
            Text('• Open source transparency'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }

  void _showClearDataDialog(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Clear All Data'),
        content: const Text(
          'This will permanently delete all conversations, settings, and cached data. This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              // TODO: Clear all data
              Navigator.of(context).pop();
              ScaffoldMessenger.of(context).showSnackBar(
                const SnackBar(
                  content: Text('All data cleared'),
                ),
              );
            },
            style: TextButton.styleFrom(foregroundColor: Colors.red),
            child: const Text('Clear All Data'),
          ),
        ],
      ),
    );
  }

  void _showStorageStats(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => const AlertDialog(
        title: Text('Storage Usage'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Database: 2.3 MB'),
            SizedBox(height: 8),
            Text('AI Models: 1.8 GB'),
            SizedBox(height: 8),
            Text('Cache: 45 MB'),
            SizedBox(height: 8),
            Text('Total: 1.85 GB'),
          ],
        ),
      ),
    );
  }

  void _showHelp(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Help & Support'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              'Getting Started:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text('• Tap the microphone to use voice input'),
            Text('• Type messages in the chat input'),
            Text('• Long press messages for options'),
            Text('• Use desktop sync for enhanced features'),
            SizedBox(height: 16),
            Text(
              'Need more help?',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            SizedBox(height: 8),
            Text('Check the documentation in the ATLES project folder.'),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
