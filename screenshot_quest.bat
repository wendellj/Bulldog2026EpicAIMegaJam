@echo off
set ADB="C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe"

%ADB% shell screencap -p /sdcard/screen.png
%ADB% pull /sdcard/screen.png C:\Bulldog\quest_screen.png
echo Screenshot saved to C:\Bulldog\quest_screen.png
