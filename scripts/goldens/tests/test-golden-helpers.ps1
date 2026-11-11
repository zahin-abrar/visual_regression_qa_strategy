#requires -Version 5.1
# Offline safety tests: real temporary file operations, mocked ADB/pytest only.
$ErrorActionPreference = 'Stop'
. (Join-Path $PSScriptRoot '../promote-golden.ps1')
$repo = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$realPython = Join-Path $repo 'qa_visual/.venv/Scripts/python.exe'
$realProcess = ${function:Invoke-GProcess}
$sandbox = Join-Path ([IO.Path]::GetTempPath()) ('golden-tests-' + [guid]::NewGuid().ToString('N'))
[IO.Directory]::CreateDirectory($sandbox) | Out-Null
$count = 0
$saved = @{}
$keys = @('VVP_GOLDEN_PROFILE','VVP_ANDROID_UDID','VVP_ANDROID_DEVICE','VVP_ANDROID_PACKAGE','VVP_ANDROID_ACTIVITY','VVP_METRO_HOST','VVP_METRO_PORT','VVP_APPIUM_URL','VVP_CHANNEL_TOLERANCE','VVP_MAX_CHANGED_RATIO','VVP_QA_LAUNCH_URL','PYTEST_ADDOPTS','PYTEST_PLUGINS')
foreach ($key in $keys) { $saved[$key] = [Environment]::GetEnvironmentVariable($key); [Environment]::SetEnvironmentVariable($key, $null) }

function Assert-Test([bool]$Condition, [string]$Message) { if (!$Condition) { throw "TEST ASSERTION: $Message" } }
function Test-Case([string]$Label, [scriptblock]$Body) {
    & $Body
    $script:count++
    Write-Host "PASS $Label"
}
function Must-Reject([scriptblock]$Body, [string]$Pattern) {
    $caught = $null
    try { & $Body | Out-Null } catch { $caught = $_ }
    if (!$caught -or $caught.Exception.Message -notmatch $Pattern) { throw "Expected rejection /$Pattern/; got $caught" }
}
function New-TestRoot {
    $script:root = Join-Path $sandbox ([guid]::NewGuid().ToString('N'))
    foreach ($dir in @('qa_visual/.venv/Scripts','qa_visual/baselines/android/pixel10-api37','qa_visual/artifacts/android/pixel10-api37')) {
        [IO.Directory]::CreateDirectory((Join-Path $root $dir)) | Out-Null
    }
    [IO.File]::WriteAllText((Join-Path $root 'qa_visual/.venv/Scripts/python.exe'), 'mock executable marker')
    $script:mode = 'pass'; $script:deviceMode = 'normal'; $script:confirmation = 'PROMOTE'
    $script:scenario = 'breaking_news'
    $script:baseline = Join-Path $root 'qa_visual/baselines/android/pixel10-api37/breaking_news.png'
    [IO.File]::Copy($white, $baseline)
}
function Get-TestDevice {
    $d = [ordered]@{serial='emulator-5554';state='device';boot='1';api='37';abi='x86_64';size='Physical size: 1080x2424';density='Physical density: 420';font='1.0';avd="Pixel_10`nOK";fingerprint='synthetic/test/image';package='package:/data/app/test/base.apk'}
    if ($deviceMode -eq 'wrong') { $d.size = 'Physical size: 1080x2424' + "`nOverride size: 720x1280" }
    if ($deviceMode -eq 'unavailable') { $d.state = 'unauthorized' }
    return $d
}
function Get-GDevice([string]$Root) { $d = Get-TestDevice; Assert-GDevice $d; return $d }
function Read-Host { param($Prompt) return $script:confirmation }

