import base64
import copy
import hashlib
import importlib.util
import json
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('render_report', ROOT / 'scripts/render_report.py')
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)
FIXTURE = ROOT / 'tests/fixtures/case.json'


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids = []
        self.links = []
        self.details = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag == 'a' and 'href' in attrs:
            self.links.append(attrs['href'])
        if tag == 'details':
            self.details.append(attrs)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(FIXTURE.read_text())

    def validate(self):
        renderer.validate(self.data, FIXTURE.parent)

    def test_fixture_contract(self):
        self.validate()

    def test_all_links_resolve_and_default_disclosures_closed(self):
        result = renderer.render(self.data, {})
        page = Page(result)
        self.assertEqual(len(page.ids), len(set(page.ids)))
        self.assertTrue(all(link[1:] in page.ids for link in page.links if link.startswith('#')))
        self.assertTrue(all('open' not in item for item in page.details))
        self.assertLess(result.index('案例事实'), result.index('问题分析'))
        self.assertIn('本页投影：2 次模型记录 · 2 次工具事件', result)

    def test_original_messages_preserved_and_executable_text_escaped(self):
        payload = '<script>alert("x")</script>\n下一行 & "文本"'
        self.data['messages'][0]['text'] = payload
        result = renderer.render(self.data, {})
        self.assertIn(renderer.esc(payload), result)
        self.assertNotIn(payload, result)
        self.assertEqual(result.count('<script>'), 1)

    def test_unknown_version_rejected(self):
        self.data['schema_version'] = 2
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_unknown_fields_rejected_instead_of_silently_discarded(self):
        self.data['events'][0]['reasoning'] = 'must not render'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_duplicate_id_rejected(self):
        self.data['messages'][0]['id'] = 'S1'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_null_id_rejected(self):
        self.data['messages'][0]['id'] = None
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_reserved_page_id_rejected(self):
        self.data['sources'][0]['id'] = 'analysis'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_candidate_cannot_be_labeled_confirmed(self):
        self.data['analysis']['findings'][1]['certainty'] = 'confirmed'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_invalid_enum_type_rejected(self):
        self.data['events'][0]['kind'] = []
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_dangling_refs_rejected(self):
        for group, key in [('evidence', 'event_ids'), ('messages', 'source_ids')]:
            with self.subTest(group=group):
                data = copy.deepcopy(self.data)
                data[group][0][key] = ['does-not-exist']
                with self.assertRaises(renderer.ContractError):
                    renderer.validate(data, FIXTURE.parent)

    def test_fields_read_exact_parameter_not_a_second_model_copy(self):
        tool = self.data['events'][-1]
        self.assertEqual(renderer.pointer(tool, '/input/arguments/arguments/modelVersion'), 'example-image-v1')
        tool['input']['arguments']['arguments']['modelVersion'] = 'changed-model'
        self.assertIn('changed-model', renderer.render(self.data, {}))
        tool['fields'][0]['value'] = 'invented-model'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_missing_pointer_rejected(self):
        self.data['events'][-1]['fields'][0]['pointer'] = '/output/actualModel'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_json_pointer_escaping_and_array_indices(self):
        item = {'input': {'a/b~c': ['first', 'second']}}
        self.assertEqual(renderer.pointer(item, '/input/a~1b~0c/1'), 'second')
        for suffix in ['-1', '01', '-', '5']:
            with self.subTest(suffix=suffix), self.assertRaises(renderer.ContractError):
                renderer.pointer(item, '/input/a~1b~0c/' + suffix)

    def test_root_requires_confirmation_and_mechanism(self):
        finding = self.data['analysis']['findings'][1]
        finding['role'] = 'root-cause'
        with self.assertRaises(renderer.ContractError):
            self.validate()
        finding['certainty'] = 'confirmed'
        with self.assertRaises(renderer.ContractError):
            self.validate()
        finding['mechanism'] = '合成 fixture 的独立机制证据描述，不代表真实根因。'
        self.validate()
        self.data['evidence'][2]['status'] = 'inferred'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_event_order_cannot_be_rearranged_across_messages(self):
        self.data['events'][0]['after_message_id'] = 'M2'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_parent_reference_must_be_an_existing_predecessor(self):
        self.data['events'][1]['parent_id'] = 'R2'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_flow_cycle_and_missing_node_rejected(self):
        flow = self.data['analysis']['flow']
        flow['edges'].append({'from': 'N4', 'to': 'N1', 'relation': 'inferred'})
        with self.assertRaises(renderer.ContractError):
            self.validate()
        flow['edges'][-1]['to'] = 'missing'
        with self.assertRaises(renderer.ContractError):
            self.validate()

    def test_unknown_conversation_and_single_error_do_not_invent_messages(self):
        self.data['messages'] = []
        event = self.data['events'][-1]
        event.pop('parent_id')
        event['after_message_id'] = None
        self.data['events'] = [event]
        self.data['evidence'] = [self.data['evidence'][2]]
        self.data['analysis']['findings'] = []
        self.data['analysis']['flow'] = {'nodes': [], 'edges': [], 'note': '证据不足，无法可靠成图。'}
        self.validate()
        result = renderer.render(self.data, {})
        self.assertIn('原始对话未取得', result)
        self.assertIn('证据不足，无法可靠成图', result)
        self.assertNotIn('class="message user"', result)

    def test_candidate_does_not_auto_become_confirmed(self):
        result = renderer.render(self.data, {})
        self.assertIn('根因候选 · 推断', result)
        self.assertNotIn('已确认根因 · 已确认', result)

    def test_rejected_submission_does_not_invent_actual_model(self):
        result = renderer.render(self.data, {})
        self.assertIn('not-submitted', result)
        self.assertIn('example-image-v1', result)
        self.assertIn('实际生成模型未执行', result)
        self.assertNotIn('actualModel', result)

    def test_inferred_edges_render_as_dashed(self):
        self.data['analysis']['flow']['edges'][0]['relation'] = 'inferred'
        self.assertIn('stroke-dasharray="5 4"', renderer.render(self.data, {}))

    def test_offline_security_policy_matches_template_assets(self):
        result = renderer.render(self.data, {})
        self.assertNotIn('https://', result)
        for asset in ['report.css', 'report.js']:
            digest = base64.b64encode(hashlib.sha256((ROOT / 'assets' / asset).read_bytes()).digest()).decode()
            self.assertIn('sha256-' + digest, result)
        self.assertIn("connect-src 'none'", result)

    def test_attachment_paths_cannot_escape_input_root(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            folder = base / 'input'
            folder.mkdir()
            (base / 'secret.txt').write_text('outside')
            (folder / 'leak.txt').symlink_to(base / 'secret.txt')
            for path in ['../secret.txt', str(base / 'secret.txt'), 'https://host/image.jpg', 'leak.txt', 'C:\\secret.txt']:
                with self.subTest(path=path), self.assertRaises(renderer.ContractError):
                    renderer.local_file(folder, path)

    def test_portable_bundle_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            (base / 'note.txt').write_text('synthetic artifact\n')
            self.data['messages'][0]['attachments'][0] = {'id': 'A1', 'name': 'note.txt', 'status': 'available', 'path': 'note.txt'}
            source = base / 'case.json'
            source.write_text(json.dumps(self.data))
            first = base / 'first'
            result = renderer.build(source, first)
            self.assertTrue(result.is_file())
            portable = json.loads((first / 'case.json').read_text())
            renderer.validate(portable, first)
            artifact = first / portable['messages'][0]['attachments'][0]['path']
            self.assertEqual(artifact.read_bytes(), (base / 'note.txt').read_bytes())
            second = base / 'second'
            renderer.build(first / 'case.json', second)
            self.assertEqual((second / 'index.html').read_bytes(), result.read_bytes())
            with self.assertRaises(renderer.ContractError):
                renderer.build(source, first)


if __name__ == '__main__':
    unittest.main()
