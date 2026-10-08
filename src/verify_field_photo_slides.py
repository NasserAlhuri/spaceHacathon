"""Verify presentation/media changes against an external public-tree baseline.

No analysis is run. Native desktop PowerPoint rendering is not tested.
"""
import argparse
import hashlib
import json
import re
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import fitz
import numpy as np
from lxml import etree
from pptx import Presentation

from add_field_photos_to_presentation import CHANGES, PHOTOS

ALLOWED_EXISTING = {
    'PROJECT_STATE.md', 'README.md', 'PACKAGE-SHA256.json',
    'docs/UrbanHeat-AlKhor-Pitch.pdf', 'docs/UrbanHeat-AlKhor-Pitch.pptx',
    'docs/Three-Minute-Presentation.md', 'docs/Delivery-Guide.md',
    'docs/Site-Media-Receipt-2026-10-08.md', 'docs/Submission-Checklist.md',
    'src/build_delivery.py',
}
REGIONS = {6: [(48, 102, 913, 475)], 8: [(48, 321, 914, 383)],
           11: [(48, 185, 914, 247), (48, 477, 914, 529)],
           12: [(48, 375, 914, 447)]}
NS = {'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',
      'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(element):
    return etree.tostring(element, method='c14n')


def verify(root, baseline, tree_file, timing_file):
    pdf_name = 'docs/UrbanHeat-AlKhor-Pitch.pdf'
    ppt_name = 'docs/UrbanHeat-AlKhor-Pitch.pptx'
    before = Presentation(baseline / ppt_name)
    after = Presentation(root / ppt_name)
    assert len(before.slides) == len(after.slides) == 12
    assert (before.slide_width, before.slide_height) == (after.slide_width, after.slide_height)
    for slide in after.slides:
        ids = [s.shape_id for s in slide.shapes]
        assert len(ids) == len(set(ids))
        for shape in slide.shapes:
            assert min(shape.left, shape.top) >= 0
            assert shape.left + shape.width <= after.slide_width
            assert shape.top + shape.height <= after.slide_height
    expected_parts = {'[Content_Types].xml', 'ppt/slides/slide6.xml',
                      'ppt/slides/_rels/slide6.xml.rels', 'ppt/slides/slide8.xml',
                      'ppt/slides/slide11.xml', 'ppt/slides/slide12.xml'}
    with zipfile.ZipFile(baseline / ppt_name) as a, zipfile.ZipFile(root / ppt_name) as b:
        assert a.testzip() is b.testzip() is None
        assert set(a.namelist()) <= set(b.namelist())
        changed = {n for n in a.namelist() if a.read(n) != b.read(n)}
        assert changed == expected_parts, changed
        added = set(b.namelist()) - set(a.namelist())
        assert len(added) == 3 and all(n.startswith('ppt/media/') for n in added)
        expected = {sha((root / 'app/assets/site-photos' / n).read_bytes()) for n, _, _ in PHOTOS}
        assert {sha(b.read(n)) for n in added} == expected
        # Original theme/fonts/media and all unrelated archive parts are exact.
        for number in [8, 11, 12]:
            left = etree.fromstring(a.read(f'ppt/slides/slide{number}.xml'))
            right = etree.fromstring(b.read(f'ppt/slides/slide{number}.xml'))
            shapes_a = left.find('p:cSld/p:spTree', NS)
            shapes_b = right.find('p:cSld/p:spTree', NS)
            assert len(shapes_a) == len(shapes_b)
            modified = {index + 2 for slide, index in CHANGES if slide == number}
            for index, (old, new) in enumerate(zip(shapes_a, shapes_b)):
                if index not in modified:
                    assert canonical(old) == canonical(new), (number, index)
                else:
                    assert canonical(old.find('p:spPr', NS)) == canonical(new.find('p:spPr', NS))
                    assert canonical(old.find('p:nvSpPr', NS)) == canonical(new.find('p:nvSpPr', NS))
        table_a = etree.fromstring(a.read('ppt/slides/slide8.xml')).find('.//a:tbl', NS)
        table_b = etree.fromstring(b.read('ppt/slides/slide8.xml')).find('.//a:tbl', NS)
        assert canonical(table_a) == canonical(table_b)
        for i in [0, 1]:
            assert canonical(before.slides[5].shapes[i]._element) == canonical(after.slides[5].shapes[i]._element)
    pictures = [s for s in after.slides[5].shapes if s.shape_type == 13]
    assert len(pictures) == 3
    photo_checks = []
    receipt = json.loads((root / 'metadata/site-media-receipt-2026-10-08.json').read_text())
    received = {item['filename']: item for item in receipt['items']}
    for picture, (filename, heading, _) in zip(pictures, PHOTOS):
        original = (root / 'app/assets/site-photos' / filename).read_bytes()
        assert picture.name == filename
        assert picture.image.blob == original
        assert sha(original) == received[filename]['sha256']
        assert not any([picture.crop_left, picture.crop_top, picture.crop_right, picture.crop_bottom])
        w, h = picture.image.size
        assert abs(picture.width / picture.height - w / h) < .00001
        description = picture._element.nvPicPr.cNvPr.get('descr')
        assert all(term in description for term in ['8 October 2026', '13:00–14:00',
                   'Qatar (UTC+3)', 'Shared capture window', 'Confirmed by Nasser, not EXIF',
                   'Exact per-file time: Unknown'])
        photo_checks.append({'filename': filename, 'case': heading, 'original_sha256': sha(original),
                             'pptx_native_picture_bytes_match': True, 'full_frame_aspect_ratio_preserved': True})
    text_checks = span_checks = 0
    pixels = []
    normalize = lambda text: re.sub(r'\s+', '', text)
    with fitz.open(baseline / pdf_name) as old, fitz.open(root / pdf_name) as new:
        assert len(old) == len(new) == 12
        extracted = {sha(new.extract_image(image[0])['image']) for image in new[5].get_images()}
        assert expected <= extracted, 'Original JPEG bytes must also match embedded PDF images.'
        for info in photo_checks:
            info['pdf_embedded_jpeg_bytes_match'] = True
        for number, (a, b, slide) in enumerate(zip(old, new, after.slides), 1):
            assert a.rect == b.rect
            page_text = normalize(b.get_text())
            for shape in slide.shapes:
                frames = [shape.text_frame] if shape.has_text_frame else []
                if shape.has_table:
                    frames += [cell.text_frame for row in shape.table.rows for cell in row.cells]
                for frame in frames:
                    for para in frame.paragraphs:
                        if para.text.strip():
                            assert normalize(para.text) in page_text, (number, para.text)
                            text_checks += 1
            for block in b.get_text('dict', flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']:
                for line in block.get('lines', []):
                    for span in line['spans']:
                        assert b.rect.contains(fitz.Rect(span['bbox'])), (number, span)
                        assert '\ufffd' not in span['text']
                        span_checks += 1
            aa = a.get_pixmap(alpha=False)
            bb = b.get_pixmap(alpha=False)
            array_a = np.frombuffer(aa.samples, dtype=np.uint8).reshape(aa.height, aa.width, aa.n)
            array_b = np.frombuffer(bb.samples, dtype=np.uint8).reshape(bb.height, bb.width, bb.n)
            assert array_a.shape == array_b.shape
            if number not in REGIONS:
                assert np.array_equal(array_a, array_b), number
                pixels.append({'slide': number, 'unchanged_rendered_pixels': 'identical'})
            else:
                mask = np.ones(array_a.shape[:2], dtype=bool)
                for x0, y0, x1, y1 in REGIONS[number]:
                    mask[y0:y1, x0:x1] = False
                assert np.array_equal(array_a[mask], array_b[mask]), ('unintended visual change', number)
                pixels.append({'slide': number, 'pixels_outside_changed_regions': 'identical'})
        image_page = new[5]
        # Explicit layout separations: headings/photos/captions/provenance/footer.
        for picture in pictures:
            assert picture.top / 12700 >= 133.2 - .1
            assert (picture.top + picture.height) / 12700 <= 385.2 + .1
        preview = root / 'results/field-photo-slide-review/slide-6.png'
        preview.parent.mkdir(exist_ok=True)
        image_page.get_pixmap(matrix=fitz.Matrix(4 / 3, 4 / 3), alpha=False).save(preview)
    tree = json.loads(tree_file.read_text())
    protected = []
    for item in tree['tree']:
        name = item['path']
        if item['type'] != 'blob' or name in ALLOWED_EXISTING:
            continue
        data = (root / name).read_bytes()
        assert hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest() == item['sha'], name
        protected.append(name)
    inputs = json.loads((root / 'data/sample_input/SHA256.json').read_text())
    tables = json.loads((root / 'metadata/original-results-sha256.json').read_text())
    assert len(inputs) == 35 and len(tables) == 7
    for name, expected_sha in inputs.items():
        assert sha((root / 'data/sample_input' / name).read_bytes()) == expected_sha
    for name, expected_sha in tables.items():
        assert sha((root / name).read_bytes()) == expected_sha
    for item in receipt['items']:
        assert sha((root / item['public_asset_path']).read_bytes()) == item['sha256']
    script = (root / 'docs/Three-Minute-Presentation.md').read_text()
    spoken = [re.search(r'## Slide ' + str(n) + r' — [^\n]+\n\n(.*?)(?=\n## |\Z)', script, re.S).group(1).strip() for n in range(1, 13)]
    timing = json.loads(timing_file.read_text())
    assert sum(len(s.split()) for s in spoken) == timing['word_count'] == 394
    assert timing['sections'][0]['start_seconds'] == 0 and timing['sections'][-1]['end_seconds'] == 180
    assert timing['actual_rehearsal_seconds'] is None
    gallery = json.loads((root / 'results/site-media-capture-verification-2026-10-08.json').read_text())
    assert sha((root / 'preview/UrbanHeat-AlKhor-Preview.html').read_bytes()) == gallery['preview_sha256']
    report = {
        'checked_at_utc': datetime.now(timezone.utc).isoformat(),
        'status': 'field_photo_presentation_checks_passed_native_powerpoint_and_member_acceptance_pending',
        'baseline_public_commit': '9fa71a86c9d44b4303c36eac9c1fc2f4b91e7596',
        'pdf_pages': 12, 'pptx_slides': 12, 'changed_slides': [6, 8, 11, 12],
        'photograph_checks': photo_checks,
        'pptx_existing_parts_changed': sorted(changed), 'pptx_original_parts_deleted': 0,
        'original_theme_fonts_unrelated_parts_media': 'byte-identical',
        'slide_8_table_values_style_geometry_xml': 'identical',
        'pdf_pptx_paragraph_table_cell_matches': text_checks,
        'pdf_text_span_boundary_checks': span_checks, 'pdf_pixel_checks': pixels,
        'visual_review': 'PDF slides 6/8/11/12 individually rendered and inspected at 1280 × 720 scale; clear subjects/case labels, no obvious clipping or overlap.',
        'desktop_powerpoint_opened': False,
        'pdf_method': 'Original pages retained with targeted PyMuPDF image/text replacement; existing Noto Sans PDF style. No native PowerPoint export/render claim.',
        'native_powerpoint_limits': 'Desktop PowerPoint and LibreOffice unavailable. Editable PPTX parsed/structure checked; actual presentation-machine font/render acceptance remains pending.',
        'capture_source': 'Nasser explicit confirmation, not EXIF; Abdulrahman Almohannadi photographer',
        'shared_capture_window': '8 October 2026, 13:00–14:00 Qatar (UTC+3); applies to all three photographs',
        'exact_individual_time': 'Unknown; no minute assigned per file',
        'protected_prior_public_files': len(protected), 'protected_files': protected,
        'original_input_hashes_verified': len(inputs), 'original_csv_hashes_verified': len(tables),
        'all_original_media_hashes_verified': len(receipt['items']),
        'script_timing': timing, 'browser_rerun': False,
        'browser_reason': 'App/standalone/media bytes unchanged; matching real Chromium evidence retained in results/site-media-capture-verification-2026-10-08.json.',
        'preview_sha256': gallery['preview_sha256'], 'analysis_rerun': False,
        'ranking_changed': False, 'raw_data_original_tables_backups_changed': False,
        'primary_dw_threshold': .60, 'primary_dw_coverage_percent': 30.938509530941777,
        'coverage_gate_percent': 50, 'primary_gate': 'failed',
        'Unknown_excluded_common_percent': 69.06149046905822,
        'independent_scientific_validation': 'pending',
        'project_member_reviews_and_rehearsal': 'pending until individually confirmed',
        'submission': 'not performed; no organizer contact',
        'files': {name: {'bytes': (root / name).stat().st_size,
                         'sha256': sha((root / name).read_bytes())}
                  for name in [pdf_name, ppt_name, 'docs/Three-Minute-Presentation.md',
                               'results/field-photo-slide-review/slide-6.png']},
    }
    (root / 'results/field-photo-slides-verification-2026-10-08.json').write_text(json.dumps(report, indent=2) + '\n')
    return {k: report[k] for k in ['status', 'pdf_pages', 'pptx_slides', 'changed_slides',
            'pdf_pptx_paragraph_table_cell_matches', 'protected_prior_public_files',
            'original_input_hashes_verified', 'original_csv_hashes_verified']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline', type=Path, required=True)
    parser.add_argument('--public-tree', type=Path, required=True)
    parser.add_argument('--script-timing', type=Path, required=True)
    args = parser.parse_args()
    print(json.dumps(verify(args.project.resolve(), args.baseline.resolve(),
                           args.public_tree.resolve(), args.script_timing.resolve()), indent=2))
