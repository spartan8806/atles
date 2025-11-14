import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/atles_provider.dart';

class SyncIndicator extends StatefulWidget {
  const SyncIndicator({super.key});

  @override
  State<SyncIndicator> createState() => _SyncIndicatorState();
}

class _SyncIndicatorState extends State<SyncIndicator>
    with TickerProviderStateMixin {
  late AnimationController _pulseController;
  late Animation<double> _pulseAnimation;

  @override
  void initState() {
    super.initState();
    _pulseController = AnimationController(
      duration: const Duration(seconds: 2),
      vsync: this,
    );
    _pulseAnimation = Tween<double>(
      begin: 0.5,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _pulseController,
      curve: Curves.easeInOut,
    ));
    
    _pulseController.repeat(reverse: true);
  }

  @override
  void dispose() {
    _pulseController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    
    return Consumer<ATLESProvider>(
      builder: (context, provider, child) {
        final isConnected = provider.isConnectedToDesktop;
        
        return GestureDetector(
          onTap: () => _showSyncDetails(context, provider),
          child: Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
            margin: const EdgeInsets.only(right: 8),
            decoration: BoxDecoration(
              color: isConnected
                  ? Colors.green.withOpacity(0.1)
                  : Colors.grey.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
              border: Border.all(
                color: isConnected
                    ? Colors.green.withOpacity(0.3)
                    : Colors.grey.withOpacity(0.3),
              ),
            ),
            child: Row(
              mainAxisSize: MainAxisSize.min,
              children: [
                AnimatedBuilder(
                  animation: _pulseAnimation,
                  builder: (context, child) {
                    return Transform.scale(
                      scale: isConnected ? _pulseAnimation.value : 1.0,
                      child: Icon(
                        isConnected ? Icons.cloud_done : Icons.cloud_off,
                        size: 16,
                        color: isConnected ? Colors.green : Colors.grey,
                      ),
                    );
                  },
                ),
                const SizedBox(width: 4),
                Text(
                  isConnected ? 'Synced' : 'Offline',
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: isConnected ? Colors.green : Colors.grey,
                    fontWeight: FontWeight.w500,
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  void _showSyncDetails(BuildContext context, ATLESProvider provider) {
    showModalBottomSheet(
      context: context,
      builder: (context) => SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                children: [
                  Icon(
                    provider.isConnectedToDesktop
                        ? Icons.cloud_done
                        : Icons.cloud_off,
                    color: provider.isConnectedToDesktop
                        ? Colors.green
                        : Colors.grey,
                  ),
                  const SizedBox(width: 8),
                  Text(
                    'Desktop Sync Status',
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ],
              ),
              const SizedBox(height: 16),
              
              _buildStatusRow(
                'Connection',
                provider.isConnectedToDesktop ? 'Connected' : 'Disconnected',
                provider.isConnectedToDesktop ? Colors.green : Colors.red,
              ),
              
              _buildStatusRow(
                'Mode',
                provider.isConnectedToDesktop 
                    ? 'Hybrid (Mobile + Desktop)'
                    : 'Offline-Only (Mobile)',
                provider.isConnectedToDesktop ? Colors.blue : Colors.orange,
              ),
              
              _buildStatusRow(
                'AI Model',
                provider.currentModel,
                Colors.purple,
              ),
              
              const SizedBox(height: 16),
              
              if (provider.isConnectedToDesktop) ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.green.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.green.withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.check_circle, color: Colors.green, size: 16),
                          const SizedBox(width: 8),
                          Text(
                            'Enhanced Capabilities Active',
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              fontWeight: FontWeight.w500,
                              color: Colors.green,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        '• Complex queries use desktop ATLES\n'
                        '• Conversations sync automatically\n'
                        '• Shared memory and learning\n'
                        '• Enhanced processing power',
                        style: TextStyle(fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ] else ...[
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.orange.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.orange.withOpacity(0.3)),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        children: [
                          const Icon(Icons.offline_bolt, color: Colors.orange, size: 16),
                          const SizedBox(width: 8),
                          Text(
                            'Offline Mode Active',
                            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                              fontWeight: FontWeight.w500,
                              color: Colors.orange,
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 8),
                      const Text(
                        '• All processing on your device\n'
                        '• Complete privacy protection\n'
                        '• Works anywhere without internet\n'
                        '• Local AI model responses',
                        style: TextStyle(fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
              
              const SizedBox(height: 16),
              
              Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () {
                        Navigator.of(context).pop();
                        provider.syncWithDesktop();
                      },
                      icon: const Icon(Icons.sync),
                      label: const Text('Sync Now'),
                    ),
                  ),
                  const SizedBox(width: 8),
                  Expanded(
                    child: OutlinedButton.icon(
                      onPressed: () {
                        Navigator.of(context).pop();
                        _showSyncSettings(context);
                      },
                      icon: const Icon(Icons.settings),
                      label: const Text('Settings'),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildStatusRow(String label, String value, Color color) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(
            label,
            style: const TextStyle(fontWeight: FontWeight.w500),
          ),
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 2),
            decoration: BoxDecoration(
              color: color.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Text(
              value,
              style: TextStyle(
                color: color,
                fontSize: 12,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ],
      ),
    );
  }

  void _showSyncSettings(BuildContext context) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Sync Settings'),
        content: const Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Text('Desktop sync settings will be available in the Settings tab.'),
            SizedBox(height: 16),
            Text(
              'Configure your desktop ATLES connection, sync preferences, and collaboration settings.',
              style: TextStyle(fontSize: 12),
            ),
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('Close'),
          ),
          TextButton(
            onPressed: () {
              Navigator.of(context).pop();
              // Navigate to settings - this would be implemented with proper navigation
            },
            child: const Text('Open Settings'),
          ),
        ],
      ),
    );
  }
}
