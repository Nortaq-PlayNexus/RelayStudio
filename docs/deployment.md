# Deployment / Release

## Intended distribution

Relay Studio Desktop 0.4.0 is distributed as an **unsigned Windows 11 x64 NSIS installer** with a bundled Electron runtime. The source zip and SHA256 manifest are included in the release package.

## Verify before install

```powershell
Get-FileHash .\RelayStudio-0.4.0-Windows-x64-Setup.exe -Algorithm SHA256
Get-FileHash .\Relay-Studio-Desktop-04-Source.zip -Algorithm SHA256
```

Compare against `SHA256SUMS.txt` / `docs/release/SHA256SUMS.txt`, or run `docs/release/VERIFY-WINDOWS.ps1`.

## Install

1. Close existing Relay Studio instances.
2. Run `RelayStudio-0.4.0-Windows-x64-Setup.exe`.
3. Default install is `%LOCALAPPDATA%\Programs\RelayStudio` (per-user, no admin by default).
4. Launch from Start menu.

## Uninstall

Use Windows Installed Apps or the Start menu shortcut. The uninstaller asks whether to delete Relay Studio user settings and encrypted saved keys. It does not delete exported conversations saved elsewhere.

## Release checklist

- [ ] Update version in `desktop/package.json`, `desktop/main.cjs`, docs, changelog.
- [ ] Run syntax checks and desktop tests on Windows where possible.
- [ ] Build installer with NSIS on a controlled machine.
- [ ] Verify Electron runtime checksum against official Electron release.
- [ ] Generate SHA256SUMS for installer/source.
- [ ] Test install/launch/uninstall on a real Windows 11 x64 machine.
- [ ] Test DPAPI save/restore/clear flow on Windows.
- [ ] Code-sign installer (release gate for non-evaluation distribution).
- [ ] Tag release and attach installer, source zip, checksums, READ-FIRST, test/build reports.

## Current release gate status (0.4.0)

- Code signing: **not done** (unsigned evaluation build).
- Real Windows install/DPAPI acceptance: **not done in delivery environment**.
- Native dialog behavior on Windows: **mocked in Linux tests**.
- Real provider inference benchmark: **not done**.
