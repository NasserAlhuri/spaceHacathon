"""Render the existing 18 targets with supplied dated RGB; read-only references.

No target reselection, new model, reflectance analysis or class replacement.
2021 RGB is already display-stretched; 2026 bands use the same 0..3500 DN
display stretch. Source-georeferenced nearest sampling handles the 5 m offset
in the original 2026 grid. Enlargement adds no spatial detail.
"""
import json
from pathlib import Path

import numpy as np
import rasterio
from rasterio.warp import reproject, Resampling
from PIL import Image, ImageDraw

from validate_dynamic_world_rasters import GRID

ROOT = Path(__file__).resolve().parents[1]


def main():
    samples = json.loads((ROOT / 'results/dynamic-world-scientific-sample-selection.json').read_text())['samples']
    assert len(samples) == 18
    shape = (1057, 1108)
    images = {}
    qa = {}
    for date in ['20210901', '20210926']:
        path = ROOT / f'data/dynamic_world/reference/2026-10-08/AlKhor_Sentinel2_Reference_{date}.tif'
        with rasterio.open(path) as s:
            assert s.crs.to_epsg() == 32639 and s.transform == GRID
            assert (s.height, s.width) == shape
            assert s.descriptions == ('red', 'green', 'blue', 'qa60')
            a = s.read()
            assert s.nodata == 65535 and np.all(a[:3] <= 255)
            images[date] = a[:3].transpose(1, 2, 0).astype('uint8')
            qa[date] = a[3]
    for date in ['20260905', '20260915']:
        bands = []
        base = ROOT / f'data/sample_input/multidate/S2B_39RWJ_{date}_0_L2A'
        for name in ['red', 'green', 'blue']:
            dst = np.zeros(shape, dtype='float32')
            with rasterio.open(base / f'{name}.tif') as s:
                reproject(s.read(1), dst, src_transform=s.transform, src_crs=s.crs,
                          dst_transform=GRID, dst_crs='EPSG:32639', resampling=Resampling.nearest)
            bands.append(dst)
        images[date] = (np.clip(np.stack(bands, axis=-1) / 3500, 0, 1) * 255).astype('uint8')
    output = ROOT / 'results/dynamic-world-paired-context'
    output.mkdir(exist_ok=True)
    dates = list(images)
    support = []
    for sample in samples:
        r, c = sample['row'], sample['col']
        x, y = GRID * (c + .5, r + .5)
        assert (x, y) == (sample['easting'], sample['northing'])
        support.append({'sample_id': sample['sample_id'], 'qa60_20210901': int(qa['20210901'][r, c]),
                        'qa60_20210926': int(qa['20210926'][r, c]),
                        'qa60_cloud_or_cirrus_at_target': bool((qa['20210901'][r,c] | qa['20210926'][r,c]) & 3072),
                        'dated_context_count': 4})
    for page in range(6):
        canvas = Image.new('RGB', (1560, 1000), '#f7f8f8')
        draw = ImageDraw.Draw(canvas)
        draw.text((15, 10), 'Paired dated Sentinel contexts: fixed existing DW targets. Gold = exact exported 10 m target.', fill='black')
        draw.text((15, 32), '410 m context + 90 m detail enlarged with nearest sampling. Same-source visual diagnostic, not independent truth.', fill='black')
        for i, sample in enumerate(samples[page*3:page*3+3]):
            top = 75 + i * 295
            r, c = sample['row'], sample['col']
            draw.text((15, top), sample['sample_id'] + ': ' + sample['stratum'], fill='black')
            draw.text((15, top+22), f"0.50: {sample['sensitivity_label_2021']} -> {sample['sensitivity_label_2026']}", fill='black')
            draw.text((15, top+44), f"0.60: {sample['primary_label_2021']} -> {sample['primary_label_2026']}", fill='black')
            draw.text((15, top+66), f"Conf: {sample['confidence_2021']:.4f} / {sample['confidence_2026']:.4f}", fill='black')
            draw.text((15, top+88), f"{sample['latitude']:.7f}, {sample['longitude']:.7f}", fill='black')
            for j, date in enumerate(dates):
                left = 280 + j * 320
                draw.text((left, top), f'{date[:4]}-{date[4:6]}-{date[6:]} ' + ('L1C RGB/QA60' if date.startswith('2021') else 'L2A RGB'), fill='black')
                crop = images[date][r-20:r+21, c-20:c+21]
                assert crop.shape == (41, 41, 3)
                context = Image.fromarray(crop).resize((205, 205), Image.Resampling.NEAREST)
                d = ImageDraw.Draw(context)
                d.rectangle((100, 100, 104, 104), outline='#ffd500', width=1)
                canvas.paste(context, (left, top+25))
                detail = Image.fromarray(images[date][r-4:r+5,c-4:c+5]).resize((90,90),Image.Resampling.NEAREST)
                d = ImageDraw.Draw(detail)
                d.rectangle((40,40,49,49), outline='#ffd500', width=1)
                canvas.paste(detail, (left+214, top+25))
                draw.text((left+214, top+125), '90 m detail', fill='black')
                if date.startswith('2021'):
                    draw.text((left+214, top+147), f'QA60 {int(qa[date][r,c])}', fill='black')
                    draw.text((left+214, top+169), 'native 60 m', fill='black')
        draw.text((15,975),'Contains modified Copernicus Sentinel data (2021, 2026). Unknown/thresholds stay unchanged; do not infer citywide accuracy.',fill='black')
        canvas.save(output / f'page-{page+1}.png')
    report = {'status': 'paired_contexts_rendered_for_visual_inspection', 'sample_locations': 18,
              'context_count': 72, 'dates': dates, 'sample_target_checks': support,
              'source_grid_handling': '2021 exact DW grid; 2026 native 5 m offset georeferenced with nearest sampling',
              'display_only': True, 'baseline_analysis_rerun': False}
    (ROOT / 'results/dynamic-world-paired-render-verification.json').write_text(json.dumps(report,indent=2)+'\n')
    print('Rendered 72 dated contexts at the 18 unchanged targets. Visual review still required.')


if __name__ == '__main__':
    main()
