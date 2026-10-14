from __future__ import annotations

import importlib.util
import unittest
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "validate-site.py"
SPEC = importlib.util.spec_from_file_location("validate_site", MODULE_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Could not load {MODULE_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class JsonLdInventoryValidationTests(unittest.TestCase):
    inventory = [("one", "One"), ("two", "Two")]

    def test_missing_metadata_reports_a_failure_without_crashing(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_json_ld_inventory(None, self.inventory, failures)

        self.assertEqual(failures, ["site must include JSON-LD metadata"])

    def test_mismatched_items_report_a_failure(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [{"name": "One"}, {"name": "Two"}],
            }
        }

        VALIDATOR.validate_json_ld_inventory(json_ld, self.inventory, failures)

        self.assertEqual(
            failures,
            [
                "JSON-LD skill items must match visible skill cards in order, "
                "name, position, and URL"
            ],
        )

    def test_matching_inventory_passes(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "One",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}one/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Two",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}two/",
                    },
                ],
            }
        }

        VALIDATOR.validate_json_ld_inventory(json_ld, self.inventory, failures)

        self.assertEqual(failures, [])

    def test_rejects_an_order_or_position_mismatch(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "Two",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}two/",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "One",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}one/",
                    },
                ],
            }
        }

        VALIDATOR.validate_json_ld_inventory(json_ld, self.inventory, failures)

        self.assertEqual(
            failures,
            [
                "JSON-LD skill items must match visible skill cards in order, "
                "name, position, and URL"
            ],
        )

    def test_accepts_additional_valid_list_item_properties(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "One",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}one/",
                        "description": "An optional Schema.org property.",
                    },
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Two",
                        "url": f"{VALIDATOR.SKILL_URL_PREFIX}two/",
                    },
                ],
            }
        }

        VALIDATOR.validate_json_ld_inventory(json_ld, self.inventory, failures)

        self.assertEqual(failures, [])


class VisibleSkillInventoryTests(unittest.TestCase):
    def test_reads_index_row_order_and_display_name(self) -> None:
        html = (
            '<tr data-skill="one" data-stage="decide"><td>Decide</td>'
            '<th class="guide-name" scope="row"><a href="one/">One &amp; Only</a><small>1 routes · 2 references</small></th></tr>'
            '<tr data-skill="two"><th class="guide-name"><a href="two/">Two</a></th></tr>'
        )

        self.assertEqual(
            VALIDATOR.visible_skill_inventory(html),
            [("one", "One & Only"), ("two", "Two")],
        )

    def test_accepts_single_quoted_skill_attributes(self) -> None:
        html = "<tr data-skill='one'><th class=\"guide-name\"><a href='one/'>One</a></th></tr>"

        self.assertEqual(VALIDATOR.visible_skill_inventory(html), [("one", "One")])


class SkillCardStructureValidationTests(unittest.TestCase):
    def test_accepts_balanced_sibling_skill_cards(self) -> None:
        parser = VALIDATOR.SiteParser()
        parser.feed(
            '<article data-skill="one"></article>'
            '<article data-skill="two"></article>'
        )
        failures: list[str] = []

        VALIDATOR.validate_skill_card_structure(parser, failures)

        self.assertEqual(failures, [])

    def test_rejects_nested_and_unclosed_skill_cards(self) -> None:
        parser = VALIDATOR.SiteParser()
        parser.feed(
            '<article data-skill="one">'
            '<article data-skill="two"></article>'
        )
        failures: list[str] = []

        VALIDATOR.validate_skill_card_structure(parser, failures)

        self.assertEqual(
            failures,
            [
                "site skill cards must not be nested inside other skill cards",
                "every site skill-card article must have a closing tag",
            ],
        )


