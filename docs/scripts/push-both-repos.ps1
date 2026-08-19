# One-time: add git remote and push both IFP repos.
# Usage:
#   .\push-both-repos.ps1 -IfpTestsUrl "https://github.com/org/ifp-frequency-cap-tests.git" -McpServerUrl "https://github.com/org/ifp-mcp-server.git"

param(
    [Parameter(Mandatory = $true)]
    [string]$IfpTestsUrl,

    [Parameter(Mandatory = $true)]
    [string]$McpServerUrl
)

$ErrorActionPreference = "Stop"

$testsRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$mcpRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\ifp-mcp-server")).Path

function Push-Repo {
    param([string]$Path, [string]$RemoteUrl)

    Push-Location $Path
    try {
        $existing = git remote get-url origin 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "origin already set in $Path -> $existing"
            Write-Host "Skipping remote add. Run: git push -u origin main"
        } else {
            git remote add origin $RemoteUrl
            git push -u origin main
        }
    } finally {
        Pop-Location
    }
}

Write-Host "Pushing ifp-frequency-cap-tests..."
Push-Repo -Path $testsRoot -RemoteUrl $IfpTestsUrl

Write-Host "Pushing ifp-mcp-server..."
Push-Repo -Path $mcpRoot -RemoteUrl $McpServerUrl

Write-Host "Done. Share clone URLs from docs/CLONE-INSTRUCTIONS.md"
