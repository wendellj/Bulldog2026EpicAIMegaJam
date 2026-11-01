@echo off
set ADB="C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe"
set DEST=/storage/emulated/0/Android/data/com.YourCompany.BulldogMegaJam/files/UnrealGame/BulldogMegaJam/BulldogMegaJam/Content/Paks

echo Pushing updated pak files...
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks\BulldogMegaJam-Android.pak" %DEST%/
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks\BulldogMegaJam-Android.ucas" %DEST%/
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks\BulldogMegaJam-Android.utoc" %DEST%/
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks\global.ucas" %DEST%/
%ADB% push "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks\global.utoc" %DEST%/

echo Restarting app...
%ADB% shell am force-stop com.YourCompany.BulldogMegaJam
%ADB% shell am start -n com.YourCompany.BulldogMegaJam/com.epicgames.unreal.GameActivity
echo Done!
