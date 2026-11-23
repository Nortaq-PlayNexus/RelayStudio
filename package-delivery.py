"""Build the small browser-only demo; not the Windows installer."""
from pathlib import Path
import zipfile,re
root=Path(__file__).resolve().parent
html=(root/'public/index.html').read_text().replace('<body>','<body data-standalone="true">')
for sheet in ['style','desktop-ui']:
    css=(root/f'public/{sheet}.css').read_text()
    html=re.sub(r'<link\b[^>]*href=[\"\x27]/'+re.escape(sheet)+r'\.css[\"\x27][^>]*>',lambda m:'<style>'+css+'</style>',html)
for script in ['sculpture','app','polish','desktop-ui']:
    html=html.replace(f'<script src="/{script}.js"></script>','<script>'+(root/f'public/{script}.js').read_text()+'</script>')
assert 'src="/' not in html
name='Relay-Studio-Browser-04'
(root/f'{name}.html').write_text(html)
(root.parent/f'{name}.html').write_text(html)
files=['README.md','DESIGN.md','UI-REFINEMENT.md','TEST-RESULTS.md','Start-Relay.cmd','server.mjs','tests.mjs','package-delivery.py',f'{name}.html']
files+=[str(p.relative_to(root)) for p in (root/'public').glob('*') if p.is_file()]
with zipfile.ZipFile(root.parent/f'{name}.zip','w',zipfile.ZIP_DEFLATED) as z:
    for f in files:z.write(root/f,'relay/'+f)
print(name+'.html and browser-only source ZIP ready.')
