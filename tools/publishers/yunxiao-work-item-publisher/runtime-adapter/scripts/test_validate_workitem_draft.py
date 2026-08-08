#!/usr/bin/env python3

from __future__ import annotations

import copy
import unittest

from validate_workitem_draft import fingerprint, validate


def valid_payload() -> dict:
    file_name = "evidence.png"
    return {
        "project": {"id": "project-id", "name": "Test"},
        "work_item_type": "缺陷",
        "title": "【Skill 管理】安装后需要重启",
        "priority": "中",
        "description": (
            "【问题现象】安装后需要重启\n"
            "【期望结果】无需重启\n"
            "【排查证据】见附件 evidence.png\n"
            "【排查结论】运行时未同步\n"
            "【验收标准】新会话可以识别"
        ),
        "evidence": [
            {
                "level": "已验证",
                "kind": "截图",
                "source": file_name,
                "observation": "安装成功但提示重启",
                "supports": "问题发生在运行时刷新阶段",
            }
        ],
        "attachments": [
            {
                "file_name": file_name,
                "mime_type": "image/png",
                "size_bytes": 1024,
                "sha256": "a" * 64,
                "sensitivity_check": "passed",
            }
        ],
        "duplicate_check": {"status": "passed"},
        "confirmation": {"status": "pending"},
    }


class AttachmentValidationTests(unittest.TestCase):
    def test_valid_screenshot_attachment(self) -> None:
        errors, warnings, _ = validate(valid_payload(), require_confirmed=False)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_attachment_metadata_changes_confirmation_fingerprint(self) -> None:
        before = valid_payload()
        after = copy.deepcopy(before)
        after["attachments"][0]["sha256"] = "b" * 64
        self.assertNotEqual(fingerprint(before), fingerprint(after))

    def test_oversized_attachment_is_rejected(self) -> None:
        payload = valid_payload()
        payload["attachments"][0]["size_bytes"] = 10 * 1024 * 1024 + 1
        errors, _, _ = validate(payload, require_confirmed=False)
        self.assertIn("attachments[0].size_bytes exceeds the 10 MB MCP limit", errors)

    def test_sensitive_attachment_is_rejected(self) -> None:
        payload = valid_payload()
        payload["attachments"][0]["sensitivity_check"] = "blocked"
        errors, _, _ = validate(payload, require_confirmed=False)
        self.assertIn("attachments[0].sensitivity_check must be passed", errors)

    def test_local_path_is_rejected(self) -> None:
        payload = valid_payload()
        payload["attachments"][0]["file_name"] = "/tmp/evidence.png"
        errors, _, _ = validate(payload, require_confirmed=False)
        self.assertIn("attachments[0].file_name must not contain a local path", errors)


if __name__ == "__main__":
    unittest.main()
