@echo off
set "JAVA_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK"
set "ANDROID_HOME=C:\Program Files\Unity\Hub\Editor\6000.4.2f1\Editor\Data\PlaybackEngines\AndroidPlayer\SDK"
cd /d "C:\Bulldog\Game\Intermediate\Android\arm64\gradle"
call "C:\Bulldog\Game\Intermediate\Android\arm64\gradle\gradlew.bat" :app:assembleDebug --no-configuration-cache
