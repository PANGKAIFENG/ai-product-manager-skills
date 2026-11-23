#!/usr/bin/env python3
"""Validate a redacted case projection and render a portable offline report."""

import argparse
import base64
import hashlib
import html
import json
import re
import shutil
import tempfile
from collections import Counter
from pathlib import Path
from string import Template


ROOT = Path(__file__).resolve().parent.parent
ID = re.compile(r"[A-Za-z][A-Za-z0-9_-]*\Z")
CERTAINTIES = {"confirmed": "已确认", "inferred": "推断", "unknown": "待验证"}
ROLES = {"failure-point": "失败点", "root-cause-candidate": "根因候选", "root-cause": "已确认根因",
         "amplifier": "放大因素", "opportunity": "优化候选", "unknown": "待定位"}
STATUSES = {"recorded": "已记录", "returned": "已返回", "error": "错误", "rejected": "被拒绝", "unknown": "状态未知"}
ORIGINS = {"trace": "trace 记录", "client": "客户端记录", "tool-interaction": "工具交互记录", "summary": "分析者摘要，非原话"}


class ContractError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ContractError(message)


def shape(item, required, optional=()):
    require(isinstance(item, dict), "对象必须是 JSON object")
    require(set(required) <= item.keys(), f"缺少字段：{set(required) - item.keys()}")
    require(not item.keys() - set(required) - set(optional), f"未知字段：{item.keys() - set(required) - set(optional)}")


def nonempty(value):
    require(isinstance(value, str) and bool(value.strip()), "字段必须是非空字符串")


def choice(value, values, message):
    require(isinstance(value, str) and value in values, message)


def pointer(event, value):
    require(isinstance(value, str) and value.startswith(("/input/", "/output/")), "字段指针必须指向 input/output 内部")
    current = event
    try:
        for segment in value[1:].split("/"):
            require(not re.search(r"~(?![01])", segment), "JSON Pointer 转义无效")
            key = segment.replace("~1", "/").replace("~0", "~")
            if isinstance(current, list):
                require(bool(re.fullmatch(r"0|[1-9][0-9]*", key)), "数组指针须为非负规范索引")
                current = current[int(key)]
            else:
                current = current[key]
    except (KeyError, IndexError, TypeError, ValueError) as error:
        raise ContractError(f"指针无法解析：{value}") from error
    return current


def local_file(base, value):
    require(isinstance(value, str) and bool(value) and "\\" not in value, "附件路径须为相对文件路径")
    relative = Path(value)
    require(not relative.is_absolute() and ".." not in relative.parts and ":" not in value, "附件路径不安全")
    target = (base / relative).resolve()
    require(target.is_relative_to(base.resolve()) and target.is_file(), f"附件不存在或越界：{value}")
    return target


