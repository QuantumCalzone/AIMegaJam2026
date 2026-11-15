# T74: the stage close-ups picture. The proscenium shot (a cherub, the left boxes) with its left 17%
# cut off, beside the chandelier shot, both 700 px tall, on the cream sheet. Same layout as the
# 2026-11-15 picture (compose.py, with PIL). Windows PowerShell 5.1 with System.Drawing.
# Run (tested by the T74 prep on the 2026-11-15 close-ups):
#   powershell -NoProfile -ExecutionPolicy Bypass -File details.ps1 -A proscenium.png -B chandelier.png -Out stage_details.png
param(
    [Parameter(Mandatory = $true)][string]$A,
    [Parameter(Mandatory = $true)][string]$B,
    [Parameter(Mandatory = $true)][string]$Out,
    [double]$CutLeft = 0.17
)
Add-Type -AssemblyName System.Drawing
$pad = 24; $gap = 16; $rowH = 700
$bg = [System.Drawing.Color]::FromArgb(250, 246, 238)

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

$imA = [System.Drawing.Image]::FromFile((Resolve-Path $A).Path)
$imB = [System.Drawing.Image]::FromFile((Resolve-Path $B).Path)
try {
    $ax = [int][Math]::Floor($imA.Width * $CutLeft)
    $aBox = New-Object System.Drawing.Rectangle $ax, 0, ($imA.Width - $ax), $imA.Height
    $aw = [int][Math]::Round($aBox.Width * $rowH / $aBox.Height)
    $bw = [int][Math]::Round($imB.Width * $rowH / $imB.Height)
    $W = $pad * 2 + $aw + $gap + $bw
    $H = $pad * 2 + $rowH
    $img = New-Object System.Drawing.Bitmap $W, $H
    $g = [System.Drawing.Graphics]::FromImage($img)
    $g.Clear($bg)
    $g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
    $g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
    $c1 = RoundRect $pad $pad $aw $rowH 16
    $g.SetClip($c1)
    $g.DrawImage($imA, (New-Object System.Drawing.Rectangle $pad, $pad, $aw, $rowH), $aBox, [System.Drawing.GraphicsUnit]::Pixel)
    $g.ResetClip(); $c1.Dispose()
    $bx = $pad + $aw + $gap
    $c2 = RoundRect $bx $pad $bw $rowH 16
    $g.SetClip($c2)
    $g.DrawImage($imB, (New-Object System.Drawing.Rectangle $bx, $pad, $bw, $rowH), (New-Object System.Drawing.Rectangle 0, 0, $imB.Width, $imB.Height), [System.Drawing.GraphicsUnit]::Pixel)
    $g.ResetClip(); $c2.Dispose()
    $g.Dispose()
    $img.Save($ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Out), [System.Drawing.Imaging.ImageFormat]::Png)
    $img.Dispose()
    Write-Output ("{0}: {1}x{2}" -f $Out, $W, $H)
}
finally {
    $imA.Dispose(); $imB.Dispose()
}
