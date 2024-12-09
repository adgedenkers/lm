# Variables
$nginxRoot = "C:\nginx"
$appRoot = "$HOME\stuff4sale"
$venvPath = "$appRoot\.venv"
$domain = "dev.denkers.co"
$hostsFile = "C:\Windows\System32\drivers\etc\hosts"
$pythonVersion = "3.11.6"

# Step 1: Install Chocolatey (if not installed)
if (-Not (Get-Command choco -ErrorAction SilentlyContinue)) {
    Write-Host "Installing Chocolatey..."
    Set-ExecutionPolicy Bypass -Scope Process -Force
    [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
    Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
} else {
    Write-Host "Chocolatey is already installed."
}

# Step 2: Install packages using Chocolatey
$packages = @(
    'git',
    'python3',
    'nodejs',
    'nginx',
    'docker-desktop',
    'visualstudiocode'
)

Write-Host "Installing required packages via Chocolatey..."
choco install $packages -y --allow-empty-checksums

# Step 3: Ensure Python is on the PATH
$pythonPath = Get-Command python | Select-Object -ExpandProperty Path
if (-not $pythonPath) {
    Write-Host "Python is not on the PATH. Adding it now..."
    $env:Path += ";C:\Python311;C:\Python311\Scripts"
}

# Step 4: Check Python version
Write-Host "Checking Python version..."
$pythonVersionCheck = python --version
if ($pythonVersionCheck -like "*$pythonVersion*") {
    Write-Host "Python $pythonVersion is installed."
} else {
    Write-Host "Please ensure Python $pythonVersion is installed."
}

# Step 5: Create application directory
Write-Host "Creating application directory at $appRoot..."
New-Item -ItemType Directory -Path $appRoot -Force

# Step 6: Set up Python virtual environment
Write-Host "Setting up Python virtual environment at $venvPath..."
python -m venv $venvPath

# Step 7: Activate virtual environment and install required Python packages
Write-Host "Activating virtual environment and installing Python packages..."
& "$venvPath\Scripts\activate.ps1"
pip install --upgrade pip
pip install fastapi uvicorn streamlit tortoise-orm pydantic

# Step 8: Set up Nginx configuration
Write-Host "Setting up Nginx configuration for dev.denkers.co..."
$nginxConfPath = "$nginxRoot\conf\dev.conf"
$nginxConf = @"
server {
    listen 80;
    server_name $domain;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;
    }

    error_log logs/dev_error.log;
    access_log logs/dev_access.log;
}
"@

Set-Content -Path $nginxConfPath -Value $nginxConf

# Step 9: Update hosts file
Write-Host "Adding $domain to hosts file..."
if ((Get-Content $hostsFile) -notmatch [regex]::Escape("127.0.0.1 dev.denkers.co")) {
    Add-Content -Path $hostsFile -Value "127.0.0.1 dev.denkers.co"
    Write-Host "$domain added to hosts file."
} else {
    Write-Host "$domain is already in the hosts file."
}

# Step 10: Start Nginx
Write-Host "Starting Nginx..."
Start-Process -FilePath "$nginxRoot\nginx.exe"

# Step 11: Run Streamlit app (optional)
Write-Host "Starting Streamlit app on http://localhost:8501..."
cd $appRoot
streamlit run app.py

Write-Host "Development environment setup is complete!"
