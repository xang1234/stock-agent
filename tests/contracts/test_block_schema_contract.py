import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "spec" / "finance_research_spec.md"
SCHEMA_PATH = ROOT / "spec" / "finance_research_block_schema.json"
OPENAPI_PATH = ROOT / "spec" / "finance_research_openapi.yaml"


def _yaml_section(text: str, section_name: str) -> str:
    lines = text.splitlines()
    header = f"    {section_name}:"
    for start, line in enumerate(lines):
        if line == header:
            section_lines = [line]
            for following in lines[start + 1 :]:
                if following.startswith("    ") and not following.startswith("      "):
                    break
                section_lines.append(following)
            return "\n".join(section_lines) + "\n"
    raise AssertionError(f"Section {section_name!r} not found")


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

    def test_openapi_block_envelope_uses_typed_block_schema(self) -> None:
        openapi_text = OPENAPI_PATH.read_text()
        block_envelope = _yaml_section(openapi_text, "BlockEnvelope")
        self.assertIn("      properties:\n", block_envelope)
        self.assertIn("        blocks:\n", block_envelope)
        self.assertIn("          type: array\n", block_envelope)
        self.assertIn(
            "            $ref: './finance_research_block_schema.json#/$defs/Block'\n",
            block_envelope,
        )

        subject_ref = _yaml_section(openapi_text, "SubjectRef")
        self.assertEqual(
            subject_ref,
            "    SubjectRef:\n"
            "      $ref: './finance_research_block_schema.json#/$defs/SubjectRef'\n",
        )

    def test_schema_subject_refs_and_closed_variants(self) -> None:
        schema = json.loads(SCHEMA_PATH.read_text())
        defs = schema["$defs"]

        self.assertIn("SubjectKind", defs)
        self.assertIn("SubjectRef", defs)

        subject_ref = defs["SubjectRef"]
        self.assertEqual(subject_ref["type"], "object")
        self.assertEqual(subject_ref["properties"]["kind"]["$ref"], "#/$defs/SubjectKind")
        self.assertEqual(subject_ref["required"], ["kind", "id"])
        self.assertFalse(subject_ref["additionalProperties"])

        for block_name, field_name in (
            ("PerfComparison", "subject_refs"),
            ("MetricsComparison", "subjects"),
            ("FindingCard", "subject_refs"),
        ):
            variant = defs[block_name]["allOf"][1]
            items = variant["properties"][field_name]["items"]
            self.assertEqual(items, {"$ref": "#/$defs/SubjectRef"})

        self.assertNotEqual(defs["BaseBlock"].get("additionalProperties"), True)

        closed_variants = {
            name: definition["allOf"][1]
            for name, definition in defs.items()
            if isinstance(definition, dict)
            and isinstance(definition.get("allOf"), list)
            and len(definition["allOf"]) == 2
            and definition["allOf"][0] == {"$ref": "#/$defs/BaseBlock"}
        }
        self.assertGreater(len(closed_variants), 0)
        for block_name, variant in closed_variants.items():
            self.assertIn(
                "unevaluatedProperties",
                variant,
                msg=f"{block_name} must declare unevaluatedProperties",
            )
            self.assertIs(
                variant["unevaluatedProperties"],
                False,
                msg=f"{block_name} must reject unexpected top-level properties",
            )


if __name__ == "__main__":
    unittest.main()
