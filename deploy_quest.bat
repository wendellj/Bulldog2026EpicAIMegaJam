@echo off
set ADB="C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe"

echo Installing APK...
%ADB% install -r "C:\Bulldog\Game\Intermediate\Android\arm64\gradle\app\build\outputs\apk\debug\app-debug.apk"

echo Creating OBB directory...
%ADB% shell "mkdir -p /storage/emulated/0/Android/obb/com.YourCompany.BulldogMegaJam"

echo Pushing OBB...
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\main.1.com.YourCompany.BulldogMegaJam.obb" /storage/emulated/0/Android/obb/com.YourCompany.BulldogMegaJam/

echo Launching app...
%ADB% shell am start -n com.YourCompany.BulldogMegaJam/com.epicgames.unreal.GameActivity

echo Done!
