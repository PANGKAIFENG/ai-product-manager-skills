"""Optional Playwright smoke test; requires Python playwright and Chromium."""

import argparse
import base64
import importlib.util
import json
import tempfile
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('renderer', ROOT / 'scripts/render_report.py')
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as temporary, sync_playwright() as playwright:
        base = Path(temporary)
        data = json.loads((ROOT / 'tests/fixtures/case.json').read_text())
        data['messages'][0]['attachments'] = [{
            'id': 'A1', 'name': 'synthetic.png', 'status': 'available', 'path': 'synthetic.png',
        }]
        (base / 'synthetic.png').write_bytes(base64.b64decode(
            'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+jRZkAAAAASUVORK5CYII='))
        (base / 'case.json').write_text(json.dumps(data, ensure_ascii=False))
        report = renderer.build(base / 'case.json', base / 'report')
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={'width': 1024, 'height': 900}, reduced_motion='reduce')
        errors, external = [], []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.on('console', lambda item: errors.append(item.text) if item.type == 'error' else None)
        page.on('request', lambda request: external.append(request.url) if request.url.startswith(('http:', 'https:')) else None)
        page.goto(report.as_uri(), wait_until='networkidle')
        assert page.locator('.process[open],.analysis[open],.event[open],.raw[open]').count() == 0
        assert page.locator('#M1 .message-text').inner_text() == data['messages'][0]['text']
        assert page.locator('#M2 .message-text').inner_text() == data['messages'][1]['text']
        assert page.locator('.event').count() == 4
        page.screenshot(path=str(args.output_dir / '01-default.png'))
        page.locator('.attachment > summary').click()
        page.locator('.attachment img').wait_for(state='visible')
        assert page.locator('.attachment img').evaluate('image => image.complete && image.naturalWidth > 0')
        page.locator('.attachment > summary').click()
        page.locator('.process > summary').click()
        assert page.locator('.event[open]').count() == 0
        page.locator('#T2 > summary').click()
        fields = page.locator('#T2 .fields').inner_text()
        assert 'example-image-v1' in fields and 'not-submitted' in fields and 'false' in fields
        assert page.locator('#T2 .raw[open]').count() == 0
        page.locator('#T2 .raw > summary').click()
        raw = json.loads(page.locator('#T2 pre').inner_text())
        assert raw['input']['arguments']['arguments']['modelVersion'] == 'example-image-v1'
        page.locator('#T2 .raw > summary').click()
        page.goto(report.as_uri() + '#analysis', wait_until='networkidle')
        assert page.locator('#analysis').evaluate('element => element.open')
        assert page.locator('.flow a').count() == 4
        page.locator('#E3 a[data-locate]').click()
        page.wait_for_function("document.querySelector('#T2').open")
        assert page.locator('.process').evaluate('element => element.open')
        assert page.locator('#location-bar').is_visible()
        assert page.locator('#T2').evaluate("element => element.classList.contains('located')")
        page.locator('#location-return').click()
        assert page.locator('#location-bar').is_hidden()
        assert page.locator('#analysis').evaluate('element => element.open')
        for anchor in ['T2', 'E3', 'F2', 'S1']:
            page.goto(report.as_uri() + '#' + anchor, wait_until='networkidle')
            assert page.locator('#' + anchor).is_visible()
        widths = []
        for expanded in [False, True]:
            page.evaluate('(open) => document.querySelectorAll("details").forEach(item => item.open = open)', expanded)
            for width in [1440, 1024, 826, 390, 360]:
                page.set_viewport_size({'width': width, 'height': 900})
                excess = page.evaluate('document.documentElement.scrollWidth - innerWidth')
                assert excess <= 1, (expanded, width, excess)
                widths.append({'expanded': expanded, 'width': width, 'overflow': excess})
        page.set_viewport_size({'width': 1024, 'height': 900})
        page.goto(report.as_uri() + '#analysis', wait_until='networkidle')
        page.screenshot(path=str(args.output_dir / '02-analysis.png'))
        page.set_viewport_size({'width': 390, 'height': 844})
        page.goto(report.as_uri() + '#T2', wait_until='networkidle')
        page.screenshot(path=str(args.output_dir / '03-tool-mobile.png'))
        assert not external, external
        assert not errors, errors
        browser.close()
        result = {'result': 'PASS', 'widths': widths, 'browser_errors': errors, 'external_requests': external}
        (args.output_dir / 'result.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
        print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
