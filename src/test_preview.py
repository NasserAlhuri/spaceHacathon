"""Verify the single-file preview in real Chromium with networking disabled."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('preview', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    report = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'preview_sha256': hashlib.sha256(args.preview.read_bytes()).hexdigest(), 'offline': True, 'delivery': 'HTML content loaded through Playwright set_content; managed Chromium policy blocks file:// navigation', 'profiles': [], 'status': 'failed'}
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            report['browser'] = browser.version
            for name, viewport in [('desktop', {'width': 1440, 'height': 900}), ('mobile', {'width': 390, 'height': 844})]:
                record = {'name': name, 'viewport': viewport, 'page_errors': [], 'console_errors': [], 'network_requests': []}
                report['profiles'].append(record)
                context = browser.new_context(viewport=viewport, is_mobile=name == 'mobile', has_touch=name == 'mobile', offline=True, accept_downloads=True)
                page = context.new_page()
                page.on('pageerror', lambda e, r=record: r['page_errors'].append(str(e)))
                page.on('console', lambda m, r=record: r['console_errors'].append(m.text) if m.type == 'error' else None)
                page.on('request', lambda q, r=record: r['network_requests'].append(q.url) if q.url.startswith(('http:', 'https:')) else None)
                page.set_content(args.preview.read_text(), wait_until='load')
                page.wait_for_function("document.getElementById('cell-select').options.length === 1112")
                assert 'Loading' not in page.locator('#map-caption').inner_text()
                assert page.locator('header').evaluate('(e) => getComputedStyle(e).backgroundColor') == 'rgb(17, 38, 60)'
                assert page.locator('#map-frame').bounding_box()['height'] > 500
                images = page.evaluate("""async () => {const images=JSON.parse(document.getElementById('preview-images').textContent); return Promise.all(Object.entries(images).map(async ([name,src])=>{const image=new Image();image.src=src;await image.decode();return {name,width:image.naturalWidth,height:image.naturalHeight};}));}""")
                assert len(images) == 12 and all(i['width'] > 0 and i['height'] > 0 for i in images)
                record['decoded_images'] = images
                for date in ['2026-09-14', '2026-09-30']:
                    page.locator('#date').select_option(date)
                    for layer in ['temperature', 'greenery', 'buildings', 'priority', 'uncertainty']:
                        page.locator(f'[data-layer="{layer}"]').click()
                        assert page.locator('#layer-image').get_attribute('href').startswith('data:image/png;base64,')
                        assert page.locator(f'[data-layer="{layer}"]').get_attribute('aria-pressed') == 'true'
                for cid in ['V04-23', 'V28-17', 'V04-24']:
                    page.locator('#cell-select').select_option(cid)
                    assert page.locator('#cell-badge').inner_text() == cid
                    assert page.locator('.local-details h3').inner_text()
                page.locator('#comparison-toggle').click()
                assert page.locator('#comparison-body tr').count() == 3
                assert page.locator('#comparison').is_visible()
                page.locator('#comparison-toggle').click()
                with page.expect_download() as event:
                    page.locator('#download-review').click()
                downloaded = event.value
                assert downloaded.failure() is None
                downloaded.save_as(args.output / (name + '-review.csv'))
                with (args.output / (name + '-review.csv')).open(newline='') as f:
                    rows = list(csv.DictReader(f))
                assert len(rows) == 6
                record['csv_rows'] = len(rows)
                page.locator('#reset').click()
                initial = page.locator('#map').get_attribute('viewBox')
                page.locator('#zoom-in').click()
                assert page.locator('#map').get_attribute('viewBox') != initial
                page.locator('#reset').click()
                assert page.locator('#map').get_attribute('viewBox') == initial
                page.locator('[data-layer="priority"]').click()
                page.screenshot(path=str(args.output / (name + '.png')), full_page=True)
                assert not record['page_errors'] and not record['console_errors'] and not record['network_requests']
                record['status'] = 'passed'
                context.close()
            browser.close()
        report['status'] = 'passed'
    finally:
        (args.output / 'preview-check.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
