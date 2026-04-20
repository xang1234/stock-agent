from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
SCHEMA_PATH = ROOT / "spec" / "finance_research_block_schema.json"


class BlockSchemaContractTest(unittest.TestCase):
    def test_spec_declares_block_bindings_and_consumers(self) -> None:
        spec_text = SPEC_PATH.read_text()
        self.assertIn("### 8.1 Block schema contract and render rules", spec_text)
        self.assertIn(
            "Every block kind inherits the `BaseBlock` contract: `id`, `kind`, `snapshot_id`, `data_ref`, `source_refs`, and `as_of`.",
            spec_text,
        )
        self.assertIn("The canonical schema field is `data_ref`.", spec_text)
        self.assertIn(
            "Earlier analysis used `dataRef` or `queryRef`; the schema standardizes this as `data_ref`.",
            spec_text,
        )
        self.assertIn(
            "`Sources` is the required provenance surface whenever external evidence appears in the answer.",
            spec_text,
        )
        self.assertIn("### 8.2 Downstream consumer rules for block artifacts", spec_text)
        self.assertIn(
            "Thread coordinator and transport (`P2.1`) consumes `Block[]` as the streamed and persisted assistant payload.",
            spec_text,
        )
        self.assertIn(
            "Frontend renderer (`PX.3`) consumes `Block[]` via a shared `BlockRegistry` and must not treat rendering as a tool invocation.",
            spec_text,
        )

    def test_schema_describes_typed_response_boundary(self) -> None:
        schema_text = SCHEMA_PATH.read_text()
        self.assertIn(
            "Typed assistant-response schema for structured Block[] artifacts rendered by Chat, Analyze, and findings surfaces.",
            schema_text,
        )
        self.assertIn(
            "Canonical backend binding for a block. Historical dataRef/queryRef language maps to data_ref in this schema.",
            schema_text,
        )
        self.assertIn(
            "Shared render, audit, provenance, and snapshot binding fields for every block.",
            schema_text,
        )
        self.assertIn(
            "Provenance block required whenever external evidence appears in the answer.",
            schema_text,
        )
        self.assertIn(
            "Disclosure block for trust and compliance notes; orchestration may inject it.",
            schema_text,
        )


if __name__ == "__main__":
    unittest.main()
