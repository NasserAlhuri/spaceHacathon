"""Apply the reviewed wording corrections to a verified baseline deck and PDF.

Keep the 12-slide design: only four text nodes in slides 5, 9 and 10 change.
The matching PDF retains every untouched page and redraws only those paragraphs
with its existing Noto Sans size, colour, baseline and background. This is a
content/geometry check, not a claim of desktop PowerPoint rendering or rehearsal.
Original scientific data and application/preview files are never read as outputs
or changed. Supply the pre-correction baseline files from source 865c7f2d... .
"""
import argparse
import hashlib
import json
import zipfile
from pathlib import Path

import fitz
from lxml import etree

REPLACEMENTS = [
    (5, 'Deterministic processing; upstream WorldCover uses ML. Our own segmentation model is future work.',
     'External AI land cover: WorldCover for heat screening; Dynamic World in a separate experiment. QA/ranking are rule based. No new model trained.'),
    (9, 'Optical rule checks: 24/25 grass points pass; 0/30 building points pass. All 30 coastal points are excluded from thermal support.',
     'NDVI >=0.30 at 24/25 grass references and 0/30 building references. All 30 coastal references are excluded from retained thermal support.'),
    (10, 'Completed: reproducible satellite screening, sensitivity checks and local-review examples for site assessment.',
     'Completed: satellite screening, sensitivity checks, local examples and assistant review of 18 sites across four dates.'),
    (10, 'Exported: September 2021/2026 Dynamic World. Primary matched coverage: 30.94% (50% required). Dated-imagery scientific review is pending; 2023 is deferred.',
     'Limited Dynamic World experiment: common coverage 30.94% (50% gate). Independent scientific validation pending; 2023 deferred.'),
]


def normalized(text):
    return ' '.join(text.split())


def wrapped(text, font, size, width):
    lines = ['']
    for word in text.split():
        candidate = (lines[-1] + ' ' + word).strip()
        if font.text_length(candidate, fontsize=size) > width:
            assert lines[-1], 'A word does not fit the retained text box'
            lines.append(word)
        else:
            lines[-1] = candidate
    return lines


def revise(pptx, pdf, output, font_file):
    assert pptx.resolve() != (output / pptx.name).resolve()
    assert pdf.resolve() != (output / pdf.name).resolve()
    output.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(pptx) as old, zipfile.ZipFile(output / pptx.name, 'w') as new:
        assert old.testzip() is None
        for info in old.infolist():
            data = old.read(info.filename)
            changes = [r for r in REPLACEMENTS if info.filename == f'ppt/slides/slide{r[0]}.xml']
            if changes:
                tree = etree.fromstring(data)
                for _, before, after in changes:
                    nodes = [n for n in tree.iter('{http://schemas.openxmlformats.org/drawingml/2006/main}t') if n.text == before]
                    assert len(nodes) == 1, (info.filename, before)
                    nodes[0].text = after
                data = etree.tostring(tree, xml_declaration=True, encoding='UTF-8', standalone=True)
            new.writestr(info, data)
    font = fitz.Font(fontfile=str(font_file))
    report = {'method': 'retain original OOXML and PDF design; replace four reviewed paragraphs',
              'desktop_powerpoint_opened': False, 'slides_changed': [5, 9, 10], 'paragraphs': []}
    with fitz.open(pdf) as document:
        assert len(document) == 12
        grouped = {}
        for number, before, after in REPLACEMENTS:
            page = document[number - 1]
            candidates = [b for b in page.get_text('dict')['blocks'] if 'lines' in b and
                          normalized(''.join(s['text'] for line in b['lines'] for s in line['spans'])) == before]
            assert len(candidates) == 1, (number, before)
            block = candidates[0]
            span = block['lines'][0]['spans'][0]
            x, y = span['origin']
            size = span['size']
            leading = block['lines'][1]['spans'][0]['origin'][1] - y
            colour = tuple(((span['color'] >> shift) & 255) / 255 for shift in [16, 8, 0])
            width = 825.6 if number == 5 else 849.6
            lines = wrapped(after, font, size, width)
            assert len(lines) <= 2, 'Shorten text instead of changing design/font size'
            rect = fitz.Rect(block['bbox']) + (-1, -1, 1, 1)
            background = tuple(v/255 for v in page.get_pixmap().pixel(54, 470))
            grouped.setdefault(number, []).append((rect, background, x, y, size, leading, colour, lines))
            report['paragraphs'].append({'slide': number, 'before': before, 'after': after,
                                        'font': 'Noto Sans Regular, matching existing PDF',
                                        'font_size': size, 'line_count': len(lines), 'baseline': [x, y],
                                        'line_spacing': leading, 'redaction_rect': list(rect)})
        for number, changes in grouped.items():
            page = document[number - 1]
            for rect, background, *_ in changes:
                page.add_redact_annot(rect, fill=background, cross_out=False)
            page.apply_redactions(images=0, graphics=0)
            for _, _, x, y, size, leading, colour, lines in changes:
                for j, line in enumerate(lines):
                    page.insert_text((x, y + j*leading), line, fontname='ReviewedNoto', fontfile=str(font_file), fontsize=size, color=colour)
        document.save(output/pdf.name, garbage=4, deflate=True)
    report['files'] = {n: {'bytes': (output/n).stat().st_size, 'sha256': hashlib.sha256((output/n).read_bytes()).hexdigest()}
                       for n in [pdf.name, pptx.name]}
    (output/'presentation-edit-details.json').write_text(json.dumps(report, indent=2)+'\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseline-pptx', required=True, type=Path)
    parser.add_argument('--baseline-pdf', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--font', type=Path, default=Path('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf'))
    args = parser.parse_args()
    print(json.dumps(revise(args.baseline_pptx, args.baseline_pdf, args.output, args.font), indent=2))
