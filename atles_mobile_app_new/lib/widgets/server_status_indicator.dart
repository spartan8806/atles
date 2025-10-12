import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../providers/atles_provider.dart';

class ServerStatusIndicator extends StatelessWidget {
  const ServerStatusIndicator({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    final atlesProvider = Provider.of<AtlesProvider>(context);
    
    Color statusColor;
    String statusText;
    IconData statusIcon;
    
    if (atlesProvider.isConnecting) {
      statusColor = Colors.blue;
      statusText = 'Connecting...';
      statusIcon = Icons.sync;
    } else if (atlesProvider.isConnected) {
      statusColor = Colors.green;
      statusText = 'Connected to ATLES Server';
      statusIcon = Icons.check_circle;
    } else {
      statusColor = Colors.red;
      statusText = 'Not Connected';
      statusIcon = Icons.error_outline;
    }
    
    return Container(
      padding: const EdgeInsets.symmetric(vertical: 8, horizontal: 16),
      decoration: BoxDecoration(
        color: statusColor.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: statusColor.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(
            statusIcon,
            color: statusColor,
          ),
          const SizedBox(width: 8),
          Text(
            statusText,
            style: TextStyle(
              color: statusColor,
              fontWeight: FontWeight.bold,
            ),
          ),
        ],
      ),
    );
  }
}