def validate(data, base):
    shape(data, ("schema_version", "case", "sources", "messages", "events", "evidence", "analysis"))
    require(type(data["schema_version"]) is int and data["schema_version"] == 1, "不支持的数据契约版本")
    shape(data["case"], ("id", "title", "request", "inputs", "expected", "actual", "coverage"))
    for value in data["case"].values():
        nonempty(value)
    shape(data["analysis"], ("conclusion", "findings", "flow"))
    nonempty(data["analysis"]["conclusion"])
    flow = data["analysis"]["flow"]
    shape(flow, ("nodes", "edges", "note"))
    require(isinstance(flow["note"], str), "图说明须为文本")
    groups = {key: data[key] for key in ("sources", "messages", "events", "evidence")}
    groups.update(findings=data["analysis"]["findings"], nodes=flow["nodes"])
    known = {}
    all_ids = {'facts', 'conversation', 'analysis', 'sources', 'arrow', 'location-bar', 'location-label', 'location-return', 'clear-location'}
    for name, group in groups.items():
        require(isinstance(group, list), f"{name} 必须是数组")
        known[name] = set()
        for item in group:
            require(isinstance(item, dict) and isinstance(item.get("id"), str) and ID.fullmatch(item["id"]), f"{name} ID 无效")
            require(item["id"] not in all_ids, f"重复 ID：{item['id']}")
            all_ids.add(item["id"])
            known[name].add(item["id"])

    def refs(item, key, group):
        values = item[key]
        require(isinstance(values, list) and all(isinstance(value, str) for value in values), f"{key} 必须是 ID 数组")
        require(len(values) == len(set(values)) and set(values) <= known[group], f"{item['id']} 的 {key} 含重复或悬空引用")

    for source in data["sources"]:
        shape(source, ("id", "label", "locator"))
        nonempty(source["label"])
        nonempty(source["locator"])
    for message in data["messages"]:
        shape(message, ("id", "role", "text", "origin", "source_ids"), ("attachments",))
        choice(message["role"], {"user", "assistant"}, "消息角色无效")
        choice(message["origin"], ORIGINS, "消息来源类型无效")
        require(isinstance(message["text"], str), "消息正文须为文本")
        refs(message, "source_ids", "sources")
        require(bool(message["source_ids"]), "消息须有来源")
        attachments = message.get("attachments", [])
        require(isinstance(attachments, list), "attachments 必须是数组")
        for attachment in attachments:
            shape(attachment, ("id", "name", "status"), ("path", "thumbnail", "note"))
            require(isinstance(attachment["id"], str) and ID.fullmatch(attachment["id"]) and attachment["id"] not in all_ids, "附件 ID 无效或重复")
            all_ids.add(attachment["id"])
            nonempty(attachment["name"])
            choice(attachment["status"], {"available", "missing", "redacted"}, "附件状态无效")
            if "note" in attachment:
                nonempty(attachment["note"])
            if attachment["status"] == "available":
                require("path" in attachment, "available 附件缺少 path")
                local_file(base, attachment["path"])
                if "thumbnail" in attachment:
                    local_file(base, attachment["thumbnail"])
            else:
                require(not {"path", "thumbnail"} & attachment.keys(), "缺失/去敏附件不可携带可读路径")
    message_order = {message["id"]: index for index, message in enumerate(data["messages"])}
    seen_events = set()
    previous = -1
    for event in data["events"]:
        shape(event, ("id", "kind", "name", "status", "after_message_id", "source_ids"), ("parent_id", "time", "input", "output", "fields"))
        choice(event["kind"], {"model", "tool"}, "事件类型无效")
        choice(event["status"], STATUSES, "事件状态无效")
        nonempty(event["name"])
        refs(event, "source_ids", "sources")
        require(bool(event["source_ids"]), "事件须有来源")
        anchor = event["after_message_id"]
        require(anchor is None or isinstance(anchor, str), "消息定位须为 ID 或 null")
        require(anchor is None or anchor in message_order, "事件消息定位不存在")
        index = message_order.get(anchor, -1)
        require(index >= previous, "事件跨消息的展示位置会改变原有顺序")
        previous = index
        if "parent_id" in event:
            require(isinstance(event["parent_id"], str) and event["parent_id"] in seen_events, "parent_id 须指向已记录的前序事件")
        seen_events.add(event["id"])
        if "time" in event:
            nonempty(event["time"])
        require(isinstance(event.get("fields", []), list), "fields 须为数组")
        for field in event.get("fields", []):
            shape(field, ("label", "pointer"))
            nonempty(field["label"])
            pointer(event, field["pointer"])
    evidence_by_id = {item["id"]: item for item in data["evidence"]}
    for evidence in data["evidence"]:
        shape(evidence, ("id", "status", "text", "source_ids", "message_ids", "event_ids"))
        choice(evidence["status"], CERTAINTIES, "证据状态无效")
        nonempty(evidence["text"])
        for key, group in (("source_ids", "sources"), ("message_ids", "messages"), ("event_ids", "events")):
            refs(evidence, key, group)
        require(evidence["status"] == "unknown" or any(evidence[key] for key in ("source_ids", "message_ids", "event_ids")), "证据缺少可定位来源")
    for finding in data["analysis"]["findings"]:
        shape(finding, ("id", "title", "role", "certainty", "fact", "impact", "recommendation", "verification", "evidence_ids"), ("mechanism",))
        for key in ("title", "fact", "impact", "recommendation", "verification"):
            nonempty(finding[key])
        choice(finding["role"], ROLES, "诊断角色无效")
        choice(finding["certainty"], CERTAINTIES, "置信状态无效")
        if "mechanism" in finding:
            nonempty(finding["mechanism"])
        refs(finding, "evidence_ids", "evidence")
        require(bool(finding["evidence_ids"]), "诊断须引用证据")
        if finding["role"] == "root-cause":
            require(finding["certainty"] == "confirmed", "已确认根因不能同时为推断/未知")
            nonempty(finding.get("mechanism"))
            require(any(evidence_by_id[key]["status"] == "confirmed" for key in finding["evidence_ids"]), "根因缺少已确认机制证据")
        if finding["role"] == "root-cause-candidate":
            require(finding["certainty"] != "confirmed", "根因候选仍须标为推断或待验证")
    for node in flow["nodes"]:
        shape(node, ("id", "label", "evidence_ids"), ("finding_id",))
        nonempty(node["label"])
        require(len(node["label"]) <= 32, "图节点标签过长，请把详细内容放证据链")
        refs(node, "evidence_ids", "evidence")
        require(bool(node["evidence_ids"]), "图节点须引用证据")
        require("finding_id" not in node or (isinstance(node["finding_id"], str) and node["finding_id"] in known["findings"]), "图节点引用了不存在的诊断")
    require(isinstance(flow["edges"], list), "图边须为数组")
    require(len(flow["nodes"]) >= 2 or (not flow["edges"] and bool(flow["note"].strip())), "不足两节点时须说明无法成图")
    graph = {key: [] for key in known["nodes"]}
    for edge in flow["edges"]:
        shape(edge, ("from", "to", "relation"))
        require(isinstance(edge["from"], str) and isinstance(edge["to"], str) and edge["from"] in graph and edge["to"] in graph, "图边定位无效")
        choice(edge["relation"], {"observed", "inferred"}, "图边关系无效")
        graph[edge["from"]].append(edge["to"])
    visited, active = set(), set()

    def visit(key):
        require(key not in active, "流程图含环，请合并重复事件并保留次数")
        if key in visited:
            return
        active.add(key)
        for child in graph[key]:
            visit(child)
        active.remove(key)
        visited.add(key)

    for key in graph:
        visit(key)


