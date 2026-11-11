#requires -Version 5.1
<#
Capture requires the existing emulator, development app, Metro and Appium.
Run no other pytest/device operations in this checkout while either helper runs.
The exclusive helper lock cannot control arbitrary external test processes.
Profile checks describe observable settings, not exact historical rendering parity.
Dot-sourcing defines functions only, allowing offline tests without native services.
#>
[CmdletBinding()]
param([string]$Scenario)

function Get-GNode([string]$Name) {
    $nodes = @{
        long_headline = 'test_long_headline_android_card_matches_reviewed_golden'
        breaking_news = 'test_breaking_news_banner_matches_reviewed_golden'
        dark_article = 'test_dark_article_android_card_matches_reviewed_golden'
        no_image = 'test_no_image_android_card_matches_reviewed_golden'
        empty_feed = 'test_empty_feed_android_state_matches_reviewed_golden'
    }
    if (!$Name -or $Name -cnotin @($nodes.Keys)) { throw 'Unsupported scenario.' }
    return $nodes[$Name]
}

function Assert-GPath([string]$Path, [string]$Within) {
    $full = [IO.Path]::GetFullPath($Path)
    $base = [IO.Path]::GetFullPath($Within).TrimEnd('\', '/')
    if ($full -ne $base -and !$full.StartsWith($base + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw 'Path escapes permitted directory.'
    }
    $cursor = $full
    while ($cursor) {
        if (Test-Path -LiteralPath $cursor) {
            if ((Get-Item -Force -LiteralPath $cursor).Attributes -band [IO.FileAttributes]::ReparsePoint) {
                throw 'Reparse points are not permitted.'
            }
        }
        $parent = [IO.Path]::GetDirectoryName($cursor)
        if ($parent -eq $cursor) { break }
        $cursor = $parent
    }
    return $full
}

function Get-GHash([string]$Path) {
    if (!(Test-Path -LiteralPath $Path -PathType Leaf)) { return $null }
    return (Get-FileHash -LiteralPath $Path -Algorithm SHA256).Hash.ToLowerInvariant()
}

function Write-GJson($Value, [string]$Path) {
    $Value | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $Path -Encoding UTF8
}

function Read-GJson([string]$Path) {
    return (Get-Content -Raw -LiteralPath $Path -ErrorAction Stop | ConvertFrom-Json -ErrorAction Stop)
}

function Enter-GLock([string]$Root) {
    $folder = Assert-GPath (Join-Path $Root 'qa_visual/artifacts') $Root
    [IO.Directory]::CreateDirectory($folder) | Out-Null
    $path = Assert-GPath (Join-Path $folder 'golden-helper.lock') $Root
    try { return [IO.File]::Open($path, 'OpenOrCreate', 'ReadWrite', 'None') }
    catch { throw 'Another golden helper holds the lock (or the lock is inaccessible).' }
}

function Invoke-GProcess([string]$Exe, [string[]]$Arguments, [string]$Working, [string]$Log, [int]$Seconds = 600) {
    # Windows command-line quoting; no shell interpretation or string-built commands.
    $quoted = foreach ($a in $Arguments) {
        '"' + ([regex]::Replace(([regex]::Replace($a, '(\\*)"', '$1$1\"')), '(\\+)$', '$1$1')) + '"'
    }
    $info = New-Object Diagnostics.ProcessStartInfo
    $info.FileName = $Exe
    $info.Arguments = $quoted -join ' '
    $info.WorkingDirectory = $Working
    $info.UseShellExecute = $false
    $info.CreateNoWindow = $true
    $info.RedirectStandardOutput = $true
    $info.RedirectStandardError = $true
    $p = New-Object Diagnostics.Process
    $p.StartInfo = $info
    try {
        if (!$p.Start()) { throw 'Process did not start.' }
        $stdout = $p.StandardOutput.ReadToEndAsync()
        $stderr = $p.StandardError.ReadToEndAsync()
        if (!$p.WaitForExit($Seconds * 1000)) {
            $p.Kill()
            $p.WaitForExit()
            if ($Log) { [IO.File]::WriteAllText($Log, $stdout.Result + "`n" + $stderr.Result) }
            throw 'Process timed out; execution incomplete.'
        }
        $result = $stdout.Result + "`n" + $stderr.Result
        if ($Log) { [IO.File]::WriteAllText($Log, $result) }
        return @{ Code = $p.ExitCode; Text = $result.Trim() }
    } finally { $p.Dispose() }
}

function Assert-GEnvironment([string]$Name) {
    Get-GNode $Name | Out-Null
    $defaults = @{
        VVP_GOLDEN_PROFILE = 'pixel10-api37'; VVP_ANDROID_UDID = 'emulator-5554'
        VVP_ANDROID_DEVICE = 'Pixel_10'; VVP_ANDROID_PACKAGE = 'de.volksverpetzer.app'
        VVP_ANDROID_ACTIVITY = '.MainActivity'; VVP_METRO_HOST = '127.0.0.1'; VVP_METRO_PORT = '8081'
        VVP_APPIUM_URL = 'http://127.0.0.1:4723'
        VVP_CHANNEL_TOLERANCE = '12'; VVP_MAX_CHANGED_RATIO = '0.002'
    }
    foreach ($key in $defaults.Keys) {
        $v = [Environment]::GetEnvironmentVariable($key)
        if ($null -ne $v -and $v -cne $defaults[$key]) { throw "Unsupported environment setting: $key" }
    }
    $url = [Environment]::GetEnvironmentVariable('VVP_QA_LAUNCH_URL')
    $expected = 'exp+vvpapp://expo-development-client/?url=http%3A%2F%2F127.0.0.1%3A8081&qa_scenario=' + $Name
    if ($url -and $url -cne $expected) { throw 'Conflicting/noncanonical VVP_QA_LAUNCH_URL; unset it.' }
    if ($env:PYTEST_ADDOPTS -or $env:PYTEST_PLUGINS) { throw 'Unset PYTEST_ADDOPTS and PYTEST_PLUGINS.' }
}

function Get-GDevice([string]$Root) {
    $queries = [ordered]@{
        state = @('get-state'); boot = @('shell','getprop','sys.boot_completed')
        api = @('shell','getprop','ro.build.version.sdk'); abi = @('shell','getprop','ro.product.cpu.abi')
        size = @('shell','wm','size'); density = @('shell','wm','density')
        font = @('shell','settings','get','system','font_scale')
        avd = @('emu','avd','name'); fingerprint = @('shell','getprop','ro.build.fingerprint')
        package = @('shell','pm','path','de.volksverpetzer.app')
    }
    $observed = [ordered]@{ serial = 'emulator-5554' }
    foreach ($key in $queries.Keys) {
        $r = Invoke-GProcess 'adb.exe' (@('-s','emulator-5554') + $queries[$key]) $Root '' 20
        if ($r.Code -ne 0) { throw "ADB query failed: $key" }
        $observed[$key] = $r.Text
    }
    Assert-GDevice $observed
    return $observed
}

function Assert-GDevice($d) {
    if ($d.serial -ne 'emulator-5554' -or $d.state -ne 'device' -or $d.boot -ne '1' -or
        $d.api -ne '37' -or $d.abi -ne 'x86_64' -or $d.font -notmatch '^1(?:\.0+)?$' -or
        $d.avd -notmatch '^Pixel_10(?:\r?\nOK)?$' -or !$d.fingerprint -or $d.package -notmatch '^package:') {
        throw 'Device unavailable or incompatible with pixel10-api37.'
    }
    $sizes = [regex]::Matches($d.size, '(?:Physical|Override) size: (\d+x\d+)')
    $densities = [regex]::Matches($d.density, '(?:Physical|Override) density: (\d+)')
    if (!$sizes.Count -or $sizes[$sizes.Count-1].Groups[1].Value -ne '1080x2424' -or
        !$densities.Count -or $densities[$densities.Count-1].Groups[1].Value -ne '420') { throw 'Wrong effective display profile.' }
}

function Assert-GPng([string]$Python, [string]$Path, [string]$Working) {
    $code = 'from PIL import Image; import sys; im=Image.open(sys.argv[1]); assert im.format=="PNG"; im.load(); assert im.width>0 and im.height>0'
    $r = Invoke-GProcess $Python @('-c', $code, $Path) $Working '' 30
    if ($r.Code -ne 0) { throw 'Missing or invalid PNG.' }
}

function Get-GClassification([string]$Packet, [string]$Name, [int]$ExitCode, [bool]$HadReference) {
    $node = Get-GNode $Name
    $settings = New-Object Xml.XmlReaderSettings
    $settings.DtdProcessing = [Xml.DtdProcessing]::Prohibit
    $reader = [Xml.XmlReader]::Create((Join-Path $Packet 'junit.xml'), $settings)
    try { $xml = New-Object Xml.XmlDocument; $xml.Load($reader) } finally { $reader.Dispose() }
    $cases = @($xml.SelectNodes('//testcase'))
    $suite = @($xml.SelectNodes('//testsuite'))
    if ($cases.Count -ne 1 -or $suite.Count -ne 1 -or $suite[0].tests -ne '1' -or
        $suite[0].errors -ne '0' -or $suite[0].skipped -ne '0' -or
        $cases[0].name -cne $node -or $cases[0].classname -cnotin @("tests.test_$Name", "qa_visual.tests.test_$Name") -or
        $xml.SelectNodes('//error|//skipped').Count) { throw 'Unexpected/incomplete JUnit result.' }
    $failures = @($cases[0].SelectNodes('failure'))
    if ($suite[0].failures -ne [string]$failures.Count -or $failures.Count -gt 1) { throw 'Contradictory JUnit failures.' }
    foreach ($required in @('candidate.png','context.png','pytest.log')) {
        if (!(Test-Path -LiteralPath (Join-Path $Packet $required) -PathType Leaf)) { throw "Missing evidence: $required" }
    }
    if ($Name -ne 'long_headline') {
        $meta = Read-GJson (Join-Path $Packet 'capture.json')
        if ($meta.scenario -cne $Name -or $meta.identity -cne "qa-scenario:$Name" -or !$meta.session -or
            !(Test-Path -LiteralPath (Join-Path $Packet 'hierarchy.xml'))) { throw 'Incomplete capture identity metadata.' }
    }
    if ($ExitCode -eq 0 -and !$failures.Count -and $HadReference) { $kind = 'comparison-pass' }
    elseif ($ExitCode -eq 1 -and $failures.Count -eq 1) {
        $message = $failures[0].GetAttribute('message')
        if ($HadReference -and $message.StartsWith('AssertionError: Visual regression: changed=')) { $kind = 'comparison-mismatch' }
        elseif (!$HadReference -and $message.StartsWith('Failed: Golden missing. An ACTUAL native screenshot was saved at ')) { $kind = 'golden-missing' }
        else { throw 'Failure was not an expected comparison failure.' }
    } else { throw 'Interrupted or contradictory pytest outcome.' }
    if ($HadReference) {
        $c = Read-GJson (Join-Path $Packet 'comparison.json')
        if ($c.channel_tolerance -ne 12 -or $c.max_changed_ratio -ne 0.002 -or
            $c.passed -isnot [bool] -or $c.passed -ne ($kind -eq 'comparison-pass') -or
            !(Test-Path -LiteralPath (Join-Path $Packet 'diff.png'))) { throw 'Contradictory comparison evidence.' }
    } elseif ((Test-Path -LiteralPath (Join-Path $Packet 'comparison.json')) -or
        (Test-Path -LiteralPath (Join-Path $Packet 'diff.png'))) { throw 'Metrics/diff without reference.' }
    if ($kind -ne 'comparison-pass') {
        $f = Read-GJson (Join-Path $Packet 'failure.json')
        $reason = if ($HadReference) { 'visual comparison failed' } else { 'golden missing' }
        if ($f.reason -cne $reason -or $f.scenario -cne $Name -or $f.test -notlike "*test_$Name.py::$node (call)" -or
            @($f.collection_problems).Count -ne 0 -or $f.files_sha256.'actual.png' -ne (Get-GHash (Join-Path $Packet 'candidate.png')) -or
            $f.files_sha256.'context.png' -ne (Get-GHash (Join-Path $Packet 'context.png'))) { throw 'Incomplete/mismatched failure retention evidence.' }
    }
    return $kind
}

function Invoke-GCapture([string]$Root, [string]$Name) {
    $ErrorActionPreference = 'Stop'
    Assert-GEnvironment $Name
    $lock = Enter-GLock $Root
    $packet = $null
    $before = $null
    try {
        $device = Get-GDevice $Root
        $qa = Join-Path $Root 'qa_visual'
        $python = Join-Path $qa '.venv/Scripts/python.exe'
        if (!(Test-Path -LiteralPath $python)) { throw 'Create qa_visual/.venv and install requirements first.' }
        $reviewRoot = Assert-GPath (Join-Path $qa 'artifacts/review') $Root
        $packet = Join-Path $reviewRoot ((Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssZ') + "-$Name-" + [guid]::NewGuid().ToString('N'))
        [IO.Directory]::CreateDirectory($packet) | Out-Null
        $output = Assert-GPath (Join-Path $qa 'artifacts/android/pixel10-api37') $Root
        [IO.Directory]::CreateDirectory($output) | Out-Null
        $baselines = Assert-GPath (Join-Path $qa 'baselines/android/pixel10-api37') $Root
        $before = @{}
        Get-ChildItem -LiteralPath $baselines -Filter '*.png' | ForEach-Object {
            Assert-GPath $_.FullName $Root | Out-Null
            $before[$_.Name] = Get-GHash $_.FullName
        }
        $reference = Join-Path $baselines "$Name.png"
        $referenceHash = Get-GHash $reference
        if ($referenceHash) { [IO.File]::Copy($reference, (Join-Path $packet 'reference.png'), $false) }
        $prior = Join-Path $packet 'prior'
        [IO.Directory]::CreateDirectory($prior) | Out-Null
        # Move old rolling evidence aside, including diagnostics. Failure packages remain intact.
        foreach ($f in @(Get-ChildItem -LiteralPath $output -File)) {
            if ($f.Name.StartsWith("$Name.") -or $f.Name -match '^(failure-|screenshot-error|page-source-error)') {
                Assert-GPath $f.FullName $Root | Out-Null
                Move-Item -LiteralPath $f.FullName -Destination (Join-Path $prior $f.Name)
            }
        }
        $launch = Assert-GPath (Join-Path $output "launch-diagnostics/$Name") $Root
        if (Test-Path -LiteralPath $launch) {
            Get-ChildItem -LiteralPath $launch -Recurse -Force | ForEach-Object { Assert-GPath $_.FullName $Root | Out-Null }
            Move-Item -LiteralPath $launch -Destination (Join-Path $prior 'launch-diagnostics')
        }
        $failureRoot = Join-Path $output 'failures'
        Assert-GPath $failureRoot $Root | Out-Null
        $oldFailures = @(Get-ChildItem -LiteralPath $failureRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object Name)
        $node = Get-GNode $Name
        $arguments = @('-m','pytest',"tests/test_$Name.py::$node",'-v','-s',"--junitxml=$(Join-Path $packet 'junit.xml')")
        $started = [DateTime]::UtcNow
        $run = Invoke-GProcess $python $arguments $qa (Join-Path $packet 'pytest.log')
        if (Test-Path -LiteralPath $launch) {
            Get-ChildItem -LiteralPath $launch -Recurse -Force | ForEach-Object { Assert-GPath $_.FullName $Root | Out-Null }
            Copy-Item -LiteralPath $launch -Destination (Join-Path $packet 'launch-diagnostics') -Recurse
            throw 'Launch failure diagnostics present; capture rejected.'
        }
        foreach ($suffix in @('actual.png','context.png','diff.png','comparison.json','capture.json','hierarchy.xml')) {
            $source = Assert-GPath (Join-Path $output "$Name.$suffix") $Root
            if (Test-Path -LiteralPath $source) {
                if ((Get-Item -LiteralPath $source).LastWriteTimeUtc -lt $started) { throw 'Stale capture evidence.' }
                $target = if ($suffix -eq 'actual.png') { 'candidate.png' } else { $suffix }
                [IO.File]::Copy($source, (Join-Path $packet $target), $false)
            }
        }
        foreach ($f in @(Get-ChildItem -LiteralPath $output -File | Where-Object Name -Match '^(failure-|screenshot-error|page-source-error)')) {
            Assert-GPath $f.FullName $Root | Out-Null
            [IO.File]::Copy($f.FullName, (Join-Path $packet $f.Name), $false)
            throw 'Driver failure diagnostics present; capture rejected.'
        }
        $newFailures = @(Get-ChildItem -LiteralPath $failureRoot -Directory -ErrorAction SilentlyContinue | Where-Object { $_.Name -notin $oldFailures })
        if ($newFailures.Count -gt 1) { throw 'Concurrent/unrelated failure evidence detected.' }
        if ($newFailures.Count -eq 1) {
            $fp = Assert-GPath (Join-Path $newFailures[0].FullName 'manifest.json') $Root
            $fm = Read-GJson $fp
            # Do not replicate arbitrary VVP_* environment values from the runner manifest.
            Write-GJson ([ordered]@{ reason=$fm.reason; scenario=$fm.scenario; test=$fm.test; files_sha256=$fm.files_sha256; collection_problems=$fm.collection_problems }) (Join-Path $packet 'failure.json')
        }
        Assert-GPng $python (Join-Path $packet 'candidate.png') $qa
        Assert-GPng $python (Join-Path $packet 'context.png') $qa
        $kind = Get-GClassification $packet $Name $run.Code ([bool]$referenceHash)
        if ($kind -eq 'comparison-pass' -and $newFailures.Count) { throw 'Contradictory failure package.' }
        if ($referenceHash) {
            # Independently recompute metrics from packet bytes with the unchanged comparator.
            $code = 'import sys,json; from pathlib import Path; from dataclasses import asdict; from visualqa.image_diff import compare_png; p=Path(sys.argv[1]); r=asdict(compare_png(p/"reference.png",p/"candidate.png",p/"verified.diff.png")); assert json.loads(json.dumps(r))==json.loads((p/"comparison.json").read_text(encoding="utf-8-sig"))'
            $check = Invoke-GProcess $python @('-c', $code, $packet) $qa '' 30
            if ($check.Code -ne 0) { throw 'Comparison does not match preserved PNG bytes.' }
        }
        $afterDevice = Get-GDevice $Root
        if (($device | ConvertTo-Json -Compress) -cne ($afterDevice | ConvertTo-Json -Compress)) { throw 'Device observations changed during capture.' }
        $head = Invoke-GProcess 'git.exe' @('rev-parse','HEAD') $Root '' 10
        if ($head.Code -ne 0 -or $head.Text -notmatch '^[a-f0-9]{40}$') { throw 'Cannot establish source commit.' }
        $hashes = @{}
        Get-ChildItem -LiteralPath $packet -File | ForEach-Object { $hashes[$_.Name] = Get-GHash $_.FullName }
        Write-GJson ([ordered]@{
            schema='golden-review-v1'; producer='capture-candidate.ps1'; accepted=$true
            scenario=$Name; profile='pixel10-api37'; classification=$kind; candidate_sha256=$hashes['candidate.png']
            reference_sha256=$referenceHash; device=$device; source_commit=$head.Text
            started_utc=$started.ToString('o'); completed_utc=[DateTime]::UtcNow.ToString('o'); pytest_exit=$run.Code
            command=@('.venv/Scripts/python.exe','-m','pytest',"tests/test_$Name.py::$node",'-v','-s','--junitxml=<packet>/junit.xml')
            files_sha256=$hashes; missing_optional=@(@('capture.json','hierarchy.xml','diff.png','comparison.json','reference.png') | Where-Object { !$hashes.ContainsKey($_) })
            limitations='Exclusive helper lock does not control external pytest/device operations; observable profile is not historical rendering certification.'
        }) (Join-Path $packet 'manifest.json')
        Write-Host "CANDIDATE CAPTURED ($kind): $packet"
        Write-Host "SHA-256: $($hashes['candidate.png']). Human review and independent stability capture required before approval."
        return $packet
    } catch {
        if ($packet) {
            # A rejected packet must never retain an acceptance manifest.
            if (Test-Path -LiteralPath (Join-Path $packet 'manifest.json')) { Remove-Item -LiteralPath (Join-Path $packet 'manifest.json') }
            'Capture rejected; evidence retained. See pytest.log and the reported exception.' | Set-Content -LiteralPath (Join-Path $packet 'REJECTED.txt')
            Write-Warning "Rejected packet retained: $packet"
        }
        throw
    } finally {
        try {
            if ($before) {
                $after = @{}
                Get-ChildItem -LiteralPath $baselines -Filter '*.png' | ForEach-Object { $after[$_.Name] = Get-GHash $_.FullName }
                if (($before.Keys.Count -ne $after.Keys.Count) -or @($before.Keys | Where-Object { $before[$_] -ne $after[$_] }).Count) {
                    if ($packet -and (Test-Path -LiteralPath (Join-Path $packet 'manifest.json'))) { Remove-Item -LiteralPath (Join-Path $packet 'manifest.json') }
                    throw 'Golden reference changed during capture; no candidate accepted. Investigate external activity.'
                }
            }
        } finally { $lock.Dispose() }
    }
}

if ($MyInvocation.InvocationName -ne '.') {
    Invoke-GCapture ([IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../..'))) $Scenario
}
