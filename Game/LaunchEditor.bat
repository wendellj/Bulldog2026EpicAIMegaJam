@echo off
REM Launch Unreal Editor with MCP server and Android SDK configured

REM Set Android SDK paths (using Unity's SDK)
set ANDROID_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK
set NDKROOT=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\NDK
set JAVA_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK

REM Launch Unreal Editor with MCP server
start "" "C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe" "%~dp0BulldogMegaJam.uproject" -ModelContextProtocolStartServer