def esc(value):
    return html.escape(str(value), quote=True)


def display(value):
    return value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2)


def link(key, label=None):
    return f'<a href="#{esc(key)}">{esc(label or key)}</a>'


def render_flow(flow, findings):
    if len(flow["nodes"]) < 2:
        return f'<p class="muted">{esc(flow["note"])}</p>'
    nodes = flow["nodes"]
    levels = {node["id"]: 0 for node in nodes}
    for _ in nodes:
        for edge in flow["edges"]:
            levels[edge["to"]] = max(levels[edge["to"]], levels[edge["from"]] + 1)
    layers = {}
    for node in nodes:
        layers.setdefault(levels[node["id"]], []).append(node)
    width = max(len(layer) for layer in layers.values()) * 260
    height = (max(layers) + 1) * 140
    positions = {node["id"]: ((width - len(layer) * 260) / 2 + i * 260 + 10, level * 140 + 10)
                 for level, layer in layers.items() for i, node in enumerate(layer)}
    parts = [f'<div class="flow-scroll"><svg class="flow" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="诊断流程图；实线为记录顺序，虚线为推断关系"><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0 0L8 4L0 8" fill="#a0aba5"/></marker></defs>']
    for edge in flow["edges"]:
        x1, y1 = positions[edge["from"]]
        x2, y2 = positions[edge["to"]]
        dash = ' stroke-dasharray="5 4"' if edge["relation"] == "inferred" else ''
        parts.append(f'<path d="M{x1+120} {y1+90}C{x1+120} {y1+115} {x2+120} {y2-25} {x2+120} {y2}" fill="none" stroke="#a0aba5"{dash} marker-end="url(#arrow)"/>')
    for node in nodes:
        x, y = positions[node["id"]]
        finding = findings.get(node.get("finding_id"), {})
        role = finding.get("role", "neutral")
        label = node["label"]
        lines = [label[i:i+16] for i in range(0, len(label), 16)]
        require(len(lines) <= 2, "图节点标签过长，请缩为最多 32 字符，详细内容放证据链")
        parts.append(f'<a href="#{esc(node["evidence_ids"][0])}"><g class="node {role}"><title>{esc(label)}</title><rect x="{x}" y="{y}" width="240" height="90" rx="4"/><text x="{x+12}" y="{y+20}" class="node-meta">{esc(" / ".join(node["evidence_ids"]))} · {esc(ROLES.get(role, "记录"))}</text>')
        for index, line in enumerate(lines):
            parts.append(f'<text x="{x+12}" y="{y+43+index*19}">{esc(line)}</text>')
        parts.append('</g></a>')
    parts.append(f'</svg></div><p class="muted">实线：记录顺序；虚线：推断关系。箭头本身不证明因果。{esc(flow["note"])}</p>')
    return ''.join(parts)


