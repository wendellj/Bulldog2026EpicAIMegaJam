@echo off
set ADB="C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe"
set OBB_PATH=/storage/emulated/0/Android/obb/com.YourCompany.BulldogMegaJam

echo Creating OBB directory...
%ADB% shell "mkdir -p %OBB_PATH%"

echo Creating OBB from pak files...
cd /d "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks"

REM Create a zip file containing all pak content
"C:\Program Files\7-Zip\7z.exe" a -tzip "C:\Bulldog\Game\Saved\StagedBuilds\main.1.com.YourCompany.BulldogMegaJam.obb" *.*

echo Pushing OBB to device...
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\main.1.com.YourCompany.BulldogMegaJam.obb" %OBB_PATH%/

echo Verifying...
%ADB% shell "ls -la %OBB_PATH%/"

echo Done.
