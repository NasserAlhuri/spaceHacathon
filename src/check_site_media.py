"""Shared real-browser checks of received site evidence; never run analysis."""
import hashlib
from pathlib import Path


def check_site_media(page, reviews, output=None):
    checked = []
    for review in reviews:
        cid = review['cell_id']
        page.locator('#cell-select').select_option(cid)
        gallery = page.locator('.photo-gallery')
        photos = review.get('photos', [])
        videos = review.get('videos', [])
        assert gallery.locator('img').count() == len(photos), cid
        assert gallery.locator('video').count() == len(videos), cid
        assert gallery.locator('figure').count() == len(photos) + len(videos), cid
        if not photos and not videos:
            assert 'Evidence pending' in gallery.inner_text()
        dimensions = []
        for index, item in enumerate(photos + videos):
            figure = gallery.locator('figure').nth(index)
            caption = figure.locator('figcaption').inner_text()
            assert item['original_filename'] in caption
            assert 'Capture: Unknown' in caption and 'Photographer: Unknown' in caption
            assert 'Location: Unknown' in caption and 'Viewing direction: Unknown' in caption
            assert item['site_association'] == cid
            if index < len(photos):
                image = figure.locator('img')
                dimensions.append(image.evaluate('''async e => {
                    e.loading='eager'; await e.decode();
                    if (!e.naturalWidth || !e.naturalHeight) throw new Error('Undecoded photo');
                    return {width:e.naturalWidth,height:e.naturalHeight};
                }'''))
                assert figure.locator('a').get_attribute('download') == item['original_filename']
            else:
                video = figure.locator('video')
                assert video.get_attribute('controls') is not None
                assert video.get_attribute('playsinline') is not None
                playback = video.evaluate('''async v => {
                    const timeout = new Promise((_, reject) => setTimeout(() => reject(new Error('Video playback timed out')), 15000));
                    const played = new Promise(async (resolve, reject) => {
                        v.onerror = () => reject(new Error('Video decode failed: '+v.error?.code));
                        v.onended = () => resolve({duration:v.duration, end:v.currentTime, width:v.videoWidth, height:v.videoHeight, ended:v.ended});
                        v.muted=true;
                        try { await v.play(); } catch(e) { reject(e); }
                    });
                    return await Promise.race([played,timeout]);
                }''')
                assert 6 < playback['duration'] < 6.1 and playback['ended']
                assert playback['width'] == 576 and playback['height'] == 1024, playback
                dimensions.append(playback)
                assert figure.locator('a').get_attribute('download') == item['original_filename']
            media = figure.locator('img,video')
            box = media.bounding_box()
            assert box and box['width'] > 0 and box['width'] <= page.evaluate('innerWidth'), cid
            assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), cid
            with page.expect_download() as event:
                figure.locator('a').click()
            downloaded = event.value
            assert downloaded.failure() is None
            assert downloaded.suggested_filename == item['original_filename']
            assert hashlib.sha256(Path(downloaded.path()).read_bytes()).hexdigest() == item['sha256']
        evidence = page.locator('.evidence-status').inner_text()
        assert ('Nasser confirms site visits' in evidence) == bool(review.get('site_confirmation'))
        assert 'have not been measured' in evidence
        if output and photos:
            gallery.locator('figure').first.screenshot(path=str(output / (cid + '-first-photo.png')))
        if output and videos:
            gallery.locator('video').screenshot(path=str(output / (cid + '-video.png')))
        checked.append({'cell_id': cid, 'photographs': len(photos), 'videos': len(videos),
                        'capture_date_time': 'Unknown', 'decoded_media': dimensions,
                        'original_media_download_hashes': 'all matched received bytes'})
    assert sum(r['photographs'] for r in checked) == 11
    assert sum(r['videos'] for r in checked) == 1
    return checked
