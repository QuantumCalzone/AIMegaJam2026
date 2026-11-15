# T74: the cast picture. Five close-ups side by side in seat order, each labeled with its provider
# (a seat-color swatch and the name) and, smaller, the role it plays. Windows PowerShell 5.1 with
# System.Drawing: no package to install. The 2026-11-15 sheet (compose.py, with PIL) had this layout.
# Run (tested by the T74 prep on the 2026-11-15 close-ups):
#   powershell -NoProfile -ExecutionPolicy Bypass -File cast.ps1 -Dir <shots folder> -Out cast.png -Roles "farm kid,smuggler pilot,old desert hermit,masked villain,rebel princess"
# It reads <Dir>/bot_openai.png, bot_anthropic.png, bot_spacexai.png, bot_meta.png, bot_you.png,
# crops each to 3:4 around its middle and scales it to 380 x 506.
param(
    [Parameter(Mandatory = $true)][string]$Dir,
    [Parameter(Mandatory = $true)][string]$Out,
    [string]$Roles = ""
)
Add-Type -AssemblyName System.Drawing
$seats = @(
    @{ key = "openai";    name = "OpenAI";    rgb = @(0xA8, 0xCC, 0xFF) },
    @{ key = "anthropic"; name = "Anthropic"; rgb = @(0xE8, 0x89, 0x4A) },
    @{ key = "spacexai";  name = "SpaceXAI";  rgb = @(0xD8, 0xF0, 0x4A) },
    @{ key = "meta";      name = "Meta";      rgb = @(0x5B, 0x8C, 0xFF) },
    @{ key = "you";       name = "You";       rgb = @(0x3F, 0xD0, 0xC9) }
)
$roleList = @()
if ($Roles) { $roleList = $Roles.Split(",") | ForEach-Object { $_.Trim() } }
$tw = 380; $th = 506; $gap = 16; $pad = 24
$lab = if ($roleList.Count -gt 0) { 104 } else { 70 }
$W = $pad * 2 + 5 * $tw + 4 * $gap
$H = $pad * 2 + $th + $lab
$bg = [System.Drawing.Color]::FromArgb(250, 246, 238)
$ink = [System.Drawing.Color]::FromArgb(43, 29, 18)
$soft = [System.Drawing.Color]::FromArgb(110, 92, 74)

function RoundRect([float]$x, [float]$y, [float]$w, [float]$h, [float]$r) {
    $p = New-Object System.Drawing.Drawing2D.GraphicsPath
    $d = 2 * $r
    $p.AddArc($x, $y, $d, $d, 180, 90)
    $p.AddArc($x + $w - $d, $y, $d, $d, 270, 90)
    $p.AddArc($x + $w - $d, $y + $h - $d, $d, $d, 0, 90)
    $p.AddArc($x, $y + $h - $d, $d, $d, 90, 90)
    $p.CloseFigure()
    return $p
}

$img = New-Object System.Drawing.Bitmap $W, $H
$g = [System.Drawing.Graphics]::FromImage($img)
$g.Clear($bg)
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$fName = New-Object System.Drawing.Font("Segoe UI", 30, [System.Drawing.FontStyle]::Bold, [System.Drawing.GraphicsUnit]::Pixel)
$fRole = New-Object System.Drawing.Font("Segoe UI", 22, [System.Drawing.FontStyle]::Regular, [System.Drawing.GraphicsUnit]::Pixel)
$inkBrush = New-Object System.Drawing.SolidBrush $ink
$softBrush = New-Object System.Drawing.SolidBrush $soft
$inkPen = New-Object System.Drawing.Pen $ink, 2

for ($k = 0; $k -lt 5; $k++) {
    $s = $seats[$k]
    $file = Join-Path $Dir ("bot_{0}.png" -f $s.key)
    $src = [System.Drawing.Image]::FromFile((Resolve-Path $file).Path)
    # 3:4 box in the middle of the close-up
    $cw = $src.Width; $ch = [int][Math]::Round($cw * 4 / 3)
    if ($ch -gt $src.Height) { $ch = $src.Height; $cw = [int][Math]::Round($ch * 3 / 4) }
    $sx = [int][Math]::Floor(($src.Width - $cw) / 2); $sy = [int][Math]::Floor(($src.Height - $ch) / 2)
    $x = $pad + $k * ($tw + $gap)
    $clip = RoundRect $x $pad $tw $th 16
    $g.SetClip($clip)
    $g.DrawImage($src, (New-Object System.Drawing.Rectangle $x, $pad, $tw, $th), (New-Object System.Drawing.Rectangle $sx, $sy, $cw, $ch), [System.Drawing.GraphicsUnit]::Pixel)
    $g.ResetClip()
    $clip.Dispose(); $src.Dispose()
    # Label: seat-color swatch, provider name, then the role
    $y = $pad + $th + 16
    $sw = RoundRect ($x + 4) ($y + 8) 24 24 6
    $swBrush = New-Object System.Drawing.SolidBrush ([System.Drawing.Color]::FromArgb($s.rgb[0], $s.rgb[1], $s.rgb[2]))
    $g.FillPath($swBrush, $sw); $g.DrawPath($inkPen, $sw)
    $sw.Dispose(); $swBrush.Dispose()
    $g.DrawString($s.name, $fName, $inkBrush, [float]($x + 38), [float]$y)
    if ($k -lt $roleList.Count -and $roleList[$k]) {
        $g.DrawString($roleList[$k], $fRole, $softBrush, [float]($x + 6), [float]($y + 44))
    }
}
$g.Dispose()
$img.Save($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Out), [System.Drawing.Imaging.ImageFormat]::Png)
$img.Dispose()
Write-Output ("{0}: {1}x{2}" -f $Out, $W, $H)
