# Quest 3 Setup Guide for Bulldog MegaJam

This guide covers two ways to run the game on Quest 3:

1. **VR Preview** (easy, fast iteration, requires PC tethered)
2. **Standalone APK** (harder, runs without PC)

Most of the time you'll use VR Preview. Only build APKs when testing standalone or preparing for submission.

---

## Prerequisites (One-Time Setup)

### On Your PC

1. Install **Meta Quest Link** app from https://www.meta.com/quest/setup/
2. Open Meta Quest Link app and sign in with your Meta account
3. Keep it running in the background when doing VR work

### On Your Quest 3

1. Put on headset
2. Go to **Settings** (gear icon in quick settings)
3. Select **System** > **Quest Link**
4. Toggle **Quest Link** to ON
5. For wireless: also toggle **Air Link** to ON

### Enable Developer Mode (Required for APK installs)

1. On your phone, install the **Meta Horizon** app
2. Sign in with same Meta account as your headset
3. Go to **Menu** > **Devices** > select your Quest 3
4. Tap **Headset Settings** > **Developer Mode**
5. Toggle Developer Mode ON
6. Restart your Quest 3

---

## Method 1: VR Preview (Recommended for Daily Work)

This runs the game directly from Unreal on your PC, streamed to your headset. No building required.

### Connect Your Quest 3

**Option A: USB Cable (most reliable)**
1. Plug Quest 3 into PC with USB-C cable
2. Put on headset, accept "Allow USB debugging" prompt
3. Accept "Enable Quest Link" prompt
4. You should see your PC desktop in VR

**Option B: Air Link (wireless)**
1. Quest 3 and PC must be on same WiFi network (5GHz recommended)
2. PC should be wired to router if possible
3. In headset: Settings > System > Quest Link > Launch Air Link
4. Select your PC from the list
5. Click Pair, then Launch

### Run VR Preview in Unreal

1. Open the project: `C:\Bulldog\Game\BulldogMegaJam.uproject`
2. Wait for shaders to compile (first time takes a while)
3. Look at the toolbar near the top. Find the green **Play** button
4. Click the small **three dots (⋮)** next to the Play button
5. In the dropdown, find **Active Play Mode** and select **VR Preview**
6. Now click the Play button
7. Put on your headset. The game should appear

To stop: press **Escape** on your keyboard or click Stop in Unreal.

### Troubleshooting VR Preview

| Problem | Solution |
|---------|----------|
| "VR Preview" option is grayed out | Install OpenXR plugin: Edit > Plugins > search "OpenXR" > enable it > restart Unreal |
| Game appears on monitor but not in headset | Make sure Quest Link is active (you should see PC desktop in headset) |
| Black screen in headset | Check Meta Quest Link app on PC shows "Connected" |
| Laggy or stuttering | Use USB cable instead of Air Link, or move closer to router |

---

## Method 2: Build and Deploy APK (Standalone)

This creates an app that runs on Quest 3 without a PC. Takes longer but needed for final testing.

### First Time: Verify Android SDK

Open a command prompt and run:
```
cd C:\Bulldog
cook_android.bat
```

If it fails with SDK errors, talk to Wendell. The SDK setup is already configured but may need adjustment for your machine.

### Build Steps

Open a command prompt (Win+R, type `cmd`, press Enter).

**Step 1: Cook the content**
```
cd C:\Bulldog
cook_android.bat
```
This packages all the game content. Takes 5-15 minutes first time.

**Step 2: Build the APK**
```
build_apk_nocache.bat
```
This compiles the actual Android app. Takes 5-10 minutes.

**Step 3: Create the OBB** (contains game data)
```
powershell -ExecutionPolicy Bypass -File create_obb.ps1
```

**Step 4: Deploy to Quest**
1. Connect Quest 3 via USB
2. Put on headset and accept any permission prompts
3. Take off headset
4. Run:
```
deploy_quest.bat
```

**Step 5: Launch the game**
1. Put on Quest 3
2. Go to **Apps** (grid icon in menu bar)
3. In top-right dropdown, select **Unknown Sources**
4. Find and launch **BulldogMegaJam**

### Quick Update (Content Only)

If you only changed content (not code), you can skip the APK rebuild:
```
cook_android.bat
push_paks.bat
```
Then relaunch from Unknown Sources.

---

## Taking Screenshots from Quest

To capture what you see in the headset:
```
cd C:\Bulldog
screenshot_quest.bat
```
Screenshot saves to `C:\Bulldog\screenshots\`

---

## Viewing Logs (Debugging)

If the app crashes or behaves strangely:
```
cd C:\Bulldog
logcat.bat
```
This shows recent log messages. Share these with Wendell if something's broken.

---

## Quick Reference

| Task | Command or Action |
|------|-------------------|
| Fast iteration (daily work) | VR Preview via Quest Link |
| Test standalone build | Run all 4 build steps above |
| Content-only update | `cook_android.bat` then `push_paks.bat` |
| Take screenshot | `screenshot_quest.bat` |
| Debug crashes | `logcat.bat` |

---

## Getting Help

- **Unreal issues**: Ask in #programming on Discord
- **Quest connection issues**: Check Meta's support site or ask Wendell
- **Build script errors**: Copy the error message and post in #programming

