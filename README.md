# Wholeness — Android App

Native Android wrapper for the Wholeness life tracker. Your full HTML/CSS/JS app
runs inside a configured WebView, with `localStorage` enabled so all user data
(goals, logs, name) persists across app launches just like on the web.

## What's inside

```
wholeness-android/
├── app/
│   ├── src/main/
│   │   ├── AndroidManifest.xml
│   │   ├── java/com/team21/wholeness/MainActivity.java   ← WebView host
│   │   ├── assets/web/index.html                         ← your full app
│   │   └── res/                                          ← icons, theme, strings
│   └── build.gradle
├── build.gradle
├── settings.gradle
├── gradle.properties
└── gradle/wrapper/
```

## Build the APK — 3 ways

### Option A — Android Studio (easiest, recommended)

1. Install **Android Studio** (Hedgehog or newer) from
   https://developer.android.com/studio
2. Open the project: **File → Open** → select the `wholeness-android/` folder
3. When prompted, accept SDK component installations (Android SDK, build tools)
4. Wait for the initial Gradle sync to finish (5–10 minutes the first time)
5. Build: **Build → Build Bundle(s) / APK(s) → Build APK(s)**
6. Click the **locate** link in the notification — your APK is at:
   `app/build/outputs/apk/debug/app-debug.apk`

To get a signed release APK:
- **Build → Generate Signed Bundle / APK → APK**, then create a keystore.

### Option B — Command line (Linux / macOS / WSL)

Requires JDK 17+ and the Android SDK with build-tools 34.

```bash
cd wholeness-android

# First-time only: generate the gradle wrapper jar
gradle wrapper --gradle-version 8.4

# Build a debug APK
./gradlew assembleDebug

# Output:
ls app/build/outputs/apk/debug/app-debug.apk
```

If you don't have `gradle` installed locally, download it from
https://gradle.org/releases/ and run the wrapper command once.

### Option C — GitHub Actions (build in the cloud, no local setup)

Create `.github/workflows/build.yml` in your repo:

```yaml
name: Build APK
on: [push, workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { distribution: temurin, java-version: 17 }
      - uses: android-actions/setup-android@v3
      - run: gradle wrapper --gradle-version 8.4
      - run: ./gradlew assembleDebug
      - uses: actions/upload-artifact@v4
        with:
          name: wholeness-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
```

Push to GitHub, and download the APK from the Actions tab.

## Install the APK on a phone

1. Transfer `app-debug.apk` to your Android device (email, USB, or
   Google Drive).
2. On the device, tap the file. Android will warn that it's from an
   unknown source — go to **Settings → Apps → Special access → Install
   unknown apps** and enable it for the file manager you're using.
3. Tap **Install**. The Wholeness icon will appear in your launcher.

## Updating your web app

To push a new version of the HTML to the APK:

1. Replace `app/src/main/assets/web/index.html` with your new file
2. Bump `versionCode` and `versionName` in `app/build.gradle`
3. Rebuild

User data (localStorage) survives app updates because we keep the same
`applicationId`.

## Notes on the WebView setup

- **localStorage is enabled** — all your existing storage code (`whn_<name>_…`
  keys) works unchanged.
- **Google Fonts are loaded over HTTPS.** The first launch needs internet for
  fonts to load; afterwards they're cached. The app otherwise works fully
  offline.
- **Hardware back button** navigates web history before exiting.
- **Status bar and navigation bar** are tinted dark to match the splash and
  avoid white flashes.
- **Splash screen** uses the gold "Wholeness" wordmark on dark background
  while the WebView warms up.
- **`minSdk = 21`** (Android 5.0+, ~99% of active devices).
- **No third-party dependencies** — pure Android framework.

## Customising

- **App name:** `app/src/main/res/values/strings.xml`
- **Colors:** `app/src/main/res/values/colors.xml`
- **Launcher icons:** regenerate with `python3 generate_icons.py` after
  editing the script.
- **Package name:** change `applicationId` in `app/build.gradle` and the
  folder structure under `app/src/main/java/`.

## License

© Innocent Forteh · Team21 Academy · Inno4te Publishing
