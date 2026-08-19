param(
    [string]$Results = "output/results.json",
    [string]$Expectations = "reference/cap-ratio-expectations.json"
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $root

$resultsDoc = Get-Content $Results -Raw | ConvertFrom-Json
$expectations = Get-Content $Expectations -Raw | ConvertFrom-Json
$defaultTolerance = if ($expectations.default_tolerance) { [double]$expectations.default_tolerance } else { 0.001 }

$expectedById = @{}
foreach ($case in $expectations.cases) {
    if ($case.id) { $expectedById[$case.id] = $case }
}

$failures = 0

foreach ($result in $resultsDoc.results) {
    $caseId = $result.case_id
    $expectedCase = $expectedById[$caseId]
    $expectedRatio = $expectedCase.expected_avail_capacity_ratio
    $tolerance = if ($expectedCase.tolerance) { [double]$expectedCase.tolerance } else { $defaultTolerance }
    $actualRatio = $result.actual_avail_capacity_ratio
    $status = $result.status

    if ($status -ne "ok") {
        Write-Host "FAIL ${caseId}: forecast call failed ($status)"
        $failures++
        continue
    }

    if ($null -eq $expectedRatio) {
        Write-Host "SKIP ${caseId}: no expected ratio configured"
        continue
    }

    if ($null -eq $actualRatio) {
        Write-Host "FAIL ${caseId}: could not compute avail/capacity ratio from response"
        $failures++
        continue
    }

    $diff = [Math]::Abs([double]$actualRatio - [double]$expectedRatio)
    if ($diff -le $tolerance) {
        Write-Host ("PASS {0}: ratio {1:N6} ~= {2:N6}" -f $caseId, $actualRatio, $expectedRatio)
    }
    else {
        Write-Host ("FAIL {0}: ratio {1:N6} != {2:N6} (tolerance {3})" -f $caseId, $actualRatio, $expectedRatio, $tolerance)
        $failures++
    }
}

if ($failures -gt 0) {
    Write-Host ""
    Write-Host "$failures failure(s)"
    exit 1
}

Write-Host ""
Write-Host "All configured cases passed"
exit 0
