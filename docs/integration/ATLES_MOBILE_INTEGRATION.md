# ATLES Mobile App Integration
## Connecting ATLES to Your Google Pixel 9

This guide provides detailed instructions for connecting ATLES to your Google Pixel 9 smartphone using a Flutter mobile app and the ATLES API server.

### Overview

The integration consists of two main components:
1. **ATLES API Server** - Runs on your PC and provides a secure interface for mobile apps
2. **ATLES Mobile App** - A Flutter app that runs on your Google Pixel 9 and connects to the API server

## Part 1: Setting Up the ATLES API Server

### Requirements
- Python 3.8+
- ATLES installed and working on your PC
- Flask (will be installed automatically)
- Your PC and phone on the same WiFi network

### Installation

1. Run the API server installation script:
   ```bash
   # Install required packages
   pip install flask flask-cors waitress
   ```

2. Start the ATLES API server:
   ```bash
   python atles_api_server.py
   ```

3. Note the displayed IP address and port (typically 8080).

### API Endpoints

The server provides the following REST API endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Check if the API server is running |
| `/api/chat` | POST | Send a message to ATLES |
| `/api/sessions/:id` | GET | Get message history for a session |
| `/api/sessions` | GET | List all active sessions |
| `/api/status` | GET | Get detailed server status |

## Part 2: Setting Up the Mobile App

### Requirements
- Flutter SDK (for building the app)
- Android Studio (for debugging)
- Flutter development environment setup
- Or alternatively, use the pre-built APK

### Option 1: Using the Pre-built APK

1. Download the ATLES Mobile app APK from the repository
2. Install it on your Google Pixel 9
3. Open the app and enter the API server details (IP address and port)
4. Connect and start chatting with ATLES

### Option 2: Building from Source

1. Clone the Flutter project repository
2. Install Flutter dependencies:
   ```bash
   cd atles_mobile_app
   flutter pub get
   ```

3. Build the app for Android:
   ```bash
   flutter build apk --release
   ```

4. Install the built APK on your Google Pixel 9

## Usage Instructions

### Connecting to ATLES

1. Start the ATLES API server on your PC
2. Open the ATLES Mobile app on your Google Pixel 9
3. Enter the server IP address and port shown by the API server
4. Tap "Connect"
5. Once connected, you can start chatting with ATLES

### Features

- **Chat Interface**: Send messages to ATLES and receive responses
- **Session Management**: All conversations are saved in sessions
- **Constitutional Protection**: The same constitutional rules apply to mobile interactions
- **Offline Mode**: The app works when connected to your home network (no internet required)

### Troubleshooting

If you have trouble connecting:

1. Make sure your phone and PC are on the same WiFi network
2. Check if your PC's firewall is blocking port 8080
3. Try restarting the API server
4. Verify the IP address is correct

## Security Considerations

1. The API server currently runs without HTTPS (secure only on your local network)
2. For remote access, additional security measures would be required
3. Do not expose the API server directly to the internet

## Future Enhancements

- HTTPS encryption for secure remote access
- User authentication
- Push notifications
- Voice interactions
- End-to-end encryption
- Cloud synchronization

## Technical Details

### API Request Format

To send a chat message:

```json
POST /api/chat
{
  "message": "Your message to ATLES here",
  "session_id": "optional-session-id"
}
```

### API Response Format

```json
{
  "session_id": "generated-session-id",
  "response": "ATLES response here"
}
```
