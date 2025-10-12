# ATLES Mobile App for Google Pixel 9

## Overview
This Flutter app connects to your ATLES server running on your PC, allowing you to chat with ATLES from your Google Pixel 9 smartphone.

## Features
- Chat interface with ATLES
- Constitutional protection enforcement
- Session management
- Light/dark theme support
- Markdown message formatting

## Prerequisites
- Flutter SDK installed
- Android Studio or VS Code with Flutter plugin
- A device or emulator running Android

## Building the App
1. Install Flutter dependencies:
   ```bash
   flutter pub get
   ```

2. Run the app in debug mode:
   ```bash
   flutter run
   ```

3. Build release APK:
   ```bash
   flutter build apk --release
   ```

4. Build app bundle for Play Store:
   ```bash
   flutter build appbundle
   ```

## Installation
Transfer the built APK to your Google Pixel 9 and install it.

## Usage
1. Start the ATLES API server on your PC
2. Open the app on your Google Pixel 9
3. Enter your PC's local IP address and port (default: 8080)
4. Connect and start chatting with ATLES

## Development
Feel free to customize this app to your needs. The main code structure:

- `lib/`
  - `main.dart` - App entry point
  - `models/` - Data models
  - `providers/` - State management
  - `screens/` - App screens
  - `widgets/` - Reusable UI components

## API Server
The app requires the ATLES API server running on your PC. Start it with:
```bash
python atles_api_server.py
```
