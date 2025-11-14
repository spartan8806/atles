# Deploy ATLES Mobile App to Google Pixel 9

## Current Status ✅
- ✅ Google Pixel 9 connected and authorized (Device ID: 52120DLAQ0003V)
- ✅ Android Studio installed and opening your Flutter project
- ✅ Flutter app code is ready in `atles_mobile_app/` directory
- ✅ ATLES API server ready in `atles_api_server.py`

## Method 1: Using Android Studio (RECOMMENDED - Currently Opening)

Android Studio should be opening with your Flutter project. Follow these steps:

### Step 1: Install Flutter Plugin (if needed)
1. If prompted, install the Flutter plugin
2. Click "Install" and restart Android Studio if needed

### Step 2: Get Dependencies
1. You should see a banner saying "Packages get has not been run"
2. Click "Get dependencies" or "Pub get"
3. Wait for dependencies to download

### Step 3: Build and Run
1. Make sure your Pixel 9 is selected in the device dropdown (top toolbar)
2. Click the green ▶️ play button
3. Choose "Run" (not Debug) for better performance
4. Wait for the app to build and install

## Method 2: Manual APK Build (Alternative)

If Android Studio doesn't work, you can build manually:

### Option A: Download Flutter SDK
```powershell
# Quick Flutter setup (run in PowerShell as Administrator)
mkdir C:\flutter
cd C:\flutter
# Download from: https://docs.flutter.dev/get-started/install/windows
# Extract flutter SDK to C:\flutter
$env:PATH += ";C:\flutter\bin"
cd D:\portfolio\atles\atles_mobile_app
flutter pub get
flutter build apk --release
adb install build\app\outputs\flutter-apk\app-release.apk
```

### Option B: Use Online Build Service
1. Zip your `atles_mobile_app` folder
2. Use services like:
   - Codemagic (free tier available)
   - GitHub Actions with Flutter
   - AppCenter

## Method 3: Direct APK Installation (If you have a pre-built APK)

If someone provides you with a pre-built APK:
```powershell
adb install path\to\atles-mobile-app.apk
```

## Starting the ATLES API Server

Before using the app, start the server:
```powershell
python atles_api_server.py
```

Note the IP address and port (usually your PC's IP:8080)

## Connecting the App

1. Open the ATLES app on your Pixel 9
2. Go to Settings
3. Enter your PC's IP address and port (8080)
4. Tap "Connect to ATLES"
5. Start chatting!

## Troubleshooting

### Device Not Found
```powershell
adb devices  # Should show: 52120DLAQ0003V device
```

### App Won't Install
```powershell
adb uninstall com.example.atles_mobile_app  # Remove old version
adb install -r build\app\outputs\flutter-apk\app-release.apk  # Force reinstall
```

### Connection Issues
- Make sure both devices are on the same WiFi network
- Check Windows Firewall settings
- Try your PC's IP address: `ipconfig` to find it

## Next Steps After Installation

1. ✅ Install app on Pixel 9
2. ✅ Start ATLES API server
3. ✅ Connect app to server
4. ✅ Test chat functionality
5. ✅ Verify constitutional rules are working

Your ATLES mobile app will provide the same constitutional AI experience as your desktop version, accessible from anywhere in your home!
