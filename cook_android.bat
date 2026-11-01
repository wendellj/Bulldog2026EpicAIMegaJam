@echo off
set "ANDROID_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK"
set "NDKROOT=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\NDK"
set "NDK_ROOT=%NDKROOT%"
set "ANDROID_NDK_ROOT=%NDKROOT%"
set "JAVA_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK"

echo Cooking Android content...
"C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="C:\Bulldog\Game\BulldogMegaJam.uproject" -platform=Android -clientconfig=Development -cook -stage -pak -package -nodebuginfo
