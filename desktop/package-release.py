"""Package the already-built Windows installer with source and verification data."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT.parent
CACHE=ROOT/'node_modules/desktop-runtime'
INSTALLER=CACHE/'RelayStudio-0.4.0-Windows-x64-Setup.exe'
NAME='Relay-Studio-Desktop-04-Windows-x64'
def sha(p):
    with open(p,'rb') as f:return hashlib.file_digest(f,'sha256').hexdigest()
assert INSTALLER.exists()
assert INSTALLER.stat().st_size>=100*1024*1024,'Installer is below the requested meaningful-size target'
source=CACHE/'Relay-Studio-Desktop-04-Source.zip'
files=['README.md','DESIGN.md','UI-REFINEMENT.md','UPGRADE-NOTES.md','TEST-RESULTS.md','server.mjs','tests.mjs','package-delivery.py','Start-Relay.cmd']
for folder in ['desktop','public']:
    files.extend(str(p.relative_to(ROOT)) for p in (ROOT/folder).rglob('*') if p.is_file())
with zipfile.ZipFile(source,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for f in sorted(set(files)):z.write(ROOT/f,'relay/'+f)
report={
 'product':'Relay Studio Desktop','version':'0.4.0','intendedTarget':'Windows 11 x64','runtime':'Electron 45.4.1',
 'runtimeSource':'https://github.com/electron/electron/releases/download/v45.4.1/electron-v45.4.1-win32-x64.zip',
 'runtimeSHA256':'2ba6223afa9121f42831fefe92c434334907540165294fc56697449d12e7cfe9',
 'runtimeChecksumVerified':True,'installer':INSTALLER.name,'installerBytes':INSTALLER.stat().st_size,'installerSHA256':sha(INSTALLER),
 'sourceArchive':source.name,'sourceSHA256':sha(source),'installedPayloadBytes':sum(p.stat().st_size for p in (CACHE/'staging').rglob('*') if p.is_file()),
 'sizeTargetBytes':100*1024*1024,'sizeReason':'Complete bundled Windows runtime, application and licences; no filler or padding.',
 'signing':'Unsigned evaluation installer','windowsExecutionTested':False,'windowsDPAPITested':False,
 'linuxElectronShellTested':True,'nativeDialogsMockedInTests':True,'realProviderInferenceTested':False,
 'installerArchiveIntegrity':'7-Zip NSIS archive integrity test passed; extracted application files matched staging SHA-256 values.',
 'appSourceSHA256':{str(p.relative_to(CACHE/'staging')):sha(p) for p in (CACHE/'staging/resources/app').rglob('*') if p.is_file()}
}
readme=(ROOT/'desktop/README-WINDOWS.md').read_text()
checksums=f'{sha(INSTALLER)}  {INSTALLER.name}\n{sha(source)}  {source.name}\n'
verify=f'''# Read-only verification of the two main delivery artifacts.\n$ErrorActionPreference = 'Stop'\n$expected = @{{\n  '{INSTALLER.name}' = '{sha(INSTALLER)}'\n  '{source.name}' = '{sha(source)}'\n}}\nforeach ($entry in $expected.GetEnumerator()) {{\n  $actual = (Get-FileHash -Algorithm SHA256 -LiteralPath (Join-Path $PSScriptRoot $entry.Key)).Hash.ToLowerInvariant()\n  if ($actual -ne $entry.Value) {{ throw "Checksum mismatch: $($entry.Key)" }}\n  Write-Host "Verified: $($entry.Key)"\n}}\n'''
# Standard ZIP containing an already strongly compressed installer; no duplicate runtime.
final=OUT/(NAME+'.zip')
with zipfile.ZipFile(final,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    z.write(INSTALLER,INSTALLER.name)
    z.write(source,source.name)
    z.writestr('READ-FIRST-WINDOWS.md',readme)
    z.writestr('TEST-REPORT-DESKTOP.md',(ROOT/'desktop/TEST-REPORT-DESKTOP.md').read_text())
    z.writestr('BUILD-REPORT.json',json.dumps(report,indent=2))
    z.writestr('SHA256SUMS.txt',checksums)
    z.writestr('VERIFY-WINDOWS.ps1',verify)
    z.writestr('ELECTRON-LICENSE.txt',(CACHE/'staging/LICENSE').read_text())
    license_path=Path('/usr/share/doc/nsis/copyright')
    if license_path.exists():z.writestr('NSIS-LICENSE.txt',license_path.read_text())
assert final.stat().st_size>=100*1024*1024
with zipfile.ZipFile(final) as z:assert z.testzip() is None
report.update({'deliveryZIP':final.name,'deliveryZIPBytes':final.stat().st_size,'deliveryZIPDecimalMB':round(final.stat().st_size/1_000_000,3),'deliveryZIPMiB':round(final.stat().st_size/1024**2,3),'deliveryZIPSHA256':sha(final),'deliveryZIPIntegrity':'passed'})
(OUT/(NAME+'-report.json')).write_text(json.dumps(report,indent=2))
(OUT/(NAME+'.sha256')).write_text(sha(final)+'  '+final.name+'\n')
print(json.dumps({k:report[k] for k in ['deliveryZIP','deliveryZIPBytes','deliveryZIPDecimalMB','deliveryZIPMiB','deliveryZIPSHA256','deliveryZIPIntegrity']},indent=2))