def render(data, assets):
    def attachment(item):
        if item["status"] != "available":
            return f'<p class="attachment-missing">{esc(item["name"])} · {"未取得" if item["status"] == "missing" else "已去敏"} {esc(item.get("note", ""))}</p>'
        original = assets[item["path"]]
        preview = assets.get(item.get("thumbnail"), original)
        image = f'<img src="{esc(preview)}" alt="{esc(item["name"])}" loading="lazy">' if Path(preview).suffix in {".png", ".jpg", ".jpeg", ".webp", ".gif"} else ''
        return f'<details class="attachment"><summary>{esc(item["name"])}</summary>{image}<a href="{esc(original)}" target="_blank" rel="noopener">打开附件</a></details>'

    def event(item):
        fields = ''.join(f'<div><dt>{esc(field["label"])}</dt><dd>{esc(display(pointer(item, field["pointer"])))}</dd></div>' for field in item.get("fields", []))
        raw = {key: item[key] for key in ("input", "output") if key in item}
        return f'<li><details class="event {item["kind"]}" id="{item["id"]}"><summary><span class="kind">{"模型" if item["kind"] == "model" else "工具"}</span><span class="event-name">{esc(item["name"])}</span><span class="state {item["status"]}">{STATUSES[item["status"]]}</span></summary><div class="event-body"><p class="muted">{esc(item.get("time", "时间未记录"))} · 记录 ID：{item["id"]}</p><dl class="fields">{fields}</dl><details class="raw"><summary>脱敏原始记录 JSON</summary><pre>{esc(display(raw))}</pre></details><p class="muted">来源：{" · ".join(link(key) for key in item["source_ids"])}</p></div></details></li>'

    def process(anchor):
        group = [item for item in data["events"] if item["after_message_id"] == anchor]
        if not group:
            return ''
        counts = Counter(item["kind"] for item in group)
        return f'<details class="process"><summary>处理过程 <span>{counts["model"]} 次模型记录 · {counts["tool"]} 次工具事件</span></summary><ol>{"".join(event(item) for item in group)}</ol></details>'

    conversation = process(None)
    if not data["messages"]:
        conversation = '<p class="muted">原始对话未取得；下方仅为已取得的执行投影。</p>' + conversation
    for item in data["messages"]:
        conversation += f'<article class="message {item["role"]}" id="{item["id"]}"><header>{"用户" if item["role"] == "user" else "Agent"}<small>{ORIGINS[item["origin"]]}</small></header><div class="message-text">{esc(item["text"])}</div>{"".join(attachment(part) for part in item.get("attachments", []))}</article>{process(item["id"])}'
    case = data["case"]
    facts = ''.join(f'<div><dt>{label}</dt><dd>{esc(case[key])}</dd></div>' for key, label in (("request", "用户要求"), ("inputs", "关键输入"), ("expected", "预期交付"), ("actual", "实际结果"), ("coverage", "证据范围")))
    findings = ''
    for item in data["analysis"]["findings"]:
        findings += f'<article class="finding" id="{item["id"]}"><p class="certainty {item["role"]}">{ROLES[item["role"]]} · {CERTAINTIES[item["certainty"]]}</p><h3>{esc(item["title"])}</h3><dl>{"".join(f"<div><dt>{label}</dt><dd>{esc(item[key])}</dd></div>" for key, label in (("fact", "事实"), ("impact", "影响"), ("recommendation", "优化方向"), ("verification", "如何验证")))}{f"<div><dt>机制依据</dt><dd>{esc(item['mechanism'])}</dd></div>" if item.get('mechanism') else ""}</dl><p class="evidence-links">证据：{" · ".join(link(key) for key in item["evidence_ids"])}</p></article>'
    evidence = ''
    for item in data["evidence"]:
        targets = item["message_ids"] + item["event_ids"]
        actions = ' · '.join(f'<a href="#{key}" data-locate data-return="{item["id"]}">定位 {key}</a>' for key in targets)
        evidence += f'<article class="evidence-item" id="{item["id"]}"><h3>{item["id"]} <small>{CERTAINTIES[item["status"]]}</small></h3><p>{esc(item["text"])}</p><p>{actions}</p><p class="muted">来源：{" · ".join(link(key) for key in item["source_ids"]) or "待补"}</p></article>'
    sources = ''.join(f'<li id="{item["id"]}"><strong>{item["id"]} · {esc(item["label"])}</strong><p>{esc(item["locator"])}</p></li>' for item in data["sources"])
    css = (ROOT / 'assets/report.css').read_text(encoding='utf-8')
    script = (ROOT / 'assets/report.js').read_text(encoding='utf-8')
    digest = lambda content: base64.b64encode(hashlib.sha256(content.encode()).digest()).decode()
    return Template((ROOT / 'assets/report.html').read_text(encoding='utf-8')).substitute(
        title=esc(case["title"]), css=css, script=script, style_hash=digest(css), script_hash=digest(script),
        facts=facts, conversation=conversation, conclusion=esc(data["analysis"]["conclusion"]),
        flow=render_flow(data["analysis"]["flow"], {item["id"]: item for item in data["analysis"]["findings"]}),
        findings=findings or '<p class="muted">未确认需要单列的问题。</p>', evidence=evidence, sources=sources,
        counts=f'本页投影：{sum(item["kind"] == "model" for item in data["events"])} 次模型记录 · {sum(item["kind"] == "tool" for item in data["events"])} 次工具事件',
    )


