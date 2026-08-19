param(
    [string]$BaseRequest = "config/base-request.json",
    [string]$Expectations = "reference/cap-ratio-expectations.json",
    [string]$Output = "output/results.json",
    [string]$ApiUrl = $env:IFP_API_URL,
    [string]$Source = $env:IFP_SOURCE_HEADER,
    [int]$TimeoutSec = 120,
    [string[]]$CaseId = @()
)

$ErrorActionPreference = "Stop"

if (-not $ApiUrl) {
    $ApiUrl = "http://inventory-forecasting-prod-dplus.ava.prod.hulu.com/v1/inventory/forecast"
}
if (-not $Source) {
    $Source = "RYM Frequency Cap Test"
}

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

$baseRequest = Get-Content $BaseRequest -Raw | ConvertFrom-Json
$expectations = Get-Content $Expectations -Raw | ConvertFrom-Json
$cases = @($expectations.cases)

if ($CaseId.Count -gt 0) {
    $cases = @($cases | Where-Object { $CaseId -contains $_.id })
    if ($cases.Count -eq 0) {
        Write-Error "No matching cases found for -CaseId"
    }
}

$outputDir = Split-Path $Output -Parent
if ($outputDir -and -not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
}

$results = @()

foreach ($case in $cases) {
    $caseId = $case.id
    $cap = $case.frequency_cap

    $payload = $baseRequest | ConvertTo-Json -Depth 20 | ConvertFrom-Json
    $payload."frequency-cap-detail"."frequency-caps" = @($cap)

    $entry = [ordered]@{
        case_id                         = $caseId
        description                     = $case.description
        frequency_cap                   = $cap
        expected_avail_capacity_ratio   = $case.expected_avail_capacity_ratio
        request                         = $payload
        ran_at                          = (Get-Date).ToUniversalTime().ToString("o")
    }

    try {
        $body = $payload | ConvertTo-Json -Depth 20 -Compress
        $response = Invoke-RestMethod -Uri $ApiUrl -Method Post -Body $body `
            -ContentType "application/json" `
            -Headers @{ Accept = "application/json"; Source = $Source } `
            -TimeoutSec $TimeoutSec

        $entry.response = $response
        $entry.status = "ok"

        if ($null -ne $response.availability -and $null -ne $response.capacity -and $response.capacity -ne 0) {
            $entry.actual_avail_capacity_ratio = [double]$response.availability / [double]$response.capacity
        }
    }
    catch {
        $entry.status = "error"
        if ($_.Exception.Response) {
            $entry.http_status = [int]$_.Exception.Response.StatusCode
            try {
                $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $entry.error = $reader.ReadToEnd()
            }
            catch {
                $entry.error = $_.Exception.Message
            }
        }
        else {
            $entry.error = $_.Exception.Message
        }
    }

    $results += [pscustomobject]$entry
    Write-Host "$caseId`: $($entry.status)"
}

$outputDoc = [ordered]@{
    api_url       = $ApiUrl
    source_header = $Source
    ran_at        = (Get-Date).ToUniversalTime().ToString("o")
    results       = $results
}

$outputDoc | ConvertTo-Json -Depth 30 | Set-Content $Output -Encoding utf8
Write-Host "Wrote $Output"