class InstallCommandValidationTests(unittest.TestCase):
    def validate_commands(
        self,
        managed_commands: tuple[str, ...] = VALIDATOR.EXPECTED_DALO_COMMANDS,
        optional_commands: tuple[str, ...] = VALIDATOR.EXPECTED_OPTIONAL_INSTRUCTION_COMMANDS,
        disclosure: bool = True,
    ) -> list[str]:
        parser = VALIDATOR.SiteParser()
        optional_html = (
            '<code id="optional-instructions-command">'
            + "\n".join(optional_commands)
            + "</code>"
        )
        if disclosure:
            optional_html = (
                "<details><summary>Optional instructions</summary><div>"
                + optional_html
                + "</div></details>"
            )
        parser.feed(
            '<code id="dalo-command">'
            + "\n".join(managed_commands)
            + "</code>"
            + optional_html
        )
        failures: list[str] = []
        VALIDATOR.validate_install_commands(parser, failures)
        return failures

    def test_accepts_separate_optional_pack_activation(self) -> None:
        self.assertEqual(self.validate_commands(), [])

    def test_rejects_pack_activation_in_the_default_install_even_if_optional_is_present(self) -> None:
        failures = self.validate_commands(
            managed_commands=(
                *VALIDATOR.EXPECTED_DALO_COMMANDS,
                VALIDATOR.EXPECTED_OPTIONAL_INSTRUCTION_COMMANDS[0],
            )
        )
        self.assertIn(
            "managed skill install must not activate optional instruction packs", failures
        )

    def test_requires_managed_commands_in_the_managed_block(self) -> None:
        misplaced = VALIDATOR.EXPECTED_DALO_COMMANDS[-1]
        failures = self.validate_commands(
            managed_commands=VALIDATOR.EXPECTED_DALO_COMMANDS[:-1],
            optional_commands=(
                *VALIDATOR.EXPECTED_OPTIONAL_INSTRUCTION_COMMANDS,
                misplaced,
            ),
        )
        self.assertIn(
            f"managed install block is missing DALO command: {misplaced}", failures
        )

    def test_requires_both_optional_pack_commands(self) -> None:
        failures = self.validate_commands(
            optional_commands=VALIDATOR.EXPECTED_OPTIONAL_INSTRUCTION_COMMANDS[:1]
        )
        self.assertIn(
            "optional instruction block is missing DALO command: "
            + VALIDATOR.EXPECTED_OPTIONAL_INSTRUCTION_COMMANDS[1],
            failures,
        )

    def test_requires_a_disclosure_for_optional_instructions(self) -> None:
        self.assertIn(
            "optional instruction commands must be inside a details disclosure",
            self.validate_commands(disclosure=False),
        )


class ComparisonInventoryValidationTests(unittest.TestCase):
    inventory = [
        ("one/skills", "https://github.com/one/skills"),
        ("two/tool", "https://github.com/two/tool"),
    ]

    def test_reads_visible_comparison_name_and_source(self) -> None:
        html = """
        <article class="comparison-card reveal">
          <h3>one/skills</h3>
          <a href="https://github.com/one/skills">Inspect source <span>↗</span></a>
        </article>
        """

        self.assertEqual(
            VALIDATOR.visible_comparison_inventory(html),
            [self.inventory[0]],
        )

    def test_matching_comparison_metadata_passes(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": position,
                        "name": name,
                        "url": url,
                    }
                    for position, (name, url) in enumerate(self.inventory, start=1)
                ],
            }
        }

        VALIDATOR.validate_comparison_json_ld(json_ld, self.inventory, failures)

        self.assertEqual(failures, [])

    def test_rejects_duplicate_or_misplaced_comparison_item(self) -> None:
        failures: list[str] = []
        json_ld = {
            "mainEntity": {
                "numberOfItems": 2,
                "itemListElement": [
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "one/skills",
                        "url": "https://github.com/one/skills",
                    },
                    {
                        "@type": "ListItem",
                        "position": 1,
                        "name": "one/skills",
                        "url": "https://github.com/one/skills",
                    },
                ],
            }
        }

        VALIDATOR.validate_comparison_json_ld(json_ld, self.inventory, failures)

        self.assertEqual(
            failures,
            [
                "comparison JSON-LD items must match visible cards in order, "
                "name, position, and URL"
            ],
        )


class ProofRowValuesTests(unittest.TestCase):
    def test_reads_values_from_dd_elements(self) -> None:
        html = (
            '<dl class="proof-row" aria-label="Collection facts">'
            "<div><dt>practice-built skills</dt><dd>20</dd></div>"
            "<div><dt>focused references</dt><dd>184</dd></div>"
            "<div><dt>connected quality system</dt><dd>1</dd></div>"
            "</dl>"
        )

        self.assertEqual(VALIDATOR.proof_row_values(html), [20, 184, 1])


