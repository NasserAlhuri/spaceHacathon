from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'REASSEMBLY.json').read_text())
for item in manifest['files']:
    target=root/item['name']
    if Path(item['name']).name!=item['name']: raise ValueError('Unsafe output name')
    assembled=hashlib.sha256();size=0
    with target.open('wb') as output:
        for part in item['parts']:
            if Path(part['name']).name!=part['name']: raise ValueError('Unsafe part name')
            data=(root/part['name']).read_bytes()
            if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
                raise ValueError('Corrupt or incomplete part: '+part['name'])
            output.write(data);assembled.update(data);size+=len(data)
    if size!=item['bytes'] or assembled.hexdigest()!=item['sha256']:
        raise ValueError('Reassembled file mismatch: '+item['name'])
    print('Verified exact original:',item['name'],size,assembled.hexdigest())
