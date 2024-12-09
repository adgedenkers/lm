param (
    [string]$base_directory
)

if (-not $base_directory) {
    $base_directory = Split-Path -Leaf (Get-Location)
}

Write-Host "base_directory: $base_directory"
