"""Package the unchanged static map into one offline-preview HTML file."""
import argparse
import base64
import hashlib
import json
import mimetypes
import re
from pathlib import Path


def replace_once(text, old, new):
    if text.count(old) != 1:
        raise ValueError(f'Expected one source marker: {old}')
    return text.replace(old, new, 1)


def json_script(identifier, value):
    # JSON in a script element must not contain an HTML closing tag.
    payload = json.dumps(value, separators=(',', ':'), ensure_ascii=True).replace('<', '\\u003c')
    return f'<script type="application/json" id="{identifier}">{payload}</script>'


def build(app, destination):
    data = json.loads((app / 'assets/data.json').read_text())
    review = json.loads((app / 'local-review.json').read_text())
    image_names = ['assets/satellite.jpg', 'assets/excluded.png']
    image_names += [f'assets/{layer}-{date}.png' for layer in ['temperature', 'greenery', 'buildings', 'priority', 'uncertainty'] for date in data['dates']]
    for cell in review.get('cells', []):
        for kind, suffix in [('photos', r'jpe?g|png|webp'), ('videos', r'mp4|webm')]:
            for media in cell.get(kind, []):
                name = media.get('src', '')
                if not re.fullmatch(r'assets/site-photos/[a-zA-Z0-9_-]+\.(' + suffix + ')', name):
                    raise ValueError(f'Unsafe site-media path: {name}')
                if app.resolve() not in (app / name).resolve().parents:
                    raise ValueError(f'Site-media path escapes app: {name}')
                image_names.append(name)
    image_names = list(dict.fromkeys(image_names))
    images = {}
    for name in image_names:
        mime = mimetypes.guess_type(name)[0]
        images[name] = f'data:{mime};base64,' + base64.b64encode((app / name).read_bytes()).decode('ascii')

    html = (app / 'index.html').read_text()
    css = (app / 'style.css').read_text()
    javascript = (app / 'app.js').read_text()
    html = replace_once(html, '<link rel="stylesheet" href="style.css">', '<style>' + css + '</style>')
    for name in ['assets/satellite.jpg', 'assets/excluded.png']:
        html = replace_once(html, f'href="{name}"', f'href="{images[name]}"')
    javascript = replace_once(javascript, "fetch('assets/data.json')", "Promise.resolve({ok:true,json:async()=>JSON.parse(document.getElementById('preview-data').textContent)})")
    javascript = replace_once(javascript, "fetch('local-review.json')", "Promise.resolve({ok:true,json:async()=>JSON.parse(document.getElementById('preview-review').textContent)})")
    javascript = replace_once(javascript, '`assets/${state.layer}-${state.date}.png`', 'previewImages[`assets/${state.layer}-${state.date}.png`]')
    javascript = replace_once(javascript, 'const reviewPhotoSource=src=>src;', 'const reviewPhotoSource=src=>previewImages[src]||"";')
    scripts = json_script('preview-data', data) + json_script('preview-review', review) + json_script('preview-images', images)
    scripts += '<script>const previewImages=JSON.parse(document.getElementById("preview-images").textContent);\n' + javascript + '</script>'
    html = replace_once(html, '<script src="app.js"></script>', scripts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(html)
    return {'output': str(destination), 'bytes': destination.stat().st_size, 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(), 'embedded_images': sum(src.startswith('data:image/') for src in images.values()), 'embedded_videos': sum(src.startswith('data:video/') for src in images.values()), 'cells': len(data['cells']), 'dates': data['dates']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[1] / 'app')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(build(args.app, args.output), indent=2))
