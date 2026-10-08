"""Embed three original field photographs in an existing twelve-slide deck.

Presentation preparation only: no image retouching, analytical computation or
native PowerPoint PDF export. Supply an external, preserved baseline directory
containing docs/UrbanHeat-AlKhor-Pitch.{pptx,pdf} from commit 9fa71a86.
Requires python-pptx, PyMuPDF and lxml in the presentation environment.
"""
import argparse
import io
import zipfile
from pathlib import Path

import fitz
from lxml import etree
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

PHOTOS = [
    ('V04-23-01.jpeg', 'V04-23 | Bus-stop road', 'Trees and stop sign; no shelter visible.'),
    ('V28-17-04.jpeg', 'V28-17 | Stadium parking', 'Stadium and parking; use unmeasured.'),
    ('V18-26-02.jpeg', 'V18-26 | Jogging route', 'Marked path beside road and sandy ground.'),
]
DATE = '8 October 2026 | 13:00–14:00 Qatar (UTC+3) | Shared capture window'
SOURCE = ('Photographer: Abdulrahman Almohannadi | Confirmed by Nasser, not EXIF | '
          'Exact per-file time: Unknown')
CHANGES = {
    (8, 2): 'Bus stop: waiting-area shade. Stadium: event use. Jogging route: reported lack of path shade. Photos received; use and detailed shade unmeasured.',
    (11, 2): 'Abdulrahman Almohannadi: supplied 11 photos + one video; project review remains pending.',
    (11, 6): 'Photographed-site visits and supplied media collection confirmed by Nasser. Detailed assessment, member reviews and rehearsals remain pending.',
    (12, 4): 'Field photos: Abdulrahman Almohannadi, 8 October 2026, shared 13:00–14:00 Qatar (UTC+3) window. Confirmed by Nasser, not EXIF; exact per-file times Unknown.',
}
BODY = (33 / 255, 56 / 255, 70 / 255)
TITLE = (22 / 255, 61 / 255, 70 / 255)
FOOTER = (82 / 255, 101 / 255, 105 / 255)
BACKGROUND = (247 / 255, 246 / 255, 241 / 255)
REGULAR = Path('/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf')
BOLD = Path('/usr/share/fonts/truetype/noto/NotoSans-Bold.ttf')


def normalized(text):
    return ' '.join(text.split())


def wrapped(text, font, size, width):
    lines = []
    line = ''
    for word in text.split():
        assert font.text_length(word, fontsize=size) <= width
        candidate = (line + ' ' + word).strip()
        if line and font.text_length(candidate, fontsize=size) > width:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def replace_text(shape, text, size=None):
    # Keep the original paragraph/font/margins/shape rather than resetting it.
    para = shape.text_frame.paragraphs[0]
    run = para.runs[0] if para.runs else para.add_run()
    run.text = text
    for extra in list(para.runs)[1:]:
        extra._r.getparent().remove(extra._r)
    for extra in list(shape.text_frame.paragraphs)[1:]:
        extra._p.getparent().remove(extra._p)
    if size is not None:
        run.font.name = 'Bitstream Charter'
        run.font.size = Pt(size)
        run.font.color.rgb = RGBColor(33, 56, 70)


def text_box(slide, text, rect, size, bold=False, color=(33, 56, 70)):
    x, y, w, h = rect
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.margin_left = frame.margin_right = 0
    frame.margin_top = frame.margin_bottom = 0
    frame.vertical_anchor = MSO_ANCHOR.TOP
    frame.word_wrap = True
    para = frame.paragraphs[0]
    para.alignment = PP_ALIGN.LEFT
    para.space_after = Pt(0)
    para.line_spacing = 1.2
    run = para.add_run()
    run.text = text
    run.font.name = 'Bitstream Charter'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = RGBColor(*color)
    return box


def picture_rect(index, width, height):
    x = .667 + index * 4.1
    scale = min(3.8 / width, 3.5 / height)
    w, h = width * scale, height * scale
    return x + (3.8 - w) / 2, 1.85 + (3.5 - h) / 2, w, h


def draw_text(page, text, rect, size, bold=False, color=BODY):
    x, y, w, h = [v * 72 for v in rect]
    font_path = BOLD if bold else REGULAR
    font = fitz.Font(fontfile=str(font_path))
    lines = wrapped(text, font, size, w)
    baseline = y + font.ascender * size
    assert (baseline - font.descender * size + (len(lines) - 1) * size * 1.2) <= y + h + 1
    for i, line in enumerate(lines):
        page.insert_text((x, baseline + i * size * 1.2), line,
                         fontsize=size, fontname='field-bold' if bold else 'field-regular',
                         fontfile=str(font_path), color=color)


