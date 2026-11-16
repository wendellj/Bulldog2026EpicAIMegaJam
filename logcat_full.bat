@echo off
set ADB="C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe"
%ADB% logcat -d -t 500 --pid=$(%ADB% shell pidof com.YourCompany.BulldogMegaJam)
