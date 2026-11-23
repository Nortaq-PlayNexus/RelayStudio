"""Rebuild the Windows installer on a host with Python 3 and NSIS.
Downloads only the pinned official Electron runtime and verifies its SHA-256.
The final desktop application does not require Python or Node installation.
"""
from pathlib import Path
import hashlib, json, shutil, subprocess, urllib.request, zipfile
ROOT=Path(__file__).resolve().parent.parent
CACHE=ROOT/'node_modules/desktop-runtime'
VERSION='45.4.1'
RUNTIME=f'electron-v{VERSION}-win32-x64.zip'
EXPECTED='2ba6223afa9121f42831fefe92c434334907540165294fc56697449d12e7cfe9'
CACHE.mkdir(parents=True,exist_ok=True)
archive=CACHE/RUNTIME
if not archive.exists():
    urllib.request.urlretrieve(f'https://github.com/electron/electron/releases/download/v{VERSION}/{RUNTIME}',archive)
assert hashlib.file_digest(open(archive,'rb'),'sha256').hexdigest()==EXPECTED,'Runtime checksum mismatch'
stage=CACHE/'staging'
if stage.exists():shutil.rmtree(stage)
with zipfile.ZipFile(archive) as z:z.extractall(stage)
(stage/'electron.exe').rename(stage/'RelayStudio.exe')
(stage/'resources/default_app.asar').unlink(missing_ok=True)
app=stage/'resources/app'
app.mkdir(parents=True,exist_ok=True)
for folder in ['desktop','public']:
    shutil.copytree(ROOT/folder,app/folder,ignore=shutil.ignore_patterns('tests.mjs','installer.nsi','README-WINDOWS.md','TEST-REPORT-DESKTOP.md','build.py'))
(app/'package.json').write_text(json.dumps({'name':'relay-studio','productName':'Relay Studio','version':'0.4.0','main':'desktop/main.cjs','private':True},indent=2))
shutil.copy(ROOT/'desktop/README-WINDOWS.md',stage/'README-WINDOWS.md')
subprocess.run(['makensis','-V3','installer.nsi'],cwd=ROOT/'desktop',check=True)
print(CACHE/'RelayStudio-0.4.0-Windows-x64-Setup.exe')
