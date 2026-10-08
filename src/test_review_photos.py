"""Test review statuses and gallery integration using a non-evidence fixture."""
import argparse
import base64
import json
import shutil
import tempfile
from pathlib import Path
from playwright.sync_api import sync_playwright
from build_preview import build


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();args.output.mkdir(parents=True,exist_ok=True)
    root=Path(__file__).resolve().parents[1]
    checks=[]
    with tempfile.TemporaryDirectory(prefix='urbanheat-photo-fixture-') as temporary:
        app=Path(temporary)/'app';shutil.copytree(root/'app',app)
        review=json.loads((app/'local-review.json').read_text())
        received_photos=sum(len(c.get('photos',[])) for c in review['cells'])
        received_videos=sum(len(c.get('videos',[])) for c in review['cells'])
        assert received_photos==11 and received_videos==1
        for c in review['cells']:c['photos']=[];c['videos']=[]
        # A one-pixel test image is never inserted into the project or delivery ZIP.
        image=base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII=')
        photos=app/'assets/site-photos';photos.mkdir(exist_ok=True)
        (photos/'fixture.png').write_bytes(image)
        site=next(c for c in review['cells'] if c['cell_id']=='V18-26')
        site['photos']=[{'src':'assets/site-photos/fixture.png','observer':'TEST FIXTURE ONLY',
            'captured_at':None,'location':None,'caption':'<img onerror=alert(1)> TEST ONLY'}]
        (app/'local-review.json').write_text(json.dumps(review))
        standalone=Path(temporary)/'fixture.html';metadata=build(app,standalone)
        assert metadata['embedded_images']==13
        checks.append('Builder embeds a temporary fixture photo; original 11 photos and one video remain untouched')
        with sync_playwright() as p:
            browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
            for name,viewport in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844})]:
                context=browser.new_context(viewport=viewport,offline=True,is_mobile=name=='mobile',has_touch=name=='mobile')
                page=context.new_page();errors=[];requests=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
                page.set_content(standalone.read_text(),wait_until='load')
                page.wait_for_function("document.getElementById('cell-select').options.length===1112")
                page.locator('#cell-select').select_option('V18-26')
                photo=page.locator('.photo-gallery img')
                assert photo.count()==1 and photo.get_attribute('src').startswith('data:image/png;base64,')
                photo.scroll_into_view_if_needed()
                photo.evaluate('(e)=>{e.loading="eager";}')
                page.wait_for_function("document.querySelector('.photo-gallery img').naturalWidth===1",timeout=8000)
                photo.evaluate('(e)=>e.decode()')
                caption=page.locator('figcaption').inner_text()
                assert '<img onerror=alert(1)>' in caption and 'Capture: Unknown' in caption and 'Location: Unknown' in caption
                assert page.locator('figcaption img').count()==0
                assert 'Nasser confirms Abdulrahman Almohannadi visited' in page.locator('.evidence-status').inner_text()
                assert 'Metadata source: Unknown' in caption  # Fixture does not inherit real capture metadata.
                for cid in ['V04-24','V24-07']:
                    page.locator('#cell-select').select_option(cid)
                    assert page.locator('.photo-gallery img').count()==0
                    assert 'Evidence pending' in page.locator('.photo-gallery').inner_text()
                assert 'V04-24' in page.locator('#priority-list').inner_text()
                assert page.locator('#priority-list button').count()==3
                assert page.locator('#case-study-list button').count()==5
                assert 'primary coverage gate failed' in page.locator('.historical').inner_text()
                assert not errors and not requests
                checks.append(name+': embedded photo decodes offline; metadata unknowns, escaped captions, pending galleries, original top three and failed historical coverage gate verified')
                context.close()
            browser.close()
        site['photos'][0]['src']='../../outside.png'
        (app/'local-review.json').write_text(json.dumps(review))
        try:build(app,standalone)
        except ValueError:checks.append('Unsafe photo traversal path rejected')
        else:raise AssertionError('Unsafe photo path accepted')
    report={'status':'passed','method':'Real offline Chromium; temporary synthetic fixture only',
        'real_photographs_received':received_photos,'real_videos_received':received_videos,'fixture_in_deliverables':False,'checks':checks,
        'member_acceptance':'pending','physical_device_check':False}
    (args.output/'photo-review-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