def revise(root, baseline):
    ppt_name = 'docs/UrbanHeat-AlKhor-Pitch.pptx'
    pdf_name = 'docs/UrbanHeat-AlKhor-Pitch.pdf'
    deck = Presentation(baseline / ppt_name)
    assert len(deck.slides) == 12
    slide = deck.slides[5]
    old_picture = [s for s in slide.shapes if s.shape_type == 13]
    assert len(old_picture) == 1, 'Use the unmodified external baseline.'
    old_picture[0]._element.getparent().remove(old_picture[0]._element)
    for index, (filename, heading, caption) in enumerate(PHOTOS):
        data = (root / 'app/assets/site-photos' / filename).read_bytes()
        image = fitz.Pixmap(data)
        rect = picture_rect(index, image.width, image.height)
        x, y, w, h = rect
        picture = slide.shapes.add_picture(io.BytesIO(data), Inches(x), Inches(y),
                                           width=Inches(w), height=Inches(h))
        picture.name = filename
        picture._element.nvPicPr.cNvPr.set('descr', f'{heading}; {filename}; {DATE}; {SOURCE}')
        text_box(slide, heading, (.667 + index * 4.1, 1.48, 3.8, .35), 18, bold=True, color=(22, 61, 70))
        text_box(slide, caption, (.667 + index * 4.1, 5.42, 3.8, .49), 12.5)
    text_box(slide, DATE, (.667, 6.03, 12, .29), 15.2, color=(22, 61, 70))
    text_box(slide, SOURCE, (.667, 6.36, 12, .24), 11.5, color=(82, 101, 105))
    for (number, index), text in CHANGES.items():
        replace_text(deck.slides[number - 1].shapes[index], text, 18.5 if number == 12 else None)
    stream = io.BytesIO()
    deck.save(stream)
    # Splice only changed slides/relationships and new JPEG parts into the
    # baseline archive. Every unrelated original part remains byte-identical.
    allowed = {'ppt/slides/slide6.xml', 'ppt/slides/_rels/slide6.xml.rels',
               'ppt/slides/slide8.xml', 'ppt/slides/slide11.xml', 'ppt/slides/slide12.xml'}
    with zipfile.ZipFile(baseline / ppt_name) as old, zipfile.ZipFile(stream) as candidate:
        original = {n: old.read(n) for n in old.namelist()}
        new_media = set(candidate.namelist()) - set(original)
        assert len(new_media) == 3 and all(n.startswith('ppt/media/') and n.endswith('.jpg') for n in new_media)
        for name in allowed | new_media:
            original[name] = candidate.read(name)
        content_types = etree.fromstring(original['[Content_Types].xml'])
        ns = 'http://schemas.openxmlformats.org/package/2006/content-types'
        assert not any(e.get('Extension') == 'jpg' for e in content_types)
        etree.SubElement(content_types, '{' + ns + '}Default', Extension='jpg', ContentType='image/jpeg')
        original['[Content_Types].xml'] = etree.tostring(content_types, xml_declaration=True, encoding='UTF-8', standalone=True)
        with zipfile.ZipFile(root / ppt_name, 'w', zipfile.ZIP_DEFLATED) as out:
            for name, data in original.items():
                out.writestr(name, data)

    original_deck = Presentation(baseline / ppt_name)
    with fitz.open(baseline / pdf_name) as pdf:
        # Remove the old illustrative figure only. Title and original footer stay.
        page = pdf[5]
        page.add_redact_annot(fitz.Rect(48, 102, 913, 475), fill=BACKGROUND)
        page.apply_redactions(images=2, graphics=0)
        for index, (filename, heading, caption) in enumerate(PHOTOS):
            data = (root / 'app/assets/site-photos' / filename).read_bytes()
            image = fitz.Pixmap(data)
            x, y, w, h = picture_rect(index, image.width, image.height)
            page.insert_image(fitz.Rect(x * 72, y * 72, (x + w) * 72, (y + h) * 72), stream=data)
            draw_text(page, heading, (.667 + index * 4.1, 1.48, 3.8, .35), 18, True, TITLE)
            draw_text(page, caption, (.667 + index * 4.1, 5.42, 3.8, .49), 12.5)
        draw_text(page, DATE, (.667, 6.03, 12, .29), 15.2, color=TITLE)
        draw_text(page, SOURCE, (.667, 6.36, 12, .24), 11.5, color=FOOTER)
        for (number, index), text in CHANGES.items():
            page = pdf[number - 1]
            if number == 12:
                draw_text(page, text, (.7646, 5.31, 11.8, .78), 18.5)
                continue
            old_text = original_deck.slides[number - 1].shapes[index].text
            blocks = page.get_text('dict', flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']
            found = [b for b in blocks if normalized(''.join(s['text'] for line in b.get('lines', []) for s in line['spans'])) == normalized(old_text)]
            assert len(found) == 1, (number, old_text)
            block = found[0]
            spans = [s for line in block['lines'] for s in line['spans']]
            first = spans[0]
            size = first['size']
            x, y = first['origin']
            leading = block['lines'][1]['spans'][0]['origin'][1] - y if len(block['lines']) > 1 else size * 1.2
            font = fitz.Font(fontfile=str(REGULAR))
            lines = wrapped(text, font, size, 849.6)
            assert len(lines) <= len(block['lines']), (number, len(lines), len(block['lines']))
            bbox = fitz.Rect(block['bbox']) + (-1, -1, 1, 1)
            page.add_redact_annot(bbox, fill=BACKGROUND)
            page.apply_redactions(images=0, graphics=0)
            color = tuple(((first['color'] >> shift) & 255) / 255 for shift in (16, 8, 0))
            for line_index, line in enumerate(lines):
                page.insert_text((x, y + line_index * leading), line, fontsize=size,
                                 fontname='field-regular', fontfile=str(REGULAR), color=color)
        pdf.save(root / pdf_name, garbage=4, deflate=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--project', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--baseline', type=Path, required=True)
    args = parser.parse_args()
    revise(args.project.resolve(), args.baseline.resolve())
