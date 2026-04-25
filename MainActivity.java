name: Build APK

on:
  push:
    branches: [main, master]
  pull_request:
    branches: [main, master]
  workflow_dispatch:

jobs:
  build:
    name: Build debug APK
    runs-on: ubuntu-latest

    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up JDK 17
        uses: actions/setup-java@v4
        with:
          distribution: temurin
          java-version: '17'

      - name: Set up Android SDK
        uses: android-actions/setup-android@v3

      - name: Set up Gradle
        uses: gradle/actions/setup-gradle@v3

      - name: Generate Gradle wrapper
        run: gradle wrapper --gradle-version 8.4 --distribution-type bin

      - name: Make wrapper executable
        run: chmod +x gradlew

      - name: Build debug APK
        run: ./gradlew assembleDebug --no-daemon

      - name: Upload APK
        uses: actions/upload-artifact@v4
        with:
          name: wholeness-debug-apk
          path: app/build/outputs/apk/debug/app-debug.apk
          retention-days: 30

      - name: Build release APK (debug-signed)
        run: ./gradlew assembleRelease --no-daemon

      - name: Upload release APK
        uses: actions/upload-artifact@v4
        with:
          name: wholeness-release-apk
          path: app/build/outputs/apk/release/app-release.apk
          retention-days: 30
