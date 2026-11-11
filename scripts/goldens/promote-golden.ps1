#requires -Version 5.1
<# Human approval must follow external image/context/diff review. No automatic approval.
No Android services are needed here. Native verification is a separate required step.
If it later fails, retain the promoted reference, packet and backup; no automatic rollback.
#>
[CmdletBinding()]
param([string]$ReviewDir, [string]$ApprovedHash)

. (Join-Path $PSScriptRoot 'capture-candidate.ps1')

function Copy-GCandidate([string]$Source, [string]$Destination, [bool]$Replace) {
    [IO.File]::Copy($Source, $Destination, $Replace)
}

function Invoke-GPromotion([string]$Root, [string]$Review, [string]$Hash) {
    $ErrorActionPreference = 'Stop'
    $lock = Enter-GLock $Root
    try {
        $packet = Assert-GPath $Review (Join-Path $Root 'qa_visual/artifacts/review')
        $manifestPath = Assert-GPath (Join-Path $packet 'manifest.json') $Root
        $m = Read-GJson $manifestPath
        $node = Get-GNode $m.scenario
        if ($m.schema -cne 'golden-review-v1' -or $m.producer -cne 'capture-candidate.ps1' -or
            $m.accepted -isnot [bool] -or !$m.accepted -or $m.profile -cne 'pixel10-api37' -or
            $m.classification -notin @('comparison-pass','comparison-mismatch','golden-missing') -or
            $m.source_commit -notmatch '^[a-f0-9]{40}$' -or
            (Test-Path -LiteralPath (Join-Path $packet 'REJECTED.txt'))) { throw 'Not an accepted capture-helper packet.' }
        $start = [DateTime]::Parse($m.started_utc).ToUniversalTime()
        $end = [DateTime]::Parse($m.completed_utc).ToUniversalTime()
        if ($end -lt $start -or !$m.command -or !$m.files_sha256) { throw 'Incomplete capture provenance.' }
        Assert-GDevice $m.device
        foreach ($property in $m.files_sha256.PSObject.Properties) {
            if ($property.Name -notmatch '^[a-z][a-z0-9.-]*$' -or $property.Value -notmatch '^[a-f0-9]{64}$') { throw 'Invalid packet hash entry.' }
            $p = Assert-GPath (Join-Path $packet $property.Name) $packet
            if ((Get-GHash $p) -ne $property.Value) { throw "Packet artifact changed: $($property.Name)" }
        }
        $requiredFiles = @('candidate.png','context.png','junit.xml','pytest.log')
        if ($m.reference_sha256) {
            $requiredFiles += @('reference.png','comparison.json','diff.png','verified.diff.png')
            if ($m.files_sha256.'reference.png' -ne $m.reference_sha256) { throw 'Reference inventory mismatch.' }
        }
        if ($m.scenario -ne 'long_headline') { $requiredFiles += @('capture.json','hierarchy.xml') }
        if ($m.classification -ne 'comparison-pass') { $requiredFiles += 'failure.json' }
        foreach ($required in $requiredFiles) {
            if (!$m.files_sha256.PSObject.Properties[$required]) { throw 'Incomplete packet hash inventory.' }
        }
        if ((Get-GClassification $packet $m.scenario $m.pytest_exit ([bool]$m.reference_sha256)) -cne $m.classification) { throw 'Capture classification changed.' }
        $candidate = Assert-GPath (Join-Path $packet 'candidate.png') $packet
        $python = Join-Path $Root 'qa_visual/.venv/Scripts/python.exe'
        Assert-GPng $python $candidate (Join-Path $Root 'qa_visual')
        Assert-GPng $python (Join-Path $packet 'context.png') (Join-Path $Root 'qa_visual')
        if ($Hash -notmatch '^[a-fA-F0-9]{64}$' -or (Get-GHash $candidate) -ne $Hash -or $m.candidate_sha256 -ne $Hash) { throw 'Candidate does not match approved SHA-256.' }
        $destination = Assert-GPath (Join-Path $Root "qa_visual/baselines/android/pixel10-api37/$($m.scenario).png") $Root
        $current = Get-GHash $destination
        if ($current -ne $m.reference_sha256) { throw 'Original reference changed since capture.' }
        $backup = Assert-GPath (Join-Path $packet 'previous-approved.png') $packet
        $record = Assert-GPath (Join-Path $packet 'promotion.json') $packet
        if ((Test-Path -LiteralPath $backup) -or (Test-Path -LiteralPath $record)) { throw 'Backup or promotion record already exists; never overwritten.' }
        Write-Host "Scenario: $($m.scenario) / pixel10-api37`nReview: $packet`nDestination: $destination`nCurrent: $current`nCandidate: $Hash"
        Write-Host 'The supplied hash is not proof of review. Human review of image, context, diff and stability must already be complete.'
        if ((Read-Host 'Type PROMOTE to authorize this exact byte copy') -cne 'PROMOTE') { throw 'Promotion declined.' }
        # Recheck after the human pause. Hashes and path guards do not authorize concurrent external writers.
        Assert-GPath $destination $Root | Out-Null
        Assert-GPath $candidate $packet | Out-Null
        if ((Get-GHash $candidate) -ne $Hash -or (Get-GHash $destination) -ne $current) { throw 'Files changed during confirmation.' }
        if ($current) {
            [IO.File]::Copy($destination, $backup, $false)
            if ((Get-GHash $backup) -ne $current) { throw 'Backup verification failed.' }
        }
        Write-GJson @{ status='copy-started'; scenario=$m.scenario; candidate_sha256=$Hash; previous_sha256=$current; utc=[DateTime]::UtcNow.ToString('o') } $record
        try {
            Copy-GCandidate $candidate $destination ([bool]$current)
            if ((Get-GHash $destination) -ne $Hash) { throw 'Destination hash verification failed.' }
            Write-GJson @{ status='promoted-native-verification-pending'; scenario=$m.scenario; candidate_sha256=$Hash; previous_sha256=$current; utc=[DateTime]::UtcNow.ToString('o') } $record
        } catch {
            Write-GJson @{ status='copy-or-verification-failed'; scenario=$m.scenario; candidate_sha256=$Hash; previous_sha256=$current; utc=[DateTime]::UtcNow.ToString('o') } $record
            throw
        }
        Write-Host 'PROMOTED  NATIVE VERIFICATION PENDING'
        Write-Host "Set-Location '$((Join-Path $Root 'qa_visual').Replace("'", "''"))'"
        Write-Host ".\.venv\Scripts\python.exe -m pytest .\tests\test_$($m.scenario).py::$node -v -s"
        Write-Host "if (`$LASTEXITCODE -ne 0) { throw 'Native verification failed; retain all evidence.' }"
        $relative = ".\baselines\android\pixel10-api37\$($m.scenario).png"
        Write-Host "if ((Get-FileHash -LiteralPath '$relative' -Algorithm SHA256).Hash -ne '$Hash') { throw 'Reference hash changed.' }"
        Write-Host 'Native comparison must pass before committing. If it fails, retain candidate, promoted reference, backup and evidence; reviewer decides restoration. No automatic rollback or retry.'
    } finally { $lock.Dispose() }
}

if ($MyInvocation.InvocationName -ne '.') {
    Invoke-GPromotion ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))) $ReviewDir $ApprovedHash
}