def build(input_path, output_dir):
    data = json.loads(input_path.read_text(encoding='utf-8'))
    validate(data, input_path.parent)
    require(not output_dir.exists(), "输出目录已存在；请选择新目录，不覆盖旧报告")
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.trace-report-', dir=output_dir.parent) as temporary:
        stage = Path(temporary) / 'report'
        stage.mkdir()
        assets = {}
        for message in data["messages"]:
            for item in message.get("attachments", []):
                if item["status"] != "available":
                    continue
                for key in ("path", "thumbnail"):
                    if key not in item:
                        continue
                    source = local_file(input_path.parent, item[key])
                    hasher = hashlib.sha256()
                    with source.open('rb') as stream:
                        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
                            hasher.update(chunk)
                    digest = hasher.hexdigest()
                    extension = source.suffix.lower()
                    if extension not in {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.pdf', '.txt', '.csv', '.docx', '.xlsx', '.zip'}:
                        extension = '.bin'
                    relative = f'attachments/{digest}{extension}'
                    target = stage / relative
                    target.parent.mkdir(exist_ok=True)
                    shutil.copyfile(source, target)
                    assets[item[key]] = relative
        page = render(data, assets)
        portable = json.loads(json.dumps(data))
        for message in portable["messages"]:
            for item in message.get("attachments", []):
                for key in ("path", "thumbnail"):
                    if key in item:
                        item[key] = assets[item[key]]
        (stage / 'index.html').write_text(page, encoding='utf-8')
        (stage / 'case.json').write_text(json.dumps(portable, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        stage.rename(output_dir)
    return output_dir / 'index.html'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='Versioned, redacted case.json projection')
    parser.add_argument('--validate-only', action='store_true', help='Check without writing any report')
    parser.add_argument('--output-dir', type=Path, help='New report directory; existing directories are not overwritten')
    args = parser.parse_args()
    try:
        if args.validate_only:
            validate(json.loads(args.input.read_text(encoding='utf-8')), args.input.parent)
            print('PASS: case contract and references')
        else:
            require(args.output_dir is not None, '缺少 --output-dir，或使用 --validate-only')
            print(build(args.input.resolve(), args.output_dir.resolve()))
    except (ContractError, OSError, json.JSONDecodeError) as error:
        parser.exit(2, f'ERROR: {error}\n')


if __name__ == '__main__':
    main()
