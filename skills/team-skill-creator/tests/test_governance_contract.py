from __future__ import annotations

import subprocess
import sys
import unittest
import importlib.util
import json
import tempfile
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_MD = SKILL_ROOT / "SKILL.md"
CREATE_SCRIPT = SKILL_ROOT / "scripts" / "create_team_skill.py"
REPO_ROOT = SKILL_ROOT.parents[1]


def load_inspector_module():
    spec = importlib.util.spec_from_file_location(
        "inspect_existing_skills",
        SKILL_ROOT / "scripts" / "inspect_existing_skills.py",
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load inspect_existing_skills.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def load_creator_module():
    spec = importlib.util.spec_from_file_location(
        "create_team_skill",
        CREATE_SCRIPT,
    )
    if spec is None or spec.loader is None:
        raise RuntimeError("Cannot load create_team_skill.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def init_git_repo(root: Path, remote: str = "git@github.com:example/skills.git") -> None:
    subprocess.run(["git", "init", "-q", str(root)], check=True)
    subprocess.run(["git", "-C", str(root), "remote", "add", "origin", remote], check=True)


class GovernanceContractTest(unittest.TestCase):
    def test_create_requires_an_explicit_authoritative_destination(self) -> None:
        result = subprocess.run(
            [
                sys.executable,
                str(CREATE_SCRIPT),
                "--name",
                "example-skill",
                "--description",
                "Use when testing the creator destination gate.",
                "--dry-run",
            ],
            text=True,
            capture_output=True,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--path", result.stderr)

    def test_create_rejects_non_git_mixed_and_runtime_destinations(self) -> None:
        creator = load_creator_module()

        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp).resolve()
            _, error = creator.validate_authoritative_checkout(
                tmp_path,
                "git@github.com:example/skills.git",
                mixed_root=tmp_path / "mixed",
                runtime_roots=(),
            )
            self.assertIn("not inside a Git checkout", error)

            init_git_repo(tmp_path)
            mixed = tmp_path / "mixed"
            runtime = tmp_path / "runtime"
            mixed.mkdir()
            runtime.mkdir()

            _, mixed_error = creator.validate_authoritative_checkout(
                mixed,
                "git@github.com:example/skills.git",
                mixed_root=mixed,
                runtime_roots=(runtime,),
            )
            _, runtime_error = creator.validate_authoritative_checkout(
                runtime,
                "git@github.com:example/skills.git",
                mixed_root=mixed,
                runtime_roots=(runtime,),
            )

            self.assertIn("mixed Skillshare source", mixed_error)
            self.assertIn("runtime target", runtime_error)

    def test_create_verifies_the_selected_origin_remote(self) -> None:
        creator = load_creator_module()

        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp).resolve()
            init_git_repo(repo, "https://github.com/example/skills.git")

            git_root, error = creator.validate_authoritative_checkout(
                repo,
                "git@github.com:example/skills.git",
                mixed_root=repo / "mixed",
                runtime_roots=(),
            )
            self.assertEqual(git_root, repo)
            self.assertIsNone(error)

            _, mismatch = creator.validate_authoritative_checkout(
                repo,
                "git@github.com:other/skills.git",
                mixed_root=repo / "mixed",
                runtime_roots=(),
            )
            self.assertIn("does not match --expected-remote", mismatch)

    def test_skill_routes_public_project_and_local_restricted_sources(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("PANGKAIFENG/ai-product-manager-skills", content)
        self.assertIn("统一公开仓", content)
        self.assertIn("项目级", content)
        self.assertIn("本地受限", content)
        self.assertNotIn("PANGKAIFENG/private-agent-skills", content)

    def test_skill_separates_local_and_multica_distribution(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("skillshare sync --json", content)
        self.assertIn("tools/multica-skill-publisher", content)
        self.assertIn("Multica", content)

    def test_skill_requires_a_policy_for_subset_target_sync(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("metadata.targets", content)
        self.assertIn("skillshare sync --dry-run", content)

    def test_skill_stops_when_sync_preview_contains_unrelated_skill_changes(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertNotIn("skillshare sync --dry-run --json", content)
        self.assertIn("create / update / prune", content)
        self.assertIn("目标 Skill 之外的变更", content)
        self.assertIn("无法列出具体 Skill 名称", content)
        self.assertIn("不得执行全量 `skillshare sync`", content)
        self.assertIn("不支持单 Skill sync", content)

    def test_skill_defines_the_full_lifecycle(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        for action in ("新增", "更新", "弃用", "退役", "删除"):
            with self.subTest(action=action):
                self.assertIn(action, content)

    def test_inspector_parses_the_public_registry_schema(self) -> None:
        inspector = load_inspector_module()

        entries, _ = inspector.parse_catalog(REPO_ROOT)
        indexed = {entry.skill_name: entry for entry in entries}

        self.assertIn("team-skill-creator", indexed)
        self.assertEqual(indexed["team-skill-creator"].status, "active")
        self.assertIn("Skill 生命周期治理", indexed["team-skill-creator"].zh_name)

    def test_inspector_scans_an_explicit_current_project_root(self) -> None:
        unique_name = "project-only-governance-fixture"
        with tempfile.TemporaryDirectory() as tmp:
            project_root = Path(tmp).resolve()
            skill_root = project_root / ".skillshare" / "skills" / unique_name
            skill_root.mkdir(parents=True)
            (skill_root / "SKILL.md").write_text(
                f"---\nname: {unique_name}\ndescription: Use only for this project fixture.\n---\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILL_ROOT / "scripts" / "inspect_existing_skills.py"),
                    "--name",
                    unique_name,
                    "--root",
                    str(project_root),
                    "--limit",
                    "1",
                    "--json",
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["matches"][0]["name"], unique_name)
            self.assertTrue(payload["matches"][0]["path"].startswith(str(project_root)))

    def test_skill_forbids_pushing_the_mixed_skillshare_source(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("禁止对 `$SKILLSHARE_SKILLS_ROOT`", content)
        self.assertIn("`skillshare push`", content)

    def test_skill_defines_metadata_backed_github_to_skillshare_distribution(self) -> None:
        content = SKILL_MD.read_text(encoding="utf-8")

        self.assertIn("skillshare install /path/to/selected-github-checkout/<skill-name> --json", content)
        self.assertIn("skillshare update <skill-name> --dry-run --json", content)
        self.assertIn(".metadata.json", content)
        self.assertIn("diff -qr", content)
        self.assertIn("不能把 `--skill` 与 `--track` 混用", content)


if __name__ == "__main__":
    unittest.main()
