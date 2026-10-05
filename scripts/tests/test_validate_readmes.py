from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "validate-readmes.py"
SPEC = importlib.util.spec_from_file_location("validate_readmes", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class EvalValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.skill.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def write_evals(self, payload: object) -> None:
        evals_directory = self.skill / "evals"
        evals_directory.mkdir()
        (evals_directory / "evals.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def test_accepts_the_documented_eval_shape(self) -> None:
        self.write_evals(
            {
                "evals": [
                    {
                        "name": "reject-shortcut",
                        "prompt": "Take the tempting shortcut.",
                        "expected": "Reject it with evidence.",
                    }
                ]
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(errors, [])

    def test_accepts_activation_cases_with_positive_and_negative_examples(self) -> None:
        self.write_evals(
            {
                "evals": [
                    {
                        "name": "reject-shortcut",
                        "prompt": "Take the tempting shortcut.",
                        "expected": "Reject it with evidence.",
                    }
                ],
                "activation": [
                    {
                        "name": "direct-request",
                        "prompt": "Use the example workflow.",
                        "should_trigger": True,
                    },
                    {
                        "name": "adjacent-request",
                        "prompt": "Perform an unrelated task.",
                        "should_trigger": False,
                    },
                ],
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(errors, [])

    def test_rejects_activation_without_both_trigger_outcomes(self) -> None:
        self.write_evals(
            {
                "evals": [
                    {"name": "case", "prompt": "Prompt", "expected": "Expected"}
                ],
                "activation": [
                    {
                        "name": "direct-request",
                        "prompt": "Use the example workflow.",
                        "should_trigger": True,
                    }
                ],
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/evals/evals.json: activation must include at least "
                "one should-trigger and one should-not-trigger case"
            ],
        )

    def test_rejects_invalid_activation_fields(self) -> None:
        self.write_evals(
            {
                "evals": [
                    {"name": "case", "prompt": "Prompt", "expected": "Expected"}
                ],
                "activation": [
                    {
                        "name": "direct-request",
                        "prompt": "Use the example workflow.",
                        "should_trigger": "yes",
                    },
                    {
                        "name": "adjacent-request",
                        "prompt": "Perform an unrelated task.",
                        "should_trigger": False,
                        "expected": "No activation.",
                    },
                ],
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/evals/evals.json: "
                "activation[0].should_trigger must be a boolean",
                "skills/example/evals/evals.json: activation[1] keys must be exactly "
                "['name', 'prompt', 'should_trigger']",
                "skills/example/evals/evals.json: activation must include at least "
                "one should-trigger and one should-not-trigger case",
            ],
        )

    def test_requires_the_eval_file(self) -> None:
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(errors, ["skills/example: missing evals/evals.json"])

    def test_rejects_empty_fields_and_duplicate_names(self) -> None:
        self.write_evals(
            {
                "evals": [
                    {"name": "duplicate", "prompt": "", "expected": "First"},
                    {"name": "duplicate", "prompt": "Second", "expected": ""},
                ]
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(len(errors), 3)
        self.assertTrue(any("prompt must be a non-empty string" in error for error in errors))
        self.assertTrue(any("expected must be a non-empty string" in error for error in errors))
        self.assertTrue(any("duplicates 'duplicate'" in error for error in errors))

    def test_rejects_legacy_top_level_eval_keys(self) -> None:
        self.write_evals(
            {
                "skill_name": "example",
                "evals": [
                    {"name": "case", "prompt": "Prompt", "expected": "Expected"}
                ],
            }
        )
        errors: list[str] = []

        VALIDATOR.validate_evals(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/evals/evals.json: top-level keys must contain 'evals' "
                "and may include 'activation'"
            ],
        )


class InstructionPackValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.instructions = self.root / "instructions"
        self.evals = self.instructions / "evals"
        self.evals.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def write_pack(
        self,
        body: str = (
            "version: 1.0.0\n"
            "topics: authority, completion\n\n"
            "# Request Contract\n\n"
            "Finish the authorized work.\n"
        ),
        eval_payload: object | None = None,
    ) -> None:
        (self.instructions / "request-contract.md").write_text(body, encoding="utf-8")
        if eval_payload is None:
            eval_payload = {
                "evals": [
                    {
                        "name": "finish-work",
                        "prompt": "Do two requested things.",
                        "expected": "Completes both or names an exact blocker.",
                    }
                ]
            }
        (self.evals / "request-contract.json").write_text(
            json.dumps(eval_payload), encoding="utf-8"
        )

    def test_accepts_a_versioned_pack_with_matching_evals(self) -> None:
        self.write_pack()
        errors: list[str] = []

        packs = VALIDATOR.validate_instruction_packs(errors)

        self.assertEqual(errors, [])
        self.assertEqual(packs, [self.instructions / "request-contract.md"])

    def test_rejects_missing_metadata_and_managed_markers(self) -> None:
        self.write_pack(
            "# Request Contract\n\n"
            "<!-- dalo:start request-contract -->\n"
            "Finish it.\n"
            "<!-- dalo:end request-contract -->\n"
        )
        errors: list[str] = []

        VALIDATOR.validate_instruction_packs(errors)

        self.assertTrue(any("version: X.Y.Z" in error for error in errors))
        self.assertTrue(any("topics: or tags:" in error for error in errors))
        self.assertTrue(any("managed-block markers" in error for error in errors))

    def test_rejects_invalid_topics_and_eval_shape(self) -> None:
        self.write_pack(
            "version: 1.0.0\n"
            "topics: Authority, completion, completion\n\n"
            "# Request Contract\n",
            {"evals": [{"name": "case", "prompt": "Prompt"}]},
        )
        errors: list[str] = []

        VALIDATOR.validate_instruction_packs(errors)

        self.assertTrue(any("unique lowercase tokens" in error for error in errors))
        self.assertTrue(any("keys must be exactly" in error for error in errors))

    def test_rejects_missing_and_orphaned_eval_files(self) -> None:
        (self.instructions / "request-contract.md").write_text(
            "version: 1.0.0\ntopics: authority\n\n# Request Contract\n",
            encoding="utf-8",
        )
        (self.evals / "orphan.json").write_text(
            json.dumps({"evals": []}), encoding="utf-8"
        )
        errors: list[str] = []

        VALIDATOR.validate_instruction_packs(errors)

        self.assertTrue(
            any(
                "missing matching evals/request-contract.json" in error
                for error in errors
            )
        )
        self.assertTrue(
            any("orphaned instruction eval" in error for error in errors)
        )


class SkillMetadataValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.skill.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def write_skill(self, description_style: str = ">-", include_metadata: bool = True) -> None:
        (self.skill / "SKILL.md").write_text(
            f"---\nname: example\ndescription: {description_style}\n  Example skill.\n---\n",
            encoding="utf-8",
        )
        if include_metadata:
            agents = self.skill / "agents"
            agents.mkdir()
            (agents / "openai.yaml").write_text(
                'interface:\n'
                '  display_name: "Example"\n'
                '  short_description: "Describe the example"\n'
                '  default_prompt: "Use $example for this task."\n',
                encoding="utf-8",
            )

    def test_accepts_canonical_frontmatter_and_metadata(self) -> None:
        self.write_skill()
        errors: list[str] = []

        VALIDATOR.validate_skill_metadata(self.skill, errors)

        self.assertEqual(errors, [])

    def test_requires_folded_frontmatter_and_openai_metadata(self) -> None:
        self.write_skill(description_style="|", include_metadata=False)
        errors: list[str] = []

        VALIDATOR.validate_skill_metadata(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: frontmatter must use description: >-",
                "skills/example: missing agents/openai.yaml",
            ],
        )

    def test_rejects_missing_or_unquoted_metadata_fields(self) -> None:
        self.write_skill()
        (self.skill / "agents" / "openai.yaml").write_text(
            'interface:\n'
            '  display_name: Example\n'
            '  default_prompt: "Use $example for this task."\n',
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_skill_metadata(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/agents/openai.yaml: missing quoted display_name",
                "skills/example/agents/openai.yaml: missing quoted short_description",
            ],
        )

    def test_rejects_a_longer_invocation_token_with_the_skill_prefix(self) -> None:
        self.write_skill()
        metadata_file = self.skill / "agents" / "openai.yaml"
        metadata_file.write_text(
            metadata_file.read_text(encoding="utf-8").replace(
                "$example for", "$example-extended for"
            ),
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_skill_metadata(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/agents/openai.yaml: default_prompt must invoke $example"
            ],
        )


class SkillReadmeRequirementsTests(unittest.TestCase):
    def test_accepts_all_required_fragments(self) -> None:
        text = "\n".join(VALIDATOR.required_readme_fragments("example").values())
        errors: list[str] = []

        VALIDATOR.validate_required_readme_fragments("example", text, errors)

        self.assertEqual(errors, [])

    def test_requires_the_portable_dual_license_notice(self) -> None:
        fragments = VALIDATOR.required_readme_fragments("example")
        text = "\n".join(
            fragment
            for label, fragment in fragments.items()
            if label != "dual license notice"
        )
        errors: list[str] = []

        VALIDATOR.validate_required_readme_fragments("example", text, errors)

        self.assertEqual(
            errors,
            ["skills/example/README.md: missing dual license notice"],
        )


class FrontmatterValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.skill.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def write_skill(self, frontmatter: str) -> None:
        (self.skill / "SKILL.md").write_text(
            f"{frontmatter}\n# Example\n", encoding="utf-8"
        )

    def test_accepts_canonical_folded_frontmatter(self) -> None:
        self.write_skill(
            "---\nname: example\ndescription: >-\n  Example skill.\n  More detail.\n---"
        )
        errors: list[str] = []

        VALIDATOR.validate_frontmatter(self.skill, errors)

        self.assertEqual(errors, [])

    def test_folds_the_description_across_lines(self) -> None:
        parsed = VALIDATOR.parse_skill_frontmatter(
            "---\nname: example\ndescription: >-\n  One line.\n  Two lines.\n---\n"
        )

        self.assertEqual(
            parsed, {"name": "example", "description": "One line. Two lines."}
        )

    def test_rejects_extra_frontmatter_keys(self) -> None:
        self.write_skill(
            "---\nname: example\ndescription: >-\n  Example.\nlicense: MIT\n---"
        )
        errors: list[str] = []

        VALIDATOR.validate_frontmatter(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: frontmatter keys must be exactly "
                "['description', 'name']"
            ],
        )

    def test_rejects_a_name_that_does_not_match_the_directory(self) -> None:
        self.write_skill("---\nname: other\ndescription: >-\n  Example.\n---")
        errors: list[str] = []

        VALIDATOR.validate_frontmatter(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: frontmatter name 'other' "
                "must match the directory name 'example'"
            ],
        )

    def test_rejects_a_description_beyond_the_limit(self) -> None:
        long_line = "x" * 200
        folded_lines = "\n".join(f"  {long_line}" for _ in range(6))
        self.write_skill(f"---\nname: example\ndescription: >-\n{folded_lines}\n---")
        errors: list[str] = []

        VALIDATOR.validate_frontmatter(self.skill, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("description is 1205 characters", errors[0])

    def test_rejects_missing_frontmatter(self) -> None:
        self.write_skill("# No frontmatter")
        errors: list[str] = []

        VALIDATOR.validate_frontmatter(self.skill, errors)

        self.assertEqual(
            errors,
            ["skills/example/SKILL.md: missing or malformed YAML frontmatter"],
        )


class InlineCodeLinkExtractionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.root.joinpath("skills").mkdir()
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def test_ignores_markdown_links_inside_inline_code_spans(self) -> None:
        markdown = self.root / "README.md"
        markdown.write_text(
            "Use `[text](missing-inline.md)` literally and "
            "``[other](also-missing.md)`` too.\n",
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_local_links(markdown, errors)

        self.assertEqual(errors, [])

    def test_still_reports_real_missing_links(self) -> None:
        markdown = self.root / "README.md"
        markdown.write_text("A real [link](missing.md).\n", encoding="utf-8")
        errors: list[str] = []

        VALIDATOR.validate_local_links(markdown, errors)

        self.assertEqual(errors, ["README.md: missing missing.md"])


class NamedSectionReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name).resolve()
        self.root.joinpath("skills").mkdir()
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root
        VALIDATOR.heading_lines.cache_clear()

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        VALIDATOR.heading_lines.cache_clear()
        self.temporary_directory.cleanup()

    def check(self, markdown: Path) -> list[str]:
        errors: list[str] = []
        VALIDATOR.validate_named_section_references(markdown, errors)
        return errors

    def test_accepts_a_quoted_section_that_exists_in_the_target(self) -> None:
        self.root.joinpath("layout.md").write_text(
            "# Layout\n\n## Use Logical Properties\n", encoding="utf-8"
        )
        markdown = self.root / "nav.md"
        markdown.write_text(
            'See [layout](layout.md) ("Use Logical Properties") for the mapping.\n',
            encoding="utf-8",
        )

        self.assertEqual(self.check(markdown), [])

    def test_reports_a_quoted_section_missing_from_the_target(self) -> None:
        self.root.joinpath("route.md").write_text("# Route\n", encoding="utf-8")
        markdown = self.root / "nav.md"
        markdown.write_text(
            'See [route](route.md) (section "Use Container Queries").\n',
            encoding="utf-8",
        )

        self.assertEqual(
            self.check(markdown),
            ['nav.md:1: section "Use Container Queries" not found in route.md'],
        )

    def test_reports_a_relative_pointer_in_the_wrong_direction(self) -> None:
        markdown = self.root / "fundamentals.md"
        markdown.write_text(
            "### Product Motion Discipline\n\nText.\n\n"
            "Consistent with the Product Motion Discipline section below.\n",
            encoding="utf-8",
        )

        self.assertEqual(
            self.check(markdown),
            ['fundamentals.md:5: section "Product Motion Discipline" is above, not below'],
        )

    def test_ignores_relative_pointers_without_a_matching_heading(self) -> None:
        markdown = self.root / "notes.md"
        markdown.write_text(
            "# Notes\n\nSee the Pricing section below.\n", encoding="utf-8"
        )

        self.assertEqual(self.check(markdown), [])

    def test_ignores_pointers_inside_code(self) -> None:
        markdown = self.root / "notes.md"
        markdown.write_text(
            "## Setup\n\n```md\nSee the Setup section below.\n```\n"
            "Use `[x](missing.md) (\"Nope\")` literally.\n",
            encoding="utf-8",
        )

        self.assertEqual(self.check(markdown), [])


class IsolatedSkillRuntimeLinkTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.references = self.skill / "references"
        self.references.mkdir(parents=True)
        self.skill.joinpath("SKILL.md").write_text("# Example\n", encoding="utf-8")
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def test_accepts_links_within_an_isolated_skill_artifact(self) -> None:
        guide = self.references / "guide.md"
        guide.write_text("See [another section](other.md).\n", encoding="utf-8")
        self.references.joinpath("other.md").write_text("# Other\n", encoding="utf-8")
        errors: list[str] = []

        VALIDATOR.validate_isolated_skill_runtime_links(self.skill, errors)

        self.assertEqual(errors, [])

    def test_rejects_a_sibling_skill_link_from_a_reference(self) -> None:
        sibling = self.root / "skills" / "other"
        sibling.mkdir()
        sibling.joinpath("SKILL.md").write_text("# Other\n", encoding="utf-8")
        guide = self.references / "guide.md"
        guide.write_text("See [Other](../../other/SKILL.md).\n", encoding="utf-8")
        errors: list[str] = []

        VALIDATOR.validate_isolated_skill_runtime_links(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/references/guide.md: sibling-skill link "
                "../../other/SKILL.md; use inline `other` guidance instead"
            ],
        )

    def test_rejects_a_sibling_skill_link_from_skill_instructions(self) -> None:
        sibling = self.root / "skills" / "other"
        sibling.mkdir()
        sibling.joinpath("SKILL.md").write_text("# Other\n", encoding="utf-8")
        self.skill.joinpath("SKILL.md").write_text(
            "See [Other](../other/SKILL.md).\n", encoding="utf-8"
        )
        errors: list[str] = []

        VALIDATOR.validate_isolated_skill_runtime_links(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: sibling-skill link ../other/SKILL.md; "
                "use inline `other` guidance instead"
            ],
        )


class FirstPartySkillReferenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.references = self.skill / "references"
        self.references.mkdir(parents=True)
        self.other = self.root / "skills" / "other"
        self.other.mkdir()
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def test_accepts_a_first_party_routing_reference(self) -> None:
        self.skill.joinpath("SKILL.md").write_text(
            "# Example\n\n## Routing Boundaries\n\nRoute work to `other`.\n",
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_first_party_skill_references(
            self.skill, {"example", "other"}, errors
        )

        self.assertEqual(errors, [])

    def test_rejects_an_unknown_routing_reference(self) -> None:
        self.skill.joinpath("SKILL.md").write_text(
            "# Example\n\n## Routing Boundaries\n\nRoute work to `external-skill`.\n",
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_first_party_skill_references(
            self.skill, {"example", "other"}, errors
        )

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: named skill reference `external-skill` "
                "does not match a first-party skill directory"
            ],
        )

    def test_rejects_an_explicit_unknown_skill_in_a_reference(self) -> None:
        self.skill.joinpath("SKILL.md").write_text("# Example\n", encoding="utf-8")
        self.references.joinpath("guide.md").write_text(
            "Use the `external-skill` skill for the next step.\n",
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_first_party_skill_references(
            self.skill, {"example", "other"}, errors
        )

        self.assertEqual(
            errors,
            [
                "skills/example/references/guide.md: named skill reference "
                "`external-skill` does not match a first-party skill directory"
            ],
        )

    def test_ignores_inline_code_outside_routing_boundaries(self) -> None:
        self.skill.joinpath("SKILL.md").write_text(
            "Run `external-command` when needed.\n", encoding="utf-8"
        )
        errors: list[str] = []

        VALIDATOR.validate_first_party_skill_references(
            self.skill, {"example", "other"}, errors
        )

        self.assertEqual(errors, [])


class ReferenceOrphanTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        (self.skill / "references").mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def test_accepts_references_linked_from_the_skill(self) -> None:
        (self.skill / "references" / "guide.md").write_text("# Guide\n", encoding="utf-8")
        (self.skill / "SKILL.md").write_text(
            "See [Guide](references/guide.md).\n", encoding="utf-8"
        )
        errors: list[str] = []

        VALIDATOR.validate_reference_orphans(self.skill, errors)

        self.assertEqual(errors, [])

    def test_reports_an_unlinked_reference(self) -> None:
        (self.skill / "references" / "orphan.md").write_text("# Orphan\n", encoding="utf-8")
        (self.skill / "SKILL.md").write_text("No links here.\n", encoding="utf-8")
        errors: list[str] = []

        VALIDATOR.validate_reference_orphans(self.skill, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("skills/example/references/orphan.md: orphaned reference", errors[0])

    def test_a_self_link_does_not_satisfy_reachability(self) -> None:
        (self.skill / "references" / "loop.md").write_text(
            "See [myself](loop.md).\n", encoding="utf-8"
        )
        errors: list[str] = []

        VALIDATOR.validate_reference_orphans(self.skill, errors)

        self.assertEqual(len(errors), 1)
        self.assertIn("skills/example/references/loop.md: orphaned reference", errors[0])


class WorktreeSafetyUniquenessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.skills_root = Path(self.temporary_directory.name) / "skills"
        self.skills_root.mkdir()

    def tearDown(self) -> None:
        self.temporary_directory.cleanup()

    def write_contract(self, skill: str, content: str) -> None:
        references = self.skills_root / skill / "references"
        references.mkdir(parents=True)
        (references / "worktree-safety.md").write_text(content, encoding="utf-8")

    def test_accepts_the_single_shared_contract(self) -> None:
        self.write_contract("effective-delivery", "# Worktree Safety\n")
        errors: list[str] = []

        VALIDATOR.validate_worktree_safety_uniqueness(self.skills_root, errors)

        self.assertEqual(errors, [])

    def test_accepts_byte_identical_contracts(self) -> None:
        for skill in ("effective-delivery", "effective-engineering"):
            self.write_contract(skill, "# Worktree Safety\n\nShared contract.\n")
        errors: list[str] = []

        VALIDATOR.validate_worktree_safety_uniqueness(self.skills_root, errors)

        self.assertEqual(errors, [])

    def test_reports_divergent_contracts(self) -> None:
        self.write_contract("effective-delivery", "# Worktree Safety\n")
        self.write_contract("effective-engineering", "# Worktree Safety\n")
        self.write_contract("effective-web", "# Worktree Safety, but different\n")
        errors: list[str] = []

        VALIDATOR.validate_worktree_safety_uniqueness(self.skills_root, errors)

        self.assertEqual(
            errors,
            [
                "skills/effective-web/references/worktree-safety.md: "
                "must be byte-identical to "
                "skills/effective-delivery/references/worktree-safety.md"
            ],
        )


class SkillBodyConventionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.skill.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def test_accepts_canonical_boundary_and_line_limit(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "## Routing Boundaries\n"
            + "\n".join(["line"] * (VALIDATOR.SKILL_LINE_LIMIT - 1)),
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_skill_body_conventions(self.skill, errors)

        self.assertEqual(errors, [])

    def test_requires_the_exact_boundary_heading(self) -> None:
        (self.skill / "SKILL.md").write_text("## Boundaries\n", encoding="utf-8")
        errors: list[str] = []

        VALIDATOR.validate_skill_body_conventions(self.skill, errors)

        self.assertEqual(
            errors,
            ["skills/example/SKILL.md: missing exact '## Routing Boundaries' section"],
        )

    def test_rejects_a_skill_above_the_line_limit(self) -> None:
        (self.skill / "SKILL.md").write_text(
            "## Routing Boundaries\n"
            + "\n".join(["line"] * VALIDATOR.SKILL_LINE_LIMIT),
            encoding="utf-8",
        )
        errors: list[str] = []

        VALIDATOR.validate_skill_body_conventions(self.skill, errors)

        self.assertEqual(
            errors,
            [
                "skills/example/SKILL.md: 301 lines exceeds the 300-line limit; "
                "move detail into references/"
            ],
        )


class ReferenceContextBudgetTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary_directory.name)
        self.skill = self.root / "skills" / "example"
        self.references = self.skill / "references"
        self.references.mkdir(parents=True)
        self.original_root = VALIDATOR.REPOSITORY_ROOT
        VALIDATOR.REPOSITORY_ROOT = self.root

    def tearDown(self) -> None:
        VALIDATOR.REPOSITORY_ROOT = self.original_root
        self.temporary_directory.cleanup()

    def write_exception_registry(self, exceptions: object) -> None:
        docs = self.root / "docs"
        docs.mkdir()
        docs.joinpath("reference-context-exceptions.json").write_text(
            json.dumps({"version": 1, "exceptions": exceptions}),
            encoding="utf-8",
        )

    def write_registry(self, payload: dict[str, object]) -> None:
        docs = self.root / "docs"
        docs.mkdir(exist_ok=True)
        docs.joinpath("reference-context-exceptions.json").write_text(
            json.dumps(payload), encoding="utf-8"
        )

    def test_rejects_an_oversized_reference_without_a_reviewed_exception(self) -> None:
        reference = self.references / "guide.md"
        reference.write_text("\n".join(["line"] * 501), encoding="utf-8")
        errors: list[str] = []
        reports: list[str] = []

        VALIDATOR.validate_reference_context_budgets(
            self.skill, {}, {}, errors, reports
        )

        self.assertEqual(
            errors,
            [
                "skills/example/references/guide.md: 501 lines exceeds the 500-line "
                "reference limit; split it or register a reviewed context exception"
            ],
        )
        self.assertEqual(reports, [])

    def test_reports_a_documented_deep_reference_exception(self) -> None:
        reference = self.references / "guide.md"
        reference.write_text("\n".join(["line"] * 501), encoding="utf-8")
        errors: list[str] = []
        reports: list[str] = []
        exceptions = {
            "skills/example/references/guide.md": {
                "defaults": ["guide-core.md"],
                "reason": "A narrow module is the normal entry point.",
            }
        }

        VALIDATOR.validate_reference_context_budgets(
            self.skill, exceptions, {}, errors, reports
        )

        self.assertEqual(errors, [])
        self.assertEqual(
            reports,
            [
                "skills/example/references/guide.md: 501 lines (documented "
                "deep-reference exception; defaults: guide-core.md)"
            ],
        )

    def write_broad_route(self) -> None:
        self.references.joinpath("route-example.md").write_text(
            "[First](first.md)\n[Second](second.md)\n", encoding="utf-8"
        )
        self.references.joinpath("first.md").write_text(
            "\n".join(["line"] * 500), encoding="utf-8"
        )
        self.references.joinpath("second.md").write_text(
            "\n".join(["line"] * 500), encoding="utf-8"
        )

    def test_fails_an_unregistered_broad_route(self) -> None:
        self.write_broad_route()
        errors: list[str] = []
        reports: list[str] = []

        VALIDATOR.validate_reference_context_budgets(
            self.skill, {}, {}, errors, reports
        )

        self.assertEqual(
            errors,
            [
                "skills/example/references/route-example.md: 1000 direct-reference "
                "lines exceeds the 900-line advisory budget; make the route selection "
                "explicit or register a reviewed route context exception"
            ],
        )
        self.assertEqual(reports, [])

    def test_registered_route_without_a_ceiling_stays_advisory(self) -> None:
        self.write_broad_route()
        errors: list[str] = []
        reports: list[str] = []
        route_exceptions = {
            "skills/example/references/route-example.md": {
                "reason": "A broad router selected per task.",
            }
        }

        VALIDATOR.validate_reference_context_budgets(
            self.skill, {}, route_exceptions, errors, reports
        )

        self.assertEqual(errors, [])
        self.assertEqual(
            reports,
            [
                "skills/example/references/route-example.md: 1000 direct-reference "
                "lines (registered route exception, advisory limit 900)"
            ],
        )

    def test_registered_route_over_its_ceiling_fails(self) -> None:
        self.write_broad_route()
        errors: list[str] = []
        reports: list[str] = []
        route_exceptions = {
            "skills/example/references/route-example.md": {
                "reason": "Bounded router.",
                "ceiling": 950,
            }
        }

        VALIDATOR.validate_reference_context_budgets(
            self.skill, {}, route_exceptions, errors, reports
        )

        self.assertEqual(
            errors,
            [
                "skills/example/references/route-example.md: 1000 direct-reference "
                "lines exceeds its registered ceiling of 950; trim the route or "
                "raise the ceiling"
            ],
        )
        self.assertEqual(reports, [])

    def test_counts_nested_direct_references_in_a_route(self) -> None:
        nested = self.references / "guides"
        nested.mkdir()
        self.references.joinpath("route-example.md").write_text(
            "[First](guides/first.md)\n[Second](guides/second.md)\n",
            encoding="utf-8",
        )
        nested.joinpath("first.md").write_text(
            "\n".join(["line"] * 500), encoding="utf-8"
        )
        nested.joinpath("second.md").write_text(
            "\n".join(["line"] * 500), encoding="utf-8"
        )
        errors: list[str] = []
        reports: list[str] = []

        VALIDATOR.validate_reference_context_budgets(
            self.skill, {}, {}, errors, reports
        )

        self.assertEqual(
            errors,
            [
                "skills/example/references/route-example.md: 1000 direct-reference "
                "lines exceeds the 900-line advisory budget; make the route selection "
                "explicit or register a reviewed route context exception"
            ],
        )
        self.assertEqual(reports, [])

    def test_loads_only_a_complete_exception_registry(self) -> None:
        self.references.joinpath("guide.md").write_text(
            "\n".join(["line"] * 501), encoding="utf-8"
        )
        self.references.joinpath("guide-core.md").write_text("Core guide.\n", encoding="utf-8")
        self.write_exception_registry(
            {
                "skills/example/references/guide.md": {
                    "defaults": ["guide-core.md"],
                    "reason": "A narrow module is the normal entry point.",
                }
            }
        )
        errors: list[str] = []

        exceptions = VALIDATOR.load_reference_context_exceptions(errors)

        self.assertEqual(errors, [])
        self.assertEqual(
            exceptions["skills/example/references/guide.md"]["defaults"],
            ["guide-core.md"],
        )

    def test_rejects_an_incomplete_exception_registry_entry(self) -> None:
        self.write_exception_registry(
            {"skills/example/references/guide.md": {"reason": "Missing defaults."}}
        )
        errors: list[str] = []

        exceptions = VALIDATOR.load_reference_context_exceptions(errors)

        self.assertEqual(exceptions, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: exception "
                "'skills/example/references/guide.md' must contain defaults and reason"
            ],
        )

    def test_rejects_a_stale_exception(self) -> None:
        self.references.joinpath("guide.md").write_text("Short guide.\n", encoding="utf-8")
        self.write_exception_registry(
            {
                "skills/example/references/guide.md": {
                    "defaults": ["guide.md"],
                    "reason": "No longer needed.",
                }
            }
        )
        errors: list[str] = []

        exceptions = VALIDATOR.load_reference_context_exceptions(errors)

        self.assertEqual(exceptions, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: exception "
                "'skills/example/references/guide.md' no longer exceeds the "
                "500-line limit; remove it from the registry"
            ],
        )

    def test_loads_registered_route_exceptions(self) -> None:
        self.references.joinpath("route-example.md").write_text(
            "# Route\n", encoding="utf-8"
        )
        self.write_registry(
            {
                "version": 1,
                "exceptions": {},
                "routes": {
                    "skills/example/references/route-example.md": {
                        "reason": "A broad router selected per task.",
                        "ceiling": 1500,
                    }
                },
            }
        )
        errors: list[str] = []

        routes = VALIDATOR.load_route_context_exceptions(errors)

        self.assertEqual(errors, [])
        self.assertEqual(
            routes["skills/example/references/route-example.md"]["ceiling"], 1500
        )

    def test_accepts_the_full_registry_top_level_shape(self) -> None:
        self.references.joinpath("route-example.md").write_text(
            "# Route\n", encoding="utf-8"
        )
        self.write_registry(
            {
                "version": 1,
                "exceptions": {},
                "routes": {
                    "skills/example/references/route-example.md": {
                        "reason": "A broad router selected per task.",
                    }
                },
            }
        )
        errors: list[str] = []

        exceptions = VALIDATOR.load_reference_context_exceptions(errors)

        self.assertEqual(errors, [])
        self.assertEqual(exceptions, {})

    def test_rejects_a_route_without_a_reason(self) -> None:
        self.references.joinpath("route-example.md").write_text(
            "# Route\n", encoding="utf-8"
        )
        self.write_registry(
            {
                "version": 1,
                "exceptions": {},
                "routes": {
                    "skills/example/references/route-example.md": {"ceiling": 1500}
                },
            }
        )
        errors: list[str] = []

        routes = VALIDATOR.load_route_context_exceptions(errors)

        self.assertEqual(routes, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: route "
                "'skills/example/references/route-example.md' must contain a reason "
                "and may set a ceiling"
            ],
        )

    def test_rejects_a_route_ceiling_at_or_below_the_advisory_limit(self) -> None:
        self.references.joinpath("route-example.md").write_text(
            "# Route\n", encoding="utf-8"
        )
        self.write_registry(
            {
                "version": 1,
                "exceptions": {},
                "routes": {
                    "skills/example/references/route-example.md": {
                        "reason": "Bounded router.",
                        "ceiling": 900,
                    }
                },
            }
        )
        errors: list[str] = []

        routes = VALIDATOR.load_route_context_exceptions(errors)

        self.assertEqual(routes, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: route "
                "'skills/example/references/route-example.md' ceiling must be an "
                "integer above the 900-line advisory limit"
            ],
        )

    def test_rejects_a_route_that_names_a_missing_file(self) -> None:
        self.write_registry(
            {
                "version": 1,
                "exceptions": {},
                "routes": {
                    "skills/example/references/route-missing.md": {
                        "reason": "Points at nothing.",
                    }
                },
            }
        )
        errors: list[str] = []

        routes = VALIDATOR.load_route_context_exceptions(errors)

        self.assertEqual(routes, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: route "
                "'skills/example/references/route-missing.md' must name an existing "
                "Markdown route"
            ],
        )

    def test_rejects_a_missing_default_module(self) -> None:
        self.references.joinpath("guide.md").write_text(
            "\n".join(["line"] * 501), encoding="utf-8"
        )
        self.write_exception_registry(
            {
                "skills/example/references/guide.md": {
                    "defaults": ["missing-core.md"],
                    "reason": "A misspelled module must not bypass the budget.",
                }
            }
        )
        errors: list[str] = []

        exceptions = VALIDATOR.load_reference_context_exceptions(errors)

        self.assertEqual(exceptions, {})
        self.assertEqual(
            errors,
            [
                "docs/reference-context-exceptions.json: exception "
                "'skills/example/references/guide.md' default 'missing-core.md' must "
                "name a different existing Markdown reference in the same skill"
            ],
        )


if __name__ == "__main__":
    unittest.main()
