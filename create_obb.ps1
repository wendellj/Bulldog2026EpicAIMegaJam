$srcPath = "C:\Bulldog\Game\Saved\StagedBuilds\Android\BulldogMegaJam\Content\Paks"
$zipPath = "C:\Bulldog\Game\Saved\StagedBuilds\main.1.com.YourCompany.BulldogMegaJam.zip"
$obbPath = "C:\Bulldog\Game\Saved\StagedBuilds\main.1.com.YourCompany.BulldogMegaJam.obb"

Write-Host "Creating OBB from pak files..."

# Remove old files if exist
if (Test-Path $zipPath) { Remove-Item $zipPath -Force }
if (Test-Path $obbPath) { Remove-Item $obbPath -Force }

# Create zip archive
Compress-Archive -Path "$srcPath\*" -DestinationPath $zipPath -Force

# Rename to obb
Rename-Item -Path $zipPath -NewName "main.1.com.YourCompany.BulldogMegaJam.obb"

Write-Host "OBB created: $obbPath"
Get-Item $obbPath | Select-Object Name, @{Name='SizeMB';Expression={[math]::Round($_.Length/1MB,2)}}
