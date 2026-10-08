"""Exercise the existing portable map in real Chromium; never regenerate analysis."""
import argparse
import csv
import functools
import hashlib
import http.server
import json
import threading
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright
from check_site_media import check_site_media


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--app', type=Path, default=Path(__file__).resolve().parents[1] / 'app')
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--chromium', default='/usr/bin/chromium')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    data = json.loads((args.app / 'assets/data.json').read_text())
    reviews = json.loads((args.app / 'local-review.json').read_text())['cells']
    cells = {c['id']: c for c in data['cells']}

    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *unused):
            pass

    server = http.server.ThreadingHTTPServer(('127.0.0.1', 0), functools.partial(Handler, directory=str(args.app)))
    threading.Thread(target=server.serve_forever, daemon=True).start()
    result = {'checked_at_utc': datetime.now(timezone.utc).isoformat(), 'method': 'Real headless Chromium via Playwright, local HTTP server, actual clicks/taps and download', 'profiles': []}
    try:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=args.chromium, headless=True, args=['--no-sandbox', '--disable-dev-shm-usage'])
            result['browser'] = {'engine': 'Chromium', 'version': browser.version}
            for name, viewport in [('desktop', {'width': 1440, 'height': 900}), ('mobile', {'width': 390, 'height': 844})]:
                profile = {'name': name, 'viewport': viewport, 'touch_emulation': name == 'mobile', 'checks': [], 'page_errors': [], 'console_errors': [], 'failed_requests': [], 'media_request_cancellations': [], 'http_errors': []}
                result['profiles'].append(profile)
                context = browser.new_context(viewport=viewport, is_mobile=name == 'mobile', has_touch=name == 'mobile', device_scale_factor=1, accept_downloads=True)
                page = context.new_page()
                page.on('pageerror', lambda e, r=profile: r['page_errors'].append(str(e)))
                page.on('console', lambda m, r=profile: r['console_errors'].append(m.text) if m.type == 'error' else None)
                # Chromium cancels metadata preload when selecting another cell removes a video.
                # Keep these visible separately; actual video decoding/playback must still pass.
                def request_failed(request, record=profile):
                    cancelled = request.failure == 'net::ERR_ABORTED' and request.url.endswith('/V18-26-03.mp4')
                    record['media_request_cancellations' if cancelled else 'failed_requests'].append(
                        {'url': request.url, 'failure': request.failure})
                page.on('requestfailed', request_failed)
                page.on('response', lambda q, r=profile: r['http_errors'].append({'url': q.url, 'status': q.status}) if q.status >= 400 else None)
                page.set_default_timeout(8000)

                def check(label, action):
                    try:
                        detail = action()
                        profile['checks'].append({'name': label, 'status': 'passed', 'detail': detail})
                    except Exception as e:
                        profile['checks'].append({'name': label, 'status': 'failed', 'error': str(e)})

                def require(condition, message):
                    if not condition:
                        raise AssertionError(message)

                def click(selector):
                    locator = page.locator(selector)
                    locator.tap() if name == 'mobile' else locator.click()

                def view():
                    return [float(v) for v in page.locator('#map').get_attribute('viewBox').split()]

                def loaded_image():
                    page.wait_for_function("async () => {const i = new Image(); i.src = document.getElementById('layer-image').getAttribute('href'); try {await i.decode(); return i.naturalWidth > 0;} catch {return false;}}")

                page.goto(f'http://127.0.0.1:{server.server_port}/', wait_until='networkidle')
                page.wait_for_function("document.getElementById('cell-select').options.length === 1112")
                loaded_image()
                page.screenshot(path=str(args.output / f'{name}-initial.png'), full_page=True)

                def historical_experiment():
                    text = page.locator('.historical').inner_text()
                    require('Exports succeeded' in text and 'primary coverage gate failed' in text,
                        'Execution success and scientific gate failure must stay distinct')
                    require('69.06%' in text and 'Unknown' in text and 'scientific review is pending' in text,
                        'Unknown or pending scientific review disappeared')
                    path = args.app.parent / 'data/dynamic_world/raw/2026-10-07/AlKhor_DW_matched_changes.csv'
                    with path.open(newline='') as handle:
                        rows = list(csv.DictReader(handle))
                    for i,threshold in enumerate([.5,.6,.7]):
                        row = next(r for r in rows if float(r['confidence_threshold']) == threshold)
                        actual = page.locator('.historical tbody tr').nth(i).inner_text()
                        require(f"{float(row['common_support_m2'])/1e6:.4f} km²" in actual,
                            'Coverage display differs from immutable EE CSV area convention')
                        require(f"{float(row['common_window_fraction'])*100:.2f}%" in actual,
                            'Coverage percentage differs from actual exports')
                    return {'source':'immutable actual CSV', 'primary_gate':'failed', 'scientific_review':'pending'}
                check('historical experiment matches actual CSV and retains failed gate/Unknown', historical_experiment)
                check('all received site photographs decode, video plays to end, metadata remains Unknown',
                      lambda: check_site_media(page, reviews, args.output))

                for date in data['dates']:
                    for layer in ['temperature', 'greenery', 'buildings', 'priority', 'uncertainty']:
                        def layer_check(date=date, layer=layer):
                            page.locator('#date').select_option(date)
                            click(f'[data-layer="{layer}"]')
                            loaded_image()
                            href = page.locator('#layer-image').get_attribute('href')
                            require(href == f'assets/{layer}-{date}.png', 'Wrong date/layer image')
                            require(page.locator('[data-layer][aria-pressed="true"]').count() == 1, 'Active layer state is ambiguous')
                            require(page.locator(f'[data-layer="{layer}"]').get_attribute('aria-pressed') == 'true', 'Wrong active layer')
                            return {'date': date, 'layer': layer, 'image_decoded': True, 'legend': page.locator('#legend-title').inner_text()}
                        check(f'date and layer: {date} / {layer}', layer_check)

                    for review in reviews:
                        cid = review['cell_id']
                        def selection_check(cid=cid, review=review, date=date):
                            page.locator('#cell-select').select_option(cid)
                            require(page.locator('#cell-badge').inner_text() == cid, 'Wrong selected cell')
                            require(page.locator('#selection polygon').count() == 1, 'Missing map selection outline')
                            values = cells[cid]['values'][date]
                            green = f"{values['greenery']:.4f}%" if 0 < values['greenery'] < 0.1 else f"{values['greenery']:.1f}%"
                            expected = [f"{values['temperature']:.1f}°C", green, f"{values['uncertainty']:.2f} K"]
                            actual = page.locator('#cell-details .metrics strong').all_inner_texts()
                            require(actual == expected, f'Metrics mismatch: {actual} / {expected}')
                            require(page.locator('.local-details h3').inner_text() == review['name'], 'Wrong local review')
                            return {'cell': cid, 'date': date, 'metrics': actual}
                        check(f'select reviewed cell: {date} / {cid}', selection_check)

                def shortlist():
                    for index, review in enumerate(reviews[:3]):
                        click(f'#priority-list button:nth-child({index + 1})')
                        require(page.locator('#cell-badge').inner_text() == review['cell_id'], 'Shortlist selected the wrong site')
                    return {'selected_cells': [r['cell_id'] for r in reviews[:3]]}
                check('three shortlist buttons', shortlist)

                def comparison():
                    click('#comparison-toggle')
                    require(page.locator('#comparison').is_visible(), 'Comparison not visible')
                    require(page.locator('#comparison-toggle').get_attribute('aria-expanded') == 'true', 'Expanded state missing')
                    for date in data['dates']:
                        page.locator('#date').select_option(date)
                        rows = page.locator('#comparison-body tr')
                        require(rows.count() == len(reviews), 'Wrong comparison row count')
                        for index, review in enumerate(reviews):
                            values = rows.nth(index).locator('td').all_inner_texts()
                            require(values[1] == review['cell_id'], 'Wrong comparison cell')
                            require(values[2] == f"{cells[review['cell_id']]['values'][date]['temperature']:.1f} °C", 'Comparison temperature did not update')
                        require(date in page.locator('#comparison-date').inner_text(), 'Comparison date is stale')
                    page.locator('#comparison').scroll_into_view_if_needed()
                    page.screenshot(path=str(args.output / f'{name}-comparison.png'))
                    scroller = page.locator('#comparison .table-scroll')
                    scroller.evaluate('(e) => e.scrollLeft = e.scrollWidth')
                    scroll = scroller.evaluate('(e) => ({width:e.scrollWidth, viewport:e.clientWidth, left:e.scrollLeft})')
                    require(scroll['width'] <= scroll['viewport'] or scroll['left'] > 0, 'Hidden comparison columns cannot be reached')
                    page.screenshot(path=str(args.output / f'{name}-comparison-right.png'))
                    scroller.evaluate('(e) => e.scrollLeft = 0')
                    click('#comparison-toggle')
                    require(page.locator('#comparison').is_hidden(), 'Comparison did not close')
                    return {'rows': len(reviews), 'dates_checked': data['dates'], 'mobile_table_uses_horizontal_scroll': name == 'mobile'}
                check('comparison opens, follows date, scrolls and closes', comparison)

                def download():
                    with page.expect_download() as event:
                        click('#download-review')
                    downloaded = event.value
                    require(downloaded.failure() is None, 'Download failed')
                    require(downloaded.suggested_filename == 'AlKhor-Location-Review.csv', 'Wrong CSV filename')
                    path = args.output / f'{name}-download.csv'
                    downloaded.save_as(path)
                    rows = list(csv.DictReader(path.open(newline='')))
                    require(len(rows) == len(reviews)*len(data['dates']), 'CSV should contain all reviews across both dates')
                    for row in rows:
                        cell = cells[row['cell_id']]
                        require(float(row['surface_temperature_c']) == cell['values'][row['thermal_date']]['temperature'], 'CSV numerical value mismatch')
                        require(row['optical_date'] == ('2026-09-15' if row['thermal_date'] == '2026-09-14' else '2026-09-30'), 'Wrong optical date')
                        photographed = row['cell_id'] in ['V04-23', 'V28-17', 'V18-26']
                        require(row['media_exact_per_file_time'] == 'Unknown', 'An exact media time was invented')
                        require('Pending' in row['project_review_status'], 'Photo collection completed the project review')
                        if photographed:
                            require(row['media_photographer'] == 'Abdulrahman Almohannadi', 'Photographer confirmation missing')
                            require('13:00–14:00 Qatar (UTC+3)' in row['media_capture_window'], 'Shared capture window missing')
                            require(row['media_metadata_source'] == 'Nasser Alhuri user confirmation; not EXIF', 'Confirmation misattributed to EXIF')
                            require(row['media_collection_status'].startswith('Complete for supplied media batch'), 'Batch completion not recorded')
                        else:
                            require(row['media_photographer'] == row['media_capture_window'] == 'Unknown', 'Unreceived site evidence was invented')
                    require({r['cell_id'] for r in rows} == {r['cell_id'] for r in reviews}, 'CSV locations mismatch')
                    return {'filename': downloaded.suggested_filename, 'rows': len(rows), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
                check('actual CSV download and content', download)

                def zoom():
                    click('#reset')
                    initial = view()
                    click('#zoom-in')
                    require(view()[2] < initial[2], 'Zoom in did not reduce extent')
                    click('#zoom-out')
                    require(abs(view()[2] - initial[2]) < 0.001, 'Zoom out did not restore extent')
                    page.locator('#cell-select').select_option('V04-23')
                    click('#focus-selection')
                    require(abs(view()[2] - data['width'] / 5) < 0.001, 'Focus did not zoom to selected cell')
                    page.locator('#map').scroll_into_view_if_needed()
                    label_bounds = page.locator('#map').evaluate("""e => {const box=e.getBoundingClientRect(), scale=e.getScreenCTM().a; return [...document.querySelectorAll('#map-labels text')].filter(x=>getComputedStyle(x).display !== 'none').map(x=>{const r=x.getBoundingClientRect(); return {text:x.textContent, font:parseFloat(getComputedStyle(x).fontSize)*scale, inside:r.left>=box.left && r.right<=box.right && r.top>=box.top && r.bottom<=box.bottom};});}""")
                    require(label_bounds and all(11 <= x['font'] <= 15 and x['inside'] for x in label_bounds), 'Zoomed labels are oversized or clipped')
                    page.screenshot(path=str(args.output / f'{name}-focused.png'))
                    click('#reset')
                    require(view() == [0, 0, data['width'], data['height']], 'Reset did not restore original view')
                    return {'initial_view_box': initial, 'selection_focus_width': data['width'] / 5, 'zoomed_label_bounds': label_bounds}
                check('zoom in, zoom out, selected-site focus and reset', zoom)

                def map_selection():
                    selected = []
                    for review in reviews:
                        cid = review['cell_id']
                        page.locator('#cell-select').select_option(cid)
                        click('#focus-selection')
                        page.locator('#map').scroll_into_view_if_needed()
                        points = cells[cid]['points']
                        x0, x1 = min(q[0] for q in points), max(q[0] for q in points)
                        y0, y1 = min(q[1] for q in points), max(q[1] for q in points)
                        retained = [(x + 15, y + 15) for y in range(int(y0), int(y1), 30) for x in range(int(x0), int(x1), 30) if data['mask'][(y // 30) * data['rasterShape'][1] + x // 30]]
                        point = min(retained, key=lambda q: (q[0] - (x0 + x1) / 2) ** 2 + (q[1] - (y0 + y1) / 2) ** 2)
                        # Clear the selector first so the actual map input must restore it.
                        page.locator('#cell-select').select_option('')
                        page.locator('#map').scroll_into_view_if_needed()
                        screen = page.locator('#map').evaluate('(e, p) => {const q = new DOMPoint(...p).matrixTransform(e.getScreenCTM()); return {x:q.x,y:q.y};}', point)
                        page.touchscreen.tap(screen['x'], screen['y']) if name == 'mobile' else page.mouse.click(screen['x'], screen['y'])
                        require(page.locator('#cell-badge').inner_text() == cid, f'Actual map input did not select {cid}')
                        selected.append(cid)
                    click('#reset')
                    return {'selected_via_real_pointer': selected}
                check('actual map clicks or touch taps on all three sites', map_selection)

                def pan():
                    click('#zoom-in')
                    page.locator('#map').scroll_into_view_if_needed()
                    before = view()
                    box = page.locator('#map').bounding_box()
                    x, y = box['x'] + box['width'] / 2, box['y'] + box['height'] / 2
                    if name == 'mobile':
                        session = context.new_cdp_session(page)
                        for kind, dx in [('touchStart', 0), ('touchMove', 30), ('touchMove', 60), ('touchEnd', 60)]:
                            session.send('Input.dispatchTouchEvent', {'type': kind, 'touchPoints': [] if kind == 'touchEnd' else [{'x': x + dx, 'y': y, 'id': 1}]})
                    else:
                        page.mouse.move(x, y)
                        page.mouse.down()
                        page.mouse.move(x + 60, y, steps=5)
                        page.mouse.up()
                    require(view()[0] != before[0], 'Pan did not change map position')
                    click('#reset')
                    return {'method': 'emulated touch drag' if name == 'mobile' else 'mouse drag'}
                check('map pan', pan)

                def opacity():
                    slider = page.locator('#opacity')
                    slider.press('Home')
                    require(page.locator('#layer-image').evaluate('(e) => e.style.opacity') == '0', 'Opacity did not reach zero')
                    slider.press('End')
                    require(page.locator('#opacity-value').inner_text() == '100%', 'Opacity output is stale')
                    return {'range': '0% to 100%'}
                check('layer opacity', opacity)

                def layout():
                    measurements = []
                    for width in ([1440, 1024] if name == 'desktop' else [390, 320]):
                        page.set_viewport_size({'width': width, 'height': viewport['height']})
                        page.locator('#cell-select').select_option('V04-23')
                        m = page.evaluate("""() => {const map=document.getElementById('map'), scale=map.getScreenCTM().a; return {viewport:innerWidth, page:document.documentElement.scrollWidth, labels:[...document.querySelectorAll('#map-labels text')].map(e=>({text:e.textContent,screen_font_px:parseFloat(getComputedStyle(e).fontSize)*scale})), metrics:[...document.querySelectorAll('.metric')].map(e=>({text:e.innerText,overflow:e.scrollWidth-e.clientWidth}))};}""")
                        measurements.append(m)
                        require(m['page'] <= m['viewport'], 'Page has horizontal overflow')
                        require(all(x['overflow'] <= 1 for x in m['metrics']), 'Selected-cell metrics overflow their card')
                        require(all(x['screen_font_px'] >= 11 for x in m['labels']), 'Map labels are too small to read at the initial extent')
                    page.set_viewport_size(viewport)
                    return measurements
                check('layout and readable map labels at normal and narrow widths', layout)
                page.set_viewport_size(viewport)
                page.locator('#cell-select').select_option('V04-23')
                page.screenshot(path=str(args.output / f'{name}-final.png'), full_page=True)
                profile['status'] = 'passed' if all(c['status'] == 'passed' for c in profile['checks']) and not any(profile[k] for k in ['page_errors', 'console_errors', 'failed_requests', 'http_errors']) else 'failed'
                context.close()
            browser.close()
    finally:
        server.shutdown()
        result['status'] = 'passed' if len(result['profiles']) == 2 and all(p.get('status') == 'passed' for p in result['profiles']) else 'failed'
        (args.output / 'browser-check.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'browser': result.get('browser'), 'profiles': [{'name': p['name'], 'passed': sum(c['status'] == 'passed' for c in p['checks']), 'failures': [c for c in p['checks'] if c['status'] != 'passed'], 'page_errors': p['page_errors'], 'console_errors': p['console_errors']} for p in result['profiles']]}, indent=2))
    return 0 if result['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