class GuideIndexStatsValidationTests(unittest.TestCase):
    @staticmethod
    def row(routes: int, references: int) -> str:
        return (
            '<tr data-skill="effective-web" data-stage="build">'
            '<th class="guide-name"><a href="skills/effective-web/index.html">Effective Web</a>'
            f"<small>{routes} routes · {references} references</small></th></tr>"
        )

    def test_matching_stats_pass(self) -> None:
        routes, references = VALIDATOR.skill_inventory("effective-web")
        failures: list[str] = []

        VALIDATOR.validate_guide_index_stats(self.row(routes, references), ["effective-web"], failures)

        self.assertEqual(failures, [])

    def test_stale_stats_report_the_expected_counts(self) -> None:
        routes, references = VALIDATOR.skill_inventory("effective-web")
        failures: list[str] = []

        VALIDATOR.validate_guide_index_stats(self.row(routes + 1, references), ["effective-web"], failures)

        self.assertEqual(
            failures,
            [f"effective-web index row must show {routes} routes · {references} references"],
        )

    def test_missing_row_reports_a_failure(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_guide_index_stats("<main></main>", ["effective-web"], failures)

        self.assertEqual(len(failures), 1)

    def test_inventory_counts_agree_with_the_repository(self) -> None:
        routes, references = VALIDATOR.skill_inventory("effective-web")

        self.assertGreater(routes, 0)
        self.assertGreaterEqual(references, routes)
        self.assertGreater(VALIDATOR.scenario_count(), 0)


class SitemapLastmodValidationTests(unittest.TestCase):
    def test_matching_lastmod_passes(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_sitemap_lastmod(
            "<lastmod>2026-07-17</lastmod>",
            "2026-07-17",
            failures,
        )

        self.assertEqual(failures, [])

    def test_stale_lastmod_reports_latest_site_date(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_sitemap_lastmod(
            "<lastmod>2026-07-16</lastmod>",
            "2026-07-17",
            failures,
        )

        self.assertEqual(
            failures,
            ["sitemap lastmod must match the latest site change: 2026-07-17"],
        )


class ComparisonReviewFreshnessTests(unittest.TestCase):
    sitemap = (
        "<url><loc>https://effective-agent.dev/</loc>"
        "<lastmod>2026-07-23</lastmod></url>"
        "<url><loc>https://effective-agent.dev/comparisons.html</loc>"
        "<lastmod>2026-07-23</lastmod></url>"
    )

    def test_same_day_review_and_lastmod_pass(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_comparison_review_freshness(
            '<p class="eyebrow">Field notes · reviewed 23 July 2026</p>',
            self.sitemap,
            failures,
        )

        self.assertEqual(failures, [])

    def test_review_within_the_window_passes(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_comparison_review_freshness(
            "reviewed 1 May 2026",
            self.sitemap,
            failures,
        )

        self.assertEqual(failures, [])

    def test_stale_review_fails_against_the_page_lastmod(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_comparison_review_freshness(
            "reviewed 1 January 2026",
            self.sitemap,
            failures,
        )

        self.assertEqual(len(failures), 1)
        self.assertIn("comparison review date 2026-01-01 is 203 days older", failures[0])

    def test_missing_review_date_reports_a_failure(self) -> None:
        failures: list[str] = []

        VALIDATOR.validate_comparison_review_freshness(
            "<p>No date here.</p>",
            self.sitemap,
            failures,
        )

        self.assertIn("comparison page must state its review date", failures)

    def test_uses_the_comparison_page_lastmod_not_the_homepage(self) -> None:
        sitemap = (
            "<url><loc>https://effective-agent.dev/</loc>"
            "<lastmod>2026-12-31</lastmod></url>"
            "<url><loc>https://effective-agent.dev/comparisons.html</loc>"
            "<lastmod>2026-07-23</lastmod></url>"
        )
        failures: list[str] = []

        VALIDATOR.validate_comparison_review_freshness(
            "reviewed 23 July 2026", sitemap, failures
        )

        self.assertEqual(failures, [])




class NestedPageLinkTests(unittest.TestCase):
    def test_resolves_parent_links_and_cross_page_fragments(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            page = root / "skills" / "web" / "index.html"
            page.parent.mkdir(parents=True)
            page.write_text('<h1 id="title">Web</h1>')
            (root / "index.html").write_text('<section id="library">Skills</section>')
            (root / "styles.css").write_text("body {}")
            parser = VALIDATOR.SiteParser()
            parser.feed('<a href="../../index.html#library">All skills</a>'
                        '<a href="#title">Title</a>'
                        '<link rel="stylesheet" href="../../styles.css">')
            failures = []
            VALIDATOR.validate_page_links(page, parser, failures)
            self.assertEqual(failures, [])

    def test_reports_missing_cross_page_fragment_and_nested_asset(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            page = Path(directory) / "index.html"
            page.write_text('<h1 id="title">Web</h1>')
            sibling = Path(directory) / "other.html"
            sibling.write_text('<h1 id="other">Other</h1>')
            parser = VALIDATOR.SiteParser()
            parser.feed('<a href="other.html#missing">Other</a>'
                        '<link rel="stylesheet" href="missing.css">')
            failures = []
            VALIDATOR.validate_page_links(page, parser, failures)
            self.assertEqual(len(failures), 2)
            self.assertTrue(any("missing fragment" in failure for failure in failures))
            self.assertTrue(any("missing asset" in failure for failure in failures))

if __name__ == "__main__":
    unittest.main()
