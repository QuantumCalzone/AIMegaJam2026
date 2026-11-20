# T115: rebuilds the game icon and its candidate sheets from IconArt.cs and RevealArt.cs.
# Windows PowerShell 5.1 with System.Drawing; no packages. From the repo root:
#   powershell -ExecutionPolicy Bypass -File Docs/Art/Icon/make_icon.ps1
$ErrorActionPreference = "Stop"
$root = (Resolve-Path "$PSScriptRoot/../../..").Path
$d = "$root/Docs/Art/Icon"
Add-Type -Path "$d/IconArt.cs", "$d/RevealArt.cs" -ReferencedAssemblies System.Drawing

# Round 1: the box head alone (not picked).
foreach ($v in "A", "B", "C") { $b = [IconArt]::Render($v, 1024); [IconArt]::SavePng($b, "$d/round1/$($v)_1024.png"); $b.Dispose() }
[IconArt]::CompareSheet(@("A", "B", "C"), @("A  Ink tile, gold rim", "B  Gold tile", "C  The face is the icon"), "$d/round1/candidates.png")

# Round 2: a human pulling off the robot headpiece. My person picked R2, "Tilt".
foreach ($v in "R1", "R2", "R3") { $b = [IconArt]::Render($v, 1024); [IconArt]::SavePng($b, "$d/round2/$($v)_1024.png"); $b.Dispose() }
[IconArt]::CompareSheet(@("R1", "R2", "R3"), @("1  Lift", "2  Tilt", "3  Peek"), "$d/round2/candidates.png", 32)

# The pick: the 1024 px sources, its sheet, the Windows .ico and the Mac asset catalog.
$b = [IconArt]::Render("R2", 1024); [IconArt]::SavePng($b, "$d/icon_1024.png"); $b.Dispose()
$b = [IconArt]::MacMaster("R2"); [IconArt]::SavePng($b, "$d/icon_mac_1024.png"); $b.Dispose()
[IconArt]::CompareSheet(@("R2"), @("The icon (2 Tilt)"), "$d/icon_sheet.png", 32)
New-Item -ItemType Directory -Force "$root/Build/Windows" | Out-Null
[IconArt]::WriteIco("R2", @(16, 20, 24, 32, 40, 48, 64, 128, 256), "$root/Build/Windows/Application.ico")
[IconArt]::WriteMac("R2", "$root/Build/Mac/Resources/Assets.xcassets")
"Wrote Build/Windows/Application.ico, Build/Mac/Resources/Assets.xcassets and the sheets in Docs/Art/Icon."
