from pathlib import Path
import subprocess,json,hashlib
root=Path('work/ui-research/upstream/style-85a6aaf');sha='85a6aafc7d003ec8f61c9543b352a1f1b0f47346'
m=json.loads((root/'manifest.json').read_text())
for path in ['scripts/generate_tokens_04.py','web/openaec-tokens.css','design/ontwerp-0.4/tokens-0.4.json']:
 if any(e['path']==path for e in m):continue
 data=subprocess.check_output(['gh','api',f'repos/OpenAEC-Foundation/OpenAEC-Style-Repo/contents/{path}?ref={sha}','-H','Accept: application/vnd.github.raw+json'])
 p=root/path;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 m.append(dict(path=path,url=f'https://github.com/OpenAEC-Foundation/OpenAEC-Style-Repo/blob/{sha}/{path}',sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
(root/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
print([(x['path'],x['bytes']) for x in m[-3:]])
