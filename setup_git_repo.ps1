param (
    [string]$base_directory
)

if (-not $base_directory) {
    $base_directory = Split-Path -Leaf (Get-Location)
}

Write-Host "base_directory: $base_directory"

git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/adgedenkers/{$base_directory}.git
git push -u origin main