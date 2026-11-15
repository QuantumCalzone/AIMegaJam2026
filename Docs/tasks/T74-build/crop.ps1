# T74: crop the center of a capture to W:H and scale it to W x H, as a PNG.
# Windows PowerShell 5.1 with System.Drawing: no package to install.
# Run (tested by the T74 prep on a 2026-11-15 capture):
#   powershell -NoProfile -ExecutionPolicy Bypass -File crop.ps1 -In cap.png -Out house.png -W 1920 -H 1080
param(
    [Parameter(Mandatory = $true)][string]$In,
    [Parameter(Mandatory = $true)][string]$Out,
    [int]$W = 1920,
    [int]$H = 1080
)
Add-Type -AssemblyName System.Drawing
$src = [System.Drawing.Image]::FromFile((Resolve-Path $In).Path)
try {
    # The largest W:H box in the middle of the capture.
    $cw = $src.Width
    $ch = [int][Math]::Round($cw * $H / $W)
    if ($ch -gt $src.Height) {
        $ch = $src.Height
        $cw = [int][Math]::Round($ch * $W / $H)
    }
    $x = [int][Math]::Floor(($src.Width - $cw) / 2)
    $y = [int][Math]::Floor(($src.Height - $ch) / 2)
    $bmp = New-Object System.Drawing.Bitmap $W, $H
    $g = [System.Drawing.Graphics]::FromImage($bmp)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
    $dst = New-Object System.Drawing.Rectangle 0, 0, $W, $H
    $box = New-Object System.Drawing.Rectangle $x, $y, $cw, $ch
    $g.DrawImage($src, $dst, $box, [System.Drawing.GraphicsUnit]::Pixel)
    $g.Dispose()
    $bmp.Save($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Out), [System.Drawing.Imaging.ImageFormat]::Png)
    $bmp.Dispose()
    Write-Output ("{0}: {1}x{2} -> crop {3}x{4} at ({5},{6}) -> {7}x{8}" -f $Out, $src.Width, $src.Height, $cw, $ch, $x, $y, $W, $H)
}
finally {
    $src.Dispose()
}