function Invoke-GProcess([string]$Exe, [string[]]$Arguments, [string]$Working, [string]$Log, [int]$Seconds = 600) {
    if ($Exe -eq 'git.exe') { return @{Code=0;Text=('a' * 40)} }
    if ($Arguments[0] -eq '-m' -and $Arguments[1] -eq 'pytest') {
        $name = [regex]::Match($Arguments[2], 'tests/test_(.+)\.py::').Groups[1].Value
        $node = Get-GNode $name
        $packet = Split-Path -Parent ($Arguments[-1].Substring('--junitxml='.Length))
        $out = Join-Path $Working 'artifacts/android/pixel10-api37'
        [IO.File]::WriteAllText($Log, 'Synthetic pytest output (no device contacted).')
        if ($mode -eq 'interrupted') { throw 'Process timed out; execution incomplete.' }
        $isMissing = $mode -eq 'missing'
        $isMismatch = $mode -eq 'mismatch'
        $early = $mode -in @('startup','identity','readiness','cleanup')
        $rc = if ($isMissing -or $isMismatch -or $early) { 1 } else { 0 }
        $failure = ''
        if ($isMissing) { $failure = '<failure message="Failed: Golden missing. An ACTUAL native screenshot was saved at synthetic">comparison reached</failure>' }
        elseif ($isMismatch) { $failure = '<failure message="AssertionError: Visual regression: changed=1/1">comparison reached</failure>' }
        elseif ($early) { $failure = "<failure message=`"Unexpected $mode failure`">No comparison</failure>" }
        $failed = [int]($failure -ne '')
        $xml = "<testsuites><testsuite tests=`"1`" errors=`"0`" skipped=`"0`" failures=`"$failed`"><testcase classname=`"qa_visual.tests.test_$name`" name=`"$node`">$failure</testcase></testsuite></testsuites>"
        if ($mode -eq 'extra-test') { $xml = $xml.Replace('</testsuite>','<testcase name="unexpected"/></testsuite>') }
        if ($mode -eq 'wrong-count') { $xml = $xml.Replace('tests="1"','tests="2"') }
        if ($mode -eq 'bad-junit') { $xml = '<broken' }
        if ($mode -eq 'wrong-node') { $xml = $xml.Replace($node, 'test_unrelated') }
        if ($mode -eq 'teardown') { $xml = $xml.Replace('errors="0"','errors="1"').Replace('</testcase>','<error message="teardown failed"/></testcase>') }
        if ($mode -eq 'skip') { $xml = $xml.Replace('skipped="0"','skipped="1"').Replace('</testcase>','<skipped/></testcase>') }
        if ($mode -ne 'no-junit') { [IO.File]::WriteAllText((Join-Path $packet 'junit.xml'), $xml) }
        if ($mode -ne 'no-actual') {
            $png = if ($isMismatch) { $black } else { $white }
            [IO.File]::Copy($png, (Join-Path $out "$name.actual.png"), $true)
            if ($mode -eq 'stale') { (Get-Item -LiteralPath (Join-Path $out "$name.actual.png")).LastWriteTimeUtc = [DateTime]::UtcNow.AddDays(-1) }
            if ($mode -eq 'bad-png') { [IO.File]::WriteAllText((Join-Path $out "$name.actual.png"), 'not PNG') }
        }
        if ($mode -ne 'no-context') { [IO.File]::Copy($white, (Join-Path $out "$name.context.png"), $true) }
        if ($name -ne 'long_headline') {
            Write-GJson @{scenario=$name;identity="qa-scenario:$name";session='synthetic-session'} (Join-Path $out "$name.capture.json")
            [IO.File]::WriteAllText((Join-Path $out "$name.hierarchy.xml"), '<hierarchy/>')
        }
        if (!$isMissing -and !$early) {
            $c = @{size_match=$true;baseline_size=@(1,1);actual_size=@(1,1);changed_pixels=[int]$isMismatch;total_pixels=1;changed_ratio=[double][int]$isMismatch;max_changed_ratio=0.002;channel_tolerance=12;passed=(!$isMismatch)}
            if ($mode -eq 'contradictory') { $c.passed = $false }
            Write-GJson $c (Join-Path $out "$name.comparison.json")
            [IO.File]::Copy($white, (Join-Path $out "$name.diff.png"), $true)
        }
        if ($isMissing -or $isMismatch) {
            $folder = Join-Path $out ('failures/' + [guid]::NewGuid().ToString('N'))
            [IO.Directory]::CreateDirectory($folder) | Out-Null
            $hashes = @{'actual.png'=(Get-GHash (Join-Path $out "$name.actual.png"));'context.png'=(Get-GHash (Join-Path $out "$name.context.png"))}
            $reason = if ($isMissing) { 'golden missing' } else { 'visual comparison failed' }
            Write-GJson @{reason=$reason;scenario=$name;test="tests/test_$name.py::$node (call)";files_sha256=$hashes;collection_problems=@()} (Join-Path $folder 'manifest.json')
        }
        Get-ChildItem -LiteralPath $out -File | ForEach-Object { $_.LastWriteTimeUtc = [DateTime]::UtcNow }
        if ($mode -eq 'stale') { (Get-Item -LiteralPath (Join-Path $out "$name.actual.png")).LastWriteTimeUtc = [DateTime]::UtcNow.AddDays(-1) }
        return @{Code=$rc;Text='synthetic'}
    }
    # Real Pillow decoding and existing comparator on temporary fixture bytes only.
    return (& $realProcess $realPython $Arguments (Join-Path $repo 'qa_visual') $Log $Seconds)
}

try {
    $white = Join-Path $sandbox 'white.png'; $black = Join-Path $sandbox 'black.png'
    $code = 'from PIL import Image; import sys; Image.new("RGB",(1,1),"white").save(sys.argv[1]); Image.new("RGB",(1,1),"black").save(sys.argv[2])'
    $r = & $realProcess $realPython @('-c',$code,$white,$black) $sandbox '' 30
    Assert-Test ($r.Code -eq 0) 'Fixture generation'
    foreach ($name in @('long_headline','breaking_news','dark_article','no_image','empty_feed')) {
        Test-Case "accepted pass: $name" {
            New-TestRoot
            if ($name -ne 'breaking_news') { [IO.File]::Move($baseline, (Join-Path (Split-Path $baseline) "$name.png")) }
            $p = Invoke-GCapture $root $name
            Assert-Test ((Read-GJson (Join-Path $p 'manifest.json')).classification -eq 'comparison-pass') 'Pass classification'
        }
    }
    foreach ($invalid in @('bogus','BREAKING_NEWS','../long_headline','..\breaking_news','C:\outside')) {
        Test-Case "reject scenario: $invalid" { Must-Reject { Get-GNode $invalid } 'Unsupported' }
    }
    foreach ($badDevice in @('wrong','unavailable')) {
        Test-Case "reject device: $badDevice" { New-TestRoot; $script:deviceMode=$badDevice; Must-Reject { Invoke-GCapture $root 'breaking_news' } 'profile|incompatible' }
    }
    foreach ($key in @('VVP_GOLDEN_PROFILE','VVP_CHANNEL_TOLERANCE','VVP_MAX_CHANGED_RATIO','VVP_QA_LAUNCH_URL')) {
        Test-Case "reject inherited override: $key" {
            [Environment]::SetEnvironmentVariable($key, 'invalid')
            try { Must-Reject { Assert-GEnvironment 'breaking_news' } 'environment|URL' }
            finally { [Environment]::SetEnvironmentVariable($key, $null) }
        }
    }
    foreach ($bad in @('stale','startup','identity','readiness','cleanup','no-context','contradictory','bad-junit','wrong-node','teardown','skip','no-junit','interrupted','no-actual','bad-png','extra-test','wrong-count')) {
        Test-Case "capture rejected, evidence retained: $bad" {
            New-TestRoot; $script:mode=$bad
            $before = Get-GHash $baseline
            Must-Reject { Invoke-GCapture $root 'breaking_news' } '.'
            Assert-Test ((Get-GHash $baseline) -eq $before) 'Baseline changed on rejection'
            $packets = @(Get-ChildItem -LiteralPath (Join-Path $root 'qa_visual/artifacts/review') -Directory)
            Assert-Test ($packets.Count -eq 1 -and (Test-Path -LiteralPath (Join-Path $packets[0].FullName 'REJECTED.txt'))) 'Rejected packet absent'
            Assert-Test (!(Test-Path -LiteralPath (Join-Path $packets[0].FullName 'manifest.json'))) 'Rejected packet accepted'
        }
    }
    foreach ($good in @('mismatch','missing')) {
        Test-Case "accepted: $good" {
            New-TestRoot; $script:mode=$good
            if ($good -eq 'missing') { Remove-Item -LiteralPath $baseline }
            $p = Invoke-GCapture $root 'breaking_news'
            $expected = if ($good -eq 'missing') { 'golden-missing' } else { 'comparison-mismatch' }
            Assert-Test ((Read-GJson (Join-Path $p 'manifest.json')).classification -eq $expected) 'Wrong classification'
            Invoke-GPromotion $root $p (Get-GHash (Join-Path $p 'candidate.png'))
            Assert-Test ((Get-GHash $baseline) -eq (Get-GHash (Join-Path $p 'candidate.png'))) 'Promotion bytes'
        }
    }
    Test-Case 'old rolling output preserved and never accepted as current' {
        New-TestRoot
        $old = Join-Path $root 'qa_visual/artifacts/android/pixel10-api37/breaking_news.actual.png'
        [IO.File]::Copy($black, $old)
        $script:mode='no-actual'
        Must-Reject { Invoke-GCapture $root 'breaking_news' } '.'
        $p = (Get-ChildItem (Join-Path $root 'qa_visual/artifacts/review') -Directory)[0].FullName
        Assert-Test ((Get-GHash (Join-Path $p 'prior/breaking_news.actual.png')) -eq (Get-GHash $black)) 'Prior bytes lost'
    }
    Test-Case 'exclusive lock rejects capture and promotion' {
        New-TestRoot; $held = Enter-GLock $root
        try {
            Must-Reject { Invoke-GCapture $root 'breaking_news' } 'lock'
            Must-Reject { Invoke-GPromotion $root 'unused' ('a'*64) } 'lock'
        } finally { $held.Dispose() }
    }
    Test-Case 'separate PowerShell process cannot acquire held helper lock' {
        New-TestRoot; $held = Enter-GLock $root
        try {
            $lockPath = (Join-Path $root 'qa_visual/artifacts/golden-helper.lock').Replace("'", "''")
            $code = "try { `$h=[IO.File]::Open('$lockPath','OpenOrCreate','ReadWrite','None'); `$h.Dispose(); exit 9 } catch { exit 0 }"
            $encoded = [Convert]::ToBase64String([Text.Encoding]::Unicode.GetBytes($code))
            $r = & $realProcess (Join-Path $PSHOME 'powershell.exe') @('-NoProfile','-EncodedCommand',$encoded) $root '' 15
            Assert-Test ($r.Code -eq 0) 'Child process acquired lock'
        } finally { $held.Dispose() }
    }
    foreach ($fault in @('hash','changed-reference','declined','backup','invalid-png','path-entry','scenario','outside','tampered-artifact')) {
        Test-Case "promotion rejected: $fault" {
            New-TestRoot; $p = Invoke-GCapture $root 'breaking_news'
            $candidate = Join-Path $p 'candidate.png'; $hash = Get-GHash $candidate
            switch ($fault) {
                hash { $hash = '0'*64 }
                changed-reference { [IO.File]::Copy($black, $baseline, $true) }
                declined { $script:confirmation='NO' }
                backup { [IO.File]::Copy($black, (Join-Path $p 'previous-approved.png')) }
                invalid-png { [IO.File]::WriteAllText($candidate, 'broken') }
                path-entry { $m=Read-GJson (Join-Path $p 'manifest.json'); $m.files_sha256 | Add-Member NoteProperty '../escape' ('a'*64); Write-GJson $m (Join-Path $p 'manifest.json') }
                scenario { $m=Read-GJson (Join-Path $p 'manifest.json'); $m.scenario='../escape'; Write-GJson $m (Join-Path $p 'manifest.json') }
                outside { $p=$sandbox }
                tampered-artifact { [IO.File]::AppendAllText((Join-Path $p 'pytest.log'), 'changed') }
            }
            $before = Get-GHash $baseline
            Must-Reject { Invoke-GPromotion $root $p $hash } '.'
            Assert-Test ((Get-GHash $baseline) -eq $before) 'Rejected promotion changed destination'
        }
    }
    Test-Case 'promotion derives destination, backs up exact bytes and records pending status' {
        New-TestRoot; $script:mode='mismatch'; $p=Invoke-GCapture $root 'breaking_news'
        $before=Get-GHash $baseline; $hash=Get-GHash (Join-Path $p 'candidate.png')
        Invoke-GPromotion $root $p $hash
        Assert-Test ((Get-GHash $baseline) -eq $hash) 'Destination mismatch'
        Assert-Test ((Get-GHash (Join-Path $p 'previous-approved.png')) -eq $before) 'Backup mismatch'
        Assert-Test ((Read-GJson (Join-Path $p 'promotion.json')).status -eq 'promoted-native-verification-pending') 'Wrong promotion state'
        Must-Reject { Invoke-GPromotion $root $p $hash } 'changed|already exists'
    }
    Test-Case 'destination hash failure retains backup and failure record' {
        New-TestRoot; $p=Invoke-GCapture $root 'breaking_news'; $before=Get-GHash $baseline
        function Copy-GCandidate([string]$Source,[string]$Destination,[bool]$Replace) { [IO.File]::Copy($black,$Destination,$Replace) }
        try {
            Must-Reject { Invoke-GPromotion $root $p (Get-GHash (Join-Path $p 'candidate.png')) } 'Destination hash'
            Assert-Test ((Get-GHash (Join-Path $p 'previous-approved.png')) -eq $before) 'Failure lost backup'
            Assert-Test ((Read-GJson (Join-Path $p 'promotion.json')).status -eq 'copy-or-verification-failed') 'Failure not recorded'
        } finally { Remove-Item Function:Copy-GCandidate }
    }
    Test-Case 'reparse point and path traversal rejected' {
        New-TestRoot
        Must-Reject { Assert-GPath (Join-Path $root '../outside') $root } 'escapes'
        $link=Join-Path $root 'link'
        New-Item -ItemType Junction -Path $link -Target $sandbox | Out-Null
        try { Must-Reject { Assert-GPath (Join-Path $link 'candidate.png') $root } 'Reparse' }
        finally { [IO.Directory]::Delete($link) }
    }
    Write-Host "RESULT: $count safety cases passed; no emulator, Appium or native pytest used."
} finally {
    foreach ($key in $keys) { [Environment]::SetEnvironmentVariable($key, $saved[$key]) }
    # Verify scope before recursive removal; junction test removes its link first.
    $safe = [IO.Path]::GetFullPath($sandbox)
    if ($safe.StartsWith([IO.Path]::GetTempPath(), [StringComparison]::OrdinalIgnoreCase) -and (Split-Path $safe -Leaf) -like 'golden-tests-*') {
        Remove-Item -LiteralPath $safe -Recurse -Force
    }
}
