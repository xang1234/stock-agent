import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
REGISTRY_PATH = ROOT / "spec" / "finance_research_tool_registry.json"


class ToolRegistryContractTest(unittest.TestCase):
    def test_spec_declares_bundle_audience_and_side_effect_rules(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 9.1 Tool registry and bundle rules", spec_text)
        self.assertIn(
            "`spec/finance_research_tool_registry.json` is the normative artifact for bundle membership, tool audience, approval sensitivity, and JSON-schema-constrained inputs and outputs.",
            spec_text,
        )
        self.assertIn(
            "Tools are backend data and action surfaces; `Block[]` remains the response artifact contract.",
            spec_text,
        )
        self.assertIn(
            "`reader` tools are the only tools allowed to access raw untrusted text or raw documents.",
            spec_text,
        )
        self.assertIn(
            "Raw text must not leak into analyst-facing tools.",
            spec_text,
        )
        self.assertIn(
            "Approval-sensitive tools today are `create_alert` and `create_agent`.",
            spec_text,
        )
        self.assertIn("### 9.2 Downstream consumer rules for tool runtime", spec_text)
        self.assertIn(
            "Pre-resolve routing and budget policy (`P2.2`) depends on deterministic bundle selection, audience separation, and registry metadata before the analyst loop starts.",
            spec_text,
        )
        self.assertIn(
            "Document ingestion and extraction (`P3.2`) depends on raw document search, fetch, and extraction tools belonging to the `reader` audience.",
            spec_text,
        )
        self.assertIn(
            "Alerting and automation (`P5.1`) depends on side-effect categories and approval sensitivity so create and update flows do not execute directly from model output.",
            spec_text,
        )
        self.assertIn(
            "Tool runtime and orchestration (`PX.2`) depends on bundle membership, audience, `read_only`, `approval_required`, `cost_class`, and `freshness_expectation`.",
            spec_text,
        )

    def test_registry_declares_bundle_groups_and_design_rules(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text())

        self.assertEqual(
            registry["description"],
            "Normative tool registry for reader and analyst bundles. Tools are backend data and action surfaces; Block[] is the separate response artifact contract.",
        )
        self.assertIn(
            "System selects tool bundle; model selects tools within the bundle.",
            registry["design_rules"],
        )
        self.assertIn(
            "Reader-only tools may access raw untrusted content; analyst-facing tools may not.",
            registry["design_rules"],
        )
        self.assertIn(
            "Non-read-only tools remain write-intent policy boundaries even when approval_required is false.",
            registry["design_rules"],
        )
        self.assertEqual(
            [bundle["bundle_id"] for bundle in registry["bundles"]],
            [
                "quote_lookup",
                "single_subject_analysis",
                "peer_comparison",
                "theme_research",
                "segment_deep_dive",
                "document_research",
                "filing_research",
                "screener",
                "agent_management",
                "alert_management",
                "analyze_template_run",
            ],
        )

    def test_registry_preserves_reader_boundary_and_write_intent_categories(self) -> None:
        registry = json.loads(REGISTRY_PATH.read_text())
        tools = {tool["name"]: tool for tool in registry["tools"]}

        reader_tools = {
            name for name, tool in tools.items() if tool["audience"] == "reader"
        }
        self.assertEqual(
            reader_tools,
            {
                "search_raw_documents",
                "fetch_raw_document",
                "extract_mentions",
                "extract_claims",
                "extract_candidate_facts",
                "extract_events",
                "classify_sentiment",
            },
        )
        for tool_name in reader_tools:
            self.assertTrue(tools[tool_name]["read_only"], msg=tool_name)

        self.assertEqual(
            tools["search_raw_documents"]["description"],
            "Reader-only raw document search surface for untrusted text retrieval before extraction.",
        )
        self.assertEqual(
            tools["fetch_raw_document"]["description"],
            "Reader-only raw document fetch surface for parsing or extraction.",
        )

        self.assertEqual(
            {name for name, tool in tools.items() if tool["approval_required"]},
            {"create_alert", "create_agent"},
        )
        self.assertEqual(
            {name for name, tool in tools.items() if not tool["read_only"]},
            {"create_alert", "add_to_watchlist", "create_agent"},
        )
        self.assertEqual(
            tools["create_alert"]["description"],
            "Approval-sensitive write-intent tool that returns a pending action until orchestration or the user confirms it.",
        )
        self.assertEqual(
            tools["add_to_watchlist"]["description"],
            "Write-intent tool that may be auto-approved by policy but remains a policy boundary.",
        )
        self.assertEqual(
            tools["create_agent"]["description"],
            "Approval-sensitive write-intent tool that returns a pending action until explicit approval.",
        )


if __name__ == "__main__":
    unittest.main()
