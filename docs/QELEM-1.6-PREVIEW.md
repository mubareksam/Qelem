# Qelem 1.6 — Android preview

Qelem 1.6 is an **experimental Android arm64 preview**, not a stable release or a Dreams clone. It contains the existing Qelem native drawing app and its screenshot-inspired, single-track animation timeline. This release does not contain a new Windows build.

## Download and open

- [Download the Android 1.6 preview APK](../artifacts/releases/Qelem-1.6-preview-Android-arm64.apk) (Android 9 or later, arm64).
- After installation, open **Qelem 1.6 Preview**. Create or open an artwork and choose **Actions (wrench) → Canvas → Animation Assist**. The expanded timeline opens by default on windows at least 360 dp tall. On shorter windows, tap **▥** on the compact bar. **Canvas** returns to the compact bar.

## Artwork and installation safety

**Do not uninstall existing Qelem apps to install this preview.** The 1.6 preview is debug-signed and uses the separate application ID `com.qalam.studio.nativepreview.v16.debug`. Earlier CI previews were signed with different debug keys, so this does **not** update them. Its gallery is separate and starts empty; artwork migration has not been verified. Back up artwork before testing. Future debug builds may not update this build either.

## What is included

The expanded timeline uses a dark surface, drawing-track thumbnails, a playhead, ruler and timecode. It offers existing playback, frame navigation, hold adjustment, frame reorder, selection, batch holds, zoom and onion controls. The compact view, Page Assist and drawing tools are retained. It is an overlay for the existing layer-based animation model, not a separate stage/movie editor: independent tracks, audio/video clips, keyframes, Perform mode and full Dreams gesture parity are not implemented.

## Verification

The Android build and helper tests are run by GitHub Actions for the source commit recorded in the [APK verification record](../artifacts/releases/Qelem-1.6-preview-Android-arm64.txt). The preview has **not** been tested on a physical device; layout, touch, rendering, performance, and save/reopen require device verification. It is debug-signed, not a production release.
